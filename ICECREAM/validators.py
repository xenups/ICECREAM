from typing import Dict
from marshmallow import Schema

from ICECREAM.http import HTTPError


def validate_data(serializer: Schema, data: Dict):
    validation_errors = serializer.validate(data)
    if validation_errors:
        raise HTTPError(403, validation_errors)
    return True
