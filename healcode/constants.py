"""
HealCode Constants
"""

import os
from enum import IntEnum

# Project metadata
VERSION = "1.2.0"
APP_NAME = "HealCode"
APP_DESCRIPTION = "A Developer Diagnostics CLI"

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
