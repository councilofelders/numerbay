"""Add filtered total sales stats to product

Revision ID: cef21686bfb5
Revises: 43cecbe71690
Create Date: 2023-03-24 14:54:10.133018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cef21686bfb5'
down_revision = '43cecbe71690'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('total_qty_sales_filtered', sa.Integer(), server_default='0', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'total_qty_sales_filtered')
    # ### end Alembic commands ###