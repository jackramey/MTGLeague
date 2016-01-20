from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class LeagueForm(Form):
    name = StringField('Name', validators=[DataRequired()])
