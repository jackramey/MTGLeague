from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from mtgleague import app
from mtgleague.util import db
from mtgleague.views.scaffold import BaseView
from mtgleague.forms import EventForm
from mtgleague.models.event import Event
from mtgleague.models.league import League


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


# Page View Rules
app.add_url_rule('/event/<eid>',
                 view_func=EventView.as_view('event'))
app.add_url_rule('/league/<lid>/event/create',
                 view_func=EventCreateView.as_view('event_create'))
app.add_url_rule('/event/<eid>/edit',
                 view_func=EventEditView.as_view('event_edit'))
app.add_url_rule('/events/',
                 view_func=EventsView.as_view('events'))
