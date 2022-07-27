from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator

from_date = "{{ task_instance.xcom_pull(task_ids='get_last_successful_dagrun_date') }}"


def get_last_successful_dagrun_date_task(dag, task_id='get_last_successful_dagrun_date'):
    dag_id = '{{ti.dag_id}}'

    def check_for_start_date(*op_args, **kwargs):
        dag_val = op_args[0]
        if kwargs['dag_run'].conf:
            return kwargs['dag_run'].conf['startDate']
        get_date = f"select MAX (start_date) as start_date from dag_run where state='success' \
                and dag_id='{dag_val}';"
        postgres_hook = PostgresHook(postgres_conn_id="airflow_db")
        date = postgres_hook.get_records(sql=get_date)
        date = date[0][0]
        return date

    return PythonOperator(
        task_id=task_id,
        python_callable=check_for_start_date,
        provide_context=True,
        do_xcom_push=True,
        dag=dag,
        op_args=[dag_id]
    )
