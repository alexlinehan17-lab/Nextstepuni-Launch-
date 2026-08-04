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
# Absolute floors in points, so a shallow figure still gets a real margin.
# Larger below than above: letters under a photo row and table bodies live there.
MIN_PAD_X, MIN_PAD_TOP, MIN_PAD_BOTTOM = 22, 55, 125
ZOOM = 2.0

# A table or chart drawn as vector paths is not an image object, so
# page.get_images() cannot see it and this script used to emit nothing for it.
# The consequence reached students: the authoring wave, given no crop, wrote the
# table out as prose — "Regal: Week 1 14.7, Week 2 14.3, Week 3 13.9..." — which
# is unreadable next to the printed table it replaced. Across the ten
# Agricultural Science papers, 57 detected tables sit on pages carrying no
# raster image at all, so they were invisible by construction.
MIN_TABLE_W, MIN_TABLE_H = 120, 34
# A vector cluster needs real substance to be a chart rather than the ruled
# lines of an answer box: this many separate paths, and this much of the page.
MIN_VECTOR_PATHS = 12
MIN_VECTOR_W, MIN_VECTOR_H = 130, 90
MAX_REGION_FRACTION = 0.72
# A table's bbox is exact, unlike a photo's, so it needs a caption's worth of
# room above and very little below. The photo floors would pull the NEXT
# question into a table crop.
# Tight. 46pt above a table swept in the question line printed over it, so the
# card rendered its own question twice — once as text, once inside the picture.
# A table's title is almost always inside its own ruled box, so it needs nothing.
TABLE_PAD_X, TABLE_PAD_TOP, TABLE_PAD_BOTTOM = 10, 12, 10


def covered_by(rect, regions, frac=0.72) -> bool:
    """Is most of `rect` already inside a region we are going to render?"""
    area = abs(rect.get_area())
    if area <= 0:
        return True
    for g in regions:
        inter = rect & g
        if not inter.is_empty and abs(inter.get_area()) >= area * frac:
            return True
    return False


def table_regions(page, have: list) -> list:
    """Tables PyMuPDF can find, whether ruled in vector or implied by layout.

    This is the reliable half of the fix — find_tables() returns a real bbox, so
    there is no clustering heuristic to get wrong.
    """
    try:
        # lines_strict only: the default and 'lines' strategies read a column
        # of prose as a table — the 2021 wild-oats article came back as two —
        # and a paragraph bound to a card as a "table" would be worse than the
        # transcription this whole change exists to remove. Exam tables are
        # ruled, so requiring real rules costs nothing and removes the noise.
        found = page.find_tables(strategy='lines_strict').tables
    except Exception:
        return []
    out = []
    for t in found:
        r = fitz.Rect(t.bbox)
        if r.width < MIN_TABLE_W or r.height < MIN_TABLE_H:
            continue
        if covered_by(r, have) or covered_by(r, out):
            continue
        out.append(r)
    return out


def vector_regions(page, have: list) -> list:
    """Charts and diagrams drawn as paths — pie charts, graphs, flow diagrams.

    Riskier than tables, because every answer-box rule is also a path. Full-width
    hairlines are dropped first, then a cluster only survives if it is built from
    MIN_VECTOR_PATHS separate paths and does not span most of the page — which is
    what an answer grid looks like once its rules are joined up.
    """
    paths = []
    for d in page.get_drawings():
        r = fitz.Rect(d["rect"])
        if r.is_empty:
            continue
        # An answer line: hairline height, running most of the column.
        if r.height < 3 and r.width > page.rect.width * 0.45:
            continue
        if r.width < 5 and r.height < 5:
            continue
        paths.append(r)

    page_area = abs(page.rect.get_area())
    out = []
    for g in cluster(paths, gap=20.0):
        if g.width < MIN_VECTOR_W or g.height < MIN_VECTOR_H:
            continue
        if abs(g.get_area()) > page_area * MAX_REGION_FRACTION:
            continue
        if sum(1 for r in paths if r in g) < MIN_VECTOR_PATHS:
            continue
        if covered_by(g, have) or covered_by(g, out):
            continue
        out.append(g)
    return out


def avoid_slicing_text(page, area):
    """Pull a crop's horizontal edges clear of any line of text they cut through.

    A fixed pad cannot know where the type sits, so it lands mid-line and the
    crop opens on the bottom halves of letters — which reads as a broken image
    rather than a tight one. This walks the page's text lines and, where one
    straddles an edge, moves that edge past it.
    """
    top, bottom = area.y0, area.y1
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            x0, y0, x1, y1 = line["bbox"]
            if x1 < area.x0 or x0 > area.x1:
                continue
            # Straddles the top edge: start below it instead.
            if y0 < area.y0 < y1:
                top = max(top, y1 + 1)
            # Straddles the bottom edge: stop above it.
            if y0 < area.y1 < y1:
                bottom = min(bottom, y0 - 1)
    if bottom - top < 20:
        return area
    return fitz.Rect(area.x0, top, area.x1, bottom)


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
        # Raster clusters first, then the vector work the old pipeline could not
        # see. Order matters: a table already inside a photo's crop is skipped
        # rather than emitted twice.
        raster = cluster(boxes)
        tables = table_regions(page, raster)
        vectors = vector_regions(page, raster + tables)
        regions = ([(r, 'raster') for r in raster]
                   + [(r, 'table') for r in tables]
                   + [(r, 'vector') for r in vectors])

        for i, (rect, kind) in enumerate(regions):

            # RENDER the page region rather than pulling the embedded object.
            # SEC figures are a raster drawing with the letter labels — "X", "Y",
            # the leader lines and braces — drawn as VECTOR text on top. Extracting
            # the image object silently loses every label, which is the one thing a
            # labelling question depends on.
            #
            # The region is padded because a label sits OUTSIDE the image box: two
            # shipped crops cut off the very letter their question asked about.
            # A fraction of the figure's own size is not enough on its own. A wide,
            # shallow photo strip has a small height, so 14% of it is a few points —
            # and the Agricultural Science breed-identification questions print their
            # letters BELOW the photographs, in the answer row. Every one of those
            # crops sliced through D, E and F: the highest-value figures in the paper,
            # lost to a proportional pad. Tables fail the same way, keeping their
            # header row and losing every line of data beneath it.
            #
            # So the pad also has an absolute floor in points, and reaches further
            # DOWN than up, because that is where labels and table bodies sit. The
            # cost is some question prose inside the crop, which is harmless — the
            # card prints the question anyway.
            if kind == 'raster':
                pad_x = max(rect.width * PAD, MIN_PAD_X)
                pad_top = max(rect.height * PAD, MIN_PAD_TOP)
                pad_bottom = max(rect.height * PAD, MIN_PAD_BOTTOM)
            else:
                pad_x, pad_top, pad_bottom = TABLE_PAD_X, TABLE_PAD_TOP, TABLE_PAD_BOTTOM
            area = fitz.Rect(
                rect.x0 - pad_x,
                rect.y0 - pad_top,
                rect.x1 + pad_x,
                rect.y1 + pad_bottom,
            ) & page.rect
            # Only raster regions need growing. A photo's box excludes the labels
            # printed around it, so it must reach for them and out to the column.
            # A table's bbox is already the whole table, and growing it only
            # drags in the question text sitting above.
            if kind == 'raster':
                area = include_labels(page, area) & page.rect
                area = widen_to_column(page, area)
            else:
                area = avoid_slicing_text(page, area) & page.rect
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
                "kind": kind,
                # The rendered region, so a later step can go back to the PDF and
                # read a table's own cells rather than describing it from a guess.
                "bbox": [round(area.x0, 1), round(area.y0, 1), round(area.x1, 1), round(area.y1, 1)],
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
