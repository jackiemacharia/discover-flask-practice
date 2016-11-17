#################
#### imports ####
#################

from flask import flash, redirect, render_template, request, \
    session, url_for, Blueprint
from functools import wraps
from form import LoginForm
from project.models import User, db, bcrypt

################
#### config ####
################

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)

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
                session['logged_in'] = True
                flash('You were just logged in!')
                return redirect(url_for('home.home'))
            else:
                error = 'Invalid credentials. Please try again.'
    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('home.welcome'))
