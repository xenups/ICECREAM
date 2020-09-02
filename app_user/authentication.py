from distutils.util import strtobool

from bottle import request
from bottle_jwt2 import JWTProviderPlugin
from sqlalchemy.orm import Session
from ICECREAM.cache import RedisCache
from ICECREAM.http import HTTPError
from ICECREAM.validators import validate_data
from app_user.messages import USER_IS_NOT_ACTIVE, AUTHENTICATION_ERROR, TOKEN_EXPIRED, IP_BANNED_ERROR
from app_user.models import User
from ICECREAM.models.query import get_object
from ICECREAM.wrappers import db_handler
from app_user.schemas import user_serializer, login_serializer
from settings import project_secret, jwt_ttl, redis_cache
from limiter import FixedWindowLimiter

TEST_REDIS_CONFIG = {'host': 'redis', 'port': 6379,
                     'password': redis_cache['redis_pass'], 'db': 10}
throttle = FixedWindowLimiter(threshold=2, interval=3, redis_config=TEST_REDIS_CONFIG, name_space="default")


class LoginDefender(object):
    def __init__(self):
        self.ip = request.environ.get('HTTP_X_FORWARDED_FOR')

    def is_ip_in_blacklist(self):
        self.ip = request.environ.get('HTTP_X_FORWARDED_FOR')
        redis = RedisCache()
        is_blacklisted = redis.get(self.ip)
        if is_blacklisted:
            if strtobool(is_blacklisted.decode('utf-8')):
                raise HTTPError(*IP_BANNED_ERROR)
            return True
        return False

    def __put_ip_in_blacklist(self):
        redis = RedisCache()
        redis.set(self.ip, "True", 120)

    def check_ip_exceed(self):
        if throttle.exceeded(self.ip):
            self.__put_ip_in_blacklist()


class AuthBackend(object):
    def __init__(self):
        self.defender = LoginDefender()

    @db_handler
    def get_user_by_phone(self, db_session: Session, phone):
        user = get_object(User, db_session, User.phone == phone)
        if not user:
            # self.defender.check_ip_exceed()
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
        # self.defender.is_ip_in_blacklist()
        validate_data(login_serializer, data={"phone": username, "password": password})
        user_obj = self.get_user_by_phone(phone=username)
        if user_obj is not None:
            if username == user_obj.phone and user_obj.check_password(password):
                user = user_serializer.dump(user_obj)
                return user
        # self.defender.check_ip_exceed()
        raise HTTPError(*AUTHENTICATION_ERROR)

    def get_user(self, user_id):
        user = self.get_user_by_id(pk=user_id)
        if user_id == user['id']:
            return {k: user[k] for k in user.keys() if k != 'password'}
        raise HTTPError(*AUTHENTICATION_ERROR)


jwt_plugin = JWTProviderPlugin(
    keyword='jwt',
    auth_endpoint='/api/auth',
    refresh_endpoint='/api/refresh',
    backend=AuthBackend(),
    fields=('phone', 'password'),
    secret=project_secret,
    ttl=int(jwt_ttl),
    refresh_ttl=20000000
)
