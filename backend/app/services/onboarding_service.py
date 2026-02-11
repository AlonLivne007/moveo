from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository


class OnboardingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def save_preferences(
        self, user_id: int, assets: list[str], investor_type: str, content_types: list[str]
    ):
        return await self.user_repo.save_preferences(user_id, assets, investor_type, content_types)
