import asyncio
import jwt

from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import EmailTakenError, InvalidCredentialsError
from app.db.models import User
from app.schemas.auth import Credentials
from app.services.jwt_service import JwtService

hasher = PasswordHash.recommended()

class AuthService:
    def __init__(self, db: AsyncSession, jwt_service: JwtService):
        self.db = db
        self.jwt_service = jwt_service

    async def signup(self, data: Credentials) -> User:
        hashed = await asyncio.to_thread(hasher.hash, data.password)
        new_user = User(email=data.email, password_hash=hashed)
        self.db.add(new_user)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise EmailTakenError("The email is already taken.")
        
        return new_user

    async def login(self, email:str, password:str) -> str:
        result = await self.db.scalars(select(User).where(User.email == email))
        user = result.one_or_none()
        if user is None or not await asyncio.to_thread(hasher.verify, password, user.password_hash):
            raise InvalidCredentialsError("Invalid email or password.")
        return self.jwt_service.create_token(user)

    async def user_from_token(self, token: str) -> User:
        try:
            claims = self.jwt_service.decode_token(token)
        except jwt.InvalidTokenError:
            raise InvalidCredentialsError("Invalid or expired token.")
        user = await self.db.get(User, int(claims["sub"]))
        if user is None:
            raise InvalidCredentialsError("Invalid or expired token.")
        return user