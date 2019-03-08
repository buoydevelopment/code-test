import json
import api.api
from flask import Flask, request

app = Flask(__name__)


# Error handler when path is not available.
@app.errorhandler(404)
def not_found():
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = json.dumps(message)
    resp.status_code = 404
    return resp

# By default, all methods accepts GET requests. We need to specify that short_url() will receive POST requests.
api.api.short_url.methods = ['POST']


def main():
    # Registering main server functions.
    app.add_url_rule('/urls', 'urls', view_func=api.api.short_url)
    app.add_url_rule('/<short_name>', 'get_url', view_func=api.api.get_url)
    app.add_url_rule('/<short_name>/stats', 'stats', view_func=api.api.get_stats)
    app.run(debug=True)

    # server will run indefinitely
    while True:
        pass


if __name__ == "__main__":
    main()
