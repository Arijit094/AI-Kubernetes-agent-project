import sys

from loguru import logger


def configure_logging() -> None:
    """Configure Loguru for structured, beginner-friendly logs."""
    logger.remove()
    logger.add(
        sys.stdout,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan> - "
            "<level>{message}</level>"
        ),
        level="INFO",
    )
