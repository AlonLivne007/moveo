from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.vote_repository import VoteRepository
from app.repositories.snapshot_repository import SnapshotRepository
from app.models.user import User


class VoteService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.vote_repo = VoteRepository(db)
        self.snapshot_repo = SnapshotRepository(db)

    async def upsert_vote(self, user: User, section_type: str, content_id: int, vote_value: int):
        if vote_value not in (1, -1):
            vote_value = 1 if vote_value > 0 else -1
        return await self.vote_repo.upsert(user.id, section_type, content_id, vote_value)

    async def get_votes_for_today(self, user: User):
        from datetime import date
        snapshot = await self.snapshot_repo.get_today_for_user(user.id)
        if not snapshot:
            return []
        return await self.vote_repo.get_votes_for_snapshot(user.id, snapshot)
