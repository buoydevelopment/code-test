import random
import string
from flask import request, redirect
from flask_restplus import Namespace, Resource
from shorter_app.models import Shorter, Stats
from shorter_app.repositories import ShorterRepository, StatsRepository
from shorter_app.validator import validate_url, validate_code, ERROR_CODE_NOT_FOUND

from datetime import datetime

api = Namespace("shorter", description="Shorter App")


def generate_shortcode():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))


@api.route("/healthcheck/")
class Healthcheck(Resource):
    def get(self):
        return {"Service": "OK"}


@api.route("/urls/")
class Url(Resource):
    @api.doc("Get shorter url")
    @api.response(200, "Get Short URL  list")
    def get(self):
        shorter_list = ShorterRepository.get_all()
        return {"shorter_list": [s.as_dict() for s in shorter_list]}, 200

    @api.doc("Post shorter url")
    @api.response(201, "Short URL Created")
    def post(self):
        content = request.json
        url = content.get("url")
        code = content.get("code")

        error, status_code = validate_url(url)
        if error:
            return error, status_code

        if code:
            error, status_code = validate_code(code)
            if error:
                return error, status_code
        else:
            code = generate_shortcode()
        shorter = Shorter(url=url, code=code)
        ShorterRepository.add(shorter)
        created_at = datetime.now()
        stats = Stats(code, created_at)
        StatsRepository.add(stats)
        return {"code": code}, 201


@api.route("/urls/<string:code>/")
class UrlItem(Resource):
    @api.doc("Get shorter url")
    def get(self, code):
        result = ShorterRepository.get(code)

        if not result:
            return {"Error": ERROR_CODE_NOT_FOUND}, 404
        stats = StatsRepository.get(code)
        stats.usage_count += 1
        stats.last_usage = datetime.now()
        StatsRepository.commit()
        return redirect(result.url)


@api.route("/urls/<string:code>/stats/")
class StatsItem(Resource):
    @api.doc("Get code stast")
    def get(self, code):
        result = StatsRepository.get(code)
        if not result:
            return {"Error": ERROR_CODE_NOT_FOUND}, 404

        return {
            "created_at": str(result.created_at),
            "last_usage": str(result.last_usage),
            "usage_count": str(result.usage_count),
        }
