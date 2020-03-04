"ICECREAM"
from marshmallow import Schema, fields
from ICECREAM.util import get_media_link
from app_foo.models import RoomImage, Room


class RoomImageSchema(Schema):
    name = fields.Str(required=True)
    room_id = fields.Int(required=True)
    image_path = fields.Method("get_media_path")

    @staticmethod
    def get_media_path(room_image):
        return get_media_link(room_image.name)

    class Meta:
        model = RoomImage
        fields = ('id', 'name', 'room_id', 'files', 'image_path')


class RoomSchema(Schema):
    room_images = fields.Nested(RoomImageSchema(many=True))

    class Meta:
        model = Room
        fields = ('id', 'name', 'room_images')


room_serializer = RoomSchema()
room_image_serializer = RoomImageSchema()
