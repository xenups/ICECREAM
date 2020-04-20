import json
from webtest import TestApp
from .core_manager import Core


class APIResponse(object):
    def __init__(self):
        self.status = None
        self.status_code = None
        self.json = None
        self.body = None
        self.content_type = None


class Client(object):
    def __init__(self):
        self.test_core = TestApp(Core().execute_wsgi())

    def get_api(self, api_url, *auth):
        response = APIResponse()
        __api_url = str(api_url)
        if auth:
            self.test_core.set_authorization(auth)
        response.json = json.dumps(self.test_core.get(__api_url).json)
        test_core_response = self.test_core.get(__api_url)
        response.status = test_core_response.status
        response.status_code = test_core_response.status_code
        response.body = test_core_response.body
        response.content_type = test_core_response.content_type

        return response

    def post_api(self, api_url, data, auth=None):
        response = APIResponse()
        __api_url = str(api_url)
        if auth:
            self.test_core.set_authorization('JWT', auth)
        response.json = json.dumps(self.test_core.post_json(__api_url, params=data).json)
        response.status = self.test_core.post_json(__api_url, params=data).status
        response.status_code = self.test_core.post_json(__api_url, params=data).status_code
        response.body = self.test_core.post_json(__api_url, params=data).body
        return response

# TODO : PUT PATCH DELETE AND FILES
