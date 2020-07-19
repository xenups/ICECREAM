# -*- coding: utf-8 -*-
"""`bottle_cache.backend` module.

Provides package caching backend implementations.
"""

__author__ = 'Papavassiliou Vassilis'
__date__ = '23-1-2016'

from redis import StrictRedis
from redis.exceptions import RedisError

from ICECREAM.api_cache.bases import BaseCacheBackend, CacheError


class RedisCacheBackend(BaseCacheBackend):
    """Redis backend Implementation
    """

    def __init__(self, backend_client=StrictRedis, key_tpl='{}', **conn_data):
        """Overriding 'BaseCache.__init__' method.
        """

        redis_backend = backend_client(**conn_data)

        super(RedisCacheBackend, self).__init__(backend_client=redis_backend, key_tpl=key_tpl)

    def get(self, key):
        """Implementing `BaseCache.get` method.
        """
        try:
            return self.backend.get(key)
        except RedisError as error:  # pragma: no cover
            raise CacheError(error.args)

    def set(self, key, value, ttl=None):
        """Implementing `BaseCache.set` method.
        """
        try:
            if ttl:
                self.backend.setex(key, ttl, value)
            else:
                self.backend.set(key, value)

            return self

        except RedisError as error:  # pragma: no cover
            raise CacheError(error.args)

    def remove(self, key):
        """Implementing `BaseCache.remove` method.
        """
        try:
            self.backend.delete(key)
            return self

        except RedisError as error:  # pragma: no cover
            raise CacheError(error.args)

    def clear(self):
        self.backend.flushall()
        return self
