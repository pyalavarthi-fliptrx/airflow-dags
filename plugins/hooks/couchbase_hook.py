import _pickle as pickle
from contextlib import contextmanager
from datetime import timedelta
from functools import cached_property, lru_cache
import logging
from multiprocessing import Process, ProcessError, Value
import warnings
import tenacity

from airflow.exceptions import AirflowException
from airflow.hooks.dbapi_hook import DbApiHook
from couchbase.cluster import Cluster, PasswordAuthenticator, ClusterOptions, \
    ClusterTimeoutOptions, QueryOptions
from couchbase_core.n1ql import NOT_BOUNDED
from couchbase.exceptions import CouchbaseTransientException, TimeoutException
import couchbase.subdocument as SD

KILOBYTES_PER_UPSERT = 32 * 1024
MEGABYTES_PER_BATCH = 72 * 1024 * 1024
TIME_TO_RETRY_IN_SECS = 60
SLEEP_TIME_BETWEEN_RETRIES_IN_SECS = 5


class UpsertBatch(object):
    """
    UpsertBatch uses multiprocessing due to memory leak/buildup in multi_upsert of Couchbase
    python SDK. Current bytes per upsert which is 32 bytes, causes memory build up of around
    18 MB for each upsert. Keeping the record limit of 72 MB per batch limits the memory usage by
    Couchbase multi_upsert to upto 500-600 MB per process. Here, 72 MB refers to the size of
    serialized records through pickling.
    As the design uses per process at a time and waits for the process/batch to end before starting
    the next, maximum memory usage by this module may not go beyond 500-600 MB at any time for the
    current default limit of 72 MB.
    """
    @classmethod
    def pickle_length(cls, batch):
        return len(pickle.dumps(batch))

    def __init__(self, bucket):
        self._bucket = bucket
        self._batch = {}
        self._batch_count = 0
        #  multiprocessing shared variable to keep track of number of records across
        #  batches/processes
        self._num_completed = Value('i', 0)
        self._kilobytes_per_upsert = KILOBYTES_PER_UPSERT

    def _get_size_of_random_record(self):
        for key, doc in self._batch.items():
            return self.pickle_length({key: doc})

    def add(self, docs):
        self._batch.update(docs)
        #  As pickling is expensive for large number of records, a random record is picked and its
        #  size is calculated, which is extrapolated to all the records in the batch.
        per_record_size = self._get_size_of_random_record()
        if per_record_size and len(self._batch) >= MEGABYTES_PER_BATCH / per_record_size:
            self.spawn_subprocess_and_process_batch()
            self._batch.clear()

    def spawn_subprocess_and_process_batch(self):
        process = Process(target=self._process_batch, args=(self._batch,))
        process.start()
        #  Wait for the process to finish before starting the next batch, to limit memory
        process.join()
        #  We want to exit the parent process when any child process has failed due to some
        #  exception that is not due to timeout, as we don't retry a particular batch that failed
        #  due to unknown exception
        if process.exitcode != 0:
            raise ProcessError("Child process exited with exception!!!")
        else:
            self._batch_count += 1
            logging.info(f"Processed {self._num_completed.value} documents "
                         f"until batch {self._batch_count}")

    def _process_batch(self, batch):
        local_batch = {}
        for key, doc in batch.items():
            local_batch.update({key: doc})
            if self.pickle_length(local_batch) > self._kilobytes_per_upsert:
                self._upsert_single_kbytes_batch(local_batch)
                local_batch.clear()
        self._upsert_single_kbytes_batch(local_batch)

    def _upsert_single_kbytes_batch(self, batch):
        if not batch:
            return
        try:
            #  Turn off warning messages printed by upsert_multi
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self._bucket.upsert_multi(batch)
            self._num_completed.value += len(batch)
        except (CouchbaseTransientException, TimeoutException) as e:
            self._process_failure(e.split_results(), batch)

    def _process_failure(self, error_results, current_batch):
        (success_entry, failed_entry) = error_results
        batch = {key: current_batch[key] for key in failed_entry}
        self._num_completed.value += len(success_entry)
        self._process_batch(batch)


class CouchbaseHook(DbApiHook):
    conn_name_attr = 'couchbase_connection'
    default_conn_name = conn_name_attr

    def __init__(
            self, *args, query_timeout=600,
            scan_consistency=NOT_BOUNDED, collection=None, **kwargs):
        self.collection = collection
        self.query_timeout = query_timeout
        self.scan_consistency = scan_consistency
        super(CouchbaseHook, self).__init__(*args, **kwargs)

    @lru_cache
    def get_collection(self, is_retry=False):
        try:
            collection = self._cluster.bucket(self._connection.schema).default_collection()
            if is_retry:
                logging.info("Reconnected to couchbase")
            return collection
        except TimeoutException:
            logging.warning("Couchbase connection failed. Retrying connecting to couchbase...")
            return self.get_collection(is_retry=True)

    @cached_property
    def _connection(self):
        return self.get_connection(CouchbaseHook.conn_name_attr)

    @cached_property
    def _cluster(self):
        connection = self._connection
        if not connection:
            raise AirflowException('Missing either connection or bucket from the connection')
        authenticator = PasswordAuthenticator(connection.login, connection.password)
        timeout_options = ClusterTimeoutOptions(
            kv_timeout=timedelta(seconds=15), query_timeout=timedelta(seconds=self.query_timeout))
        return Cluster(connection.host, ClusterOptions(
            authenticator, timeout_options=timeout_options))

    @cached_property
    def _cluster_bucket(self):
        return self._cluster.bucket(self._connection.schema)

    def run(self, sql, *_):
        cluster = self._cluster_bucket
        query = sql.format(bucket=self._connection.schema)
        return cluster.query(query, QueryOptions(scan_consistency=self.scan_consistency))

    def run_with_retry(self, sql, *_):
        self._retrier = tenacity.Retrying(
            stop=tenacity.stop_after_delay(TIME_TO_RETRY_IN_SECS),
            wait=tenacity.wait_fixed(SLEEP_TIME_BETWEEN_RETRIES_IN_SECS),
            reraise=True
        )
        return self._retrier(self.run, sql, *_)

    def run_mutation(self, sql, *_):
        return self.run(sql).execute()

    def upsert_dict_to_cb(self, doc_id, data_dict):
        bucket = self.get_collection()
        return bucket.upsert(doc_id, data_dict)

    @staticmethod
    def get_document_name(sql):
        tokenized = sql.split()
        token = [item for item in tokenized if 'type' in item][0].split('=')[1]
        return token.replace('"', '')

    def get_records(self, sql, coverter=None):
        query_result = self.run_with_retry(sql)
        for result in query_result:
            data = CouchbaseHook.parse_result(result, self._connection.schema)
            if coverter is not None:
                data = coverter(data)
            yield data

    def get_records_with_id(self, sql, coverter=None):
        for _dict in self.get_records(sql, coverter=coverter):
            for id, doc in _dict.items():
                yield id, doc

    def get(self, key, quiet=True):
        result = self.get_collection().get(key, quiet=quiet)
        if result:
            return result.content

    def remove_key(self, key):
        self.get_collection().remove(key)

    def get_counter(self, key, delta=1, initial=1):
        return self.get_collection().counter(key, delta, initial=initial).value

    @classmethod
    def parse_result(cls, doc, bucket):
        if bucket not in doc:
            return doc
        if 'id' in doc:
            return {doc['id']: doc[bucket]}
        return doc[bucket]

    @contextmanager
    def batch_upserter(self):
        logging.info("Started to upsert documents in batches...")
        upsert_batch = UpsertBatch(self.get_collection())
        yield upsert_batch
        upsert_batch.spawn_subprocess_and_process_batch()
        logging.info(f"Completed processing {upsert_batch._num_completed.value} documents through "
                     f"Batch Upsert")

    def patch(self, key, updates):
        mutations = [SD.upsert(key, value) for key, value in updates.items()]
        return self.get_collection().mutate_in(key, mutations)

    def get_paginated_records(self, query, page_size, coverter=None):
        """
            Returns a generator that will iterate over all the records in a paginated manner.
            Use order by in your query to get paginated records
        """
        page_num = 0
        while True:
            offset_query = f" OFFSET {page_size * page_num} LIMIT {page_size};"""
            paginated_query = query + offset_query
            records = list(self.get_records(paginated_query, coverter=coverter))
            if not records:
                return
            yield from records
            page_num += 1
