import re
import flask
from unittest.mock import MagicMock
from shorter_app.repositories import ShorterRepository, StatsRepository
from shorter_app.apis.shorter_api import generate_shortcode, Url, UrlItem, StatsItem


class TestApi:
    def test_generate_code(self):
        code = generate_shortcode()
        assert len(code) == 6
        assert re.match("^[a-zA-Z0-9_]+$", code)

    def test_get_shorter_list(self):
        url_api = Url()
        response, status_code = url_api.get()
        assert response.get("shorter_list")
        assert status_code == 200

    def test_post_shorter_item(self, mocker):
        url_api = Url()

        request_mock = mocker.patch.object(flask, "request")
        # response, status_code = url_api.post()

    def test_get_shorter_item(self, mocker):
        url_api = UrlItem()

        query_mock = MagicMock()
        repository_get_mock = mocker.patch.object(
            ShorterRepository, "get", return_value=query_mock
        )

        stats_commit_mock = mocker.patch.object(
            StatsRepository, "commit", return_value=query_mock
        )

        stats_get_mock = mocker.patch.object(
            StatsRepository, "get", return_value=query_mock
        )

        stats_get_mock.usage_count = 0
        url_api.get("123456")
        repository_get_mock.assert_called_once_with("123456")
        stats_commit_mock.assert_called_once_with()
        stats_get_mock.assert_called_once_with("123456")

    def test_get_shorter_item_not_found(self):
        url_api = UrlItem()
        response, status_code = url_api.get("XXXXXX")
        assert status_code == 404

    # TODO  complete UT for all API
