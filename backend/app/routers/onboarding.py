from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.onboarding import OnboardingRequest, PreferencesResponse
from app.models.user import User
from app.controllers import onboarding_controller

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


@router.post("")
async def submit_onboarding(
    body: OnboardingRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await onboarding_controller.submit_onboarding(current_user, body, db)


@router.get("/preferences", response_model=PreferencesResponse)
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await onboarding_controller.get_preferences(current_user, db)
