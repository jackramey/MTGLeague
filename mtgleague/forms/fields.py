from wtforms.fields import DateField, DateTimeField
from mtgleague.forms import widgets


class MyDateField(DateField):
    widget = widgets.DateInput()


class MyDateTimeField(DateTimeField):
    widget = widgets.DateTimeInput()
