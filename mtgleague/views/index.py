from flask import redirect, render_template, url_for
from flask_login import login_user, logout_user
from mtgleague import app
from mtgleague.forms import LoginForm, RegisterForm
from mtgleague.models.user import User
from mtgleague.util import db
from mtgleague.views.scaffold import BaseView


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

app.add_url_rule('/',
                 view_func=IndexView.as_view('index'))
app.add_url_rule('/login',
                 view_func=LoginView.as_view('login'))
app.add_url_rule('/logout',
                 view_func=LogoutView.as_view('logout'))
app.add_url_rule('/register',
                 view_func=RegisterView.as_view('register'))
