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

