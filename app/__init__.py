from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from app.auth import auth_api
from app.database import db
from config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    # Blueprints registering
    app.register_blueprint(auth_api)

    # Init application database
    db.init_app(app)

    # Enable CORS for our application
    CORS(app)

    return app
