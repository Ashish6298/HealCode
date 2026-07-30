"""
HealCode Config Command
"""

import argparse
import os
from healcode.cli.commands.base import BaseCommand
from healcode.config.models import ProjectConfig
from healcode.config.manager import ConfigManager
from healcode.utils.ui import console, print_success, print_info

class ConfigCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "config"

    @property
    def description(self) -> str:
        return "Manage project and global HealCode configurations."

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        subparsers = parser.add_subparsers(dest="config_action", required=True)
        
        # Init config
        subparsers.add_parser("init", help="Initialize a new healcode.json configuration in the current directory.")
        
        # Show config
        subparsers.add_parser("show", help="Display the merged active configuration.")

    def run(self, args: argparse.Namespace, config: ProjectConfig) -> int:
        manager = ConfigManager()
        is_json = getattr(args, "json", False)
        
        if args.config_action == "init":
            if os.path.exists(manager.project_config_path):
                if is_json:
                    import json
                    print(json.dumps({
                        "command": "config init",
                        "status": "success",
                        "message": "Configuration file already exists.",
                        "path": manager.project_config_path
                    }, indent=4))
                else:
                    print_info(f"Configuration file already exists at {manager.project_config_path}")
                return 0
            
            manager.config = ProjectConfig()
            manager.save_project_config()
            
            if is_json:
                import json
                print(json.dumps({
                    "command": "config init",
                    "status": "success",
                    "message": "Initialized project configuration file successfully.",
                    "path": manager.project_config_path
                }, indent=4))
            else:
                print_success(f"Initialized project configuration file: {manager.project_config_path}")
            return 0

        elif args.config_action == "show":
            manager.load()
            if is_json:
                import json
                print(json.dumps({
                    "command": "config show",
                    "status": "success",
                    "path": manager.project_config_path,
                    "configuration": manager._model_to_dict(manager.config)
                }, indent=4))
            else:
                console.print(f"[bold]Active Configuration Path:[/] {manager.project_config_path}")
                console.print_json(data=manager._model_to_dict(manager.config))
            return 0

        return 1
