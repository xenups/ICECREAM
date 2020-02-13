"ICECREAM"
from marshmallow import Schema, fields


class RoomSchema(Schema):
    class Meta:
        fields = ('id', 'name')


room_serializer = RoomSchema()
