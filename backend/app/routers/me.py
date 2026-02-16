from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.auth import UserProfile
from app.models.user import User
from app.controllers import me_controller

router = APIRouter(tags=["me"])


@router.get("/me", response_model=UserProfile)
async def me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await me_controller.get_profile(current_user, db)
