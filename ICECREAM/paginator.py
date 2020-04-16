from marshmallow import Schema
from ICECREAM.http import HTTPError
from sqlalchemy_filters import apply_pagination


class PaginateSchema(Schema):
    class Meta:
        fields = ("result","count", "next", "total_results", "total_page")


class Paginate(object):
    def __new__(cls, query, page_number=1, page_size=10, serializer=None):
        query, pagination = apply_pagination(query, page_number=page_number,
                                             page_size=page_size)
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
