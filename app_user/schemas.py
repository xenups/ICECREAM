"ICECREAM"

from marshmallow import Schema, fields


class PersonSchema(Schema):
    class Meta:
        fields = ("id", "name", "last_name", 'phone', 'bio')


class UserSchema(Schema):
    person = fields.Nested(PersonSchema)

    class Meta:
        fields = ('id', 'username', 'password', 'person')


user_serializer = UserSchema()
person_serializer = PersonSchema()
users_serializer = UserSchema(many=True, only=('id', 'username', 'person'))
