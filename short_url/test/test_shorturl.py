import time
import datetime
import json
import unittest
import psutil as psutil
import requests
from subprocess import Popen, PIPE
from api.api import is_valid


class ShortUrlTest(unittest.TestCase):

    server_pid = 0

    @classmethod
    def setUpClass(cls):
        server = Popen(['python', '..\\app\\service.py'], stdout=PIPE, stderr=PIPE)
        cls.server_pid = server.pid
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        parent = psutil.Process(cls.server_pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()

    # Scenarios
    def test_valid_short_code(self):
        response = requests.post("http://localhost:5000/urls", json={'url': 'http://example.com', 'code': 'test01'})
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual({'code': 'test01'}, json.loads(response.text))

    def test_not_valid_short_code(self):
        response = requests.post("http://localhost:5000/urls", json={'url': 'http://example1.com', 'code': 'long_code'})
        self.assertEqual(response.status_code, 412)
        self.assertFalse(is_valid("long_code"))

    def test_existent_short_code(self):
        response = requests.post("http://localhost:5000/urls", json={'url': 'http://example2.com', 'code': 'test02'})
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual({'code': 'test02'}, json.loads(response.text))

        response = requests.post("http://localhost:5000/urls", json={'url': 'http://example2.com', 'code': 'test02'})
        # short code is already in use.
        self.assertEqual(response.status_code, 409)

    def test_without_short_code(self):
        response = requests.post("http://localhost:5000/urls", json={'url': 'http://example3.com'})
        self.assertEqual(response.status_code, 201)
        new_code = json.loads(response.text)['code']
        self.assertTrue(is_valid(new_code))
        self.assertDictEqual({'code': new_code}, json.loads(response.text))

    def test_get_url_from_valid_short_code(self):
        response = requests.post("http://localhost:5000/urls", json={'url': 'http://example4.com', 'code': 'test04'})
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual({'code': 'test04'}, json.loads(response.text))
        response = requests.get("http://localhost:5000/test04")
        self.assertEqual(response.text, "Location: http://example4.com")

    def test_get_url_from_not_valid_short_code(self):
        response = requests.get("http://localhost:5000/test05")
        self.assertEqual(response.status_code, 400)

    def test_url_stats(self):
        response = requests.post("http://localhost:5000/urls", json={'url': 'http://example6.com', 'code': 'test06'})
        created_at = datetime.datetime.utcnow().isoformat()
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual({'code': 'test06'}, json.loads(response.text))

        response = requests.get("http://localhost:5000/test06")
        time.sleep(2)
        response = requests.get("http://localhost:5000/test06")
        time.sleep(2)
        response = requests.get("http://localhost:5000/test06")
        last_usage = datetime.datetime.utcnow().isoformat()

        response = requests.get("http://localhost:5000/test06/stats")
        json_resp = json.loads(response.text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_resp['url'], "http://example6.com")
        self.assertEqual(json_resp['usage_count'], 3)
        self.assertTrue(json_resp['created_at'] <= created_at)
        self.assertTrue(json_resp['last_usage'] <= last_usage)

    def test_url_stats_with_wrong_short_code(self):
        response = requests.get("http://localhost:5000/invalid_code/stats")
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
