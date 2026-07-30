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


def cluster(rects, gap=64.0):
    """Group image boxes that belong to the same figure.

    An SEC diagram is rarely one image. A three-panel enzyme sequence, a heart
    drawn beside its inset, a karyotype and its caption are each SEVERAL image
    objects sitting side by side, with the letter labels drawn as vector text
    between them. Cropping per object returns fragments — an enzyme with no
    substrate, an arrow whose letter is in the next crop along — so boxes closer
    than `gap` are merged and rendered as one region.
    """
    groups = []
    for r in rects:
        merged = None
        for g in groups:
            probe = fitz.Rect(r.x0 - gap, r.y0 - gap, r.x1 + gap, r.y1 + gap)
            if probe.intersects(g):
                if merged is None:
                    g |= r
                    merged = g
                else:
                    merged |= g
                    groups.remove(g)
        if merged is None:
            groups.append(fitz.Rect(r))
    return groups


def content_box(page):
    """The page's text column, from where its content actually sits."""
    xs = []
    for block in page.get_text("blocks"):
        if str(block[4]).strip():
            xs.append((block[0], block[2]))
    for info in page.get_images(full=True):
        for r in page.get_image_rects(info[0]):
            xs.append((r.x0, r.x1))
    if not xs:
        return page.rect
    return fitz.Rect(min(a for a, _ in xs), page.rect.y0, max(b for _, b in xs), page.rect.y1)


def widen_to_column(page, area):
    """Take a figure region out to the full text column.

    The commonest truncation left was horizontal: a multi-panel diagram — an
    enzyme sequence, three hearts in a row — spreads wider than any sane
    clustering gap, so a panel and its letter fall outside the crop. SEC pages
    are a single column, so the sides are margin, not neighbouring content:
    widening to the column captures the whole diagram without dragging anything
    unrelated in. Vertical extent is left alone, which is what keeps the question
    text and answer boxes out.
    """
    col = content_box(page)
    return fitz.Rect(col.x0, area.y0, col.x1, area.y1) & page.rect


def include_labels(page, area, reach=52.0, max_chars=34):
    """Grow a figure region to take in the label text sitting beside it.

    Labels are vector text, not image objects, so clustering image boxes alone
    still slices them: a leader line survives while the words it points from are
    cut off at the edge. Short text blocks close to the figure are captions and
    labels; long ones are the question itself and are left out.
    """
    grown = fitz.Rect(area)
    probe = fitz.Rect(area.x0 - reach, area.y0 - reach, area.x1 + reach, area.y1 + reach)
    for block in page.get_text("blocks"):
        x0, y0, x1, y1, text = block[0], block[1], block[2], block[3], block[4]
        label = " ".join(str(text).split())
        if not label or len(label) > max_chars:
            continue
        box = fitz.Rect(x0, y0, x1, y1)
        # Question prose runs the width of the text column; a label does not.
        # Answer boxes and part markers are excluded the same way.
        if box.width > page.rect.width * 0.34:
            continue
        if re.match(r"^\(?[a-z]\)|^\(?i+v?\)|^\d+\.", label, re.I):
            continue
        if box.intersects(probe):
            grown |= box
    return grown


def extract(pdf: Path, outdir: Path) -> list:
    doc = fitz.open(pdf)
    outdir.mkdir(parents=True, exist_ok=True)
    by_hash = {}
    index = []

    for pno in range(len(doc)):
        page = doc[pno]
        boxes = []
        for info in page.get_images(full=True):
            for r in page.get_image_rects(info[0]):
                if r.width >= MIN_W / 4 and r.height >= MIN_H / 4:
                    boxes.append(r)
        for i, rect in enumerate(cluster(boxes)):

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
            area = include_labels(page, area) & page.rect
            area = widen_to_column(page, area)
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
