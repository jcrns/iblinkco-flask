# Importing all forms for user validation
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo 

class WebsitesForm(FlaskForm):
    # Setting login fields
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')