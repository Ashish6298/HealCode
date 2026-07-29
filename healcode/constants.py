"""
HealCode Constants
"""

import os
from enum import IntEnum

# Project metadata
VERSION = "1.0.0"
APP_NAME = "HealCode"
APP_DESCRIPTION = "AI-powered developer diagnostics CLI"

# Exit codes
class ExitCode(IntEnum):
    SUCCESS = 0
    ERROR = 1
    INVALID_USAGE = 2
    CONFIG_ERROR = 3
    SCAN_FAILED = 4
    PLUGIN_ERROR = 5

# Cache Defaults
CACHE_FILE_NAME = ".healcode_cache.db"
DEFAULT_CACHE_TTL = 3600  # 1 hour in seconds
