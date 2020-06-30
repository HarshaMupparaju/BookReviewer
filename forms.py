from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField 

class SignUpForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login') 

class BookSearch(FlaskForm):
    value = StringField('Details of the book')
