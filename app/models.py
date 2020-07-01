from datetime import datetime
from time import time
import re
import os
import jwt

from flask_security import UserMixin, RoleMixin
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user

from app import app, login, db
from app.forms import *

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def slugify(string):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', string)

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

user_tags = db.Table(
    'user_tags', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

post_tags = db.Table(
    'post_tags', 
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

event_tags = db.Table(
    'event_tags', 
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

photo_tags = db.Table(
    'photo_tags', 
    db.Column('photo_id', db.Integer, db.ForeignKey('photo.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '{}'.format(self.name)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    social_id = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(255))
    confirmed_at = db.Column(db.DateTime)

    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    timestamp = db.Column(db.String(128), default=int(time()))
    city = db.Column(db.String(128))

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean)

    mentor = db.Column(db.Boolean, default=False)
    level = db.Column(db.Integer, default=0)
    
    roles = db.relationship(
        'Role', secondary=roles_users, backref=db.backref('users_roles', lazy='dynamic'))

    tags = db.relationship(
        'Tag', secondary=user_tags, backref=db.backref('users_tags', lazy='dynamic'))

    last_login_at = db.Column(db.DateTime, default=datetime.now)
    current_login_at = db.Column(db.DateTime, default=datetime.now)
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer, default=0)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    events = db.relationship('Event', backref='event_author', lazy='dynamic')
    photos = db.relationship('Photo', backref='photo_author', lazy='dynamic')

    def avatar(self):
        return 'user_data/{}/avatar/avatar.png'.format(self.username + self.timestamp)
 
#### FLASK SECURITY #############
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
#################################

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    tags = db.relationship(
        'Tag', secondary=post_tags, backref=db.backref('posts_tags', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title + str(int(time())))

class Event(db.Model):
    # https://overpass.openstreetmap.ru/api/interpreter
    # https://overpass.openstreetmap.fr/api/interpreter no attic
    # https://overpass-api.de/api/interpreter
    id = db.Column(db.Integer, primary_key=True)
    event_title = db.Column(db.String(140))
    event_body = db.Column(db.Text)
    slug = db.Column(db.String(140), unique=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    event_time = db.Column(db.DateTime)
    event_place = db.Column(db.Text)
    event_geo = db.Column(db.Text)

    event_starter = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_crew = db.Column(db.Text)
    event_level = db.Column(db.Integer)

    tags = db.relationship(
        'Tag', secondary=event_tags, backref=db.backref('events_tags', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.event_title:
            self.slug = slugify(self.event_title + str(int(time())))

    def check_date(self, *args, **kwargs):
        pass
    #     if not self.event_time:
    #         raise ValidationError("Event time missing. Please check the data")
    #     if not self.created >= self.event_time:
    #         raise ValidationError("Event time must be greater than now")
    #     super().check_date(*args, **kwargs)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_title = db.Column(db.String(100))
    photo_description = db.Column(db.String(255))
    slug = db.Column(db.String(140), unique=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship(
        'Tag', secondary=photo_tags, backref=db.backref('photos_tags', lazy='dynamic'))