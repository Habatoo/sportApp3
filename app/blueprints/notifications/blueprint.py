from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_security import login_required, login_user, logout_user, current_user, roles_accepted

from .forms import NotificationForm
from datetime import datetime

from app import app
from app import db
from app import log
from app.models import *

notifications = Blueprint('notifications', __name__, template_folder='templates')

@notifications.route('/', methods=['GET', 'POST'])
@login_required
def index():
    users = User.query.all()
    # notifications = Crew.query.all()
    notifications = Crew.query.filter(Crew.user_id == current_user.id)
    events = Event.query.all()

    # for notification in notifications:
    #     if notification.user_id == current_user.id and not notification.confirmed and not notification.refused:
    #         for event in events:
    #             if event.id == notification.event_id and notification.refused != 1:
    #                 pass
    return render_template(
        'notifications/index.html',
        users=users,
        notifications=notifications,
        user=current_user,
        events=events,
        times=datetime.now(),
    )

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
