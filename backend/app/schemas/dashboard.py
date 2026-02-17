from datetime import date, datetime
from pydantic import BaseModel


class NewsItemPayload(BaseModel):
    id: int
    title: str
    source: str | None
    published_at: datetime | None
    link: str | None


class PriceItemPayload(BaseModel):
    id: str
    symbol: str
    name: str
    current_price: float
    change_24h: float | None


class PricesPayload(BaseModel):
    snapshot_id: int
    items: list[PriceItemPayload]


class AiInsightPayload(BaseModel):
    id: int
    text: str
    model_name: str | None


class MemePayload(BaseModel):
    id: int
    title: str | None
    image_url: str
    post_url: str | None


class DashboardResponse(BaseModel):
    date: date
    news: list[NewsItemPayload]
    prices: PricesPayload | None
    ai_insight: AiInsightPayload | None
    meme: MemePayload | None
