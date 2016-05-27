from flask.ext.wtf import Form
from wtforms import BooleanField, IntegerField, TextField, TextAreaField, PasswordField, validators, HiddenField, DateField, SelectField, StringField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Optional

class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class EditForm(Form):
    usernme = StringField('username', validators=[DataRequired()])
    password = TextAreaField('password', validators=[Length(min=0, max=140)])


class RegisterForm(Form):
    username = StringField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
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


class CreateC(Form):
    firstname = TextField(
        'First Name',
        validators=[Length(min=3, max=25)]
    )
    lastname = TextField(
        'Last Name',
        validators=[Length(min=3, max=25)]
    )
    img = TextField(
        'Image Url', validators = [Optional(), Length(max = 100)], filters = [lambda x: x or None]
    )