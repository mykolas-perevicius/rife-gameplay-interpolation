"""Logging configuration with Loguru."""

import sys
from pathlib import Path

from loguru import logger

# Remove default handler
logger.remove()

# Custom log object with convenient methods
class Log:
    """Wrapper for logger with convenient methods."""
    
    def __init__(self):
        self._logger = logger
    
    def debug(self, msg): self._logger.debug(msg)
    def info(self, msg): self._logger.info(msg)
    def warning(self, msg): self._logger.warning(msg)
    def error(self, msg): self._logger.error(msg)
    def success(self, msg): self._logger.success(msg)

log = Log()

def setup_logger(verbose: bool = False):
    """Configure logging."""
    # Console output
    level = "DEBUG" if verbose else "INFO"
    
    logger.add(
        sys.stderr,
        format="<dim>{time:HH:mm:ss}</dim> | <level>{level: <8}</level> | {message}",
        level=level,
        colorize=True
    )
    
    # File output
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger.add(
        log_dir / "rife_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        level="DEBUG",
        rotation="1 day",
        retention="7 days"
    )
