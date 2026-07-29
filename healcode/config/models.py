"""
HealCode Configuration Models
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class LoggingConfig:
    level: str = "INFO"
    json_format: bool = False

@dataclass
class CacheConfig:
    enabled: bool = True
    ttl: int = 3600  # Default 1 hour
    db_path: str = ".healcode_cache.db"

@dataclass
class ScanConfig:
    exclude_paths: List[str] = field(default_factory=list)
    max_depth: int = 5
    rules_enabled: List[str] = field(default_factory=list)
    profile: str = "Full"

@dataclass
class PluginConfig:
    plugin_dirs: List[str] = field(default_factory=list)
    disabled_plugins: List[str] = field(default_factory=list)

@dataclass
class BrandingConfig:
    show_banner: bool = True
    enable_animation: bool = True
    animation_speed: str = "fast"
    theme: str = "cyberpunk"
    compact_mode: bool = False
    color_scheme: str = "neon"
    alignment: str = "left"

@dataclass
class AIConfig:
    """Configuration for the optional AI Intelligence layer."""
    enabled: bool = False
    provider: str = "offline"
    model: str = ""
    offline_mode: bool = True
    mask_secrets: bool = True
    temperature: float = 0.2
    max_tokens: int = 2048
    timeout: int = 30
    retry_count: int = 2
    local_endpoint: str = ""

@dataclass
class ProjectConfig:
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    scan: ScanConfig = field(default_factory=ScanConfig)
    plugins: PluginConfig = field(default_factory=PluginConfig)
    branding: BrandingConfig = field(default_factory=BrandingConfig)
    ai: AIConfig = field(default_factory=AIConfig)

