import httpx

COINGECKO_BASE = "https://api.coingecko.com/api/v3"
# CoinGecko can block server requests (e.g. from Render) when User-Agent looks like a bot. Use a browser-like one.
COINGECKO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


async def fetch_prices(coin_ids: list[str]) -> list[dict]:
    """Fetch current price and 24h change for given coin ids. coin_ids are CoinGecko ids (e.g. bitcoin, ethereum)."""
    if not coin_ids:
        return []
    ids = ",".join(coin_ids[:10])  # limit to 10
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            r = await client.get(
                f"{COINGECKO_BASE}/coins/markets",
                params={"vs_currency": "usd", "ids": ids, "order": "market_cap_desc"},
                headers=COINGECKO_HEADERS,
            )
            r.raise_for_status()
            data = r.json()
            return [
                {
                    "id": str(d["id"]),
                    "symbol": d.get("symbol", "").upper(),
                    "name": d.get("name", ""),
                    "current_price": d.get("current_price") or 0,
                    "change_24h": d.get("price_change_percentage_24h"),
                }
                for d in data
            ]
        except Exception:
            return []
