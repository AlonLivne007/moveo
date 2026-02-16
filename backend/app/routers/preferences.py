from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.onboarding import PreferencesResponse
from app.models.user import User
from app.controllers import preferences_controller

router = APIRouter(tags=["preferences"])


@router.get("/preferences", response_model=PreferencesResponse)
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await preferences_controller.get_preferences(current_user, db)
