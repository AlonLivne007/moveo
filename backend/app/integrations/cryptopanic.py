import httpx
from datetime import datetime, timezone
from app.core.config import get_settings

CRYPTOPANIC_BASE = "https://cryptopanic.com/api/v1"


async def fetch_news(limit: int = 5) -> list[dict]:
    """Fetch recent crypto news. Returns list of {title, source, url, published_at}."""
    settings = get_settings()
    if not settings.CRYPTOPANIC_API_KEY:
        return []
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            r = await client.get(
                f"{CRYPTOPANIC_BASE}/posts/",
                params={"auth_token": settings.CRYPTOPANIC_API_KEY, "public": "true"},
            )
            r.raise_for_status()
            data = r.json()
            results = data.get("results", [])[:limit]
            out = []
            for item in results:
                published = item.get("published_at")
                if published:
                    try:
                        published_at = datetime.fromisoformat(published.replace("Z", "+00:00"))
                    except Exception:
                        published_at = None
                else:
                    published_at = None
                out.append({
                    "title": item.get("title") or "No title",
                    "source": item.get("source", {}).get("title"),
                    "url": item.get("url"),
                    "published_at": published_at,
                    "raw": item,
                })
            return out
        except Exception:
            return []
