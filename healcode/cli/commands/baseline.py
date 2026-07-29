"""
HealCode Baseline & Drift Detection Command
"""

import argparse
import os
import json
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
from healcode.utils.ui import console, print_success, print_info, print_error, get_progress_bar

class BaselineCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "baseline"

    @property
    def description(self) -> str:
        return "Capture, compare, and detect configuration drift against active baselines."

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        subparsers = parser.add_subparsers(dest="baseline_action", required=True)
        
        create_p = subparsers.add_parser("create", help="Create a new baseline recording from current scan.")
        create_p.add_argument("name", help="Name for the baseline file.")
        
        compare_p = subparsers.add_parser("compare", help="Compare current project diagnostics with a baseline.")
        compare_p.add_argument("name", help="Name of baseline to compare against.")

    def run(self, args: argparse.Namespace, config: ProjectConfig) -> int:
        baseline_dir = ".healcode_baselines"
        os.makedirs(baseline_dir, exist_ok=True)
        baseline_path = os.path.join(baseline_dir, f"{args.name}.json")

        cache_mgr = None
        if config.cache.enabled:
            cache_mgr = CacheManager(config.cache.db_path)

        try:
            if args.baseline_action == "create":
                engine = ScanEngine(config, cache_mgr)
                
                # Import core scanners
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
                    task = progress.add_task("[cyan]Scanning for baseline...", total=100)
                    findings = engine.run(".")
                    progress.update(task, completed=100)

                health_engine = HealthEngine()
                score = health_engine.calculate_score(findings)

                baseline_data = {
                    "name": args.name,
                    "timestamp": time.time(),
                    "score": score,
                    "findings": findings
                }

                with open(baseline_path, "w", encoding="utf-8") as f:
                    json.dump(baseline_data, f, indent=4)

                print_success(f"Successfully recorded baseline '{args.name}' to: {baseline_path}")
                return 0

            elif args.baseline_action == "compare":
                if not os.path.exists(baseline_path):
                    print_error(f"Baseline '{args.name}' does not exist at {baseline_path}")
                    return 1

                with open(baseline_path, "r", encoding="utf-8") as f:
                    baseline_data = json.load(f)

                engine = ScanEngine(config, cache_mgr)
                
                # Import core scanners
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
                    task = progress.add_task("[cyan]Scanning for comparison...", total=100)
                    current_findings = engine.run(".")
                    progress.update(task, completed=100)

                health_engine = HealthEngine()
                current_score = health_engine.calculate_score(current_findings)

                # Compare findings
                base_ids = {f.get("id") for f in baseline_data["findings"] if f.get("id")}
                current_ids = {f.get("id") for f in current_findings if f.get("id")}

                regressions = current_ids - base_ids
                resolved = base_ids - current_ids

                console.print(f"\n[bold cyan]HealCode Drift Report against '{args.name}':[/bold cyan]")
                
                old_score_val = baseline_data["score"].get("overall", 100.0)
                new_score_val = current_score.get("overall", 100.0)
                score_diff = new_score_val - old_score_val
                
                diff_str = f"+{score_diff:.2f}%" if score_diff >= 0 else f"{score_diff:.2f}%"
                console.print(f" - Health Score: {old_score_val}% -> {new_score_val}% ({diff_str})")
                
                if regressions:
                    console.print(f" - [bold red]Regressions (New Issues):[/bold red] {len(regressions)}")
                    for r in regressions:
                        console.print(f"   * [red]{r}[/]")
                else:
                    console.print(" - [bold green]Regressions (New Issues):[/bold green] None")

                if resolved:
                    console.print(f" - [bold green]Resolved Issues:[/bold green] {len(resolved)}")
                    for res in resolved:
                        console.print(f"   * [green]{res}[/]")
                else:
                    console.print(" - [bold yellow]Resolved Issues:[/bold yellow] None")

                return 0

            return 1
        finally:
            if cache_mgr:
                cache_mgr.close()
