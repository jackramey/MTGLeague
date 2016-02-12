from sqlalchemy import or_

from mtgleague.util import db
from mtgleague.models.match import Match


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __init__(self, user, event):
        self.user = user
        self.event = event

    def get_matches(self):
        return Match.query.filter(or_(Match.p1_id == self.id, Match.p2_id == self.id)).all()

    def get_matches_count(self):
        return Match.query.filter(or_(Match.p1_id == self.id, Match.p2_id == self.id)).count()

    def get_matches_won(self):
        return Match.query.filter_by(winner_id=self.id).all()

    def get_matches_won_count(self):
        return Match.query.filter_by(winner_id=self.id).count()

    def get_matches_lost(self):
        return Match.query.filter_by(loser_id=self.id).all()

    def get_matches_lost_count(self):
        return Match.query.filter_by(loser_id=self.id).count()

    def match_win_percentage(self):
        matches_won = self.get_matches_won_count()
        matches_total = self.get_matches_count()
        return matches_won / matches_total

    def opponent_match_win_percentage(self):
        pass

