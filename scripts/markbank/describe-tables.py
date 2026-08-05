#!/usr/bin/env python3
"""
Mark Bank — write alt text for extracted TABLE crops, from the table itself.

A table crop's description does not need an agent to look at it, and should not
have one: the cells are in the PDF as text, so the honest description is the one
read straight out of them. Nothing here is invented, which is the property the
figure pipeline exists to protect.

    python3 scripts/markbank/describe-tables.py <subject> <out.json>

Writes to a file rather than stdout: PyMuPDF prints an advisory banner to stdout
on first use, which would corrupt a redirected JSON stream.
"""

import json
import re
import sys
from pathlib import Path

import fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from markbank_text import unligature  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
MIN_DESC = 40   # bind-figures drops anything thinner as untrustworthy

# Below this, transcribe the table in full; above it, name the columns and stubs.
SMALL_TABLE_ROWS, SMALL_TABLE_COLS = 9, 3


def cells_for(page, bbox):
    """The rows of whichever detected table sits at this crop's box."""
    want = fitz.Rect(bbox)
    best, best_overlap = None, 0.0
    for t in page.find_tables(strategy='lines_strict').tables:
        r = fitz.Rect(t.bbox)
        inter = r & want
        if inter.is_empty:
            continue
        ov = abs(inter.get_area())
        if ov > best_overlap:
            best, best_overlap = t, ov
    if best is None:
        return None
    try:
        return [[unligature((c or '')).strip() for c in row] for row in best.extract()]
    except Exception:
        return None


def describe(rows) -> str:
    """Prose a student who cannot see the crop can actually answer from.

    A small table is transcribed IN FULL. Naming the columns and the first cell of
    each row is enough for a table of figures, but it is exactly wrong for the
    matching questions Business is full of: "Columns: Terms, Explanations. Rows:
    1. Merger, 2. Acquisition..." hands over the terms and silently drops the
    lettered explanations the student has to match them to. The reasoning that the
    crop carries the values does not survive contact with the reader — someone who
    cannot see the crop is the only person reading this.
    """
    rows = [r for r in rows if any(c for c in r)]
    if not rows:
        return ''
    width = max(len(r) for r in rows)
    if len(rows) <= SMALL_TABLE_ROWS and width <= SMALL_TABLE_COLS:
        lines = [' | '.join(c for c in r if c) for r in rows]
        body = 'A table from the exam paper, row by row: ' + '; '.join(l for l in lines if l) + '.'
        return re.sub(r'\s+', ' ', body).strip()
    header = [c for c in rows[0] if c]
    stubs = [r[0] for r in rows[1:] if r and r[0]]
    bits = []
    if header:
        bits.append('Columns: ' + ', '.join(header[:8]) + '.')
    if stubs:
        bits.append('Rows: ' + ', '.join(stubs[:8]) + '.')
    bits.append(f'{len(rows)} rows by {width} columns, as printed in the paper.')
    return re.sub(r'\s+', ' ', 'A table from the exam paper. ' + ' '.join(bits)).strip()


def main() -> int:
    subject = sys.argv[1]
    out = []
    for index_path in sorted((ROOT / 'exam-papers' / subject / 'figures').glob('*/index.json')):
        folder = index_path.parent.name
        year, lv = folder.split('-')
        pdf = ROOT / 'exam-papers' / subject / f'{subject}-{year}-{lv.upper()}-paper.pdf'
        if not pdf.exists():
            continue
        doc = fitz.open(pdf)
        for entry in json.load(open(index_path)):
            loc = entry['locations'][0]
            if loc.get('kind') != 'table' or 'bbox' not in loc:
                continue
            rows = cells_for(doc[loc['page'] - 1], loc['bbox'])
            desc = describe(rows) if rows else ''
            if len(desc) < MIN_DESC:
                continue
            out.append({
                'file': entry['file'],
                'kind': 'figure',
                'drawingComplete': True,
                'truncated': False,
                'description': desc,
                # A table prints words, not bare letters to decode.
                'lettersVisible': [],
                'labelMeanings': [],
                'questionRef': '',
                'notes': f"Table region on page {loc['page']}; description read from the table's own cells.",
            })
        doc.close()
    Path(sys.argv[2]).write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f'described {len(out)} table crops -> {sys.argv[2]}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
