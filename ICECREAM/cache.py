import json
import redis

from .util import Singleton


class BaseRedisConnector:
    def __init__(self):
        try:
            self.cache = redis.Redis()

        except Exception as error:
            print(error)


class RedisConnector(BaseRedisConnector, metaclass=Singleton):
    pass


class RedisCache(object):
    def __init__(self):
        self.__redis_connector = RedisConnector()

    def get_cache_multiple_value(self, key, custom_value_name):
        __json_value_data = self.__redis_connector.cache.get(key)
        if __json_value_data is not None:
            __value = (json.loads(__json_value_data)).get(custom_value_name, None)
            return __value
        return None

    def set_cache_multiple_value(self, key, value, custom_value_name, ttl=60):
        __json_value_data = self.__redis_connector.cache.get(key)
        try:
            __exist_json = json.loads(__json_value_data)
            __dict_value = {custom_value_name: value}
            __dict_value.update(__exist_json)
            __json_data = json.dumps(__dict_value)
            __cache_status = self.__redis_connector.cache.set(key, __json_data, ex=ttl)
            return __cache_status
        except Exception:
            __json_data = json.dumps({custom_value_name: str(value)})
            __cache_status = self.__redis_connector.cache.set(key, __json_data, ex=ttl)
            return __cache_status

    def delete_cache_value(self, key):
        __status = self.__redis_connector.cache.delete(key)
        return __status

    def set_cache_value(self, key, value, ttl):
        __cache_status = self.__redis_connector.cache.set(key, value, ttl)
        return __cache_status

    def get_cache_value(self, key):
        __value = self.__redis_connector.cache.get(key)
        return __value
