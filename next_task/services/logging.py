"""Initialise logging for the package."""

import os
import sys
from pathlib import Path

from loguru import logger


def logging():
    """Instansiate the logger."""
    log_levels = [
        "DEBUG",  # diagnostics
        "INFO",  # normal opperation
        "WARNING",  # something unexpected happend
        "ERROR"  # something is broken
    ]
    logger.remove()
    logger.add(f"{Path.home()}/.local/next_task.log", level="DEBUG")
    log_level = os.getenv("LOG_LEVEL")
    if not log_level:
        logger.add(sys.stdout, level="ERROR")
    elif log_level in (log_levels):
        logger.add(sys.stdout, level=log_level)
    else:
        logger.add(sys.stdout, level="DEBUG")
        logger.warning(f"\n\tLOGGING: Misstyped environment variable\n"
                       f"\ttry one of {log_levels}\n"
                       f"\teg. export LOG_LEVEL=DEBUG\n")
