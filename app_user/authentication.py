from bottle_jwt import JWTProviderPlugin
from sqlalchemy.orm import Session
from ICECREAM.http import HTTPError
from ICECREAM.validators import validate_data
from app_user.messages import USER_IS_NOT_ACTIVE, TOKEN_EXPIRED, AUTHENTICATION_ERROR
from app_user.models import User
from ICECREAM.models.query import get_object
from ICECREAM.wrappers import db_handler
from app_user.schemas import user_serializer, login_serializer
from settings import project_secret, jwt_ttl


class AuthBackend(object):
    @db_handler
    def get_user_by_phone(self, db_session: Session, phone):
        user = get_object(User, db_session, User.phone == phone)
        if not user:
            raise HTTPError(*AUTHENTICATION_ERROR)
        if not user.is_active:
            raise HTTPError(*USER_IS_NOT_ACTIVE)
        return user

    @db_handler
    def get_user_by_id(self, db_session: Session, pk):
        user = get_object(User, db_session, User.id == pk)
        dumped_user = user_serializer.dump(user)
        if not user:
            raise HTTPError(*TOKEN_EXPIRED)
        if not user.is_active:
            raise HTTPError(*USER_IS_NOT_ACTIVE)
        return dumped_user

    def authenticate_user(self, username, password):
        validate_data(login_serializer, data={"phone": username, "password": password})
        user_obj = self.get_user_by_phone(phone=username)
        if user_obj is not None:
            if username == user_obj.phone and user_obj.check_password(password):
                user = user_serializer.dump(user_obj)
                return user
        raise HTTPError(*AUTHENTICATION_ERROR)
        # return None

    def get_user(self, user_id):
        user = self.get_user_by_id(pk=user_id)
        if user_id == user['id']:
            return {k: user[k] for k in user.keys() if k != 'password'}
        raise HTTPError(*AUTHENTICATION_ERROR)


jwt_plugin = JWTProviderPlugin(
    keyword='jwt',
    auth_endpoint='/api/auth',
    backend=AuthBackend(),
    fields=('phone', 'password'),
    secret=project_secret,
    ttl=int(jwt_ttl)
)
