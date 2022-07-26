import json
from datetime import datetime
from typing import Dict

from airflow.configuration import conf

def get_env():
    return conf.get("core", "FLIPT_ENV")


def get_lowercased_field_names(member: Dict) -> Dict:
    return {k.lower(): v for k, v in member.items()}


def validation_error_key_formation(error_list):
    key_string = ""
    for each_field in error_list:
        key_string += '_' + str(each_field)
    return key_string


def extract_validation_errors(validation_error):
    errors_json_formatted = json.loads(validation_error.json())
    for error in errors_json_formatted:
        key_string = validation_error_key_formation(error['loc'])
        yield {key_string: {'error_message': error['msg']}}


def update_cb_record_timestamp():
    return {
        'updated_by': 'Airflow',
        'update_date': datetime.now().isoformat()
    }
