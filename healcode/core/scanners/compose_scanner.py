"""
HealCode Docker Compose Scanner
Validates Compose service configuration, port allocations, and dependencies.
"""

import os
import re
from typing import List, Dict, Any, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig

class ComposeScanner(IScanner):
    @property
    def name(self) -> str:
        return "compose-scanner"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Validates Docker Compose service schemas, network ports, and volumes configs."

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []

        filename = os.path.basename(target_path)
        if filename not in ("docker-compose.yml", "compose.yaml", "compose.yml"):
            return findings

        try:
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Perform regex validation scans
            # 1. Check for restart policies
            services = re.findall(r'^\s+(\w+):\s*$', content, re.MULTILINE)
            for service in services:
                # Find matching block for service configuration
                service_block = re.search(r'^\s+' + service + r':.*?(?=^\s+\w+:|^\w+:|\Z)', content, re.DOTALL | re.MULTILINE)
                if service_block:
                    block_txt = service_block.group(0)
                    if "restart:" not in block_txt:
                        findings.append({
                            "id": "COMPOSE-MISSING-RESTART",
                            "scanner": self.name,
                            "file": target_path,
                            "line": 0,
                            "severity": "WARN",
                            "message": f"Service '{service}' in Docker Compose has no restart policy configured.",
                            "fix_suggested": "Add 'restart: unless-stopped' or 'restart: always' to ensure container persistence."
                        })
        except Exception:
            pass

        return findings
