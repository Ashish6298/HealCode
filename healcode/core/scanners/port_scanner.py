"""
HealCode Port Scanner
Detects active development ports and potential collisions.
"""

import socket
from typing import List, Dict, Any, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig

class PortScanner(IScanner):
    DEFAULT_DEV_PORTS = [3000, 5000, 5173, 8000, 8080, 9000]

    @property
    def name(self) -> str:
        return "port-scanner"

    @property
    def is_global(self) -> bool:
        return True

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Checks active development ports for conflicts and processes."

    def __init__(self) -> None:
        self._findings: Optional[List[Dict[str, Any]]] = None

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        if self._findings is not None:
            return self._findings

        # Scan commonly used dev ports on localhost.
        findings: List[Dict[str, Any]] = []

        for port in self.DEFAULT_DEV_PORTS:
            if self._is_port_open("127.0.0.1", port):
                findings.append({
                    "id": f"PORT-CONFLICT-{port}",
                    "scanner": self.name,
                    "file": f"port:{port}",
                    "line": 0,
                    "severity": "WARN",
                    "message": f"Port {port} is currently active and listening on localhost.",
                    "fix_suggested": f"Check if another process/app is running on port {port} or free up the port."
                })

        self._findings = findings
        return findings

    def _is_port_open(self, host: str, port: int) -> bool:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        try:
            s.connect((host, port))
            s.close()
            return True
        except Exception:
            return False
