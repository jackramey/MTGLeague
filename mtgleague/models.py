from datetime import datetime
from sqlalchemy import or_

from flask_login import AnonymousUserMixin, UserMixin

from mtgleague.util import bcrypt, db, login_manager, login_serializer


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    league_id = db.Column(db.Integer, db.ForeignKey('league.id'))
    participants = db.relationship('Participant', backref='event',
                                   lazy='dynamic')
    stages = db.relationship('Stage', backref='event', lazy='dynamic')

    def __init__(self, name, league):
        self.name = name
        self.league_id = league.id

    def __repr__(self):
        return '<{0}: {1}, {2}>'.format(self.__class__.__name__, self.name, self.league)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    events = db.relationship('Event', backref='league', lazy='dynamic')
    members = db.relationship('Membership', backref='league', lazy='dynamic')

    def __init__(self, name, creator):
        self.name = name
        self.creator = creator

    def add_memeber(self, user):
        membership = Membership(user, self)
        db.session.add(membership)
        db.session.commit()

    def editable_by_user(self, user):
        return user.id == self.creator_id

    def __repr__(self):
        return '<{0}: {1}, {2}>'.format(self.__class__.__name__, self.id, self.name)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.id'))
    p1_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    p2_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    loser_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    p1_wins = db.Column(db.Integer)
    p2_wins = db.Column(db.Integer)
    draws = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    participant1 = db.relationship('Participant', foreign_keys=[p1_id])
    participant2 = db.relationship('Participant', foreign_keys=[p2_id])
    winner = db.relationship('Participant', foreign_keys=[winner_id])
    loser = db.relationship('Participant', foreign_keys=[loser_id])

    def __init__(self, stage, participant1, participant2):
        self.stage = stage
        self.participant1 = participant1
        self.participant2 = participant2

    def add_results(self, p1_wins=0, p2_wins=0, draws=0):
        pass
        self.p1_wins = p1_wins
        self.p2_wins = p2_wins
        self.draws = draws
        self.timestamp = datetime.now()
        if p1_wins >= 2:
            # set p1 as winner
            self.winner = self.participant1
            self.loser = self.participant2
        if p2_wins >= 2:
            # set p2 as winner
            self.winner = self.participant2
            self.loser = self.participant1
        db.session.commit()


class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    league_id = db.Column(db.Integer, db.ForeignKey('league.id'))

    def __init__(self, user, league):
        self.user = user
        self.league = league


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __init__(self, user, event):
        self.user = user
        self.event = event

    def get_matches(self):
        return Match.query.filter(or_(Match.p1_id == self.id, Match.p2_id == self.id)).all()

    def get_matches_count(self):
        return Match.query.filter(or_(Match.p1_id == self.id, Match.p2_id == self.id)).count()

    def get_matches_won(self):
        return Match.query.filter_by(winner_id=self.id).all()

    def get_matches_won_count(self):
        return Match.query.filter_by(winner_id=self.id).count()

    def get_matches_lost(self):
        return Match.query.filter_by(loser_id=self.id).all()

    def get_matches_lost_count(self):
        return Match.query.filter_by(loser_id=self.id).count()

    def match_win_percentage(self):
        matches_won = self.get_matches_won_count()
        matches_total = self.get_matches_count()
        return matches_won / matches_total

    def opponent_match_win_percentage(self):
        pass


class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    matches = db.relationship('Match', backref='stage', lazy='dynamic')

    def __init__(self, event, start_date, end_date):
        self.event = event
        self.start_date = start_date
        self.end_date = end_date


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(254), unique=True)
    password_hash = db.Column(db.String(64))
    admin = db.Column(db.Boolean)

    created_leagues = db.relationship('League', backref='creator', lazy='dynamic')
    memberships = db.relationship('Membership', backref='user', lazy='dynamic')
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

    def is_member(self, league):
        leagues = [membership.league for membership in self.memberships]
        return league in leagues

    def get_auth_token(self):
        data = [str(self.id), self.password_hash.decode('utf-8')]
        return login_serializer.dumps(data)

    def get_leagues(self):
        return [membership.league for membership in self.memberships]

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


class AnonymousUser(AnonymousUserMixin):

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

login_manager.anonymous_user = AnonymousUser
