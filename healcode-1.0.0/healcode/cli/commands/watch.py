"""
HealCode Watch Command
Monitors target directory for file modifications and triggers incremental scans.
"""

import argparse
import os
import time
from healcode.cli.commands.base import BaseCommand
from healcode.config.models import ProjectConfig
from healcode.core.engine import ScanEngine
from healcode.core.health import HealthEngine
from healcode.core.cache import CacheManager
from healcode.core.scanners.default_scanner import DefaultScanner
from healcode.core.scanners.system_scanner import SystemScanner
from healcode.core.scanners.path_analyzer import PathAnalyzer
from healcode.core.scanners.port_scanner import PortScanner
from healcode.utils.ui import console, print_info, print_success

class WatchCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "watch"

    @property
    def description(self) -> str:
        return "Monitor directory for file changes and execute incremental scans."

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("target", nargs="?", default=".", help="Target directory to watch (default: current directory).")
        parser.add_argument("--interval", type=float, default=2.0, help="Interval in seconds to check for file changes.")

    def run(self, args: argparse.Namespace, config: ProjectConfig) -> int:
        target = os.path.abspath(args.target)
        print_info(f"Starting watch mode on: [bold cyan]{target}[/] (Check interval: {args.interval}s)")
        print_info("Press Ctrl+C to stop.")

        def get_mtimes():
            mtimes = {}
            for root, dirs, files in os.walk(target):
                # skip git, venv
                if any(x in root for x in [".git", "venv", ".healcode_cache.db", ".healcode_baselines", "reports"]):
                    continue
                for file in files:
                    fp = os.path.join(root, file)
                    try:
                        mtimes[fp] = os.path.getmtime(fp)
                    except OSError:
                        pass
            return mtimes

        last_mtimes = get_mtimes()

        # Run initial scan
        self._run_scan(target, config)

        try:
            while True:
                time.sleep(args.interval)
                current_mtimes = get_mtimes()
                
                # Check for changes
                changed = []
                for fp, mtime in current_mtimes.items():
                    if fp not in last_mtimes or last_mtimes[fp] != mtime:
                        changed.append(fp)

                for fp in last_mtimes:
                    if fp not in current_mtimes:
                        changed.append(fp)

                if changed:
                    print_success(f"Detected change in {len(changed)} file(s). Triggering incremental rescan...")
                    for fp in changed[:5]:
                        console.print(f" - [dim]{fp}[/]")
                    if len(changed) > 5:
                        console.print(f" - ... and {len(changed) - 5} more files.")
                    
                    self._run_scan(target, config)
                    last_mtimes = current_mtimes

        except KeyboardInterrupt:
            console.print("\n[bold yellow]Stopping watch mode.[/bold yellow]")
            return 0

    def _run_scan(self, target: str, config: ProjectConfig):
        cache_mgr = None
        if config.cache.enabled:
            cache_mgr = CacheManager(config.cache.db_path)

        try:
            engine = ScanEngine(config, cache_mgr)
            
            # Register scanners
            from healcode.core.scanners.runtime_scanner import RuntimeScanner
            from healcode.core.scanners.compatibility_scanner import CompatibilityScanner
            from healcode.core.scanners.git_scanner import GitScanner
            from healcode.core.scanners.env_scanner import EnvScanner
            from healcode.core.scanners.secret_scanner import SecretScanner
            from healcode.core.scanners.framework_scanner import FrameworkScanner
            from healcode.core.scanners.docker_scanner import DockerScanner
            from healcode.core.scanners.dockerfile_scanner import DockerfileScanner
            from healcode.core.scanners.compose_scanner import ComposeScanner
            from healcode.core.scanners.project_scanner import ProjectScanner
            from healcode.core.scanners.cloud_scanner import CloudScanner
            from healcode.core.scanners.code_scanner import CodeScanner

            rt_scanner = RuntimeScanner()
            engine.register_scanner(DefaultScanner())
            engine.register_scanner(SystemScanner())
            engine.register_scanner(PathAnalyzer())
            engine.register_scanner(PortScanner())
            engine.register_scanner(rt_scanner)
            engine.register_scanner(CompatibilityScanner(runtime_scanner=rt_scanner))
            engine.register_scanner(GitScanner())
            engine.register_scanner(EnvScanner())
            engine.register_scanner(SecretScanner())
            engine.register_scanner(FrameworkScanner())
            engine.register_scanner(DockerScanner())
            engine.register_scanner(DockerfileScanner())
            engine.register_scanner(ComposeScanner())
            engine.register_scanner(ProjectScanner())
            engine.register_scanner(CloudScanner())
            engine.register_scanner(CodeScanner())

            findings = engine.run(target)
            health_engine = HealthEngine()
            score = health_engine.calculate_score(findings)
            
            console.print(f"[bold green]Scan Completed.[/] Overall Health Score: [bold cyan]{score.get('overall')}%[/]")
        finally:
            if cache_mgr:
                cache_mgr.close()
