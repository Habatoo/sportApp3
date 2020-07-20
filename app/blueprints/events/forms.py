from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from wtforms import TextAreaField
from wtforms.fields.html5 import DateTimeField # DateTimeLocalField


from flask_wtf import FlaskForm

from app import app
from app.models import *

tag_choices = [(tag.name, tag.slug)  for tag in Tag.query.all()]
user_choices = [(user.username, user.id)  for user in User.query.all()]

string_of_files = ['private', 'public']
list_of_files = string_of_files[0].split()
# create a list of value/description tuples
files = [(x, x) for x in list_of_files]

class EventForm(FlaskForm):
    event_title = StringField('Title', validators=[DataRequired()])
    event_body = TextAreaField('Event', validators=[DataRequired()])
    # event_time = DateTimeField('Select date and time of event', format='%d.%m.%Y %H:%M')
    event_time = DateTimeField('Select date and time of event')
    event_place = TextAreaField('Place, address', validators=[DataRequired()])
    event_geo = TextAreaField('GEO, long, lat', validators=[DataRequired()])
    event_level = StringField('Event level', validators=[DataRequired()])
    tags = RadioField('Select tags', choices=tag_choices)

    events_crew = SelectField('Select users', choices=user_choices, default=None)
    # event_private = BooleanField('Private/public event')
    event_private = BooleanField()
    submit = SubmitField('Submit')
