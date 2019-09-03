import re
from unittest.mock import MagicMock
from shorter_app.repositories import ShorterRepository, StatsRepository
from shorter_app.apis.shorter_api import generate_shortcode, Url, UrlItem, StatsItem
from shorter_app.validator import Validator
from shorter_app.models import Shorter, Stats
from shorter_app.validator import (
    ERROR_URL_IS_REQUIRED,
    ERROR_DUPLICATED_CODE,
    ERROR_INVALID_URL,
    ERROR_INVALID_CODE,
)


class TestApi:
    def test_generate_code(self):
        code = generate_shortcode()
        assert len(code) == 6
        assert re.match("^[a-zA-Z0-9_]+$", code)

    def test_get_shorter_list(self, mocker):
        shorter_get_all_mock = mocker.patch.object(
            ShorterRepository, "get_all",
            return_value=[Shorter("url1", "code1"),
                          Shorter("url2", "code2")]
        )
        url_api = Url()
        response, status_code = url_api.get()
        assert status_code == 200
        assert len(response.get("shorter_list")) == 2
        shorter_get_all_mock.assert_called_once_with()

    def test_post_shorter_item(self, mocker):
        api_mock = MagicMock()
        api_mock.payload = dict(url="http://url.com", code="123456")
        url_api = Url(api=api_mock)
        validate_url_mock = mocker.patch.object(Validator, "validate_url")
        validate_url_mock.return_value = None, None
        validate_code_mock = mocker.patch.object(Validator, "validate_code")
        validate_code_mock.return_value = None, None
        shorter_mock = mocker.patch.object(
            Shorter, "__init__", return_value=None
        )
        # shorter_mock2 = mocker.patch("shorter_app.apis.shorter_api.Shorter")
        stats_mock = mocker.patch.object(
            Stats, "__init__", return_value=None
        )
        shorter_repository_add_mock = mocker.patch.object(
            ShorterRepository, "add"
        )
        stats_repository_add_mock = mocker.patch.object(
            StatsRepository, "add"
        )
        response, status_code = url_api.post()
        assert response.get("code")
        assert 201 == status_code
        # shorter_mock2.assert_called_once_with(url="http://url.com", code="123456")
        shorter_mock.assert_called_once_with(url="http://url.com", code="123456")
        # datetime.now is not possible to test due the current time offset.
        # stats_mock.assert_called_once_with(response.get("code"), datetime.now())
        validate_url_mock.assert_called_once_with("http://url.com")
        validate_code_mock.assert_called_once_with("123456")

        # TODO fix this calls
        #shorter_repository_add_mock.assert_called_once_with(shorter_mock.result_value)
        #stats_repository_add_mock.assert_called_once_with(stats_mock)

    def test_post_invalid_code(self, mocker):
        api_mock = MagicMock()
        api_mock.payload = dict(url="http://url.com", code="1")
        url_api = Url(api=api_mock)
        validate_url_mock = mocker.patch.object(Validator, "validate_url")
        validate_url_mock.return_value = None, None
        validate_code_mock = mocker.patch.object(Validator, "validate_code")
        validate_code_mock.return_value = {"Error": ERROR_INVALID_CODE}, 400

        response, status_code = url_api.post()
        assert response.get("Error") == ERROR_INVALID_CODE
        assert 400 == status_code
        validate_url_mock.assert_called_once_with("http://url.com")
        validate_code_mock.assert_called_once_with("1")

    def test_post_invalid_url(self, mocker):
        api_mock = MagicMock()
        api_mock.payload = dict(url="XXX", code="123456")
        url_api = Url(api=api_mock)
        validate_url_mock = mocker.patch.object(Validator, "validate_url")
        validate_url_mock.return_value = {"Error": ERROR_INVALID_URL}, 400
        response, status_code = url_api.post()
        assert response.get("Error") == ERROR_INVALID_URL
        assert 400 == status_code
        validate_url_mock.assert_called_once_with("XXX")

    def test_post_missing_url(self, mocker):
        api_mock = MagicMock()
        api_mock.payload = dict(code="123456")
        url_api = Url(api=api_mock)
        validate_url_mock = mocker.patch.object(Validator, "validate_url")
        validate_url_mock.return_value = {"Error": ERROR_URL_IS_REQUIRED}, 400
        response, status_code = url_api.post()
        assert response.get("Error") == ERROR_URL_IS_REQUIRED
        assert 400 == status_code
        validate_url_mock.assert_called_once_with(None)

    def test_post_duplicated_item(self, mocker):
        api_mock = MagicMock()
        api_mock.payload = dict(url="http://url.com", code="123456")
        url_api = Url(api=api_mock)
        validate_url_mock = mocker.patch.object(Validator, "validate_url")
        validate_url_mock.return_value = None, None
        validate_code_mock = mocker.patch.object(Validator, "validate_code")
        validate_code_mock.return_value = {"Error": ERROR_DUPLICATED_CODE}, 409
        response, status_code = url_api.post()
        assert response.get("Error") == ERROR_DUPLICATED_CODE
        assert 409 == status_code
        validate_url_mock.assert_called_once_with("http://url.com")
        validate_code_mock.assert_called_once_with("123456")

    def test_generate_code(self, mocker):
        api_mock = MagicMock()
        api_mock.payload = dict(url="http://url.com")
        url_api = Url(api=api_mock)
        validate_url_mock = mocker.patch.object(Validator, "validate_url")
        validate_url_mock.return_value = None, None
        with mocker.patch('shorter_app.apis.shorter_api.generate_shortcode') as generate_shortcode_mock:
            generate_shortcode_mock.return_value  = "111111"

            shorter_mock = mocker.patch.object(
                Shorter, "__init__", return_value=None
            )
            # shorter_mock2 = mocker.patch("shorter_app.apis.shorter_api.Shorter")
            stats_mock = mocker.patch.object(
                Stats, "__init__", return_value=None
            )
            shorter_repository_add_mock = mocker.patch.object(
                ShorterRepository, "add"
            )
            stats_repository_add_mock = mocker.patch.object(
                StatsRepository, "add"
            )
            response, status_code = url_api.post()
            assert response.get("code")
            assert 201 == status_code
            # shorter_mock2.assert_called_once_with(url="http://url.com", code="123456")
            shorter_mock.assert_called_once_with(url="http://url.com")
            # datetime.now is not possible to test due the current time offset.
            # stats_mock.assert_called_once_with(response.get("code"), datetime.now())
            validate_url_mock.assert_called_once_with("http://url.com")
            generate_shortcode_mock.assert_called_once_with()
            # TODO fix this calls
            # shorter_repository_add_mock.assert_called_once_with(shorter_mock.result_value)
            # stats_repository_add_mock.assert_called_once_with(stats_mock)

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
