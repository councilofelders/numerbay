"""Add token_version to user

Revision ID: 4d8e1f2a9c30
Revises: 2f4a9d6c8b12
Create Date: 2026-10-18 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4d8e1f2a9c30"
down_revision = "2f4a9d6c8b12"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "user",
        sa.Column("token_version", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade():
    op.drop_column("user", "token_version")
