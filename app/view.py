from datetime import datetime
from werkzeug.urls import url_parse
import os
import logging
#from oauth import OAuthSignIn

from flask import render_template, flash, redirect, url_for, request
from flask import Blueprint
from flask_security import login_required, login_user, logout_user, current_user

# from flask_login import login_user
# from flask_login import logout_user
# from flask_login import current_user

from app.forms import LoginForm
from app.forms import RegistrationForm
from app import app
from app import db
from app import log

from app.models import *
from app.copydir import copydir
#from app import user_datastore
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security

### Flask-security ###
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
users = Blueprint('users', __name__, template_folder='templates')

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@users.before_app_first_request
def init_my_blueprint():
    if not app.user_datastore.get_user('admin@admin.com'):
        app.user_datastore.create_role(name='admin', description='administrator')
        db.session.commit()
        role = Role.query.first()
        app.user_datastore.create_user(email='admin@admin.com', password='admin')
        user = User.query.first()
        user_datastore.add_role_to_user(user, role)
        db.session.commit()

@users.before_app_request
def before_request():
    if request.path.startswith('/admin'):
        if current_user.is_authenticated:
            if not current_user.has_role("admin"):
                return redirect(url_for('security.logout'))
        else:
            return redirect(url_for('security.login'))


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    return render_template('index.html', user=user)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Incorrect email or password.')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)

#         log.info("User '%s' login." % (user.username))
#         return redirect(next_page)
#     return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    user = current_user.username
    logout_user()
    log.info("User '%s' logout." % (user))
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=form.password.data,
            # form.password_confirm
            city=form.city.data
            )
        # user.set_password(form.password.data)
        log.debug("user before: %s", user)
        try:
            db.session.add(user)
            db.session.commit()
            log.debug("user after: %s", user)
            new_user = User.query.filter(User.username == form.username.data).first()         
            user_dir = new_user.username + new_user.timestamp
            user_folders = os.path.join('app', 'static', 'user_data', user_dir)
            if not os.path.isdir(user_folders):
                os.mkdir(user_folders)
                os.mkdir(os.path.join(user_folders, 'photos'))
                os.mkdir(os.path.join(user_folders, 'tracking_data'))
            copydir(os.path.join('app', 'static', 'user_data', 'avatar'), user_folders)
            flash('Congratulations, you are now a registered user!')
            log.debug("user after make folder: %s", user)
            log.info("User '%s' register." % (user.username))
            return redirect(url_for('login'))
        except:
            flash('Something wrong')
            log.info("User '%s' can not register." % (user.username))
            return redirect(url_for('register'))
    return render_template('register_user.html', title='Register', form=form)
