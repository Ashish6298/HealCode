"""
Tests for Plugin Loader
"""

import os
import tempfile
from healcode.core.plugin_loader import PluginLoader
from healcode.config.models import ProjectConfig

MOCK_PLUGIN_CODE = """
from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig
from typing import List, Dict, Any

class MockScanner(IScanner):
    @property
    def name(self) -> str:
        return "mock-scanner"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Mock Scanner description"

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        return [{"id": "MOCK-001", "scanner": self.name, "file": target_path, "severity": "INFO", "message": "Mock triggered"}]
"""

def test_plugin_dynamic_loading() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        plugin_file = os.path.join(tmpdir, "mock_plugin.py")
        with open(plugin_file, "w", encoding="utf-8") as f:
            f.write(MOCK_PLUGIN_CODE)

        config = ProjectConfig()
        loader = PluginLoader(config)
        loader.load_plugins_from_dirs([tmpdir])

        assert "mock-scanner" in loader.plugins
        assert "mock-scanner" in loader.scanners
        scanner = loader.scanners["mock-scanner"]
        findings = scanner.scan("dummy_path")
        assert len(findings) == 1
        assert findings[0]["id"] == "MOCK-001"
