#!/usr/bin/env python3
"""Write the exclusions ledger for Technology, from the author's own refusals.

    python3 scripts/markbank/authoring/tech_exclusions.py --write

An exclusion is a claim that the scheme prints nothing liftable for an ask,
and reconcile.py refuses one that no longer matches an OPEN ask. Only ONE
refusal in this subject is that claim: the parts whose answer the scheme
prints as a DRAWING -- a circuit, a symbol, a sketch, a truth table -- with no
marking point beside it. Everything else the author refuses is refused for the
author's own limits (a figure it cannot carry, letters it cannot decode), and
those stay OPEN, which is what they are.

Generated rather than hand-kept because the set moves whenever the reader
improves: eleven of these were "no marking point" until the reader learned to
read a worked calculation, and an exclusion left behind after that is a stale
claim the ledger rightly reports.
"""
import argparse
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import paper_census as PC                                    # noqa: E402
import tech_all as TA                                        # noqa: E402
from tech_scheme import TechScheme                           # noqa: E402

# The two refusals that ARE the exclusion claim: the scheme prints no marking
# point for this part. Both are the same fact seen from two sides -- the text
# layer holds nothing at all, or it holds the words the extractor read off a
# drawing, which state nothing either.
REASONS = {
    'the scheme states no marking point for this part':
        'the answer the scheme prints for this part is a DRAWING - a circuit, '
        'a symbol, a sketch or a truth table - and it states no marking point '
        'beside it. The tariff IS printed, so the part is priced; there is '
        'simply nothing to lift.',
    'the scheme answers this part with a drawing the text layer reads as '
    'fragments':
        'the answer the scheme prints for this part is a DRAWING, and what '
        'the text layer holds is the words written INSIDE it - a flowchart\'s '
        'boxes, a truth table\'s rows. Not one of them states a marking '
        'point, and each would be a row a student is asked to tick.',
}
OUT = os.path.join(DIR, 'exclusions', 'technology.json')

REF = re.compile(r'(\d{4}) (HL|OL) Section ([ABC]) Q(\d{1,2})'
                 r'(?:\(([a-d])\))?(?:\((i{1,3}|iv|v)\))?')


def build():
    _cards, _refused, _examples, verdicts, _stats = TA.author()
    rows = []
    for v in verdicts:
        if v['reason'] not in REASONS:
            continue
        m = REF.match(v['ref'])
        year, level = int(m.group(1)), m.group(2).lower()
        section, q = m.group(3), int(m.group(4))
        letter, roman = m.group(5), m.group(6)
        scheme = TechScheme(year, level)
        block = scheme.blocks.get((section, q, letter))
        keys, texts, _files = PC.census_sections('technology', year, level)
        leaves = {tuple(k): texts[k] for k in PC.leaves_of(keys)}
        lines = [TA.clean(t) for t in (block.part_lines(roman)
                                       if block.romans() else block.head_lines())]
        ask = TA.clean_ask(leaves.get((section, q, letter, roman), ''))
        _cue, points = TA.split_cue(lines, ask)
        body = ' '.join(points).strip()
        address = v['ref'].split('Section ', 1)[1]
        rows.append({
            'ref': v['ref'],
            'reason': REASONS[v['reason']],
            'evidence': (
                f'{year} {level.upper()} scheme, {address}: tariff '
                f'{block.notation!r}; the scheme reprints the ask '
                f'({lines[0][:80]!r}) and answers it graphically'
                + (f', leaving only {body[:100]!r} in the text layer'
                   if body else ', with no text at all beneath it')),
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    rows = build()
    print(f'{len(rows)} exclusion(s)')
    for r in rows:
        print(f'   {r["ref"]}')
    if args.write:
        with open(OUT, 'w', encoding='utf-8') as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=1)
        print(f'wrote {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
