"""empty message

Revision ID: 9e78e61323ed
Revises: b3a1777fbfac
Create Date: 2022-04-13 18:54:03.956255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e78e61323ed'
down_revision = 'b3a1777fbfac'
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

