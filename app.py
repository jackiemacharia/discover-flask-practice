
#################
#### imports ####
#################

# import the Flask class from the flask module
# import wraps from functools
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps  # wraps allows you to define and use decorators such as login_required
import os

################
#### config ####
################


# create the application object
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])  # to add development environment to local environment use this command:  export APP_SETTINGS="config.DevelopmentConfig"
# create the sqlalchemy object
db = SQLAlchemy(app)
# come after the sqlalchemy object
from models import *
from project.users.views import users_blueprint

# register blueprints
app.register_blueprint(users_blueprint)

##########################
#### helper functions ####
##########################


# login_required decorator
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


# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    posts = db.session.query(BlogPost).all()
    return render_template('index.html', posts=posts)  # render a template


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

####################
#### run server ####
####################

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run()
