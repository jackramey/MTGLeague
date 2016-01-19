from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from mtgleague import app
from mtgleague.views.scaffold import BaseView
from mtgleague.models.league import League

class LeagueView(BaseView):
    methods = ['GET']

    def handle_request(self, lid, *args, **kwargs):
        league = League.query.filter_by(id='lid').first()
        return 'League: {0!r}'.format(league)

class LeaguesView(BaseView):
    methods = ['GET']

    def handle_request(self, *args, **kwargs):
        leagues = League.query.all()
        ret = ''
        for league in leagues:
            ret = repr(league) + '\n'
        return ret

#Page View Rules
app.add_url_rule('/league/<lid>',
                 view_func=LeagueView.as_view('league'))
app.add_url_rule('/leagues/',
                 view_func=LeaguesView.as_view('leagues'))
