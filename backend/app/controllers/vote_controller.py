from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.vote import VoteRequest, VoteResponse, VotesTodayResponse
from app.services.vote_service import VoteService
from app.models.user import User


async def post_vote(
    current_user: User, body: VoteRequest, db: AsyncSession
) -> VoteResponse:
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


async def get_votes_today(
    current_user: User, db: AsyncSession
) -> VotesTodayResponse:
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
