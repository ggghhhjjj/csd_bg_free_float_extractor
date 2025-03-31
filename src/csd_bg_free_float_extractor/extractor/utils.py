"""
Utility functions for the PDF extractor.
"""

import logging
import sys


def setup_logger(name, level=logging.INFO):
    """
    Set up a logger with console output.

    Args:
        name (str): Logger name
        level (int): Logging level

    Returns:
        Logger: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Only add handler if not already added to avoid duplicates
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

    return logger