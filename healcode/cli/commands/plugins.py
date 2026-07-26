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
        loader = PluginLoader(config)
        if config.plugins.plugin_dirs:
            loader.load_plugins_from_dirs(config.plugins.plugin_dirs)

        if getattr(args, "json", False):
            import json
            plugin_list = [
                {"name": p.name, "version": p.version, "description": p.description}
                for p in loader.plugins.values()
            ]
            print(json.dumps(plugin_list, indent=4))
        else:
            if not loader.plugins:
                console.print("[warning]No plugins loaded. Configure plugin_dirs in healcode.json to discover custom plugins.[/warning]")
                return 0

            headers = ["Plugin Name", "Version", "Description"]
            rows = [
                [p.name, p.version, p.description]
                for p in loader.plugins.values()
            ]
            render_table("Registered Plugins", headers, rows)
        return 0
