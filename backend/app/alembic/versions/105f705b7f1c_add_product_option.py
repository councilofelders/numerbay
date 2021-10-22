"""Add Product Option

Revision ID: 105f705b7f1c
Revises: ee346caf6181
Create Date: 2021-10-21 14:38:02.916286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '105f705b7f1c'
down_revision = 'ee346caf6181'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_option', sa.Column('quantity', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product_option', 'quantity')
    # ### end Alembic commands ###
