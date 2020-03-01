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
        json_value_data = self.__redis_connector.cache.get(key)
        if json_value_data is not None:
            __value = (json.loads(json_value_data)).get(custom_value_name, None)
            return __value
        return None

    def set_cache_multiple_value(self, key, value, custom_value_name, ttl=60):
        json_value = self.__redis_connector.cache.get(key)
        try:
            exist_json = json.loads(json_value)
            dict_value = {custom_value_name: value}
            dict_value.update(exist_json)
            json_data = json.dumps(dict_value)
            __cache_status = self.__redis_connector.cache.set(key, json_data, ex=ttl)
            return __cache_status
        except:
            json_data = json.dumps({custom_value_name: str(value)})
            __cache_status = self.__redis_connector.cache.set(key, json_data, ex=ttl)
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
