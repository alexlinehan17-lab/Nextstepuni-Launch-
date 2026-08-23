#!/usr/bin/env python3
"""Append a DEMANGLED form of a Mathematics scheme to its markdown.

    python3 scripts/markbank/append-scheme-notation.py --all

A Maths scheme's notation does not survive extraction: CambriaMath doubles each
italic variable and its ToUnicode map puts several glyphs in the wrong Unicode
block, so "4x^3" is stored as "4𝑥𝑥3" and a card quoting the repaired form cannot
be traced to the scheme that printed it.

mathtext.py repairs that deterministically. This writes the repaired text into
the markdown as an ADDED form, the same way append-scheme-tables.py and the
others do: append-only, idempotent, and a fold can only ever let a card trace
that could not before — no passing card can start failing.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'authoring'))
import mathtext                                              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
START = '<!-- markbank:demangled-notation -->'
END = '<!-- /markbank:demangled-notation -->'


def apply(subject, year, level):
    import pymupdf
    base = os.path.join(ROOT, 'examiner-reports', subject, 'schemes', f'{year}-{level}')
    md, pdf = base + '.md', base + '.pdf'
    if not (os.path.exists(md) and os.path.exists(pdf)):
        return f'{subject} {year} {level}: no scheme, skipped'
    lines = []
    with pymupdf.open(pdf) as doc:
        for page in doc:
            for b in page.get_text('dict')['blocks']:
                for ln in b.get('lines', []):
                    t = mathtext.line_text(ln)
                    if t:
                        lines.append(t)
    body = f'{START}\n' + '\n'.join(lines) + f'\n{END}\n'
    text = open(md, encoding='utf-8').read()
    if START in text:
        text = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '',
                      text, flags=re.S)
    open(md, 'w', encoding='utf-8').write(text.rstrip('\n') + '\n\n' + body)
    return f'{subject} {year} {level}: appended {len(lines)} demangled lines'


if __name__ == '__main__':
    if sys.argv[1:2] == ['--all']:
        d = os.path.join(ROOT, 'examiner-reports', 'maths', 'schemes')
        for f in sorted(os.listdir(d)):
            m = re.fullmatch(r'(\d{4})-(hl|ol)\.md', f)
            if m:
                print(apply('maths', int(m.group(1)), m.group(2)))
    else:
        print(apply(sys.argv[1], int(sys.argv[2]), sys.argv[3]))
