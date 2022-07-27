import datetime
import logging as log
from airflow import DAG, XComArg
from airflow.decorators import task
from Integration.plugins.config.default_dict_args import default_dag_args, default_task_args
from plugins.hooks.couchbase_hook import CouchbaseHook
from Integration.plugins.helpers import from_date, get_last_successful_dagrun_date_task
from plugins.operators.couchbase_operator import CouchbaseOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from Integration.plugins.dag_helpers.cb_claims_to_dw_claims.dw_processed_claim_sql import insert_processed_claims_sql
from plugins.operators.redshift_bulk_upsert_operator import RedshiftBulkUpsertOperator
from Integration.plugins.utils.s3_url import s3_source_error_url, s3_task_url, s3_source_url
from plugins.operators.postgres_list_operator import PostgresListOperator, PostgresHook

bucket = "`{bucket}`"
validation_query_list = """
SELECT 'call '|| task_call ||'('|| case when task_require_dag_info_as_params=1 then '''{{ti.dag_id}}'', ''{{ti.run_id}}''' else '' end || ');'  as validation_rule
FROM flipt_dw.dw_tbl_etl_validation_master_control
where lower(job_name) = lower('cb_claims_to_dw_claims')
and task_status='ACTIVE'
order by task_sequence
"""



update_dw_claims = """
update flipt_dw.dw_claims
set process_error_code = nullif(trim(process_error_code),'')
where nullif(trim(process_error_code),'') is null;
update flipt_dw.dw_claims
set process_error_code = nullif(trim(a.errors),'')
from flipt_dw.dw_claims e
join flipt_dw.dw_processedclaims p on e.auth_id=p.flipt_auth_id and cast(e.sequencenumber  as int) = p.sequence_number and p.erx_transaction_id = e.transactionid
join (
SELECT auth_id, sequencenumber,listagg(error_type,' || ') within group (order by error_date) over( partition by auth_id, sequencenumber)  as errors
FROM flipt_dw.dw_claims_validations_errors
where resolved_date is null
) a on a.auth_id=p.flipt_auth_id and cast(a.sequencenumber as int) = p.sequence_number
where nullif(trim(e.process_error_code),'') is not null
"""

schema = "flipt_dw"
viewname = "dw_first_fill_report"
sql_first_fill_report = f"REFRESH MATERIALIZED VIEW {schema}.{viewname}"

queries = [update_dw_claims, insert_processed_claims_sql, sql_first_fill_report]


COUCHBASE_CLAIMS_FILENAME = s3_source_url("from_cb_claims_{{ ts_nodash }}.jsonl")
REDSHIFT_CLAIMS_FILENAME = s3_source_url("to_redshift_rs_claims_{{ ts_nodash }}.jsonl")

with DAG(
    "cb_claims_to_dw_claims",
    schedule_interval='00 7,15 * * *',
    start_date=datetime.datetime(2020, 8, 20),
    params={'owners': ['smit', 'das', 'soumithri']},
    tags=['data-warehouse', 'claims'],
    default_args=default_task_args,
    **default_dag_args) \
        as dag:

    get_last_successful_dagrun_date = get_last_successful_dagrun_date_task(dag)

    pull_claims_from_couchbase = CouchbaseOperator(
        task_id="pull_claims_from_couchbase",
        query=f"SELECT * FROM {bucket} WHERE type='claim' \
            and (updateDate>'{from_date}' OR payer_recon_timestamp>'{from_date}' \
                OR erx_recon_timestamp>'{from_date}') and claim_status is not NULL",
        dest_s3_key=COUCHBASE_CLAIMS_FILENAME
    )

    upsert_cb_claims_with_validations = RedshiftBulkUpsertOperator(
        table="flipt_dw.dw_claims",
        primary_key="transactionid",
        task_id="upsert_cb_claims_with_validations",
        do_xcom_push=True,
        filename=COUCHBASE_CLAIMS_FILENAME
    )

    get_validation_rules = PostgresListOperator(
        task_id="postgres_validation_rules",
        sql=validation_query_list,
        column_to_list='validation_rule'
    )

    # def execute_validations(conn_id, call):
    #     hook = PostgresHook(postgres_conn_id=conn_id)
    #     try:
    #         log.info(f"Executing rule:{call['validation_rule']}")
    #         hook.run(sql=call['validation_rule'], autocommit=True)
    #     except Exception as ex:
    #         log.error(f"Failed executing rule: {call['validation_rule']}")
    #         log.error(ex)
    #         raise ex

    execute_validation_rules = PostgresOperator.partial(
        task_id="execute_validation_rules",
        postgres_conn_id="redshift_connection"
    ).expand(sql=XComArg(get_validation_rules))

    # @task
    # def execute_validations(conn_id, call):
    #     hook = PostgresHook(postgres_conn_id=conn_id)
    #     try:
    #         log.info(f"Executing rule:{call['validation_rule']}")
    #         hook.run(sql=call['validation_rule'], autocommit=True)
    #     except Exception as ex:
    #         log.error(f"Failed executing rule: {call['validation_rule']}")
    #         log.error(ex)
    #         raise ex

    # @task
    # def update_dw_claims_with_process_code(conn_id, sql):
    #     hook = PostgresHook(postgres_conn_id=conn_id)
    #     try:
    #         log.info(f"Executing sql:\n{sql}")
    #         hook.run(sql=sql, autocommit=True)
    #     except Exception as ex:
    #         log.error(f"Failed executing sql:\n{sql}")
    #         log.error(ex)
    #         raise ex
    

    # execute_validations.partial(conn_id=get_validation_rules.postgres_conn_id).expand(call=XComArg(get_validation_rules))

    update_dw_claims_with_errors = PostgresOperator(
        task_id="update_dw_claims_with_errors",
        postgres_conn_id="redshift_connection",
        sql=update_dw_claims
    )

    insert_processed_claims = PostgresOperator(
        sql=insert_processed_claims_sql,
        postgres_conn_id="redshift_connection",
        autocommit=True,
        task_id="insert_processed_claims"
    )
    refresh_dw_first_fill_report = PostgresOperator(
        sql=sql_first_fill_report,
        postgres_conn_id="redshift_connection",
        autocommit=True,
        task_id="refresh_dw_first_fill_report"
    )

get_last_successful_dagrun_date >> pull_claims_from_couchbase >> upsert_cb_claims_with_validations >> get_validation_rules  >> [execute_validation_rules]
[execute_validation_rules] >> update_dw_claims_with_errors >> insert_processed_claims >> refresh_dw_first_fill_report