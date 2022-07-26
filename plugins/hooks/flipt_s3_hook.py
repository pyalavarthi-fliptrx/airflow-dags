from tempfile import NamedTemporaryFile
from airflow.hooks.S3_hook import S3Hook
from airflow.models import Variable


class FliptS3Hook(S3Hook):
    def __init__(self, context, file_name=None, file_prefix=None, *args, **kwargs):
        super(FliptS3Hook, self).__init__(*args, **kwargs)

        task_instance = context.get("task_instance")

        self.context = context
        self.directory = task_instance.dag_id if task_instance else "misc"
        if file_prefix:
            self.directory += "/" + file_prefix
        self.file_name = file_name or f"{self.directory}/{self.context.get('run_id')}"
        self.log.info(f">>>>>>> filename: {self.file_name}")

    def upload_file(self, temp_file_name, key):
        key = key or self.file_name
        self.log.info(f">>>> Uploading file ({key})...")
        self.load_file(temp_file_name, key, bucket_name=self.bucket(), replace=True)

    @staticmethod
    def bucket():
        return Variable.get("AWS_BUCKET_NAME")

    def clean_up(self, clear_all=False):
        keys = (
            self.list_keys(bucket_name=self.bucket(), prefix=self.directory)
            if clear_all
            else [self.file_name]
        )

        self.delete_objects(bucket=self.bucket(), keys=keys)
        self.log.info(f">>>> Deleting {keys}")

    def file_download(self):
        source_s3_key_object = self.get_key(self.file_name, self.bucket())

        source_file = self.create_new_temporary_file()
        source_s3_key_object.download_fileobj(Fileobj=source_file)
        source_file.flush()

        results = source_s3_key_object.get()["Body"].read().decode("utf-8").strip().split("\n")

        return results

    @staticmethod
    def create_new_temporary_file(mode='wb'):
        return NamedTemporaryFile(mode)
