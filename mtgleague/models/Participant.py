from mtgleague.util import db
from mtgleague.models.match import Match


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __init__(self, user, event):
        self.user = user
        self.event = event
