from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from mtgleague import app
from mtgleague import db
from mtgleague.views.scaffold import BaseView
from mtgleague.forms.league import LeagueForm
from mtgleague.models.league import League

class LeagueView(BaseView):
    methods = ['GET']

    def handle_request(self, lid, *args, **kwargs):
        league = League.query.filter_by(id=lid).first()
        return 'League: {0}'.format(league)


class LeagueCreateView(BaseView):
    methods = ['GET', 'POST']

    def handle_request(self, *args, **kwargs):
        action_text = 'Create'
        action_url = url_for('league_create')
        form = LeagueForm()
        if form.validate_on_submit():
            league = League(form.name.data)
            db.session.add(league)
            db.session.commit()
            return redirect(url_for('league', lid=league.id))
        else:
            return render_template('league-edit.html', form=form, action_text=action_text, action_url=action_url,
                                   **self.context)


class LeagueEditView(BaseView):
    methods = ['GET', 'POST']

    def handle_request(self, lid, *args, **kwargs):
        action_text = 'Save'
        action_url = url_for('league_edit', lid=lid)
        league = League.query.filter_by(id=lid).first_or_404()
        form = LeagueForm(obj=league)
        if form.validate_on_submit():
            league.name = form.name.data
            db.session.commit()
            return redirect(url_for('league', lid=league.id))
        else:
            return render_template('league-edit.html', form=form, action_url=action_url, action_text=action_text,
                                   **self.context)


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
app.add_url_rule('/league/create',
                 view_func=LeagueCreateView.as_view('league_create'))
app.add_url_rule('/league/<lid>/edit',
                 view_func=LeagueEditView.as_view('league_edit'))
app.add_url_rule('/leagues/',
                 view_func=LeaguesView.as_view('leagues'))
