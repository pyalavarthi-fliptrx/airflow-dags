from airflow.models.baseoperator import BaseOperator
from airflow.hooks.S3_hook import S3Hook
from airflow.utils.decorators import apply_defaults
from dags.Integration.plugins.hooks.couchbase_hook import CouchbaseHook
from tempfile import NamedTemporaryFile
import logging as log
import json

class CouchbaseOperator(BaseOperator):
    template_fields = ('query', 'dest_s3_key')

    @apply_defaults
    def __init__(self, query, dest_s3_key,  page_size=0, converter=None, *args, **kwargs):
        super(CouchbaseOperator, self).__init__(*args, **kwargs)
        self.query = query
        self.dest_s3_key = dest_s3_key
        self._page_size = page_size
        self._converter = converter

    def execute(self, context):
        cb_hook = CouchbaseHook(context)
        queries = self.render_template(self.query, context).split(";")
        s3_key = self.render_template(self.dest_s3_key, context)
        dest_s3 = S3Hook(aws_conn_id='aws_default', verify=True)
        log.info(self.dest_s3_key)
        with NamedTemporaryFile("w") as f_dest:
            if self._page_size == 0:
                for qry in queries:
                    for doc in cb_hook.get_records(qry, self._converter):
                        f_dest.write(json.dumps(doc)+"\n")
            else:
                for qry in queries:
                    for doc in cb_hook.get_paginated_records(qry, self._page_size, self._converter):
                        f_dest.write(json.dumps(doc)+"\n")

            f_dest.flush()
            dest_s3.load_file(
                filename=f_dest.name,
                key=self.dest_s3_key,
                replace=True
            )