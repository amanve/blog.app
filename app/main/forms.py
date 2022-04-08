from flask_security.forms import LoginForm, RegisterForm
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TelField, TextAreaField
from wtforms.validators import InputRequired


#Custom Forms
class ExtendRegisterForm(RegisterForm):
    name = StringField('Name')
    username = StringField('Username')


class ExtendLoginForm(LoginForm):
    email = StringField('Username or Email Address', [InputRequired()])


class NewPost(FlaskForm):
    heading = StringField('Heading')
    subHeading = StringField('Sub-Heading')
    body = TextAreaField('Body')


class NewComment(FlaskForm):
    comment = TextAreaField('Comment')


class ContactUs(FlaskForm):
    name = StringField('Name', [InputRequired()])
    email = EmailField('Email', [InputRequired()])
    telephone = TelField('Telephone', [InputRequired()])
    message = StringField('Message', [InputRequired()])
