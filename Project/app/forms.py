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