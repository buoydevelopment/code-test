# src/test/config_test.py

import os
import unittest

from flask import current_app
from flask_testing import TestCase
from src import create_app

app = create_app()

class TestLocalConfig(TestCase):
    def create_app(self):
        app.config.from_object('src.config.LocalConfig')
        return app

    def test_app_is_local(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///test.db')

class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('src.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(app.config['IS_MEMORY_DB'])

if __name__ == '__main__':
    unittest.main()
