"""
Tests for Cloud & Kubernetes Scanner
"""

import os
import tempfile
from healcode.core.scanners.cloud_scanner import CloudScanner

def test_cloud_scanner_detection() -> None:
    scanner = CloudScanner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a mock Chart.yaml and main.tf to test detection offline
        with open(os.path.join(tmpdir, "Chart.yaml"), "w", encoding="utf-8") as f:
            f.write("apiVersion: v2\nname: test-chart\n")
            
        with open(os.path.join(tmpdir, "main.tf"), "w", encoding="utf-8") as f:
            f.write('resource "null_resource" "dummy" {}\n')
            
        findings = scanner.scan(tmpdir)
        
        finding_ids = {f["id"] for f in findings}
        assert "CLOUD-HELM-CHART-DETECTED" in finding_ids
        assert "CLOUD-IAC-TERRAFORM-DETECTED" in finding_ids
