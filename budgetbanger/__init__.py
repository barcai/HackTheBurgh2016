from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config_dict



db = SQLAlchemy()

# Authentication config
login_manager = LoginManager()


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    config_dict[config_name].init_app(app)

    db.init_app(app)
    #toolbar.init_app(app)
    login_manager.init_app(app)

    return app