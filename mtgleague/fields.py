from mtgleague.widgets import DateInput, DateTimeInput
from wtforms.fields import DateField, DateTimeField


class MyDateField(DateField):
    widget = DateInput()


class MyDateTimeField(DateTimeField):
    widget = DateTimeInput()
