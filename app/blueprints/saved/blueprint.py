from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_security import login_required, login_user, logout_user, current_user, roles_accepted

from .forms import SavedForm

from app import app
from app import db
from app import log
from app.models import *

saved = Blueprint('saved', __name__, template_folder='templates')

@saved.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user = User.query.filter(User.username==current_user.username).first()
    posts = []
    for post_ in user.save_post:
        post = Post.query.filter(Post.id==post_.id).first()
        posts.append(post)

    photos = []
    for photo_ in user.save_photo:
        photo = Photo.query.filter(Photo.id==photo_.id).first()
        photos.append(photo)

    events = []
    for event_ in user.save_event:
        event = Event.query.filter(Event.id==event_.id).first()
        events.append(event)
    return render_template(
        'saved/index.html', user=user, posts=posts, photos=photos, events=events, current_user=current_user)

@saved.route('/unsaved/<content>/<item>', methods=['GET', 'POST'])
@login_required
def unsaved(content, item):
    user = User.query.filter(User.username == current_user.username).first()
    if content == 'Post':
        post = Post.query.filter(Post.slug == item).first()
        print(post, item, content)
        user.save_post.remove(post)
    if content == 'Photo':
        photo = Photo.query.filter(Photo.id == item).first()
        user.save_photo.remove(photo)
    if content == 'Event':
        event = Event.query.filter(Event.slug == item).first()
        user.save_event.remove(event)
    db.session.commit()
    return redirect(url_for('saved.index'))

