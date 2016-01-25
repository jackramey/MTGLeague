from mtgleague.util import db
from mtgleague.models.event import Event
from mtgleague.models.league import League
from mtgleague.models.participant import Participant
from mtgleague.models.round import Round
from mtgleague.models.user import User

db.drop_all()
db.create_all()
