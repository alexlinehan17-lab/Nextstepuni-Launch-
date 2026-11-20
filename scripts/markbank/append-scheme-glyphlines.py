#!/usr/bin/env python3
"""
Mark Bank: append a scheme PDF's lines rebuilt from its glyph positions, page by page, to its .md.

    python3 scripts/markbank/append-scheme-glyphlines.py <subject> <year> <hl|ol> <page> [<page> ...]
            [--deferred] [--x-from=<fraction>] [--x-to=<fraction>]

Some schemes draw a table in vertical strips and paint the glyph at each strip's
edge twice (Music 2011 Ordinary, pages 7-8: the text layer and the flat
extraction both read "Ac ccordion", "Fre ench horn"). The words exist in the PDF,
but in no reading the provenance gate can match. This reading takes every glyph
the page draws, groups glyphs into lines by their vertical centre, orders each
line left to right, and drops a glyph that repeats the one before it at the same
place (the same character within 1pt): the second copy of a strip-edge glyph.
A gap wider than 2pt becomes a space. --x-from / --x-to keep one band of columns
(the answer column, without the rotated section labels and the marks beside it),
and a superscript ("7th") joins the row below it instead of making a row of its own.

APPEND-ONLY, as append-scheme-tables.py and append-scheme-textlayer.py: nothing
is typed; every appended character is a glyph the SEC's PDF draws. Only the
pages named are rebuilt. Re-running replaces the block, so it is idempotent.
"""
import os
import re
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
START = '<!-- glyph lines, strip-edge doubles dropped (append-scheme-glyphlines.py) -->'
END = '<!-- end glyph lines -->'


def page_lines(page, x_from=0.0, x_to=1.0):
    W = page.rect.width
    chars = []
    for block in page.get_text('rawdict')['blocks']:
        for line in block.get('lines', []):
            for span in line['spans']:
                for c in span['chars']:
                    x0, y0, x1, y1 = c['bbox']
                    if x_from * W <= x0 < x_to * W:
                        chars.append(((y0 + y1) / 2, x0, x1, c['c'], span['size']))
    if not chars:
        return []
    sizes = sorted(c[4] for c in chars)
    body = sizes[len(sizes) // 2]
    # a superscript ("7th") is set small and high: file it with the nearest full-size row below it
    full = sorted({round(c[0], 1) for c in chars if c[4] >= 0.8 * body})
    def row_of(c):
        if c[4] >= 0.8 * body or not full:
            return c[0]
        below = [y for y in full if 0 <= y - c[0] <= 8]
        return below[0] if below else c[0]
    chars = [(row_of(c), *c[1:4]) for c in chars]
    chars.sort(key=lambda t: (round(t[0], 1), t[1]))
    rows = []
    for ch in chars:
        if rows and abs(rows[-1][0] - ch[0]) < 2.5:
            rows[-1][1].append(ch)
        else:
            rows.append([ch[0], [ch]])
    out = []
    for _, cs in rows:
        cs.sort(key=lambda t: t[1])
        text, last = [], None
        for c in cs:
            if last and c[3] == last[3] and abs(c[1] - last[1]) < 1.0:
                continue
            if last and c[1] - last[2] > 2.0 and text and text[-1] != ' ':
                text.append(' ')
            text.append(c[3])
            last = c
        t = re.sub(r'\s+', ' ', ''.join(text)).strip()
        if t:
            out.append(t)
    return out


def main(subject, year, level, pages, deferred=False, x_from=0.0, x_to=1.0):
    stem = f'{year}-{level}{"-deferred" if deferred else ""}'
    base = os.path.join(ROOT, 'examiner-reports', subject, 'schemes')
    pdf = os.path.join(base, f'{stem}.pdf')
    md = os.path.join(base, f'{stem}.md')
    if not os.path.exists(pdf):
        raise SystemExit(f'no scheme PDF at {pdf}')
    doc = fitz.open(pdf)
    lines = []
    for p in pages:
        lines.append(f'## Glyph lines, page {p}')
        lines += page_lines(doc[p - 1], x_from, x_to)
    body = open(md, encoding='utf-8').read() if os.path.exists(md) else ''
    body = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', body, flags=re.S).rstrip('\n')
    block = '\n'.join([START, *lines, END])
    open(md, 'w', encoding='utf-8').write((body + '\n\n' if body else '') + block + '\n')
    print(f'{subject} {stem}: appended {len(lines)} glyph lines (pages {pages}) to {os.path.basename(md)}')


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    opt = {k: float(v) for k, v in (x[2:].split('=') for x in sys.argv[1:] if x.startswith('--x-'))}
    main(a[0], int(a[1]), a[2], [int(p) for p in a[3:]], deferred='--deferred' in sys.argv,
         x_from=opt.get('x-from', 0.0), x_to=opt.get('x-to', 1.0))
