#!/usr/bin/env python3
"""Bake the Journey island's magenta matte into real alpha, at display size.

The tile and sticker WebPs were generated on a magenta matte with no alpha
channel, and the island keyed them out at display time with a per-element SVG
filter (feColorMatrix `-3 6 -3 0 2` on the alpha row, then feComposite `in`).
WebKit runs those filters on the CPU and re-runs them whenever the map's
viewBox changes, which made dragging the island crawl on school iPads.

This applies the SAME key once, offline, in sRGB 0..1:

    A = clamp(2 + 6G - 3R - 3B, 0, 1), RGB unchanged

so the art looks as it did, then resizes with premultiplied alpha (no matte
bleeding into the edges) and writes lossy WebP with lossless-quality alpha.
It also re-encodes the two painted atlases as WebP at their original size.

Outputs go to NEW paths: browsers and the service worker cache the old URLs,
and an old RGB file drawn by filter-less code would show a magenta square.

    python3 scripts/bake-journey-art-alpha.py            # everything
    python3 scripts/bake-journey-art-alpha.py stickers   # one folder
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageMath

ROOT = Path(__file__).resolve().parent.parent / "public"
JOBS = [
    # (source folder, output folder, output edge in px; None keeps the size)
    # Tiles never draw wider than ~510 device px (the tile detail panel on a
    # 3x phone). Stickers keep their 900 px: the discovery panel shows them at
    # ~340 CSS px, which is ~1000 device px on a phone.
    ("journey-art/tiles", "journey-art/tiles-v2", 512),
    ("journey-art/stickers", "journey-art/stickers-v2", None),
]
ATLASES = [
    "art/journey-atlas-stickers/2026-09-13/pencil-map.png",
    "journey-art/atlas-directions/pencilatlas.png",
]
QUALITY = 88
ATLAS_QUALITY = 90


def key_magenta(image: Image.Image) -> Image.Image:
    """Reproduce the display-time filter: alpha from 2 + 6G - 3R - 3B."""
    r, g, b = image.convert("RGB").split()
    # In 0..255 units: 255 * (2 + 6g - 3r - 3b) = 510 + 6G - 3R - 3B.
    alpha = ImageMath.lambda_eval(
        lambda m: m["convert"](m["min"](m["max"](510 + m["g"] * 6 - m["r"] * 3 - m["b"] * 3, 0), 255), "L"),
        r=r, g=g, b=b,
    )
    return Image.merge("RGBA", (r, g, b, alpha))


def bake(source: Path, target: Path, edge: int | None) -> None:
    keyed = key_magenta(Image.open(source))
    if edge and keyed.size != (edge, edge):
        keyed = keyed.convert("RGBa").resize((edge, edge), Image.LANCZOS).convert("RGBA")
    keyed.save(target, "WEBP", quality=QUALITY, alpha_quality=100, method=6)


def main(only: str | None = None) -> None:
    for src_dir, out_dir, edge in JOBS:
        if only and only not in src_dir:
            continue
        out = ROOT / out_dir
        out.mkdir(parents=True, exist_ok=True)
        for source in sorted((ROOT / src_dir).glob("*.webp")):
            bake(source, out / source.name, edge)
            print(f"{out_dir}/{source.name}")
    if only:
        return
    for atlas in ATLASES:
        source = ROOT / atlas
        target = source.with_suffix(".webp")
        Image.open(source).convert("RGB").save(target, "WEBP", quality=ATLAS_QUALITY, method=6)
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    import sys

    main(sys.argv[1] if len(sys.argv) > 1 else None)
