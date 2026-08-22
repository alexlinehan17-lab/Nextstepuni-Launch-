#!/usr/bin/env python3
"""
Mark Bank — crop the artwork a question is built on.

Some questions cannot be asked in words. "What information does each of the
following fabric care symbols convey?" is entirely a matter of reading two
pictograms, and "Comment on the suitability of the occasion wear shown above"
points at a photograph. Six Home Economics parts came back unbuildable for
exactly this reason, and under the no-skipping rule that is a missing input to
go and get, not a gap to accept.

    python3 scripts/markbank/crop-question-art.py <paper.pdf> --page 7 \
        -o exam-papers/<subject>/figures/<year>-<level>/<subject>-<year>-<LEVEL>-paper<n>-p07-art.png

Name the output with an `-art` suffix, not the extractor's `-i<n>`. Both tools
feed the same manifest, keyed by file name, and a page render saved under a name
`extract-figures.py` can also produce is a name that means two different crops.

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
# A word the SEC underlines for emphasis ("the allele for white fruit") leaves a
# flat rule in the drawing list. It is typography, not artwork, but it is a
# drawing, so it pulled one crop down over the whole of the NEXT question.
RULE_MAX_THICKNESS = 1.5
RULE_MIN_LENGTH = 20


def is_text_rule(r):
    """A flat rule of the kind an underlined word leaves behind."""
    return (r.height <= RULE_MAX_THICKNESS and r.width >= RULE_MIN_LENGTH) or (
        r.width <= RULE_MAX_THICKNESS and r.height >= RULE_MIN_LENGTH
    )


def drawn_points(page):
    """Every point on a curved or diagonal stroke.

    An answer box and a table grid are ruled: their every stroke is horizontal
    or vertical. A chart is not. This is what separates a wide chart FRAME from
    a wide answer box, which are otherwise the same rectangle.
    """
    pts = []
    for d in page.get_drawings():
        for it in d["items"]:
            if it[0] == "c":
                pts.extend(it[1:])
            elif it[0] == "l":
                a, b = it[1], it[2]
                if abs(a.x - b.x) > 3 and abs(a.y - b.y) > 3:
                    pts.extend((a, b))
    return pts


def art_box(page, ignore_rules=False, keep_charts=False):
    """The union of the page's real artwork, excluding answer-box rules."""
    boxes = []
    drawn = drawn_points(page) if keep_charts else []
    for d in page.get_drawings():
        r = fitz.Rect(d["rect"])
        if r.is_empty:
            continue
        if r.width > page.rect.width * BOX_MIN_WIDTH_FRACTION and r.height > 8:
            # A chart drawn on the page rather than pasted in as an image is
            # framed by a rectangle as wide as an answer box, and was being
            # thrown away as one - the 2021 Higher ECB interest-rate chart came
            # out as its own bottom axis and nothing else. A frame with a curve
            # or a diagonal inside it is artwork.
            if keep_charts and any(p in r for p in drawn):
                boxes.append(r)
            continue          # a ruled answer box, not artwork
        if r.width < 3 and r.height < 3:
            continue          # a stray rule or tick
        if ignore_rules and is_text_rule(r):
            continue          # an underlined word, not artwork
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
    ap.add_argument(
        "--keep-charts",
        action="store_true",
        help="keep a wide framed rectangle when it has a curved or diagonal stroke "
             "inside it, i.e. it is a chart drawn on the page rather than an answer "
             "box. Opt-in, so no crop produced before this existed can change.",
    )
    ap.add_argument(
        "--pad-top", type=float, default=0.0,
        help="extra points of page above the artwork. The extent is taken from the "
             "drawings and images, so a label printed ABOVE them — the A, B and C over "
             "a row of breed photographs — falls outside it and is cropped away, "
             "leaving a card that asks about letters it does not show. Opt-in and "
             "zero by default, so no crop taken before this existed can change.",
    )
    ap.add_argument(
        "--ignore-rules",
        action="store_true",
        help="drop flat rules (underlined words) from the artwork extent. Opt-in, "
             "so crops taken before it existed still reproduce byte for byte.",
    )
    args = ap.parse_args()
    if fitz is None:
        print("PyMuPDF is required", file=sys.stderr)
        return 1

    doc = fitz.open(args.paper)
    page = doc[args.page - 1]
    box = art_box(page, ignore_rules=args.ignore_rules, keep_charts=args.keep_charts)
    if box is None:
        print(f"no artwork found on page {args.page}", file=sys.stderr)
        return 3
    # Keep the attribution the SEC prints beneath each symbol.
    box = fitz.Rect(box.x0 - PAD, box.y0 - PAD - args.pad_top,
                    box.x1 + PAD, box.y1 + PAD * 2.5) & page.rect
    pix = page.get_pixmap(clip=box, matrix=fitz.Matrix(args.scale, args.scale))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    pix.save(args.out)
    print(f"{args.out}  {pix.width}x{pix.height}  from page {args.page}")
    doc.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
