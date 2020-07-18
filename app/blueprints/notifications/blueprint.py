from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_security import login_required, login_user, logout_user, current_user, roles_accepted

from .forms import NotificationForm

from app import app
from app import db
from app import log
from app.models import *

notifications = Blueprint('notifications', __name__, template_folder='templates')

@notifications.route('/', methods=['GET', 'POST'])
@login_required
def index():
    users = User.query.all()
    notifications = Crew.query.all()
    events = Event.query.all()
    # Device.query.filter(DeviceGroup.type != ModelType.TYPE_BLADE_SERVER).all()
    return render_template(
        'notifications/index.html', users=users, notifications=notifications, user=current_user, events=events)

@notifications.route('/accept', methods=['GET', 'POST'])
@login_required
def accept():
    crew = Crew.query.filter(Crew.user_id==current_user.id).first()
    crew.confirmed = 1
    crew.refused = 0
    db.session.commit()
    return redirect(url_for('notifications.index'))

@notifications.route('/refuse', methods=['GET', 'POST'])
@login_required
def refuse():
    crew = Crew.query.filter(Crew.user_id==current_user.id).first()
    crew.confirmed = 0
    crew.refused = 1
    db.session.commit()
    return redirect(url_for('notifications.index'))
