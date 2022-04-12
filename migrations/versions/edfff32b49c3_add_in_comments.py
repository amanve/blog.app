"""add in comments

Revision ID: edfff32b49c3
Revises: 2c7b17f5fa1b
Create Date: 2022-04-12 13:31:58.780003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edfff32b49c3'
down_revision = '2c7b17f5fa1b'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('name', sa.String(length=128), nullable=False))
    op.add_column('comments', sa.Column('email', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'email')
    op.drop_column('comments', 'name')
    # ### end Alembic commands ###

