"""
HealCode Scan Command
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
from healcode.reporting.console import ConsoleReporter
from healcode.reporting.json_reporter import JSONReporter
from healcode.utils.os_detector import get_os_info
from healcode.utils.ui import print_info, get_progress_bar

class ScanCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "scan"

    @property
    def description(self) -> str:
        return "Run diagnostic scans on a codebase target directory."

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("target", nargs="?", default=".", help="Target directory or file to scan (default: current directory).")
        parser.add_argument("--no-cache", action="store_true", help="Disable cache reading and writing for this scan.")
        parser.add_argument("--format", choices=["console", "json", "csv", "xml"], default="console", help="Output format.")
        parser.add_argument("--profile", help="Diagnostic scanning profile name.")

    def run(self, args: argparse.Namespace, config: ProjectConfig) -> int:
        target = args.target
        is_json = getattr(args, "json", False) or args.format == "json"
        
        # Validate target path existence
        if not os.path.exists(target):
            if is_json:
                import json
                print(json.dumps({
                    "command": "scan",
                    "status": "error",
                    "error": {
                        "type": "ValidationError",
                        "message": f"Target path does not exist: {target}"
                    },
                    "exit_code": 1
                }, indent=4))
            else:
                from healcode.utils.ui import print_error
                print_error(f"Error: Target path '{target}' does not exist.")
                print_info("Guidance: Please specify a valid file or directory path, or omit the argument to scan the current directory ('.').")
            return 1

        # Validate profile name if supplied
        if args.profile:
            from healcode.core.profiles import PROFILES
            # Case-insensitive comparison is friendlier
            matched_profile = None
            for p in PROFILES:
                if p.lower() == args.profile.lower():
                    matched_profile = p
                    break
            
            if not matched_profile:
                if is_json:
                    import json
                    print(json.dumps({
                        "command": "scan",
                        "status": "error",
                        "error": {
                            "type": "ValidationError",
                            "message": f"Invalid diagnostics profile '{args.profile}'. Available: {', '.join(PROFILES.keys())}"
                        },
                        "exit_code": 1
                    }, indent=4))
                else:
                    from healcode.utils.ui import print_error
                    print_error(f"Error: Invalid diagnostics profile '{args.profile}'.")
                    print_info(f"Available profiles: {', '.join(PROFILES.keys())}")
                    print_info("Guidance: Run 'healcode profile list' to see all available profiles.")
                return 1
            
            config.scan.profile = matched_profile

        start_time = time.time()

        if args.no_cache:
            config.cache.enabled = False

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

            # Progress bar for visual polish
            findings = []
            is_json = getattr(args, "json", False) or args.format == "json"
            is_structured = is_json or args.format in ["csv", "xml"]
            
            if not is_structured:
                with get_progress_bar() as progress:
                    task = progress.add_task("[cyan]Scanning codebase and system...", total=100)
                    findings = engine.run(target)
                    progress.update(task, completed=100)
            else:
                findings = engine.run(target)

            scan_duration = time.time() - start_time

            # Compute Health Score
            health_engine = HealthEngine()
            health_score = health_engine.calculate_score(findings)

            # Choose reporter
            os_info = get_os_info()
            
            from healcode.core.interfaces import IReporter
            reporter: IReporter
            
            if is_json:
                reporter = JSONReporter()
                system_data = os_info.to_dict()
                system_data["scan_duration_seconds"] = scan_duration
                system_data["health_score"] = health_score
                reporter.generate(findings, system_data)
            elif args.format == "csv":
                from healcode.reporting.csv_reporter import CSVReporter
                reporter = CSVReporter()
                reporter.generate(findings, {})
            elif args.format == "xml":
                from healcode.reporting.xml_reporter import XMLReporter
                reporter = XMLReporter()
                reporter.generate(findings, os_info.to_dict())
            else:
                reporter = ConsoleReporter()
                if hasattr(reporter, "set_extra_metadata"):
                    getattr(reporter, "set_extra_metadata")(health_score, scan_duration)
                else:
                    reporter.health_score = health_score  # type: ignore
                    reporter.scan_duration = scan_duration  # type: ignore
                reporter.generate(findings, os_info.to_dict())

            return 0
        finally:
            if cache_mgr:
                cache_mgr.close()
