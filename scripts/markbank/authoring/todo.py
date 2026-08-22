#!/usr/bin/env python3
"""Open parts for a subject: what the paper asks and what the scheme accepts.

    python3 scripts/markbank/authoring/todo.py economics 2021 hl

A part is open when the scheme has marking points for it and no card's
questionRef names it. Prints both documents' content so the topic and tariff can
be decided without opening either, but never proposes a card: which marking
points belong on one is a judgement, not a lookup.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coverage import covered                                # noqa: E402
from lib import Author                                      # noqa: E402


def main(subject, year, level, source='pdf'):
    done = covered(subject)
    A = Author(subject, year, level)
    scheme = A.scheme_pdf if source == 'pdf' else A.scheme
    shown = 0
    for key in scheme.paths():
        q, letter, roman = key
        if any(x in done for x in [(year, level, q, letter, roman),
                                   (year, level, q, letter, None),
                                   (year, level, q, None, roman)]):
            continue
        o = A.offer(q, letter, roman, source=source)
        if not o['usable']:
            continue
        shown += 1
        flag = '  [FLAGGED question text]' if o['suspect'] else ''
        print(f"\n{o['ref']}   marks={','.join(o['marks']) or '-'}{flag}")
        print(f"   Q: {(o['question'] or '(no paper text)')[:150]}")
        for i, p, traces in o['points']:
            print(f"   [{i}] {'+' if traces else 'x'} {p[:110]}")
    print(f'\n{shown} open part(s) for {subject} {year} {level.upper()}')


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3],
         sys.argv[4] if len(sys.argv) > 4 else 'pdf')
