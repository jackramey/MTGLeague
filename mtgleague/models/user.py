from flask_login import AnonymousUserMixin, UserMixin
from mtgleague.util import bcrypt, db, login_manager, login_serializer


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(254), unique=True)
    password_hash = db.Column(db.String(64))
    admin = db.Column(db.Boolean)

    participants = db.relationship('Participant', backref='user', lazy='dynamic')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)

    def check_password(self, password):
            return bcrypt.check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def is_admin(self):
        return self.admin

    def is_anonymous(self):
        return False

    def get_auth_token(self):
        data = [str(self.id), self.password_hash]
        return login_serializer.dumps(data)

    def get_matches(self):
        matches = []
        for p in self.participants:
            matches.extend(p.get_matches())
        return matches

    def get_matches_count(self):
        num_matches = 0
        for p in self.participants:
            num_matches += p.get_matches_count()
        return num_matches

    def get_matches_won(self):
        matches_won = []
        for p in self.participants:
            matches_won.extend(p.get_matches_won())
        return matches_won

    def get_matches_won_count(self):
        num_matches_won = 0
        for p in self.participants:
            num_matches_won += p.get_matches_won_count()
        return num_matches_won

    def match_win_percentage(self):
        return self.get_matches_won_count() / self.get_matches_count()

    def __repr__(self):
        return '<{0}: {1}, {2}>'.format(self.__class__.__name__, self.name, self.email)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Anonymous(AnonymousUserMixin):

    def is_admin(self):
        return False

    def is_anonymous(self):
        return True


@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()


@login_manager.token_loader
def load_token(token):
    data = login_serializer.loads(token)
    user = User.query.filter_by(id=data[0]).first()
    if user and data[1] == user.password_hash:
        return user
    return None

login_manager.anonymous_user = Anonymous
