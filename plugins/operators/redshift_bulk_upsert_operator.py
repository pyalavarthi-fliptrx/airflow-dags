from airflow.providers.postgres.hooks.postgres import PostgresHook
from dags.Integration.plugins.hooks.flipt_s3_hook import FliptS3Hook
from airflow.models.baseoperator import BaseOperator
from airflow.models import Variable
from json import loads
import os
from airflow.utils.decorators import apply_defaults
STAGING_TABLE_NAME = 'tmp_table'


class RedshiftBulkUpsertOperator(BaseOperator):
    template_fields = ('primary_key', 'table', 'filename')

    @apply_defaults
    def __init__(self, *args, primary_key='id', filename=None, table=None, **kwargs):
        super(RedshiftBulkUpsertOperator, self).__init__(*args, **kwargs)
        self.redshift_hook = PostgresHook(postgres_conn_id='redshift_connection')
        self.primary_key = primary_key
        self.table = table
        self.filename = filename

    def execute(self, context):
        s3_hook = FliptS3Hook(context)
        filename = self.filename if self.filename else s3_hook.file_name
        self.bulk_upsert_from_s3(self.table, filename, self.primary_key)
        s3_query_result = self.get_affected_ids(s3_hook, filename, self.primary_key)
        if s3_query_result:
            affected_rows = [loads(row) for row in s3_query_result.strip().split('\n')]
        else:
            affected_rows = []

        return [row[self.primary_key] for row in affected_rows if row.get(self.primary_key, None)]

    def bulk_upsert_from_s3(self, table, file, primary_key="id"):
        sql = self._get_bulk_upsert_sql(table, file, primary_key)
        db_log = self.redshift_hook.log
        db_log.info('Executing UPSERT SQL. Logs suppressed due to secrets')
        db_log.disabled = True
        self.redshift_hook.run(sql)
        db_log.disabled = False

    @staticmethod
    def get_affected_ids(s3_hook, file, primary_key):
        serialization = {'JSON': {'Type': 'LINES'}}
        sql = f'SELECT s."{primary_key}" FROM S3Object s'
        return s3_hook.select_key(
            RedshiftBulkUpsertOperator.get_s3_url(file),
            input_serialization=serialization,
            output_serialization={'JSON': {}},
            expression=sql
        )

    @staticmethod
    def _get_bulk_upsert_sql(table, file, primary_key):
        relative_path = os.path.dirname(__file__)
        sql_file = os.path.join(relative_path, "redshift_bulk_upsert.sql")
        bulk_upsert_sql = open(sql_file).read()
        [target_schema, target_table] = table.split('.')
        return bulk_upsert_sql.format(
            target_schema=target_schema,
            target_table=target_table,
            aws_access_key=Variable.get('AWS_ACCESS_KEY_ID'),
            aws_secret=Variable.get('AWS_SECRET_ACCESS_KEY'),
            s3_file_url=RedshiftBulkUpsertOperator.get_s3_url(file),
            staging_table=STAGING_TABLE_NAME,
            p_key=primary_key
        )

    @staticmethod
    def get_s3_url(file):
        protocol = 's3://'
        if protocol in file:
            return file
        bucket = Variable.get("AWS_BUCKET_NAME")
        return f's3://{bucket}/{file}'
