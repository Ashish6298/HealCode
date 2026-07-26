"""
HealCode Sensitive Information Detection Scanner
Scans codebase files for exposed API keys, private keys, and credentials, outputting masked diagnostics.
"""

import os
import re
from typing import List, Dict, Any, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig

class SecretScanner(IScanner):
    @property
    def name(self) -> str:
        return "secret-scanner"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Scans files for accidentally exposed secrets and API credentials."

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []

        # Only scan source/text files
        if not target_path.endswith((".py", ".js", ".ts", ".json", ".yml", ".yaml", ".env", ".example", ".txt")):
            return findings

        # Secret detection pattern rules
        rules = {
            "SECRET-API-KEY": (r"(?i)(api[-_]?key|client[-_]?secret|private[-_]?key|token)\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{16,})['\"]", "Exposed API key or credential token."),
            "SECRET-PEM-KEY": (r"-----BEGIN [A-Z ]+ PRIVATE KEY-----", "Exposed private certificate key.")
        }

        try:
            with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
                for line_num, line in enumerate(f, 1):
                    for rule_id, (pattern, desc) in rules.items():
                        match = re.search(pattern, line)
                        if match:
                            # Safely extract line index and hide exact secret
                            matched_text = match.group(0)
                            # Mask values inside quotes or after colons
                            masked = re.sub(r"(['\"])[a-zA-Z0-9_\-]{8,}(['\"])", r"\1********\2", matched_text)
                            
                            findings.append({
                                "id": rule_id,
                                "scanner": self.name,
                                "file": target_path,
                                "line": line_num,
                                "severity": "CRITICAL",
                                "message": f"{desc} Detected pattern: {masked}",
                                "fix_suggested": "Remove the secret value immediately and rotate keys."
                            })
        except Exception:
            pass

        return findings
