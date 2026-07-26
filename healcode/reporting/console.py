"""
HealCode Console Reporter
Renders findings in a beautiful, styled console output.
"""

from typing import List, Dict, Any, Optional
from healcode.reporting.base import BaseReporter
from healcode.utils.ui import console, render_table, print_header, print_success, print_error, print_warning

class ConsoleReporter(BaseReporter):
    def __init__(self) -> None:
        super().__init__()
        self.health_score: Optional[Dict[str, Any]] = None
        self.scan_duration: float = 0.0

    def set_extra_metadata(self, health_score: Dict[str, Any], scan_duration: float) -> None:
        self.health_score = health_score
        self.scan_duration = scan_duration

    def generate(self, findings: List[Dict[str, Any]], system_info: Dict[str, Any]) -> None:
        print_header("HealCode Diagnostic Scan Report")
        
        # System status block
        console.print(f"[bold]Platform:[/] {system_info.get('friendly_name', 'Unknown')}")
        console.print(f"[bold]Release:[/] {system_info.get('release', '')}")
        console.print(f"[bold]Architecture:[/] {system_info.get('machine', '')}")
        console.print(f"[bold]Scan Duration:[/] {self.scan_duration:.3f} seconds\n")

        # Visual Health Score
        if self.health_score:
            score = self.health_score.get("overall", 100.0)
            if score >= 85:
                color = "green"
            elif score >= 60:
                color = "yellow"
            else:
                color = "red"
            
            from healcode.utils.ui import IS_UTF8
            bar_len = int(score / 5)
            if IS_UTF8:
                bar = "█" * bar_len + "░" * (20 - bar_len)
            else:
                bar = "#" * bar_len + "-" * (20 - bar_len)
            console.print(f"[bold]OVERALL SYSTEM HEALTH SCORE:[/] [{color}]{bar} {score}%[/{color}]\n")
            
            # Print Categories
            categories = self.health_score.get("categories", {})
            cat_list = []
            for cat, val in categories.items():
                cat_list.append(f"{cat}: [bold]{val}%[/]")
            console.print(f"Categories: {', '.join(cat_list)}\n")

        if not findings:
            print_success("No diagnostics issues found! Your system is healthy.")
            return

        # Prepare Table Rows
        headers = ["Severity", "Subsystem/File", "Line", "Code/ID", "Message"]
        rows = []
        for f in findings:
            severity = f.get("severity", "WARN").upper()
            if severity in ("ERROR", "CRITICAL"):
                sev_styled = f"[error]{severity}[/error]"
            elif severity == "WARN" or severity == "WARNING":
                sev_styled = "[warning]WARN[/warning]"
            else:
                sev_styled = "[info]INFO[/info]"

            rows.append([
                sev_styled,
                f.get("file", "unknown"),
                str(f.get("line", "-")),
                f.get("scanner", f.get("id", "unknown")),
                f.get("message", "")
            ])

        render_table("Scan Findings", headers, rows)

        # Summary footer
        summary = self.get_summary(findings)
        console.print(f"\n[bold]Summary:[/] [error]{summary.get('ERROR', 0) + summary.get('CRITICAL', 0)} Errors[/error], [warning]{summary.get('WARN', 0)} Warnings[/warning], [info]{summary.get('INFO', 0)} Info[/info] ({summary['TOTAL']} Total)")
