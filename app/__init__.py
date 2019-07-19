from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.auth import auth_api
from app.database import db
from config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    # Override config with instance folder config
    app.config.from_pyfile("config.py")

    # Blueprints registering
    app.register_blueprint(auth_api)

    # Init application database
    db.init_app(app)

    return app
