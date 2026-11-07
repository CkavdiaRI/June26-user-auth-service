from fastapi import FastAPI

from app.core.errors import AppError
from app.core.handlers import handle_app_error
from app.routers import auth, users

app = FastAPI(title="ShopNest User Authentication Service")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.add_exception_handler(AppError, handle_app_error)