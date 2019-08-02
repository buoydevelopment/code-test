# src/test/urls_api_test.py

import json
import unittest
import datetime

from flask import current_app
from flask_testing import TestCase

from src import db, create_app
# from src.api.urls import 
from src.api.models import Url
from src.test.base import BaseTestCase

app = create_app()

def add_url(code, url):
    newUrl = Url()
    newUrl.code = code
    newUrl.url = url

    newUrl.save()
    return Url.query.filter_by(code=code).first()

class TestUrlEndpoint(TestCase):
  def create_app(self):
    app.config.from_object('src.config.TestingConfig')
    return app

  def setUp(self):
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_post_should_be_ok(self):
    payload = {
      'url': 'http://example.com',
      'code': 'Ncr8p7'
    }

    expected_body = {
      'code': 'Ncr8p7'
    }
    expected_status = 201

    response = app.test_client().post(
      '/urls', 
      data=json.dumps(payload), 
      content_type='application/json'
    )
    response_body = json.loads(response.get_data())

    self.assertTrue(response.status_code == expected_status)
    self.assertTrue(response_body == expected_body)

  def test_post_should_throw_conflic(self):
    add_url('Ncr8p7', 'http://example.com')

    payload = {
      'url': 'http://example.com',
      'code': 'Ncr8p7'
    }

    expected_body = {}
    expected_status = 409

    response = app.test_client().post(
      '/urls', 
      data=json.dumps(payload), 
      content_type='application/json'
    )
    response_body = json.loads(response.get_data())

    self.assertTrue(response.status_code == expected_status)
    self.assertTrue(response_body == expected_body)
  
  def test_post_should_throw_unprocessable_entity_due_to_invalid_characters(self):
    payload = {
      'url': 'http://example.com',
      'code': '######'
    }

    expected_body = {}
    expected_status = 422

    response = app.test_client().post(
      '/urls', 
      data=json.dumps(payload), 
      content_type='application/json'
    )
    response_body = json.loads(response.get_data())

    self.assertTrue(response.status_code == expected_status)
    self.assertTrue(response_body == expected_body)

  def test_post_should_throw_unprocessable_entity_due_to_invalid_maxlength(self):
    payload = {
      'url': 'http://example.com',
      'code': 'asd21134'
    }

    expected_body = {}
    expected_status = 422

    response = app.test_client().post(
      '/urls', 
      data=json.dumps(payload), 
      content_type='application/json'
    )
    response_body = json.loads(response.get_data())

    self.assertTrue(response.status_code == expected_status)
    self.assertTrue(response_body == expected_body)

  def test_post_should_throw_unprocessable_entity_due_to_invalid_minlength(self):
    payload = {
      'url': 'http://example.com',
      'code': 'a1'
    }

    expected_body = {}
    expected_status = 422

    response = app.test_client().post(
      '/urls', 
      data=json.dumps(payload), 
      content_type='application/json'
    )
    response_body = json.loads(response.get_data())

    self.assertTrue(response.status_code == expected_status)
    self.assertTrue(response_body == expected_body) 

  def test_get_should_be_ok(self):
    expected_status = 302
    expected_location = 'http://www.google.com'
    add_url('ab1234', 'http://www.google.com')

    response = app.test_client().get(
      '/ab1234',
      content_type='application/json'
    )

    response_header_location = response.headers.get('location')

    self.assertTrue(response.status_code == expected_status)
    self.assertTrue(response_header_location == expected_location)

  def test_get_with_inexistant_code_should_be_not_found(self):
    expected_status = 404
    response = app.test_client().get(
      '/ab1234',
      content_type='application/json'
    )

    self.assertTrue(response.status_code == expected_status)

  def test_get_stats_with_existant_code_and_0_calls_should_be_ok(self):
    created_now = datetime.datetime.utcnow()

    url = Url()
    url.code = 'ab1234'
    url.url = 'http://www.google.com'
    url.created_at = created_now

    url.save()

    expected_status = 200
    expected_body = {
      'created_at': created_now.isoformat(),
      'usage_count': 0      
    }

    response = app.test_client().get(
      '/ab1234/stats',
      content_type='application/json'
    )

    response_body = json.loads(response.get_data())

    self.assertTrue(response.status_code == expected_status)
    self.assertTrue(response_body == expected_body)

  def test_get_stats_with_inexistant_code_should_be_not_found(self):
    expected_status = 404
    response = app.test_client().get(
      '/ab1234/stats',
      content_type='application/json'
    )

    self.assertTrue(response.status_code == expected_status)

  def test_get_stats_after_consume_should_be_ok(self):
    created_now = datetime.datetime.utcnow()

    url = Url()
    url.code = 'ab1234'
    url.url = 'http://www.google.com'
    url.created_at = created_now

    url.save()

    response_pre = app.test_client().get('/ab1234', content_type='application/json')
    self.assertTrue(response_pre.status_code == 302)

    expected_status = 200

    response = app.test_client().get(
      '/ab1234/stats',
      content_type='application/json'
    )

    response_body = json.loads(response.get_data())

    self.assertTrue(response.status_code == expected_status)
    self.assertTrue(response_body['created_at'] == created_now.isoformat())
    self.assertTrue(response_body['usage_count'] == 1)
    self.assertIsNotNone(response_body['last_usage'])
    