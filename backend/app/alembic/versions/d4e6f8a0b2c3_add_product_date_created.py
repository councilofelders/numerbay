"""Add Product Date Created

Revision ID: d4e6f8a0b2c3
Revises: c3d5e7f9a1b2
Create Date: 2026-11-21
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d4e6f8a0b2c3"
down_revision = "c3d5e7f9a1b2"
branch_labels = None
depends_on = None


def upgrade():
    # Default added separately so existing products stay NULL (creation time unknown).
    op.add_column("product", sa.Column("date_created", sa.DateTime(), nullable=True))
    op.execute("ALTER TABLE product ALTER COLUMN date_created SET DEFAULT now()")


def downgrade():
    op.drop_column("product", "date_created")
