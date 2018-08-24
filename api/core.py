from typing import Tuple, List
from random import sample
from werkzeug.local import LocalProxy
from flask import current_app, jsonify, make_response, redirect
from flask.wrappers import Response
import base64

# logger object for all views to use
logger = LocalProxy(lambda: current_app.logger)


class Mixin:
    """Utility Base Class for SQLAlchemy Models.

    Adds `to_dict()` to easily serialize objects to dictionaries.
    """

    def to_dict(self) -> dict:
        d_out = dict((key, val) for key, val in self.__dict__.items())
        d_out.pop("_sa_instance_state", None)
        d_out["_id"] = d_out.pop("id", None)  # rename id key to interface with response
        return d_out


def create_response(data = None, status: int = 200) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.

    :param data <Code Obj> Code found
    :param status <int> optional status code, defaults to 200
    :returns tuple of Flask Response and int
    """
    if data is None:
        raise AssertionError('Shortcode Not Found', 404)

    if status == 302:
        response = make_response(jsonify({'url': data.url}))
        response.status_code = status
        response.headers['Location'] = data.url
        response.headers['Content-Type'] = 'application/json'

    if status == 201:
        response = jsonify({'code': base64.urlsafe_b64encode(data.code.encode()).decode('ascii')})

    if status == 200:
        stats = {'created_at': data.created_at.isoformat() + 'Z'}
        if data.last_usage:
            stats['last_usage'] = data.last_usage.isoformat() + 'Z'
        stats['usage_count'] = data.usage
        response = jsonify(stats)

    if status >= 400:
        response = jsonify(data)

    return response, status


def serialize_list(items: List) -> List:
    """Serializes a list of SQLAlchemy Objects, exposing their attributes.

    :param items - List of Objects that inherit from Mixin
    :returns List of dictionaries
    """
    if not items or items is None:
        return []
    return [x.to_dict() for x in items]


# add specific Exception handlers before this, if needed
def all_exception_handler(error: Exception) -> Tuple[Response, int]:
    """Catches and handles all exceptions, add more specific error Handlers.
    :param Exception
    :returns Tuple of a Flask Response and int
    """
    try:
        status = error.args[1]
        message = error.args[0]
    except IndexError:
        status = 500
        message = error
    return jsonify({'error': str(message)}), status

def generate_code():
    """Generate a 6 Alphanumeric code"""
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    code = ''.join(sample(characters, 6))
    return code
