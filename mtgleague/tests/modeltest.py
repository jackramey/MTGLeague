import unittest

from datetime import date

from flask import Flask
from flask_testing import TestCase

from mtgleague.models import Event, League, Match, Participant, Stage, User
from mtgleague.util import db


class BaseModelTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config.from_pyfile('test.cfg', False)
        return app

    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()

        u1 = User('user1', 'user1@u1.com', 'u1')
        u2 = User('user2', 'user2@u2.com', 'u2')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        league = League('TestLeague')
        db.session.add(league)
        db.session.commit()

        event = Event('TestEvent', league)
        db.session.add(event)
        db.session.commit()

        stage = Stage(event, date.today(), date.today())
        db.session.add(stage)
        db.session.commit()

        p1 = Participant(u1, event)
        p2 = Participant(u2, event)
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()

        m = Match(stage, p1, p2)
        m.add_results(p1_wins=2,p2_wins=0)
        db.session.add(m)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()


class ModelTest(BaseModelTest):

    def test(self):
        user = User.query.filter_by(email='user1@u1.com').first()
        assert user is not None

        league = League.query.filter_by(name='TestLeague').first()
        assert league is not None

        event = Event.query.filter_by(name='TestEvent').first()
        assert event is not None
        assert event.league is league

        u1 = User.query.filter_by(email='user1@u1.com').first()
        p1 = Participant.query.filter_by(user_id=u1.id).first()
        assert p1 is not None

        u2 = User.query.filter_by(email='user2@u2.com').first()
        p2 = Participant.query.filter_by(user_id=u2.id).first()
        assert p2 is not None

        stage = Stage.query.filter_by(event_id=event.id).first()
        assert stage is not None

        match = Match.query.filter_by(stage_id=stage.id).first()
        assert match is not None
        assert match.participant1 is p1
        assert match.participant2 is p2
        assert match.winner is p1
        assert match.loser is p2

if __name__ == '__main__':
    unittest.main()
