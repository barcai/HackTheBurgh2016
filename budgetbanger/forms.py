from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, \
    Regexp, EqualTo, ValidationError
# difference bet
from .models import User

class LoginForm(Form):
    user_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class SignupForm(Form):
    user_name = StringField('Username',
                            validators = [
                                DataRequired(),
                                Length(6, 80),
                                Regexp('^[A-Za-z0-9_]{3,}$',
                                    message = 'Usernames consists of numbers, letters, and underscores.')])
    password = PasswordField('Password',
                            validators = [
                                DataRequired(),
                                EqualTo('password2', message = 'Passwords must match.')])
    password2 = PasswordField('Confirm password', validators = [DataRequired()])
    email = StringField('Email',
                        validators = [DataRequired(),
                                        Length(1, 120),
                                        Email()])

    def validate_email(self, email_field):
        if User.query.filter_by(email = email_field.data).first():
            raise ValidationError('There already exists a users with this email address.')

    def validate_user_name(self, user_name_field):
        if User.query.filter_by(user_name = user_name_field.data).first():
            raise ValidationError('There already exists a users with this username')