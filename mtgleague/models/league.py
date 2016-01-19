from mtgleague.util import db
from mtgleague.models.event import Event
from mtgleague.models.user import User


class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    events = db.relationship('Event', backref='league',
                             lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<{0}: {1}, {2}>'.format(self.__class__.__name__, self.id, self.name)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

