from fastapi import APIRouter

router = APIRouter(prefix="/users")


@router.get("/status")
def status():
    return {"status": "ok"}
