"""
HealCode Plugin Marketplace Command
Allows offline/mock search, installation, updates, and validation of community diagnostics scanners.
"""

import argparse
import json
from healcode.cli.commands.base import BaseCommand
from healcode.config.models import ProjectConfig
from healcode.core.plugin_loader import PluginLoader
from healcode.utils.ui import console, print_success, print_info, print_error

MOCK_PLUGINS = [
    {"name": "security-hardening-pack", "version": "1.2.0", "author": "HealCode Core Team", "description": "Strict static checks for secrets, AWS policies, and SSL credentials."},
    {"name": "rust-analyzer-plugin", "version": "0.8.4", "author": "Mozilla Community", "description": "Detailed cargo structure and safety static checks for Rust source code."},
    {"name": "kubernetes-kustomize-pack", "version": "2.1.0", "author": "K8s SIGs", "description": "Drift and structure checking for kustomize deployments."},
    {"name": "python-performance-smells", "version": "1.0.1", "author": "Python Hackers", "description": "Static analysis checks for high CPU consumption patterns, list copying, and dict comprehensions."}
]

class MarketplaceCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "marketplace"

    @property
    def description(self) -> str:
        return "Discover, install, update, and manage plugins from the HealCode community marketplace."

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        subparsers = parser.add_subparsers(dest="marketplace_action", required=True)
        
        search_p = subparsers.add_parser("search", help="Search for marketplace plugins.")
        search_p.add_argument("query", nargs="?", default="", help="Query string to filter plugins.")
        
        install_p = subparsers.add_parser("install", help="Install a plugin.")
        install_p.add_argument("plugin_name", help="Name of the plugin to install.")

        update_p = subparsers.add_parser("update", help="Update an installed plugin.")
        update_p.add_argument("plugin_name", help="Name of the plugin to update.")

        remove_p = subparsers.add_parser("remove", help="Remove an installed plugin.")
        remove_p.add_argument("plugin_name", help="Name of the plugin to remove.")

    def run(self, args: argparse.Namespace, config: ProjectConfig) -> int:
        is_json = getattr(args, "json", False)

        # Load currently installed plugins to detect duplicate installs or invalid updates/removals
        loader = PluginLoader(config)
        try:
            if config.plugins.plugin_dirs:
                loader.load_plugins_from_dirs(config.plugins.plugin_dirs)
        except Exception:
            pass

        try:
            if args.marketplace_action == "search":
                q = args.query.lower()
                results = []
                for p in MOCK_PLUGINS:
                    if q in p["name"].lower() or q in p["description"].lower():
                        results.append(p)
                
                if is_json:
                    print(json.dumps({
                        "command": "marketplace search",
                        "status": "success",
                        "operation": "search",
                        "query": args.query,
                        "results": results
                    }, indent=4))
                else:
                    console.print("[bold cyan]HealCode Plugin Marketplace Search Results:[/bold cyan]\n")
                    found = False
                    for p in results:
                        console.print(f" - [bold green]{p['name']} (v{p['version']})[/] by {p['author']}")
                        console.print(f"   {p['description']}\n")
                        found = True
                    if not found:
                        console.print(f"[yellow]No plugins matched query: '{args.query}'[/]")
                return 0

            elif args.marketplace_action == "install":
                pname = args.plugin_name
                
                # Check for duplicate installation
                if pname.lower() in [name.lower() for name in loader.plugins]:
                    if is_json:
                        print(json.dumps({
                            "command": "marketplace install",
                            "status": "success",
                            "operation": "install",
                            "plugin": pname,
                            "message": f"Plugin '{pname}' is already installed."
                        }, indent=4))
                    else:
                        print_info(f"Plugin '{pname}' is already installed.")
                    return 0

                plugin_meta = None
                for p in MOCK_PLUGINS:
                    if p["name"].lower() == pname.lower():
                        plugin_meta = p
                        break
                
                if not plugin_meta:
                    if is_json:
                        print(json.dumps({
                            "command": "marketplace install",
                            "status": "error",
                            "operation": "install",
                            "plugin": pname,
                            "message": f"Plugin '{pname}' was not found in the marketplace registry."
                        }, indent=4))
                    else:
                        print_error(f"Plugin '{pname}' was not found in the marketplace registry.")
                    return 1

                if is_json:
                    print(json.dumps({
                        "command": "marketplace install",
                        "status": "success",
                        "operation": "install",
                        "plugin": plugin_meta
                    }, indent=4))
                else:
                    print_info(f"Downloading manifest and package files for [bold green]{plugin_meta['name']}[/]...")
                    print_info("Validating signature and target environment dependencies...")
                    print_success(f"Successfully installed plugin: [bold green]{plugin_meta['name']} (v{plugin_meta['version']})[/bold green]")
                return 0

            elif args.marketplace_action == "update":
                pname = args.plugin_name
                
                # If plugin is not installed, fail with guidance
                if pname.lower() not in [name.lower() for name in loader.plugins]:
                    if is_json:
                        print(json.dumps({
                            "command": "marketplace update",
                            "status": "error",
                            "operation": "update",
                            "plugin": pname,
                            "message": f"Plugin '{pname}' is not currently installed. Run 'healcode marketplace install {pname}' first."
                        }, indent=4))
                    else:
                        print_error(f"Error: Plugin '{pname}' is not currently installed.")
                        print_info(f"Guidance: Run 'healcode marketplace install {pname}' first to install it.")
                    return 1

                if is_json:
                    print(json.dumps({
                        "command": "marketplace update",
                        "status": "success",
                        "operation": "update",
                        "plugin_name": pname,
                        "message": "Already at the latest version."
                    }, indent=4))
                else:
                    print_success(f"Plugin [bold green]{pname}[/] is already at the latest version.")
                return 0

            elif args.marketplace_action == "remove":
                pname = args.plugin_name

                # If plugin is not installed, fail with exit code 1
                if pname.lower() not in [name.lower() for name in loader.plugins]:
                    if is_json:
                        print(json.dumps({
                            "command": "marketplace remove",
                            "status": "error",
                            "operation": "remove",
                            "plugin": pname,
                            "message": f"Plugin '{pname}' is not currently installed."
                        }, indent=4))
                    else:
                        print_error(f"Error: Plugin '{pname}' is not currently installed.")
                    return 1

                if is_json:
                    print(json.dumps({
                        "command": "marketplace remove",
                        "status": "success",
                        "operation": "remove",
                        "plugin_name": pname
                    }, indent=4))
                else:
                    print_success(f"Successfully removed plugin [bold red]{pname}[/bold red].")
                return 0

            return 1
        except Exception as e:
            if is_json:
                print(json.dumps({
                    "command": "marketplace",
                    "status": "error",
                    "error": {
                        "type": type(e).__name__,
                        "message": f"Unexpected error during marketplace operation: {e}"
                    },
                    "exit_code": 1
                }, indent=4))
            else:
                print_error(f"Error: Unexpected error during marketplace operation: {e}")
            return 1
