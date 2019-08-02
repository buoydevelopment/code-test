# src/api/products.py

import random
import string
from flask import Blueprint, jsonify, request
from src.api.models import Url, already_existant_code, get_url_by_code, get_url_stats_by_code
from src import db
from sqlalchemy import exc

urls_blueprint = Blueprint('urls', __name__)

@urls_blueprint.route('/urls', methods=['POST'])
def add_url():
  """
    Endpoint to Add a New URL
  """
  post_data = request.get_json()

  if not post_data:
    return jsonify(response_object), 400

  url = post_data.get('url')
  code = post_data.get('code')

  if url is None or len(url) == 0:
    return {}, 400

  if code is None or len(code) == 0:
    code = generate_random_code()
  else:
    status = validate_code(code)
    if status != 201:
      return {}, status

  newUrl = Url()
  newUrl.url = url
  newUrl.code = code

  newUrl.save()

  return jsonify({ 'code': newUrl.code }), 201

@urls_blueprint.route('/<code>', methods=['GET'])
def get_by_code(code):
  """
    Endpoint to Retrieve an existant URL
  """
  url = get_url_by_code(code)

  if url == False:
    return {}, 404

  return {}, 302, { 'location': url.url }

@urls_blueprint.route('/<code>/stats', methods=['GET'])
def get_stats_by_code(code):
  """
    Endpoint to retrieve the Statistics of this particular CODE
  """
  url = get_url_stats_by_code(code)

  if url == False:
    return {}, 404

  return url.stats_to_json(), 200

def validate_code(code):
  if len(code) != 6:
    return 422
  elif any(char in string.punctuation for char in code):
    return 422
  else:
    if already_existant_code(code) == True:
      return 409
    else:
      return 201

def generate_random_code():
  letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
  return ''.join(random.choice(letters) for i in range(6))