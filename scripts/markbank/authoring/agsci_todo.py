#!/usr/bin/env python3
"""Open Agricultural Science parts: what the paper asks, what the scheme accepts.

    python3 scripts/markbank/authoring/agsci_todo.py 2021 hl

A part is open when the scheme has marking points for it and no shipped card
cites it. Prints what both documents hold so the topic and the tariff can be
decided without opening either — but never proposes a card, because which
marking points belong on one is a judgement, not a lookup.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author, part_ref                       # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
AUTHORED = os.path.join(ROOT, 'scripts/markbank/authored/agricultural-science.json')
REF = re.compile(r'^(\d{4})\s+(HL|OL)\s+Q(\d{1,2})(?:\(([a-h])\))?(?:\(([ivx]{1,4})\))?')


def carded():
    out = set()
    for c in json.load(open(AUTHORED)):
        m = REF.match(c.get('questionRef') or '')
        if m:
            y, lv, q, l, r = m.groups()
            out.add((int(y), lv.lower(), int(q), l, r))
    return out


def main(year, level):
    done = carded()
    A = Author(year, level)
    shown = 0
    for key in A.scheme.paths():
        q, letter, roman = key
        if (year, level, q, letter, roman) in done:
            continue
        o = A.offer(q, letter, roman)
        if not o['question'] or not o['usable']:
            continue
        shown += 1
        flag = '  [FLAGGED question text]' if o['suspect'] else ''
        print(f"\n{o['ref']}   marks={','.join(o['marks']) or '-'}{flag}")
        print(f"   Q: {o['question']}")
        for i, p, traces in o['points']:
            print(f"   [{i}] {'+' if traces else 'x'} {p[:104]}"
                  f"{'' if traces else '   (does not trace — unusable)'}")
    print(f'\n{shown} open part(s) for {year} {level.upper()}')


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2])
