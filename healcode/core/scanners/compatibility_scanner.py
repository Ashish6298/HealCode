"""
HealCode Runtime Compatibility Engine
Parses project manifests and flags mismatches against installed host runtimes.
"""

import os
import json
import re
from typing import List, Dict, Any, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig
from healcode.core.scanners.runtime_scanner import RuntimeScanner

class CompatibilityScanner(IScanner):
    @property
    def name(self) -> str:
        return "compatibility-scanner"

    @property
    def is_global(self) -> bool:
        return True

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Checks mismatch between installed toolchains and project manifest definitions."

    def __init__(self, runtime_scanner: Optional[RuntimeScanner] = None) -> None:
        self.runtime_scanner = runtime_scanner
        self._findings: Optional[List[Dict[str, Any]]] = None

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        # This scanner targets project configuration files within target_path.
        # We search for manifests and match them against installed versions.
        findings: List[Dict[str, Any]] = []

        # Find or run RuntimeScanner to get installed runtimes
        installed_runtimes: Dict[str, Any] = {}
        if self.runtime_scanner:
            self.runtime_scanner.scan(target_path)
            installed_runtimes = self.runtime_scanner.runtimes_data

        # 1. Parse package.json
        pkg_json_path = os.path.join(target_path, "package.json")
        if os.path.exists(pkg_json_path):
            try:
                with open(pkg_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    engines = data.get("engines", {})
                    node_req = engines.get("node")
                    if node_req:
                        findings.extend(self._verify_node_version(node_req, installed_runtimes, pkg_json_path))
            except Exception:
                pass

        # 2. Parse pyproject.toml
        pyproject_path = os.path.join(target_path, "pyproject.toml")
        if os.path.exists(pyproject_path):
            try:
                with open(pyproject_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Simple regex matching requires-python or python version constraints
                    match = re.search(r'requires-python\s*=\s*"(.*?)"', content)
                    if match:
                        py_req = match.group(1)
                        findings.extend(self._verify_python_version(py_req, installed_runtimes, pyproject_path))
            except Exception:
                pass

        return findings

    def _clean_version(self, version_str: str) -> str:
        match = re.search(r'(\d+\.\d+(?:\.\d+)?)', version_str)
        return match.group(1) if match else version_str.strip().lstrip("v")

    def _verify_node_version(self, req: str, runtimes: Dict[str, Any], path: str) -> List[Dict[str, Any]]:
        findings = []
        node_info = runtimes.get("node", {})
        if not node_info.get("installed", False):
            findings.append({
                "id": "COMPAT-NODE-MISSING",
                "scanner": self.name,
                "file": path,
                "line": 0,
                "severity": "CRITICAL",
                "message": f"Project requires Node.js {req}, but Node.js is not installed on the system.",
                "fix_suggested": "Install the specified Node.js version."
            })
            return findings

        raw_version = node_info.get("version", "")
        installed_version = self._clean_version(raw_version)
        
        # Basic semver comparison fallback (simple version checks)
        clean_req = self._clean_version(req)
        if clean_req and installed_version:
            # check major compatibility
            req_major = clean_req.split(".")[0]
            inst_major = installed_version.split(".")[0]
            if req_major.isdigit() and inst_major.isdigit() and int(inst_major) < int(req_major):
                findings.append({
                    "id": "COMPAT-NODE-MISMATCH",
                    "scanner": self.name,
                    "file": path,
                    "line": 0,
                    "severity": "ERROR",
                    "message": f"Project requires Node.js {req}, but installed version is older: v{installed_version}",
                    "fix_suggested": f"Upgrade Node.js to match constraints: {req}"
                })
        return findings

    def _verify_python_version(self, req: str, runtimes: Dict[str, Any], path: str) -> List[Dict[str, Any]]:
        findings = []
        py_info = runtimes.get("python", {})
        if not py_info.get("installed", False):
            findings.append({
                "id": "COMPAT-PYTHON-MISSING",
                "scanner": self.name,
                "file": path,
                "line": 0,
                "severity": "CRITICAL",
                "message": f"Project requires Python {req}, but Python is not installed on the system.",
                "fix_suggested": "Install Python matching project constraints."
            })
            return findings

        raw_version = py_info.get("version", "")
        installed_version = self._clean_version(raw_version)
        clean_req = self._clean_version(req)
        if clean_req and installed_version:
            req_parts = [int(p) for p in clean_req.split(".") if p.isdigit()]
            inst_parts = [int(p) for p in installed_version.split(".") if p.isdigit()]
            if req_parts and inst_parts and inst_parts[:len(req_parts)] < req_parts:
                findings.append({
                    "id": "COMPAT-PYTHON-MISMATCH",
                    "scanner": self.name,
                    "file": path,
                    "line": 0,
                    "severity": "ERROR",
                    "message": f"Project requires Python {req}, but installed version is older: v{installed_version}",
                    "fix_suggested": f"Upgrade Python version to satisfy constraints: {req}"
                })
        return findings
