from uuid import UUID

from fastapi import APIRouter, Depends

from app.modules.auth.dependencies import get_current_user_id
from app.modules.users.dependencies import get_user_service
from app.modules.users.schemas import UserChangePassword, UserResponse, UserUpdate
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

@router.patch("/me/change-password", status_code=200)
async def change_user_password(passwords: UserChangePassword, current_user_id: UUID = Depends(get_current_user_id), user_service: UserService = Depends(get_user_service)):
    return await user_service.change_password(current_user_id, passwords)

@router.delete("/me")
async def delete_account(current_user_id: UUID = Depends(get_current_user_id), user_service: UserService = Depends(get_user_service)):
    return await user_service.delete_account(current_user_id)
