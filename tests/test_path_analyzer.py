"""
Tests for PATH Analyzer
"""

import os
from unittest.mock import patch
from healcode.core.scanners.path_analyzer import PathAnalyzer

def test_path_analyzer_scan_issues() -> None:
    analyzer = PathAnalyzer()
    
    # Mock environment variable PATH containing duplicate and nonexistent dirs
    mock_path = f"C:\\Windows;C:\\Windows;C:\\nonexistent_directory_for_healcode_test"
    
    with patch.dict(os.environ, {"PATH": mock_path}):
        findings = analyzer.scan("dummy_path")
        
        # Verify it finds the duplicate and nonexistent directory
        duplicate_found = any(f["id"] == "PATH-DUPLICATE" for f in findings)
        nonexistent_found = any(f["id"] == "PATH-NONEXISTENT" for f in findings)
        
        assert duplicate_found is True
        assert nonexistent_found is True
