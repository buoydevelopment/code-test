# src/config.py

import os

class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'my_precious'
    IS_MEMORY_DB = False

class LocalConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    # IS_MEMORY_DB = True
    IS_MEMORY_DB = False

class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    IS_MEMORY_DB = True
