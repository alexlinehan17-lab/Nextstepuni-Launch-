#!/usr/bin/env python3
"""Crop the figures the printed-layout Chemistry papers (2026 on) hand their parts.

    python3 scripts/markbank/authoring/chem_print_figures.py 2026 hl          # crop
    python3 scripts/markbank/authoring/chem_print_figures.py 2026 hl --check  # verify

Each crop is a rectangle on one page of the paper (a diagram, a data table, a
reaction scheme) or of the marking scheme (a worked answer the text layer
cannot carry, such as a stacked fraction). The rectangles were measured from
the PDFs' own image and drawing boxes and every crop was opened and looked at
before its catalogue entry was written. The catalogue in
scripts/markbank/authored/chemistry-print-figures-catalogue.json holds the alt
text; bind-figures.mjs publishes what this writes.

A crop is named for its question, not its page index:
chemistry-2026-HL-paper-q8.png, chemistry-2026-HL-scheme-q7b-iv.png. The
"-scheme-" crops are marked `solution: true` in the catalogue, which the session
holds back until the student has committed to an answer.

--check re-renders every crop in memory and compares it to the published copy
in public/exam-figures/chemistry/markbank, so a changed rectangle or renderer
cannot slip a different picture under a published name.
"""
import argparse
import hashlib
import os
import sys

import fitz

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
PAPERS = os.path.join(ROOT, 'examiner-reports', 'chemistry', 'papers')
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'chemistry', 'schemes')
DPI = 150

# (name suffix, source, page, (x0, y0, x1, y1) in PDF points). A source of
# 'paper-image' takes the raster the paper embeds at that rectangle as it is,
# for a picture whose page text runs across it. 2026 HL Q4(i)'s raster was cut
# from a page and carries the tails of two neighbouring lines ("e", "ound") at
# its left edge; MASKS whites out exactly those pixel boxes, which were found
# by scanning the raster for dark pixels clear of the structure's own bonds.
CROPS = {
    (2026, 'hl'): [
        ('paper-q2a', 'paper', 3, (378, 50, 544, 192)),
        ('paper-q4i', 'paper-image', 5, (448, 352, 539, 477)),
        ('paper-q6b', 'paper', 7, (125, 226, 420, 292)),
        ('paper-q8', 'paper', 9, (130, 78, 466, 196)),
        ('paper-q9a', 'paper', 10, (80, 156, 545, 234)),
        ('paper-q9c', 'paper', 10, (460, 526, 546, 660)),
        ('paper-q11a', 'paper', 12, (165, 96, 412, 146)),
        ('paper-q11c', 'paper', 12, (128, 507, 467, 566)),
        ('paper-q11d-b', 'paper', 13, (135, 438, 490, 550)),
        ('scheme-q4c', 'scheme', 9, (50, 197.6, 200, 214)),
        ('scheme-q4k', 'scheme', 9, (50, 603, 200, 640)),
        ('scheme-q5b-iii', 'scheme', 10, (100, 468, 420, 540)),
        ('scheme-q6b-iv', 'scheme', 11, (60, 401, 420, 470)),
        ('scheme-q8b-i', 'scheme', 13, (100, 300, 470, 372)),
        ('scheme-q11a-iv', 'scheme', 17, (100, 224, 330, 292)),
        ('scheme-q11a-v', 'scheme', 17, (100, 351, 330, 404)),
        ('scheme-q7b-iv', 'scheme', 12, (100, 375, 560, 414)),
        ('scheme-q7b-v', 'scheme', 12, (100, 450, 560, 534)),
    ],
    (2026, 'ol'): [
        ('paper-q1', 'paper', 2, (110, 150, 485, 275)),
        ('paper-q2', 'paper', 3, (495, 52, 545, 270)),
        ('paper-q2c', 'paper', 3, (52, 365, 545, 428)),
        ('paper-q3', 'paper', 4, (52, 259, 545, 326)),
        ('paper-q6', 'paper', 7, (205, 92, 390, 235)),
        ('paper-q8', 'paper', 9, (65, 75, 530, 140)),
        ('paper-q9c', 'paper', 10, (280, 490, 372, 532)),
        ('paper-q10b', 'paper-image', 11, (468, 320, 540, 421)),
        ('paper-q11c', 'paper', 12, (52, 412, 545, 700)),
        ('scheme-q1c-ii', 'scheme', 6, (108, 507, 275, 588)),
        ('scheme-q2c-ii', 'scheme', 7, (105, 531, 560, 614)),
        ('scheme-q4j', 'scheme', 9, (80, 446, 248, 489)),
        ('scheme-q5a-iv', 'scheme', 10, (108, 322, 228, 424)),
        ('scheme-q6c-i', 'scheme', 11, (110, 378.5, 260, 401)),
        ('scheme-q6d-ii', 'scheme', 11, (109, 531.5, 320, 609)),
        ('scheme-q9a-ii', 'scheme', 14, (108, 178.5, 330, 217)),
    ],
}


MASKS = {
    'chemistry-2026-HL-paper-q4i.png': [(0, 350, 20, 386), (0, 489, 92, 515)],
}


def out_dir(year, lvl):
    # bind-figures.mjs resolves a crop as exam-papers/<subject>/figures/<year>-<level>/.
    return os.path.join(ROOT, 'exam-papers', 'chemistry', 'figures', f'{year}-{lvl}')


suffix_of = {(src, pg, rect): suf for crops in CROPS.values() for suf, src, pg, rect in crops}


def render(year, lvl, source, page, rect):
    path = os.path.join(PAPERS, f'{year}-{lvl}-paper.pdf') if source.startswith('paper') \
        else os.path.join(SCHEMES, f'{year}-{lvl}.pdf')
    doc = fitz.open(path)
    pg = doc[page - 1]
    if source == 'paper-image':
        want = fitz.Rect(*rect)
        hits = [img[0] for img in pg.get_images(full=True)
                if any(want.contains(r) for r in pg.get_image_rects(img[0]))]
        if len(hits) != 1:
            raise SystemExit(f'p{page}: {len(hits)} images inside {rect}')
        pix = fitz.Pixmap(doc, hits[0])
        for box in MASKS.get(name(year, lvl, suffix_of[(source, page, rect)]), []):
            pix.set_rect(fitz.IRect(*box), (255,) * pix.n)
        return pix.tobytes('png')
    return pg.get_pixmap(dpi=DPI, clip=fitz.Rect(*rect)).tobytes('png')


def name(year, lvl, suffix):
    return f'chemistry-{year}-{lvl.upper()}-{suffix}.png'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('lvl', choices=['hl', 'ol'])
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    crops = CROPS.get((args.year, args.lvl), [])
    od = out_dir(args.year, args.lvl)
    os.makedirs(od, exist_ok=True)
    bad = 0
    for suffix, source, page, rect in crops:
        png = render(args.year, args.lvl, source, page, rect)
        dest = os.path.join(od, name(args.year, args.lvl, suffix))
        if args.check:
            # The committed copy is the one bind-figures.mjs published.
            dest = os.path.join(ROOT, 'public', 'exam-figures', 'chemistry', 'markbank',
                                name(args.year, args.lvl, suffix))
            ok = os.path.exists(dest) and open(dest, 'rb').read() == png
            bad += not ok
            print(('ok   ' if ok else 'DIFF ') + os.path.basename(dest))
        else:
            with open(dest, 'wb') as f:
                f.write(png)
            print(os.path.basename(dest), hashlib.md5(png).hexdigest())
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
