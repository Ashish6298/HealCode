"""
Tests for Project Quality & Structure Scanner
"""

import os
import tempfile
from healcode.core.scanners.project_scanner import ProjectScanner

def test_project_scanner_issues() -> None:
    scanner = ProjectScanner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a manifest file but keep lockfile missing
        with open(os.path.join(tmpdir, "package.json"), "w", encoding="utf-8") as f:
            f.write("{}")
            
        findings = scanner.scan(tmpdir)
        
        finding_ids = {f["id"] for f in findings}
        assert "PROJ-DEP-MISSING-LOCKFILE" in finding_ids
        assert "PROJ-QUALITY-MISSING-README" in finding_ids
        assert "PROJ-IGNORE-MISSING-GITIGNORE" in finding_ids
