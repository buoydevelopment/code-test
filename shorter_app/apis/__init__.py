from flask_restplus import Api

from shorter_app.apis.shorter_api import api as shorter_api

api = Api(title="Shorter API", version="1.0", description="Shorter API")

api.add_namespace(shorter_api)
