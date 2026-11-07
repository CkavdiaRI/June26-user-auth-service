from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.errors import AppError


async def handle_app_error(request: Request, exc: AppError):
    body = {"error": {"code": exc.status_code, "message": str(exc)}}
    headers = {"WWW-Authenticate": "Bearer"} if exc.status_code == 401 else None
    return JSONResponse(status_code=exc.status_code, content=body, headers=headers)
