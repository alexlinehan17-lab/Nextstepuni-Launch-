#!/usr/bin/env python3
"""Every Construction Studies part the author refuses, with its scheme block.

    python3 scripts/markbank/authoring/cs_why.py            # tally
    python3 scripts/markbank/authoring/cs_why.py --dump     # and the blocks

Written because "the scheme prints no tariff" was claimed for 87 parts of a
document that prices every line it awards. A refusal that frequent is a reader
fault until the scheme itself is read and says otherwise.
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cs_lib                                                # noqa: E402
from cs_lib import Author, Refused                           # noqa: E402


def reason(e):
    s = str(e)
    if 'past the 14' in s:
        return 'display cap'
    if 'prints no tariff' in s:
        return 'no tariff found'
    if 'never prints' in s:
        return 'tariff derived'
    if 'claims' in s:
        return 'tariff > options'
    if 'not in the scheme' in s:
        return 'extraction'
    return 'other'


if __name__ == '__main__':
    dump = '--dump' in sys.argv
    want = next((a for a in sys.argv[1:] if not a.startswith('--')), None)
    tally, shown = Counter(), 0
    for year in range(2021, 2026):
        for level in ('hl', 'ol'):
            A = Author(year, level)
            for (q, letter) in A.S.parts():
                if not A.question(q, letter):
                    continue
                gs = [g for g in A.S.groups(q, letter, 'indicative') if len(g[2]) >= 2]
                if not gs:
                    continue
                try:
                    A.card(q, letter, cid=f'probe-{year}-{level}-{q}-{letter}',
                           topic='cons-1-1', concept='probe')
                    tally['CARDED'] += 1
                except Refused as e:
                    r = reason(e)
                    tally[r] += 1
                    if dump and (want is None or want == r) and shown < 26:
                        shown += 1
                        print(f'=== {year} {level.upper()} Q{q}({letter})  [{r}] ===')
                        print(f'    Q: {A.question(q, letter)[:120]}')
                        for l in A.S.marks.get((q, letter), [])[:14]:
                            print(f'    | {l[:104]}')
                        print()
    for k, v in tally.most_common():
        print(f'{v:>4}  {k}')
