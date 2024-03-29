"""Add discord social

Revision ID: 5eacb83fd25a
Revises: cef21686bfb5
Create Date: 2023-04-22 06:54:20.904113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5eacb83fd25a'
down_revision = 'cef21686bfb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('social_discord', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'social_discord')
    # ### end Alembic commands ###
