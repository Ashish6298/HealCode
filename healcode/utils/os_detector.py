"""
HealCode OS Detector
"""

import sys
import platform
import os
from typing import Dict, Any

class OSInfo:
    def __init__(self) -> None:
        self.system: str = platform.system()
        self.release: str = platform.release()
        self.version: str = platform.version()
        self.machine: str = platform.machine()
        self.is_windows: bool = self.system == "Windows"
        self.is_mac: bool = self.system == "Darwin"
        self.is_linux: bool = self.system == "Linux"
        self.is_wsl: bool = self._detect_wsl()
        
    def _detect_wsl(self) -> bool:
        if not self.is_linux:
            return False
        # Check /proc/version or WSL_DISTRO_NAME environment variable
        if "WSL_DISTRO_NAME" in os.environ:
            return True
        try:
            with open("/proc/version", "r", encoding="utf-8") as f:
                if "microsoft" in f.read().lower():
                    return True
        except (FileNotFoundError, PermissionError):
            pass
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "system": self.system,
            "release": self.release,
            "version": self.version,
            "machine": self.machine,
            "is_windows": self.is_windows,
            "is_mac": self.is_mac,
            "is_linux": self.is_linux,
            "is_wsl": self.is_wsl,
            "friendly_name": self.friendly_name()
        }

    def friendly_name(self) -> str:
        if self.is_wsl:
            return "Linux (WSL)"
        if self.is_windows:
            return "Windows"
        if self.is_mac:
            return "macOS"
        if self.is_linux:
            return "Linux"
        return f"Unknown ({self.system})"

def get_os_info() -> OSInfo:
    return OSInfo()
