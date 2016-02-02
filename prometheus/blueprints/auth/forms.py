from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo


class LoginForm(Form):
    email = StringField('Email*', [Required(), Email()])
    password = PasswordField('Password*',[Required(), Length(3, 36)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class ChangePassword(Form):
    password = PasswordField('New Password', [Required(), EqualTo('confirm',
                                              message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    submit = SubmitField('Change')
