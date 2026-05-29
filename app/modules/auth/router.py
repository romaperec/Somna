from fastapi import APIRouter

router = APIRouter(prefix="/auth")


@router.get("/status")
def status():
    return {"status": "ok"}
