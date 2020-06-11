from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired
from wtforms import TextAreaField
from flask_security.forms import RegisterForm, ConfirmRegisterForm

from app import app
from app.models import *


class LoginForm(FlaskForm):
    pass

class ExtendedRegisterForm(RegisterForm, FlaskForm):
    username = StringField('Display name', validators=[DataRequired()])
    city = RadioField('Select your city', default = '', validators=[DataRequired()],
                    choices=[(city['label'], city['value']) for city in app.config['CITIES']])

class ExtendedConfirmRegisterForm(ExtendedRegisterForm, ConfirmRegisterForm):
    pass
