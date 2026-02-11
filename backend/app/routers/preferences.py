from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.onboarding import PreferencesResponse
from app.models.user import User
from app.repositories.user_repository import UserRepository

router = APIRouter(tags=["preferences"])


@router.get("/preferences", response_model=PreferencesResponse)
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """GET /api/preferences — returns current user's onboarding preferences (optional endpoint)."""
    user_repo = UserRepository(db)
    prefs = await user_repo.get_preferences(current_user.id)
    if not prefs:
        return PreferencesResponse(assets=[], investor_type="Other", content_types=[])
    return PreferencesResponse(
        assets=list(prefs.assets or []),
        investor_type=prefs.investor_type,
        content_types=list(prefs.content_types or []),
    )
