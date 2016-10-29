# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'Hb\x8b\xbbn\xf2\x9d\xe1Q\xc2\xe1,h;\x8c\xbb\xdb\xed\xe6\xc4\xd1W \x86'  # use a random key generator command: import os. os.urandom(n)  # not advisable on a public repo
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']  # sets up environment variable for db command: export DATABASE_URL="sqlite:///posts.db"
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# for major projects, do not add your config file to a public repo  # Also if you push a config file with different settings for each environment without using the class structure,it overides previous settings each time establishing different environment settings

# config specific to local environment


class DevelopmentConfig(BaseConfig):
    DEBUG = True  # overides parent class debug mode  # you want debug true for development

# config for live environment


class ProductionConfig(BaseConfig):
    DEBUG = False  # makes sure that production environment is not debug mode to avoid exposing our server to public
