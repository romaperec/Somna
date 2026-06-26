from uuid import UUID

from fastapi import APIRouter, Depends

from app.modules.auth.dependencies import get_current_user_id
from app.modules.users.dependencies import get_user_service
from app.modules.users.schemas import UserResponse
from app.modules.users.service import UserService

router = APIRouter(prefix="/users")


@router.get("/status")
def status():
    return {"status": "ok"}

@router.get("/me", response_model=UserResponse)
async def get_user_profile(current_user_id: UUID = Depends(get_current_user_id), user_service: UserService = Depends(get_user_service)):
    return await user_service.get_profile(current_user_id)

@router.patch("/me", response_model=UserResponse)
async def update_user_profile(user_data: UserUpdate, current_user_id: UUID = Depends(get_current_user_id), user_service: UserService = Depends(get_user_service)):
    return await user_service.update_profile(current_user_id, user_data)
