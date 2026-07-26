"""
HealCode Dockerfile Best Practices Scanner
Parses Dockerfiles and flags anti-patterns (latest tags, missing healthchecks, root executions).
"""

import os
import re
from typing import List, Dict, Any, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig

class DockerfileScanner(IScanner):
    @property
    def name(self) -> str:
        return "dockerfile-scanner"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Scans Dockerfile configurations for security, layer optimization, and standard best practices."

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []

        filename = os.path.basename(target_path)
        if not (filename.startswith("Dockerfile") or filename.endswith(".dockerfile")):
            return findings

        try:
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.splitlines()
            has_healthcheck = False
            has_user = False

            for idx, line in enumerate(lines, 1):
                clean_line = line.strip()
                if clean_line.startswith("#") or not clean_line:
                    continue

                # 1. Check for latest tag usage
                if clean_line.startswith("FROM"):
                    if ":latest" in clean_line or (":" not in clean_line and "@" not in clean_line):
                        findings.append({
                            "id": "DOCKERFILE-LATEST-TAG",
                            "scanner": self.name,
                            "file": target_path,
                            "line": idx,
                            "severity": "WARN",
                            "message": f"Avoid using 'latest' or unpinned version tag in base image: {clean_line}",
                            "fix_suggested": "Pin base images to a specific version or hash digest."
                        })

                if clean_line.startswith("HEALTHCHECK"):
                    has_healthcheck = True
                
                if clean_line.startswith("USER"):
                    has_user = True

            # 2. Check for missing healthcheck
            if not has_healthcheck:
                findings.append({
                    "id": "DOCKERFILE-MISSING-HEALTHCHECK",
                    "scanner": self.name,
                    "file": target_path,
                    "line": 0,
                    "severity": "INFO",
                    "message": "Dockerfile does not contain a HEALTHCHECK instruction.",
                    "fix_suggested": "Add a HEALTHCHECK command to allow Docker engine to verify service status dynamically."
                })

            # 3. Check for root execution warning
            if not has_user:
                findings.append({
                    "id": "DOCKERFILE-RUNS-AS-ROOT",
                    "scanner": self.name,
                    "file": target_path,
                    "line": 0,
                    "severity": "WARN",
                    "message": "No non-root USER instruction configured in Dockerfile. Container will default to root execution.",
                    "fix_suggested": "Configure a non-root USER mapping to secure runtime execution privileges."
                })

        except Exception:
            pass

        return findings
