from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import UserProfile
from app.models.user import User
from app.services.auth_service import AuthService


async def get_profile(current_user: User, db: AsyncSession) -> UserProfile:
    service = AuthService(db)
    data = await service.get_profile_data(current_user)
    return UserProfile(**data)
