from mtgleague.util import db
from mtgleague.models.participant import Participant


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    league_id = db.Column(db.Integer, db.ForeignKey('league.id'))
    participants = db.relationship('Participant', backref='event',
                                   lazy='dynamic')

    def __init__(self, name, league):
        self.name = name
        self.league_id = league.id

    def __repr__(self):
        return '<{0}: {1}, {2}>'.format(self.__class__.__name__, self.name, self.league)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

