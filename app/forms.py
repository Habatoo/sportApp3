from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from wtforms import TextAreaField
from flask_security.forms import RegisterForm, ConfirmRegisterForm, LoginForm

from app import app
from app.models import *


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
