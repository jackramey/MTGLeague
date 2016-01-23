from flask import Flask

#Create the app
app = Flask(__name__)
app.config.from_pyfile('mtgleague.cfg', False)

from mtgleague.views.index import *
from mtgleague.views.league import *
from mtgleague.views.event import *
