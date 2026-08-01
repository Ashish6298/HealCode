"""
HealCode Logging Framework
Supports levels: TRACE, DEBUG, INFO, WARN, ERROR
"""

from __future__ import annotations

import logging
import sys
from typing import Any, Optional

from rich.console import Console
from rich.logging import RichHandler

# ----------------------------------------------------------------------
# Custom TRACE Level
# ----------------------------------------------------------------------

TRACE_LEVEL_NUM = 5
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")


class HealCodeLoggerImpl(logging.Logger):
    """
    Custom Logger implementation that adds TRACE support.
    """

    def trace(
        self,
        message: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if self.isEnabledFor(TRACE_LEVEL_NUM):
            self._log(TRACE_LEVEL_NUM, message, args, **kwargs)


# Register the custom logger class before any logger is created.
logging.setLoggerClass(HealCodeLoggerImpl)


class HealCodeLogger:
    """
    HealCode Logger Factory
    """

    _logger: Optional[HealCodeLoggerImpl] = None
    _console: Console = Console(stderr=True)

    @classmethod
    def setup(
        cls,
        level: str = "INFO",
        json_output: bool = False,
    ) -> HealCodeLoggerImpl:
        """
        Configure and return the HealCode logger.
        """

        level_upper = level.upper()

        if level_upper == "TRACE":
            numeric_level = TRACE_LEVEL_NUM
        elif level_upper == "DEBUG":
            numeric_level = logging.DEBUG
        elif level_upper == "INFO":
            numeric_level = logging.INFO
        elif level_upper in ("WARN", "WARNING"):
            numeric_level = logging.WARNING
        elif level_upper == "ERROR":
            numeric_level = logging.ERROR
        else:
            numeric_level = logging.INFO

        logger = logging.getLogger("healcode")

        # This should always be true because we've registered our logger class.
        assert isinstance(logger, HealCodeLoggerImpl)

        logger.setLevel(numeric_level)

        # Prevent duplicate handlers
        logger.handlers.clear()

        if json_output:
            handler = logging.StreamHandler(sys.stderr)

            formatter = logging.Formatter(
                '{"timestamp":"%(asctime)s",'
                '"name":"%(name)s",'
                '"level":"%(levelname)s",'
                '"message":"%(message)s"}'
            )

            handler.setFormatter(formatter)
            logger.addHandler(handler)

        else:
            rich_handler = RichHandler(
                console=cls._console,
                show_time=True,
                show_level=True,
                show_path=numeric_level <= logging.DEBUG,
                markup=True,
                rich_tracebacks=True,
            )

            logger.addHandler(rich_handler)

        cls._logger = logger
        return logger

    @classmethod
    def get_logger(cls) -> HealCodeLoggerImpl:
        """
        Return the configured HealCode logger.
        """

        if cls._logger is None:
            return cls.setup()

        return cls._logger