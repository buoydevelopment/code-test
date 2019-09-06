import random
import string
from flask import redirect
from flask_restplus import Namespace, Resource, fields, marshal
from shorter_app.models import Shorter, Stats
from shorter_app.repositories import ShorterRepository, StatsRepository
from shorter_app.validator import Validator, ERROR_CODE_NOT_FOUND

from datetime import datetime

api = Namespace("shorter", description="Shorter App")


def get_current_time():
    return datetime.now()


def generate_shortcode():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))


@api.route("/healthcheck/")
class HealtCheck(Resource):
    def get(self):
        return {"Service": "OK"}


request_shorter_url = api.model(
    "Post Short URL (Request)",
    {
        "code": fields.String,
        "url": fields.String,
    },
)

response_shorter_url = api.model(
    "Get Short URL list (Response)",
    {
        "code": fields.String,
        "url": fields.String,
    },
)

response_stats = api.model(
    "Get Stats(Response)",
    {
        "created_at": fields.String,
        "last_usage": fields.String,
        "usage_count": fields.String,
    },
)


@api.route("/urls/")
class Url(Resource):
    @api.doc("Get short url")
    # TODO update response_shorter_url
    @api.response(200, "Get Short URL list", response_shorter_url)
    @api.response(401, "Unauthorized")
    @api.response(400, "Bad Request")
    def get(self):
        shorter_list = ShorterRepository.get_all()
        return marshal(shorter_list, response_shorter_url), 200

    @api.doc("Post short url")
    @api.expect(request_shorter_url)
    @api.response(401, "Unauthorized")
    @api.response(400, "Bad Request")
    @api.response(409, "Duplicated code")
    @api.response(201, "Short URL Created", response_shorter_url)
    def post(self):
        url = self.api.payload.get("url")
        code = self.api.payload.get("code")

        error, status_code = Validator().validate_url(url)
        if error:
            return error, status_code

        if code:
            error, status_code = Validator().validate_code(code)
            if error:
                return error, status_code
        else:
            code = generate_shortcode()
        shorter = Shorter(url=url, code=code)
        ShorterRepository.add(shorter)
        created_at = get_current_time()
        stats = Stats(code, created_at)
        StatsRepository.add(stats)
        return marshal(shorter, response_shorter_url), 201


@api.route("/urls/<string:code>/")
class UrlItem(Resource):
    @api.doc("Get short url by code")
    @api.response(200, "Get Short URL list", response_shorter_url)
    @api.response(401, "Unauthorized")
    @api.response(404, "Not Found")
    def get(self, code):
        result = ShorterRepository.get(code)

        if not result:
            return {"Error": ERROR_CODE_NOT_FOUND}, 404
        stats = StatsRepository.get(code)
        stats.usage_count += 1
        stats.last_usage = get_current_time()
        StatsRepository.commit()
        return redirect(result.url)


@api.route("/urls/<string:code>/stats/")
class StatsItem(Resource):
    @api.doc("Get code stast")
    @api.response(200, "Get Short URL stasts", response_stats)
    @api.response(401, "Unauthorized")
    @api.response(404, "Not Found")
    def get(self, code):
        result = StatsRepository.get(code)
        if not result:
            return {"Error": ERROR_CODE_NOT_FOUND}, 404

        return marshal(result, response_stats), 200
