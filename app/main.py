from fastapi import FastAPI

from app.core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
