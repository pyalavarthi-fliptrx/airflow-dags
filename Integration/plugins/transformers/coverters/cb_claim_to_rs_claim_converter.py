#!/usr/bin/env python3
import ast
import json
import logging as log
from typing import List
from pydantic import ValidationError
from dags.Integration.plugins.utils.helper_functions import extract_validation_errors
from dags.Integration.plugins.models.couchbase.claim import Claim as CouchbaseClaim
from dags.Integration.plugins.models.redshift.claim import InvalidClaim as Validation
from dags.Integration.plugins.models.redshift.claim import ValidClaim as RedshiftClaim
from dags.Integration.plugins.utils.money import Money


def convert_cb_claim_to_rs_stg_claim(cb_claim):
    rs_claim = cb_claim_to_rs_claim(cb_claim)
    rs_claim = validate_data(rs_claim)
    rs_claim = _format_decimals(rs_claim)
    return rs_claim

def _prepend_keys(sub_document, prefix):
    if sub_document:
        return {prefix + "_" + k: v for k, v in sub_document.items()}
    else:
        return {}

def _stringify_lists(dict):
    return {k: (json.dumps(v) if isinstance(v, List) else v) for k, v in dict.items()}

def cb_claim_to_rs_claim(cb_claim):

    try:
        cb_claim = CouchbaseClaim(**cb_claim).dict()
    except ValidationError as e:
        error_code_dict = list(extract_validation_errors(e))
        cb_claim['process_error_code'] = str(error_code_dict)
        log.error(f'{cb_claim["auth_id"]}-{cb_claim["sequenceNumber"]}:{str(error_code_dict)}')
        for field in error_code_dict:
            for key in field:
                attr_name = key[1:] if key.startswith('_') else key
                cb_claim[attr_name] = None
        cb_claim = CouchbaseClaim(**cb_claim).dict()

    rs_claim = {
        **cb_claim,
        **_prepend_keys(cb_claim["claim_request"], "request"),
        **_prepend_keys(cb_claim["claim_response"], "response"),
        **_prepend_keys(cb_claim["claim_transfer_request"], "transferrequest"),
        **_prepend_keys(cb_claim["claim_transfer_response"], "transferresponse"),
    }
    rs_claim = _stringify_lists(rs_claim)
    return RedshiftClaim(**rs_claim).dict()


def validate_data(rs_claim):
    try:
        Validation(**rs_claim)
    except ValidationError as e:
        error_code_dict = list(extract_validation_errors(e))
        rs_claim['process_error_code'] = error_code_dict
    except KeyError as e:
        error_field_dict = {"field missing": str(e)}
        rs_claim['process_error_code'] = error_field_dict
    return rs_claim


def _format_decimals(dailyclaim_claim):
    fields_to_change = ["payer_patient_paid_amount", "payer_ing_cost", "payer_dispensing_fee",
                        "payer_sales_tax", "payer_client_due_amt"]
    for field_name in fields_to_change:
        field_value = dailyclaim_claim.get(field_name, "0.0")
        dailyclaim_claim[field_name] = str(Money(field_value or "0.0", precision='1.00'))
    return dailyclaim_claim

