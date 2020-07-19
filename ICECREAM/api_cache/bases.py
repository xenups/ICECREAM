# -*- coding: utf-8 -*-
"""`bottle_cache.bases` module.

Provides the main package interfaces for caching.
"""

__author__ = 'Papavassiliou Vassilis'
__date__ = '23-1-2016'

import abc
import six
from . import __version__ as version


class CacheError(Exception):
    """Raises when a caching error occurs (i.e connection error)
    """
    pass


@six.add_metaclass(abc.ABCMeta)
class BaseCacheBackend(object):
    """Base class interface.
    """

    api_version = tuple(map(int, version.split('.')))

    __slots__ = ('backend', 'key_tpl')

    def __init__(self, backend_client, key_tpl=None):
        self.backend = backend_client
        self.key_tpl = key_tpl

    @abc.abstractmethod
    def get(self, key):
        """Retrieve from cache based on key.
        Args:
            key(basestring): The cached object key string.

        Returns:
            'Hiredis' parsed python object (dict) if key exists or None
        """
        pass

    @abc.abstractmethod
    def set(self, key, value, ttl=None):
        """Set a value in cache under a specific key, with time to live

        Args:
            key (str): The cache key string.
            value (dict): The dict value.
            ttl (int): The time to live. If none key never expires.

        Returns:
            Cache instance.
        """
        pass

    @abc.abstractmethod
    def remove(self, key):
        """Remove a key/value from cache.

        Args:
            key (str): The cache key.

        Returns:
            Cache instance.
        """

    @abc.abstractmethod
    def clear(self):
        """Removes all key/ values from cache storage.

        Returns:
            Cache instance.
        """

    def key_func(self, key):  # pragma: no cover
        return self.key_tpl.format(key)
