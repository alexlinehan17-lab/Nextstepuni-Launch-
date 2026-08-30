#!/usr/bin/env python3
"""Author every Computer Science part the scheme states and prices.

    python3 scripts/markbank/authoring/cs_all.py            # emit JSON
    python3 scripts/markbank/authoring/cs_all.py --report   # counts and refusals

Unlike the other subjects, this one is driven from the CENSUS rather than from
a hand-written work list: 484 asks is too many to enumerate by hand, and every
card here is the scheme's own text against the paper's own ask, so there is
nothing per-card to decide except the topic. What the census says the paper
prints is the list; what cs_scheme states and prices is what can be carded.

Three refusals, all of them the rules already in force:

  * the scheme states nothing at this key,
  * it prints no tariff that reads one way -- see cs_scheme.tariff(), which
    takes the part's own row, then the parent's printed split, then the
    paper's "All questions carry equal marks" rubric, and refuses beyond that,
  * the wording files under no syllabus topic. A wrong shelf sends a student
    to revise the wrong thing; a gap only asks a person to look.

The lead-in "Any response that captures the essence of any of the following:"
is dropped where the scheme prints it. It introduces the marking points and is
not one of them, and a card that opened with it would be quoting the
examiner's instruction to the examiner.
"""
import argparse
import collections
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)

import paper as PP                                          # noqa: E402
import reconcile as R                                       # noqa: E402
from paper_census import census_subject                     # noqa: E402
from lib import Author, Refused                             # noqa: E402
from cs_topics import topic_for, concept_for                 # noqa: E402
import cardlint                                             # noqa: E402

# The examiner's instruction ABOUT the marking points, not one of them.
LEAD_IN = re.compile(r'^(any response that captures|any \w+ of the following|'
                     r'accept any|examples? of|the following are|'
                     r'any \d+ (?:from|of)|marks? awarded for)', re.I)
# A row of a printed table or a fragment of a code listing that the paper
# reader lifted as prose. It is not a marking point and reads as noise.
NOT_PROSE = re.compile(r'^[\W\d]+$')
MAX_ROWS = 12


def cardable(points):
    """The marking points a card may claim, lead-in and noise removed."""
    out = []
    for p in points:
        t = ' '.join(p.split())
        if not t or LEAD_IN.match(t) or NOT_PROSE.match(t):
            continue
        if len(t) < 3:
            continue
        out.append(t)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    args = ap.parse_args()

    idx = R.leaf_index(census_subject('computer-science'))
    cards, refused = [], collections.Counter()
    examples = collections.defaultdict(list)

    for (year, level, _), leaves in sorted(idx.items()):
        A = Author('computer-science', year, level)
        table = A._source('table')
        for leaf in sorted(leaves):
            section, q, letter, roman = leaf[0], leaf[1], leaf[2], leaf[3]
            ref = (f'{year} {level.upper()} Q{q}'
                   + (f'({letter})' if letter else '')
                   + (f'({roman})' if roman else ''))
            try:
                ask = A.paper.text(q, letter, roman) or ''
            except Exception:                                # noqa: BLE001
                ask = ''
            rows = cardable(table.points(q, letter, roman))
            tariff = table.tariff(q, letter, roman)
            topic, _ = topic_for(ask + ' ' + ' '.join(rows))

            def note(reason):
                refused[reason] += 1
                if len(examples[reason]) < 4:
                    examples[reason].append(f'{ref}: {" ".join(ask.split())[:60]}')

            if not ask.strip():
                note('the paper reader recovers no ask')
                continue
            if not rows:
                note('the scheme states nothing at this key')
                continue
            if not tariff:
                note('no tariff that reads one way')
                continue
            if not topic:
                note('files under no syllabus topic')
                continue
            # The same rule card lint applies to the shipped deck, applied
            # here so the card is never written rather than written and
            # flagged. Computer Science trips it more than any other subject:
            # its questions print PROGRAMS, and the text layer gives them back
            # as "1 def gcd(a, b): 2 while a != b: 3 if a > b:" -- a listing
            # with its line numbers run into the code. That belongs in a crop,
            # which is a figure pass this subject has not had.
            # Card lint reads the STEM as well as the question text, and the
            # stem is where a shared "such as that shown in Figure 3" lives.
            stem = ''
            try:
                stem = A.paper.stem(q, letter) or A.paper.stem(q) or ''
            except Exception:                                # noqa: BLE001
                pass
            joined = ' '.join(f'{stem} {ask}'.split())
            if (cardlint.FIG_REF.search(joined)
                    and not cardlint.SELF_WORK.search(joined)
                    and not cardlint.NO_DEPENDENCY.search(joined)):
                note('points at printed matter the card cannot carry')
                continue
            if len(rows) > MAX_ROWS:
                rows = rows[:MAX_ROWS]
            # One mark per point where the tariff divides, else the whole
            # tariff on a single claim. Never a guessed split.
            if len(rows) == 1 or tariff % len(rows):
                use, marks = [0], [tariff]
                rows = rows[:1]
            else:
                use, marks = list(range(len(rows))), [tariff // len(rows)] * len(rows)
            cid = (f'cs-{year}-{level}-q{q}'
                   + (f'-{letter}' if letter else '')
                   + (f'-{roman}' if roman else ''))
            try:
                A.card(q, letter, roman, topic=topic,
                       concept=concept_for(ask), source='table',
                       use=use, marks=marks, tariff='fixed', card_id=cid)
            except Refused as exc:
                note(str(exc).split(':', 1)[-1].strip()[:60])
        cards.extend(A.cards)

    if args.report:
        print(f'{len(cards)} card(s) from {sum(len(v) for v in idx.values())} asks')
        for reason, n in refused.most_common():
            print(f'   {n:4} REFUSED  {reason}')
            for e in examples[reason][:3]:
                print(f'             {e}')
        return 0
    print(json.dumps(cards, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
