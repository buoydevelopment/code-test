# src/__init__.py

import os
import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

#from project.api.models import Product

#instantiate the app
app = Flask(__name__)

#set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

#instantiate the db
db = SQLAlchemy(app)

def create_app(script_info=None):
    #instiantiate the app
    app = Flask(__name__)

    #set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    #set up extensions
    db.init_app(app)

    #register blueprints
    from src.api.urls import urls_blueprint
    app.register_blueprint(urls_blueprint)
    # from project.api.products import products_blueprint
    # app.register_blueprint(products_blueprint)

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})

    return app