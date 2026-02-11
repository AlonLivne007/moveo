"""Static fallback data when external APIs are unavailable."""


FALLBACK_NEWS = [
    {"title": "Bitcoin holds key support as macro outlook improves", "source": "CryptoBriefing", "url": "https://example.com/1", "published_at": None},
    {"title": "Ethereum upgrade expected to reduce gas fees", "source": "Decrypt", "url": "https://example.com/2", "published_at": None},
    {"title": "Stablecoin regulations under discussion in major markets", "source": "CoinDesk", "url": "https://example.com/3", "published_at": None},
    {"title": "DeFi TVL recovers amid renewed investor interest", "source": "The Block", "url": "https://example.com/4", "published_at": None},
    {"title": "Crypto adoption continues in emerging markets", "source": "Bloomberg Crypto", "url": "https://example.com/5", "published_at": None},
]

FALLBACK_MEME = {
    "title": "HODL strong 💪",
    "image_url": "https://via.placeholder.com/400x300?text=Crypto+Meme+of+the+Day",
    "post_url": "https://reddit.com/r/cryptomemes",
}

FALLBACK_AI_INSIGHT = (
    "Markets are dynamic—stay informed with the news and prices above, "
    "and remember to only invest what you can afford to lose. Diversification and a clear strategy "
    "fit your investor profile. Check back tomorrow for a fresh insight!"
)
