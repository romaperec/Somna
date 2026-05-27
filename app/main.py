from core.lifespan import lifespan
from fastapi import FastAPI

app = FastAPI(lifespan=lifespan)
