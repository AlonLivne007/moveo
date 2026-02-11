from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.vote import Vote
from app.models.snapshot import DailySnapshot


class VoteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert(self, user_id: int, section_type: str, content_id: int, vote_value: int) -> Vote:
        result = await self.db.execute(
            select(Vote).where(
                Vote.user_id == user_id,
                Vote.section_type == section_type,
                Vote.content_id == content_id,
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.vote_value = vote_value
            await self.db.flush()
            await self.db.refresh(existing)
            return existing
        vote = Vote(
            user_id=user_id,
            section_type=section_type,
            content_id=content_id,
            vote_value=vote_value,
        )
        self.db.add(vote)
        await self.db.flush()
        await self.db.refresh(vote)
        return vote

    async def get_votes_for_snapshot(self, user_id: int, snapshot: DailySnapshot) -> list[Vote]:
        """Return votes for this user that reference content from the given snapshot."""
        result = await self.db.execute(select(Vote).where(Vote.user_id == user_id))
        all_votes = list(result.scalars().all())
        news_ids = {n.id for n in snapshot.news_items}
        prices_id = snapshot.prices.id if snapshot.prices else None
        ai_id = snapshot.ai_insight.id if snapshot.ai_insight else None
        meme_id = snapshot.meme.id if snapshot.meme else None
        return [
            v for v in all_votes
            if (v.section_type == "NEWS" and v.content_id in news_ids)
            or (v.section_type == "PRICES" and v.content_id == prices_id)
            or (v.section_type == "AI_INSIGHT" and v.content_id == ai_id)
            or (v.section_type == "MEME" and v.content_id == meme_id)
        ]
