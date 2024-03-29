"""Add default receiving wallet address to User

Revision ID: 9d06b3058ad6
Revises: bcbca7b17c1d
Create Date: 2024-02-04 01:52:09.900869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d06b3058ad6'
down_revision = 'bcbca7b17c1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('default_receiving_wallet_address', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'user', ['default_receiving_wallet_address'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'default_receiving_wallet_address')
    # ### end Alembic commands ###
