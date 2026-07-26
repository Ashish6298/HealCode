"""
Tests for System Scanner
"""

import sys
from healcode.core.scanners.system_scanner import SystemScanner
from healcode.config.models import ProjectConfig

def test_system_scanner_collect_info() -> None:
    scanner = SystemScanner()
    info = scanner.collect_system_info()
    
    assert "os" in info
    assert "cpu" in info
    assert "memory" in info
    assert "disks" in info
    assert "network" in info
    assert "shell" in info
    
    # Assert type characteristics
    assert isinstance(info["cpu"]["cores_physical"], int)
    assert isinstance(info["memory"]["total"], int)
    assert isinstance(info["disks"], list)
    assert len(info["disks"]) > 0

def test_system_scanner_scan() -> None:
    scanner = SystemScanner()
    findings = scanner.scan("dummy_path")
    assert isinstance(findings, list)
