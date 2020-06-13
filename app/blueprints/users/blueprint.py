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

@users.route('/tag/<slug>')
@login_required
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug==slug).first()
    users = tag.users_tags.all()
    return render_template('users/tag_detail.html', tag=tag, users=users)

@users.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.city = form.city.data
        current_user.tags.append(Tag.query.filter_by(name=form.tags.data).first())
        db.session.commit()
        flash('Your changes have been saved.')
        log.info("User '%s' edit profile." % (current_user.username))
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('users/edit_profile.html', title='Edit Profile', form=form)
