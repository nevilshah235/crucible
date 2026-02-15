"""Phase 1 schema: concepts, quizzes, failure_facts, curriculum_drafts, ingested_docs, concept_completions.

Revision ID: 001
Revises:
Create Date: 2025-02-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "concepts",
        sa.Column("id", sa.String(128), primary_key=True),
        sa.Column("track", sa.String(64), nullable=False, server_default="system_design"),
        sa.Column("phase", sa.String(64), nullable=False, server_default="fundamentals"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("prerequisite_concept_ids", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("title", sa.String(512), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("tags", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
    )
    op.create_table(
        "quizzes",
        sa.Column("id", sa.String(128), primary_key=True),
        sa.Column("concept_id", sa.String(128), sa.ForeignKey("concepts.id"), nullable=False),
        sa.Column("questions", postgresql.JSONB(), nullable=False),
        sa.Column("difficulty_tier", sa.String(32), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
    )
    op.create_table(
        "failure_facts",
        sa.Column("id", sa.String(128), primary_key=True),
        sa.Column("concept_id", sa.String(128), sa.ForeignKey("concepts.id"), nullable=True),
        sa.Column("tags", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("keywords", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("fact", sa.Text(), nullable=False),
        sa.Column("prompt_hint", sa.String(1024), nullable=True),
        sa.Column("difficulty_tier", sa.String(32), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
    )
    op.create_table(
        "curriculum_drafts",
        sa.Column("id", sa.String(128), primary_key=True),
        sa.Column("type", sa.String(32), nullable=False),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
    )
    op.create_table(
        "ingested_docs",
        sa.Column("doc_id", sa.String(256), primary_key=True),
        sa.Column("name", sa.String(512), nullable=False),
        sa.Column("type", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
    )
    op.create_table(
        "concept_completions",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("user_id", sa.String(256), nullable=True),
        sa.Column("session_id", sa.String(256), nullable=True),
        sa.Column("concept_id", sa.String(128), sa.ForeignKey("concepts.id"), nullable=False),
        sa.Column("completed_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("quiz_score", sa.Integer(), nullable=True),
        sa.Column("design_submitted", sa.Boolean(), server_default="false", nullable=True),
    )


def downgrade() -> None:
    op.drop_table("concept_completions")
    op.drop_table("ingested_docs")
    op.drop_table("curriculum_drafts")
    op.drop_table("failure_facts")
    op.drop_table("quizzes")
    op.drop_table("concepts")
