#!/usr/bin/env python3
"""Generate assets/app.ico with wind/snow emoji (fallback: drawn symbol)."""
from __future__ import annotations

import math
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Install Pillow: python -m pip install pillow", file=sys.stderr)
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "app.ico")
EMOJI = "\U0001F328\U0000FE0F"  # 🌨️

FONT_CANDIDATES = [
    ("/System/Library/Fonts/Apple Color Emoji.ttc", 0),
    ("C:/Windows/Fonts/seguiemj.ttf", 0),
    ("C:/Windows/Fonts/segoeuiemoji.ttf", 0),
]


def load_emoji_font(size: int):
    for path, index in FONT_CANDIDATES:
        if os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size=size, index=index)
            except OSError:
                continue
    return None


def draw_fallback(draw: ImageDraw.ImageDraw, size: int) -> None:
    cx, cy = size / 2, size / 2
    r = size * 0.28
    white = (240, 248, 255, 255)
    light = (180, 220, 255, 220)
    for i in range(6):
        ang = math.radians(i * 60)
        x2 = cx + r * math.cos(ang)
        y2 = cy + r * math.sin(ang)
        draw.line((cx, cy, x2, y2), fill=white, width=max(1, size // 16))
        br = r * 0.35
        bx = x2 - br * math.cos(ang)
        by = y2 - br * math.sin(ang)
        draw.line((x2, y2, bx + br * math.cos(ang + 0.9), by + br * math.sin(ang + 0.9)), fill=white, width=max(1, size // 20))
        draw.line((x2, y2, bx + br * math.cos(ang - 0.9), by + br * math.sin(ang - 0.9)), fill=white, width=max(1, size // 20))
    draw.ellipse((cx - r * 0.18, cy - r * 0.18, cx + r * 0.18, cy + r * 0.18), fill=white)
    wind_y = cy + r * 0.95
    for i, dx in enumerate((-r * 0.55, 0, r * 0.45)):
        y = wind_y + i * size * 0.07
        draw.arc(
            (cx - r * 0.75 + dx, y - size * 0.08, cx + r * 0.15 + dx, y + size * 0.08),
            start=200,
            end=340,
            fill=light,
            width=max(1, size // 18),
        )


def render(size: int, use_emoji: bool) -> Image.Image:
    img = Image.new("RGBA", (size, size), (14, 51, 82, 255))
    draw = ImageDraw.Draw(img)
    if use_emoji:
        font = load_emoji_font(max(14, int(size * 0.58)))
        if font:
            draw.text((0, 0), EMOJI, font=font, embedded_color=True)
            if img.getbbox() and (img.getbbox()[2] - img.getbbox()[0]) > size * 0.2:
                return img
    draw = ImageDraw.Draw(img)
    draw_fallback(draw, size)
    return img


def main() -> None:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    use_emoji = load_emoji_font(48) is not None
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img = render(256, use_emoji)
    img.save(OUT, format="ICO", sizes=sizes)
    mode = "emoji" if use_emoji else "fallback symbol"
    print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes, {mode})")


if __name__ == "__main__":
    main()
