from datetime import datetime

from mtgleague.util import db


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))
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

    def __init__(self, round, participant1, participant2):
        self.round = round
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

