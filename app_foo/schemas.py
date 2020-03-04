"ICECREAM"
from marshmallow import Schema, fields

from app_foo.models import RoomImage, Room


class RoomImageSchema(Schema):
    name = fields.Str(required=True)
    room_id = fields.Int(required=True)

    class Meta:
        model = RoomImage
        fields = ('id', 'name', 'room_id', 'files')


class RoomSchema(Schema):
    room_images = fields.Nested(RoomImageSchema(many=True))

    class Meta:
        model = Room
        fields = ('id', 'name', 'room_images')


room_serializer = RoomSchema()
room_image_serializer = RoomImageSchema()
