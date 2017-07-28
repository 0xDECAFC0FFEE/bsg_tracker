"""added game expansion information

Revision ID: b90abc28439d
Revises: cf0da8b2f4b3
Create Date: 2017-07-26 20:09:51.053117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b90abc28439d'
down_revision = 'cf0da8b2f4b3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('game', sa.Column('used_daybreak', sa.BOOLEAN(), nullable=True))
    op.add_column('game', sa.Column('used_exodus', sa.BOOLEAN(), nullable=True))
    op.add_column('game', sa.Column('used_pegasus', sa.BOOLEAN(), nullable=True))


def downgrade():
    op.drop_column('game', 'used_pegasus')
    op.drop_column('game', 'used_exodus')
    op.drop_column('game', 'used_daybreak')
