"""
HealCode Cloud and Kubernetes Scanner
Detects cloud CLIs (AWS, Azure, GCP), Kubernetes kubectl config, Helm charts, and Terraform IaC settings offline.
"""

import os
import shutil
import subprocess
from typing import List, Dict, Any, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig

class CloudScanner(IScanner):
    @property
    def name(self) -> str:
        return "cloud-scanner"

    @property
    def is_global(self) -> bool:
        return True

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Audits cloud CLIs configurations, kubectl context files, Helm chart layouts, and Terraform setups."

    def __init__(self) -> None:
        self._findings: Optional[List[Dict[str, Any]]] = None
        self.cloud_data: Dict[str, Any] = {}

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        if self._findings is not None:
            return self._findings

        findings: List[Dict[str, Any]] = []
        self.cloud_data = {}

        # 1. Cloud CLIs detection
        clis = ["aws", "gcloud", "az", "terraform", "helm"]
        for cli in clis:
            self.cloud_data[cli] = {
                "installed": shutil.which(cli) is not None
            }

        # 2. Check Kubernetes config
        kubeconfig = os.path.expanduser("~/.kube/config")
        has_kubeconfig = os.path.exists(kubeconfig)
        self.cloud_data["kubeconfig_found"] = has_kubeconfig

        if shutil.which("kubectl") and not has_kubeconfig:
            findings.append({
                "id": "CLOUD-KUBE-NO-CONFIG",
                "scanner": self.name,
                "file": "kubeconfig",
                "line": 0,
                "severity": "WARN",
                "message": "kubectl CLI is installed, but ~/.kube/config is missing.",
                "fix_suggested": "Configure context credentials or log in to a Kubernetes provider."
            })

        # 3. Helm template chart detection
        for root, dirs, files in os.walk(target_path):
            if "Chart.yaml" in files:
                findings.append({
                    "id": "CLOUD-HELM-CHART-DETECTED",
                    "scanner": self.name,
                    "file": os.path.join(root, "Chart.yaml"),
                    "line": 0,
                    "severity": "INFO",
                    "message": f"Detected Helm chart configuration at: {root}",
                    "fix_suggested": "Validate chart files configuration structures using 'helm lint'."
                })

            if any(f.endswith(".tf") for f in files):
                findings.append({
                    "id": "CLOUD-IAC-TERRAFORM-DETECTED",
                    "scanner": self.name,
                    "file": root,
                    "line": 0,
                    "severity": "INFO",
                    "message": f"Detected Terraform deployment files in: {root}",
                    "fix_suggested": "Format and validate definitions with 'terraform fmt' and 'terraform validate'."
                })

        self._findings = findings
        return findings
