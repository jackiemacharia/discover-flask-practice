import os

# default config


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'Hb\x8b\xbbn\xf2\x9d\xe1Q\xc2\xe1,h;\x8c\xbb\xdb\xed\xe6\xc4\xd1W \x86'  # use a random key generator command: import os. os.urandom(n)  # not advisable on a public repo
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']  # sets up a local environment variable for db command: export DATABASE_URL="sqlite:///posts.db" with postgres: export DATABASE_URL="postgresql:///discover_flask_final" where discover_flask_final is the db name
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # print SQLALCHEMY_DATABASE_URI


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# for major projects, do not add your config file to a public repo  # Also if you push a config file with different settings for each environment without using the class structure,it overides previous settings each time establishing different environment settings
# access db: sudo -u postgres psql postgres
# config specific to local environment


class DevelopmentConfig(BaseConfig):
    DEBUG = True  # overides parent class debug mode  # you want debug true for development

# config for live environment


class ProductionConfig(BaseConfig):
    DEBUG = False  # makes sure that production environment is not debug mode to avoid exposing our server to public
#  heroku config:set APP_SETTINGS=config.ProductionConfig --remote heroku sets heroku as production remote


# The export commands have to be ran with every new instance of the terminal

# export DATABASE_URL="postgresql:///discover_flask_final"

# export APP_SETTINGS="config.DevelopmentConfig"

# autoenv sets directory specific environment variables - check it out - alternative to using export all the time

# add environment variables on postactivate script - triggered after activating env with WORKON

# cd $VIRTUAL_ENV/bin - takes you to where the postactivate script is found when virtual env is activated

# to edit postactivate in vim: ~/Documents/code_cave/playground/discover-flask/discover-flask-practice$ vi $VIRTUAL_ENV/bin/postactivate

# then add environment variables: export DATABASE_URL="postgresql:///discover_flask_final" & export APP_SETTINGS="config.DevelopmentConfig"

# solves having to keep exporting environment variables every time the terminal powers up esc then :wq saves and exits vim
