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
        'saved/index.html', user=current_user, posts=posts, photos=photos, events=events)

@saved.route('/unsaved', methods=['GET', 'POST'])
@login_required
def unsaved():
    # crew = Crew.query.filter(Crew.user_id==current_user.id).first()
    # crew.confirmed = 1
    # crew.refused = 0
    # db.session.commit()
    return redirect(url_for('saved.index'))

