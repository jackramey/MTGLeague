from mtgleague.util import db
from mtgleague.models.league import League

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    league_id = db.Column(db.Integer, db.ForeignKey('legaue.id'))
    league = db.relationship('League',
        backref=db.backref('events', lazy='dynamic'))

    def __repr__(self):
        return '<{0}: {1}, {2}>'.format(self.__class__.__name__, self.name, self.league)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

