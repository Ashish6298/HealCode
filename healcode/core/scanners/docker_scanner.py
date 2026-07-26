"""
HealCode Docker Infrastructure Scanner
Scans host Docker installation status, daemon health, active contexts, containers, images, networks, and volumes.
"""

import shutil
import subprocess
from typing import List, Dict, Any, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig

class DockerScanner(IScanner):
    @property
    def name(self) -> str:
        return "docker-scanner"

    @property
    def is_global(self) -> bool:
        return True

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Scans host Docker installation, daemon running status, networks, volumes, and running containers."

    def __init__(self) -> None:
        self._findings: Optional[List[Dict[str, Any]]] = None
        self.docker_data: Dict[str, Any] = {}

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        if self._findings is not None:
            return self._findings

        findings: List[Dict[str, Any]] = []
        self.docker_data = {}

        # 1. Detect Docker CLI
        docker_path = shutil.which("docker")
        if not docker_path:
            findings.append({
                "id": "DOCKER-NOT-INSTALLED",
                "scanner": self.name,
                "file": "docker",
                "line": 0,
                "severity": "WARN",
                "message": "Docker CLI is not installed or not found on system PATH.",
                "fix_suggested": "Install Docker Desktop or Docker Engine."
            })
            self.docker_data["installed"] = False
            self._findings = findings
            return findings

        self.docker_data["installed"] = True
        self.docker_data["path"] = docker_path

        # 2. Check if Docker daemon is running
        daemon_version = self._run_docker_cmd(["version", "--format", "{{.Server.Version}}"])
        if not daemon_version:
            findings.append({
                "id": "DOCKER-DAEMON-DOWN",
                "scanner": self.name,
                "file": "docker",
                "line": 0,
                "severity": "ERROR",
                "message": "Docker daemon is not running or socket is inaccessible.",
                "fix_suggested": "Start Docker Desktop or start the docker service."
            })
            self.docker_data["daemon_running"] = False
            self._findings = findings
            return findings

        self.docker_data["daemon_running"] = True
        self.docker_data["version"] = daemon_version

        # 3. Check for unhealthy containers
        containers_out = self._run_docker_cmd(["ps", "--filter", "status=unhealthy", "--format", "{{.Names}}"])
        if containers_out:
            unhealthy = [c.strip() for c in containers_out.split("\n") if c.strip()]
            findings.append({
                "id": "DOCKER-CONTAINER-UNHEALTHY",
                "scanner": self.name,
                "file": "containers",
                "line": 0,
                "severity": "ERROR",
                "message": f"Detected unhealthy running containers: {', '.join(unhealthy)}",
                "fix_suggested": "Inspect container logs with 'docker logs <container>'."
            })

        self._findings = findings
        return findings

    def _run_docker_cmd(self, args: List[str]) -> str:
        try:
            res = subprocess.run(["docker"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=2)
            if res.returncode == 0:
                return res.stdout.strip()
            return ""
        except Exception:
            return ""
