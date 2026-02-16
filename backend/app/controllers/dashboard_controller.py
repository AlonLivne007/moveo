from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.dashboard import (
    DashboardResponse,
    NewsItemPayload,
    PriceItemPayload,
    PricesPayload,
    AiInsightPayload,
    MemePayload,
)
from app.services.dashboard_service import DashboardService
from app.models.user import User


async def get_today_dashboard(current_user: User, db: AsyncSession) -> DashboardResponse:
    service = DashboardService(db)
    snapshot = await service.get_or_create_today_snapshot(current_user)
    news = [
        NewsItemPayload(
            id=n.id,
            title=n.title,
            source=n.source,
            published_at=n.published_at,
            link=n.url,
        )
        for n in snapshot.news_items
    ]
    prices_payload = None
    if snapshot.prices and snapshot.prices.raw_json:
        items = snapshot.prices.raw_json.get("items", [])
        prices_payload = PricesPayload(
            snapshot_id=snapshot.prices.id,
            items=[
                PriceItemPayload(
                    id=p.get("id", ""),
                    symbol=p.get("symbol", ""),
                    name=p.get("name", ""),
                    current_price=p.get("current_price", 0),
                    change_24h=p.get("change_24h"),
                )
                for p in items
            ],
        )
    ai_insight_payload = None
    if snapshot.ai_insight:
        ai_insight_payload = AiInsightPayload(
            id=snapshot.ai_insight.id,
            text=snapshot.ai_insight.text,
            model_name=snapshot.ai_insight.model_name,
        )
    meme_payload = None
    if snapshot.meme:
        meme_payload = MemePayload(
            id=snapshot.meme.id,
            title=snapshot.meme.title,
            image_url=snapshot.meme.image_url,
            post_url=snapshot.meme.post_url,
        )
    return DashboardResponse(
        date=snapshot.snapshot_date,
        news=news,
        prices=prices_payload,
        ai_insight=ai_insight_payload,
        meme=meme_payload,
    )
