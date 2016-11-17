
#################
#### imports ####
#################

# import wraps from functools
from project import app, db
from project.models import BlogPost
from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from flask_login import login_required

################
#### config ####
################

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)


################
#### routes ####
################


# use decorators to link the function to a url
@home_blueprint.route('/')
@login_required
def home():
    posts = db.session.query(BlogPost).all()
    return render_template('index.html', posts=posts)  # render a template


@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template
