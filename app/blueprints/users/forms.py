from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from wtforms import TextAreaField

from flask_wtf import FlaskForm


from app import app
from app.models import *

cities = app.config['CITIES']
tag_choices = [(tag.name, tag.slug)  for tag in Tag.query.all()]

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    city = RadioField('Select your city', validators=[DataRequired()],
                    choices=[(city['label'], city['value']) for city in cities])
    tags = RadioField('Select your hobby', validators=[DataRequired()],
                    choices=tag_choices)               
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')