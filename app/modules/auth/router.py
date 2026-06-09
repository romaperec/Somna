from fastapi import APIRouter, Depends, Response

from app.core.config import settings
from app.modules.auth.dependencies import get_auth_service
from app.modules.auth.schemas import TokenPair
from app.modules.auth.service import AuthService
from app.modules.users.schemas import UserCreate

router = APIRouter(prefix="/auth")


@router.get("/status")
def status():
    return {"status": "ok"}


@router.post("/register", response_model=TokenPair, status_code=201)
async def register(user: UserCreate, response: Response, service: AuthService = Depends(get_auth_service)):
    tokens: TokenPair = await service.register_user(user)

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.jwt.refresh_token_expire_days * 24 * 60 * 60,
    )

    return tokens
