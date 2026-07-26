"""
Tests for Configuration Manager
"""

import os
import tempfile
from healcode.config.manager import ConfigManager
from healcode.config.models import ProjectConfig

def test_default_config() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ConfigManager(project_dir=tmpdir)
        cfg = manager.load()
        assert isinstance(cfg, ProjectConfig)
        assert cfg.logging.level == "INFO"
        assert cfg.cache.enabled is True
        assert cfg.cache.ttl == 3600

def test_config_save_load() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ConfigManager(project_dir=tmpdir)
        cfg = manager.load()
        cfg.logging.level = "DEBUG"
        cfg.scan.max_depth = 10
        manager.save_project_config()

        # Reload
        new_manager = ConfigManager(project_dir=tmpdir)
        new_cfg = new_manager.load()
        assert new_cfg.logging.level == "DEBUG"
        assert new_cfg.scan.max_depth == 10
