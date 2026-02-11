from datetime import datetime, timezone
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255), nullable=False)
    email = sa.Column(sa.String(255), unique=True, nullable=False, index=True)
    password_hash = sa.Column(sa.String(255), nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    preferences = relationship("UserPreferences", back_populates="user", uselist=False)
    snapshots = relationship("DailySnapshot", back_populates="user")
    votes = relationship("Vote", back_populates="user")


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    assets = sa.Column(ARRAY(sa.Text), nullable=False, default=list)
    investor_type = sa.Column(sa.String(64), nullable=False)
    content_types = sa.Column(ARRAY(sa.Text), nullable=False, default=list)
    created_at = sa.Column(sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="preferences")
