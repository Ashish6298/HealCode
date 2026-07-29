"""
Tests for the HealCode startup splash screen subsystem.
"""

import sys
from unittest.mock import patch, MagicMock
from healcode.cli.splash import SplashManager
from healcode.cli.gradient import build_gradient, build_palette
from healcode.config.models import ProjectConfig, BrandingConfig, LoggingConfig, CacheConfig, ScanConfig, PluginConfig, AIConfig


def test_banner_gradient_builds_expected_length() -> None:
    palette = build_palette("cyberpunk")
    gradient = build_gradient(20, palette)
    assert len(gradient) == 20
    assert gradient[0].startswith("#")
    assert gradient[-1].startswith("#")


def test_splash_config_default() -> None:
    config = ProjectConfig(
        logging=LoggingConfig(),
        cache=CacheConfig(),
        scan=ScanConfig(),
        plugins=PluginConfig(),
        branding=BrandingConfig(),
        ai=AIConfig(),
    )
    assert config.branding.show_banner is True
    assert config.branding.enable_animation is True
    assert config.branding.animation_speed == "fast"
    assert config.branding.theme == "cyberpunk"
    assert config.branding.compact_mode is False


def test_splash_manager_disables_banner_when_no_banner_flag(monkeypatch) -> None:
    config = ProjectConfig(branding=BrandingConfig())
    manager = SplashManager(config=config, no_banner=True, json_mode=False)
    monkeypatch.setattr(manager, "_is_ci", lambda: False)
    monkeypatch.setattr(manager, "_is_interactive", lambda: True)
    with patch.object(manager, "animation") as animation_mock:
        manager.display()
        animation_mock.play.assert_not_called()


def test_splash_manager_renders_only_once(monkeypatch) -> None:
    config = ProjectConfig(branding=BrandingConfig())
    manager = SplashManager(config=config, no_banner=False, json_mode=False)
    monkeypatch.setattr(manager, "_is_ci", lambda: False)
    monkeypatch.setattr(manager, "_is_interactive", lambda: True)
    with patch("healcode.cli.splash.BannerDefinition.get_banner_lines", return_value=["A"]), \
         patch.object(manager.renderer, "render", return_value=[MagicMock()]) as render_mock, \
         patch.object(manager.animation, "play", return_value=None) as play_mock:
        SplashManager.reset()
        manager.display()
        manager.display()
        assert render_mock.call_count == 1
        assert play_mock.call_count == 1


def test_splash_manager_disables_in_json_mode(monkeypatch) -> None:
    config = ProjectConfig(branding=BrandingConfig())
    manager = SplashManager(config=config, no_banner=False, json_mode=True)
    monkeypatch.setattr(manager, "_is_ci", lambda: False)
    monkeypatch.setattr(manager, "_is_interactive", lambda: True)
    with patch.object(manager, "animation") as animation_mock:
        manager.display()
        animation_mock.play.assert_not_called()
