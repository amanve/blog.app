import os

from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore

from app import create_app, db
from app.main.forms import ExtendLoginForm, ExtendRegisterForm
from app.models import Role, User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app,
                    user_datastore,
                    register_form=ExtendRegisterForm,
                    login_form=ExtendLoginForm)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
