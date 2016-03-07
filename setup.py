from mtgleague import app
from mtgleague.util import db
from mtgleague.models import User

name = app.config['DEFAULT_ADMIN']
email = app.config['DEFAULT_ADMIN_EMAIL']
password = app.config['DEFAULT_ADMIN_PASSWORD']

admin = User.query.filter_by(email=email).first()
if admin is not None:
    if not admin.admin:
        admin.admin = True
        db.session.commit()
else:
    admin = User(name, email, password)
    admin.admin = True
    db.session.add(admin)
    db.session.commit()

