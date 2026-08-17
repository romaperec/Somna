from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppBaseException
from app.core.lifespan import lifespan
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as user_router

app = FastAPI(lifespan=lifespan, version="1.0.0")
app.include_router(auth_router)
app.include_router(user_router)

@app.exception_handler(AppBaseException)
async def app_base_exception_handler(request: Request, exc: AppBaseException):
    return JSONResponse(status_code=exc.status_code, content={"status": "error", "message": exc.message})
