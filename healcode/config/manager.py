"""
HealCode Configuration Manager
"""

import os
import json
from typing import Optional, Dict, Any
from healcode.config.models import ProjectConfig, LoggingConfig, CacheConfig, ScanConfig, PluginConfig
from healcode.exceptions import ConfigurationError
from healcode.utils.logger import HealCodeLogger

logger = HealCodeLogger.get_logger()

class ConfigManager:
    def __init__(self, project_dir: str = ".") -> None:
        self.project_dir = os.path.abspath(project_dir)
        self.project_config_path = os.path.join(self.project_dir, "healcode.json")
        self.global_config_path = os.path.expanduser("~/.healcode/config.json")
        self.config: ProjectConfig = ProjectConfig()

    def load(self) -> ProjectConfig:
        """Loads configuration from global config and merges with project config."""
        # 1. Start with default
        merged_data: Dict[str, Any] = {}

        # 2. Load global config
        if os.path.exists(self.global_config_path):
            try:
                with open(self.global_config_path, "r", encoding="utf-8") as f:
                    global_data = json.load(f)
                    if isinstance(global_data, dict):
                        merged_data.update(global_data)
            except Exception as e:
                raise ConfigurationError(f"Failed to read global config: {e}")

        # 3. Load project config
        if os.path.exists(self.project_config_path):
            try:
                with open(self.project_config_path, "r", encoding="utf-8") as f:
                    project_data = json.load(f)
                    if isinstance(project_data, dict):
                        # Merge dictionaries nested
                        self._deep_merge(merged_data, project_data)
            except Exception as e:
                raise ConfigurationError(f"Failed to read project config: {e}")

        # 4. Bind to models
        try:
            self.config = self._dict_to_model(merged_data)
        except Exception as e:
            raise ConfigurationError(f"Configuration validation failed: {e}")

        return self.config

    def _deep_merge(self, dest: Dict[str, Any], src: Dict[str, Any]) -> None:
        for key, value in src.items():
            if isinstance(value, dict) and key in dest and isinstance(dest[key], dict):
                self._deep_merge(dest[key], value)
            else:
                dest[key] = value

    def _dict_to_model(self, data: Dict[str, Any]) -> ProjectConfig:
        log_data = data.get("logging", {})
        cache_data = data.get("cache", {})
        scan_data = data.get("scan", {})
        plugin_data = data.get("plugins", {})

        logging_cfg = LoggingConfig(
            level=log_data.get("level", "INFO"),
            json_format=log_data.get("json_format", False)
        )
        cache_cfg = CacheConfig(
            enabled=cache_data.get("enabled", True),
            ttl=cache_data.get("ttl", 3600),
            db_path=cache_data.get("db_path", ".healcode_cache.db")
        )
        scan_cfg = ScanConfig(
            exclude_paths=scan_data.get("exclude_paths", []),
            max_depth=scan_data.get("max_depth", 5),
            rules_enabled=scan_data.get("rules_enabled", [])
        )
        plugin_cfg = PluginConfig(
            plugin_dirs=plugin_data.get("plugin_dirs", []),
            disabled_plugins=plugin_data.get("disabled_plugins", [])
        )

        return ProjectConfig(
            logging=logging_cfg,
            cache=cache_cfg,
            scan=scan_cfg,
            plugins=plugin_cfg
        )

    def save_project_config(self) -> None:
        """Saves current configuration to project healcode.json."""
        try:
            os.makedirs(self.project_dir, exist_ok=True)
            data = self._model_to_dict(self.config)
            with open(self.project_config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            raise ConfigurationError(f"Failed to save project config: {e}")

    def _model_to_dict(self, model: ProjectConfig) -> Dict[str, Any]:
        return {
            "logging": {
                "level": model.logging.level,
                "json_format": model.logging.json_format
            },
            "cache": {
                "enabled": model.cache.enabled,
                "ttl": model.cache.ttl,
                "db_path": model.cache.db_path
            },
            "scan": {
                "exclude_paths": model.scan.exclude_paths,
                "max_depth": model.scan.max_depth,
                "rules_enabled": model.scan.rules_enabled
            },
            "plugins": {
                "plugin_dirs": model.plugins.plugin_dirs,
                "disabled_plugins": model.plugins.disabled_plugins
            }
        }
