"""
Tests for Environment Configuration Scanner
"""

import os
import tempfile
from healcode.core.scanners.env_scanner import EnvScanner

def test_env_scanner_missing_env() -> None:
    scanner = EnvScanner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create .env.example but keep .env missing
        with open(os.path.join(tmpdir, ".env.example"), "w", encoding="utf-8") as f:
            f.write("PORT=8080\nAPI_KEY=\n")
            
        findings = scanner.scan(tmpdir)
        
        assert len(findings) == 1
        assert findings[0]["id"] == "ENV-FILE-MISSING"

def test_env_scanner_keys_drift() -> None:
    scanner = EnvScanner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, ".env.example"), "w", encoding="utf-8") as f:
            f.write("PORT=8080\nAPI_KEY=\nDB_URL=\n")
        with open(os.path.join(tmpdir, ".env"), "w", encoding="utf-8") as f:
            f.write("PORT=8080\n")
            
        findings = scanner.scan(tmpdir)
        
        assert len(findings) == 1
        assert findings[0]["id"] == "ENV-KEYS-DRIFT"
        assert "API_KEY" in findings[0]["message"]
        assert "DB_URL" in findings[0]["message"]
