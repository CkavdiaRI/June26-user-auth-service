from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_db
from app.db.models import User
from app.services.auth_service import AuthService
from app.services.jwt_service import JwtService
from app.core.errors import InvalidCredentialsError



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    jwt_service = JwtService(secret=settings.jwt_secret, expire_minutes=settings.jwt_expire_minutes)
    return AuthService(db, jwt_service)

async def get_current_user(token: str = Depends(oauth2_scheme), service: AuthService = Depends(get_auth_service)) -> User:
    if token is None:
        raise InvalidCredentialsError("Not authenticated")
    return service.user_from_token(token)