"""Add Model Stake Info

Revision ID: 73cce7709e29
Revises: fb1871e8ba31
Create Date: 2022-04-07 14:13:57.812946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73cce7709e29'
down_revision = 'fb1871e8ba31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('model', sa.Column('stake_info', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('model', 'stake_info')
    # ### end Alembic commands ###
