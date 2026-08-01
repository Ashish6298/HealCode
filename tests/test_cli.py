"""
Tests for CLI Command Routing
"""

import sys
import json
from unittest.mock import patch
from healcode.cli.entrypoint import main
from healcode.constants import VERSION

def test_cli_version(capsys) -> None:
    exit_code = main(["version"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert VERSION in captured.out

def test_cli_version_json(capsys) -> None:
    exit_code = main(["--json", "version"])
    assert exit_code == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out.strip())
    assert data["version"] == VERSION

def test_cli_invalid_command() -> None:
    try:
        main(["nonexistent-command"])
    except SystemExit as e:
        assert e.code != 0


def test_cli_bare_command_shows_help(capsys) -> None:
    exit_code = main([])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Quick Start" in captured.out


def test_cli_no_banner_flag(capsys) -> None:
    exit_code = main(["--no-banner", "version"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "HealCode" in captured.out


def test_cli_log_level_flag(capsys) -> None:
    # Test valid log level
    exit_code = main(["version", "--log-level", "DEBUG"])
    assert exit_code == 0
    
    # Test invalid log level
    exit_code_invalid = main(["version", "--log-level", "INVALID"])
    assert exit_code_invalid != 0
    captured = capsys.readouterr()
    assert "Invalid logging level" in captured.err or "Invalid logging level" in captured.out


def test_cli_scan_validation(capsys) -> None:
    # Test invalid target path
    exit_code_path = main(["scan", "nonexistent_directory_xyz"])
    assert exit_code_path == 1
    captured = capsys.readouterr()
    assert "Target path 'nonexistent_directory_xyz' does not exist" in captured.err or "Target path 'nonexistent_directory_xyz' does not exist" in captured.out

    # Test invalid diagnostics profile
    exit_code_profile = main(["scan", "--profile", "nonexistent_profile_abc"])
    assert exit_code_profile == 1
    captured_profile = capsys.readouterr()
    assert "Invalid diagnostics profile" in captured_profile.err or "Invalid diagnostics profile" in captured_profile.out


