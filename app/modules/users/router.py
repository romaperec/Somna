from fastapi import APIRouter

router = APIRouter(prefix="/users")


@router.get("/status")
def status():
    return {"status": "ok"}

@router.get("/me", response_model=UserResponse)
async def get_user_profile(current_user_id: UUID = Depends(get_current_user_id), user_service: UserService = Depends(get_user_service)):
    return await user_service.get_profile(current_user_id)
