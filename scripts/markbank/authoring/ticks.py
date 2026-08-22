#!/usr/bin/env python3
"""Read the answers a marking scheme states with a tick.

    python3 scripts/markbank/authoring/ticks.py biology 2021 hl

True/false questions are answered by putting a tick in a True or False column.
The tick is a Wingdings check mark, U+F050, and the text extraction drops it
into an empty-looking block — which is why no parser could read these, and why
the parsers then handed the question the NEXT question's marking points.

But the glyph is in the text layer, and it has coordinates. So does the column
heading it sits under, and so does the statement it sits beside. Matching a
tick's x against the headings gives the answer and its y against the statements
gives the question, which turns a page that had to be looked at into one that
can be read outright — and the same page can still be rendered and eyeballed to
check the reading, which is how this was verified on Biology 2021 HL.
"""
import os
import re
import sys

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
TICK = re.compile(r'[✓✔]')
LETTER = re.compile(r'^\(([a-h])\)$')
QNUM = re.compile(r'^\d{1,2}$')


def read(subject, year, level):
    """-> {(page, letter): 'True'|'False'} for every ticked statement found."""
    path = os.path.join(ROOT, 'examiner-reports', subject, 'schemes',
                        f'{year}-{level}.pdf')
    out = {}
    with pymupdf.open(path) as doc:
        for pno in range(doc.page_count):
            words = doc[pno].get_text('words')
            heads = {w[4]: (w[0] + w[2]) / 2 for w in words if w[4] in ('True', 'False')}
            if len(heads) < 2:
                continue
            ticks = [w for w in words if TICK.search(w[4])]
            letters = [(w[1], LETTER.match(w[4]).group(1)) for w in words
                       if LETTER.match(w[4])]
            if not ticks or not letters:
                continue
            # The question these statements belong to: the last "Question N"
            # printed above them on the page.
            qheads = [(w[1], int(words[i + 1][4]))
                      for i, w in enumerate(words[:-1])
                      if w[4] in ('Question', 'QUESTION') and QNUM.match(words[i + 1][4])]
            for tx0, ty0, tx1, ty1, *_ in ticks:
                cx = (tx0 + tx1) / 2
                # Nearest column heading by x, nearest statement by y.
                answer = min(heads, key=lambda k: abs(heads[k] - cx))
                near = min(letters, key=lambda pair: abs(pair[0] - ty0))
                if abs(near[0] - ty0) <= 24:
                    above = [qn for qy, qn in qheads if qy <= ty0]
                    qnum = above[-1] if above else None
                    out[(pno + 1, qnum, near[1])] = answer
    return out


if __name__ == '__main__':
    subject, year, level = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    got = read(subject, year, level)
    for (page, qnum, letter), answer in sorted(got.items(), key=lambda kv: (kv[0][0], kv[0][2])):
        print(f'  p{page:<3} Q{qnum} ({letter})  {answer}')
    print(f'{len(got)} ticked statement(s)')
