from mtgleague.util import db
from mtgleague.models.match import Match


class EventRound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    matches = db.relationship('Match', backref='round', lazy='dynamic')

    def __init__(self, event, start_date, end_date):
        self.event = event
        self.start_date = start_date
        self.end_date = end_date
