import json
from webtest import TestApp
from .core_manager import Core


class APIResponse(object):
    def __init__(self):
        self.status = None
        self.status_code = None
        self.json = None
        self.body = None


class Client(object):
    def __init__(self):
        self.test_core = TestApp(Core().execute_wsgi())

    def get_api(self, api_url):
        response = APIResponse()
        __api_url = str(api_url)
        response.json = json.dumps(self.test_core.get(__api_url).json)
        response.status = self.test_core.get(__api_url).status
        response.status_code = self.test_core.get(__api_url).status_code
        response.body = self.test_core.get(__api_url).body
        return response

    def post_api(self, api_url, data):
        response = APIResponse()
        __api_url = str(api_url)
        response.json = json.dumps(self.test_core.post_json(__api_url, params=data).json)
        response.status = self.test_core.post_json(__api_url, params=data).status
        response.status_code = self.test_core.post_json(__api_url, params=data).status_code
        response.body = self.test_core.post_json(__api_url, params=data).body
        self.test_core.post_json()
        return response

# TODO : PUT PATCH DELETE AND FILES
