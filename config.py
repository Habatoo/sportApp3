import os
import urllib
import psycopg2
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
    MAIL_SERVER = 'smtp.yandex.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SECURITY_REGISTERABLE = True # create a user registration endpoint
    SECURITY_RECOVERABLE = True # create a password reset/recover endpoint
    # SECURITY_CONFIRMABLE = True # specifies if users are required to confirm their email address when registering a new account. 
     
    ############# Login config ################################
    OAUTH_CREDENTIALS = os.environ.get('OAUTH_CREDENTIALS')


class DevConfig(Configuration):
    DEBUG = True
    DEVELOPMENT = True


config = {
    'dev': DevConfig,
    #'prod': ProdConfig,
    'default': Configuration,
}

 