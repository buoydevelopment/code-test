import utils
from flask import (
    Flask,
    jsonify,
    request,
    redirect,
)


app = Flask(__name__)


##
# Flask commands
# drop-tables
# create-tables
#

@app.cli.command()
def drop_tables():
    """Use PeeWee to drop tables."""
    utils.drop_tables()


@app.cli.command()
def create_tables():
    """Use PeeWee to create tables."""
    utils.create_tables()


##
# Flask endpoints
# index
# url_get
# url_stats
# url_post
#

@app.route('/', methods=['GET'])
def index():
    """Home"""
    endpoints = {
        "/urls": "POST -> url:str:required, code:str:optional",
        "/<code>": "GET -> code:str:required",
        "/<code>/stats": "GET -> code:str:required"
    }

    return jsonify(endpoints=endpoints)


@app.route('/urls', methods=['POST'])
def url_post():
    """Saves URLs if ok, else wont (?)"""
    data = request.json.copy()
    if "url" not in list(data.keys()):
        return jsonify(error="URL not provided"), 400

    else:
        if "code" not in list(data.keys()):
            code = utils.gen_code()
        else:
            code = data.get('code')
            if not utils.is_valid_code(code):
                return jsonify(error="Code not valid"), 409

        _, exists = utils.code_exists(code)
        if exists:
            return jsonify(error="Code in use"), 422
        else:
            if utils.is_valid_url(data.get('url')):
                utils.insert_url(data.get('url'), code)
            else:
                return jsonify(error="URL not valid"), 409

        return jsonify(code=code), 201


@app.route('/<code>/stats', methods=['GET'])
def url_stats(code: str):
    """Shows stats for a given code"""
    _, exists = utils.code_exists(code)
    if not exists:
        return jsonify(error="Code Not Found"), 404
    else:
        created_at, last_usage, usage_count = utils.get_stats(
            code
        )

        result = {
            'created_at': utils.to_iso8601(created_at),
            'usage_count': usage_count
        }
        if last_usage:
            result['last_usage'] = utils.to_iso8601(last_usage)

        return jsonify(result), 200



@app.route('/<code>', methods=['GET'])
def url_get(code: str):
    """Redirects to a URL given a code else 404"""
    q, exists = utils.code_exists(code)
    if exists:
        url_id, url = q.execute().cursor.fetchone()
        utils.bump_stats(url_id)
        return redirect(url, code=302)

    else:
        return jsonify(error="Code Not Found"), 404

