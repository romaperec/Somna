from fastapi import Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.core.security import password_service
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService


def get_cache_redis_client(request: Request) -> Redis:
    return request.app.state.cache_redis

def get_user_repository(
    session: AsyncSession = Depends(db_helper.session_getter),
    redis: Redis = Depends(get_cache_redis_client),
) -> UserRepository:
    return UserRepository(session=session, redis=redis)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(
        repo=repo,
        password_service=password_service,
    )
