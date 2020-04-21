"ICECREAM"

from marshmallow import Schema, fields, validate, EXCLUDE


class SuperPersonSchema(Schema):
    class Meta:
        fields = ("id", "name", "last_name", 'email')


class SuperUserSchema(Schema):
    person = fields.Nested(SuperPersonSchema)
    id = fields.Integer(allow_none=True)
    name = fields.String(required=True)
    phone = fields.String(required=True, validate=[validate.Length(equal=11)])

    class Meta:
        fields = ("id", 'phone', 'password', 'roles', 'person')


class PersonSchema(Schema):
    class Meta:
        fields = ("id", "name", "last_name", 'email')


class UserSchema(Schema):
    person = fields.Nested(PersonSchema)
    name = fields.String(required=True)
    phone = fields.String(required=True, validate=[validate.Length(equal=11)])
    password = fields.Str(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)
    roles = fields.Method("format_roles")

    @staticmethod
    def format_roles(user):
        return user.roles.split(",")

    class Meta:
        fields = ('id', 'phone', 'password', 'person', 'roles')
        unknown = EXCLUDE


class ForgetPasswordSMSSchema(Schema):
    phone = fields.String(required=True, validate=[validate.Length(equal=11)])

    class Meta:
        fields = ('phone',)


class ResetPasswordSMS(Schema):
    phone = fields.String(required=True, validate=[validate.Length(equal=11)])
    password = fields.Str(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)
    token = fields.String(required=True)

    class Meta:
        fields = ('phone', 'password', 'token')


superuser_serializer = SuperUserSchema()
user_serializer = UserSchema(only=('id', 'phone', 'roles', 'password', 'person'))
person_serializer = PersonSchema()
users_serializer = UserSchema(many=True, only=('id', 'phone', 'person', 'roles'))
forget_pass_serializer = ForgetPasswordSMSSchema(only=('phone',))
reset_password_serializer = ResetPasswordSMS()
