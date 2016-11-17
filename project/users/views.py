#################
#### imports ####
#################

from flask import flash, redirect, render_template, request, url_for, Blueprint  # pragma: no cover
# from functools import wraps  # wraps allows you to define and use decorators such as login_required
from form import LoginForm, RegisterForm  # pragma: no cover
from project import db  # pragma: no cover
from project.models import User, bcrypt  # pragma: no cover
from flask_login import login_user, login_required, logout_user  # pragma: no cover

################
#### config ####
################

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)  # pragma: no cover
"""
##########################
#### helper functions ####
##########################


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap
"""

################
#### routes ####
################


# route for handling the login page logic
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['username']).first()
            password = form.password.data
            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):  # .encode('utf-8')
                # session['logged_in'] = True
                login_user(user)
                flash('You were just logged in!')
                return redirect(url_for('home.home'))
            else:
                error = 'Invalid credentials. Please try again.'
    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    #session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('home.welcome'))


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)  # To automatically log the user in after registration
        return redirect(url_for('home.home'))
    else:
        flash('Invalid credentials. Please try again.')
    return render_template('register.html', form=form)
