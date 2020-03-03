"ICECREAM"
from marshmallow import Schema, fields


class RoomSchema(Schema):
    class Meta:
        fields = ('id', 'name')


class RoomImageSchema(Schema):
    name = fields.Str(required=True)
    room_id = fields.Int(required=True)

    class Meta:
        fields = ('id', 'name', 'room_id', 'files')


room_serializer = RoomSchema()
room_image_serializer = RoomImageSchema()
