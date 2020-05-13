import json
from itertools import starmap

import rootpath
import unittest

rootpath.append()
from ICECREAM.test import Client


def register_user(phone, password, roles):
    return Client().post_api('/api/user', data={
        "phone": phone,
        "password": password,
        "roles": roles,
        "person": {
            "name": "test_user",
            "last_name": "test_user",
            "email": "test@test.com"
        }
    })


def login_user(phone, password):
    return Client().post_api(api_url='/api/auth', data={
        "phone": phone,
        "password": password})


class TestFunctions(unittest.TestCase):
    # def test_register_user_without_permission(self):
    #     response = register_user(phone="09123456789", password="test", roles=["admin"])
    #     self.assertEqual(403, response.status_code)

    def test_login(self):
        response = login_user(phone="admin", password="admin")
        data = json.loads(response.json)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data["token"])

    def test_get_users(self):
        login_info = login_user(phone="admin", password="admin")
        token = json.loads(login_info.json)["token"]
        response = Client().get_api('/api/users', *('JWT', token))
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.content_type == 'application/json')

    def test_get_user(self):
        login_info = login_user(phone="admin", password="admin")
        token = json.loads(login_info.json)["token"]
        response = Client().get_api('/api/users/1', *('JWT', token))
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.content_type == 'application/json')

    def test_get_current_user(self):
        login_info = login_user(phone="admin", password="admin")
        token = json.loads(login_info.json)["token"]
        response = Client().get_api('/api/users/current', *('JWT', token))
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.content_type == 'application/json')

    def test_get_roles(self):
        login_info = login_user(phone="admin", password="admin")
        token = json.loads(login_info.json)["token"]
        response = Client().get_api('/api/roles', *('JWT', token))
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.content_type == 'application/json')

    def test_get_rules(self):
        login_info = login_user(phone="admin", password="admin")
        token = json.loads(login_info.json)["token"]
        response = Client().get_api('/api/rules', *('JWT', token))
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.content_type == 'application/json')

    def test_edit_user(self):
        data = {
            "phone": "admin",
            "password": "admin",
            "roles": ["admin", ],
            "person": {
                "name": "amir",
                "last_name": "lesani",
                "email": "folan@folan2i.com"
            }
        }
        login_info = login_user(phone="admin", password="admin")
        token = json.loads(login_info.json)["token"]
        response = Client().patch_api('/api/users/1', data, *('JWT', token))
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.content_type == 'application/json')


if __name__ == '__main__':
    unittest.main()
