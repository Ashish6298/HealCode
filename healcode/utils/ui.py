"""
HealCode UI Helpers
Wrappers around rich for tables, spinners, progress bars, and status.
"""

from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.theme import Theme

# Define professional theme
HEALCODE_THEME = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red bold",
    "success": "green bold",
    "title": "magenta bold",
    "highlight": "blue bold"
})

console = Console(theme=HEALCODE_THEME)

def print_header(title: str) -> None:
    console.print(f"\n[title]=== {title} ===[/title]")

import sys

def _is_utf8() -> bool:
    try:
        encoding = getattr(sys.stdout, "encoding", None) or ""
        return "utf" in encoding.lower() or "65001" in encoding
    except Exception:
        return False

IS_UTF8 = _is_utf8()

def print_success(message: str) -> None:
    icon = "✔" if IS_UTF8 else "[+]"
    console.print(f"[success]{icon} {message}[/success]")

def print_warning(message: str) -> None:
    icon = "⚠" if IS_UTF8 else "[!]"
    console.print(f"[warning]{icon} {message}[/warning]")

def print_error(message: str) -> None:
    icon = "✘" if IS_UTF8 else "[-]"
    console.print(f"[error]{icon} {message}[/error]")

def print_info(message: str) -> None:
    icon = "ℹ" if IS_UTF8 else "[i]"
    console.print(f"[info]{icon} {message}[/info]")

def render_table(title: str, headers: List[str], rows: List[List[str]]) -> None:
    table = Table(title=title, show_header=True, header_style="bold magenta")
    for header in headers:
        table.add_column(header)
    for row in rows:
        table.add_row(*row)
    console.print(table)

def get_progress_bar() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        transient=True
    )
