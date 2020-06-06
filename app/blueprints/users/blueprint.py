from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_security import login_required, login_user, logout_user, current_user
from .forms import EditProfileForm

from app import app, log
from app import db
from app.models import *

users = Blueprint('users', __name__, template_folder='templates')

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('users/index.html', user=user)


