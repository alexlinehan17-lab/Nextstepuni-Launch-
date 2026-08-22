#!/usr/bin/env python3
"""Append each scheme PDF's block-ordered text to its markdown, for the gate.

    python3 scripts/markbank/authoring/append-scheme-blocks.py agricultural-science

The provenance gate — in the build, the deck test and provcheck — reads
examiner-reports/<subject>/schemes/<year>-<level>.md. That markdown is a
flattened conversion, and flattening a two-column scheme page interleaves the
columns: an answer that reads "Cows housed in loose house or slats" in the PDF
is spliced with the neighbouring column in the markdown. So a marking point
lifted correctly from the PDF can fail to trace, purely because the copy the
gate holds is damaged.

This appends the PDF's block-ordered text to the same file under a marker. The
scheme text the gate compares against becomes the union of both renderings, so:

  * every claim that traced before still traces — nothing is removed;
  * a claim lifted from a table cell now traces too, against text that came
    from the same SEC PDF.

It is a repair to the gate's copy of the source, not a loosening of the rule.
Re-runnable: the appended section is replaced, never stacked.
"""
import os
import re
import subprocess
import sys

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
MARK = '<!-- pdf-block-order: appended by append-scheme-blocks.py -->'
FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fold-scheme-text.mjs')


def fold(text):
    """Apply the bank's own glyph folding to text lifted straight from a PDF.

    The SEC typesets "letters" with a single Ʃ and "ti" with Ɵ, and
    test/markBankSchemes.test.ts holds every scheme file to being extractor
    output with those folded away. Shelling out to foldDigits keeps this the
    same fold the rest of the pipeline uses instead of a second copy of the
    table that could drift from it.
    """
    proc = subprocess.run(['node', FOLDER], input=text, capture_output=True,
                          text=True)
    if proc.returncode != 0:
        raise RuntimeError(f'fold-scheme-text.mjs failed: {proc.stderr.strip()}')
    return proc.stdout


def block_text(pdf):
    out = []
    with pymupdf.open(pdf) as doc:
        for n in range(doc.page_count):
            for b in sorted(doc[n].get_text('blocks'), key=lambda b: (round(b[1], 1), b[0])):
                text = ' '.join(b[4].split())
                if text:
                    out.append(text)
    return '\n'.join(out)


def main(subject):
    root = os.path.join(ROOT, 'examiner-reports', subject, 'schemes')
    done = 0
    for name in sorted(os.listdir(root)):
        if not name.endswith('.pdf'):
            continue
        md = os.path.join(root, name[:-4] + '.md')
        if not os.path.exists(md):
            print(f'  no markdown for {name} — skipped', file=sys.stderr)
            continue
        original = open(md, encoding='utf-8', errors='ignore').read()
        original = original.split(MARK)[0].rstrip('\n')
        appended = fold(block_text(os.path.join(root, name)))
        with open(md, 'w', encoding='utf-8') as fh:
            fh.write(f'{original}\n\n{MARK}\n\n{appended}\n')
        done += 1
        print(f'  {name[:-4]}.md  +{len(appended.splitlines())} block lines')
    print(f'{done} scheme(s) updated')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'agricultural-science')
