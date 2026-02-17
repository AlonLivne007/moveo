from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.snapshot import DailySnapshot
from app.models.user import User
from app.repositories.snapshot_repository import SnapshotRepository
from app.repositories.user_repository import UserRepository
from app.integrations.cryptopanic import fetch_news as fetch_cryptopanic_news
from app.integrations.coingecko import fetch_prices
from app.integrations.reddit import fetch_meme as fetch_reddit_meme
from app.integrations.huggingface_or_openrouter import generate_insight
from app.utils.fallback_data import FALLBACK_NEWS, FALLBACK_MEME, FALLBACK_AI_INSIGHT


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.snapshot_repo = SnapshotRepository(db)
        self.user_repo = UserRepository(db)

    async def get_or_create_today_snapshot(self, user: User) -> DailySnapshot:
        snapshot = await self.snapshot_repo.get_today_for_user(user.id)
        if snapshot:
            return snapshot
        prefs = await self.user_repo.get_preferences(user.id)
        assets = list(prefs.assets or []) if prefs else []
        investor_type = prefs.investor_type if prefs else "Other"
        content_types = list(prefs.content_types or []) if prefs else []
        snapshot = await self.snapshot_repo.create_snapshot(user.id)
        await self._fill_snapshot(snapshot, assets, investor_type, content_types)
        # Reload snapshot with relationships
        result = await self.db.execute(
            select(DailySnapshot)
            .where(DailySnapshot.id == snapshot.id)
            .options(
                selectinload(DailySnapshot.news_items),
                selectinload(DailySnapshot.prices),
                selectinload(DailySnapshot.ai_insight),
                selectinload(DailySnapshot.meme),
            )
        )
        return result.scalar_one()

    async def _fill_snapshot(
        self,
        snapshot: DailySnapshot,
        assets: list[str],
        investor_type: str,
        content_types: list[str],
    ) -> None:
        # News: CryptoPanic or fallback (never let integration failure break the dashboard)
        try:
            news_raw = await fetch_cryptopanic_news(limit=5)
            raw_list = news_raw if news_raw else FALLBACK_NEWS
        except Exception:
            raw_list = FALLBACK_NEWS
        news_items = [
            {"title": (n.get("title") or "No title"), "source": n.get("source"), "url": n.get("url"), "published_at": n.get("published_at")}
            for n in raw_list[:5]
        ]
        await self.snapshot_repo.add_news_items(snapshot.id, news_items)

        # Prices: CoinGecko (fallback to empty so dashboard still loads)
        coin_ids = [a.strip().lower().replace(" ", "-") for a in assets if a][:10]
        if not coin_ids:
            coin_ids = ["bitcoin", "ethereum"]
        try:
            prices_data = await fetch_prices(coin_ids)
            prices_payload = {
                "items": [
                    {"id": p["id"], "symbol": p["symbol"], "name": p["name"], "current_price": p["current_price"], "change_24h": p.get("change_24h")}
                    for p in prices_data
                ]
            }
        except Exception:
            prices_payload = {"items": []}
        await self.snapshot_repo.set_prices(snapshot.id, prices_payload)

        # AI insight
        headlines = [n["title"] for n in news_items[:5]]
        try:
            text, model_name = await generate_insight(assets or ["crypto"], investor_type, headlines)
            if not text:
                text = FALLBACK_AI_INSIGHT
                model_name = "fallback"
        except Exception:
            text = FALLBACK_AI_INSIGHT
            model_name = "fallback"
        await self.snapshot_repo.set_ai_insight(snapshot.id, text, model_name, {"headlines": headlines})

        # Meme
        try:
            meme_data = await fetch_reddit_meme()
        except Exception:
            meme_data = None
        if not meme_data:
            meme_data = {
                "title": FALLBACK_MEME["title"],
                "image_url": FALLBACK_MEME["image_url"],
                "post_url": FALLBACK_MEME["post_url"],
            }
        await self.snapshot_repo.set_meme(
            snapshot.id,
            meme_data.get("title"),
            meme_data["image_url"],
            meme_data.get("post_url"),
            meme_data,
        )
