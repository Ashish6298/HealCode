"""
HealCode Interfaces
Defines abstract base classes for plugins, scanners, rules, health checks, and reporters.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from healcode.config.models import ProjectConfig

class IPlugin(ABC):
    """Base interface for dynamic plugins."""
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def initialize(self, config: ProjectConfig) -> None:
        pass


class IScanner(IPlugin):
    """Interface for scanning codebases/files."""
    @property
    def is_global(self) -> bool:
        return False
    @abstractmethod
    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        """
        Runs scanner logic on target_path and returns list of findings.
        Each finding is a dict:
        {
            "id": "RULE-001",
            "scanner": "my-scanner",
            "file": "path/to/file",
            "line": 42,
            "severity": "ERROR", # INFO, WARN, ERROR
            "message": "Detailed issue description",
            "fix_suggested": "Suggested resolution"
        }
        """
        pass


class IReporter(ABC):
    """Interface for generating diagnostics reports."""
    @abstractmethod
    def generate(self, findings: List[Dict[str, Any]], system_info: Dict[str, Any]) -> None:
        """Processes and outputs findings."""
        pass
