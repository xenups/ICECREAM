"ICECREAM"

from marshmallow import Schema, fields, validate


class SuperPersonSchema(Schema):
    class Meta:
        fields = ("id", "name", "last_name", 'bio')


class SuperUserSchema(Schema):
    person = fields.Nested(SuperPersonSchema)
    id = fields.Integer(allow_none=True)
    name = fields.String(required=True)
    phone = fields.String(required=True, validate=[validate.Length(equal=11)])

    class Meta:
        fields = ("id", 'phone', 'password', 'roles', 'person')


class PersonSchema(Schema):
    class Meta:
        fields = ("id", "name", "last_name", 'bio')


class UserSchema(Schema):
    person = fields.Nested(PersonSchema)
    name = fields.String(required=True)
    signup_token = fields.UUID(required=True)
    phone = fields.String(required=True, validate=[validate.Length(equal=11)])
    password = fields.Str(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)

    # roles =fields.String(required=True)

    class Meta:
        fields = ('id', 'signup_token', 'phone', 'password', 'roles', 'person')


superuser_serializer = SuperUserSchema()
user_serializer = UserSchema(only=('id', 'signup_token', 'phone', 'password', 'roles', 'person'))
person_serializer = PersonSchema()
users_serializer = UserSchema(many=True, only=('id', 'signup_token', 'phone', 'roles', 'person'))
