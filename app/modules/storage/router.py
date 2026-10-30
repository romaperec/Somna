from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import ValidationError

from app.modules.auth.dependencies import get_current_user_id
from app.modules.storage.dependencies import get_storage_service
from app.modules.storage.schemas import AudioCreate
from app.modules.storage.service import StorageService


router = APIRouter(prefix="/storage")


def audio_data_from_form(data: str = Form(...)) -> AudioCreate:
    try:
        return AudioCreate.model_validate_json(data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())  # noqa: B904


@router.get("/status")
def status():
    return {"status": "ok"}


@router.post("/audio/upload")
async def upload_audio(
    file: UploadFile = File(...),  # noqa: B008
    data: AudioCreate = Depends(audio_data_from_form),
    current_user_id: UUID = Depends(get_current_user_id),
    service: StorageService = Depends(get_storage_service),
):
    return await service.upload_audio(file, data, current_user_id)


@router.get("/audio/{id}")
async def get_audio_by_id(
    id: int, service: StorageService = Depends(get_storage_service)
):
    return await service.get_audio_by_id(id)


@router.delete("/audio/{id}")
async def delete_audio_by_id(
    id: int,
    current_user_id: UUID = Depends(get_current_user_id),
    service: StorageService = Depends(get_storage_service),
):
    return await service.delete_audio(id, current_user_id)


@router.get("/audio/category/{category}")
async def get_audio_by_category(
    category: str,
    limit: int = 10,
    service: StorageService = Depends(get_storage_service),
):
    return await service.get_audio_by_category(category, limit)
