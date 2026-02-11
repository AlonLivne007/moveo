from datetime import datetime, timezone
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.db.base import Base


class Vote(Base):
    __tablename__ = "votes"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    section_type = sa.Column(sa.String(32), nullable=False)  # NEWS, PRICES, AI_INSIGHT, MEME
    content_id = sa.Column(sa.Integer, nullable=False)
    vote_value = sa.Column(sa.SmallInteger, nullable=False)  # +1 or -1
    created_at = sa.Column(sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="votes")

    __table_args__ = (
        sa.UniqueConstraint("user_id", "section_type", "content_id", name="uq_user_section_content"),
    )
