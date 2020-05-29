import json

from bottle import HTTPResponse as BottleHttpResponse


class HTTPResponse(BottleHttpResponse):
    default_status = 500

    def __init__(self, status=None, body=None, headers=None, exception=None, message="msg", traceback=None,
                 **options):
        self.exception = exception
        self.traceback = traceback
        self.body = self.convert_to_json(body, message)
        headers = headers or {'Content-type': 'application/json'}
        super(HTTPResponse, self).__init__(self.body, headers=headers, status=status, **options)

    @staticmethod
    def convert_to_json(body, message):
        if body is None:
            return body
        if type(body) is dict:
            return json.dumps(body)
        return json.dumps({message: body})


class HTTPError(HTTPResponse):
    pass
