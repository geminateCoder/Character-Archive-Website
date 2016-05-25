from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm,EditForm, RegisterForm
from .models import User, UserSettings
from datetime import datetime

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_login_at = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login", methods=['GET','POST'])
@oid.loginhandler
def login():
    error=None
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=request.form['username']).first()
            if user is not None and user.password == request.form['password']:
                session['remember_me'] = form.remember_me.data
                db.session.commit()
                login_user(user)
                return redirect(url_for('index'))
            else:
                error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)

@app.route('/register', methods=['GET', 'POST'])   # pragma: no cover
def register():
    pageType='register'
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data

        )
        db.session.add(user)
        user.follow.append(user)
        user.settings.append(UserSettings(displayname=form.username.data))
        user.login_count = 1
        user.current_login_at = datetime.now()
        user.current_login_ip = request.remote_addr
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form, page=pageType)

@app.route('/logout')
def logout():
    user = current_user
    user.last_login_at = datetime.now()
    user.last_login_ip = request.remote_addr
    db.session.commit()
    logout_user()
    return redirect(url_for('index'))

@app.route("/profile/<username>", methods=['GET','POST'])
@login_required
def profile(username):
    pageType='profile'
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    return render_template('user.html',
                           user=user)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)

