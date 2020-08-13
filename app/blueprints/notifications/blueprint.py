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
    notifications = Crew.query.filter(Crew.user_id == current_user.id)

    event_list = []
    soon_event_list = []
    for notification in notifications:
        event = Event.query.filter(Event.id == notification.event_id).first()
        if not notification.confirmed:
            event_list.append(event)
        if notification.confirmed:
            # if (event.event_time - datetime.now()).days < 1 and (event.event_time - datetime.now()).days > 0:
            soon_event_list.append(event)

    return render_template(
        'notifications/index.html',
        event_list=event_list,
        soon_event_list=soon_event_list,
    )

@notifications.route('/accept', methods=['GET', 'POST'])
@login_required
def accept():
    crew = Crew.query.filter(Crew.user_id==current_user.id).first()
    crew.confirmed = 1
    crew.refused = 0
    print(crew.id)
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

# <!--    <br> {% for notification in notifications %}-->
# <!--    {% if notification.user_id==current_user.id and not notification.confirmed and not notification.refused %}-->
# <!--    <br> {% for event in events %}-->
# <!--    {{ event.event_time - time }}-->
# <!--    {% if event.id==notification.event_id and notification.confirmed == 1 and notification.refused !=1 %}-->
#
# <!--    {% if (event.event_time - time).day < 1 and (event.event_time - time).day > 0 %}-->
# <!--    Event title: <a href="{{ url_for('events.event_detail', slug=event.slug) }}">{{ event.event_title }} </a>-->
# <!--    <br> Event body: {{ event.event_body}}-->
# <!--    {% endif %}-->
# <!--    {% endif %}-->
# <!--    {% endfor %} {% endif %}-->
# <!--    <hr>-->
# <!--    {% endfor %}-->
