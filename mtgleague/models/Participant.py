from mtgleague.util import db


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __init__(self, user, event):
        self.user_id = user.id
        self.event_id = event.id
