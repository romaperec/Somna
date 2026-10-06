from pathlib import Path
import uuid

from fastapi import UploadFile

from app.modules.storage.repository import StorageRepository
from app.modules.storage.exceptions import (
    InvalidFileTypeException,
    FileNotFound,
    PermissionDenied,
)
from app.modules.storage.schemas import AudioCreate


class StorageService:
    def __init__(self, repo: StorageRepository):
        self.repo = repo

    async def get_audio_by_id(self, id: int):
        audio = await self.repo.get_audio_by_id(id)
        if audio is None:
            raise FileNotFound
        audio = await self.repo.get_public_url(
            "files", f"audio/{audio.unique_filename}"
        )
        return audio

    async def get_audio_by_category(self, category: str, limit: int):
        audios = await self.repo.get_audio_by_category(category, limit)
        return audios

    async def delete_audio(self, id: int, user_id: uuid.UUID):
        audio = await self.repo.get_audio_by_id(id)
        if not audio:
            raise FileNotFound

        if audio.user_id != user_id:
            raise PermissionDenied

        return await self.repo.delete_audio(audio)

    async def upload_audio(
        self, file: UploadFile, schema: AudioCreate, user_id: uuid.UUID
    ):
        if not file.content_type.startswith("audio/"):
            raise InvalidFileTypeException

        unique_name = self._generate_unique_filename(file.filename)
        audio_data = schema.model_dump()
        audio_data["original_filename"] = file.filename
        audio_data["unique_filename"] = unique_name
        audio_data["path"] = f"audio/{unique_name}"
        audio_data["user_id"] = user_id

        content = await file.read()

        await self.repo.upload_audio(audio_data)
        return await self.repo.upload_file("files", f"audio/{unique_name}", content)

    def _generate_unique_filename(self, original_filename: str) -> str:
        file_extension = Path(original_filename).suffix

        unique_name = f"{uuid.uuid4()}{file_extension}"
        return unique_name
