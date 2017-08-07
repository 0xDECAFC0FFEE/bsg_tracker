"""some characters missing

Revision ID: acdf7e5e52f4
Revises: fba99cec7788
Create Date: 2017-08-04 22:51:50.870969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acdf7e5e52f4'
down_revision = 'fba99cec7788'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('player', 'character')
    op.add_column('player', sa.Column('character', sa.Enum("adama", "s tigh", "boomer", "apollo", "starbuck", "chief", "zarek", "baltar", "roslin",     # original
    "cain", "helo", "dee", "kat", "e tigh", "condy", "six", "doral", "biers", "cavil", # pegasus
    "gaeta", "anders", "cally", "foster",   # exodus
    "hoshi", "hot dog", "doc", "helo a", "apollo a", "zarek a", "baltar a", "lampkin", "o'neil", "athena", name='characters'), nullable=True))
    
def downgrade():
    op.drop_column('player', 'character')
    op.add_column('player', sa.Column('character', sa.Enum('adama', 's tigh', 'boomer', 'apollo', 'starbuck', 'valerii', 'chief', 'zarek', 'baltar', 'roslin', 'cain', 'helo', 'dee', 'kat', 'e tigh', 'condy', 'six', 'doral', 'biers', 'cavilgaeta', 'anders', 'cally', 'foster', 'hoshi', 'hot dog', 'doc', 'appolo a', 'zarek a', 'baltar a', 'lampkin', "o'neil", 'athena', name='characters'), nullable=True))
    