from flask_security.forms import LoginForm, RegisterForm
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TelField, TextAreaField
from wtforms.validators import InputRequired, ValidationError
from ..models import Post


#Custom Forms
class ExtendRegisterForm(RegisterForm):
    name = StringField('Name')
    username = StringField('Username')


class ExtendLoginForm(LoginForm):
    email = StringField('Username or Email Address', [InputRequired()])


class NewPost(FlaskForm):
    heading = StringField('Heading', [InputRequired()])
    subHeading = StringField('Sub-Heading')
    body = TextAreaField('Body', [InputRequired()])

    def validate_heading(self, heading):
        heading_obj = Post.query.filter(Post.heading == heading.data).first()
        if heading_obj is not None:
            raise ValidationError(
                'Post already exists. Please re-write the post.!')


class NewComment(FlaskForm):
    name = StringField('Name', [InputRequired()])
    email = StringField('Email', [InputRequired()])
    comment = TextAreaField('Comment', [InputRequired()])


class ContactUs(FlaskForm):
    name = StringField('Name', [InputRequired()])
    email = EmailField('Email', [InputRequired()])
    telephone = TelField('Telephone', [InputRequired()])
    message = StringField('Message', [InputRequired()])
