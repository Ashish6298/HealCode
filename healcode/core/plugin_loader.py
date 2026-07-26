"""
HealCode Dynamic Plugin Loader
"""

import os
import sys
import importlib.util
import inspect
from typing import List, Type, Dict
from healcode.core.interfaces import IPlugin, IScanner
from healcode.exceptions import PluginError
from healcode.config.models import ProjectConfig
from healcode.utils.logger import HealCodeLogger

logger = HealCodeLogger.get_logger()

class PluginLoader:
    def __init__(self, config: ProjectConfig) -> None:
        self.config = config
        self.plugins: Dict[str, IPlugin] = {}
        self.scanners: Dict[str, IScanner] = {}

    def load_plugins_from_dirs(self, dirs: List[str]) -> None:
        """Dynamically loads python plugins from directories."""
        for directory in dirs:
            abs_dir = os.path.abspath(directory)
            if not os.path.isdir(abs_dir):
                logger.warning(f"Plugin directory not found: {abs_dir}")
                continue

            logger.debug(f"Scanning for plugins in: {abs_dir}")
            for filename in os.listdir(abs_dir):
                if filename.endswith(".py") and not filename.startswith("__"):
                    filepath = os.path.join(abs_dir, filename)
                    try:
                        self._load_plugin_file(filepath)
                    except Exception as e:
                        logger.error(f"Failed to load plugin from {filepath}: {e}")

    def _load_plugin_file(self, filepath: str) -> None:
        module_name = os.path.splitext(os.path.basename(filepath))[0]
        
        # Avoid module name collisions
        unique_module_name = f"healcode.dynamic_plugins.{module_name}"
        
        spec = importlib.util.spec_from_file_location(unique_module_name, filepath)
        if not spec or not spec.loader:
            raise PluginError(f"Could not load spec for plugin: {filepath}")
            
        module = importlib.util.module_from_spec(spec)
        sys.modules[unique_module_name] = module
        
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            raise PluginError(f"Execution error loading plugin module {module_name}: {e}")

        # Scan module for classes implementing IPlugin
        loaded_any = False
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Must subclass IPlugin or IScanner and not be the interface itself
            if issubclass(obj, IPlugin) and obj not in (IPlugin, IScanner):
                # Ensure it has a parameterless constructor or standard constructor
                try:
                    instance = obj()
                    
                    # Check if disabled
                    if instance.name in self.config.plugins.disabled_plugins:
                        logger.info(f"Plugin '{instance.name}' is disabled in configuration.")
                        continue

                    # Initialize plugin
                    instance.initialize(self.config)
                    
                    # Register plugin
                    self.plugins[instance.name] = instance
                    if isinstance(instance, IScanner):
                        self.scanners[instance.name] = instance
                        
                    logger.debug(f"Successfully loaded and registered plugin: {instance.name} (v{instance.version})")
                    loaded_any = True
                except Exception as e:
                    logger.error(f"Error instantiating plugin class {name} from {filepath}: {e}")

        if not loaded_any:
            logger.warning(f"No valid IPlugin implementations found in {filepath}")
