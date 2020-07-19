import json
import logging

from redis import Redis

from settings import redis_cache
from .util import Singleton

logger = logging.getLogger()

CHUNK_SIZE = 5000


class BaseRedisConnector(Redis):
    def __init__(self):
        try:
            super().__init__(host=redis_cache['redis_host'], port=redis_cache['redis_port'],
                             password=redis_cache['redis_pass'])

        except Exception as error:
            logger.error(error)
            raise error


class RedisConnector(BaseRedisConnector, metaclass=Singleton):
    pass


class RedisCache(RedisConnector):
    def __init__(self):
        super().__init__()

    def get_cache_multiple_value(self, key, custom_value_name):
        if key:
            __json_value_data = self.get(key)
            if __json_value_data is not None:
                __value = (json.loads(__json_value_data)).get(custom_value_name, None)
                return __value
        return None

    def set_cache_multiple_value(self, key, value, custom_value_name, ttl=60):
        __json_value_data = self.get(key)
        try:
            __exist_json = json.loads(__json_value_data)
            __dict_value = {custom_value_name: value}
            __dict_value.update(__exist_json)
            __json_data = json.dumps(__dict_value)
            __cache_status = self.set(key, __json_data, ex=ttl)
            return __cache_status
        except Exception as error:
            logger.error(error)
            __json_data = json.dumps({custom_value_name: str(value)})
            __cache_status = self.set(key, __json_data, ex=ttl)
            return __cache_status

    def clear_ns(self, ns):
        cursor = '0'
        ns_keys = ns + '*'
        while cursor != 0:
            cursor, keys = self.scan(cursor=cursor, match=ns_keys, count=CHUNK_SIZE)
            if keys:
                self.delete(*keys)
        return True
