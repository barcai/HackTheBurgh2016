from flask import (render_template, url_for, request, redirect,
                  flash, current_app, session)
from flask_login import login_required, login_user, logout_user, current_user

from . import app, db, login_manager
from .forms import LoginForm, SignupForm
from .models import User

# call back to get the user object from
# the user_id stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/index')
def index():
    return "Hy"


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_user_name(form.user_name.data)
        if (user is not None) and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.user_name))
            return redirect(url_for('budget'))
        flash('Incorrect username or password')
    return render_template("login.html", form = form)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    user_name = form.user_name.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.user_name))
        return redirect(url_for('authorisation.login'))
    return render_template("signup.html", form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())


    return redirect(url_for('main.index'))