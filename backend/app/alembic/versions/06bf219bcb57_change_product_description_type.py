"""Change Product Description Type

Revision ID: 06bf219bcb57
Revises: f484f9b8e59c
Create Date: 2022-01-05 01:59:23.656562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06bf219bcb57'
down_revision = 'f484f9b8e59c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product', 'description',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product', 'description',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    # ### end Alembic commands ###
