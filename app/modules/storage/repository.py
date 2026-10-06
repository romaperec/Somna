from io import BufferedReader
from typing import Any
from sqlalchemy import select
from storage3.types import (
    CreateOrUpdateBucketOptions,
    FileOptions,
    URLOptions,
    UploadResponse,
)

from supabase import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.storage.models import Audio


class StorageRepository:
    def __init__(self, supabase: AsyncClient, session: AsyncSession):
        self.supabase = supabase
        self.session = session

    async def create_bucket(
        self, bucket_name: str, options: CreateOrUpdateBucketOptions | None = None
    ) -> dict[str, str]:
        return await self.supabase.storage.create_bucket(bucket_name, options)

    async def delete_bucket(self, bucket_name: str) -> dict[str, str]:
        return await self.supabase.storage.delete_bucket(bucket_name)

    async def upload_file(
        self,
        bucket_name: str,
        path: str,
        file: BufferedReader,
        file_options: FileOptions | None = None,
    ) -> UploadResponse:
        return await self.supabase.storage.from_(bucket_name).upload(
            path, file, file_options
        )

    async def delete_files(
        self, bucket_name: str, paths: list[str]
    ) -> list[dict[str, Any]]:
        return await self.supabase.storage.from_(bucket_name).remove(paths)

    async def get_public_url(
        self, bucket_name: str, path: str, options: URLOptions | None = None
    ) -> str:
        return await self.supabase.storage.from_(bucket_name).get_public_url(
            path, options
        )

    async def get_audio_by_id(self, id: int) -> Audio | None:
        audio = await self.session.execute(select(Audio).where(Audio.id == id))
        audio = audio.scalar_one_or_none()
        return audio

    async def get_audio_by_category(self, category: str, limit: int) -> list[Audio]:
        audios = await self.session.execute(
            select(Audio).where(Audio.category == category).limit(limit)
        )
        audios = audios.scalars().all()
        return audios

    async def upload_audio(self, audio_data: dict) -> Audio:
        new_audio = Audio(**audio_data)

        self.session.add(new_audio)
        await self.session.commit()

        await self.session.refresh(new_audio)

        return new_audio

    async def delete_audio(self, audio: Audio) -> bool:
        await self.session.delete(audio)
        await self.session.commit()
        return True
