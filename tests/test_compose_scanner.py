"""
Tests for Docker Compose Scanner
"""

import os
import tempfile
from healcode.core.scanners.compose_scanner import ComposeScanner

def test_compose_scanner_missing_restart() -> None:
    scanner = ComposeScanner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        compose_path = os.path.join(tmpdir, "docker-compose.yml")
        with open(compose_path, "w", encoding="utf-8") as f:
            f.write("version: '3'\nservices:\n  web:\n    image: nginx\n")
            
        findings = scanner.scan(compose_path)
        
        assert len(findings) == 1
        assert findings[0]["id"] == "COMPOSE-MISSING-RESTART"
        assert "web" in findings[0]["message"]
