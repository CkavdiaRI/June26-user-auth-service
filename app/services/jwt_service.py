from datetime import datetime, timedelta, timezone

import jwt

from app.db.models import User


class JwtService:
    def __init__(self, secret: str, expire_minutes: int):
        self.secret = secret
        self.expire_minutes = expire_minutes

    def create_token(self, user: User) -> str:
        expires = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)
        claims = {"sub": str(user.id), "role": user.role.value, "exp": expires}
        return jwt.encode(claims, self.secret, algorithm="HS256")

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, self.secret, algorithms=["HS256"], options={"require": ["exp", "sub"]})