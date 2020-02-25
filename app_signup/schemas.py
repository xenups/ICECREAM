"ICECREAM"
from marshmallow import Schema, fields


class SMSSchema(Schema):
    class Meta:
        fields = ('cell_no',)


room_serializer = SMSSchema()
