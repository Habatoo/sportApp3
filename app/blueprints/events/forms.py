from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from wtforms import TextAreaField
from wtforms.fields.html5 import DateTimeLocalField


from flask_wtf import FlaskForm

from app import app
from app.models import *

tag_choices = [(tag.name, tag.slug)  for tag in Tag.query.all()]


class EventForm(FlaskForm):
    event_title = StringField('Title', validators=[DataRequired()])
    event_body = TextAreaField('Event', validators=[DataRequired()])
    event_time = DateTimeLocalField(
        'Select date and time of event', format='%d.%m.%Y %H:%M', default=datetime.today) #, validators=[DataRequired()])
    event_place = TextAreaField('Place, address', validators=[DataRequired()])
    event_geo = TextAreaField('GEO, long, lat', validators=[DataRequired()])
    event_level = StringField('Event level', validators=[DataRequired()])
    tags = RadioField(
        'Select tags', choices=tag_choices)
    # event_crew = db.Column(db.Integer, db.ForeignKey('user.id'))
    submit = SubmitField('Submit')
