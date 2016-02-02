from mtgleague.util import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    draw = db.Column(db.Boolean)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    loser_id = db.Column(db.Integer, db.ForeignKey('participant.id'))

    winner = db.relationship('Participant', foreign_keys=[winner_id])
    loser = db.relationship('Participant', foreign_keys=[loser_id])

    def __init__(self, match, draw=False, winner=None, loser=None):
        self.match = match
        self.draw = draw
        if not draw:
            self.winner = winner
            self.loser = loser
