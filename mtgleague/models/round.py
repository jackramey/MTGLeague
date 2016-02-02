from mtgleague.util import db


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __init__(self, start_date, end_date, event):
        self.start_date = start_date
        self.end_date = end_date
        self.event_id = event.id
