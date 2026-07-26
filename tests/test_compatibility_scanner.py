"""
Tests for Runtime Compatibility Scanner
"""

import os
import json
import tempfile
from healcode.core.scanners.compatibility_scanner import CompatibilityScanner
from healcode.core.scanners.runtime_scanner import RuntimeScanner

def test_compatibility_node_mismatch() -> None:
    # Set up mock installed runtimes data
    rt_scanner = RuntimeScanner()
    rt_scanner.scan = lambda target_path: []  # type: ignore
    rt_scanner.runtimes_data = {
        "node": {
            "installed": True,
            "version": "14.15.0",
            "path": "/usr/local/bin/node"
        }
    }
    
    scanner = CompatibilityScanner(runtime_scanner=rt_scanner)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a package.json requiring Node.js >= 18
        pkg_json = os.path.join(tmpdir, "package.json")
        with open(pkg_json, "w", encoding="utf-8") as f:
            json.dump({"engines": {"node": ">=18.0.0"}}, f)
            
        findings = scanner.scan(tmpdir)
        
        assert len(findings) == 1
        assert findings[0]["id"] == "COMPAT-NODE-MISMATCH"
        assert "installed version is older" in findings[0]["message"]
