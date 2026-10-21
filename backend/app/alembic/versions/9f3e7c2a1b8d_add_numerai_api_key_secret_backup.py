"""Add numerai_api_key_secret_backup to user

Revision ID: 9f3e7c2a1b8d
Revises: 6c8e2b4f9d17
Create Date: 2026-10-21 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9f3e7c2a1b8d"
down_revision = "6c8e2b4f9d17"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "user",
        sa.Column("numerai_api_key_secret_backup", sa.String(), nullable=True),
    )
    op.execute(
        'UPDATE "user" SET numerai_api_key_secret_backup = numerai_api_key_secret '
        "WHERE numerai_api_key_secret IS NOT NULL"
    )


def downgrade():
    op.execute(
        'UPDATE "user" SET numerai_api_key_secret = numerai_api_key_secret_backup '
        "WHERE numerai_api_key_secret_backup IS NOT NULL "
        "AND numerai_api_key_secret IS NULL"
    )
    op.drop_column("user", "numerai_api_key_secret_backup")
