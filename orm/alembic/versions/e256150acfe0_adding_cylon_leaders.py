"""adding cylon leaders

Revision ID: e256150acfe0
Revises: 9f450115435d
Create Date: 2017-07-31 18:45:32.004293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e256150acfe0'
down_revision = '9f450115435d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('cylon_leader',
    sa.Column('game_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], [u'bsg_info.game.game_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], [u'bsg_info.user.user_id'], ),
    sa.PrimaryKeyConstraint('game_id', 'user_id'),
    schema='bsg_info'
    )


def downgrade():
    op.drop_table('cylon_leader', schema='bsg_info')
