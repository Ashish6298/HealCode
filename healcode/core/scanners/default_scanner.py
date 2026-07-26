"""
HealCode Built-in Default Scanner
"""

import os
from typing import List, Dict, Any
from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig

class DefaultScanner(IScanner):
    @property
    def name(self) -> str:
        return "default-scanner"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Built-in default scanner to check for common codebase issues."

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []
        if not os.path.exists(target_path):
            return findings

        # 1. Check for abnormally large files
        try:
            size = os.path.getsize(target_path)
            if size > 10 * 1024 * 1024:  # > 10MB
                findings.append({
                    "id": "LARGE-FILE",
                    "scanner": self.name,
                    "file": target_path,
                    "line": 0,
                    "severity": "WARN",
                    "message": f"Large file detected ({size / (1024 * 1024):.2f} MB). Consider adding to gitignore.",
                    "fix_suggested": "Compress, remove, or add to gitignore."
                })
        except Exception:
            pass

        # 2. Check for TODOs in source files
        if target_path.endswith((".py", ".js", ".ts", ".html", ".css", ".md", ".json")):
            try:
                with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        if "TODO" in line:
                            findings.append({
                                "id": "TODO-FOUND",
                                "scanner": self.name,
                                "file": target_path,
                                "line": line_num,
                                "severity": "INFO",
                                "message": f"TODO found: {line.strip()}",
                                "fix_suggested": "Resolve the TODO item."
                            })
            except Exception:
                pass

        return findings
