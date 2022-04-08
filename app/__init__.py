from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import config
from sqlalchemy import MetaData
from flask_migrate import Migrate

#Custom DB Naming Convention
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Database connection/migrations
db = SQLAlchemy()
metadata = MetaData(naming_convention=convention)
migrate = Migrate(app, db, metadata=metadata)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app