#!/usr/bin/env python3
"""Everything needed to author one excluded Economics part, in one place.

    python3 scripts/markbank/authoring/econ_backfill_scout.py [--bucket CHART] [--limit 20]

Economics reports "100.0%" coverage while excluding 154 of 658 asks. Bucketing
the exclusion reasons showed only 3 of the original 161 were the one blocker the
rules recognise ("the scheme prints no tariff"); the rest are charts whose crop
was already catalogued, tick tables, diagrams and worked calculations — every
one of which this bank has a mechanism for. This prints, per excluded ask:

  * the PAPER's wording (the question a student is set),
  * the SCHEME's block for it — printed tariff cells and split responses,
  * the catalogued figure keyed to that ref, with its alt text.

The scheme block is located by the paper's OWN wording rather than by a
(question, letter, roman) key. Economics agrees with that key in 12% of cases
(markbank-authoring-flow Law 4), but its scheme reprints each question above the
answer, so anchoring on the wording makes the pairing self-confirming: if the
anchor is found, the block returned is provably the one that answers this ask.

Nothing here decides anything. A refusal bucket is a hypothesis and so is a
page-adjacent figure — five of the first twenty-six crops matched this way were
for a different question entirely, and the alt text is what catches that.
"""
import argparse
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import paper as PP                      # noqa: E402
from econ_auto import Paper as SchemePaper  # noqa: E402

EXCL = os.path.join(DIR, 'exclusions/economics.json')
FIGS = os.path.join(ROOT, 'components/MarkBank/figures.json')
AUTHORED = os.path.join(ROOT, 'scripts/markbank/authored/economics.json')

REF = re.compile(r'(\d{4})\s+(HL|OL)\s+(?:Section ([A-Z])\s+)?Q(\d+)'
                 r'(?:\(([a-h])\))?(?:\(([ivx]+)\))?')


def bucket(reason):
    r = (reason or '').lower()
    if 'tick' in r:
        return 'TICK'
    if any(w in r for w in ('chart', 'graph printed', 'infographic', 'table printed',
                            'reading the', 'read off', 'reads the')):
        return 'CHART'
    if 'worked' in r or 'calculation' in r:
        return 'CALC'
    if any(w in r for w in ('label', 'diagram', 'drawn', 'graph to be', 'draw')):
        return 'DIAGRAM'
    if 'no tariff' in r or 'attributes no tariff' in r:
        return 'NO-TARIFF'
    if 'table completion' in r:
        return 'TABLE'
    return 'OTHER'


def anchors_from(question, n=3):
    """Distinctive openers for the scheme lookup, longest first.

    A scheme welds its answer onto the tail of its own question cue, so the
    first clause of the paper's wording is usually present verbatim above the
    responses. Several lengths are tried because the scheme sometimes rewrites
    the tail ("Sept. 22" for "September 2022").
    """
    words = re.sub(r'\s+', ' ', question or '').split()
    return [' '.join(words[i:i + 9]) for i in (0, 1, 2)][:n] + [' '.join(words[:6])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bucket')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--year', type=int)
    args = ap.parse_args()

    figs = {k: v for k, v in json.load(open(FIGS)).items() if k.startswith('economics-')}
    byref = {}
    for k, v in figs.items():
        r = re.sub(r'\s+', ' ', (v.get('questionRef') or '')).strip()
        if r:
            byref.setdefault(r, []).append(k)
    bound = {c['figureKey'] for c in json.load(open(AUTHORED)) if c.get('figureKey')}

    papers, schemes, shown = {}, {}, 0
    for e in json.load(open(EXCL)):
        ref = re.sub(r'\s+', ' ', e.get('ref', '')).strip()
        b = bucket(e.get('reason'))
        if args.bucket and b != args.bucket:
            continue
        m = REF.match(ref)
        if not m:
            print(f'!! ref not parsed: {ref}')
            continue
        year, lvl, sec, q, letter, roman = m.groups()
        year, q = int(year), int(q)
        if args.year and year != args.year:
            continue
        lv = 'hl' if lvl == 'HL' else 'ol'
        level = 'higher' if lv == 'hl' else 'ordinary'

        P = papers.setdefault((year, lv), PP.Paper('economics', year, lv))
        try:
            qtext = P.text(q, letter, roman)
        except Exception as exc:                     # noqa: BLE001
            qtext = f'<paper reader: {type(exc).__name__}: {exc}>'

        S = schemes.setdefault((year, level, sec), SchemePaper(year, level, sec) if sec
                               else SchemePaper(year, level))
        part, used = None, None
        for a in anchors_from(qtext):
            if not a.strip() or a.startswith('<'):
                break
            try:
                part, used = S.find(a), a
                break
            except Exception:                        # noqa: BLE001
                continue

        cands = byref.get(ref) or byref.get(re.sub(r'\([ivx]+\)$', '', ref).strip()) or []
        print('=' * 100)
        print(f'REF     {ref}   [{b}]')
        print(f'REASON  {(e.get("reason") or "")[:150]}')
        print(f'PAPER   {qtext}')
        if part:
            print(f'SCHEME  anchor={used[:48]!r}')
            print(f'        cells={part["cells"]} claim={part["claim"]} per={part["per"]} '
                  f'steps={part["steps"]} nopts={len(part["options"])}')
            for o in part['options'][:8]:
                print(f'          - {o[:220]}')
            if not part['options']:
                print(f'        WELDED: {(part.get("question") or "")[:400]}')
        else:
            print('SCHEME  <no block found by the paper\'s own wording>')
        for k in cands[:2]:
            print(f'FIGURE  {k}{"  (already bound)" if k in bound else ""}')
            print(f'        {(figs[k].get("alt") or "")[:220]}')
        if not cands:
            print('FIGURE  <none keyed to this ref>')
        shown += 1
        if args.limit and shown >= args.limit:
            break
    print('=' * 100)
    print(f'{shown} ask(s) shown')


if __name__ == '__main__':
    main()
