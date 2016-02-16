from mtgleague.fields import MyDateField
from flask_wtf import Form
from wtforms import PasswordField, StringField, SubmitField, FieldList, FormField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo


class StageForm(Form):
    start_date = DateField('Start Date', format="%Y-%m-%d")
    end_date = DateField('End Date', format="%Y-%m-%d")


class EventForm(Form):
    name = StringField('Event Name', validators=[DataRequired()])
    stages = FieldList(FormField(StageForm), min_entries=2)
    submit = SubmitField('Submit', validators=[DataRequired()])


class LeagueForm(Form):
    name = StringField('League Name', validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])


class RegisterForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Submit', validators=[DataRequired()])
