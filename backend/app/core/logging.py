"""
Logging configuration
Sets up structured logging for the application
"""

import logging
import sys
from typing import Any

from app.core.config import settings

def setup_logging() -> None:
    """
    Configure application logging
    """
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=settings.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module
    """
    return logging.getLogger(name)