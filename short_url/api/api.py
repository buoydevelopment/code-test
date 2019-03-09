import re
import random
import string
import json
import datetime
from flask import Response, request


# global variables
stored_urls = {}
letters_and_digits = string.ascii_letters + string.digits


def is_valid(short_code):
    """ Checks if short_code complies with requirements: alphanumeric and length = 6."""
    return re.match(r'[A-Za-z0-9]', short_code) and len(short_code) == 6


def exist(short_code):
    """ Checks if short_code is already in use."""
    return short_code in stored_urls.keys()


def generate_random_code(string_length=6):
    """ Generates a random alphanumeric string. """
    global letters_and_digits
    return ''.join(random.choice(letters_and_digits) for i in range(string_length))


def short_url():
    """ Relates a short alphanumeric code which will represents a long url."""
    content = request.get_json()
    print json.dumps(content)
    # checks if code is missing. If yes, a new code is generated.
    if 'code' in content.keys():
        # validate short code
        if is_valid(content['code']):
            if not exist(content['code']):
                short_code = content['code']
            else:
                return "Short code is already in use", 409
        else:
            return "Precondition failed", 412
    else:
        short_code = generate_random_code()
        print short_code

    # creates new element
    new_url_item = {
        'url': content['url'],
        'created_at': datetime.datetime.utcnow().isoformat(),
        'last_usage': datetime.datetime.utcnow().isoformat(),
        'usage_count': 0}

    # stores new element
    stored_urls[short_code] = new_url_item

    response = {'code': short_code}
    return Response(json.dumps(response), status=201, mimetype='application/json')


def get_url(short_name):
    """ Returns the long url associated to short code name."""
    if short_name in stored_urls.keys():
        # update usage count
        current_count = stored_urls[short_name]['usage_count']
        stored_urls[short_name]['usage_count'] = current_count+1

        # update last usage time
        stored_urls[short_name]['last_usage'] = datetime.datetime.utcnow().isoformat()
        return "Location: {0}".format(stored_urls[short_name]['url']), 302
    else:
        return "Bad Request.", 400


def get_stats(short_name):
    """ Returns additional information related to short code name."""
    if short_name in stored_urls.keys():
        response = stored_urls[short_name]
        return Response(json.dumps(response), status=200, mimetype='application/json')
    else:
        return "Bad Request.", 400
