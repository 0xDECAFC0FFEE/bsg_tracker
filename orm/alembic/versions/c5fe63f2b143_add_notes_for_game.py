"""add notes for game

Revision ID: c5fe63f2b143
Revises: 82e283678251
Create Date: 2017-07-29 18:33:04.827810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5fe63f2b143'
down_revision = '82e283678251'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('game', sa.Column('notes', sa.VARCHAR(length=60), nullable=True))


def downgrade():
    op.drop_column('game', 'notes')
