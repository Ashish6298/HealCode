"""
HealCode Banner Gradient Engine
"""

from typing import List, Tuple, Dict

Color = Tuple[int, int, int]
_gradient_cache: Dict[Tuple[int, Tuple[Color, ...]], List[str]] = {}


def _clamp(value: int) -> int:
    return max(0, min(255, value))


def _interpolate(start: Color, end: Color, fraction: float) -> Color:
    return (
        _clamp(int(start[0] + (end[0] - start[0]) * fraction)),
        _clamp(int(start[1] + (end[1] - start[1]) * fraction)),
        _clamp(int(start[2] + (end[2] - start[2]) * fraction)),
    )


def rgb_to_hex(color: Color) -> str:
    return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"


def build_gradient(length: int, palette: List[Color]) -> List[str]:
    if length <= 0 or not palette:
        return []

    cache_key = (length, tuple(palette))
    if cache_key in _gradient_cache:
        return _gradient_cache[cache_key]

    gradients: List[str] = []
    segments = max(len(palette) - 1, 1)
    base_size = length // segments
    remainder = length % segments
    index = 0

    for segment_index in range(segments):
        start = palette[segment_index]
        end = palette[min(segment_index + 1, len(palette) - 1)]
        segment_size = base_size + (1 if segment_index < remainder else 0)
        if segment_size <= 0:
            continue

        for offset in range(segment_size):
            fraction = offset / max(segment_size - 1, 1)
            color = _interpolate(start, end, fraction)
            gradients.append(rgb_to_hex(color))
            index += 1

    gradients = gradients[:length]
    while len(gradients) < length:
        gradients.append(rgb_to_hex(palette[-1]))

    _gradient_cache[cache_key] = gradients
    return gradients


def build_palette(theme: str = "cyberpunk") -> List[Color]:
    if theme == "cyberpunk":
        return [
            (188, 87, 255),
            (117, 170, 255),
            (78, 255, 189),
            (255, 171, 84),
            (255, 85, 196),
        ]

    if theme == "sunrise":
        return [
            (255, 110, 141),
            (255, 210, 107),
            (104, 243, 207),
        ]

    return [
        (180, 114, 255),
        (92, 206, 255),
        (77, 255, 192),
    ]
