"""changed all caps enum to lower case, added on update cascasde and added phases to players

Revision ID: fba99cec7788
Revises: 66c4745db6ed
Create Date: 2017-08-04 20:32:38.766535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fba99cec7788'
down_revision = '66c4745db6ed'
branch_labels = None
depends_on = None


def upgrade():
    # doing this hacky ass solution cause can't alter primary key in alembic apparently 
    op.drop_table('human', schema='bsg_info')
    op.drop_table('cylon_leader', schema='bsg_info')
    op.drop_table('cylon', schema='bsg_info')
    op.drop_table('player', schema='bsg_info')
    op.drop_table('user', schema='bsg_info')
    op.drop_table('game', schema='bsg_info')

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
        sa.Column('phase', sa.INTEGER(), nullable=False),
        sa.Column('character', sa.Enum('adama', 's tigh', 'boomer', 'apollo', 'starbuck', 'valerii', 'chief', 'zarek', 'baltar', 'roslin', 'cain', 'helo', 'dee', 'kat', 'e tigh', 'condy', 'six', 'doral', 'biers', 'cavil', 'gaeta', 'anders', 'cally', 'foster', 'hoshi', 'hot dog', 'doc', 'apollo a', 'zarek a', 'baltar a', 'lampkin', 'o\'neil', 'athena', name='characters'), nullable=True),
        sa.ForeignKeyConstraint(['game_id'], [u'bsg_info.game.game_id'], name='player.game_id game.game_id fk', ondelete='CASCADE', onupdate='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], [u'bsg_info.user.user_id'], name='player.user_id user.user_id fk', onupdate='CASCADE'),
        sa.PrimaryKeyConstraint('game_id', 'user_id', 'phase'),
        schema='bsg_info'
    )
    op.create_table('cylon',
        sa.Column('game_id', sa.INTEGER(), nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.Column('phase', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['game_id', 'user_id', 'phase'], [u'bsg_info.player.game_id', 'bsg_info.player.user_id', 'bsg_info.player.phase'], name='cylon player fk', ondelete='CASCADE', onupdate='CASCADE'),
        sa.PrimaryKeyConstraint('game_id', 'user_id', 'phase'),
        schema='bsg_info'
    )
    op.create_table('cylon_leader',
        sa.Column('game_id', sa.INTEGER(), nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.Column('phase', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['game_id', 'user_id', 'phase'], [u'bsg_info.player.game_id', 'bsg_info.player.user_id', 'bsg_info.player.phase'], name='cylon_leader player fk', ondelete='CASCADE', onupdate='CASCADE'),
        sa.PrimaryKeyConstraint('game_id', 'user_id', 'phase'),
        schema='bsg_info'
    )
    op.create_table('human',
        sa.Column('game_id', sa.INTEGER(), nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.Column('phase', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['game_id', 'user_id', 'phase'], [u'bsg_info.player.game_id', 'bsg_info.player.user_id', 'bsg_info.player.phase'], name='human player fk', ondelete='CASCADE', onupdate='CASCADE'),
        sa.PrimaryKeyConstraint('game_id', 'user_id', 'phase'),
        schema='bsg_info'
    )
    

def downgrade():
    op.drop_table('human', schema='bsg_info')
    op.drop_table('cylon_leader', schema='bsg_info')
    op.drop_table('cylon', schema='bsg_info')
    op.drop_table('player', schema='bsg_info')
    op.drop_table('user', schema='bsg_info')
    op.drop_table('game', schema='bsg_info')

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
        sa.Column('character', sa.Enum('ADAMA', 'S TIGH', 'BOOMER', 'APOLLO', 'STARBUCK', 'VALERII', 'CHIEF', 'ZAREK', 'BALTAR', 'ROSLIN', 'CAIN', 'HELO', 'DEE', 'KAT', 'E TIGH', 'GAETA', 'ANDERS', 'CALLY', 'FOSTER', 'HOSHI', 'HOT DOG', 'DOC', 'APPOLO A', 'ZAREK A', 'BALTAR A', 'LAMPKIN', name='characters'), nullable=True),
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