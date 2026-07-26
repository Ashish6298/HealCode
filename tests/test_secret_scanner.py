"""
Tests for Sensitive Information Detection Scanner
"""

import os
import tempfile
from healcode.core.scanners.secret_scanner import SecretScanner

def test_secret_scanner_detection() -> None:
    scanner = SecretScanner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a file containing a mock secret
        secret_file = os.path.join(tmpdir, "config.py")
        with open(secret_file, "w", encoding="utf-8") as f:
            f.write('API_KEY = "super_secret_token_12345"\n')
            
        findings = scanner.scan(secret_file)
        
        assert len(findings) == 1
        assert findings[0]["id"] == "SECRET-API-KEY"
        # Make sure the secret itself is masked and not printed in message
        assert "super_secret_token_12345" not in findings[0]["message"]
        assert "********" in findings[0]["message"]
