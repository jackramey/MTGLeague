from flask import redirect, render_template, url_for
from flask_login import login_user, logout_user
from mtgleague import app
from mtgleague.forms.login import LoginForm
from mtgleague.forms.register import RegisterForm
from mtgleague.models.user import User
from mtgleague.views.scaffold import BaseView


class IndexView(BaseView):
    methods = ['GET']

    def handle_request(self):
        return render_template('index.html', **self.context)


class LoginView(BaseView):
    methods = ['GET', 'POST']

    def handle_request(self, *args, **kwargs):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None:
                error = "That user does not exist."
                return render_template('login.html', error=error)
            else:
                if user.check_password(form.password.data):
                    login_user(user, remember=True)
                    return redirect(url_for('index'))
                else:
                    error = "Username and Password combination are incorrect."
                    return render_template('login.html', error=error, **self.context)
        else:
            return render_template('login.html', form=form, **self.context)


class LogoutView(BaseView):
    methods = ['GET']

    def handle_request(self, *args, **kwargs):
        logout_user()
        return redirect(url_for('index'))


class RegisterView(BaseView):
    methods = ['GET', 'POST']

    def handle_request(self, *args, **kwargs):
        form = RegisterForm()
        if form.validate_on_submit():
                return redirect(url_for('index'))
        else:
            return render_template('register.html', form=form, **self.context)

app.add_url_rule('/',
                 view_func=IndexView.as_view('index'))
app.add_url_rule('/login',
                 view_func=LoginView.as_view('login'))
app.add_url_rule('/logout',
                 view_func=LogoutView.as_view('logout'))
app.add_url_rule('/register',
                 view_func=RegisterView.as_view('register'))
