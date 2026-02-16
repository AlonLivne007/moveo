from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from app.core.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsError


async def signup(body: SignupRequest, db: AsyncSession) -> TokenResponse:
    service = AuthService(db)
    try:
        _, token = await service.signup(body.name, body.email, body.password)
        return TokenResponse(access_token=token)
    except EmailAlreadyRegisteredError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def login(body: LoginRequest, db: AsyncSession) -> TokenResponse:
    service = AuthService(db)
    try:
        _, token = await service.login(body.email, body.password)
        return TokenResponse(access_token=token)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
