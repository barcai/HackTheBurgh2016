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
    # If user is logged in, show useful information here, otherwise show login and register
    return render_template('index.html', l_form=LoginForm(), r_form=SignupForm())


@app.route('/login', methods=['POST'])
def login():
    l_form = LoginForm()
    if l_form.validate_on_submit():
        user = User.get_by_user_name(l_form.user_name.data)
        if (user is not None) and user.check_password(l_form.password.data):
            login_user(user)
            flash("Logged in successfully as {}.".format(user.user_name))
            return redirect(url_for('budget'))
    flash('Incorrect username or password')
    return render_template('index.html', l_form=l_form, r_form=SignupForm())


@app.route('/register', methods=['POST'])
def register():
    r_form = SignupForm()
    if r_form.validate_on_submit():
        user = User(email = r_form.email.data,
                    user_name = r_form.user_name.data,
                    password = r_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.user_name))
        return redirect(url_for('budget'))
    return render_template('index.html', l_form=LoginForm(), r_form=r_form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    
    return redirect(url_for('index'))

@app.route("/budget")
@login_required
def budget():
    return render_template("budget.html", xp_per_level = 50)


@app.route("/ajax", methods = ['GET', 'POST'])
@login_required
def ajax():
    if request.method == "POST":
        return jsonify(request.get_json(force=True))
    else:
        return jsonify({"todo":[{"checked":"false","id":"0","value":"This is an example todo"}]})
