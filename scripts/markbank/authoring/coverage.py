#!/usr/bin/env python3
"""How much of each subject's papers the Mark Bank actually covers.

    python3 scripts/markbank/authoring/coverage.py            # every subject
    python3 scripts/markbank/authoring/coverage.py biology    # one

A subject is finished when every part of every paper it sets is carded, not
when every topic has been touched — Agricultural Science looked finished at 790
cards and was leaving 129 parts uncarded. This counts parts, so the number
means something.

A part counts as covered when some card's questionRef names it. The formats
differ by subject — "2021 HL Q1(b)", "2021 HL Section 1 Q1", "2023 HL Q4(iv),
(v)", "2022 HL Q11(b)(iv)–(v)" — so every question and part marker mentioned in
a reference is read out of it, and a card that cites a range covers the range.
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from align import align_ordered                             # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
AUTHORED = os.path.join(ROOT, 'scripts/markbank/authored')
SUBJECTS = ['agricultural-science', 'biology', 'business', 'chemistry',
            'economics', 'home-economics', 'physics']

HEAD = re.compile(r'(\d{4})\s+(HL|OL)\b')
QNUM = re.compile(r'\bQ\s?(\d{1,2})\b')
MARKER = re.compile(r'\(([a-hA-H]|i{1,3}|iv|vi{0,3})\)')


LETTERS = set('abcdefgh')


def covered(subject):
    """For each (year, level, question), the marker shapes cards cite for it.

    A reference names its markers in one of three shapes, and which shape it is
    decides what it covers. "Q11(c)(i)" names both a letter and a roman and
    covers only that one part. "Q11(b)" names a letter and covers everything
    under it. "Q3(v)" names a roman alone, which is how Physics cites a part the
    paper prints as Q3(b)(v) — so a bare roman covers that roman under any
    letter, while a letter that is named has to match.
    """
    out = collections.defaultdict(list)
    path = os.path.join(AUTHORED, f'{subject}.json')
    for card in json.load(open(path)):
        ref = card.get('questionRef') or ''
        h = HEAD.search(ref)
        if not h:
            continue
        year, level = int(h.group(1)), h.group(2).lower()
        for qm in QNUM.finditer(ref):
            q = int(qm.group(1))
            marks = [m.group(1).lower() for m in MARKER.finditer(ref[qm.end():])]
            # 'i' reads as both a letter and a roman; every paper in the corpus
            # that sets an (i) means the roman, so it is only ever read that way.
            letters = {m for m in marks if m in LETTERS and m != 'i'}
            romans = {m for m in marks if m not in letters}
            out[(year, level, q)].append((letters, romans))
    return out


def report(subject):
    done = covered(subject)
    total = uncovered = 0
    gaps = collections.Counter()
    for year in range(2021, 2026):
        for level in ('hl', 'ol'):
            try:
                P, S, pairs, positional = align_ordered(subject, year, level)
            except Exception:
                continue
            # Count in the PAPER's numbering, because that is what a card cites.
            # The two documents do not agree: Physics marks its answer sections
            # independently, so the scheme's Question 2 is the paper's Question
            # 14, and counting scheme keys against card references reported 65
            # Physics parts open that were carded all along.
            paired = {**positional, **pairs}
            for skey, (pkey, _) in paired.items():
                if not S.points(*skey):
                    continue
                q, letter, roman = pkey
                total += 1
                hit = False
                for letters, romans in done.get((year, level, q), ()):
                    if not letters and not romans:
                        hit = letter is None and roman is None
                    else:
                        hit = ((letter is None or not letters or letter in letters)
                               and (roman is None or not romans or roman in romans))
                    if hit:
                        break
                if not hit:
                    uncovered += 1
                    gaps[(year, level)] += 1
    pct = 100 - (uncovered * 100 // total) if total else 0
    print(f'{subject:<22} {total:>5} scheme parts   {total - uncovered:>5} covered   '
          f'{uncovered:>5} open   {pct:>3}%')
    return total, uncovered, gaps


if __name__ == '__main__':
    targets = sys.argv[1:] or SUBJECTS
    grand_t = grand_u = 0
    for s in targets:
        t, u, _ = report(s)
        grand_t += t
        grand_u += u
    if len(targets) > 1:
        print(f'\n{"TOTAL":<22} {grand_t:>5} scheme parts   '
              f'{grand_t - grand_u:>5} covered   {grand_u:>5} open')
