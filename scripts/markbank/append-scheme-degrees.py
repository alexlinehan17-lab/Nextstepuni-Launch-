#!/usr/bin/env python3
"""Append the scheme's lines with their DEGREE SIGNS read as degree signs.

    python3 scripts/markbank/append-scheme-degrees.py dcg 2018 hl

Some SEC schemes set the degree sign as a raised small letter o: the 2018 DCG
Ordinary scheme prints "0o to 120o, Uniform Velocity" with each o an 8pt
superscript beside 12pt digits, 4pt above the baseline. The extractor reports
the letter, so the markdown reads "0o to 120o" and a card lifted from it shows
a student "0o" where the paper they sat printed 0°.

This reads the PDF, finds every superscript span that is the letter o and
follows a digit, and writes the line it sits on with that o as a degree sign
into the markdown as an ADDED form, between markers, the way the other
append-scheme-*.py tools do: append-only, idempotent, and only lines the PDF
itself shows a raised o in. Nothing in the printed body changes, so no card
that traces today can stop tracing; dcg_scheme.py uses a repaired line only
where this block holds it.
"""
import os
import re
import sys

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
START = '<!-- markbank:degree-signs -->'
END = '<!-- /markbank:degree-signs -->'
SUPERSCRIPT = 1          # pymupdf span flag


def degree_lines(pdf):
    """Every printed line holding a raised 'o' after a digit, repaired."""
    out = []
    with pymupdf.open(pdf) as doc:
        for page in doc:
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    spans = line['spans']
                    text, changed = '', False
                    for i, span in enumerate(spans):
                        t = span['text']
                        raised = (span['flags'] & SUPERSCRIPT and i > 0
                                  and span['size'] < spans[i - 1]['size'])
                        if raised and t.strip() == 'o' \
                                and re.search(r'\d\s*$', text):
                            text = text.rstrip() + '°' + (' ' if t.endswith(' ') else '')
                            changed = True
                            continue
                        text += t
                    if changed:
                        out.append(' '.join(text.split()))
    return out


def apply(subject, year, level):
    base = os.path.join(ROOT, 'examiner-reports', subject, 'schemes', f'{year}-{level}')
    md, pdf = base + '.md', base + '.pdf'
    lines = degree_lines(pdf)
    text = open(md, encoding='utf-8').read()
    if START in text:
        text = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '',
                      text, flags=re.S)
    if lines:
        if not text.endswith('\n'):
            text += '\n'
        text += f'{START}\n' + '\n'.join(lines) + f'\n{END}\n'
    with open(md, 'w', encoding='utf-8') as fh:
        fh.write(text)
    return f'{subject} {year} {level}: {len(lines)} line(s) with a degree sign'


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    print(apply(sys.argv[1], int(sys.argv[2]), sys.argv[3]))
