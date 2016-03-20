from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

'''
give backrefs unique names
'''

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(120), unique = True)
    level_income = db.Column(db.Integer)
    level_expenditure = db.Column(db.Integer)
    current_xp_income = db.Column(db.Integer)
    current_xp_expenditure = db.Column(db.Integer)


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
    def verify_password(user_name, password):
        if User.get_by_user_name(user_name):
            u = User.get_by_user_name(user_name)
            return u.check_password(password)
        else:
            return False

    def __repr__(self):
        return '<User %r>' % self.user_name


class Money(db.Model):
    __tablename__ = 'Money'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    type = db.Column(db.Boolean)
    done = db.Column(db.Boolean)
    desc = db.Column(db.String(120))
    category = db.Column(db.String(120))
    amount = db.Column(db.Float)


class Periodic(db.Model):
    __tablename__ = 'Periodic'
    periodic_id = db.Column(db.Integer, db.ForeignKey('Money.id'), primary_key = True)
    periodid_length = db.Column(db.Integer)
    start_date = db.Column(db.String(80))
    end_date = db.Column(db.String(80))