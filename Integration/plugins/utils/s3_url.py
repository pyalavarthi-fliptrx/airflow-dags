from airflow.models import Variable
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

S3_PATH = 's3://{{var.value.AWS_BUCKET_NAME}}/{{var.value.S3_ENV_PREFIX}}'


def s3_url_complete(path, key):
    return f's3://{path}/{key}'


def s3_url(key):
    return f'{S3_PATH}/{key}'

def s3_source_url(key):
    return S3_PATH + '/{{ ti.dag_id }}/source/{{ds_nodash}}/' + key

def s3_source_error_url(key):
    return S3_PATH + '/{{ ti.dag_id }}/error/{{ds_nodash}}/' + key

def s3_source_processed_url(key):
    return S3_PATH + '/{{ ti.dag_id }}/processed/{{ds_nodash}}/' + key

def s3_task_url(key):
    return S3_PATH + '/{{ ti.dag_id }}/{{ run_id }}/' + key


def raw_s3_url(key):
    return f's3://{Variable.get("AWS_BUCKET_NAME")}/{Variable.get("S3_ENV_PREFIX")}/{key}'


def s3_bucket():
    try:
        return Variable.get("AWS_BUCKET_NAME")
    except (SQLAlchemyError, KeyError):
        # We are in a test context and the db has not been loaded
        return 'flipt-airflow'


def horizon_medical_file_name():
    file_name = 'IPSFLPMR.HORIZON.{}.txt.PGP'.format(datetime.now().strftime("%Y%m%d-%f"))
    return'{}/{}'.format(datetime.now().strftime("%Y%m%d-%f"), file_name)


def grandrounds_sftp_prefix():
    try:
        return Variable.get("GRANDROUNDS_SFTP_PREFIX")
    except (SQLAlchemyError, KeyError):
        # We are in a test context and the db has not been loaded
        return '/'
