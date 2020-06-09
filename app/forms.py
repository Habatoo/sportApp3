from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from wtforms import TextAreaField
from flask_security.forms import RegisterForm, ConfirmRegisterForm

from app import app
from app.models import *


cities = app.config['CITIES']

class LoginForm(FlaskForm):
    pass

class ExtendedRegisterForm(RegisterForm, FlaskForm):
    username = StringField('Display name', validators=[DataRequired()])
    city = RadioField('Select your city', default = '', validators=[DataRequired()],
                    choices=[(city['label'], city['value']) for city in cities])

class ExtendedConfirmRegisterForm(ExtendedRegisterForm, ConfirmRegisterForm):
    pass

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')

    # def validate_email(self, email):
    #     email = User.query.filter_by(email=email.data).first()
    #     if email is not None:
    #         raise ValidationError('Please use a different email.')
