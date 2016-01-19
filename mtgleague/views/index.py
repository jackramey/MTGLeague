from flask import redirect, render_template, request, url_for
from mtgleague import app
from mtgleague.forms.login import LoginForm
from mtgleague.forms.register import RegisterForm
from mtgleague.views.scaffold import BaseView


class IndexView(BaseView):
    methods = ['GET']

    def handle_request(self):
        return render_template('index.html', **self.context)


class LoginView(BaseView):
    methods = ['GET', 'POST']

    def handle_request(self, *args, **kwargs):
        form = LoginForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                return redirect(url_for('index'))
        else:
            return render_template('login.html', form=form, **self.context)


class RegisterView(BaseView):
    methods = ['GET', 'POST']

    def handle_request(self, *args, **kwargs):
        form = RegisterForm()
        if form.is_submitted():
            print('form submitted')
        if form.validate():
            print('form validated')
        else:
            print('form not valid')
        if form.validate_on_submit():
                return redirect(url_for('index'))
        else:
            return render_template('register.html', form=form, **self.context)

app.add_url_rule('/',
                 view_func=IndexView.as_view('index'))
app.add_url_rule('/login',
                 view_func=LoginView.as_view('login'))
app.add_url_rule('/register',
                 view_func=RegisterView.as_view('register'))
