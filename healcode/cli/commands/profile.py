"""
HealCode Profile Command
"""

import argparse
import os
from healcode.cli.commands.base import BaseCommand
from healcode.config.models import ProjectConfig
from healcode.config.manager import ConfigManager
from healcode.core.profiles import PROFILES
from healcode.utils.ui import console, print_success, print_info, print_error

class ProfileCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "profile"

    @property
    def description(self) -> str:
        return "Manage diagnostics scanning profiles."

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        subparsers = parser.add_subparsers(dest="profile_action", required=True)
        subparsers.add_parser("list", help="List all predefined diagnostic profiles.")
        subparsers.add_parser("show", help="Display the active diagnostics profile.")
        
        set_parser = subparsers.add_parser("set", help="Set the active diagnostics profile.")
        set_parser.add_argument("profile_name", help="The name of the profile to set (e.g., DevOps, Security, Minimal, Full).")

    def run(self, args: argparse.Namespace, config: ProjectConfig) -> int:
        manager = ConfigManager()

        if args.profile_action == "list":
            console.print("[bold cyan]Available Scanning Profiles:[/bold cyan]\n")
            for name, scanners in PROFILES.items():
                scanner_list = ", ".join(scanners) if scanners else "All Scanners"
                console.print(f" - [bold green]{name:12}[/] : {scanner_list}")
            return 0

        elif args.profile_action == "show":
            active = config.scan.profile or "Full"
            console.print(f"Current active scanning profile: [bold green]{active}[/bold green]")
            return 0

        elif args.profile_action == "set":
            pname = args.profile_name
            matching_key = None
            for key in PROFILES:
                if key.lower() == pname.lower():
                    matching_key = key
                    break

            if not matching_key:
                print_error(f"Invalid profile name: {pname}. Available: {', '.join(PROFILES.keys())}")
                return 1

            config.scan.profile = matching_key
            manager.config = config
            manager.save_project_config()
            print_success(f"Successfully set active diagnostics profile to: [bold green]{matching_key}[/bold green]")
            return 0

        return 1
