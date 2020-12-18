import bottle
from functools import wraps
from time import time
from bottle import request
from sqlalchemy.exc import SQLAlchemyError

from ICECREAM.cache import RedisCache
from ICECREAM.db_initializer import DataBaseConnectionManager
import logging

logger = logging.getLogger()


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        logger.info('func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te - ts))
        return result

    return wrap


def pass_data(func):
    def wrapper(*args, **kwargs):
        if request.json is not None:
            kwargs['data'] = request.json
        elif request.forms is not None:
            my_data = {}
            data_list = request.forms.dict
            for key in data_list.keys():
                my_data[key] = data_list[key][0]
            if request.files is not None and request.files.dict is not None:
                my_data['files'] = request.files.dict.get('files')

            kwargs['data'] = my_data

        rtn = func(*args, **kwargs)
        return rtn

    return wrapper


@bottle.route('/<:re:.*>', method='OPTIONS')
def cors(fn):
    def _cors(*args, **kwargs):
        # set CORS headers
        bottle.response.headers['Access-Control-Allow-Origin'] = '*'
        bottle.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        bottle.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _cors


def db_handler(func):
    def wrapper(*args, **kwargs):
        session = DataBaseConnectionManager().get_db_session()
        try:
            session.expire_on_commit = False
            kwargs['db_session'] = session
            rtn = func(*args, **kwargs)
            kwargs['db_session'].commit()
            return rtn
        except(SQLAlchemyError, bottle.HTTPError, Exception):
            session.rollback()
            raise

    return wrapper


def debug(fn):
    def wrapper(*args, **kwargs):
        logger.info("Entering {:s}".format(fn.__name__))
        result = fn(*args, **kwargs)
        logger.info("Finished {:s}".format(fn.__name__))
        return result

    return wrapper


def clear_cache(cached_url):
    def decorator(function):
        def wrapper(*args, **kwargs):
            redis = RedisCache()
            redis.clear_ns(ns=cached_url)
            result = function(*args, **kwargs)
            return result
        return wrapper
    return decorator
