from flask import Flask
from flask_migrate import Migrate
from flask_security import (Security, SQLAlchemyUserDatastore)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from config import Config

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors

# Setup Flask Security
""" user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app,
                    user_datastore,
                    register_form=ExtendRegisterForm,
                    login_form=ExtendLoginForm) """

from app import models