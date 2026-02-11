import httpx
from app.core.config import get_settings


async def generate_insight(
    assets: list[str],
    investor_type: str,
    news_headlines: list[str],
) -> tuple[str, str | None]:
    """
    Generate a short AI insight. Returns (text, model_name).
    Uses OpenRouter or HuggingFace; fallback returns empty string and None.
    """
    settings = get_settings()
    prompt = _build_prompt(assets, investor_type, news_headlines)

    # Try OpenRouter first if key present
    if settings.OPENROUTER_API_KEY:
        text, model = await _try_openrouter(prompt, settings.OPENROUTER_API_KEY)
        if text:
            return (text, model)

    # Try HuggingFace
    if settings.HUGGINGFACE_API_KEY:
        text, model = await _try_huggingface(prompt, settings.HUGGINGFACE_API_KEY)
        if text:
            return (text, model)

    return ("", None)


def _build_prompt(assets: list[str], investor_type: str, news_headlines: list[str]) -> str:
    assets_str = ", ".join(assets) if assets else "general market"
    news_str = "\n".join(news_headlines[:5]) if news_headlines else "No specific news today."
    return f"""You are a crypto advisor. In 2-3 short sentences, give a friendly daily insight for a {investor_type} interested in: {assets_str}.

Today's headlines (for context):
{news_str}

Reply with only the insight, no preamble."""


async def _try_openrouter(prompt: str, api_key: str) -> tuple[str, str | None]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            r = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 150,
                },
            )
            r.raise_for_status()
            data = r.json()
            content = (data.get("choices") or [{}])[0].get("message", {}).get("content", "").strip()
            model = data.get("model")
            return (content, model)
        except Exception:
            return ("", None)


async def _try_huggingface(prompt: str, api_key: str) -> tuple[str, str | None]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            r = await client.post(
                "https://api-inference.huggingface.co/models/google/flan-t5-base",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"inputs": prompt, "parameters": {"max_length": 150}},
            )
            if r.status_code != 200:
                return ("", None)
            data = r.json()
            if isinstance(data, list) and len(data) > 0:
                text = data[0].get("generated_text", "").strip()
                return (text, "flan-t5-base")
            return ("", None)
        except Exception:
            return ("", None)
