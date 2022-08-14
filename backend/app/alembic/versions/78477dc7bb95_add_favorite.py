"""Add Favorite

Revision ID: 78477dc7bb95
Revises: 72059e3bfee8
Create Date: 2021-10-31 13:36:19.636594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78477dc7bb95'
down_revision = '72059e3bfee8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete="CASCADE"),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_favorite_id'), 'favorite', ['id'], unique=False)
    op.create_index(op.f('ix_favorite_user_id'), 'favorite', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_favorite_user_id'), table_name='favorite')
    op.drop_index(op.f('ix_favorite_id'), table_name='favorite')
    op.drop_table('favorite')
    # ### end Alembic commands ###