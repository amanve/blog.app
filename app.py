from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, \
     current_user, login_required, roles_required, roles_accepted
from flask_security.forms import RegisterForm, LoginForm
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, TelField
from wtforms.validators import InputRequired
from datetime import datetime
from sqlalchemy import desc, MetaData
from sqlalchemy.ext.hybrid import hybrid_property
import pandas as pd

# Create App/Configurations
app = Flask(__name__)
# Database Configs
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/amve_blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['POSTS_PER_PAGE'] = 10
app.config['COMMENTS_PER_PAGE'] = 5

# Flask Config
app.config['SECRET_KEY'] = 'mysecret!'

# Flask Security Configs
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'somesaltforapp!'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = ('username', 'email')

#Custom DB Naming Convention
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Database connection/migrations
db = SQLAlchemy(app)
metadata = MetaData(naming_convention=convention)
migrate = Migrate(app, db, metadata=metadata)

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
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(300))
    username = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(1000))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role',
                            secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    posts = db.relationship('Post', backref='users', lazy='dynamic')
    comments = db.relationship('Comments', backref='users', lazy='dynamic')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(50), unique=True, nullable=False)
    subHeading = db.Column(db.String(100))
    body = db.Column(db.Text(), nullable=False)
    dateCreated = db.Column(db.DateTime(), default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    comments = db.relationship('Comments', backref='post', lazy='dynamic')


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.Column(db.Text(1000))
    dateCreated = db.Column(db.DateTime())


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
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(desc(Post.dateCreated)).paginate(
        page, app.config['POSTS_PER_PAGE'], True)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html',
                           posts=posts,
                           next_url=next_url,
                           prev_url=prev_url)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    form = NewComment()
    post = Post.query.get(int(post_id))
    comments_page = request.args.get('comments_page', 1, type=int)

    if form.validate_on_submit():
        comment = Comments(user_id=current_user.id,
                           comment=form.comment.data,
                           dateCreated=datetime.now())
        post.comments.append(comment)
        db.session.commit()

        return redirect(url_for('post', post_id=post.id))

    comments = Comments.query.filter_by(post_id=post_id).order_by(
        desc(Comments.dateCreated)).paginate(comments_page,
                                             app.config['COMMENTS_PER_PAGE'],
                                             True)
    # comments = Comments.query.filter_by(post_id=post_id).all()

    next_url = url_for('post', comments_page=comments.next_num, post_id=post.id) \
    if comments.has_next else None
    prev_url = url_for('post', comments_page=comments.prev_num, post_id=post.id) \
    if comments.has_prev else None

    return render_template('post.html',
                           post=post,
                           form=form,
                           comments=comments,
                           next_url=next_url,
                           prev_url=prev_url)


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = NewPost()
    if form.validate_on_submit():
        new_post = Post(heading=form.heading.data,
                        subHeading=form.subHeading.data,
                        body=form.body.data,
                        dateCreated=datetime.now(),
                        user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_post.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactUs()

    if form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        telephone = request.form['telephone']
        message = request.form['message']
        res = pd.DataFrame({
            'name': [name],
            'email': [email],
            'telephone': [telephone],
            'message': [message],
            'datetime': [datetime.strftime(datetime.now(), '''%d/%m/%y''')]
        })
        res.to_csv('./contactusMessage.csv', mode='a', index=False)
        # Todo
        """ Delete data as per datetime - need to figure out """

        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)


#Execute App
if __name__ == '__main__':
    app.run()
