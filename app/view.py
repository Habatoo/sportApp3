from datetime import datetime
from werkzeug.urls import url_parse
import os
import logging
from oauth import OAuthSignIn

from flask import render_template, flash, redirect, url_for, request
from flask import Blueprint

from flask_security import login_required, login_user, logout_user, current_user, url_for_security
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security.utils import hash_password

from app.forms import *
from app import app
from app import db
from app import log

from app.models import *
from app.copydir import copydir
from app.security import *


@app.before_first_request
def create_admin():
    db.create_all()
    if not user_datastore.get_user('admin@admin.com'):
        user_datastore.create_role(name='admin', description='administrator')
        db.session.commit()
        role = Role.query.first()
        user_datastore.create_user(
            email='admin@admin.com', username='administrator', password=hash_password('admin'))
        user = User.query.first()
        user_datastore.add_role_to_user(user, role)
        db.session.commit()

@app.before_request
def before_request():
    if request.path.startswith('/admin'):
        if current_user.is_authenticated:
            if not current_user.has_role("admin"):
                return redirect(url_for('security.logout'))
        else:
            return redirect(url_for('security.login'))

    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    log.info("User '%s' login." % (user.username))
    return render_template('index.html', user=user)

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for_security('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for_security('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for_security('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, username=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index')) 
       
# @app.route('/logout')
# def logout():
#     user = current_user.username
#     logout_user()
#     log.info("User '%s' logout." % (user))
#     return redirect(url_for_security('index'))

# def register_user(**kwargs):
#     confirmation_link, token = None, None
#     kwargs['password'] = hash_password(kwargs['password'])
#     user = _datastore.create_user(**kwargs)
#     _datastore.commit()

#     if _security.confirmable:
#         confirmation_link, token = generate_confirmation_link(user)
#         do_flash(*get_message('CONFIRM_REGISTRATION', email=user.email))

#     user_registered.send(app._get_current_object(),
#                          user=user, confirm_token=token)

#     if config_value('SEND_REGISTER_EMAIL'):
#         send_mail(config_value('EMAIL_SUBJECT_REGISTER'), user.email,
#                   'welcome', user=user, confirmation_link=confirmation_link)

#     return user

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
    # form = ExtendedRegisterForm()

    # # if request.method == 'POST':
    # #     user_datastore.create_user(
    # #         email=request.form.get('email'),
    # #         password=hash_password(request.form.get('password'))
    # #     )
    # #     db.session.commit()
    # #     return redirect(url_for('profile'))
    # # return render_template('register.html')

    # if form.validate_on_submit():
    #     user = User(
    #         username=form.username.data, 
    #         email=form.email.data, 
    #         password=hash_password(form.password.data),
    #         city=form.city.data
    #         )
    #     log.debug("user before: %s", user)
    #     try:
    #         db.session.add(user)
    #         db.session.commit()
    #         log.debug("user after: %s", user)
    #         new_user = User.query.filter(User.username == form.username.data).first()         
    #         user_dir = new_user.username + new_user.timestamp
    #         user_folders = os.path.join('app', 'static', 'user_data', user_dir)
    #         if not os.path.isdir(user_folders):
    #             os.mkdir(user_folders)
    #             os.mkdir(os.path.join(user_folders, 'photos'))
    #             os.mkdir(os.path.join(user_folders, 'tracking_data'))
    #         copydir(os.path.join('app', 'static', 'user_data', 'avatar'), user_folders)
    #         flash('Congratulations, you are now a registered user!')
    #         log.debug("user after make folder: %s", user)
    #         log.info("User '%s' register." % (user.username))
    #         return redirect(url_for('login'))
    #     except:
    #         flash('Something wrong')
    #         log.info("User '%s' can not register." % (user.username))
    #         return redirect(url_for('register'))
    # return render_template('security/register_user.html', title='Register', form=form)
    # # return redirect(url_for('security.login', next=request.url))


