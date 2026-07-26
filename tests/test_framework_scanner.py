"""
Tests for Project Framework Scanner
"""

import os
import json
import tempfile
from healcode.core.scanners.framework_scanner import FrameworkScanner

def test_framework_scanner_detection() -> None:
    scanner = FrameworkScanner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a package.json containing React dependencies
        pkg_json = os.path.join(tmpdir, "package.json")
        with open(pkg_json, "w", encoding="utf-8") as f:
            json.dump({
                "dependencies": {
                    "react": "^18.2.0"
                }
            }, f)
            
        findings = scanner.scan(tmpdir)
        
        assert len(findings) == 1
        assert findings[0]["id"] == "FW-DETECTED"
        assert "React" in findings[0]["message"]
