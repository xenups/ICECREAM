from marshmallow import Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from ICECREAM.http import HTTPError


def validate_data(serializer: Schema, data: {}):
    validation_errors = serializer.validate(data)
    if validation_errors:
        raise HTTPError(403, validation_errors)
    return True


