"""
Tests for Runtime Scanner
"""

from healcode.core.scanners.runtime_scanner import RuntimeScanner

def test_runtime_scanner_detection() -> None:
    scanner = RuntimeScanner()
    findings = scanner.scan("dummy_path")
    
    assert isinstance(findings, list)
    assert "node" in scanner.runtimes_data
    assert "python" in scanner.runtimes_data
    assert "npm" in scanner.runtimes_data
    assert "pip" in scanner.runtimes_data
