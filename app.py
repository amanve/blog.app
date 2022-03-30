from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_security.forms import RegisterForm, LoginForm
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired
from datetime import datetime

# Create App/Configurations
app = Flask(__name__)
# Database Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask Config
app.config['SECRET_KEY'] = 'mysecret!'

# Flask Security Configs
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'somesaltforapp!'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = ('username', 'email')

# Database connection/migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define models of used in the app
roles_users = db.Table(
    'roles_users', db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(250))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    username = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(1000))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role',
                            secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(50), unique=True, nullable=False)
    subHeading = db.Column(db.String(100))
    body = db.Column(db.Text(), nullable=False)
    dateCreated = db.Column(db.DateTime(), default=datetime.utcnow)


class ExtendRegisterForm(RegisterForm):
    name = StringField('Name')
    username = StringField('Username')


class ExtendLoginForm(LoginForm):
    email = StringField('Username or Email Address', [InputRequired()])


class NewPost(FlaskForm):
    heading = StringField('Heading')
    subHeading = StringField('Sub-Heading')
    body = TextAreaField('Body')


# Setup Flask Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app,
                    user_datastore,
                    register_form=ExtendRegisterForm,
                    login_form=ExtendLoginForm)


#Custom Templates
@app.template_filter('datetime_format')
def datetime_format(value, format='%d %B,%Y'):
    if value == None:
        return None
    return value.strftime(format)


#Register Routes
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/post')
def post():
    return render_template('post.html')


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = NewPost()
    if form.validate_on_submit():
        new_post = Post(heading=form.heading.data,
                        subHeading=form.subHeading.data,
                        body=form.body.data,
                        dateCreated=datetime.now())
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('post'))

    return render_template('add_post.html', form=form)


#Execcute App
if __name__ == '__main__':
    app.run()
