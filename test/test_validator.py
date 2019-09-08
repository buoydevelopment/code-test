from unittest.mock import MagicMock
from shorter_app.repositories import ShorterRepository
from shorter_app.validator import (
    Validator,
    ERROR_INVALID_URL,
    ERROR_DUPLICATED_CODE,
    ERROR_INVALID_CODE,
    ERROR_URL_IS_REQUIRED,
)


class TestValidator:
    def test_generate_code(self):
        assert Validator().is_valid_code("ABC123")
        assert Validator().is_valid_code("abc123")
        assert Validator().is_valid_code("123456")
        assert Validator().is_valid_code("ABCDEF")
        assert Validator().is_valid_code("abcdef")
        assert not Validator().is_valid_code("xxx")
        assert not Validator().is_valid_code("xxxxxxxx")
        assert not Validator().is_valid_code("!@@$")

        assert not Validator().is_valid_code("")
        assert not Validator().is_valid_code(None)


class TestvalidateURL:
    def test_validate_url(self):
        error, status_code = Validator().validate_url("http://url.com")
        assert not error
        assert not status_code

    def test_validate_missing_url(self):
        error, status_code = Validator().validate_url("")
        assert error.get("Error") == ERROR_URL_IS_REQUIRED
        assert status_code == 400

    def test_validate_wrong_url(self):
        error, status_code = Validator().validate_url("XXX")
        assert error.get("Error") == ERROR_INVALID_URL
        assert status_code == 400


class TestvalidateCode:
    def test_validate_code(self):
        error, status_code = Validator().validate_code("ABCDEF")
        assert not error
        assert not status_code

    def test_validate_missing_code(self):
        error, status_code = Validator().validate_code("")
        assert error.get("Error") == ERROR_INVALID_CODE
        assert status_code == 400

    def test_validate_wrong_code(self):
        error, status_code = Validator().validate_code("XXX")
        assert error.get("Error") == ERROR_INVALID_CODE
        assert status_code == 400

    def test_validate_duplicated_code(self, mocker):
        query_mock = MagicMock()
        repository_get_mock = mocker.patch.object(
            ShorterRepository, "get", return_value=query_mock
        )
        error, status_code = Validator().validate_code("123456")
        assert error.get("Error") == ERROR_DUPLICATED_CODE
        assert status_code == 409
        repository_get_mock.assert_called_once_with("123456")
