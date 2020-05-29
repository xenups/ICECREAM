"ICECREAM"
from app_user.models import PersonImage
from ICECREAM.util import get_media_link
from ICECREAM.rbac import get_roles_list
from marshmallow import Schema, fields, validate, EXCLUDE, ValidationError


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


class RoleFormat(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value.split(",")

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, list) and set(value).issubset(set(get_roles_list())):
            return value
        raise ValidationError('role is not valid', "_precessing")


class PersonImageSchema(Schema):
    name = fields.Str()
    person_id = fields.Int(required=True, load_only=True)
    image_path = fields.Method("get_media_path")

    @staticmethod
    def get_media_path(person_image):
        return get_media_link(person_image.name)

    class Meta:
        model = PersonImage
        fields = ('id', 'person_id', 'files', 'image_path')


class PersonSchema(Schema):
    person_images = fields.Nested(PersonImageSchema(many=True))

    class Meta:
        fields = ("id", "person_images", "name", "last_name", 'email')


class LoginSchema(Schema):
    phone = fields.String(required=True)
    password = fields.String(required=True)

    class Meta:
        fields = ("phone", "password")


class UserSchema(Schema):
    # password_strength_validator = [
    #     validate.Regexp("/^(?=(?:[^A-Z]*[A-Z]){2})(?=(?:[^0-9]*[0-9]){2}).{8,}$/", 'CaSu4Li8'), ]
    person = fields.Nested(PersonSchema)
    name = fields.String(required=True)
    phone = fields.String(required=True, validate=[validate.Length(equal=11)])
    password = fields.Str(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)
    roles = RoleFormat(attribute="roles")

    class Meta:
        fields = ('id', 'phone', 'password', 'person', 'roles')


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


class ChangePassword(Schema):
    old_password = fields.Str(required=True, load_only=True)
    password = fields.Str(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)

    class Meta:
        fields = ('old_password', 'password')


class RoleSchema(Schema):
    roles = RoleFormat(attribute="roles")

    class Meta:
        fields = ('roles',)


superuser_serializer = SuperUserSchema()
login_serializer = LoginSchema()
user_serializer = UserSchema(only=('id', 'phone', 'roles', 'password', 'person'))
user_edit_serializer = UserSchema(only=('id', 'phone', 'password', 'person'))
set_role_serializer = RoleSchema(only=('roles',))
person_serializer = PersonSchema()
users_serializer = UserSchema(many=True, only=('id', 'phone', 'person', 'roles'))
forget_pass_serializer = ForgetPasswordSMSSchema(only=('phone',))
reset_password_serializer = ResetPasswordSMS()
person_image_serializer = PersonImageSchema()
change_password_serializer = ChangePassword(only=('old_password', 'password'))
