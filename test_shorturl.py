import json
import utils
import datetime
import unittest
from shorturl import app


def cmp_dt(dt_a: str, dt_b: str) -> bool:
    dt_a = datetime.datetime.strftime(
        datetime.datetime.strptime(
            dt_a, '%Y-%m-%dT%H:%M:%S.%f'
        ), '%Y-%m-%dT%H:%M:%S'
    )
    dt_b = datetime.datetime.strftime(
         dt_b, '%Y-%m-%dT%H:%M:%S'
    )
    return dt_a == dt_b


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

    def test_url_get_302(self):
        post = self.app.post('/urls',
                                 data=json.dumps({
                                     "url": self.data["url"]
                                 }),
                                 content_type='application/json')
        code = post.json["code"]
        response = self.app.get(f"/{code}",
                                follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_url_get_404(self):
        code = "err404"
        response = self.app.get(f"/{code}",
                                follow_redirects=False)
        self.assertEqual(response.status_code, 404)

    def test_url_stats_200(self):
        now = utils.now()
        post = self.app.post('/urls',
                                 data=json.dumps({
                                     "url": self.data["url"]
                                 }),
                                 content_type='application/json')
        code = post.json["code"]
        usage_expected = 5
        for i in range(usage_expected):
            self.app.get(f"/{code}",
                         follow_redirects=False)
            now_usage = utils.now()

        response = self.app.get(f"/{code}/stats")

        self.assertEqual(response.json["usage_count"],
                         usage_expected)
        self.assertTrue(cmp_dt(response.json["created_at"],
                               now))
        self.assertTrue(cmp_dt(response.json["last_usage"],
                               now_usage))


    def test_url_stats_404(self):
        response = self.app.get("/err404/stats")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
