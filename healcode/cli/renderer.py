"""
HealCode Banner Renderer
"""

import os
from typing import List, Optional
from rich.console import Console
from rich.text import Text
from rich.style import Style
from healcode.cli.gradient import build_gradient, build_palette
from healcode.cli.banner import BannerDefinition
from healcode.utils.ui import console


class BannerRenderer:
    def __init__(self, console_obj: Console = console, theme: str = "cyberpunk", alignment: str = "left") -> None:
        self.console = console_obj
        self.theme = theme
        self.alignment = alignment.lower()

    def supports_rgb(self) -> bool:
        return self.console.color_system == "truecolor"

    def supports_color(self) -> bool:
        return self.console.color_system is not None

    def get_terminal_width(self) -> int:
        try:
            return max(self.console.size.width, 40)
        except Exception:
            return int(os.environ.get("COLUMNS", 80))

    def render(self, lines: List[str], compact: bool = False) -> List[Text]:
        width = self.get_terminal_width()
        output: List[Text] = []
        palette = build_palette(self.theme)

        for line in lines:
            if not self.supports_color():
                styled = Text(line)
            else:
                styled = self._gradient_text(line, palette)
            output.append(self._align_text(styled, width))

        return output

    def _gradient_text(self, line: str, palette: List[tuple]) -> Text:
        text = Text()
        gradient_colors = build_gradient(max(len(line), 1), palette)
        for index, char in enumerate(line):
            color = gradient_colors[index]
            if char == " ":
                text.append(char)
            else:
                text.append(char, Style(color=color, bold=True))
        return text

    def _align_text(self, text: Text, width: int) -> Text:
        if len(text.plain) >= width:
            return text
        if self.alignment == "center":
            padding = (width - len(text.plain)) // 2
            return Text(" " * padding) + text
        return text

    def print(self, rendered_lines: List[Text]) -> None:
        for line in rendered_lines:
            self.console.print(line)
