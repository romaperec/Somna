from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import FastAPI
from loguru import logger

from app.core.config import settings
from app.core.logging import setup_logging

redis_pool: aioredis.BlockingConnectionPool | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_pool
    setup_logging()
    logger.info("Initializing application components")

    logger.info("Connecting to Redis")
    redis_pool = aioredis.BlockingConnectionPool(
        host=settings.redis.host,
        port=settings.redis.port,
        max_connections=settings.redis.max_connections,
        timeout=settings.redis.timeout,
        decode_responses=True,
    )

    try:
        async with aioredis.Redis(connection_pool=redis_pool) as client:
            await client.ping()
        logger.info("Redis connected successfully")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise e

    yield

    logger.info("Shutting down application")
    if redis_pool:
        logger.info("Closing redis connection pool")
        await redis_pool.disconnect()
        logger.info("Redis connection pool closed")
