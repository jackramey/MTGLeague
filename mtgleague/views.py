from flask import redirect, render_template, url_for
from flask.views import View
from flask_login import current_user, login_required, login_user, logout_user

from mtgleague.forms import EventForm, LeagueForm, LoginForm, RegisterForm
from mtgleague.models import Event, Match, League, Participant, User
from mtgleague.util import db


class BaseView(View):
    context = {}

    def prepare(self, *args, **kwargs):
        # Any processing that needs to happen before each request is handled
        # gets taken care of here
        pass

    def handle_request(self, *args, **kwargs):
        """Subclasses have to override this method to implement the
        actual view function code.  This method is called with all
        the arguments from the URL rule.
        """
        raise NotImplementedError()

    def dispatch_request(self, *args, **kwargs):
        self.context = dict()
        self.prepare(self, *args, **kwargs)
        return self.handle_request(*args, **kwargs)


class EventView(BaseView):
    methods = ['GET']

    def handle_request(self, eid, *args, **kwargs):
        event = Event.query.filter_by(id=eid).first_or_404()
        return "Event: {0}".format(event)


class EventCreateView(BaseView):
    methods = ['GET', 'POST']

    def handle_request(self, lid, *args, **kwargs):
        action_text = 'Create'
        action_url = url_for('event_create', lid=lid)
        form = EventForm()
        league = League.query.filter_by(id=lid).first_or_404()
        if form.validate_on_submit():
            event = Event(form.name.data, league)
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('event', eid=event.id))
        else:
            return render_template('event-edit.html', form=form, action_text=action_text, action_url=action_url,
                                   **self.context)


class EventEditView(BaseView):
    methods = ['GET', 'POST']

    def handle_request(self, eid, *args, **kwargs):
        action_text = 'Edit'
        action_url = url_for('event_edit', eid=eid)
        event = Event.query.filter_by(id=eid).first_or_404()
        form = EventForm(obj=event)
        if form.validate_on_submit():
            event.name = form.name.data
            db.session.commit()
            return redirect(url_for('event', eid=event.id))
        else:
            return render_template('event-edit.html', form=form, action_text=action_text, action_url=action_url,
                                   **self.context)


class EventsView(BaseView):
    methods = ['GET']

    def handle_request(self, *args, **kwargs):
        return "Events"



class IndexView(BaseView):
    methods = ['GET']

    def handle_request(self):
        return render_template('index.html', **self.context)


class LoginView(BaseView):
    methods = ['GET', 'POST']

    def handle_request(self, *args, **kwargs):
        form = LoginForm()
        errors = []
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.lower()).first()
            if user is None:
                errors.append("That user does not exist.")
                return render_template('login.html', form=form, errors=errors)
            else:
                if user.check_password(form.password.data):
                    login_user(user, remember=True)
                    return redirect(url_for('index'))
                else:
                    errors.append("Username and Password combination are incorrect.")
                    return render_template('login.html', form=form, errors=errors, **self.context)
        else:
            return render_template('login.html', form=form, errors=errors, **self.context)


class LogoutView(BaseView):
    methods = ['GET']

    def handle_request(self, *args, **kwargs):
        logout_user()
        return redirect(url_for('index'))


class RegisterView(BaseView):
    methods = ['GET', 'POST']

    def handle_request(self, *args, **kwargs):
        errors = []
        form = RegisterForm()
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data.lower()).first() is not None:
                errors.append("A user has already registered this email address.")
                return render_template('register.html', form=form, errors=errors, **self.context)
            else:
                new_user = User(form.name.data, form.email.data, form.password.data)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('index'))
        else:
            return render_template('register.html', form=form, **self.context)


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