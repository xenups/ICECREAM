import bottle
from marshmallow import Schema
from ICECREAM.http import HTTPError
from sqlalchemy_filters import apply_pagination


class PaginateSchema(Schema):
    class Meta:
        fields = ("result", "count", "next", "total_results", "total_page")


class Paginate(object):
    def __new__(cls, query, serializer=None):
        page_number = bottle.request.GET.get('page') or 1
        page_size = bottle.request.GET.get('count') or 10
        query, pagination = apply_pagination(query, page_number=int(page_number),
                                             page_size=int(page_size))
        page_size, page_number, num_pages, total_results = pagination
        _next = cls.is_next_page(page_number, page_size, total_results)
        result = serializer.dump(query)
        __paginate_serializer = PaginateSchema()
        __dict_paginate = {"count": page_number, "next": _next, "total_results": total_results, "total_page": num_pages,
                           "result": result}
        __serialized_result = __paginate_serializer.dump(__dict_paginate)
        return __serialized_result

    @staticmethod
    def is_next_page(page_number, page_size, total_result):
        if total_result - (page_number * page_size) <= 0:
            return False
        return True

    @staticmethod
    def validate_response_count(count):
        if int(count) > 30:
            raise HTTPError(404, "count of page is too big")
        return int(count)
