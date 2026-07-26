"""
HealCode Core Scanning Engine
"""

import os
from typing import List, Dict, Any, Optional
from healcode.config.models import ProjectConfig
from healcode.core.interfaces import IScanner
from healcode.core.plugin_loader import PluginLoader
from healcode.core.cache import CacheManager
from healcode.utils.logger import HealCodeLogger

logger = HealCodeLogger.get_logger()

class ScanEngine:
    def __init__(self, config: ProjectConfig, cache_manager: Optional[CacheManager] = None) -> None:
        self.config = config
        self.plugin_loader = PluginLoader(self.config)
        self.cache_manager = cache_manager
        
        # Load core scanners dynamically if configured
        if self.config.plugins.plugin_dirs:
            self.plugin_loader.load_plugins_from_dirs(self.config.plugins.plugin_dirs)

    def register_scanner(self, scanner: IScanner) -> None:
        self.plugin_loader.scanners[scanner.name] = scanner
        self.plugin_loader.plugins[scanner.name] = scanner

    def run(self, target_path: str) -> List[Dict[str, Any]]:
        """Runs all registered scanners on target_path, with caching support."""
        target_path = os.path.abspath(target_path)
        logger.info(f"Starting scan engine on target: {target_path}")

        # Check cache if enabled
        import sys
        cache_key = f"scan:{target_path}:{hash(frozenset(self.plugin_loader.scanners.keys()))}:{sys.version_info.major}.{sys.version_info.minor}"
        if self.config.cache.enabled and self.cache_manager:
            cached_findings = self.cache_manager.get(cache_key, target_path)
            if cached_findings is not None:
                logger.info("Found cached scan results, skipping live scan.")
                return cached_findings

        all_findings: List[Dict[str, Any]] = []

        # Walk target_path if it's a directory
        targets = []
        if os.path.isdir(target_path):
            for root, dirs, files in os.walk(target_path):
                # Filter excluded paths
                dirs[:] = [d for d in dirs if not self._is_excluded(os.path.join(root, d))]
                
                # Check max depth
                depth = root[len(target_path):].count(os.sep)
                if depth >= self.config.scan.max_depth:
                    continue

                for file in files:
                    file_path = os.path.join(root, file)
                    if not self._is_excluded(file_path):
                        targets.append(file_path)
        else:
            if not self._is_excluded(target_path):
                targets.append(target_path)

        # Run registered scanners
        total_scanners = len(self.plugin_loader.scanners)
        logger.info(f"Running {total_scanners} scanners across {len(targets)} files.")

        for scanner_name, scanner in self.plugin_loader.scanners.items():
            logger.debug(f"Running scanner: {scanner_name}")
            if getattr(scanner, "is_global", False):
                try:
                    findings = scanner.scan(target_path)
                    all_findings.extend(findings)
                except Exception as e:
                    logger.error(f"Error during global scan by {scanner_name}: {e}")
            else:
                for target in targets:
                    try:
                        findings = scanner.scan(target)
                        all_findings.extend(findings)
                    except Exception as e:
                        logger.error(f"Error during scan by {scanner_name} on {target}: {e}")

        # Cache results if enabled
        if self.config.cache.enabled and self.cache_manager:
            self.cache_manager.set(cache_key, all_findings, self.config.cache.ttl, target_path)

        return all_findings

    def _is_excluded(self, path: str) -> bool:
        norm_path = os.path.normpath(path)
        for pattern in self.config.scan.exclude_paths:
            if pattern in norm_path or norm_path.endswith(pattern):
                return True
        # Always exclude venv, git, and cache db
        for default_exclude in [".git", "venv", ".healcode_cache.db"]:
            if default_exclude in norm_path:
                return True
        return False
