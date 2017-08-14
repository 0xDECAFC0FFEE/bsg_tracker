"""removed raptors and vipers from game stats

Revision ID: c227766b5342
Revises: de555bce13b0
Create Date: 2017-08-14 16:53:51.692381

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c227766b5342'
down_revision = 'de555bce13b0'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('game', 'raptors_left')
    op.drop_column('game', 'vipers_left')
    

def downgrade():
    op.add_column('game', sa.Column('vipers_left', mysql.SMALLINT(display_width=6), autoincrement=False, nullable=True))
    op.add_column('game', sa.Column('raptors_left', mysql.SMALLINT(display_width=6), autoincrement=False, nullable=True))
    