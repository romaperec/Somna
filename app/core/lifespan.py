from contextlib import asynccontextmanager

from core.logging import setup_logging
from fastapi import FastAPI
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Initializing application components")
    yield
    logger.info("Shutting down application")
