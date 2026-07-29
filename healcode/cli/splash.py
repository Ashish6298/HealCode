"""
HealCode Splash Screen Subsystem
"""

import os
import sys
from typing import List, Optional
from healcode.config.models import ProjectConfig
from healcode.cli.banner import BannerDefinition
from healcode.cli.renderer import BannerRenderer
from healcode.cli.animation import BannerAnimation
from healcode.utils.ui import console


CI_ENV_VARS = [
    "CI",
    "GITHUB_ACTIONS",
    "GITLAB_CI",
    "BUILDKITE",
    "AZURE_HTTP_USER_AGENT",
    "TF_BUILD",
]


class SplashManager:
    _displayed = False

    def __init__(self, config: ProjectConfig, no_banner: bool = False, json_mode: bool = False) -> None:
        self.config = config
        self.no_banner = no_banner
        self.json_mode = json_mode
        self.renderer = BannerRenderer(
            theme=self.config.branding.theme,
            alignment=self.config.branding.alignment,
        )
        self.animation = BannerAnimation(
            console=console,
            enable=self.config.branding.enable_animation,
            speed=self.config.branding.animation_speed,
        )

    @classmethod
    def has_been_displayed(cls) -> bool:
        return cls._displayed

    @classmethod
    def reset(cls) -> None:
        cls._displayed = False

    def _is_ci(self) -> bool:
        return any(os.getenv(key) for key in CI_ENV_VARS)

    def _is_interactive(self) -> bool:
        return sys.stdout.isatty() and console.is_terminal

    def _should_render(self) -> bool:
        if self.no_banner:
            return False
        if self.json_mode:
            return False
        if self._is_ci():
            return False
        if not self._is_interactive():
            return False
        if not self.config.branding.show_banner:
            return False
        return True

    def display(self) -> None:
        if SplashManager._displayed:
            return
        if not self._should_render():
            SplashManager._displayed = True
            return

        compact = self.config.branding.compact_mode or self.renderer.get_terminal_width() < 80
        lines = BannerDefinition.get_banner_lines(compact=compact)
        rendered = self.renderer.render(lines, compact=compact)
        self.animation.play(rendered)
        SplashManager._displayed = True
