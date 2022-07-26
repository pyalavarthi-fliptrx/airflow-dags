import json
from datetime import datetime, date, time
from uuid import UUID
from dags.Integration.plugins.utils.money import Money, Decimal


def dump_json(obj):
    return json.dumps(obj, default=dt_serializer, allow_nan=False)


def dt_serializer(obj):
    if isinstance(obj, datetime) or isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, (UUID, datetime, date, time, Money, Decimal)):
        return str(obj)
    raise TypeError(f"Unknown serializer for type: {type(obj).__name__}")
