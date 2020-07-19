# -*- coding: utf-8 -*-
"""`bottle_cache.plugin` module.

Provides bottle.py cache plugin.
modified by amir lesani
"""

__author__ = 'Papavassiliou Vassilis'
__date__ = '23-1-2016'

import bottle
import collections
import inspect
import ujson

from ICECREAM.api_cache import backend

CacheInfo = collections.namedtuple('CacheInfo', 'ttl, cache_key_func, content_type')


def available_backend():  # pragma: no cover
    """Auto loading available cache backend implementation
    without hard-coding them.
    """

    backend_module = backend

    available_list = [
        callback for callback in dir(backend_module)
        if 'cachebackend' in callback.lower() and
           'base' not in callback.lower()
    ]

    return {callback.lower().replace('cachebackend', ''): getattr(backend_module, callback)
            for callback in available_list}


def cache_for(ttl, cache_key_func='full_path', content_type='application/json'):
    """A decorator that signs a callable object with a 'CacheInfo'
    attribute.

    Args:
        ttl (int): Cache Time to live in seconds.
        cache_key_func (str): The key for the cache key function installed on Plugin.
        content_type (str): Handler response type.
    Returns:
        The callable object.
    """

    def _wrapped(callback):
        setattr(
            callback,
            'cache_info',
            CacheInfo(ttl, cache_key_func, content_type)
        )

        return callback

    return _wrapped


class CachePlugin(object):
    """A `bottle.Bottle` application plugin for `bottle_cache.backend` implementations.

    Attributes:
        keyword (str): The string keyword for application registry.
        provider (instance): A JWTProvider instance.
        login_enable (bool): If True app is mounted with a login handler.
        auth_endpoint (str): The authentication uri for provider if
                             login_enabled is True.
        kwargs : JWTProvider init parameters.
    """

    api = 2

    content_types = (
        ('text/html', lambda x: x),
        ('application/json', ujson.dumps)
    )

    cache_key_rules = {
        'full_path': lambda req, cxt: str(cxt.rule) + req.query_string,
        'query_path': lambda req, cxt: req.query_string,
    }

    def __init__(self, keyword, backend, **backend_kwargs):  # pragma: no cover

        if backend not in available_backend():
            raise bottle.PluginError(
                'Invalid backend {} provided. Available until now: ({})'.format(
                    backend, ', '.join(available_backend().keys())
                )
            )

        self.backend = available_backend()[backend](**backend_kwargs)
        self.keyword = keyword

    def register_rule(self, rule_key, rule_callback):  # pragma: no cover
        self.cache_key_rules[rule_key] = rule_callback
        return self

    def setup(self, app):  # pragma: no cover
        """Make sure that other installed plugins don't affect the same
        keyword argument and check if metadata is available.
        """
        for other in app.plugins:
            if not isinstance(other, CachePlugin):
                continue
            if other.keyword == self.keyword:
                raise bottle.PluginError(
                    "Found another cache plugin "
                    "with conflicting settings ("
                    "non-unique keyword)."
                )

    def apply(self, callback, context):  # pragma: no cover
        """Implement bottle.py API version 2 `apply` method.
        """
        cache_enabled = getattr(callback, 'cache_info', None)

        if not cache_enabled:
            callback_args = inspect.getfullargspec(context.callback).args

            if self.keyword not in callback_args:
                return callback

            def _wrapped_injected(*args, **kwargs):
                kwargs[self.keyword] = self.backend
                return callback(*args, **kwargs)

            return _wrapped_injected

        if cache_enabled.cache_key_func not in self:
            raise bottle.PluginError(
                'Unregistered cache key function: '
                '{}.'.format(cache_enabled.cache_key_func)
            )

        def wrapper(*args, **kwargs):

            cache_key_fn = self.cache_key_rules[cache_enabled.cache_key_func]
            key = cache_key_fn(bottle.request, context)
            data = self.backend.get(key)

            if data:
                bottle.response.content_type = cache_enabled.content_type
                return ujson.loads(data)

            result = callback(*args, **kwargs)
            if result.status == "200 OK":
                self.backend.set(key, ujson.dumps(result.body), cache_enabled.ttl)
            return result

        return wrapper

    def __repr__(self):  # pragma: no cover
        return "<{} instance at: 0x{:x}>".format(self.__class__, id(self))

    def __str__(self):  # pragma: no cover
        return '<{} instance> {}'.format(
            self.__class__.__name__,
            self.keyword
        )

    def __iter__(self):  # pragma: no cover
        for key in self.cache_key_rules:
            yield key

    def __contains__(self, item):  # pragma: no cover
        return item in self.cache_key_rules

    def __getitem__(self, item):  # pragma: no cover
        return self.cache_key_rules.get(item, None)

    def __setitem__(self, key, value):  # pragma: no cover
        self.cache_key_rules[key] = value

    def __delitem__(self, key):  # pragma: no cover
        del self.cache_key_rules[key]
