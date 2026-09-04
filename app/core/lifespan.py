from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from redis.asyncio import BlockingConnectionPool, Redis

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.tasks import broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Initializing application components")

    cache_pool = BlockingConnectionPool(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db_cache,
        max_connections=settings.redis.max_connections,
        timeout=settings.redis.timeout,
        decode_responses=True,
    )
    cache_redis = Redis(connection_pool=cache_pool)

    auth_pool = BlockingConnectionPool(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db_auth,
        max_connections=settings.redis.max_connections,
        timeout=settings.redis.timeout,
        decode_responses=True,
    )
    auth_redis = Redis(connection_pool=auth_pool)

    try:
        await cache_redis.ping()
        logger.info(f"Redis cache connected. DB {settings.redis.db_cache}")

        await auth_redis.ping()
        logger.info(f"Redis auth connected. DB {settings.redis.db_auth}")

        logger.info("Connecting to NATS JetStream broker")
        await broker.startup()
        logger.info("NATS JetStream broker started successfully")

    except Exception as e:
        logger.critical(f"Failed to connect to Redis: {e}")
        await cache_pool.disconnect()
        await auth_pool.disconnect()
        raise e

    app.state.cache_redis = cache_redis
    app.state.auth_redis = auth_redis

    yield

    logger.info("Shutting down application")

    logger.info("Closing NATS JetStream broker connection")
    await broker.shutdown()
    logger.info("NATS JetStream broker connection closed successfully")

    logger.info("Closing redis client and connection pool")

    await cache_redis.aclose()
    await cache_pool.disconnect()

    await auth_redis.aclose()
    await auth_pool.disconnect()

    logger.info("Redis connections closed successfully")
    logger.info("All connections closed successfully")
