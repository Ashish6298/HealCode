"""
Tests for Port Scanner
"""

from unittest.mock import patch
from healcode.core.scanners.port_scanner import PortScanner

def test_port_scanner_detection() -> None:
    scanner = PortScanner()
    
    # Mock _is_port_open to simulate listening port
    with patch.object(scanner, "_is_port_open", side_effect=lambda host, port: port == 8080):
        findings = scanner.scan("dummy_path")
        
        assert len(findings) == 1
        assert findings[0]["id"] == "PORT-CONFLICT-8080"
        assert findings[0]["severity"] == "WARN"
        assert "8080" in findings[0]["message"]
