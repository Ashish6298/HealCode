"""
Tests for Code Intelligence & Static Analysis Scanner
"""

import os
import tempfile
from healcode.core.scanners.code_scanner import CodeScanner

def test_code_scanner_detection() -> None:
    scanner = CodeScanner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a file containing highly nested loops (smell detection)
        code_file = os.path.join(tmpdir, "nested.py")
        with open(code_file, "w", encoding="utf-8") as f:
            f.write(
                "def process():\n"
                "    for i in range(10):\n"
                "        for j in range(10):\n"
                "            for k in range(10):\n"
                "                for l in range(10):\n"
                "                    print(i, j, k, l)\n"
            )
            
        findings = scanner.scan(code_file)
        
        finding_ids = {f["id"] for f in findings}
        assert "CODE-COMPLEX-NESTING" in finding_ids
        assert "CODE-PERF-NESTED-LOOP" in finding_ids
