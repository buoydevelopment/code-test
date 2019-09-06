import logging


class FixedConfig:
    DEBUG = False
    TESTING = False
    JSON_AS_ASCII = False
    USE_FILE_LOGGING = True
    LOG_LOCATION = "./log/shorter.log"
    LOG_MAX_BYTES = 100000
    LOG_BACKUP_COUNT = 2
    LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    LOG_LEVEL = logging.DEBUG
    SQLALCHEMY_ECHO = False
    DATABASE_NAME = "shorter"
    USE_API_STUBS = False
    INTERNAL_API_TIMEOUT = 3.5
    SWAGGER_DOC_PATH = "/documents/"


class DefaultConfig(FixedConfig):
    SERVER_NAME = "localhost:5000"
    ENVIRONMENT_NAME = "development"
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/app.db"
    BASE_URL = ""


class TestConfig(FixedConfig):
    SERVER_NAME = "localhost:5000"
    ENVIRONMENT_NAME = "local_test"
    SQLALCHEMY_DATABASE_URI = ""
    USE_LOCAL_MOCK_SERVER = True
    BASE_URL = "shorter"
