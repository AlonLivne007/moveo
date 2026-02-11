from datetime import datetime
from pydantic import BaseModel


class VoteRequest(BaseModel):
    section_type: str  # NEWS, PRICES, AI_INSIGHT, MEME
    content_id: int
    vote_value: int  # +1 or -1


class VoteResponse(BaseModel):
    id: int
    section_type: str
    content_id: int
    vote_value: int
    created_at: datetime

    class Config:
        from_attributes = True


class VotesTodayResponse(BaseModel):
    votes: list[VoteResponse]
