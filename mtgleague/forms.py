from mtgleague.fields import MyDateField
from flask_wtf import Form
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class EventForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    start_date = MyDateField('Start Date', format="%m/%d/%Y")
    end_date = MyDateField('End Date', format="%m/%d/%Y")
    submit = SubmitField('Submit', validators=[DataRequired()])


class LeagueForm(Form):
    name = StringField('Name', validators=[DataRequired()])
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