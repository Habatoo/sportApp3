from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from wtforms import TextAreaField, SelectMultipleField

from flask_wtf import FlaskForm

from app import app
from app.models import *

tier_choices = [(tier.tier_id, tier.title) for tier in Tier.query.all()]

class CabinetForm(FlaskForm):
    user_firstname = StringField('First name', validators=[DataRequired()])
    user_lastname = StringField('Last name', validators=[DataRequired()])

    user_age = IntegerField('Age', validators=[DataRequired()])
    user_phone = StringField('Phone', validators=[DataRequired()])

    user_address = TextAreaField('Address', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    sponsor_tier = RadioField('Select tiers', choices=tier_choices, validators=[DataRequired()])
    submit = SubmitField('Submit')
