"""
Tests for OS Detector
"""

from healcode.utils.os_detector import get_os_info, OSInfo

def test_os_detector_fields() -> None:
    info = get_os_info()
    assert isinstance(info, OSInfo)
    assert hasattr(info, "system")
    assert hasattr(info, "release")
    assert hasattr(info, "version")
    assert hasattr(info, "machine")
    assert hasattr(info, "is_windows")
    assert hasattr(info, "is_mac")
    assert hasattr(info, "is_linux")
    assert hasattr(info, "is_wsl")
    assert isinstance(info.to_dict(), dict)
    assert isinstance(info.friendly_name(), str)
