import sys

from core.config import settings
from loguru import logger


def setup_logging() -> None:
    logger.remove()

    logger.add(
        sys.stdout,
        level=settings.logger.level,
        format=settings.logger.format,
        colorize=True,
    )
