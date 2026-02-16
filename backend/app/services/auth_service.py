from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsError


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def signup(self, name: str, email: str, password: str) -> tuple[dict, str]:
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise EmailAlreadyRegisteredError("Email already registered")
        user = await self.user_repo.create(name, email, hash_password(password))
        token = create_access_token(user.id)
        return {"id": user.id, "name": user.name, "email": user.email}, token

    async def login(self, email: str, password: str) -> tuple[dict, str]:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid email or password")
        token = create_access_token(user.id)
        return {"id": user.id, "name": user.name, "email": user.email}, token

    async def get_profile_data(self, user: User) -> dict:
        """Return profile dict with id, name, email, onboarded (business rule: onboarded = has preferences)."""
        prefs = await self.user_repo.get_preferences(user.id)
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "onboarded": prefs is not None,
        }
