"""slug url in post

Revision ID: 5d15a977a5e5
Revises: b3a1777fbfac
Create Date: 2022-04-13 19:04:09.979945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d15a977a5e5'
down_revision = 'b3a1777fbfac'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('slug_url', sa.String(length=25), nullable=True))
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'slug_url')
    # ### end Alembic commands ###

