from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.core.jwt_helper import jwt_helper
from app.core.recovery_helper import recovery_helper
from app.core.security import password_service
from app.modules.auth.repository import AuthRepository
from app.modules.auth.service import AuthService
from app.modules.users.dependencies import get_user_service
from app.modules.users.service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_auth_redis_client(request: Request) -> Redis:
    return request.app.state.auth_redis

def get_auth_repository(redis: Redis = Depends(get_auth_redis_client), session: AsyncSession = Depends(db_helper.session_getter)) -> AuthRepository:
    return AuthRepository(redis=redis, session=session)

def get_auth_service(repo: AuthRepository = Depends(get_auth_repository), user_service: UserService = Depends(get_user_service)) -> AuthService:
    return AuthService(repo=repo, jwt_service=jwt_helper, user_service=user_service, password_service=password_service, recovery_helper=recovery_helper)

def get_current_user_id(token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.get_user_id_by_token(token)
