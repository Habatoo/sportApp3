from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, BooleanField, PasswordField, SelectField, DateTimeField
from wtforms.validators import DataRequired
from wtforms import TextAreaField
from flask_security.forms import RegisterForm, ConfirmRegisterForm, LoginForm

from datetime import datetime

from app import app
from app.models import *


tag_choices = [(tag.name, tag.name) for tag in Tag.query.all()]
cities = [(event.event_city, event.event_city) for event in Event.query.all()]
levels = [(level.description, level.description) for level in Level.query.all()]
themes = [(theme.name, theme.name) for theme in Theme.query.all()]
clubs = [(club.name, club.name) for club in Club.query.all()]
############################# TODO - change to ==True
trainers = [(trainer.username, trainer.username) for trainer in User.query.filter(User.mentor!=True)]

class ExtendedLoginForm(LoginForm, FlaskForm):
    email = StringField('Email', validators=[DataRequired()], default='guest@guest.com')
    password = PasswordField('Password', validators=[DataRequired()], default='guest')
    remember_me = BooleanField('Remember Me')
    submit2 = SubmitField('Explore as Guest')

class ExtendedRegisterForm(RegisterForm, FlaskForm):
    username = StringField('Display name', validators=[DataRequired()])
    city = RadioField('Select your city', default = '', validators=[DataRequired()],
                    choices=[(city['label'], city['value']) for city in app.config['CITIES']])

class ExtendedConfirmRegisterForm(ExtendedRegisterForm, ConfirmRegisterForm):
    pass

class IndexFindForm(FlaskForm):
    f_city = SelectField('Select your city', validators=[DataRequired()],
                    choices=set(cities))
    # f_theme = SelectField('Select theme', choices=themes, default=None)
    f_exercise = SelectField('Select your hobby', choices=tag_choices, default=None)
    f_levels = SelectField('Select hobby levels', choices=levels, default=None)
    # f_clubs = SelectField('Select clubs', choices=clubs, default=None)
    f_time = DateTimeField('Select date from current to ...', default=datetime.now)
    f_trainers = SelectField('Select trainer', choices=trainers, default=None)

    submit = SubmitField('Submit')
