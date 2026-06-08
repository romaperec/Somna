from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from redis.asyncio import BlockingConnectionPool, Redis

from app.core.config import settings
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Initializing application components")

    logger.info("Connecting to Redis")
    redis_pool = BlockingConnectionPool(
        host=settings.redis.host,
        port=settings.redis.port,
        max_connections=settings.redis.max_connections,
        timeout=settings.redis.timeout,
        decode_responses=True,
    )
    redis_client = Redis(connection_pool=redis_pool, db=settings.redis.db_cache)

    try:
        await redis_client.ping()
        logger.info(f"Redis connected successfully. DB {settings.redis.db_cache}")
    except Exception as e:
        logger.critical(f"Failed to connect to Redis: {e}")
        await redis_pool.disconnect()
        raise e

    app.state.redis = redis_client

    yield

    logger.info("Shutting down application")
    if redis_pool:
        logger.info("Closing redis client and connection pool")
        await redis_client.aclose()
        await redis_pool.disconnect()
        logger.info("Redis connections closed successfully")
