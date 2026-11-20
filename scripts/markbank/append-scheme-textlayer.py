#!/usr/bin/env python3
"""
Mark Bank: append a scheme PDF's own text layer, page by page, to its .md.

    python3 scripts/markbank/append-scheme-textlayer.py <subject> <year> <hl|ol> [--deferred]

The Music schemes from 2026 set the paper again with the answers in boxes laid
OVER it ("Up to 3 marks for a correct description of the texture of the music
heard / in this excerpt." printed across the paper's own "Description:" label).
The flat extraction reads across rows, so the paper's label lands in the middle
of the SEC's sentence and the sentence exists nowhere in the .md; the columns
reading (append-scheme-columns.py) cannot separate words that overlap. The PDF's
own text layer keeps the box's lines together, in the order the SEC wrote them.

APPEND-ONLY, the argument append-scheme-tables.py makes: comparableScheme()
joins every line, so each claim that traces today still traces afterwards, and
nothing is invented: every appended line is a line of the SEC's own text layer.
Re-running replaces the block, so it is idempotent.
"""
import os
import re
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
START = '<!-- text layer, page by page (append-scheme-textlayer.py) -->'
END = '<!-- end text layer -->'


def main(subject, year, level, deferred=False):
    stem = f'{year}-{level}{"-deferred" if deferred else ""}'
    base = os.path.join(ROOT, 'examiner-reports', subject, 'schemes')
    pdf = os.path.join(base, f'{stem}.pdf')
    md = os.path.join(base, f'{stem}.md')
    if not os.path.exists(pdf):
        raise SystemExit(f'no scheme PDF at {pdf}')
    lines = []
    for i, page in enumerate(fitz.open(pdf)):
        text = [l.strip() for l in page.get_text().split('\n') if l.strip()]
        if text:
            lines.append(f'## Text layer, page {i + 1}')
            lines += text
    body = open(md, encoding='utf-8').read() if os.path.exists(md) else ''
    body = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', body, flags=re.S).rstrip('\n')
    block = '\n'.join([START, *lines, END])
    open(md, 'w', encoding='utf-8').write((body + '\n\n' if body else '') + block + '\n')
    print(f'{subject} {stem}: appended {len(lines)} text-layer lines to {os.path.basename(md)}')


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    main(a[0], int(a[1]), a[2], deferred='--deferred' in sys.argv)
