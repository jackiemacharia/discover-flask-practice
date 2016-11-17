
#################
#### imports ####
#################

# import the Flask class from the flask module
# import wraps from functools
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

################
#### config ####
################


# create the application object
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])  # to add development environment to local environment use this command:  export APP_SETTINGS="config.DevelopmentConfig"
# create the sqlalchemy object
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.home.views import home_blueprint

# register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(home_blueprint)
