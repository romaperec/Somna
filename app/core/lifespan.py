from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Initializing application components")
    yield
    logger.info("Shutting down application")
