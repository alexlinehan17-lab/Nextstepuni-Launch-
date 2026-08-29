#!/usr/bin/env python3
"""Find the SCHEME page a printed run sits on, and list the page by coordinate.

    python3 scripts/markbank/authoring/econ_scheme_page.py 2023 hl "calculate the Herfindahl"

Why this exists
---------------
Two different jobs need the same thing and neither can be done from flat text.

A mark cell is printed in the RIGHT MARGIN on the row it prices, but extraction
emits it wherever the PDF's content stream happens to put it — for 2021 OL Q3
the cell for "Answer: - 4.71" comes out three runs early, and reading top-down
attributes it to the following part. Reading the y coordinate settles it: the
cell and the line it prices share a row. The check that an attribution is right
is that the question's cells then sum to what the paper pays for it.

And a worked calculation is often set as a FRACTION or with SUPERSCRIPTS, which
flatten into text that is not merely ugly but false: the scheme's HHI working
prints as "482 + 272 + ... = 3172" once the squares are lost, and the multiplier
prints as "0.1 + 0.4 = 2". Neither can go on a card. The fix is the one the tick
tables already use — crop the scheme's own working and publish it as a
`solution: true` figure — and a crop needs bounds read off the page.
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
import fitz                                    # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level', choices=['hl', 'ol'])
    ap.add_argument('probe', help='a run of text printed on the page you want')
    ap.add_argument('--page', type=int, help='skip the search and list this page')
    args = ap.parse_args()

    path = os.path.join(ROOT, 'examiner-reports/economics',
                        f'{args.year}-{args.level}-marking-scheme.pdf')
    doc = fitz.open(path)
    want = ' '.join(args.probe.split()).lower()
    pages = ([args.page - 1] if args.page else
             [n for n in range(doc.page_count)
              if want in ' '.join(doc[n].get_text('text').split()).lower()])
    if not pages:
        print(f'no page contains {args.probe!r}')
    for n in pages[:2]:
        pg = doc[n]
        width = pg.rect.width
        print(f'──── SCHEME page {n + 1} (crop with --page {n + 1}) ────')
        for d in pg.get_drawings():
            r = d['rect']
            if r.width * r.height >= 2000:
                print(f'  DRAW x0={r.x0:6.1f} y0={r.y0:6.1f} '
                      f'x1={r.x1:6.1f} y1={r.y1:6.1f}')
        for b in sorted(pg.get_text('blocks'), key=lambda b: (round(b[1], 1), b[0])):
            t = ' '.join(b[4].split())
            if t:
                col = 'MARKS' if b[0] > width * 0.78 else '     '
                print(f'  y={b[1]:6.1f} x={b[0]:6.1f} {col} {t[:86]}')
    doc.close()


if __name__ == '__main__':
    main()
