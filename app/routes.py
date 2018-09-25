from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, \
logout_user, login_required
from flask import request
from werkzeug.urls import url_parse
from app.models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
	# user = {'username': 'Miguel'}
	posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

	return render_template("index.html", title="Big World", posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # user already logined
        return redirect(url_for('index'))

    # User not yet login
    form = LoginForm()
    if form.validate_on_submit():
        # Login form submitted
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Wrong Username or password. Please try again!")
            return redirect(url_for('login'))
        # username and password hash match record in database, login user
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc!='':
            next_page = url_for('index')
        return redirect(next_page)

    # render login page if form is not submitted
    return render_template("login.html", title="Sign In", 
                           form=form)
	

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # no validation errors on submit
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
