from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_security.forms import RegisterForm, LoginForm
from wtforms import StringField
from wtforms.validators import InputRequired

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
    body = db.Column(db.String(), nullable=False)


class ExtendRegisterForm(RegisterForm):
    name = StringField('Name')
    username = StringField('Username')


class ExtendLoginForm(LoginForm):
    email = StringField('Username or Email Address', [InputRequired()])


# Setup Flask Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app,
                    user_datastore,
                    register_form=ExtendRegisterForm,
                    login_form=ExtendLoginForm)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/post')
def post():
    return render_template('post.html')


if __name__ == '__main__':
    app.run()
