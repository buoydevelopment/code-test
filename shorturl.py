from flask import (
    Flask,
    jsonify,
    redirect
)


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Home"""
    return jsonify(endpoints={}), 200


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
