#!/usr/bin/env python3
"""
Mark Bank — crop the artwork a question is built on.

Some questions cannot be asked in words. "What information does each of the
following fabric care symbols convey?" is entirely a matter of reading two
pictograms, and "Comment on the suitability of the occasion wear shown above"
points at a photograph. Six Home Economics parts came back unbuildable for
exactly this reason, and under the no-skipping rule that is a missing input to
go and get, not a gap to accept.

    python3 scripts/markbank/crop-question-art.py <paper.pdf> --page 7 -o out.png

The general figure extractor was built for diagrams that sit in a band of the
page, and on these it clipped the second of two symbols — the question asks about
both. This takes the artwork's OWN extent instead: the union of every vector
drawing and raster image on the page, minus the answer-box rules, padded a
little. The attribution line the SEC prints under each symbol is kept, because it
is part of what was printed and a student sees it.
"""

import argparse
import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    fitz = None

PAD = 10
# An answer box is a wide, empty ruled rectangle. It is not the artwork, and
# including it drags the crop across the page and shrinks the symbols.
BOX_MIN_WIDTH_FRACTION = 0.30


def art_box(page):
    """The union of the page's real artwork, excluding answer-box rules."""
    boxes = []
    for d in page.get_drawings():
        r = fitz.Rect(d["rect"])
        if r.is_empty:
            continue
        if r.width > page.rect.width * BOX_MIN_WIDTH_FRACTION and r.height > 8:
            continue          # a ruled answer box, not artwork
        if r.width < 3 and r.height < 3:
            continue          # a stray rule or tick
        boxes.append(r)
    for img in page.get_images(full=True):
        for r in page.get_image_rects(img[0]):
            boxes.append(fitz.Rect(r))
    if not boxes:
        return None
    box = boxes[0]
    for r in boxes[1:]:
        box |= r
    return box


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paper", type=Path)
    ap.add_argument("--page", type=int, required=True, help="1-based")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--scale", type=float, default=3.0)
    args = ap.parse_args()
    if fitz is None:
        print("PyMuPDF is required", file=sys.stderr)
        return 1

    doc = fitz.open(args.paper)
    page = doc[args.page - 1]
    box = art_box(page)
    if box is None:
        print(f"no artwork found on page {args.page}", file=sys.stderr)
        return 3
    # Keep the attribution the SEC prints beneath each symbol.
    box = fitz.Rect(box.x0 - PAD, box.y0 - PAD, box.x1 + PAD, box.y1 + PAD * 2.5) & page.rect
    pix = page.get_pixmap(clip=box, matrix=fitz.Matrix(args.scale, args.scale))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    pix.save(args.out)
    print(f"{args.out}  {pix.width}x{pix.height}  from page {args.page}")
    doc.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
