from dags.Integration.plugins.hooks.flipt_s3_hook import FliptS3Hook
from dags.Integration.plugins.utils.dump_json import dump_json
import json
from typing import Generator


class JsonS3Hook(FliptS3Hook):
    def __init__(self, context={}, *args, **kwargs):
        super(JsonS3Hook, self).__init__(context, *args, **kwargs)
        self.__file = self.create_new_temporary_file('w')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.flush()

    def append(self, dict_obj):
        json_object = dump_json(dict_obj)
        self.__file.write(json_object + "\n")

    def flush(self):
        self.__file.flush()
        bucket = self.bucket() if 's3://' not in self.file_name else None
        self.load_file(self.__file.name, self.file_name, bucket, True)
        self.__file.close()
        return self.file_name

    def get_records(self, sql=None):
        return [json.loads(line) for line in self.file_download()]

    @classmethod
    def to_json_s3_file(cls, file_name: str, generator: Generator):
        with JsonS3Hook(file_name=file_name) as json_s3:
            for obj in generator:
                json_s3.append(obj)
