from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm, EditForm, RegisterForm, CreateC
from .models import User, UserSettings, Character
from datetime import datetime

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

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
            user = User.query.filter_by(username=request.form['username'].lower()).first()
            if user is not None and user.password == request.form['password']:
                session['remember_me'] = form.remember_me.data
                user.login_count = user.login_count +1
                user.current_login_at = datetime.now()
                user.current_login_ip = request.remote_addr
                db.session.commit()
                login_user(user)
                return redirect(url_for('index'))
            else:
                error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)

@app.route('/register', methods=['GET', 'POST'])   # pragma: no cover
def register():
    pageType='register'
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            username=remove_html_tags(form.username.data).lower(),
            email=remove_html_tags(form.email.data).lower(),
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


@app.route("/create", methods=['GET','POST'])
@login_required
def create():
    return render_template("Create.html")




@app.route("/create/original", methods=['GET','POST'])
@login_required
def original():
    pageType='original'
    form = CreateC()
    character ='None'
    if form.validate_on_submit():
        character = Character(
            username=current_user.username,
            firstname=remove_html_tags(form.firstname.data),
            lastname=remove_html_tags(form.lastname.data),
            img=form.img.data,
            created=datetime.now()
        )
        db.session.add(character)
        db.session.commit()
        return redirect(url_for('create'))
    return render_template("CreateForms.html", page=pageType, form=form, character=character)

@app.route("/create/fandom", methods=['GET','POST'])
@login_required
def fandom():
    pageType='fandom'
    return render_template("CreateForms.html", page=pageType)

@app.route("/create/original_fandom", methods=['GET','POST'])
@login_required
def originalFandom():
    pageType='ofandom'
    return render_template("CreateForms.html", page=pageType)

@app.route("/create/d&d", methods=['GET','POST'])
@login_required
def DnD():
    pageType='ofandom'
    return render_template("CreateForms.html", page=pageType)