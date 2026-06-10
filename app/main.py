from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppBaseException
from app.core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

@app.exception_handler(AppBaseException)
async def app_base_exception_handler(request: Request, exc: AppBaseException):
    return JSONResponse(status_code=exc.status_code, content={"status": "error", "message": exc.message})
