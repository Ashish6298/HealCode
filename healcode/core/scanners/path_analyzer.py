"""
HealCode PATH Analyzer
Scans and analyzes system PATH variables for configurations and conflicts.
"""

import os
import sys
from typing import List, Dict, Any, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig

class PathAnalyzer(IScanner):
    @property
    def name(self) -> str:
        return "path-analyzer"

    @property
    def is_global(self) -> bool:
        return True

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Analyzes environment PATH variables for duplicate, missing, or invalid entries."

    def __init__(self) -> None:
        self._findings: Optional[List[Dict[str, Any]]] = None

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        if self._findings is not None:
            return self._findings

        # PATH analyzer runs against the system environment PATH.
        # We only run it once.
        findings: List[Dict[str, Any]] = []
        
        path_env = os.environ.get("PATH", "")
        if not path_env:
            findings.append({
                "id": "PATH-EMPTY",
                "scanner": self.name,
                "file": "PATH",
                "line": 0,
                "severity": "CRITICAL",
                "message": "Environment PATH variable is empty or not set.",
                "fix_suggested": "Configure the PATH environment variable."
            })
            return findings

        # Check total PATH length
        if len(path_env) > 2048:
            findings.append({
                "id": "PATH-TOO-LONG",
                "scanner": self.name,
                "file": "PATH",
                "line": 0,
                "severity": "WARN",
                "message": f"PATH variable is unusually long ({len(path_env)} characters). Might cause buffer limitations.",
                "fix_suggested": "Clean up unused or duplicate entries from PATH."
            })

        # Process individual path entries
        sep = ";" if sys.platform == "win32" else ":"
        entries = path_env.split(sep)
        seen = set()

        for index, entry in enumerate(entries):
            if not entry.strip():
                continue
            
            # Normalize path representation
            norm_entry = os.path.normpath(entry.strip())

            # 1. Check for duplicates
            if norm_entry.lower() in seen if sys.platform == "win32" else norm_entry in seen:
                findings.append({
                    "id": "PATH-DUPLICATE",
                    "scanner": self.name,
                    "file": "PATH",
                    "line": index + 1,
                    "severity": "INFO",
                    "message": f"Duplicate PATH entry detected: {entry}",
                    "fix_suggested": "Remove the duplicate entry."
                })
            else:
                seen.add(norm_entry.lower() if sys.platform == "win32" else norm_entry)

            # 2. Check existence
            if not os.path.exists(norm_entry):
                findings.append({
                    "id": "PATH-NONEXISTENT",
                    "scanner": self.name,
                    "file": "PATH",
                    "line": index + 1,
                    "severity": "WARN",
                    "message": f"Nonexistent directory in PATH: {entry}",
                    "fix_suggested": "Remove the dead directory entry from environment variables."
                })
            else:
                # 3. Check readability/access
                if not os.access(norm_entry, os.R_OK):
                    findings.append({
                        "id": "PATH-INACCESSIBLE",
                        "scanner": self.name,
                        "file": "PATH",
                        "line": index + 1,
                        "severity": "WARN",
                        "message": f"Inaccessible directory in PATH (no read permissions): {entry}",
                        "fix_suggested": "Correct directory permissions or remove the entry."
                    })

        # 4. Check for commonly expected directories
        if sys.platform == "win32":
            windir = os.environ.get("SystemRoot", "C:\\Windows")
            expected = [
                os.path.join(windir, "System32"),
                windir
            ]
            for exp in expected:
                if not any(exp.lower() in e.lower() for e in seen):
                    findings.append({
                        "id": "PATH-MISSING-SYSTEM",
                        "scanner": self.name,
                        "file": "PATH",
                        "line": 0,
                        "severity": "CRITICAL",
                        "message": f"Expected system directory missing from PATH: {exp}",
                        "fix_suggested": "Add the system folder back to your PATH environment variable."
                    })

        self._findings = findings
        return findings
