from mtgleague.util import ma
from mtgleague.models import Event, League, Match, Membership, User


class EventSchema(ma.ModelSchema):
    class Meta:
        model = Event


class LeagueSchema(ma.ModelSchema):
    class Meta:
        model = League


class MatchSchema(ma.ModelSchema):
    class Meta:
        model = Match


class MembershipSchema(ma.ModelSchema):
    class Meta:
        model = Membership


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        exclude = ["email", "password_hash"]
