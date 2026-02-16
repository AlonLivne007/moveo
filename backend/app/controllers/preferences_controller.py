from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.onboarding import PreferencesResponse
from app.models.user import User
from app.controllers.onboarding_controller import get_preferences as _get_preferences


async def get_preferences(current_user: User, db: AsyncSession) -> PreferencesResponse:
    return await _get_preferences(current_user, db)
