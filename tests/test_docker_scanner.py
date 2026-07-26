"""
Tests for Docker Scanner
"""

from unittest.mock import patch
from healcode.core.scanners.docker_scanner import DockerScanner

def test_docker_scanner_detection() -> None:
    scanner = DockerScanner()
    
    # Mock _run_docker_cmd to simulate daemon versions
    def mock_run(args):
        if "version" in args:
            return "24.0.7"
        if "ps" in args:
            return "test-container"
        return ""

    with patch.object(scanner, "_run_docker_cmd", side_effect=mock_run):
        findings = scanner.scan("dummy_path")
        
        assert scanner.docker_data["installed"] is True
        assert scanner.docker_data["daemon_running"] is True
        assert scanner.docker_data["version"] == "24.0.7"
        assert len(findings) == 1
        assert findings[0]["id"] == "DOCKER-CONTAINER-UNHEALTHY"
