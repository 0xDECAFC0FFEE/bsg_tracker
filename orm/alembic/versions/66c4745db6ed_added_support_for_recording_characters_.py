"""added support for recording characters played by users

Revision ID: 66c4745db6ed
Revises: f50428bb961d
Create Date: 2017-08-03 05:13:03.736540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66c4745db6ed'
down_revision = 'f50428bb961d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('player', sa.Column('character', sa.Enum('ADAMA', 'S TIGH', 'BOOMER', 'APOLLO', 'STARBUCK', 'VALERII', 'CHIEF', 'ZAREK', 'BALTAR', 'ROSLIN', 'CAIN', 'HELO', 'DEE', 'KAT', 'E TIGH', 'GAETA', 'ANDERS', 'CALLY', 'FOSTER', 'HOSHI', 'HOT DOG', 'DOC', 'APPOLO A', 'ZAREK A', 'BALTAR A', 'LAMPKIN', name='characters'), nullable=True))
    

def downgrade():
    op.drop_column('player', 'character')