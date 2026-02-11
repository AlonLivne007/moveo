from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://moveo:moveo_secret@localhost:5432/moveo_crypto"

    # JWT
    JWT_SECRET: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MINUTES: int = 1440  # 24h

    # Optional API keys (fallbacks used when empty)
    CRYPTOPANIC_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    HUGGINGFACE_API_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
