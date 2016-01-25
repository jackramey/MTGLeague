from mtgleague import widgets
from wtforms.fields import DateField, DateTimeField


class MyDateField(DateField):
    widget = widgets.DateInput()


class MyDateTimeField(DateTimeField):
    widget = widgets.DateTimeInput()
