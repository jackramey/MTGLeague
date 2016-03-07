from flask import Flask
import os
from wtforms.fields import HiddenField

# Create the app
app = Flask(__name__)
app.config.from_pyfile('mtgleague.cfg', False)
app.config.from_object('config')


# Jinja Template Additions
def is_hidden_field_filter(field):
    return isinstance(field, HiddenField)

app.jinja_env.globals['is_hidden_field'] =\
    is_hidden_field_filter


# Logging
if not app.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/mtgleague.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('MTGLeague startup')

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('microblog startup')

from mtgleague.routes import *
