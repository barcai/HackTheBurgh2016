from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

'''
give backrefs unique names
'''

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(120), unique = True)
    is_admin = db.Column(db.Boolean, default=False)

    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('password is a write only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_user_name(user_name):
        return User.query.filter_by(user_name = user_name).first()

    @staticmethod
    @httpauth.verify_password
    def verify_password(user_name, password):
        if User.get_by_user_name(user_name):
            u = User.get_by_user_name(user_name)
            return u.check_password(password)
        else:
            return False

    def __repr__(self):
        return '<User %r>' % self.user_name


class Money(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(120), unique = True)
        