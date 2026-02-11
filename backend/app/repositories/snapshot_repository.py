from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.snapshot import (
    DailySnapshot,
    SnapshotNewsItem,
    SnapshotPrices,
    SnapshotAiInsight,
    SnapshotMeme,
)


class SnapshotRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_today_for_user(self, user_id: int) -> DailySnapshot | None:
        today = date.today()
        result = await self.db.execute(
            select(DailySnapshot)
            .where(DailySnapshot.user_id == user_id, DailySnapshot.snapshot_date == today)
            .options(
                selectinload(DailySnapshot.news_items),
                selectinload(DailySnapshot.prices),
                selectinload(DailySnapshot.ai_insight),
                selectinload(DailySnapshot.meme),
            )
        )
        return result.scalar_one_or_none()

    async def create_snapshot(self, user_id: int) -> DailySnapshot:
        today = date.today()
        snapshot = DailySnapshot(user_id=user_id, snapshot_date=today)
        self.db.add(snapshot)
        await self.db.flush()
        await self.db.refresh(snapshot)
        return snapshot

    async def add_news_items(self, snapshot_id: int, items: list[dict]) -> list[SnapshotNewsItem]:
        created = []
        for item in items:
            news = SnapshotNewsItem(
                snapshot_id=snapshot_id,
                title=item.get("title", ""),
                source=item.get("source"),
                url=item.get("url"),
                published_at=item.get("published_at"),
                raw_json=item,
            )
            self.db.add(news)
            created.append(news)
        await self.db.flush()
        for n in created:
            await self.db.refresh(n)
        return created

    async def set_prices(self, snapshot_id: int, raw_json: dict) -> SnapshotPrices:
        prices = SnapshotPrices(snapshot_id=snapshot_id, raw_json=raw_json)
        self.db.add(prices)
        await self.db.flush()
        await self.db.refresh(prices)
        return prices

    async def set_ai_insight(
        self, snapshot_id: int, text: str, model_name: str | None = None, raw_json: dict | None = None
    ) -> SnapshotAiInsight:
        insight = SnapshotAiInsight(
            snapshot_id=snapshot_id, text=text, model_name=model_name, raw_json=raw_json
        )
        self.db.add(insight)
        await self.db.flush()
        await self.db.refresh(insight)
        return insight

    async def set_meme(
        self,
        snapshot_id: int,
        title: str | None,
        image_url: str,
        post_url: str | None = None,
        raw_json: dict | None = None,
    ) -> SnapshotMeme:
        meme = SnapshotMeme(
            snapshot_id=snapshot_id,
            title=title,
            image_url=image_url,
            post_url=post_url,
            raw_json=raw_json,
        )
        self.db.add(meme)
        await self.db.flush()
        await self.db.refresh(meme)
        return meme
