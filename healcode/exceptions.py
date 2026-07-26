"""
HealCode Custom Exceptions
"""

class HealCodeError(Exception):
    """Base class for all HealCode exceptions."""
    pass

class ConfigurationError(HealCodeError):
    """Raised when there is an issue loading or parsing configuration."""
    pass

class PluginError(HealCodeError):
    """Raised when plugin loading, registration, or execution fails."""
    pass

class ScanError(HealCodeError):
    """Raised when scanning engine or specific scanner encounters an unrecoverable error."""
    pass

class CacheError(HealCodeError):
    """Raised when cache operations fail."""
    pass
