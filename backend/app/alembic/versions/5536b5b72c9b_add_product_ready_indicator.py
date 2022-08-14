"""Add Product Ready Indicator

Revision ID: 5536b5b72c9b
Revises: 58e5c7e048ac
Create Date: 2021-10-14 05:12:13.909761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5536b5b72c9b'
down_revision = '58e5c7e048ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('is_ready', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'is_ready')
    # ### end Alembic commands ###