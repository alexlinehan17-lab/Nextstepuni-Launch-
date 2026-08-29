#!/usr/bin/env python3
"""Crop a marking scheme's COMPLETED tick table and stage it for the manifest.

    # 1. find the table: prints every block on the page with its y, so the
    #    bounds below are read off the page rather than guessed
    python3 scripts/markbank/authoring/econ_tick_crop.py 2022 ol --page 6 --show

    # 2. crop it, and print a catalogue stub to fill in after LOOKING at the png
    python3 scripts/markbank/authoring/econ_tick_crop.py 2022 ol --page 6 \\
        --top 535 --bottom 700 --slug q4 --ref "2022 OL Section A Q4"

Why this exists
---------------
A tick table is answered by a ✔ that is DRAWN, not set in the text layer. The
glyph survives extraction but the COLUMN it sits in does not, so the flat text
reads as though every item were ticked in the same column — and the column is
the whole answer. No parser can recover it and nothing may be typed in its
place (see lift-never-write-exam-content).

The scheme states the answer graphically, so the answer is taken graphically:
the completed table is cropped and published as a SOLUTION figure. That is the
same mechanism the Maths deck has used for 819 printed model solutions — the
app hides a solution crop until the card is revealed
(SessionScreen.tsx: `revealed || !figure.solution`) and renders it large to be
read. The card's row still carries the scheme's own contiguous run so the claim
traces to its document; the picture is what disambiguates it.

The crop is NOT described here. Bind refuses a description under 40 characters,
and a description written without opening the file is exactly the hand-
transcribed path both historical figure corruptions in this repo came in
through. Open the png, then write what is in it.
"""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
SCHEME = os.path.join(ROOT, 'examiner-reports/economics/{year}-{level}-marking-scheme.pdf')
OUTDIR = os.path.join(ROOT, 'exam-papers/economics/figures/{year}-{level}')
CROP = os.path.join(ROOT, 'scripts/markbank/crop-question-art.py')


def show(path, page):
    """Every block on the page with its y, so bounds are read and not guessed."""
    import fitz
    doc = fitz.open(path)
    pg = doc[page - 1]
    width = pg.rect.width
    for b in sorted(pg.get_text('blocks'), key=lambda b: (round(b[1], 1), b[0])):
        text = ' '.join(b[4].split())
        if not text:
            continue
        col = 'MARKS' if b[0] > width * 0.75 else '     '
        print(f'  y={b[1]:7.1f}  x={b[0]:6.1f}  {col}  {text[:96]}')
    doc.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level', choices=['hl', 'ol'])
    ap.add_argument('--page', type=int, required=True, help='1-based, in the SCHEME pdf')
    ap.add_argument('--show', action='store_true', help='list the page and stop')
    ap.add_argument('--top', type=float)
    ap.add_argument('--bottom', type=float)
    ap.add_argument('--slug', help='question slug for the file name, e.g. q4')
    ap.add_argument('--ref', help='the citation this table answers')
    args = ap.parse_args()

    scheme = SCHEME.format(year=args.year, level=args.level)
    if not os.path.exists(scheme):
        sys.exit(f'no scheme at {scheme}')

    if args.show:
        show(scheme, args.page)
        return

    for needed in ('top', 'bottom', 'slug', 'ref'):
        if getattr(args, needed) is None:
            sys.exit(f'--{needed} is required to crop (run --show first)')

    outdir = OUTDIR.format(year=args.year, level=args.level)
    os.makedirs(outdir, exist_ok=True)
    name = (f'economics-{args.year}-{args.level.upper()}'
            f'-scheme-p{args.page:02d}-{args.slug}-ticks.png')
    out = os.path.join(outdir, name)

    subprocess.run([sys.executable, CROP, scheme, '--page', str(args.page),
                    '--top', str(args.top), '--bottom', str(args.bottom),
                    '-o', out], check=True)

    print('\nOPEN THIS FILE, then write its description into the stub below:')
    print(f'  {out}\n')
    print(json.dumps([{
        'file': name,
        'kind': 'figure',
        'truncated': False,
        'drawingComplete': True,
        'solution': True,
        'questionRef': args.ref,
        'description': 'TODO — open the png and describe the completed table: the column '
                       'headings, and which column each item is ticked under.',
    }], indent=1))
    print('\nThen: node scripts/markbank/bind-figures.mjs <that catalogue>.json')


if __name__ == '__main__':
    main()
