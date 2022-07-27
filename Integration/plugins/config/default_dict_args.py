from datetime import timedelta
#from utils.error_handler import error_handler

default_task_args = {
    "email": "",
    "email_on_failure": False,
    "email_on_retry": False,
    "owner": "airflow",
    "retries": 0,
    "queue": "default",
    "on_failure_callback": "",
    "retry_delay": timedelta(minutes=5),
    'execution_timeout': timedelta(hours=12)
}

default_dag_args = {
    'catchup': False,
    'dagrun_timeout': timedelta(hours=24),
    'max_active_runs': 1
}