"""Add Order Last Submit Round

Revision ID: 306195a7f16f
Revises: 3554967bf4ab
Create Date: 2021-12-04 14:01:55.329570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '306195a7f16f'
down_revision = '3554967bf4ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('last_submit_round', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'last_submit_round')
    # ### end Alembic commands ###
