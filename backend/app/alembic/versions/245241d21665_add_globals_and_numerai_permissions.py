"""Add Globals and Numerai Permissions

Revision ID: 245241d21665
Revises: 7ddf2372a420
Create Date: 2021-09-03 11:49:45.297383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '245241d21665'
down_revision = '7ddf2372a420'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('globals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('active_round', sa.Integer(), nullable=False),
    sa.Column('selling_round', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'active_round', 'selling_round')
    )
    op.create_index(op.f('ix_globals_active_round'), 'globals', ['active_round'], unique=False)
    op.create_index(op.f('ix_globals_id'), 'globals', ['id'], unique=False)
    op.create_index(op.f('ix_globals_selling_round'), 'globals', ['selling_round'], unique=False)
    op.add_column('user', sa.Column('numerai_api_key_can_upload_submission', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('numerai_api_key_can_stake', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('numerai_api_key_can_read_submission_info', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('numerai_api_key_can_read_user_info', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('numerai_wallet_address', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'numerai_wallet_address')
    op.drop_column('user', 'numerai_api_key_can_read_user_info')
    op.drop_column('user', 'numerai_api_key_can_read_submission_info')
    op.drop_column('user', 'numerai_api_key_can_stake')
    op.drop_column('user', 'numerai_api_key_can_upload_submission')
    op.drop_index(op.f('ix_globals_selling_round'), table_name='globals')
    op.drop_index(op.f('ix_globals_id'), table_name='globals')
    op.drop_index(op.f('ix_globals_active_round'), table_name='globals')
    op.drop_table('globals')
    # ### end Alembic commands ###
