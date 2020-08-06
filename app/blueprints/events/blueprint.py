from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_security import login_required, login_user, logout_user, current_user, roles_accepted
from wtforms_components import read_only

from .forms import EventForm

from app import app
from app import db
from app import log
from app.models import *

try:
    from geopy.geocoders import Nominatim
except:
    redirect('events.index')

events = Blueprint('events', __name__, template_folder='templates')

@events.route('/event_new', methods=['GET', 'POST'])
@login_required
def event_new():
    users = User.query.all()
    form = EventForm()
    read_only(form.event_geo)
    read_only(form.event_place)
    read_only(form.event_country)
    read_only(form.event_city)
    if request.args == '':
        return redirect('')
    if request.method == 'GET':
        place = request.args
        geolocator = Nominatim(user_agent='habatoo@yandex.ru') 
        try:
            location = geolocator.geocode(place.get('search', default=None))
        except:
            location = None
        if location:
            newLocation = str(location.latitude) + str(", ") + str(location.longitude)  
            location_geo = geolocator.reverse([location.latitude, location.longitude]) # 37.62, 55.75
            address = location_geo.address
            event_country = location_geo.raw['address'].get('country')
            event_city = location_geo.raw['address'].get('city')
            event = Event(
            event_title=None, 
            event_body=None, 
            event_time=None,
            event_place = address,
            event_geo = newLocation,
            event_country = event_country,
            event_city = event_city,
            event_level = None,
            event_private = False,
            event_author = current_user)
            form = EventForm(
                formdata=request.form, obj=event)
            return render_template('events/new_event.html', form=form, users=users)
        else:
            print('no search')
            return redirect('')          

    if form.validate_on_submit():

        event = Event(
            event_title=form.event_title.data, 
            event_body=form.event_body.data,
            event_time=form.event_time.data,
            event_place=form.event_place.data,
            event_geo=form.event_geo.data,
            event_level=form.event_level.data,
            event_private=True if form.event_private.data else False,
            event_country=form.event_country.data,
            event_city=form.event_city.data,
            event_author=current_user)
        event.tags.append(Tag.query.filter_by(name=form.tags.data).first())

        user = User.query.filter_by(username=form.events_crew.raw_data[0]).first()
        crew = Crew(
            event_user=user,
            event_crew=event
            ) 
        if Crew.query.filter(Crew.event_user==current_user).first():
            crew = Crew(
                event_user=current_user,
                event_crew=event
            )
        event.events_crew.append(crew)
        db.session.commit()
        flash('Your cane make event!')
        return redirect(url_for('events.index'))
    return render_template('events/new_event.html', form=form, users=users)

@events.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(slug):
    event = Event.query.filter(Event.slug==slug).first()
    users = User.query.all()
    form = EventForm(formdata=request.form, obj=event)

    if form.validate_on_submit():
        event.event_title = form.event_title.data
        event.event_body = form.event_body.data
        event.event_time = form.event_time.data
        event.event_place = form.event_place.data
        event.event_geo = form.event_geo.data
        event.event_level = form.event_level.data
        event.event_country = form.event_country.data
        event.event_city = form.event_city.data
        event.event_private = True if form.event_private.data else False
        try:
            event.tags.append(Tag.query.filter_by(name=form.tags.data).first())
            db.session.commit()
            flash('Your event edited')
            log.info("User '%s' edit event '%s'." % (current_user.username, event.event_title))
            return redirect(url_for('events.event_detail', slug=event.slug))
        except:
           return redirect('events.index')
    form = EventForm(obj=event)
    return render_template('events/edit_event.html', form=form, users=users)

@events.route('/', methods=['GET', 'POST'])
@login_required
def index():
    users = User.query.all()
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    if q:
        events = Event.query.filter(Event.event_title.contains(q) | Event.event_body.contains(q).all())
    else:
        events = Event.query.order_by(Event.created.desc())    
    pages = events.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])
    levels = Level.query.all()
    return render_template('events/index.html', pages=pages, levels=levels, users=users)

@events.route('/<slug>')
@login_required
def event_detail(slug):
    users = User.query.all()
    event = Event.query.filter(Event.slug==slug).first()
    tags = event.tags
    return render_template('events/event_detail.html', event=event, tags=tags, users=users)


@events.route('/<slug>/<username>')
@login_required
def save_event(slug, username):
    event = Event.query.filter(Event.slug==slug).first()
    tags = event.tags
    user = User.query.filter(User.username==username).first()
    if event not in user.save_event:
        user.save_event.append(Event.query.filter(Event.slug==slug).first())
    db.session.commit()
    return render_template(
        'events/event_detail.html', event=event, tags=tags, user=user, current_user=current_user)

@events.route('/<slug>/<username>')
@login_required
def join_event(slug, username):
    event = Event.query.filter(Event.slug==slug).first()
    tags = event.tags
    user = User.query.filter(User.username==username).first()
    if Crew.query.filter(Crew.event_user == user).first():
        crew = Crew(
            event_user=user,
            event_crew=event
        )
        event.events_crew.append(crew)
        db.session.commit()
    return redirect('events.event_detail')

@events.route('/tag/<slug>')
@login_required
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug==slug).first()
    events = tag.events_tags.all()
    return render_template('events/tag_detail.html', tag=tag, events=events)