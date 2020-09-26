# -*- coding: utf-8 -*-
#
#    Copyright (C) 2015  Papavassiliou Vassilis
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""`bottle_smart_filters` package.
Smart Querystring Params guessing for bottle.py applications.
"""

__version__ = '0.3'

__author__ = 'Papavassiliou Vassilis'
__date__ = '2016-9-14'

__all__ = ('SmartFiltersPlugin',)

import ast
from functools import partial
import bottle
import ujson
from mongosql import MongoQuery, MongoQuerySettingsDict
from sqlalchemy_filters import apply_filters

from ICECREAM.http import HTTPResponse, HTTPError
from ICECREAM.paginator import Paginate


class SmartFiltersPlugin(object):
    """Bottle.py application plugin for query string parameters smart detection.
    Attributes:
        keyword (str): The string keyword for application registry.
        filter_set (instance): A QueryFilterSet instance.
    """
    scope = ('plugin', 'middleware')
    api = 2

    def __init__(self, keyword='smart_filters', multiple_separator=',', json_identifiers=None):
        self.keyword = keyword
        self.separator = multiple_separator
        self.json_identifiers = set(json_identifiers) if json_identifiers else {'[', '{'}

    def setup(self, app):  # pragma: no cover
        """Make sure that other installed plugins don't affect the same
        keyword argument and check if metadata is available.
        """

        for other in app.plugins:
            if not isinstance(other, SmartFiltersPlugin):
                continue
            if other.keyword == self.keyword:
                raise bottle.PluginError("Found another plugin "
                                         "with conflicting settings ("
                                         "non-unique keyword).")

    def apply(self, callback, context):  # pragma: no cover
        """Implement bottle.py API version 2 `apply` method.
        """
        assert context

        def _wrapper(*args, **kwargs):
            """Decorated Injection
            """
            setattr(bottle.request.query, 'smart_filters',
                    lambda: partial(self.filter_set, bottle.request.query)())

            return callback(*args, **kwargs)

        return _wrapper

    def filter_set(self, query_data):
        """Query Filter smart guessing functionality.
        Args:
            query_data (object): A `bottle.FormsDict` instance.
        Returns:
            A dictionary mapping of querystring names -> smart guessed values (if possible or just the values)
        """

        request_data = dict(query_data.iteritems())

        request_filters = {}

        if not request_data:
            return {}

        for alias, value in request_data.items():

            if self.separator not in value or set(value).intersection(self.json_identifiers):
                try:
                    request_filters[alias] = ujson.loads(value)
                except ValueError:
                    request_filters[alias] = value
            else:

                value_list = [val.strip() for val in value.split(self.separator)]
                try:
                    request_filters[alias] = [ujson.loads(val) for val in value_list]

                except ValueError:
                    request_filters[alias] = value_list

        return request_filters


class RestFilter(object):
    def __init__(self, db_session, model, serializer):
        self.db_session = db_session
        self.model = model
        self.serializer = serializer

    def filters(self):
        filter_spec = self.__get_uri_query()
        query = self.db_session.query(self.model)
        try:
            filtered_query = apply_filters(query, filter_spec)
        except Exception as e:
            raise HTTPResponse(status=200, body=e.args)
        result = Paginate(filtered_query, self.serializer)
        return result

    def __get_uri_query(self):
        try:
            filters = bottle.request.query.smart_filters()
            filter_spec = filters.get("filters")
            filter_spec = ast.literal_eval(filter_spec)
        except Exception as e:
            raise HTTPResponse(status=404, body="url_is_not_valid")
        return filter_spec


def get_params_from_url(params: list):
    fields_dict = {}
    for param in params:
        search_field = bottle.request.query.smart_filters().get(param)
        if search_field:
            fields_dict[str(param)] = str(search_field.encode("ISO-8859-1").decode("utf-8"))
        else:
            raise HTTPResponse(status=403, body="not_valid_field")
    return fields_dict


def get_query_from_url(query: str):
    filter_query = bottle.request.query[query]
    query = ast.literal_eval(filter_query.encode("ISO-8859-1").decode("utf-8"))
    return query


class MongoFilter(object):
    def __init__(self, model, query, mongo_filter_query):
        self.query = query
        self.model = model
        self.mongo_filter_query = mongo_filter_query

    def filter(self):
        try:
            result = self.model.mongoquery(self.query).query(**self.mongo_filter_query).end()
            return result
        except Exception as e:
            raise HTTPError(403, e.args)
