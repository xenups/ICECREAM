"ICECREAM"
from marshmallow import Schema, fields


class SMSSchema(Schema):
    class Meta:
        fields = ('cell_number',)


SMS_serializer = SMSSchema()
