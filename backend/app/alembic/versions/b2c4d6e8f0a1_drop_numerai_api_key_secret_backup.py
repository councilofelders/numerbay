"""Drop numerai_api_key_secret_backup from user

Revision ID: b2c4d6e8f0a1
Revises: 9f3e7c2a1b8d
Create Date: 2026-10-21
"""
from alembic import op
import sqlalchemy as sa

revision = "b2c4d6e8f0a1"
down_revision = "9f3e7c2a1b8d"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("user", "numerai_api_key_secret_backup")


def downgrade():
    op.add_column(
        "user",
        sa.Column("numerai_api_key_secret_backup", sa.String(), nullable=True),
    )
