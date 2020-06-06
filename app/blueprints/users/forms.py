from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from wtforms import TextAreaField

from flask_wtf import FlaskForm


from app import app
from app.models import *

cities = app.config['CITIES']


class EditProfileForm(FlaskForm):
    pass