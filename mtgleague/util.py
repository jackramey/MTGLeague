from flask import redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer

from mtgleague import app

#Bcrypt
bcrypt = Bcrypt(app)

#Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#Flask Admin
admin = Admin(app, name='mtgleague', template_mode='bootstrap3')

class MTGLeagueModelView(ModelView):

    def is_accessible(self):
        return current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('index'))

#Database
db = SQLAlchemy(app)

#Login Serializer
login_serializer = URLSafeTimedSerializer(app.secret_key)

