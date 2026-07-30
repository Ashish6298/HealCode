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
        import platform
        import sys
        
        is_json = getattr(args, "json", False)
        
        try:
            py_ver = sys.version.split()[0]
            os_name = platform.system() or "Unknown OS"
            arch = platform.machine() or "Unknown Arch"
            release_type = "stable"
            build_type = "official release"
            
            if is_json:
                import json
                print(json.dumps({
                    "command": "version",
                    "status": "success",
                    "name": APP_NAME,
                    "version": VERSION,
                    "description": APP_DESCRIPTION,
                    "release_type": release_type,
                    "python_version": py_ver,
                    "os": os_name,
                    "architecture": arch,
                    "build_type": build_type
                }, indent=4))
            else:
                console.print(f"[highlight]{APP_NAME}[/] v{VERSION} - [info]{APP_DESCRIPTION}[/]")
                console.print(f"[dim]Release:[/] {release_type} | [dim]Python Runtime:[/] {py_ver} | [dim]OS:[/] {os_name} ({arch})")
            return 0
        except Exception as e:
            if is_json:
                import json
                print(json.dumps({
                    "command": "version",
                    "status": "error",
                    "error": {
                        "type": type(e).__name__,
                        "message": f"Failed to retrieve version information: {e}"
                    },
                    "exit_code": 1
                }, indent=4))
            else:
                from healcode.utils.ui import print_error
                print_error(f"Error: Failed to retrieve version information: {e}")
            return 1
