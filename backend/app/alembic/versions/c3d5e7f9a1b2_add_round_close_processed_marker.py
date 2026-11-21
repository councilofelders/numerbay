"""Add Round Close Processed Marker

Revision ID: c3d5e7f9a1b2
Revises: b2c4d6e8f0a1
Create Date: 2026-11-21
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c3d5e7f9a1b2"
down_revision = "b2c4d6e8f0a1"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "globals",
        sa.Column("last_round_close_processed", sa.Integer(), nullable=True),
    )
    op.execute(
        "UPDATE globals SET last_round_close_processed = active_round "
        "WHERE selling_round > active_round"
    )


def downgrade():
    op.drop_column("globals", "last_round_close_processed")
