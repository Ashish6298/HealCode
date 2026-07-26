"""
Tests for Logging Framework
"""

import logging
from healcode.utils.logger import HealCodeLogger, TRACE_LEVEL_NUM

def test_logger_setup() -> None:
    logger = HealCodeLogger.setup(level="TRACE")
    assert logger.level == TRACE_LEVEL_NUM
    
    logger.info("Test INFO log")
    logger.debug("Test DEBUG log")
    logger.trace("Test TRACE log")  # Should not raise exception
    
    logger = HealCodeLogger.setup(level="WARN")
    assert logger.level == logging.WARNING
