import secrets
from distutils.util import strtobool

from bottle import request

from ICECREAM.http import HTTPError


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def generate_otp_code():
    return secrets.SystemRandom().randrange(999, 9999)


def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


def get_media_link(file_name):
    host = request.get_header('host')
    # for production
    return 'http://{}/api/statics/media/{}'.format(host, file_name)
    # return 'http://{}:8080/api/media/{}'.format(host, file_name)


def str_to_bool(val):
    try:
        return strtobool(val)
    except Exception as e:
        return None
