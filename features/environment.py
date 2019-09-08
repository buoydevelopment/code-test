import os
import tempfile
from behave import fixture, use_fixture

from shorter_app.app import create_app
from shorter_app.database import init_db
from shorter_app.config import TestConfig


@fixture
def shorter_client(context, *args, **kwargs):
    app = create_app(TestConfig)
    context.db, app.config["DATABASE"] = tempfile.mkstemp()
    app.testing = True
    context.client = app.test_client()
    with app.app_context():
        init_db()
    yield context.client
    # -- CLEANUP:
    os.close(context.db)
    os.unlink(app.config["DATABASE"])


def before_feature(context, feature):
    use_fixture(shorter_client, context)
