"""
Tests for Core Scan Engine
"""

import os
import tempfile
from healcode.core.engine import ScanEngine
from healcode.core.scanners.default_scanner import DefaultScanner
from healcode.config.models import ProjectConfig

def test_engine_scan() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a file with TODO to trigger default scanner
        todo_file = os.path.join(tmpdir, "todo.py")
        with open(todo_file, "w", encoding="utf-8") as f:
            f.write("# TODO: implement something\n")

        # Create a large file
        large_file = os.path.join(tmpdir, "large.bin")
        with open(large_file, "wb") as f:
            f.write(b"\0" * (11 * 1024 * 1024))  # 11MB

        config = ProjectConfig()
        # Exclude large file to test exclusion
        config.scan.exclude_paths = ["large.bin"]

        engine = ScanEngine(config)
        engine.register_scanner(DefaultScanner())
        findings = engine.run(tmpdir)

        # Should only find the TODO
        assert len(findings) == 1
        assert findings[0]["id"] == "TODO-FOUND"
        assert "todo.py" in findings[0]["file"]
