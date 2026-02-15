"""Phase S0: users table for Google Auth.

Revision ID: 002
Revises: 001
Create Date: 2025-02-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(256), primary_key=True),
        sa.Column("email", sa.String(512), nullable=True),
        sa.Column("name", sa.String(512), nullable=True),
        sa.Column("avatar_url", sa.String(1024), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("users")
