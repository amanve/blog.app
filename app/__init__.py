import logging
import os
from logging.handlers import RotatingFileHandler

from config import Config
from flask import Flask
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, desc

# Create App/Configurations
app = Flask(__name__)

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

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log',
                                           maxBytes=1024,
                                           backupCount=10)
        file_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog Startup')

from app import errors, models, routes
