import utils
import unittest
from shorturl import app


class ShorturlTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()
        utils.create_tables()

        self.test_data = {
            "url":"https://sdf.org/",
            "code": "sdforg",
            "id": 0
        }
        self.test_data["id"] = utils.insert_url(
            self.test_data["url"],
            self.test_data["code"]
        )

        print (self.test_data)

        self.assertEqual(app.debug, True)

    def tearDown(self):
        utils.drop_tables()

    def test_index(self):
        response = self.app.get('/',
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_url_get_ok(self):
        response = self.app.get('/abc123',
                                follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_url_get_err(self):
        response = self.app.get('/abc123',
                                follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_url_stats(self):
        response = self.app.get('/abc123/stats',
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_url_post_ok(self):
        response = self.app.post('/urls',
                                 data={
                                     "url": "http://ddg.gg/",
                                     "code": "ddg123"
                                 })
        self.assertEqual(response.status_code, 201)

    def test_url_post_err(self):
        response = self.app.post('/urls',
                                 data={
                                     "url": "http://ddg.gg/",
                                     "code": "wololo"
                                 })
        self.assertEqual(response.status_code, 201)

    def test_url_post_nocode(self):
        response = self.app.post('/urls',
                                 data={
                                     "url": "http://sdf.org/",
                                 })
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
