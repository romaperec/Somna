import sys

from loguru import logger

from app.core.config import settings


def setup_logging() -> None:
    logger.remove()

    logger.add(
        sys.stdout,
        level=settings.logger.level,
        format=settings.logger.format,
        colorize=True,
    )
