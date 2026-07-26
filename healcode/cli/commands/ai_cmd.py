"""
HealCode AI CLI Command
Runs the AI Intelligence Engine on scan findings to produce
root-cause analysis, recommendations, and executive summaries.
"""

import argparse
import os
import time
from healcode.cli.commands.base import BaseCommand
from healcode.config.models import ProjectConfig
from healcode.core.engine import ScanEngine
from healcode.core.scanners.default_scanner import DefaultScanner
from healcode.core.scanners.system_scanner import SystemScanner
from healcode.core.scanners.path_analyzer import PathAnalyzer
from healcode.core.scanners.port_scanner import PortScanner
from healcode.core.cache import CacheManager
from healcode.core.health import HealthEngine
from healcode.ai.engine import AIEngine
from healcode.ai.provider import get_provider
from healcode.utils.ui import print_info, get_progress_bar


class AICommand(BaseCommand):
    @property
    def name(self) -> str:
        return "ai"

    @property
    def description(self) -> str:
        return "Run AI-powered analysis on scan findings (offline-first)."

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "target", nargs="?", default=".",
            help="Target directory to scan (default: current directory).",
        )
        parser.add_argument(
            "--offline", action="store_true", default=False,
            help="Force offline heuristic provider (no external API calls).",
        )

    def run(self, args: argparse.Namespace, config: ProjectConfig) -> int:
        target = args.target
        start = time.time()

        # Determine provider
        provider_name = "offline" if args.offline else config.ai.provider
        provider = get_provider(provider_name)

        # Run the scan pipeline first (AI never bypasses scanners)
        cache_mgr = None
        if config.cache.enabled:
            cache_mgr = CacheManager(config.cache.db_path)

        try:
            engine = ScanEngine(config, cache_mgr)

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

            with get_progress_bar() as progress:
                task = progress.add_task("[cyan]Scanning...", total=100)
                findings = engine.run(target)
                progress.update(task, completed=100)

            # Run AI analysis
            ai_engine = AIEngine(provider=provider)
            analysis = ai_engine.analyse(findings)

            # Display results
            from rich.console import Console
            from rich.panel import Panel
            from rich.table import Table

            console = Console()

            # Executive Summary
            console.print(Panel(
                analysis["summary"],
                title="[bold cyan]AI Executive Summary[/bold cyan]",
                border_style="cyan",
            ))

            # Root Causes
            if analysis["root_causes"]:
                table = Table(title="Root Cause Analysis", show_lines=True)
                table.add_column("Group", style="bold")
                table.add_column("Findings", justify="right")
                table.add_column("Confidence", justify="right")
                table.add_column("Summary")
                for cause in analysis["root_causes"][:10]:
                    table.add_row(
                        cause["group"],
                        str(cause["finding_count"]),
                        f"{cause['confidence']}%",
                        cause["summary"],
                    )
                console.print(table)

            # Recommendations
            if analysis["recommendations"]:
                rec_table = Table(title="Top Recommendations", show_lines=True)
                rec_table.add_column("Finding", style="bold")
                rec_table.add_column("Risk")
                rec_table.add_column("Est. Minutes", justify="right")
                rec_table.add_column("Description")
                for rec in analysis["recommendations"][:10]:
                    rec_table.add_row(
                        rec["finding_id"],
                        rec["risk"],
                        str(rec["estimated_minutes"]),
                        rec["description"],
                    )
                console.print(rec_table)

            elapsed = time.time() - start
            console.print(f"\n[dim]AI Provider: {provider.name} | Duration: {elapsed:.2f}s[/dim]")

            return 0
        finally:
            if cache_mgr:
                cache_mgr.close()
