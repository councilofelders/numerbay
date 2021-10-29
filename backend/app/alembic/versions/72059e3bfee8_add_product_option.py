"""Add Product Option

Revision ID: 72059e3bfee8
Revises: ee346caf6181
Create Date: 2021-10-28 07:06:32.482619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72059e3bfee8'
down_revision = 'ee346caf6181'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_option',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_on_platform', sa.Boolean(), server_default='f', nullable=False),
    sa.Column('third_party_url', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('currency', sa.String(), server_default='USD', nullable=False),
    sa.Column('wallet', sa.String(), nullable=True),
    sa.Column('chain', sa.String(), nullable=True),
    sa.Column('stake_limit', sa.Numeric(), nullable=True),
    sa.Column('mode', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default='t', nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete="CASCADE"),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_option_id'), 'product_option', ['id'], unique=False)
    op.create_index(op.f('ix_product_option_price'), 'product_option', ['price'], unique=False)
    op.add_column('order', sa.Column('quantity', sa.Integer(), server_default='1', nullable=False))
    op.alter_column('product', 'is_on_platform',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('false'))
    op.alter_column('product', 'price',
               existing_type=sa.NUMERIC(),
               nullable=True)
    op.alter_column('product', 'currency',
               existing_type=sa.VARCHAR(),
               nullable=True,
               existing_server_default=sa.text("'USD'::character varying"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product', 'currency',
               existing_type=sa.VARCHAR(),
               nullable=False,
               existing_server_default=sa.text("'USD'::character varying"))
    op.alter_column('product', 'price',
               existing_type=sa.NUMERIC(),
               nullable=False)
    op.alter_column('product', 'is_on_platform',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('false'))
    op.drop_column('order', 'quantity')
    op.drop_index(op.f('ix_product_option_price'), table_name='product_option')
    op.drop_index(op.f('ix_product_option_id'), table_name='product_option')
    op.drop_table('product_option')
    # ### end Alembic commands ###