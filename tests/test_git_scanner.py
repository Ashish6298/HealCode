"""
Tests for Git Scanner
"""

from unittest.mock import patch
from healcode.core.scanners.git_scanner import GitScanner

def test_git_scanner_detection() -> None:
    scanner = GitScanner()
    
    # Mock _run_git_cmd to return mock command line outputs
    def mock_run(args, cwd=None):
        if "--version" in args:
            return "git version 2.40.0"
        if "rev-parse" in args:
            return "true"
        if "config" in args:
            return "test-user"
        return "mock-value"

    with patch.object(scanner, "_run_git_cmd", side_effect=mock_run):
        findings = scanner.scan("dummy_path")
        
        assert scanner.git_data["installed"] is True
        assert scanner.git_data["is_repository"] is True
        assert scanner.git_data["user_name"] == "test-user"
