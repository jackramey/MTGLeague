from mtgleague.util import db

from mtgleague.models.game import Game


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p1_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    p2_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))
    games = db.relationship('Game', backref='match', lazy='dynamic')

    participant1 = db.relationship('Participant', foreign_keys=[p1_id])
    participant2 = db.relationship('Participant', foreign_keys=[p2_id])

    def __init__(self, participant1, participant2):
        self.participant1 = participant1
        self.participant2 = participant2
