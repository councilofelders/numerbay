"""Add date_registered and unique lower indexes

Revision ID: 6c8e2b4f9d17
Revises: 5e8f2a1b4c56
Create Date: 2026-10-18 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6c8e2b4f9d17"
down_revision = "5e8f2a1b4c56"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "user",
        sa.Column("date_registered", sa.DateTime(), nullable=True),
    )
    op.execute('ALTER TABLE "user" ALTER COLUMN date_registered SET DEFAULT now()')
    op.add_column(
        "user",
        sa.Column(
            "email_verified",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
    )
    op.execute(
        'UPDATE "user" SET public_address = lower(public_address) '
        "WHERE public_address IS NOT NULL"
    )
    op.create_index(
        "user_public_address_lower_key",
        "user",
        [sa.text("lower(public_address)")],
        unique=True,
    )
    op.create_index(
        "user_email_lower_key",
        "user",
        [sa.text("lower(email)")],
        unique=True,
    )


def downgrade():
    op.drop_index("user_email_lower_key", table_name="user")
    op.drop_index("user_public_address_lower_key", table_name="user")
    op.drop_column("user", "email_verified")
    op.drop_column("user", "date_registered")
