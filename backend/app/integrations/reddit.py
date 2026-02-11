import httpx

REDDIT_JSON = "https://www.reddit.com/r/cryptomemes.json"


async def fetch_meme() -> dict | None:
    """Fetch a random meme from Reddit r/cryptomemes. Returns {title, image_url, post_url} or None."""
    async with httpx.AsyncClient(timeout=15.0, headers={"User-Agent": "MoveoCryptoAdvisor/1.0"}) as client:
        try:
            r = await client.get(REDDIT_JSON, params={"limit": 25})
            r.raise_for_status()
            data = r.json()
            children = data.get("data", {}).get("children", [])
            for c in children:
                d = c.get("data", {})
                if d.get("post_hint") != "image" and not d.get("url", "").endswith((".jpg", ".jpeg", ".png", ".gif")):
                    continue
                url = d.get("url") or d.get("thumbnail")
                if not url:
                    continue
                return {
                    "title": d.get("title"),
                    "image_url": url,
                    "post_url": f"https://reddit.com{d.get('permalink', '')}",
                    "raw": d,
                }
            return None
        except Exception:
            return None
