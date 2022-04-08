import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'myseceretkey!'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 5
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_SALT = 'somesaltforblog!'
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_USER_IDENTITY_ATTRIBUTES = ('username', 'email')


@staticmethod
def init_app(app):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL'
    ) or 'mysql+mysqlconnector://root:password@localhost/amve_blog'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
'sqlite:///blog_test.db'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}