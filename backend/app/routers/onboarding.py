from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.onboarding import OnboardingRequest, PreferencesResponse
from app.services.onboarding_service import OnboardingService
from app.models.user import User

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


@router.post("")
async def submit_onboarding(
    body: OnboardingRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = OnboardingService(db)
    prefs = await service.save_preferences(
        current_user.id, body.assets, body.investor_type, body.content_types
    )
    return {"ok": True, "message": "Preferences saved"}


@router.get("/preferences", response_model=PreferencesResponse)
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = OnboardingService(db)
    prefs = await service.user_repo.get_preferences(current_user.id)
    if not prefs:
        return PreferencesResponse(assets=[], investor_type="Other", content_types=[])
    return PreferencesResponse(
        assets=list(prefs.assets or []),
        investor_type=prefs.investor_type,
        content_types=list(prefs.content_types or []),
    )
