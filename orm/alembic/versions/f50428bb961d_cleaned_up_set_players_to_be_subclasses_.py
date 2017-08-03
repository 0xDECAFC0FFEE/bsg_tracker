"""cleaned up, set players to be subclasses and named constraints

Revision ID: f50428bb961d
Revises: 
Create Date: 2017-08-03 04:49:18.760035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f50428bb961d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('game',
        sa.Column('game_id', sa.INTEGER(), nullable=False),
        sa.Column('date', sa.TIMESTAMP(), nullable=False),
        sa.Column('loss_condition', sa.Enum('won', 'galactica', 'fuel', 'food', 'morale', 'population', 'heavy_raider', name='loss_conditions'), nullable=False),
        sa.Column('raptors_left', sa.SMALLINT(), nullable=True),
        sa.Column('vipers_left', sa.SMALLINT(), nullable=True),
        sa.Column('fuel_left', sa.SMALLINT(), nullable=True),
        sa.Column('food_left', sa.SMALLINT(), nullable=True),
        sa.Column('morale_left', sa.SMALLINT(), nullable=True),
        sa.Column('population_left', sa.SMALLINT(), nullable=True),
        sa.Column('distance_left', sa.SMALLINT(), nullable=True),
        sa.Column('used_pegasus', sa.BOOLEAN(), nullable=True),
        sa.Column('used_daybreak', sa.BOOLEAN(), nullable=True),
        sa.Column('used_exodus', sa.BOOLEAN(), nullable=True),
        sa.Column('notes', sa.VARCHAR(length=60), nullable=True),
        sa.PrimaryKeyConstraint('game_id'),
        schema='bsg_info',
        mysql_charset='utf8',
        mysql_engine='InnoDB'
    )
    op.create_table('user',
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.Column('name', sa.VARCHAR(length=30), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('name'),
        schema='bsg_info',
        mysql_charset='utf8',
        mysql_engine='InnoDB'
    )
    op.create_table('player',
        sa.Column('game_id', sa.INTEGER(), nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['game_id'], [u'bsg_info.game.game_id'], name='player.game_id game.game_id fk', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], [u'bsg_info.user.user_id'], name='player.user_id user.user_id fk'),
        sa.PrimaryKeyConstraint('game_id', 'user_id'),
        schema='bsg_info'
    )
    op.create_table('cylon',
        sa.Column('game_id', sa.INTEGER(), nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['game_id'], [u'bsg_info.player.game_id'], name='cylon.game_id player.game_id fk', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], [u'bsg_info.player.user_id'], name='cylon.user_id player.user_id fk', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('game_id', 'user_id'),
        schema='bsg_info'
    )
    op.create_table('cylon_leader',
        sa.Column('game_id', sa.INTEGER(), nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['game_id'], [u'bsg_info.player.game_id'], name='cylon_leader.game_id player.game_id fk', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], [u'bsg_info.player.user_id'], name='cylon_leader.user_id player.user_id fk', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('game_id', 'user_id'),
        schema='bsg_info'
    )
    op.create_table('human',
        sa.Column('game_id', sa.INTEGER(), nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['game_id'], [u'bsg_info.player.game_id'], name='human.game_id player.game_id fk', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], [u'bsg_info.player.user_id'], name='human.user_id player.user_id fk', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('game_id', 'user_id'),
        schema='bsg_info'
    )


def downgrade():
    op.drop_table('human', schema='bsg_info')
    op.drop_table('cylon_leader', schema='bsg_info')
    op.drop_table('cylon', schema='bsg_info')
    op.drop_table('player', schema='bsg_info')
    op.drop_table('user', schema='bsg_info')
    op.drop_table('game', schema='bsg_info')
