"""Add Round Open Processed Marker

Revision ID: 2f4a9d6c8b12
Revises: 9d06b3058ad6
Create Date: 2026-05-17 13:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2f4a9d6c8b12"
down_revision = "9d06b3058ad6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "globals",
        sa.Column("last_round_open_processed", sa.Integer(), nullable=True),
    )


def downgrade():
    op.drop_column("globals", "last_round_open_processed")
