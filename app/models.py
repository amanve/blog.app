from datetime import datetime

from flask_security import RoleMixin, UserMixin
from markdown import markdown as md
import bleach

from app import db
from slugify import slugify

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


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(50), unique=True, nullable=False)
    subHeading = db.Column(db.String(100))
    body = db.Column(db.Text(), nullable=False)
    body_html = db.Column(db.Text)
    slug_url = db.Column(db.String(25))
    dateCreated = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    comments = db.relationship('Comments', backref='post', lazy='dynamic')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
            'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p'
        ]
        target.body_html = bleach.linkify(
            bleach.clean(md(value, output_format='html'),
                         tags=allowed_tags,
                         strip=True))

    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug_url or value != oldvalue):
            target.slug_url = slugify(value, max_length=25)


db.event.listen(Post.body, 'set', Post.on_changed_body)
db.event.listen(Post.heading, 'set', Post.slugify, retval=False)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    comment = db.Column(db.Text(1000))
    comment_html = db.Column(db.Text(1000))
    dateCreated = db.Column(db.DateTime())

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
            'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p'
        ]
        target.comment_html = bleach.linkify(
            bleach.clean(md(value, output_format='html'),
                         tags=allowed_tags,
                         strip=True))


db.event.listen(Comments.comment, 'set', Comments.on_changed_body)