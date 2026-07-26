"""
HealCode Environment Scanner
Discovers, parses, and compares environment configuration files for configuration drift.
"""

import os
from typing import List, Dict, Any, Set, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig

class EnvScanner(IScanner):
    @property
    def name(self) -> str:
        return "env-scanner"

    @property
    def is_global(self) -> bool:
        return True

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Checks environment configurations, missing keys, and env template mismatches."

    def __init__(self) -> None:
        self._findings: Optional[List[Dict[str, Any]]] = None

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        if self._findings is not None:
            return self._findings

        findings: List[Dict[str, Any]] = []

        env_file = os.path.join(target_path, ".env")
        env_example = os.path.join(target_path, ".env.example")

        # Check example template presence
        if os.path.exists(env_example):
            example_keys = self._parse_env_keys(env_example)
            
            if not os.path.exists(env_file):
                findings.append({
                    "id": "ENV-FILE-MISSING",
                    "scanner": self.name,
                    "file": ".env",
                    "line": 0,
                    "severity": "ERROR",
                    "message": "Local environment configuration .env file is missing, but .env.example exists.",
                    "fix_suggested": "Copy .env.example to .env and configure local secrets."
                })
            else:
                local_keys = self._parse_env_keys(env_file)
                # Compare keys
                missing_keys = example_keys - local_keys
                if missing_keys:
                    findings.append({
                        "id": "ENV-KEYS-DRIFT",
                        "scanner": self.name,
                        "file": ".env",
                        "line": 0,
                        "severity": "WARN",
                        "message": f"Configuration drift: .env is missing keys defined in .env.example: {', '.join(missing_keys)}",
                        "fix_suggested": "Synchronize .env with .env.example by adding the missing keys."
                    })
        elif os.path.exists(env_file):
            findings.append({
                "id": "ENV-EXAMPLE-MISSING",
                "scanner": self.name,
                "file": ".env.example",
                "line": 0,
                "severity": "INFO",
                "message": "Environment .env file exists, but .env.example template is missing.",
                "fix_suggested": "Create a .env.example template file to share configuration structures securely."
            })

        self._findings = findings
        return findings

    def _parse_env_keys(self, filepath: str) -> Set[str]:
        keys = set()
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key = line.split("=")[0].strip()
                        if key:
                            keys.add(key)
        except Exception:
            pass
        return keys
