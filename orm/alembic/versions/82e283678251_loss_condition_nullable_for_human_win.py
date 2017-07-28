"""loss_condition nullable for human win

Revision ID: 82e283678251
Revises: b90abc28439d
Create Date: 2017-07-28 05:14:51.760363

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '82e283678251'
down_revision = 'b90abc28439d'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('game', 'loss_condition',
               existing_type=mysql.SMALLINT(display_width=6),
               nullable=True)


def downgrade():
    op.alter_column('game', 'loss_condition',
               existing_type=mysql.SMALLINT(display_width=6),
               nullable=False)
