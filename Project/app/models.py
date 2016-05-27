from app import db
from flask.ext.login import UserMixin
from hashlib import md5


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
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return self.username


class UserSettings(db.Model):
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
    headcanon = db.Column(db.Text(length=None))
    fandom = db.Column(db.String(255))
    theme = db.Column(db.String(255))
    url = db.Column(db.String(255))
    img = db.Column(db.String(255),default="/static/img/default_image.png")
    favorited = db.relationship('User', secondary=favorite,
        backref=db.backref('favorite'))
    created = db.Column(db.DateTime())




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return self.body
