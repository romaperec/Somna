from fastapi import Depends, Request
from supabase import AsyncClient

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.core.config import settings
from app.modules.storage.repository import StorageRepository
from app.modules.storage.service import StorageService


def get_supabase_client(request: Request) -> AsyncClient:
    return request.app.state.supabase_client


def get_storage_repository(
    supabase: AsyncClient = Depends(get_supabase_client),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> StorageRepository:
    return StorageRepository(supabase=supabase, session=session)


def get_storage_service(
    repo: StorageRepository = Depends(get_storage_repository),
    bucket: str = settings.storage.bucket,
    max_file_size: int = settings.storage.max_file_size,
) -> StorageService:
    return StorageService(repo=repo, bucket=bucket, max_file_size=max_file_size)
