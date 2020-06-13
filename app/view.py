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
from flask_security.registerable import register_user

from app.forms import *
from app import app
from app import db
from app import log

from app.models import *
from app.copydir import copydir
from app.security import user_datastore, security


@app.before_first_request
def create_initial_users():
    db.create_all()
    initial_users_list = [
        {'name': 'admin', 'description': 'administrator', 'email': 'admin@admin.com', 'password': 'admin'},
        {'name': 'guest', 'description': 'guest', 'email': 'guest@guest.com', 'password': 'guest'},
    ]
    def create_user(initial_users_list):
        for user in initial_users_list:
            if not user_datastore.get_user(user['email']):
                user_datastore.create_role(name=user['name'], description=user['description'])
                db.session.commit()
                role = Role.query.first()
                user_datastore.create_user(
                    email=user['email'], username=user['name'], password=hash_password(user['password']))
                user = User.query.first()
                user_datastore.add_role_to_user(user, role)
                db.session.commit()
    create_user(initial_users_list)

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
    
    user_dir = user.username + user.timestamp
    user_folders = os.path.join('app', 'static', 'user_data', user_dir)
    if not os.path.isdir(user_folders):
        log.info("User '%s' register." % (user.username)) 
        os.mkdir(user_folders)
        os.mkdir(os.path.join(user_folders, 'photos'))
        os.mkdir(os.path.join(user_folders, 'tracking_data'))
        copydir(os.path.join('app', 'static', 'user_data', 'avatar'), user_folders)
        log.debug("User after make folder: %s", user)

    remote_addr = request.remote_addr or 'untrackable'
    old_current_login, new_current_login = user.current_login_at, datetime.utcnow()
    old_current_ip, new_current_ip = user.current_login_ip, remote_addr
    user.last_login_at = old_current_login or new_current_login
    user.current_login_at = new_current_login
    user.last_login_ip = old_current_ip or new_current_ip
    user.current_login_ip = new_current_ip
    user.login_count = user.login_count + 1 if user.login_count else 1
    db.session.commit()
    log.info("User '%s' login with ip '%s'." % (user.username, user.current_login_ip)) 
    return render_template('index.html', user=user)

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    try:
        oauth = OAuthSignIn.get_provider(provider)
        return oauth.authorize()
    except:
        return redirect(url_for_security('login'))

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user_datastore.create_user(social_id=social_id, username=username, email=email)
        user = User.query.filter_by(social_id=social_id).first()
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))
