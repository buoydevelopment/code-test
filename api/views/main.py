from flask import Blueprint, request
from api.models import Code, db
from api.core import create_response, serialize_list, logger
import base64

main = Blueprint("main", __name__)

# POST /urls
# Content-Type: "application/json"
# {
#   "url": "http://example.com",
#   "code": "example"
# }
#
# Response
#
# 201 Created
# Content-Type: "application/json"
#
# {
#   "code": :shortcode
# }
#
# Errors
# Bad Request: If ```url``` is not present
# Conflict: If the the desired shortcode is already in use.
# Unprocessable Entity: If the shortcode doesn't doesn't comply with its description.
@main.route("/urls", methods=["POST"])
def post_url():
    data = request.get_json()
    shortcode = Code(**data)
    db.session.add(shortcode)
    db.session.commit()
    return create_response(shortcode, status=201)


# GET /:code
# Content-Type: "application/json"
# @param: code
#
# Response
#
# HTTP/1.1 302 Found
# Location: http://www.example.com
#
# Errors
# Not Found: If the `shortcode` cannot be found
@main.route("/<code>", methods=["GET"])
def get_url(code):
    code = base64.urlsafe_b64decode(code).decode('ascii')
    shortcode = Code.query.filter_by(code=code).first()
    if shortcode:
        shortcode.usage += 1
        db.session.commit()
    return create_response(shortcode, status=302)

# GET /:code/stats

# GET /:code/stats
# Content-Type: "application/json"
# @param: code
#
# Response
#
# 200 OK
# Content-Type: "application/json"
#
# {
#   "created_at": "2012-04-23T18:25:43.511Z",
#   "last_usage": "2012-04-23T18:25:43.511Z",
#   "usage_count": 1
# }
#
# start_date: [ISO8601](http://en.wikipedia.org/wiki/ISO_8601) formatted date when the shortened URL was created
# usage_count: Number of requests to the endpoint `GET /code`
# last_usage: Date of the last time the shortened URL was requested. Not included if it has never been requested.
#
# Errors
# Not Found: If the `shortcode` cannot be found
@main.route("/<code>/stats", methods=["GET"])
def get_url_stats(code):
    code = base64.urlsafe_b64decode(code).decode('ascii')
    shortcode = Code.query.filter_by(code=code).first()
    return create_response(shortcode)
