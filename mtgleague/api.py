from flask.views import MethodView
from flask_login import login_required
from mtgleague.models import League, Membership, User
from mtgleague.schemas import LeagueSchema, MembershipSchema, UserSchema


class LeagueAPI(MethodView):
    league_schema = LeagueSchema()

    @login_required
    def get(self, lid):
        league = League.query.filter_by(id=lid).first()
        return self.league_schema.jsonify(league)

    @login_required
    def post(self, lid):
        return 'got it: ' + lid


class MembershipAPI(MethodView):
    membership_schema = MembershipSchema()

    @login_required
    def get(self, mid):
        membership = Membership.query.filter_by(id=mid).first()
        return self.membership_schema.jsonify(membership)


class UserAPI(MethodView):
    user_schema = UserSchema()

    @login_required
    def get(self, uid):
        user = User.query.filter_by(id=uid).first()
        return self.user_schema.jsonify(user)


class UsersAPI(MethodView):
    user_schema = UserSchema(exclude='password_hash')

    @login_required
    def get(self):
        users = User.query.all()
        return self.user_schema.jsonify(users)
