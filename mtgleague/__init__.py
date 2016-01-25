from flask import Flask
from wtforms.fields import HiddenField

# Create the app
app = Flask(__name__)
app.config.from_pyfile('mtgleague.cfg', False)


# Jinja Template Additions
def is_hidden_field_filter(field):
    return isinstance(field, HiddenField)

app.jinja_env.globals['is_hidden_field'] =\
    is_hidden_field_filter

# Logging
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/mtgleague.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('MTGLeague startup')

from mtgleague.views.index import *
from mtgleague.views.league import *
from mtgleague.views.event import *
