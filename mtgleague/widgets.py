from wtforms.widgets import Input


class DateInput(Input):
    input_type = 'date'


class DateTimeInput(Input):
    input_type = 'datetime'
