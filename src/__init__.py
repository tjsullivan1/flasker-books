# src/__init__.py
import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# instantiate db
db = SQLAlchemy()


# new
def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    app.logger.setLevel(LOG_LEVEL)
    app.logger.info(f"Starting Booker app -- log level: {LOG_LEVEL}")

    app.logger.debug(f"Starting Booker app -- name is {__name__}")

    # set up extensions
    db.init_app(app)

    # register api
    from src.api import api

    api.init_app(app)

    @app.route("/")
    def index():
        return "Hello World!"

    @app.route("/stocks/")
    def stocks():
        return "<h2>Stock List...</h2>"

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
