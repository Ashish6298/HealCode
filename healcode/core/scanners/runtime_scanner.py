"""
HealCode Runtime Scanner
Detects and analyzes installed language runtimes, package managers, and version managers.
"""

import os
import sys
import subprocess
import shutil
from typing import List, Dict, Any, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig

class RuntimeScanner(IScanner):
    @property
    def name(self) -> str:
        return "runtime-scanner"

    @property
    def is_global(self) -> bool:
        return True

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Detects installed language runtimes, package managers, and version managers."

    def __init__(self) -> None:
        self._findings: Optional[List[Dict[str, Any]]] = None
        self.runtimes_data: Dict[str, Any] = {}

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        if self._findings is not None:
            return self._findings

        findings: List[Dict[str, Any]] = []
        self.runtimes_data = {}

        # 1. List of runtimes to check
        runtimes_to_check = {
            "node": ["node", "--version"],
            "python": ["python", "--version"],
            "java": ["java", "-version"],
            "go": ["go", "version"],
            "rust": ["rustc", "--version"],
            "dart": ["dart", "--version"],
            "flutter": ["flutter", "--version"]
        }

        for name, cmd in runtimes_to_check.items():
            exe_path = shutil.which(cmd[0])
            if exe_path:
                version = self._get_version_output(cmd)
                self.runtimes_data[name] = {
                    "installed": True,
                    "path": exe_path,
                    "version": version
                }
            else:
                self.runtimes_data[name] = {"installed": False}

        # 2. List of package managers to check
        package_managers = {
            "npm": ["npm", "--version"],
            "yarn": ["yarn", "--version"],
            "pnpm": ["pnpm", "--version"],
            "bun": ["bun", "--version"],
            "pip": ["pip", "--version"],
            "poetry": ["poetry", "--version"],
            "cargo": ["cargo", "--version"]
        }

        for name, cmd in package_managers.items():
            exe_path = shutil.which(cmd[0])
            if exe_path:
                version = self._get_version_output(cmd)
                self.runtimes_data[name] = {
                    "installed": True,
                    "path": exe_path,
                    "version": version
                }
            else:
                self.runtimes_data[name] = {"installed": False}

        # 3. Check for version managers
        version_managers = {
            "nvm": ["nvm", "--version"],
            "fnm": ["fnm", "--version"],
            "pyenv": ["pyenv", "--version"],
            "rustup": ["rustup", "--version"]
        }
        for name, cmd in version_managers.items():
            exe_path = shutil.which(cmd[0])
            if exe_path:
                version = self._get_version_output(cmd)
                self.runtimes_data[name] = {
                    "installed": True,
                    "path": exe_path,
                    "version": version
                }
            else:
                self.runtimes_data[name] = {"installed": False}

        # Generate findings for missing key toolchains if we are in a targeted dev environment
        # (e.g. if we detect missing runtime managers or broken environments)
        if not self.runtimes_data.get("node", {}).get("installed", False) and not self.runtimes_data.get("python", {}).get("installed", False):
            findings.append({
                "id": "RT-NO-COMMON-RUNTIMES",
                "scanner": self.name,
                "file": "runtimes",
                "line": 0,
                "severity": "WARN",
                "message": "Neither Node.js nor Python runtimes were detected on this machine.",
                "fix_suggested": "Install Python or Node.js to begin software development."
            })

        self._findings = findings
        return findings

    def _get_version_output(self, cmd: List[str]) -> str:
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=2)
            out = (res.stdout or res.stderr or "").strip()
            # Clean up output e.g. "Python 3.11.4" -> "3.11.4"
            if "version" in out.lower():
                # Extract first word resembling version
                for part in out.split():
                    if any(char.isdigit() for char in part):
                        return part.strip("v").strip()
            return out.split("\n")[0].strip()
        except Exception:
            return "unknown"
