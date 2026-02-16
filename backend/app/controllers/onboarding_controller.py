from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.onboarding import OnboardingRequest, PreferencesResponse
from app.services.onboarding_service import OnboardingService
from app.models.user import User


async def submit_onboarding(
    current_user: User, body: OnboardingRequest, db: AsyncSession
) -> dict:
    service = OnboardingService(db)
    await service.save_preferences(
        current_user.id, body.assets, body.investor_type, body.content_types
    )
    return {"ok": True, "message": "Preferences saved"}


async def get_preferences(current_user: User, db: AsyncSession) -> PreferencesResponse:
    service = OnboardingService(db)
    assets, investor_type, content_types = await service.get_preferences_data(current_user.id)
    return PreferencesResponse(
        assets=assets,
        investor_type=investor_type,
        content_types=content_types,
    )
