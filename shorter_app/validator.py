import re
from shorter_app.repositories import ShorterRepository

ERROR_INVALID_CODE = (
    "Invalid code. The code must comply with the following restrictions: "
    "Alphanumeric string. "
    "6 chars length. "
    "Case-sensitive"
)
ERROR_DUPLICATED_CODE = "Code already registered. Try a new one"
ERROR_INVALID_URL = "An invalid URL was provided"
ERROR_CODE_NOT_FOUND = "Code was not found"
ERROR_URL_IS_REQUIRED = "URL is required"


class Validator:
    def is_valid_code(self, code):
        return code and len(code) == 6 and re.match("^[a-zA-Z0-9_]+$", code)

    def validate_url(self, url):
        if not url:
            return {"Error": ERROR_URL_IS_REQUIRED}, 400

        import validators
        if not validators.url(url):
            return {"Error": ERROR_INVALID_URL}, 400

        return None, None

    def validate_code(self, code):
        if self.is_valid_code(code):
            result = ShorterRepository.get(code)
            if result:
                return {"Error": ERROR_DUPLICATED_CODE}, 409
            else:
                return None, None
        else:
            return {"Error": ERROR_INVALID_CODE}, 400
