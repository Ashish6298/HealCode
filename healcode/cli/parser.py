"""
HealCode CLI Argument Parser
"""

import argparse
from typing import Dict
from healcode.cli.commands.base import BaseCommand
from healcode.constants import APP_NAME, APP_DESCRIPTION

def create_parser(commands: Dict[str, BaseCommand]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="healcode",
        description=f"{APP_NAME}: {APP_DESCRIPTION}",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Global arguments
    parser.add_argument("--json", action="store_true", help="Output results in machine-readable JSON format.")
    parser.add_argument("--log-level", default=None, choices=["TRACE", "DEBUG", "INFO", "WARN", "ERROR"],
                        help="Override default logging level.")

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", required=True, title="Commands", metavar="<command>")

    for command_name, cmd_obj in commands.items():
        cmd_parser = subparsers.add_parser(
            command_name,
            help=cmd_obj.description,
            description=cmd_obj.description
        )
        cmd_obj.setup_parser(cmd_parser)

    return parser
