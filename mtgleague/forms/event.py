from flask_wtf import Form
from wtforms import StringField
from mtgleague.forms.fields import MyDateField
from wtforms.validators import DataRequired


class EventForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    start_date = MyDateField('Start Date', format="%m/%d/%Y")
    end_date = MyDateField('End Date', format="%m/%d/%Y")
