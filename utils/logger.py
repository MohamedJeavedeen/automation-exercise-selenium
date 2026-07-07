"""
logger.py
---------
Centralized logger. Every page object and test uses get_logger(__name__)
so log lines are traceable back to the exact module that produced them.
Logs go to logs/automation.log (rotating) and also to console.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from config.config_reader import ConfigReader

_LOG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ConfigReader.get_log_dir(),
)
os.makedirs(_LOG_DIR, exist_ok=True)
_LOG_FILE = os.path.join(_LOG_DIR, "automation.log")

_FORMATTER = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        # Already configured (avoids duplicate handlers on repeated calls)
        return logger

    logger.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler(
        _LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setFormatter(_FORMATTER)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(_FORMATTER)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger
