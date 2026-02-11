"""Initial schema

Revision ID: 001
Revises:
Create Date: 2025-02-11

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "user_preferences",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("assets", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("investor_type", sa.String(64), nullable=False),
        sa.Column("content_types", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "daily_snapshots",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("snapshot_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "snapshot_date", name="uq_user_snapshot_date"),
    )
    op.create_index(op.f("ix_daily_snapshots_user_id"), "daily_snapshots", ["user_id"], unique=False)

    op.create_table(
        "snapshot_news_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("snapshot_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(1024), nullable=False),
        sa.Column("source", sa.String(255), nullable=True),
        sa.Column("url", sa.String(2048), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("raw_json", postgresql.JSONB(), nullable=True),
        sa.ForeignKeyConstraint(["snapshot_id"], ["daily_snapshots.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "snapshot_prices",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("snapshot_id", sa.Integer(), nullable=False),
        sa.Column("raw_json", postgresql.JSONB(), nullable=False),
        sa.ForeignKeyConstraint(["snapshot_id"], ["daily_snapshots.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("snapshot_id"),
    )

    op.create_table(
        "snapshot_ai_insights",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("snapshot_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("model_name", sa.String(128), nullable=True),
        sa.Column("raw_json", postgresql.JSONB(), nullable=True),
        sa.ForeignKeyConstraint(["snapshot_id"], ["daily_snapshots.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("snapshot_id"),
    )

    op.create_table(
        "snapshot_memes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("snapshot_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(1024), nullable=True),
        sa.Column("image_url", sa.String(2048), nullable=False),
        sa.Column("post_url", sa.String(2048), nullable=True),
        sa.Column("raw_json", postgresql.JSONB(), nullable=True),
        sa.ForeignKeyConstraint(["snapshot_id"], ["daily_snapshots.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("snapshot_id"),
    )

    op.create_table(
        "votes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("section_type", sa.String(32), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.Column("vote_value", sa.SmallInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "section_type", "content_id", name="uq_user_section_content"),
    )
    op.create_index(op.f("ix_votes_user_id"), "votes", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_votes_user_id"), table_name="votes")
    op.drop_table("votes")
    op.drop_table("snapshot_memes")
    op.drop_table("snapshot_ai_insights")
    op.drop_table("snapshot_prices")
    op.drop_table("snapshot_news_items")
    op.drop_index(op.f("ix_daily_snapshots_user_id"), table_name="daily_snapshots")
    op.drop_table("daily_snapshots")
    op.drop_table("user_preferences")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
