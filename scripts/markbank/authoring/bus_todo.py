#!/usr/bin/env python3
"""Business parts with no card asking them.

    python3 scripts/markbank/authoring/bus_todo.py           # all ten papers
    python3 scripts/markbank/authoring/bus_todo.py 2023 hl   # one

Reads the part list out of the marking scheme with bus_parts, because the paper
is an answerbook the generic parser cannot follow — sixty-six Business parts
could not be measured at all before this. Coverage is decided on the question
text, the same test partcheck.py uses for every other subject: a part is carded
when some card of that year and level asks it.

Sections 2 and 3 only. Section 1's scheme table is tariff with no wording.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bus_parts import parts, ref                            # noqa: E402
from partcheck import squash, covered_by_text, FLOOR        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
CARDS = os.path.join(ROOT, 'scripts/markbank/authored/business.json')


def asked(year, level):
    """Question texts and cited references for one paper."""
    texts, refs = [], set()
    for c in json.load(open(CARDS)):
        lv = 'hl' if str(c.get('level', '')).lower().startswith('h') else 'ol'
        if int(c['year']) == year and lv == level:
            texts.append(squash(c.get('questionText')))
            refs.add(squash(c.get('questionRef')))
    return texts, refs


def run(year, level, show=True):
    texts, refs = asked(year, level)
    open_ = short = 0
    for p in parts(year, level):
        r = ref(p, year, level)
        # Some questions are too short to identify by their wording — 'What do
        # the letters CCPC stand for?' is 28 characters once punctuation is
        # dropped, and several papers ask it. For those the citation is the only
        # handle there is, and this subject's citations follow the scheme's own
        # section-and-part numbering, which is exactly what bus_parts reads.
        if squash(r) in refs:
            continue
        if len(squash(p['text'])) < FLOOR:
            # 'Employer and employee' is a bullet under its part, not a question.
            short += 1
            continue
        if covered_by_text(p['text'], texts):
            continue
        open_ += 1
        if show:
            print(f"\n{r}  [{','.join(p['marks']) or '-'}]")
            print(f"   Q: {p['text'][:170]}")
    return open_, short


if __name__ == '__main__':
    if len(sys.argv) > 2:
        o, s = run(int(sys.argv[1]), sys.argv[2])
        print(f'\n{o} uncarded part(s); {s} too short to measure')
    else:
        total = shorts = 0
        for y in range(2021, 2026):
            for l in ('hl', 'ol'):
                o, s = run(y, l, show=False)
                total += o
                shorts += s
                print(f'{y} {l.upper()}   {o:>3} uncarded   {s:>3} too short')
        print(f'\n{total} uncarded across ten papers; {shorts} too short to measure')
