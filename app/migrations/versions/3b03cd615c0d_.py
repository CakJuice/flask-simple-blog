"""empty message

Revision ID: 3b03cd615c0d
Revises: bc3f734003b5
Create Date: 2017-12-19 13:33:54.924573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b03cd615c0d'
down_revision = 'bc3f734003b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entry', sa.Column('status', sa.SmallInteger(), server_default='0'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('entry', 'status')
    # ### end Alembic commands ###