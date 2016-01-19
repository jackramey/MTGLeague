from mtgleague import app
from flask.ext.bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer

#Bcrypt
bcrypt = Bcrypt(app)

#Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#Database
db = SQLAlchemy(app)

#Login Serializer
login_serializer = URLSafeTimedSerializer(app.secret_key)

