"""added support for deleting rows

Revision ID: 798bb8352cbf
Revises: e615221a721d
Create Date: 2017-07-20 20:12:25.586924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '798bb8352cbf'
down_revision = 'e615221a721d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('isDeleted', sa.BOOLEAN(), nullable=False))
    op.add_column('user', sa.Column('isDeleted', sa.BOOLEAN(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'isDeleted')
    op.drop_column('game', 'isDeleted')
    # ### end Alembic commands ###