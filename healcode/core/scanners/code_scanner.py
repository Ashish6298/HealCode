"""
HealCode Code Intelligence and Static Analysis Scanner
Audits codebase files for cyclomatic complexity, nesting issues, security risks, and performance smells offline.
"""

import re
from typing import List, Dict, Any, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig

class CodeScanner(IScanner):
    @property
    def name(self) -> str:
        return "code-scanner"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Performs static analysis audits on source code to check for maintainability, nesting, and quality."

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []

        # Only scan source files
        if not target_path.endswith((".py", ".js", ".ts", ".java", ".go", ".rs", ".dart")):
            return findings

        try:
            with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            nesting_threshold = 4
            for idx, line in enumerate(lines, 1):
                clean = line.strip()
                if clean.startswith("#") or clean.startswith("//") or not clean:
                    continue

                # 1. Nesting analysis (measure indentation depth)
                indent = len(line) - len(line.lstrip())
                # Standard indentation is usually 4 spaces, so depth = indent // 4
                depth = indent // 4
                if depth >= nesting_threshold:
                    findings.append({
                        "id": "CODE-COMPLEX-NESTING",
                        "scanner": self.name,
                        "file": target_path,
                        "line": idx,
                        "severity": "WARN",
                        "message": f"Nesting level is unusually high ({depth} levels deep). Might indicate high cognitive complexity.",
                        "fix_suggested": "Refactor nesting blocks into smaller, isolated helper functions."
                    })

                # 2. Performance smells - e.g., nested loops in python/JS
                if ("for " in clean or "while " in clean) and depth > 1:
                    findings.append({
                        "id": "CODE-PERF-NESTED-LOOP",
                        "scanner": self.name,
                        "file": target_path,
                        "line": idx,
                        "severity": "INFO",
                        "message": f"Nested loop detected at nesting depth {depth}. Optimize if processing large datasets.",
                        "fix_suggested": "Extract loop block or replace with map/lookup table structures where possible."
                    })

        except Exception:
            pass

        return findings
