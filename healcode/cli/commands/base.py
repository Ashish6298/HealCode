"""
HealCode CLI Command Interface
"""

import argparse
from abc import ABC, abstractmethod
from healcode.config.models import ProjectConfig

class BaseCommand(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        pass

    @abstractmethod
    def run(self, args: argparse.Namespace, config: ProjectConfig) -> int:
        pass
