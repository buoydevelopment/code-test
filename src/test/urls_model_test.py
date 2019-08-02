# src/test/urls_model_test.py

import json
import unittest
import datetime

from flask import current_app
from flask_testing import TestCase

from src import db, create_app
from src.api.models import Url, get_url_by_code, get_url_stats_by_code, already_existant_code
from src.test.base import BaseTestCase

app = create_app()

def new_url(code, url):
    newUrl = Url()
    newUrl.code = code
    newUrl.url = url

    newUrl.save()
    return Url.query.filter_by(code=code).first()

class TestUrlModel(TestCase):
    def create_app(self):
        app.config.from_object('src.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_url_correctly(self):
        url = Url()
        url.code = 'aBC123'
        url.url = 'http://www.google.com'

        url.save()

        added_url = Url.query.filter_by(code='aBC123').first()
        self.assertIsNotNone(added_url)
        self.assertIsNotNone(added_url.created_at)
        self.assertIsNone(added_url.last_usage)
        self.assertTrue(added_url.usage_count == 0)

    def test_to_json_method_ok(self):
        url = Url()
        url.code = 'aBC124'
        url.url = 'http://www.google.com/'

        expected_json = {
            'url': 'http://www.google.com/',
            'code': 'aBC124'
        }

        self.assertTrue(url.to_json() == expected_json)

    def test_to_json_method_not_ok(self):
        url = Url()
        url.code = 'aBC125'
        url.url = 'http://www.google.com/'

        expected_json = {
            'url': 'http://www.google.com/'
        }

        self.assertTrue(url.to_json() != expected_json)

    def test_stats_to_json_method_ok(self):
        created_now = datetime.datetime.utcnow()
        updated_now = datetime.datetime.utcnow()

        url = Url()
        url.code = 'aBC126'
        url.url = 'http://www.google.com/'
        url.created_at = created_now
        url.last_usage = updated_now
        url.usage_count = 3
        url.save()
        
        added_url = Url.query.filter_by(code='aBC126').first()

        expected_json = {
            'created_at': created_now.isoformat(),
            'last_usage': updated_now.isoformat(),
            'usage_count': 3
        }

        self.assertTrue(added_url.stats_to_json() == expected_json)

    def test_stats_to_json_method_with_default_values_ok(self):
        created_now = datetime.datetime.utcnow()

        url = Url()
        url.code = 'aBC127'
        url.url = 'http://www.google.com/'
        url.created_at = created_now
        url.save()
        
        added_url = Url.query.filter_by(code='aBC127').first()

        expected_json = {
            'created_at': created_now.isoformat(),
            'usage_count': 0
        }

        self.assertTrue(added_url.stats_to_json() == expected_json)

    def test_stats_to_json_method_not_ok(self):
        created_now = datetime.datetime.utcnow()
        updated_now = datetime.datetime.utcnow()

        url = Url()
        url.code = 'aBC126'
        url.url = 'http://www.google.com/'
        url.created_at = created_now
        url.last_usage = updated_now
        url.usage_count = 3
        url.save()
        
        added_url = Url.query.filter_by(code='aBC126').first()

        expected_json = {
            'created_at': created_now.isoformat(),
            'last_usage': updated_now.isoformat(),
            'usage_count': 4
        }

        self.assertTrue(added_url.stats_to_json() != expected_json)

class TestHelperMethods(TestCase):
    def create_app(self):
        app.config.from_object('src.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_url_by_code_ok(self):
        url = new_url('a123bc', 'http://www.google.com')
        expected_url = get_url_by_code('a123bc')

        self.assertTrue(url == expected_url)
    
    def test_get_url_by_code_not_ok(self):
        url = new_url('a123bc', 'http://www.google.com')
        expected_url = get_url_by_code('bc123a')

        self.assertFalse(expected_url)
        self.assertTrue(url != expected_url)
    
    def test_get_url_stats_by_code_ok(self):
        url = new_url('bc123a', 'http://www.google.com')
        expected_url = get_url_by_code('bc123a')

        self.assertTrue(url == expected_url)

    def test_get_url_stats_by_code_not_ok(self):
        url = new_url('bc123a', 'http://www.google.com')
        expected_url = get_url_by_code('123456')

        self.assertFalse(expected_url)
        self.assertTrue(url != expected_url)

    def test_already_existant_code_ok(self):
        url = new_url('bc123a', 'http://www.google.com')
        
        self.assertFalse(already_existant_code('a1234c'))
        self.assertTrue(already_existant_code('bc123a'))