from mtgleague.util import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    league_id = db.Column(db.Integer, db.ForeignKey('league.id'))

    def __repr__(self):
        return '<{0}: {1}, {2}>'.format(self.__class__.__name__, self.name, self.league)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

