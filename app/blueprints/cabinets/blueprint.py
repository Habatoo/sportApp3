from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_security import login_required, login_user, logout_user, current_user, roles_accepted

from .forms import CabinetForm

from app import app
from app import db
from app import log
from app.models import *

cabinets = Blueprint('cabinets', __name__, template_folder='templates')

@cabinets.route('/<username>', methods=['GET', 'POST'])
@login_required
def index(username):
    user = User.query.filter_by(username=username).first_or_404()
    cabinet = Cabinet.query.filter(Cabinet.user_id == user.id).first()
    events = Event.query.all()

    if user.mentor:
        return render_template(
        'cabinets/user_cabinet.html', cabinet=cabinet, user=current_user, events=events)

    form = CabinetForm()
    if form.validate_on_submit():
        cabinet = Cabinet(
            user_firstname=form.user_firstname.data,
            user_lastname=form.user_lastname.data,
            user_age=form.user_age.data,
            user_phone=form.user_phone.data,
            user_address=form.user_address.data,
            title=form.user_address.data,
            description=form.user_address.data,
            user=current_user,
            )
        try:
            #sponsor_tier = db.relationship('Tier', backref='tier', lazy='dynamic')
            cabinet.sponsor_tier.append(Tier.query.filter_by(title=form.sponsor_tier.data).first())
            #db.session.add(post)
            #db.session.commit()
            flash('Your cabinet is now live!')
            return redirect(url_for('cabinets.index'))
        except:
            redirect('index')

    return render_template(
        'cabinets/index.html', cabinet=cabinet, user=current_user, events=events, form=form)

# @notifications.route('/accept', methods=['GET', 'POST'])
# @login_required
# def accept():
#     crew = Crew.query.filter(Crew.user_id==current_user.id).first()
#     crew.confirmed = 1
#     crew.refused = 0
#     db.session.commit()
#     return redirect(url_for('notifications.index'))
#
# @notifications.route('/refuse', methods=['GET', 'POST'])
# @login_required
# def refuse():
#     crew = Crew.query.filter(Crew.user_id==current_user.id).first()
#     crew.confirmed = 0
#     crew.refused = 1
#     db.session.commit()
#     return redirect(url_for('notifications.index'))
