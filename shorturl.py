import utils
from models import (
    db,
    URL,
    Stats
)
from flask import (
    Flask,
    jsonify,
    redirect
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
    """Save URLs"""
    return jsonify(code="abc123"), 201


@app.route('/<code>/stats', methods=['GET'])
def url_stats(code: str):
    """Shows stats for a given code"""
    return jsonify(data={}), 200


@app.route('/<code>', methods=['GET'])
def url_get(code: str):
    """Redirects to a URL given a code else 404"""
    return redirect("http://ddg.gg/", code=302)
