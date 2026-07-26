"""
HealCode Health Engine Foundation
Provides diagnostic checks on local project environments and calculates weighted scores.
"""

import os
import sys
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from healcode.utils.os_detector import get_os_info

class HealthCheck(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """Runs the check and returns status/details."""
        pass


class PythonVersionCheck(HealthCheck):
    @property
    def name(self) -> str:
        return "Python Version Check"

    @property
    def description(self) -> str:
        return "Verifies if the current python environment is compatible (>= 3.11)."

    def run(self) -> Dict[str, Any]:
        major = sys.version_info.major
        minor = sys.version_info.minor
        passed = (major == 3 and minor >= 11) or (major > 3)
        return {
            "name": self.name,
            "status": "PASSED" if passed else "FAILED",
            "message": f"Detected Python {major}.{minor}.{sys.version_info.micro}",
            "details": {
                "version": sys.version,
                "executable": sys.executable
            }
        }


class OSCompatCheck(HealthCheck):
    @property
    def name(self) -> str:
        return "OS Compatibility Check"

    @property
    def description(self) -> str:
        return "Checks OS support compatibility."

    def run(self) -> Dict[str, Any]:
        info = get_os_info()
        supported = info.is_windows or info.is_mac or info.is_linux
        return {
            "name": self.name,
            "status": "PASSED" if supported else "WARNING",
            "message": f"Running on: {info.friendly_name()}",
            "details": info.to_dict()
        }


class HealthEngine:
    def __init__(self) -> None:
        self.checks: List[HealthCheck] = [
            PythonVersionCheck(),
            OSCompatCheck()
        ]

    def register_check(self, check: HealthCheck) -> None:
        self.checks.append(check)

    def run_diagnostics(self) -> List[Dict[str, Any]]:
        results = []
        for check in self.checks:
            try:
                results.append(check.run())
            except Exception as e:
                results.append({
                    "name": check.name,
                    "status": "ERROR",
                    "message": f"Error running check: {e}",
                    "details": {}
                })
        return results

    def calculate_score(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates a weighted health score based on scan findings.
        Returns a dictionary with scores per category and overall score.
        """
        categories = {
            "SYSTEM": 100.0,
            "HARDWARE": 100.0,
            "STORAGE": 100.0,
            "NETWORK": 100.0,
            "SHELL": 100.0,
            "ENVIRONMENT": 100.0,
            "PERFORMANCE": 100.0,
            "RUNTIME_HEALTH": 100.0,
            "TOOLCHAIN_HEALTH": 100.0,
            "PACKAGE_MANAGER_HEALTH": 100.0,
            "VERSION_COMPATIBILITY": 100.0,
            "ENV_READINESS": 100.0,
            "GIT_HEALTH": 100.0,
            "AUTHENTICATION_HEALTH": 100.0,
            "ENVIRONMENT_HEALTH": 100.0,
            "REPOSITORY_HEALTH": 100.0,
            "FRAMEWORK_READINESS": 100.0,
            "CONFIGURATION_QUALITY": 100.0,
            "SECRET_HYGIENE": 100.0,
            "DOCKER_HEALTH": 100.0,
            "CONTAINER_HEALTH": 100.0,
            "IMAGE_HEALTH": 100.0,
            "DOCKERFILE_QUALITY": 100.0,
            "COMPOSE_QUALITY": 100.0,
            "NETWORK_HEALTH": 100.0,
            "VOLUME_HEALTH": 100.0,
            "CONTAINER_SECURITY_READINESS": 100.0,
            "DOCKER_ENVIRONMENT_READINESS": 100.0,
            "PROJECT_STRUCTURE_HEALTH": 100.0,
            "DEPENDENCY_HEALTH": 100.0,
            "REPOSITORY_QUALITY": 100.0,
            "DOCUMENTATION_QUALITY": 100.0,
            "BUILD_HEALTH": 100.0,
            "TESTING_HEALTH": 100.0,
            "CICD_HEALTH": 100.0,
            "WORKSPACE_HEALTH": 100.0,
            "CONFIGURATION_HEALTH": 100.0,
            "IGNORE_FILE_HEALTH": 100.0,
            "PROJECT_MAINTAINABILITY": 100.0,
            "PROJECT_READINESS": 100.0,
            "CLOUD_CLI_HEALTH": 100.0,
            "CLOUD_AUTHENTICATION_HEALTH": 100.0,
            "CLOUD_CONFIGURATION_HEALTH": 100.0,
            "KUBERNETES_HEALTH": 100.0,
            "MANIFEST_QUALITY": 100.0,
            "HELM_HEALTH": 100.0,
            "IAC_HEALTH": 100.0,
            "CLUSTER_READINESS": 100.0,
            "DEPLOYMENT_READINESS": 100.0,
            "INFRASTRUCTURE_SECURITY": 100.0,
            "CREDENTIAL_HYGIENE": 100.0,
            "CLOUD_PROJECT_READINESS": 100.0,
            "CODE_QUALITY": 100.0,
            "MAINTAINABILITY": 100.0,
            "ARCHITECTURE_QUALITY": 100.0,
            "COMPLEXITY_HEALTH": 100.0,
            "SECURITY_ANALYSIS": 100.0,
            "PERFORMANCE_HEALTH": 100.0,
            "DOCUMENTATION_COMPLETENESS": 100.0,
            "TEST_QUALITY": 100.0,
            "TECHNICAL_DEBT": 100.0,
            "CODE_READINESS": 100.0,
            "STATIC_ANALYSIS_HEALTH": 100.0,
            "DEPENDENCY_GRAPH_HEALTH": 100.0,
            "AI_READINESS": 100.0,
            "ROOT_CAUSE_COVERAGE": 100.0,
            "RECOMMENDATION_QUALITY": 100.0
        }

        # Severity weights
        weights = {
            "CRITICAL": 30.0,
            "ERROR": 25.0,
            "WARN": 10.0,
            "WARNING": 10.0,
            "INFO": 2.0
        }

        # Deduct scores based on finding categories
        for f in findings:
            fid = f.get("id", "")
            severity = f.get("severity", "WARN").upper()
            deduction = weights.get(severity, 5.0)

            # Route findings to correct categories
            if fid.startswith("SYS-MEM") or fid.startswith("SYS-CPU"):
                categories["HARDWARE"] = max(0.0, categories["HARDWARE"] - deduction)
            elif fid.startswith("SYS-DISK"):
                categories["STORAGE"] = max(0.0, categories["STORAGE"] - deduction)
            elif fid.startswith("SYS-NET") or fid.startswith("PORT"):
                categories["NETWORK"] = max(0.0, categories["NETWORK"] - deduction)
            elif fid.startswith("PATH"):
                categories["ENVIRONMENT"] = max(0.0, categories["ENVIRONMENT"] - deduction)
            elif fid.startswith("RT-"):
                categories["RUNTIME_HEALTH"] = max(0.0, categories["RUNTIME_HEALTH"] - deduction)
                categories["TOOLCHAIN_HEALTH"] = max(0.0, categories["TOOLCHAIN_HEALTH"] - deduction)
            elif fid.startswith("COMPAT-"):
                categories["VERSION_COMPATIBILITY"] = max(0.0, categories["VERSION_COMPATIBILITY"] - deduction)
                categories["ENV_READINESS"] = max(0.0, categories["ENV_READINESS"] - deduction)
            elif fid.startswith("GIT-AUTH-"):
                categories["AUTHENTICATION_HEALTH"] = max(0.0, categories["AUTHENTICATION_HEALTH"] - deduction)
            elif fid.startswith("GIT-"):
                categories["GIT_HEALTH"] = max(0.0, categories["GIT_HEALTH"] - deduction)
                categories["REPOSITORY_HEALTH"] = max(0.0, categories["REPOSITORY_HEALTH"] - deduction)
            elif fid.startswith("ENV-"):
                categories["ENVIRONMENT_HEALTH"] = max(0.0, categories["ENVIRONMENT_HEALTH"] - deduction)
                categories["CONFIGURATION_QUALITY"] = max(0.0, categories["CONFIGURATION_QUALITY"] - deduction)
            elif fid.startswith("SECRET-"):
                categories["SECRET_HYGIENE"] = max(0.0, categories["SECRET_HYGIENE"] - deduction)
            elif fid.startswith("FW-"):
                categories["FRAMEWORK_READINESS"] = max(0.0, categories["FRAMEWORK_READINESS"] - deduction)
            elif fid.startswith("DOCKERFILE-"):
                categories["DOCKERFILE_QUALITY"] = max(0.0, categories["DOCKERFILE_QUALITY"] - deduction)
                categories["CONTAINER_SECURITY_READINESS"] = max(0.0, categories["CONTAINER_SECURITY_READINESS"] - deduction)
            elif fid.startswith("DOCKER-"):
                categories["DOCKER_HEALTH"] = max(0.0, categories["DOCKER_HEALTH"] - deduction)
                categories["DOCKER_ENVIRONMENT_READINESS"] = max(0.0, categories["DOCKER_ENVIRONMENT_READINESS"] - deduction)
            elif fid.startswith("COMPOSE-"):
                categories["COMPOSE_QUALITY"] = max(0.0, categories["COMPOSE_QUALITY"] - deduction)
            elif fid.startswith("PROJ-DEP-"):
                categories["DEPENDENCY_HEALTH"] = max(0.0, categories["DEPENDENCY_HEALTH"] - deduction)
            elif fid.startswith("PROJ-CICD-"):
                categories["CICD_HEALTH"] = max(0.0, categories["CICD_HEALTH"] - deduction)
            elif fid.startswith("PROJ-QUALITY-"):
                categories["REPOSITORY_QUALITY"] = max(0.0, categories["REPOSITORY_QUALITY"] - deduction)
                categories["DOCUMENTATION_QUALITY"] = max(0.0, categories["DOCUMENTATION_QUALITY"] - deduction)
            elif fid.startswith("PROJ-IGNORE-"):
                categories["IGNORE_FILE_HEALTH"] = max(0.0, categories["IGNORE_FILE_HEALTH"] - deduction)
            elif fid.startswith("CLOUD-KUBE-"):
                categories["KUBERNETES_HEALTH"] = max(0.0, categories["KUBERNETES_HEALTH"] - deduction)
                categories["CLUSTER_READINESS"] = max(0.0, categories["CLUSTER_READINESS"] - deduction)
            elif fid.startswith("CLOUD-HELM-"):
                categories["HELM_HEALTH"] = max(0.0, categories["HELM_HEALTH"] - deduction)
                categories["CLOUD_PROJECT_READINESS"] = max(0.0, categories["CLOUD_PROJECT_READINESS"] - deduction)
            elif fid.startswith("CLOUD-IAC-"):
                categories["IAC_HEALTH"] = max(0.0, categories["IAC_HEALTH"] - deduction)
            elif fid.startswith("CODE-COMPLEX-"):
                categories["CODE_QUALITY"] = max(0.0, categories["CODE_QUALITY"] - deduction)
                categories["COMPLEXITY_HEALTH"] = max(0.0, categories["COMPLEXITY_HEALTH"] - deduction)
                categories["STATIC_ANALYSIS_HEALTH"] = max(0.0, categories["STATIC_ANALYSIS_HEALTH"] - deduction)
            elif fid.startswith("CODE-PERF-"):
                categories["PERFORMANCE_HEALTH"] = max(0.0, categories["PERFORMANCE_HEALTH"] - deduction)
            else:
                categories["SYSTEM"] = max(0.0, categories["SYSTEM"] - deduction)

        # Average score
        overall = sum(categories.values()) / len(categories)

        return {
            "overall": round(overall, 2),
            "categories": {k: round(v, 2) for k, v in categories.items()}
        }
