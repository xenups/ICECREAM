import json
import rootpath
import unittest

rootpath.append()
from ICECREAM.test import Client


class TestFunctions(unittest.TestCase):
    def test_hello_world(self):
        excepted_response = json.dumps({'result': 'hello world'})
        response = Client().get_api('/hello')

        self.assertEqual(excepted_response, response.json)
        self.assertEqual(200, response.status_code)

    def test_add_room(self):
        post_data = {
            "name": "ghazvin"
        }
        response = Client().post_api('/addroom', data=post_data)
        self.assertEqual(200, response.status_code)

    def test_get_rooms(self):
        response = Client().get_api('/getrooms')
        print(response.json)
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
