import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'myseceretkey!'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL'
    ) or 'mysql+mysqlconnector://root:password@localhost/amve_blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 5
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_SALT = 'somesaltforblog!'
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_USER_IDENTITY_ATTRIBUTES = ('username', 'email')
