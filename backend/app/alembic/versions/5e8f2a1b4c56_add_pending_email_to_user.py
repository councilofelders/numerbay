"""Add pending_email to user

Revision ID: 5e8f2a1b4c56
Revises: 4d8e1f2a9c30
Create Date: 2026-10-18 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5e8f2a1b4c56"
down_revision = "4d8e1f2a9c30"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("user", sa.Column("pending_email", sa.String(), nullable=True))


def downgrade():
    op.drop_column("user", "pending_email")
