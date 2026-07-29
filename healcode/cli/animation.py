"""
HealCode Banner Animation
"""

import os
import time
from typing import List
from rich.text import Text
from rich.console import Console


class BannerAnimation:
    def __init__(self, console: Console, enable: bool = True, speed: str = "fast") -> None:
        self.console = console
        self.enable = enable and console.is_terminal
        self.speed = speed
        self.duration_ms = self._duration_from_speed(speed)

    def _duration_from_speed(self, speed: str) -> int:
        if speed == "instant":
            return 0
        if speed == "slow":
            return 700
        if speed == "medium":
            return 450
        return 320

    def play(self, rendered_lines: List[Text]) -> None:
        if not self.enable or self.duration_ms <= 0:
            for line in rendered_lines:
                self.console.print(line)
            return

        frames = len(rendered_lines)
        delay = self.duration_ms / max(frames, 1) / 1000.0
        for index, line in enumerate(rendered_lines):
            self.console.print(line)
            if index < frames - 1:
                time.sleep(delay)

    def play_heartbeat(self, frames: List[Text]) -> None:
        for frame in frames:
            self.console.print(frame)
            time.sleep(0.06)
