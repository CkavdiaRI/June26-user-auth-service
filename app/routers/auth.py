from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm


from app.core.config import settings
from app.db.database import get_db
from app.schemas.auth import Credentials, TokenOut, UserOut
from app.services.auth_service import AuthService
from app.services.jwt_service import JwtService
from app.core.security import get_auth_service



router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserOut, status_code=201, summary="Create an account")
async def signup(data: Credentials, service: AuthService = Depends(get_auth_service)):
    return await service.signup(data)

# @router.post("/login", response_model=TokenOut, summary="Login to your account")
# async def login(data: Credentials, service: AuthService = Depends(get_auth_service)):
#     token = await service.login(data)
#     return {"access_token": token}

@router.post("/login", response_model=TokenOut, summary="Login to your account")
async def login(
    form : Annotated[OAuth2PasswordRequestForm, Depends()] ,
    service: AuthService = Depends(get_auth_service),
):
    token = await service.login(form.username, form.password)
    return {"access_token": token}

