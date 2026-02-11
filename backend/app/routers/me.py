from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.auth import UserProfile
from app.models.user import User
from app.repositories.user_repository import UserRepository

router = APIRouter(tags=["me"])


@router.get("/me", response_model=UserProfile)
async def me(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    prefs = await user_repo.get_preferences(current_user.id)
    onboarded = prefs is not None
    return UserProfile(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        onboarded=onboarded,
    )
