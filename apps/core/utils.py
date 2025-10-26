"""
Common utility functions
"""
import logging

logger = logging.getLogger(__name__)


def log_info(message):
    """Log informational messages"""
    logger.info(message)


def log_error(message):
    """Log error messages"""
    logger.error(message)


def log_warning(message):
    """Log warning messages"""
    logger.warning(message)

