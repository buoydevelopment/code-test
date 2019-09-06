from flask import Flask
from shorter_app.apis import api
from shorter_app.config import DefaultConfig
from shorter_app.database import db_session, init_db


def create_app(config=DefaultConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    api._doc = app.config.get("SWAGGER_DOC_PATH")
    api.init_app(
        app,
        title="Shorter Application",
        version="0.0.1",
        description="Microservice for translate URL in a shorter URL",
    )

    init_db()

    @app.teardown_request
    def teardown_request(request):
        db_session.remove()

    return app
