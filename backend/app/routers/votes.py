from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.vote import VoteRequest, VoteResponse, VotesTodayResponse
from app.services.vote_service import VoteService
from app.models.user import User

router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("", response_model=VoteResponse)
async def post_vote(
    body: VoteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = VoteService(db)
    vote = await service.upsert_vote(
        current_user, body.section_type, body.content_id, body.vote_value
    )
    return VoteResponse(
        id=vote.id,
        section_type=vote.section_type,
        content_id=vote.content_id,
        vote_value=vote.vote_value,
        created_at=vote.created_at,
    )


@router.get("/today", response_model=VotesTodayResponse)
async def get_votes_today(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = VoteService(db)
    votes = await service.get_votes_for_today(current_user)
    return VotesTodayResponse(
        votes=[
            VoteResponse(
                id=v.id,
                section_type=v.section_type,
                content_id=v.content_id,
                vote_value=v.vote_value,
                created_at=v.created_at,
            )
            for v in votes
        ]
    )
