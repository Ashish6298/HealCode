"""
HealCode Plugins Command
"""

import argparse
from healcode.cli.commands.base import BaseCommand
from healcode.config.models import ProjectConfig
from healcode.core.plugin_loader import PluginLoader
from healcode.utils.ui import console, render_table

class PluginsCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "plugins"

    @property
    def description(self) -> str:
        return "List loaded plugins and scanners."

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        pass

    def run(self, args: argparse.Namespace, config: ProjectConfig) -> int:
        is_json = getattr(args, "json", False)
        loader = PluginLoader(config)
        
        try:
            if config.plugins.plugin_dirs:
                loader.load_plugins_from_dirs(config.plugins.plugin_dirs)
        except Exception as e:
            if is_json:
                import json
                print(json.dumps({
                    "command": "plugins",
                    "status": "error",
                    "error": {
                        "type": type(e).__name__,
                        "message": f"Failed to load plugins: {e}"
                    },
                    "exit_code": 1
                }, indent=4))
            else:
                from healcode.utils.ui import print_error
                print_error(f"Error: Failed to load plugins: {e}")
            return 1

        # Safeguard optional fields and filter out duplicates or invalid entries
        seen_plugins = set()
        plugin_list = []
        for p in loader.plugins.values():
            name = getattr(p, "name", None) or "unknown-plugin"
            if name in seen_plugins:
                continue
            seen_plugins.add(name)
            
            plugin_list.append({
                "name": name,
                "version": getattr(p, "version", None) or "0.0.0",
                "description": getattr(p, "description", None) or "No description provided."
            })

        if is_json:
            import json
            print(json.dumps({
                "command": "plugins",
                "status": "success",
                "plugins": plugin_list
            }, indent=4))
        else:
            if not plugin_list:
                console.print("[warning]No plugins loaded. Configure plugin_dirs in healcode.json to discover custom plugins.[/warning]")
                return 0

            headers = ["Plugin Name", "Version", "Description"]
            rows = [
                [p["name"], p["version"], p["description"]]
                for p in plugin_list
            ]
            render_table("Registered Plugins", headers, rows)
        return 0
