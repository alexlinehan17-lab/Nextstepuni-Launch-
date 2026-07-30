#!/usr/bin/env python3
"""
Mark Bank — extract figures from an SEC exam paper.

The previous figure pipeline put the wrong image on four Biology cards. Two
things caused it, and both are designed out here:

  1. A verifying agent hand-transcribed the crop path into JSON. Every name this
     script emits is derived from the image's own position in the PDF —
     page number and index on the page — so there is no name to mistype.
     (Two shipped crops are also TRUNCATED, cutting off a label the question
     asks about, which is what the padding below exists to prevent.)
  2. The apply step deduplicated on the DESTINATION filename rather than the
     source bytes, so two entries could resolve to one crop. Here every image is
     hashed, and identical bytes are reported as one image with several
     locations rather than silently written twice.

Output is a directory of PNGs plus an index.json recording, for each image, its
page, its index on that page, its size, its md5, and the text nearest to it on
the page — which is what lets a human recognise it without guessing.

    python3 scripts/markbank/extract-figures.py <paper.pdf> -o <outdir>
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

import fitz  # PyMuPDF

# Below this an "image" is a rule, a bullet, a logo fragment — not a figure.
MIN_W, MIN_H, MIN_BYTES = 90, 70, 3000
# Fraction of the figure's own size added on each side, so labels sitting just
# outside the image box are captured rather than cropped away.
PAD = 0.14
ZOOM = 2.0


def nearby_text(page, rect, pad=46) -> str:
    """Text immediately around an image — the question number and caption live
    here, and it is what makes an extracted crop identifiable."""
    area = fitz.Rect(rect.x0 - pad, rect.y0 - pad, rect.x1 + pad, rect.y1 + pad)
    words = page.get_text("words", clip=area)
    text = " ".join(w[4] for w in sorted(words, key=lambda w: (round(w[1], 1), w[0])))
    return re.sub(r"\s+", " ", text).strip()[:220]


def question_hint(page) -> str:
    """The question numbers printed on this page, so a figure can be tied to one."""
    text = page.get_text()
    hits = re.findall(r"^\s*(\d{1,2})\s*\.", text, re.M) + re.findall(r"Question\s+(\d{1,2})", text)
    seen = []
    for h in hits:
        if h not in seen:
            seen.append(h)
    return ",".join(seen[:6])


def extract(pdf: Path, outdir: Path) -> list:
    doc = fitz.open(pdf)
    outdir.mkdir(parents=True, exist_ok=True)
    by_hash = {}
    index = []

    for pno in range(len(doc)):
        page = doc[pno]
        for i, info in enumerate(page.get_images(full=True)):
            xref = info[0]
            rects = page.get_image_rects(xref)
            if not rects:
                continue
            rect = rects[0]
            if rect.width < MIN_W / 4 or rect.height < MIN_H / 4:
                continue

            # RENDER the page region rather than pulling the embedded object.
            # SEC figures are a raster drawing with the letter labels — "X", "Y",
            # the leader lines and braces — drawn as VECTOR text on top. Extracting
            # the image object silently loses every label, which is the one thing a
            # labelling question depends on.
            #
            # The region is padded because a label sits OUTSIDE the image box: two
            # shipped crops cut off the very letter their question asked about.
            area = fitz.Rect(
                rect.x0 - rect.width * PAD,
                rect.y0 - rect.height * PAD,
                rect.x1 + rect.width * PAD,
                rect.y1 + rect.height * PAD,
            ) & page.rect
            pix = page.get_pixmap(clip=area, matrix=fitz.Matrix(ZOOM, ZOOM))
            if pix.width < MIN_W or pix.height < MIN_H:
                continue
            data = pix.tobytes("png")
            if len(data) < MIN_BYTES:
                continue

            digest = hashlib.md5(data).hexdigest()

            location = {
                "page": pno + 1,
                "indexOnPage": i,
                "questionsOnPage": question_hint(page),
                "nearbyText": nearby_text(page, rect),
            }

            if digest in by_hash:
                # Same bytes used twice in the paper: one image, two locations.
                by_hash[digest]["locations"].append(location)
                continue

            # The name is derived, never typed: page and index identify it.
            name = f"{pdf.stem}-p{pno + 1:02d}-i{i}.png"
            (outdir / name).write_bytes(data)
            entry = {
                "file": name,
                "md5": digest,
                "width": pix.width,
                "height": pix.height,
                "locations": [location],
            }
            by_hash[digest] = entry
            index.append(entry)

    doc.close()
    (outdir / "index.json").write_text(json.dumps(index, indent=1))
    return index


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    args = ap.parse_args()

    index = extract(args.pdf, args.out)
    dupes = sum(len(e["locations"]) - 1 for e in index)
    print(f"{args.pdf.name}: {len(index)} distinct figures ({dupes} repeat placements) -> {args.out}")
    for e in index:
        loc = e["locations"][0]
        print(f"  {e['file']}  {e['width']}x{e['height']}  p{loc['page']}  Q[{loc['questionsOnPage']}]  {loc['nearbyText'][:80]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
