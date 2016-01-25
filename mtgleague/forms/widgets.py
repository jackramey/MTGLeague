from wtforms.widgets import Input


class DateInput(Input):
    """
    returns a date picker widget from bootstrap
    """
    input_type = 'date'


class DateTimeInput(Input):
    """

    """
    input_type = 'datetime'
