import utils
import unittest


class UtilsTests(unittest.TestCase):
    def setUp(self):
        utils.create_tables()
        self.data = {
            "url": "https://ddg.gg/",
            "code": utils.gen_code(),
        }

    def tearDown(self):
        utils.drop_tables()

    def test_is_valid_url(self):
        self.assertEqual(
            utils.is_valid_url(self.data["url"]),
            True
        )

    def test_is_valid_code(self):
        self.assertEqual(
            utils.is_valid_code(self.data["code"]),
            True
        )

    def test_gen_code(self):
        code = utils.gen_code()
        self.assertEqual(len(code), 6)
        self.assertEqual(utils.is_valid_code(code), True)

    def test_insert_url(self):
        url_id = utils.insert_url(
            self.data["url"],
            self.data["code"]
        )
        self.assertEqual(isinstance(url_id, int), True)

    def test_stats(self):
        _id = utils.insert_url(
            self.data["url"],
            self.data["code"]
        )
        for i in range(1,5):
            utils.bump_stats(_id)
            created_at, last_usage, usage_count = utils.get_stats(
                self.data["code"]
            )
            self.assertEqual(usage_count, i)

    def test_code_exists_true(self):
        utils.insert_url(
            self.data["url"],
            self.data["code"]
        )
        _, exists = utils.code_exists(self.data["code"])
        self.assertEqual(exists, True)

    def test_code_exists_false(self):
        _, exists = utils.code_exists("abc123")
        self.assertEqual(exists, False)

    def test_date_iso8601(self):
        now = utils.now()
        now_iso8601 = now.isoformat()

        self.assertEqual(
            utils.to_iso8601(str(now)),
            now_iso8601
        )


if __name__ == "__main__":
    unittest.main()
