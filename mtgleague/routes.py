from mtgleague import app
from mtgleague.views import *

# General Navigation View Rules
app.add_url_rule('/',
                 view_func=IndexView.as_view('index'))
app.add_url_rule('/login',
                 view_func=LoginView.as_view('login'))
app.add_url_rule('/logout',
                 view_func=LogoutView.as_view('logout'))
app.add_url_rule('/register',
                 view_func=RegisterView.as_view('register'))

# General User Navigation
app.add_url_rule('/myleagues',
                 view_func=MyLeaguesView.as_view('myleagues'))

# Event View Rules
app.add_url_rule('/event/<eid>',
                 view_func=EventView.as_view('event'))
app.add_url_rule('/league/<lid>/event/create',
                 view_func=EventCreateView.as_view('event_create'))
app.add_url_rule('/event/<eid>/edit',
                 view_func=EventEditView.as_view('event_edit'))
app.add_url_rule('/events/',
                 view_func=EventsView.as_view('events'))

# League View Rules
app.add_url_rule('/league/<lid>',
                 view_func=LeagueView.as_view('league'))
app.add_url_rule('/league/create',
                 view_func=LeagueCreateView.as_view('league_create'))
app.add_url_rule('/league/<lid>/edit',
                 view_func=LeagueEditView.as_view('league_edit'))
app.add_url_rule('/leagues/',
                 view_func=LeaguesView.as_view('leagues'))
app.add_url_rule('/league/<lid>/join',
                 view_func=LeagueJoinView.as_view('league_join'))


# Participant View Rules
app.add_url_rule('/participant/<pid>',
                 view_func=ParticipantView.as_view('participant'))


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
