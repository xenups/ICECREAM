from bottle_jwt import JWTProviderPlugin

from ICECREAM.models.query import get
from ICECREAM.wrappers import db_handler
from app_user.models import User
from app_user.schemas import user_serializer
from settings import project_secret, jwt_ttl


class AuthBackend(object):
    @db_handler
    def get_user_obj(self, db_session, username):
        user = get(User, db_session, username=username)
        return user

    def authenticate_user(self, username, password):
        user_obj = self.get_user_obj(username=username)
        if user_obj is not None:
            if username == user_obj.username and user_obj.check_password(password):
                self.user = user_serializer.dump(user_obj)
                return self.user
            return None
        return None

    def get_user(self, user_id):
        if user_id == self.user['id']:
            return {k: self.user[k] for k in self.user if k != 'password'}
        return None


jwt_plugin = JWTProviderPlugin(
    keyword='jwt',
    auth_endpoint='/auth',
    backend=AuthBackend(),
    fields=('username', 'password'),
    secret=project_secret,
    ttl=int(jwt_ttl)
)
