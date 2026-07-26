"""
HealCode Project Framework Detection Scanner
Detects active development frameworks, monorepos, and build configurations.
"""

import os
import json
import re
from typing import List, Dict, Any, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig

class FrameworkScanner(IScanner):
    @property
    def name(self) -> str:
        return "framework-scanner"

    @property
    def is_global(self) -> bool:
        return True

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Detects project development frameworks, package layouts, and build settings."

    def __init__(self) -> None:
        self._findings: Optional[List[Dict[str, Any]]] = None
        self.frameworks: List[str] = []

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        if self._findings is not None:
            return self._findings

        findings: List[Dict[str, Any]] = []
        self.frameworks = []

        # 1. Check Node.js framework manifest
        pkg_json_path = os.path.join(target_path, "package.json")
        if os.path.exists(pkg_json_path):
            try:
                with open(pkg_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    deps = data.get("dependencies", {})
                    dev_deps = data.get("devDependencies", {})
                    all_deps = {**deps, **dev_deps}

                    # Detect specific Node.js frameworks
                    for fw in ["next", "react", "vue", "nuxt", "angular", "svelte", "astro", "express", "nestjs"]:
                        if fw in all_deps:
                            self.frameworks.append(fw.capitalize())
            except Exception:
                pass

        # 2. Check Python framework manifests
        pyproject_path = os.path.join(target_path, "pyproject.toml")
        if os.path.exists(pyproject_path):
            try:
                with open(pyproject_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    for fw in ["fastapi", "django", "flask", "poetry", "uv"]:
                        if re.search(r'\b' + fw + r'\b', content, re.IGNORECASE):
                            self.frameworks.append(fw.capitalize())
            except Exception:
                pass

        # Report findings summarizing the active frameworks
        if self.frameworks:
            findings.append({
                "id": "FW-DETECTED",
                "scanner": self.name,
                "file": "frameworks",
                "line": 0,
                "severity": "INFO",
                "message": f"Detected project framework toolchains: {', '.join(self.frameworks)}",
                "fix_suggested": "Ensure environment satisfies framework-specific versions."
            })
        else:
            findings.append({
                "id": "FW-NONE-DETECTED",
                "scanner": self.name,
                "file": "frameworks",
                "line": 0,
                "severity": "INFO",
                "message": "No specific framework manifests detected in target directory.",
                "fix_suggested": "Setup a standard layout package.json or pyproject.toml if applicable."
            })

        self._findings = findings
        return findings
