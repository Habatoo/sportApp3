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
    users = User.query.all()
    posts = Post.query.all()
    photos = Photo.query.all()
    events = Event.query.all()
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

