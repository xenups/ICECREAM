"ICECREAM"
from marshmallow import Schema, fields


class SMSSchema(Schema):
    class Meta:
        fields = ('phone',)


SMS_serializer = SMSSchema()
