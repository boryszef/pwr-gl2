from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField

class LoginForm(FlaskForm):
    username = StringField('Username')#, validators=[DataRequired()]) #I dont use it to make message "Wrong password or username" visible
    password = PasswordField('Password')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
