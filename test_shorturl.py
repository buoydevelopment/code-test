import os
import unittest
from shorturl import app

class ShorturlTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()
        self.assertEqual(app.debug, True)

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/', follow_redirects = True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
