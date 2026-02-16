from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.vote import VoteRequest, VoteResponse, VotesTodayResponse
from app.models.user import User
from app.controllers import vote_controller

router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("", response_model=VoteResponse)
async def post_vote(
    body: VoteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await vote_controller.post_vote(current_user, body, db)


@router.get("/today", response_model=VotesTodayResponse)
async def get_votes_today(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await vote_controller.get_votes_today(current_user, db)
