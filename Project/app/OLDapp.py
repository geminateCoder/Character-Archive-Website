import os
import sys
from functools import wraps
from flask import g, Flask, Response, abort, current_app, render_template, url_for, flash, request, redirect, session
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask.ext.security import Security, RoleMixin
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask.ext.bcrypt import Bcrypt
from flask_wtf import Form
from wtforms import BooleanField, IntegerField, TextField, TextAreaField, PasswordField, validators, HiddenField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Optional
from flask import jsonify
from datetime import datetime
from urllib.request import urlopen, quote, unquote
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:###@localhost/db'
app.config['SECRET_KEY'] = 'super-secret'
app.debug = True
db = SQLAlchemy(app)
mail = Mail(app)

#app.secret_key = "my precious"
# flask-login
login_manager = LoginManager()
login_manager.init_app(app)

#Flask Security
app.config['SECURITY_TRACKABLE'] = True


# Define models
favorite = db.Table('favorite',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'))
)

follow = db.Table('follow',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('following_id', db.Integer, db.ForeignKey('user.id'))
)







class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    settings = db.relationship('UserSettings', backref='user', lazy='dynamic')
    following = db.relationship('User',
        secondary = follow,
        primaryjoin = (follow.c.follower_id == id),
        secondaryjoin = (follow.c.following_id == id),
        backref = db.backref('follow'),
    lazy='dynamic')
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer)



class UserSettings(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), db.ForeignKey('user.username'))
    displayname = db.Column(db.String(255))
    age = db.Column(db.Integer, primary_key=False)
    gender = db.Column(db.String(255))
    sign = db.Column(db.String(255))
    timezone = db.Column(db.String(255))
    cpoints = db.Column(db.Integer(), primary_key=False) #coolpts
    status = db.Column(db.String(255))
    pref = db.Column(db.String(255))
    exp = db.Column(db.String(255))
    style = db.Column(db.String(255))
    contact = db.Column(db.String(255))
    about = db.Column(db.Text(length=None))
    img = db.Column(db.String(255),default="/static/img/default_image.png")

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    firstname = db.Column(db.String(255),default="")
    lastname = db.Column(db.String(255),default="")
    nickname = db.Column(db.String(255))
    age = db.Column(db.Integer, primary_key=False)
    gender = db.Column(db.String(255))
    birthday = db.Column(db.Date)
    sign = db.Column(db.String(255))
    sexual = db.Column(db.String(255))
    occup = db.Column(db.String(255))
    residence = db.Column(db.String(255))
    height = db.Column(db.String(255))
    weight = db.Column(db.String(255))
    hair = db.Column(db.String(255))
    eyes = db.Column(db.String(255))
    status = db.Column(db.String(255))
    likes = db.Column(db.String(255))
    dislikes = db.Column(db.String(255))
    person = db.Column(db.Text(length=None))
    appear = db.Column(db.Text(length=None))
    about = db.Column(db.Text(length=None))
    original = db.Column(db.Boolean, unique=False, default=1)
    fandom = db.Column(db.String(255))
    theme = db.Column(db.String(255))
    url = db.Column(db.String(255))
    img = db.Column(db.String(255),default="/static/img/default_image.png")
    favorited = db.relationship('User', secondary=favorite,
        backref=db.backref('favorite'))
    created = db.Column(db.DateTime())




@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

class RegisterForm(Form):
    username = TextField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')
        ]
    )
class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class Settings(Form):
    displayname = TextField(
        'Displayname',
        validators=[Length(min=3, max=25)]
    )
    current_password = PasswordField(
        'Current Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    new_password = PasswordField(
        'New Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm_new = PasswordField(
        'Repeat New password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')
        ]
    )

class CreateC(Form):
    firstname = TextField(
        'First Name',
        validators=[Length(min=3, max=25)]
    )
    lastname = TextField(
        'Last Name',
        validators=[Length(min=3, max=25)]
    )
    age = IntegerField(
        'Age',
        validators=[Length(min=1, max=3)]
    )
    gender = TextField(
        'Gender',
        validators=[Length(min=3, max=25)]
    )
    sign = SelectField(choices=[('aries', '♈'), ('taurus', '♉'), ('gemini', '♊'), ('cancer', '♋'),
                                ('leo', '♌'), ('virgo', '♍'), ('libra', '♎'), ('scorpio', '♏'),
                                ('sagittarius', '♐'), ('capricorn', '♑'), ('aquarius', '♒'), ('pisces', '♓')]
                      )
    about = TextAreaField(
        'About',
        validators=[Length(min=3, max=25)]
    )
    img = TextField(
        'Image Url', validators = [Optional(), Length(max = 100)], filters = [lambda x: x or None]
    )

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)

@app.route("/")
def index():
    pageType='index'
    allChara = Character.query.order_by(Character.id.desc()).limit(16).all()
    if current_user.is_authenticated:
        return redirect(url_for('dash'))
    else:
        return render_template("index.html", page=pageType, allChara=allChara)


@app.route("/login", methods=['GET','POST'])
def login():
    pageType='login'
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=request.form['username']).first()
            if user is not None and user.password == request.form['password']:
                user.login_count = user.login_count +1
                user.current_login_at = datetime.now()
                user.current_login_ip = request.remote_addr
                db.session.commit()
                login_user(user)
                return redirect(url_for('dash'))

            else:
                error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error, page=pageType)

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
        return redirect(url_for('dash'))
    return render_template('register.html', form=form, page=pageType)

@app.route('/logout')
def logout():
    user = current_user
    user.last_login_at = datetime.now()
    user.last_login_ip = request.remote_addr
    db.session.commit()
    session.pop('logged_in', None)
    logout_user()
    return redirect(url_for('index'))

@app.route("/dashboard")
@login_required
def dash():
    pageType='dash'
    user=current_user.username
    data = current_user
    #Chara = Character.query.all()
    cCount = 0
    allChara = Character.query.order_by(Character.id.desc()).limit(10).all()
    Chara = Character.query.filter_by(username=user).order_by(Character.id.desc()).all()
    userInfo = UserSettings.query.filter_by(username=user).first()
    for num in Chara:
        cCount = cCount+1

    return render_template("dashboard.html", page=pageType, Chara=Chara, userInfo=userInfo, allChara=allChara, cCount=cCount)


@app.route("/settings")
@login_required
def settings():
    pageType='settings'

    return render_template("user_settings.html")

@app.route("/character_create", methods=['GET','POST'])
@login_required
def createChara():
    pageType='createC'
    form = CreateC()
    character ='None'
    if form.validate_on_submit():
        character = Character(
            username=current_user.username,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            age=form.age.data,
            gender=form.gender.data,
            sign=form.sign.data,
            about=form.about.data,
            appear=form.firstname.data,
            person=form.lastname.data,
            likes=form.age.data,
            dislikes=form.gender.data,
            img=form.img.data,
            url=form.url.data,
            created=datetime.now()
        )
        db.session.add(character)
        db.session.commit()
        return redirect(url_for('createChara'))
    return render_template("Character_Create.html", page=pageType, form=form, character=character)


@app.route("/character/profile/<cid>")
def chara(cid):
    pageType='character_profile'
    character = Character.query.filter_by(id=cid).first()
    user = UserSettings.query.filter_by(username=character.username).first()
    return render_template("Character_Profile.html", user=user,page=pageType, character=character, cid=cid)

@app.route("/profile/<username>", methods=['GET','POST'])
def profile(username):
    pageType='profile'
    user = current_user
    y = "none"
    x = User.query.join(follow, (follow.c.following_id == User.id)).filter(follow.c.follower_id == user.id).all()
    for num in x:
        if username in num.username:
            if user.username == username:
                y = "Ughwork"
            else:
                y = 'Already added'
        else:
            y = " Add them"

    chara = Character.query.filter_by(username=username).order_by(Character.id.desc()).all()
    username = UserSettings.query.filter_by(username=username).first()
    return render_template("profile.html", y=y, page=pageType, user=username, characters=chara)

@app.route("/test/<user_id>")
def test(user_id):
    user = current_user
    #y = "none"
    #y= User.query.join(follow, (follow.c.follower_id == User.id)).filter(follow.c.following_id == user_id).all()
    #x = User.query.join(follow, (follow.c.following_id == User.id)).filter(follow.c.follower_id == user.id).all()
    #for num in x:
     #   if user_id in num.username:
     #       y = "yes here is a user"
    #user1 =  User.query.filter_by(id=1).first()
    #follower = x
    character = Character.query.filter_by(username=user).first()
    msg = Message("Hello",
                  body='test',
                  sender=user.username,
                  recipients=["user2"])
    return render_template("test.html",msg=msg)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")

def is_following(self, user):
    return self.follow.filter(follow.c.following_id == user.id).count() > 0


@app.route('/follow/<user_id>' )
def follows(user_id):
    user=current_user
    x = User.query.join(follow, (follow.c.following_id == User.id)).filter(follow.c.follower_id == user.id).all()
    user_id = User.query.filter_by(username=user_id).first()
    for num in x:
        if user_id.username in num.username:
            return redirect(url_for('profile', username=user_id.username))
    if user_id is None:
        return redirect(url_for('profile', username=user_id.username))
    if user_id == user:
        return redirect(url_for('profile', username=user_id.username))

    user_id.follow.append(user)
    db.session.commit()
    return redirect(url_for('profile', username=user_id.username))

@app.route('/unfollow/<user_id>')
@login_required
def unfollows(user_id):
    user=current_user
    user_id = User.query.filter_by(username=user_id).first()
    if user_id is None:
        return redirect(url_for('profile', username=user_id.username))
    if user_id == user:
        return redirect(url_for('profile', username=user_id.username))
    user_id.follow.remove(user)
    db.session.commit()
    return redirect(url_for('profile', username=user_id.username))

@app.route("/unfavorite/<character>")
def unfav(character):
    pageType='fav'
    user = current_user
    character = Character.query.filter_by(id=character).first()
    character.favorited.remove(user)
    db.session.commit()
    return render_template("test.html", page=pageType)

@app.route("/favorite/<character>")
def fav(character):
    pageType='fav'
    user = current_user
    character = Character.query.filter_by(id=character).first()
    character.favorited.append(user)
    db.session.commit()
    return render_template("test.html", page=pageType)


@app.route("/upload")
def upload():
    pageType='upload'
    return render_template("upload.html", page=pageType)

def confirmation_required(desc_fn):
    def inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.args.get('confirm') != '1':
                desc = desc_fn()
                return redirect(url_for('confirm',
                    desc=desc, action_url=quote(request.url)))
            return f(*args, **kwargs)
        return wrapper
    return inner

@app.route('/confirm')
def confirm():
    desc = request.args['desc']
    action_url = unquote(request.args['action_url'])

    return render_template('_confirm.html', desc=desc, action_url=action_url)

def you_sure():
    return "Are you sure you want to delete your character?"

@app.route("/delete/<chara_id>", methods=['GET','POST'])
@confirmation_required(you_sure)
def deleteU(chara_id):
    Character.query.filter(Character.id == chara_id).delete()
    db.session.commit()
    return redirect(url_for('dash'))

@app.route("/createnull", methods=['GET','POST'])
def createNull():
    character = Character(
        username="user",
        firstname="FirstName",
        lastname="LastName",
        nickname="Steave",
        birthday="11/11/2112",
        sexual="gay",
        occup="Vampire Hhunter",
        residence="Idk your basement",
        status="Coding",
        age=18,
        gender="Male",
        sign="gemini",
        height="4'5''",
        weight="324lb",
        hair="Long",
        eyes="Red",
        about="This is about the character.",
        appear="This guy looks awesome.",
        person="This guy is a Hero.",
        likes="Cheese",
        dislikes="Ants",
        img="/static/img/default_image.png",
        url="testchari",
        created=datetime.now()
    )
    db.session.add(character)
    db.session.commit()
    return render_template('index.html')


if __name__ == "__main__":


    # Create DB
    db.create_all()

    # Start app
    app.run()