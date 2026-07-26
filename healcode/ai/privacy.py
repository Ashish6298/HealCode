"""
HealCode Privacy Masking Layer
Scrubs sensitive information before any data leaves the local machine.
"""

import re
from typing import List, Tuple


# Each entry is (compiled regex, replacement label).
_PATTERNS: List[Tuple[re.Pattern[str], str]] = [
    # API keys / tokens (generic)
    (re.compile(r"(?i)(api[_-]?key|apikey)\s*[:=]\s*\S+"), r"\1=********"),
    (re.compile(r"(?i)(secret[_-]?key|secretkey)\s*[:=]\s*\S+"), r"\1=********"),
    (re.compile(r"(?i)(access[_-]?token|accesstoken)\s*[:=]\s*\S+"), r"\1=********"),
    (re.compile(r"(?i)(bearer)\s+\S+"), r"\1 ********"),
    # Passwords
    (re.compile(r"(?i)(password|passwd|pwd)\s*[:=]\s*\S+"), r"\1=********"),
    # Connection strings
    (re.compile(r"(?i)(connection[_-]?string)\s*[:=]\s*\S+"), r"\1=********"),
    (re.compile(r"(?i)(database[_-]?url|db[_-]?url)\s*[:=]\s*\S+"), r"\1=********"),
    # SSH / private keys
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"),
     "********"),
    # AWS-style keys
    (re.compile(r"(?i)(aws[_-]?access[_-]?key[_-]?id)\s*[:=]\s*\S+"), r"\1=********"),
    (re.compile(r"(?i)(aws[_-]?secret[_-]?access[_-]?key)\s*[:=]\s*\S+"), r"\1=********"),
]


def mask_secrets(text: str) -> str:
    """Replace any detected secrets in *text* with ``********``.

    This function is applied to all data before it is sent to an
    external AI provider.  It is **not** applied when using the
    built-in ``OfflineProvider``.
    """
    result = text
    for pattern, replacement in _PATTERNS:
        result = pattern.sub(replacement, result)
    return result
