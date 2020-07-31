import os
import urllib
# import psycopg2
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration(object): 
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
       'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 3

    LOGGER_CONFIG = dict(level=logging.DEBUG,
                     file="app.log",
                     formatter=logging.Formatter("%(asctime)s [%(levelname)s] - %(name)s:%(message)s")
                     )

    OAUTH_CREDENTIALS = os.environ.get('OAUTH_CREDENTIALS')

    CITIES = [
    {'label': 'Novosibirsk', 'value': 'Novosibirsk'},
    {'label': 'Moscow', 'value': 'Moscow'},
    ]
    ########## File upload config #############################
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    ############ Flask security ###############################
    SECURITY_PASSWORD_SALT = 'SALT'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465 # int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = True
    MAIL_USE_SSL = True

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')   
    MAIL_DEFAULT_SENDER = '"Your Name" <yourname@gmail.com>'
    ADMINS = ['"Admin One" <admin1@gmail.com>',]

    SECURITY_REGISTERABLE = True # create a user registration endpoint
    SECURITY_RECOVERABLE = True # create a password reset/recover endpoint
    SECURITY_CHANGEABLE = True # enable the change password endpoint
    SECURITY_SEND_REGISTER_EMAIL = False # Specifies whether registration email is sent.
    SECURITY_TRACKABLE = True # should track basic user login statistics
    # SECURITY_CONFIRMABLE = True # specifies if users are required to confirm their email address when registering a new account. 
     
    ############# Login config ################################
    OAUTH_CREDENTIALS = os.environ.get('OAUTH_CREDENTIALS') or {
        'facebook': 
        {'id': '0000', 'secret': 'qqqq'},
        'vc': 
        {'id': '0000', 'secret': 'qqqq'},
        'google': 
        {'id': '0000', 'secret': 'qqqq'},
        }

    SOCIAL_FACEBOOK = {
        'consumer_key': 'facebook app id',
        'consumer_secret': 'facebook app secret'
    }
    SOCIAL_GOOGLE = {
        'consumer_key': 'xxxx',
        'consumer_secret': 'xxxx'
    }
    SOCIAL_VK = {
        'consumer_key': 'xxxx',
        'consumer_secret': 'xxxx'
    }

class DevConfig(Configuration):
    DEBUG = True
    DEVELOPMENT = True

class ProdConfig(Configuration):
    DEBUG = False
    DEVELOPMENT = False

config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': Configuration,
}
 