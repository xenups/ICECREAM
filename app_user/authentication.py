from app_user.models import User
from ICECREAM.models.query import get_object
from ICECREAM.wrappers import db_handler
from bottle_jwt import JWTProviderPlugin
from app_user.schemas import user_serializer
from settings import project_secret, jwt_ttl


class AuthBackend(object):
    @db_handler
    def get_user_obj(self, db_session, phone):
        user = get_object(User, db_session, User.phone == phone)
        return user

    def authenticate_user(self, username, password):
        user_obj = self.get_user_obj(phone=username)
        if user_obj is not None:
            if username == user_obj.phone and user_obj.check_password(password):
                self.user = user_serializer.dump(user_obj)
                return self.user
            return None
        return None

    def get_user(self, user_id):
        if hasattr(self, 'user'):
            if user_id == self.user['id']:
                return {k: self.user[k] for k in self.user if k != 'password'}
        return None


jwt_plugin = JWTProviderPlugin(
    keyword='jwt',
    auth_endpoint='/auth',
    backend=AuthBackend(),
    fields=('phone', 'password'),
    secret=project_secret,
    ttl=int(jwt_ttl)
)
