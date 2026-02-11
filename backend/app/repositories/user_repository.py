from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserPreferences


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, name: str, email: str, password_hash: str) -> User:
        user = User(name=name, email=email, password_hash=password_hash)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def get_preferences(self, user_id: int) -> UserPreferences | None:
        result = await self.db.execute(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def save_preferences(
        self,
        user_id: int,
        assets: list[str],
        investor_type: str,
        content_types: list[str],
    ) -> UserPreferences:
        prefs = await self.get_preferences(user_id)
        if prefs:
            prefs.assets = assets
            prefs.investor_type = investor_type
            prefs.content_types = content_types
            await self.db.flush()
            await self.db.refresh(prefs)
            return prefs
        prefs = UserPreferences(
            user_id=user_id,
            assets=assets,
            investor_type=investor_type,
            content_types=content_types,
        )
        self.db.add(prefs)
        await self.db.flush()
        await self.db.refresh(prefs)
        return prefs
