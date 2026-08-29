#!/usr/bin/env python3
"""Find the PAPER page a part is printed on, and what artwork is on it.

    python3 scripts/markbank/authoring/econ_chart_page.py "2025 HL Q12(a)(i)"

43 of the Economics exclusions point at printed matter — "the pie chart above",
"the bar chart above", "the diagram below" — that was never extracted. The
raster extractor only sees embedded images, and a chart drawn with vector
strokes is invisible to it, which is why these crops do not exist while 161
others do.

So the artwork has to be found by its STROKES. This prints, for the page a part
sits on, the vector drawing extents alongside the text blocks, so a crop can be
bounded from what is actually on the page rather than guessed. Feed the bounds
to crop-question-art.py --keep-charts, which takes the union of every drawing
and image on the page and knows to keep a wide framed rectangle when it has a
curved or diagonal stroke (a chart) rather than dropping it as an answer box.

A crop taken this way is a QUESTION figure, not a solution: it is the artwork
the candidate was given, so it must NOT carry solution: true, and the build
refuses a solution crop in that slot anyway.
"""
import argparse
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import fitz                       # noqa: E402
import paper as PP                # noqa: E402

REF = re.compile(r'(\d{4})\s+(HL|OL)\s+(?:Section ([A-Z])\s+)?Q(\d+)'
                 r'(?:\(([a-h])\))?(?:\(([ivx]+)\))?')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ref', help='e.g. "2025 HL Q12(a)(i)"')
    ap.add_argument('--min-area', type=float, default=2000.0,
                    help='ignore drawings smaller than this many square points')
    args = ap.parse_args()

    m = REF.match(args.ref.strip())
    if not m:
        sys.exit(f'could not parse ref {args.ref!r}')
    year, lvl, _sec, q, letter, roman = m.groups()
    year, q = int(year), int(q)
    lv = 'hl' if lvl == 'HL' else 'ol'

    P = PP.Paper('economics', year, lv)
    try:
        want = ' '.join((P.text(q, letter, roman) or '').split())[:60]
    except Exception as exc:                          # noqa: BLE001
        want = ''
        print(f'(paper reader: {type(exc).__name__}: {exc})')
    print(f'looking for: {want!r}\n')

    path = os.path.join(ROOT, f'examiner-reports/economics/papers/{year}-{lv}-paper.pdf')
    doc = fitz.open(path)
    hits = [n for n in range(doc.page_count)
            if want and want[:40].lower() in ' '.join(doc[n].get_text('text').split()).lower()]
    if not hits:
        print('part wording not found on any page; falling back to the question head')
        hits = [n for n in range(doc.page_count)
                if re.search(rf'Question\s+{q}\b', doc[n].get_text('text'))]
    for pno in hits[:2]:
        pg = doc[pno]
        print(f'──── PAPER page {pno + 1} (crop with --page {pno + 1}) ────')
        print('  DRAWINGS (vector strokes — what the raster extractor cannot see):')
        for d in pg.get_drawings():
            r = d['rect']
            area = r.width * r.height
            if area < args.min_area:
                continue
            print(f'    x0={r.x0:6.1f} y0={r.y0:6.1f} x1={r.x1:6.1f} y1={r.y1:6.1f} '
                  f'({r.width:5.1f} x {r.height:5.1f})')
        print('  IMAGES:')
        for img in pg.get_images(full=True):
            print(f'    {img[7] or img[0]}')
        print('  TEXT:')
        width = pg.rect.width
        for b in sorted(pg.get_text('blocks'), key=lambda b: (round(b[1], 1), b[0])):
            t = ' '.join(b[4].split())
            if t:
                col = 'MARKS' if b[0] > width * 0.78 else '     '
                print(f'    y={b[1]:6.1f} {col} {t[:88]}')
    doc.close()


if __name__ == '__main__':
    main()
