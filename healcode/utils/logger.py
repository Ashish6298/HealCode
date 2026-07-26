"""
HealCode Logging Framework
Supports levels: INFO, WARN, ERROR, DEBUG, TRACE
"""

import logging
import sys
from typing import Any, Dict, Optional
from rich.console import Console
from rich.logging import RichHandler

# Define TRACE level (below DEBUG)
TRACE_LEVEL_NUM = 5
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")

def trace(self: logging.Logger, message: str, *args: Any, **kws: Any) -> None:
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, message, args, **kws)

# Bind trace method to Logger class
logging.Logger.trace = trace  # type: ignore

class HealCodeLogger:
    _logger: Optional[logging.Logger] = None
    _console: Console = Console(stderr=True)

    @classmethod
    def setup(cls, level: str = "INFO", json_output: bool = False) -> logging.Logger:
        numeric_level = logging.INFO
        level_upper = level.upper()
        if level_upper == "TRACE":
            numeric_level = TRACE_LEVEL_NUM
        elif level_upper == "DEBUG":
            numeric_level = logging.DEBUG
        elif level_upper == "INFO":
            numeric_level = logging.INFO
        elif level_upper == "WARN" or level_upper == "WARNING":
            numeric_level = logging.WARNING
        elif level_upper == "ERROR":
            numeric_level = logging.ERROR

        logger = logging.getLogger("healcode")
        logger.setLevel(numeric_level)
        # Clear existing handlers
        logger.handlers.clear()

        if json_output:
            # JSON format or simple stream format
            handler = logging.StreamHandler(sys.stderr)
            formatter = logging.Formatter(
                '{"timestamp":"%(asctime)s", "name":"%(name)s", "level":"%(levelname)s", "message":"%(message)s"}'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        else:
            # Rich handler for beautiful console output
            rich_handler = RichHandler(
                console=cls._console,
                show_time=True,
                show_level=True,
                show_path=numeric_level <= logging.DEBUG,
                markup=True,
                rich_tracebacks=True
            )
            logger.addHandler(rich_handler)

        cls._logger = logger
        return logger

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._logger is None:
            return cls.setup()
        return cls._logger
