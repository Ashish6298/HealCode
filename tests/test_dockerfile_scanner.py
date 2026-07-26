"""
Tests for Dockerfile Best Practices Scanner
"""

import os
import tempfile
from healcode.core.scanners.dockerfile_scanner import DockerfileScanner

def test_dockerfile_scanner_issues() -> None:
    scanner = DockerfileScanner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        dockerfile_path = os.path.join(tmpdir, "Dockerfile")
        with open(dockerfile_path, "w", encoding="utf-8") as f:
            f.write("FROM node:latest\nRUN npm install\n")
            
        findings = scanner.scan(dockerfile_path)
        
        # Should flag latest tag, missing healthcheck, and running as root
        finding_ids = {f["id"] for f in findings}
        assert "DOCKERFILE-LATEST-TAG" in finding_ids
        assert "DOCKERFILE-MISSING-HEALTHCHECK" in finding_ids
        assert "DOCKERFILE-RUNS-AS-ROOT" in finding_ids
