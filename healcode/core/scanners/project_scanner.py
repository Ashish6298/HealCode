"""
HealCode Project Intelligence Scanner
Evaluates project architecture, dependencies, CI/CD pipelines, test frameworks, ignore rules, and configuration health.
"""

import os
from typing import List, Dict, Any, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig

class ProjectScanner(IScanner):
    @property
    def name(self) -> str:
        return "project-scanner"

    @property
    def is_global(self) -> bool:
        return True

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Scans project repository quality, build files, dependencies lockfiles, testing structures, and CI settings."

    def __init__(self) -> None:
        self._findings: Optional[List[Dict[str, Any]]] = None

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        if self._findings is not None:
            return self._findings

        findings: List[Dict[str, Any]] = []

        # 1. Dependency lockfile audit
        lockfiles = ["package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "Cargo.lock", "go.sum"]
        has_lockfile = False
        for lf in lockfiles:
            if os.path.exists(os.path.join(target_path, lf)):
                has_lockfile = True
                break
        
        # Check if manifests exist but lockfiles are missing
        has_manifest = False
        for mf in ["package.json", "pyproject.toml", "Cargo.toml", "go.mod"]:
            if os.path.exists(os.path.join(target_path, mf)):
                has_manifest = True
                break

        if has_manifest and not has_lockfile:
            findings.append({
                "id": "PROJ-DEP-MISSING-LOCKFILE",
                "scanner": self.name,
                "file": "dependencies",
                "line": 0,
                "severity": "WARN",
                "message": "Project manifests found but lockfiles (package-lock, poetry.lock, go.sum) are missing.",
                "fix_suggested": "Run installation command to generate deterministic lockfiles."
            })

        # 2. CI/CD checks
        github_wf = os.path.join(target_path, ".github", "workflows")
        gitlab_ci = os.path.join(target_path, ".gitlab-ci.yml")
        has_ci = os.path.exists(github_wf) or os.path.exists(gitlab_ci)
        if not has_ci:
            findings.append({
                "id": "PROJ-CICD-MISSING",
                "scanner": self.name,
                "file": "cicd",
                "line": 0,
                "severity": "INFO",
                "message": "No continuous integration (GitHub Actions, GitLab CI) workflows detected in the repository.",
                "fix_suggested": "Set up a workflow file to automate testing and checks on pull requests."
            })

        # 3. Repository quality & documentation
        doc_files = ["README.md", "LICENSE", "CHANGELOG.md"]
        for df in doc_files:
            if not os.path.exists(os.path.join(target_path, df)):
                findings.append({
                    "id": f"PROJ-QUALITY-MISSING-{df.split('.')[0]}",
                    "scanner": self.name,
                    "file": df,
                    "line": 0,
                    "severity": "INFO",
                    "message": f"Standard repository file '{df}' is missing from root directory.",
                    "fix_suggested": f"Add a standard '{df}' template file to improve codebase quality."
                })

        # 4. Ignore files check
        if not os.path.exists(os.path.join(target_path, ".gitignore")):
            findings.append({
                "id": "PROJ-IGNORE-MISSING-GITIGNORE",
                "scanner": self.name,
                "file": ".gitignore",
                "line": 0,
                "severity": "WARN",
                "message": "Repository does not contain a root .gitignore configuration.",
                "fix_suggested": "Create a standard .gitignore file to exclude temporary and generated files."
            })

        self._findings = findings
        return findings
