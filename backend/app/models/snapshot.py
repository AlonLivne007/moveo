from datetime import datetime, timezone, date
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base


class DailySnapshot(Base):
    __tablename__ = "daily_snapshots"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    snapshot_date = sa.Column(sa.Date, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="snapshots")
    news_items = relationship("SnapshotNewsItem", back_populates="snapshot", cascade="all, delete-orphan")
    prices = relationship("SnapshotPrices", back_populates="snapshot", uselist=False, cascade="all, delete-orphan")
    ai_insight = relationship("SnapshotAiInsight", back_populates="snapshot", uselist=False, cascade="all, delete-orphan")
    meme = relationship("SnapshotMeme", back_populates="snapshot", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (sa.UniqueConstraint("user_id", "snapshot_date", name="uq_user_snapshot_date"),)


class SnapshotNewsItem(Base):
    __tablename__ = "snapshot_news_items"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    snapshot_id = sa.Column(sa.Integer, sa.ForeignKey("daily_snapshots.id", ondelete="CASCADE"), nullable=False)
    title = sa.Column(sa.String(1024), nullable=False)
    source = sa.Column(sa.String(255), nullable=True)
    url = sa.Column(sa.String(2048), nullable=True)
    published_at = sa.Column(sa.DateTime(timezone=True), nullable=True)
    raw_json = sa.Column(JSONB, nullable=True)

    snapshot = relationship("DailySnapshot", back_populates="news_items")


class SnapshotPrices(Base):
    __tablename__ = "snapshot_prices"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    snapshot_id = sa.Column(sa.Integer, sa.ForeignKey("daily_snapshots.id", ondelete="CASCADE"), unique=True, nullable=False)
    raw_json = sa.Column(JSONB, nullable=False)

    snapshot = relationship("DailySnapshot", back_populates="prices")


class SnapshotAiInsight(Base):
    __tablename__ = "snapshot_ai_insights"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    snapshot_id = sa.Column(sa.Integer, sa.ForeignKey("daily_snapshots.id", ondelete="CASCADE"), unique=True, nullable=False)
    text = sa.Column(sa.Text, nullable=False)
    model_name = sa.Column(sa.String(128), nullable=True)
    raw_json = sa.Column(JSONB, nullable=True)

    snapshot = relationship("DailySnapshot", back_populates="ai_insight")


class SnapshotMeme(Base):
    __tablename__ = "snapshot_memes"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    snapshot_id = sa.Column(sa.Integer, sa.ForeignKey("daily_snapshots.id", ondelete="CASCADE"), unique=True, nullable=False)
    title = sa.Column(sa.String(1024), nullable=True)
    image_url = sa.Column(sa.String(2048), nullable=False)
    post_url = sa.Column(sa.String(2048), nullable=True)
    raw_json = sa.Column(JSONB, nullable=True)

    snapshot = relationship("DailySnapshot", back_populates="meme")
