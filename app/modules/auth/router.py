from fastapi import APIRouter, Depends, Request, Response

from app.core.config import settings
from app.core.sso import google_sso
from app.modules.auth.dependencies import get_auth_service
from app.modules.auth.schemas import TokenPair, UserLogin
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
        secure=True,
        samesite="lax",
        max_age=settings.jwt.refresh_token_expire_days * 24 * 60 * 60,
    )

    return tokens

@router.post("/login", response_model=TokenPair)
async def login(user: UserLogin, response: Response, service: AuthService = Depends(get_auth_service)):
    tokens: TokenPair = await service.login_user(user)

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.jwt.refresh_token_expire_days * 24 * 60 * 60,
    )

    return tokens

@router.post("/refresh", response_model=TokenPair)
async def update_tokens(request: Request, response: Response, service: AuthService = Depends(get_auth_service)):
    refresh_token = request.cookies.get("refresh_token")
    tokens: TokenPair = await service.update_both_tokens(refresh_token)

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.jwt.refresh_token_expire_days * 24 * 60 * 60,
    )

    return tokens

@router.post("/logout")
async def logout(request: Request, response: Response, service: AuthService = Depends(get_auth_service)):
    refresh_token = request.cookies.get("refresh_token")
    await service.logout_user(refresh_token)

    response.delete_cookie(
        key="refresh_token",
        path="/",
        httponly=True,
        samesite="lax",
        secure=True,
    )


@router.get("/google/login")
async def login_by_google():
    async with google_sso as sso:
        return await sso.get_login_redirect()


@router.get("/google/callback")
async def login_by_google_callback(request: Request, response: Response, service: AuthService = Depends(get_auth_service)):
    async with google_sso as sso:
        user_data = await sso.verify_and_process(request)
    tokens: TokenPair = await service.register_or_login_user_by_oauth(user_data.email, user_data.first_name)

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.jwt.refresh_token_expire_days * 24 * 60 * 60,
    )

    return tokens
