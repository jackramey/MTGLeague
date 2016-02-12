import unittest

from datetime import date

from flask import Flask
from flask_testing import TestCase

from mtgleague.util import db

from mtgleague.models.event import Event
from mtgleague.models.league import League
from mtgleague.models.match import Match
from mtgleague.models.participant import Participant
from mtgleague.models.round import Round
from mtgleague.models.user import User


class BaseModelTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config.from_pyfile('test.cfg', False)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class UserTest(BaseModelTest):

    def test(self):
        user = User('user', 'user@uuser.com', 'u')
        db.session.add(user)
        db.session.commit()

        assert user in db.session


class LeagueTest(BaseModelTest):

    def test(self):
        league = League('TestLeague')
        db.session.add(league)
        db.session.commit()

        assert league in db.session


class EventTest(BaseModelTest):
    def test(self):
        league = League('TestLeague')
        db.session.add(league)
        db.session.commit()

        event = Event('TestEvent', league)
        db.session.add(event)
        db.session.commit()

        assert event in db.session

class MainDbTest(BaseModelTest):

    def test(self):
        u1 = User('user1', 'user1@u1.com', 'u1')
        u2 = User('user2', 'user2@u2.com', 'u2')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        assert u1 in db.session
        assert u2 in db.session

        league = League('TestLeague')
        db.session.add(league)
        db.session.commit()

        assert league in db.session

        event = Event('TestEvent', league)
        db.session.add(event)
        db.session.commit()

        assert event in db.session

        r = Round(date.today(), date.today(), event)
        db.session.add(r)
        db.session.commit()

        assert r in db.session

        p1 = Participant(u1, event)
        p2 = Participant(u2, event)
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()

        assert p1 in db.session
        assert p2 in db.session

        m = Match(p1, p2)
        db.session.add(m)
        db.session.commit()

        assert m in db.session

        g1 = Game(m, winner=p1, loser=p2)
        db.session.add(g1)
        db.session.commit()

        assert g1 in db.session

if __name__ == '__main__':
    db.drop_all()
    unittest.main()
