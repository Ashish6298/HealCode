"""
HealCode Version Command
"""

import argparse
from healcode.cli.commands.base import BaseCommand
from healcode.config.models import ProjectConfig
from healcode.constants import VERSION, APP_NAME, APP_DESCRIPTION
from healcode.utils.ui import console

class VersionCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "version"

    @property
    def description(self) -> str:
        return "Print HealCode CLI version information."

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        pass

    def run(self, args: argparse.Namespace, config: ProjectConfig) -> int:
        if getattr(args, "json", False):
            import json
            print(json.dumps({"name": APP_NAME, "version": VERSION, "description": APP_DESCRIPTION}))
        else:
            console.print(f"[highlight]{APP_NAME}[/] v{VERSION} - [info]{APP_DESCRIPTION}[/]")
        return 0
