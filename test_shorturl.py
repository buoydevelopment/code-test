import json
import utils
import unittest
from shorturl import app


class ShorturlTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()
        utils.create_tables()
        self.data = {
            "url": "https://ddg.gg/",
            "code": utils.gen_code(),
        }
        self.assertEqual(app.debug, True)

    def tearDown(self):
        utils.drop_tables()

    def test_index(self):
        response = self.app.get('/',
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # def test_url_get_ok(self):
    #     response = self.app.get('/abc123',
    #                             follow_redirects=False)
    #     self.assertEqual(response.status_code, 302)

    # def test_url_get_err(self):
    #     response = self.app.get('/abc123',
    #                             follow_redirects=False)
    #     self.assertEqual(response.status_code, 302)

    # def test_url_stats(self):
    #     response = self.app.get('/abc123/stats',
    #                             follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)

    def test_url_post_201(self):
        response = self.app.post('/urls',
                                 data=json.dumps(self.data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["code"], self.data["code"])

    def test_url_post_201_nocode(self):
        response = self.app.post('/urls',
                                 data=json.dumps({
                                     "url": self.data["url"]
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(len(response.json["code"]) == 6)

    def test_url_post_400(self):
        response = self.app.post('/urls',
                                 data=json.dumps({}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_url_post_409_code(self):
        response = self.app.post('/urls',
                                 data=json.dumps({
                                     "url": self.data["url"],
                                     "code": "this will fail"
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_url_post_409_url(self):
        response = self.app.post('/urls',
                                 data=json.dumps({
                                     "url": "http://lalala",
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_url_post_422(self):
        self.app.post('/urls',
                      data=json.dumps(self.data),
                      content_type='application/json')
        response = self.app.post('/urls',
                                 data=json.dumps(self.data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
