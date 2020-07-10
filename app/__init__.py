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
from flask_babelex import Babel

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

babel = Babel(app)

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

from .blueprints.posts.blueprint import posts
from .blueprints.users.blueprint import users
from .blueprints.events.blueprint import events
from .blueprints.photos.blueprint import photos

app.register_blueprint(posts, url_prefix='/post')
app.register_blueprint(users, url_prefix='/user')
app.register_blueprint(events, url_prefix='/event')
app.register_blueprint(photos, url_prefix='/photo')

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
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Photo, db.session))
admin.add_view(ModelView(Club, db.session))
admin.add_view(ModelView(Tier, db.session))
admin.add_view(ModelView(Level, db.session))
