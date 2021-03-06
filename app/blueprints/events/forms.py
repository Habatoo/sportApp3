from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from wtforms import TextAreaField
from wtforms.fields.html5 import DateTimeField # DateTimeLocalField



from flask_wtf import FlaskForm

from app import app
from app.models import *

tag_choices = [(tag.name, tag.slug) for tag in Tag.query.all()]
user_choices = [(user.username, user.id) for user in User.query.all()]
levels = [(level.description, level.description) for level in Level.query.all()]
themes = [(theme.name, theme.name) for theme in Theme.query.all()]
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
    event_country = TextAreaField('Country', validators=[DataRequired()])
    event_city = TextAreaField('City', validators=[DataRequired()])
    event_geo = TextAreaField('GEO, long, lat', validators=[DataRequired()])
    event_level = SelectField('Select hobby levels', choices=levels, validators=[DataRequired()])
    tags = RadioField('Select tags', choices=tag_choices)
    theme = SelectField('Select theme', choices=themes, validators=[DataRequired()])
    events_crew = RadioField('Select users', choices=user_choices, default=None)
    event_private = BooleanField('Private/public event')

    submit = SubmitField('Submit')
