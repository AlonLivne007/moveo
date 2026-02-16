from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.routers import auth, me, onboarding, preferences, dashboard, votes, health

settings = get_settings()

app = FastAPI(title="AI Crypto Advisor API", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Allow extra origins from env (comma-separated)
if getattr(settings, "CORS_ORIGINS", None):
    origins.extend([o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(me.router, prefix="/api")
app.include_router(onboarding.router, prefix="/api")
app.include_router(preferences.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(votes.router, prefix="/api")
app.include_router(health.router, prefix="/api")
