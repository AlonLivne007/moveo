from pydantic import BaseModel


class OnboardingRequest(BaseModel):
    assets: list[str]
    investor_type: str  # HODLer, Day Trader, NFT Collector, Other
    content_types: list[str]  # Market News, Charts, Social, Fun


class PreferencesResponse(BaseModel):
    assets: list[str]
    investor_type: str
    content_types: list[str]

    class Config:
        from_attributes = True
