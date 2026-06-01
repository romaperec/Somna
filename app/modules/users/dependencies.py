from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.core.security import password_service
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService


def get_user_repository(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserRepository:
    return UserRepository(session=session)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(
        repo=repo,
        password_service=password_service,
    )
