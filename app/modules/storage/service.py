from pathlib import Path
import uuid

from fastapi import UploadFile

from app.modules.storage.repository import StorageRepository
from app.modules.storage.exceptions import (
    FileTooLargeException,
    InvalidFileTypeException,
    FileNotFoundException,
    PermissionDeniedException,
)
from app.modules.storage.schemas import AudioCreate


class StorageService:
    def __init__(self, repo: StorageRepository, bucket: str, max_file_size: int):
        self.repo = repo
        self.bucket = bucket
        self.max_file_size = max_file_size

    async def get_audio_by_id(self, id: int):
        audio = await self.repo.get_audio_by_id(id)
        if audio is None:
            raise FileNotFoundException
        audio = await self.repo.get_public_url(
            self.bucket, f"audio/{audio.unique_filename}"
        )
        return audio

    async def get_audio_by_category(self, category: str, limit: int):
        audios = await self.repo.get_audio_by_category(category, limit)
        return audios

    async def delete_audio(self, id: int, user_id: uuid.UUID):
        audio = await self.repo.get_audio_by_id(id)
        if not audio:
            raise FileNotFoundException

        if audio.user_id != user_id:
            raise PermissionDeniedException

        await self.repo.delete_files(self.bucket, [f"audio/{audio.unique_filename}"])
        return await self.repo.delete_audio(audio)

    async def upload_audio(
        self, file: UploadFile, schema: AudioCreate, user_id: uuid.UUID
    ):
        if not file.content_type.startswith("audio/"):
            raise InvalidFileTypeException

        if file.size is not None and file.size > self.max_file_size:
            raise FileTooLargeException

        unique_name = self._generate_unique_filename(file.filename)
        audio_data = schema.model_dump()
        audio_data["original_filename"] = file.filename
        audio_data["unique_filename"] = unique_name
        audio_data["path"] = f"audio/{unique_name}"
        audio_data["user_id"] = user_id

        await self.repo.upload_audio(audio_data)
        return await self.repo.upload_file(self.bucket, f"audio/{unique_name}", file.file)

    def _generate_unique_filename(self, original_filename: str) -> str:
        file_extension = Path(original_filename).suffix

        unique_name = f"{uuid.uuid4()}{file_extension}"
        return unique_name
