"""
HealCode CLI Argument Parser
"""

import argparse
from typing import Dict
from healcode.cli.commands.base import BaseCommand
from healcode.constants import APP_NAME, APP_DESCRIPTION

class HealCodeArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_full_help = False
        self.json_output = False

    def format_help(self) -> str:
        if self.prog != "healcode":
            return super().format_help()
        
        if self.json_output:
            import json
            return json.dumps({
                "command": "help",
                "status": "success",
                "description": "A Developer Diagnostics CLI",
                "usage": "healcode [options] <command>",
                "commands": {
                    "scan": "Run diagnostic scans on a codebase target directory.",
                    "config": "Manage project and global HealCode configurations.",
                    "plugins": "List loaded plugins and scanners.",
                    "version": "Print HealCode CLI version information.",
                    "ai": "Run AI-powered analysis on scan findings (offline-first).",
                    "profile": "Manage diagnostics scanning profiles.",
                    "baseline": "Capture, compare, and detect configuration drift against active baselines.",
                    "watch": "Monitor directory for file changes and execute incremental scans.",
                    "marketplace": "Discover, install, update, and manage plugins from the HealCode community marketplace."
                }
            }, indent=4) + "\n"
        
        from rich.console import Console
        from rich.panel import Panel
        
        console = Console(color_system="auto")

        if self.show_full_help:
            # Options content
            options_text = (
                "[bold cyan]--json[/]            : Output results in machine-readable JSON format.\n"
                "[bold cyan]--no-banner[/]       : Disable the HealCode startup banner for this execution.\n"
                "[bold cyan]--log-level <lvl>[/]  : Override logging level (TRACE, DEBUG, INFO, WARN, ERROR)."
            )
            
            # Categorized Commands
            core_commands = (
                "[bold green]scan[/]      : Run diagnostic scans on target directory.\n"
                "[bold green]watch[/]     : Monitor directory for file changes & rescan.\n"
                "[bold green]baseline[/]  : Capture, compare, & detect configuration drift."
            )
            
            config_commands = (
                "[bold green]config[/]      : Manage project & global configurations.\n"
                "[bold green]profile[/]     : Manage diagnostics scanning profiles.\n"
                "[bold green]plugins[/]     : List loaded plugins and scanners.\n"
                "[bold green]marketplace[/] : Discover, install, update, & manage plugins."
            )
            
            util_commands = (
                "[bold green]ai[/]      : Run AI-powered analysis on scan findings.\n"
                "[bold green]version[/] : Print HealCode CLI version information."
            )

            with console.capture() as capture:
                console.print(Panel(options_text, title="[bold cyan]Global Options[/bold cyan]", border_style="cyan", expand=False))
                console.print()
                console.print(Panel(core_commands, title="[bold green]Core Operations[/bold green]", border_style="green", expand=False))
                console.print()
                console.print(Panel(config_commands, title="[bold blue]Configuration & Extensions[/bold blue]", border_style="blue", expand=False))
                console.print()
                console.print(Panel(util_commands, title="[bold magenta]Utilities & AI[/bold magenta]", border_style="magenta", expand=False))
            
            return capture.get()
        
        # Build a beautiful custom help using Rich!
        # Overview description
        overview = (
            "HealCode is a developer diagnostics command line interface designed "
            "to audit, scan, fix, and optimize your codebase infrastructure, development environments, "
            "network ports, and container configurations."
        )
        
        # Quick Start content
        quick_start_text = (
            "Run [bold cyan]healcode --help[/] to see all commands\n"
            "Run [bold cyan]healcode version[/] to check version"
        )
        
        # Capture the Rich prints to string
        with console.capture() as capture:
            console.print(Panel(overview, title="[bold magenta]HealCode Overview[/bold magenta]", border_style="magenta", expand=False))
            console.print()
            console.print(Panel(quick_start_text, title="[bold cyan]Quick Start[/bold cyan]", border_style="cyan", expand=False))
            
        return capture.get()

def create_parser(commands: Dict[str, BaseCommand]) -> argparse.ArgumentParser:
    parser = HealCodeArgumentParser(
        prog="healcode",
        description=f"{APP_NAME}: {APP_DESCRIPTION}",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Global arguments
    parser.add_argument("--json", action="store_true", help="Output results in machine-readable JSON format.")
    parser.add_argument("--no-banner", action="store_true", help="Disable the HealCode startup banner for this execution.")
    parser.add_argument("--log-level", default=None, choices=["TRACE", "DEBUG", "INFO", "WARN", "ERROR"],
                        help="Override default logging level.")

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", required=False, title="Commands", metavar="<command>")

    for command_name, cmd_obj in commands.items():
        cmd_parser = subparsers.add_parser(
            command_name,
            help=cmd_obj.description,
            description=cmd_obj.description
        )
        cmd_obj.setup_parser(cmd_parser)

    return parser
