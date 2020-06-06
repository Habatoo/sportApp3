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


log = logging.getLogger('btb_Api')
fh = logging.FileHandler(app.config['LOGGER_CONFIG']['file'])
fh.setLevel(app.config['LOGGER_CONFIG']['level'])
fh.setFormatter(app.config['LOGGER_CONFIG']['formatter'])
log.addHandler(fh)
log.setLevel(app.config['LOGGER_CONFIG']['level'])


from app.models import *
from app import view
# from app import errors
from wtforms.fields import HiddenField


### Flask-security ###
#user_datastore = SQLAlchemyUserDatastore(db, User, Role)
#security = Security(app, user_datastore)

def is_hidden_field_filter(field):
    return isinstance(field, HiddenField)


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
class AdminUserView(ModelView):
    can_create = False
    column_exclude_list = ('password')
    form_overrides = dict(password=HiddenField)

admin = Admin(app, 'sportApp', url='/', index_view=HomeAdminView(name='Home'))

# admin.add_view(ModelView(Post, db.session))
admin.add_view(AdminView(User, db.session))
#admin.add_view(AdminUserView(User))
admin.add_view(ModelView(Role, db.session))
#path = op.join(op.dirname(__file__), 'static')
#admin.add_view(FileAdmin(path, '/static/', name='Files'))
#admin.add_link(MenuLink(name='Logout', endpoint='security.logout'))

