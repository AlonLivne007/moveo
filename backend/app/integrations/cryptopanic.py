import httpx
from datetime import datetime, timezone
from app.core.config import get_settings

# CryptoPanic API v2: https://cryptopanic.com/developers/api/
# Note: v2 posts response does NOT include article URL/link (only title, description, published_at, kind).
# We use a fallback link so items are still clickable.
CRYPTOPANIC_BASE = "https://cryptopanic.com/api/developer/v2"
CRYPTOPANIC_NEWS_FALLBACK_URL = "https://cryptopanic.com/news/"


def _normalize_source(item: dict) -> str | None:
    """Get source name from item; v2 may have source as object with title or as string."""
    raw = item.get("source")
    if raw is None:
        return None
    if isinstance(raw, str):
        return raw
    if isinstance(raw, dict):
        return raw.get("title")
    return None


def _normalize_url(item: dict) -> str:
    """Get article URL from item. Per API docs: original_url = real article, url = CryptoPanic page."""
    for key in ("original_url", "url", "link", "source_url", "external_url", "article_url"):
        val = item.get(key)
        if val and isinstance(val, str) and val.startswith(("http://", "https://")):
            return val
    source = item.get("source")
    if isinstance(source, dict):
        for key in ("url", "link", "href"):
            val = source.get(key)
            if val and isinstance(val, str) and val.startswith(("http://", "https://")):
                return val
    return CRYPTOPANIC_NEWS_FALLBACK_URL


async def fetch_news(limit: int = 5) -> list[dict]:
    """Fetch recent crypto news via CryptoPanic v2. Returns list of {title, source, url, published_at}. Never raises."""
    try:
        settings = get_settings()
        key = (settings.CRYPTOPANIC_API_KEY or "").strip()
        if not key:
            return []
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.get(
                f"{CRYPTOPANIC_BASE}/posts/",
                params={"auth_token": key, "public": "true"},
            )
            r.raise_for_status()
            data = r.json()
            results = data.get("results")
            if not isinstance(results, list):
                results = []
            out = []
            for item in results[:limit]:
                if not isinstance(item, dict):
                    continue
                try:
                    published = item.get("published_at")
                    if published:
                        try:
                            published_at = datetime.fromisoformat(str(published).replace("Z", "+00:00"))
                        except Exception:
                            published_at = None
                    else:
                        published_at = None
                    url = _normalize_url(item)
                    out.append({
                        "title": item.get("title") or "No title",
                        "source": _normalize_source(item) or "CryptoPanic",
                        "url": url,
                        "published_at": published_at,
                        "raw": item,
                    })
                except Exception:
                    continue
            return out
    except Exception:
        return []
