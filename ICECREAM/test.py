import json
from alembic import command
from alembic.config import Config
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
        self.core = Core(db_type='memory').execute_wsgi()
        self.test_core = TestApp(self.core)

    def migrate_in_memory(self, migrations_path, alembic_ini_path=None, connection=None, revision="head"):
        config = Config(alembic_ini_path)
        config.set_main_option('script_location', migrations_path)
        if connection is not None:
            config.attributes['connection'] = connection
        command.upgrade(config, revision)

    def get_api(self, api_url, *auth):
        response = APIResponse()
        __api_url = str(api_url)
        if auth:
            self.test_core.set_authorization(auth)
        test_core_response = self.test_core.get(__api_url)
        response.json = test_core_response.json
        response.status = test_core_response.status
        response.status_code = test_core_response.status_code
        response.body = test_core_response.body
        response.content_type = test_core_response.content_type

        return response

    def post_api(self, api_url, data, *auth):
        response = APIResponse()
        __api_url = str(api_url)
        if auth:
            self.test_core.set_authorization(auth)
        test_core_response = self.test_core.post_json(__api_url, params=data)
        response.json = json.dumps(test_core_response.json)
        response.status = test_core_response.status
        response.status_code = test_core_response.status_code
        response.body = test_core_response.body
        return response

    def patch_api(self, api_url, data, *auth):
        response = APIResponse()
        __api_url = str(api_url)
        if auth:
            self.test_core.set_authorization(auth)
        test_core_response = self.test_core.patch_json(__api_url, params=data)
        response.json = json.dumps(test_core_response.json)
        response.status = test_core_response.status
        response.status_code = test_core_response.status_code
        response.body = test_core_response.body
        return response

    def put_api(self, api_url, data, *auth):
        response = APIResponse()
        __api_url = str(api_url)
        if auth:
            self.test_core.set_authorization(auth)
        test_core_response = self.test_core.put_json(__api_url, params=data)
        response.json = json.dumps(test_core_response.json)
        response.status = test_core_response.status
        response.status_code = test_core_response.status_code
        response.body = test_core_response.body
        return response

    def delete_api(self, api_url, data, *auth):
        response = APIResponse()
        __api_url = str(api_url)
        if auth:
            self.test_core.set_authorization(auth)
        test_core_response = self.test_core.delete_json(__api_url, params=data)
        response.json = json.dumps(test_core_response.json)
        response.status = test_core_response.status
        response.status_code = test_core_response.status_code
        response.body = test_core_response.body
        return response
