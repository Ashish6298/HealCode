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
    assert "usage: healcode" in captured.out
    assert "Commands" in captured.out


def test_cli_no_banner_flag(capsys) -> None:
    exit_code = main(["--no-banner", "version"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "HealCode" in captured.out
