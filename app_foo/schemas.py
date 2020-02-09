from bottle_marshmallow import MarshmallowPlugin
from marshmallow import Schema, fields, validate

from app_foo.models import Categores, Comments

ma = MarshmallowPlugin()


class CategorySchema(Schema):
    class Meta:
        model = Categores
        fields = ('id', 'name')

    id = fields.Integer(required=True)
    name = fields.String(required=True)


class CommentSchema(Schema):
    class Meta:
        model = Comments
        fields = ('id', 'category_id', 'comment')

    id = fields.Integer(dump_only=True)
    category_id = fields.Integer(required=True)
    comment = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()
