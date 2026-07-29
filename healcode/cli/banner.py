"""
HealCode Banner Definition
"""

from typing import List


class BannerDefinition:
    # Block-style ASCII art that spells HEALCODE in the splash banner.
    FULL_BANNER: List[str] = [
    "██╗  ██╗███████╗ █████╗ ██╗      ██████╗ ██████╗ ██████╗ ███████╗",
    "██║  ██║██╔════╝██╔══██╗██║     ██╔════╝██╔═══██╗██╔══██╗██╔════╝",
    "███████║█████╗  ███████║██║     ██║     ██║   ██║██║  ██║█████╗  ",
    "██╔══██║██╔══╝  ██╔══██║██║     ██║     ██║   ██║██║  ██║██╔══╝  ",
    "██║  ██║███████╗██║  ██║███████╗╚██████╗╚██████╔╝██████╔╝███████╗",
    "╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝",
]

    COMPACT_BANNER: List[str] = [
        "HEALCODE",
        "Diagnose. Fix. Optimize. Heal.",
    ]

    @classmethod
    def get_banner_lines(cls, compact: bool = False) -> List[str]:
        if compact:
            return cls.COMPACT_BANNER

        return [
            *cls.FULL_BANNER,
            "",
            "  Diagnose. Fix. Optimize. Heal.",
        ]
