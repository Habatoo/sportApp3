from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
from flask_moment import Moment

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from time import time
import os.path as op

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user

from flask import request, redirect, url_for

from config import config
from wtforms.fields import HiddenField


app = Flask(__name__)
app.config.from_object(config.get('dev'))

db  = SQLAlchemy(app)
mail = Mail(app)
moment = Moment(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

login = LoginManager(app)
login.login_view = 'login'

######## logger ###################
log = logging.getLogger('btb_Api')
fh = logging.FileHandler(app.config['LOGGER_CONFIG']['file'])
fh.setLevel(app.config['LOGGER_CONFIG']['level'])
fh.setFormatter(app.config['LOGGER_CONFIG']['formatter'])
log.addHandler(fh)
log.setLevel(app.config['LOGGER_CONFIG']['level'])
###################################


from app import view
from app.security import *
from app import errors


from .blueprints.users.blueprint import users

app.register_blueprint(users, url_prefix='/user')

# #### ADMIN ####
class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))

class AdminView(AdminMixin, ModelView):
    pass

class HomeAdminView(AdminMixin, AdminIndexView):
    pass

# Setup Flask-admin
def is_hidden_field_filter(field):
    return isinstance(field, HiddenField)

class AdminUserView(ModelView):
    can_create = False
    column_exclude_list = ('password')
    form_overrides = dict(password=HiddenField)

admin = Admin(app, 'sportApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(AdminView(User, db.session))
admin.add_view(ModelView(Role, db.session))

def init_email_error_handler(app):
    # Initialize a logger to send emails on error-level messages.
    # Unhandled exceptions will now send an email message to app.config.ADMINS.
    if app.debug:
        return  # Do not send error emails while developing

    # Retrieve email settings from app.config
    host = app.config['MAIL_SERVER']
    port = app.config['MAIL_PORT']
    from_addr = app.config['MAIL_DEFAULT_SENDER']
    username = app.config['MAIL_USERNAME']
    password = app.config['MAIL_PASSWORD']
    secure = () if app.config.get('MAIL_USE_TLS') else None

    # Retrieve app settings from app.config
    to_addr_list = app.config['ADMINS']
    subject = app.config.get('APP_SYSTEM_ERROR_SUBJECT_LINE', 'System Error')

    # Setup an SMTP mail handler for error-level messages
    import logging
    from logging.handlers import SMTPHandler

    mail_handler = SMTPHandler(
        mailhost=(host, port),  # Mail host and port
        fromaddr=from_addr,  # From address
        toaddrs=to_addr_list,  # To address
        subject=subject,  # Subject line
        credentials=(username, password),  # Credentials
        secure=secure,
    )
    
    # Log errors using: app.logger.error('Some error message')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
