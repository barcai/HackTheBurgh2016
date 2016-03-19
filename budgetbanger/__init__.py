from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config_dict



db = SQLAlchemy()

# Authentication config
login_manager = LoginManager()




app = Flask(__name__)
app.config.from_object(config_dict["dev"])
config_dict["dev"].init_app(app)


db.init_app(app)
login_manager.init_app(app)

import budgetbanger.views