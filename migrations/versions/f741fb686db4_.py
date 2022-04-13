"""empty message

Revision ID: f741fb686db4
Revises: 9e78e61323ed
Create Date: 2022-04-13 18:54:53.380496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f741fb686db4'
down_revision = '9e78e61323ed'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    pass


def downgrade_():
    pass

