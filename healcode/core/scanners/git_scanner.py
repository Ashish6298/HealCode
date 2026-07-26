"""
HealCode Git and Authentication Scanner
Scans git version, local repository status, branch configuration, cleanliness, and authentication.
"""

import os
import sys
import shutil
import subprocess
from typing import List, Dict, Any, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig

class GitScanner(IScanner):
    @property
    def name(self) -> str:
        return "git-scanner"

    @property
    def is_global(self) -> bool:
        return True

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Scans local repository state, branch details, cleanliness, and authentication keys."

    def __init__(self) -> None:
        self._findings: Optional[List[Dict[str, Any]]] = None
        self.git_data: Dict[str, Any] = {}

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        if self._findings is not None:
            return self._findings

        findings: List[Dict[str, Any]] = []
        self.git_data = {}

        # 1. Detect git executable
        git_path = shutil.which("git")
        if not git_path:
            findings.append({
                "id": "GIT-NOT-INSTALLED",
                "scanner": self.name,
                "file": "git",
                "line": 0,
                "severity": "CRITICAL",
                "message": "Git is not installed or not found on PATH.",
                "fix_suggested": "Install Git and ensure it is registered on your system PATH."
            })
            self.git_data["installed"] = False
            self._findings = findings
            return findings

        self.git_data["installed"] = True
        self.git_data["path"] = git_path
        self.git_data["version"] = self._run_git_cmd(["--version"])

        # 2. Check if inside git repo
        is_repo = self._run_git_cmd(["rev-parse", "--is-inside-work-tree"], cwd=target_path) == "true"
        if not is_repo:
            findings.append({
                "id": "GIT-NOT-REPOSTORY",
                "scanner": self.name,
                "file": "git",
                "line": 0,
                "severity": "INFO",
                "message": f"Target path {target_path} is not inside a Git repository.",
                "fix_suggested": "Run 'git init' to initialize a Git repository."
            })
            self.git_data["is_repository"] = False
            self._findings = findings
            return findings

        self.git_data["is_repository"] = True
        self.git_data["branch"] = self._run_git_cmd(["rev-parse", "--abbrev-ref", "HEAD"], cwd=target_path)
        self.git_data["user_name"] = self._run_git_cmd(["config", "user.name"], cwd=target_path)
        self.git_data["user_email"] = self._run_git_cmd(["config", "user.email"], cwd=target_path)

        # 3. Check username / email configuration
        if not self.git_data["user_name"] or not self.git_data["user_email"]:
            findings.append({
                "id": "GIT-NO-USER-CONFIG",
                "scanner": self.name,
                "file": "git",
                "line": 0,
                "severity": "WARN",
                "message": "Git user.name or user.email is not configured locally or globally.",
                "fix_suggested": "Run 'git config --global user.name \"Your Name\"' and 'git config --global user.email \"your@email.com\"'."
            })

        # 4. Check repo cleanliness
        status_out = self._run_git_cmd(["status", "--porcelain"], cwd=target_path)
        self.git_data["clean"] = len(status_out) == 0
        if not self.git_data["clean"]:
            findings.append({
                "id": "GIT-REPO-DIRTY",
                "scanner": self.name,
                "file": "git",
                "line": 0,
                "severity": "INFO",
                "message": "Git repository has uncommitted, modified, or untracked changes.",
                "fix_suggested": "Commit, stash, or clean your pending changes."
            })

        # 5. Check SSH authentication keys
        ssh_dir = os.path.expanduser("~/.ssh")
        self.git_data["ssh_configured"] = False
        if os.path.exists(ssh_dir):
            for file in os.listdir(ssh_dir):
                if file in ("id_rsa", "id_ed25519", "id_ecdsa"):
                    self.git_data["ssh_configured"] = True
                    break
        
        if not self.git_data["ssh_configured"]:
            findings.append({
                "id": "GIT-AUTH-NO-SSH-KEY",
                "scanner": self.name,
                "file": "ssh",
                "line": 0,
                "severity": "WARN",
                "message": "No standard SSH private keys (id_rsa, id_ed25519) found in ~/.ssh.",
                "fix_suggested": "Generate a new SSH keypair using 'ssh-keygen -t ed25519'."
            })

        self._findings = findings
        return findings

    def _run_git_cmd(self, args: List[str], cwd: Optional[str] = None) -> str:
        try:
            res = subprocess.run(["git"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd, timeout=2)
            return res.stdout.strip()
        except Exception:
            return ""
