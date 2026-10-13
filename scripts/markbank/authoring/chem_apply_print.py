#!/usr/bin/env python3
"""Write one printed-layout sitting's cards into authored/chemistry.json.

    python3 scripts/markbank/authoring/chem_apply_print.py 2026 hl          # write
    python3 scripts/markbank/authoring/chem_apply_print.py 2026 hl --check  # verify

The cards come from scripts/markbank/authoring/chem_<year>_<lvl>.py, which
lifts every string from the paper and the scheme. This file only places them:
a card whose id is already in the deck is replaced where it stands, a new one
is appended, and nothing else in the deck is touched.

It refuses to drop a card. If the deck holds an id under this sitting's prefix
that the generator no longer emits, the run stops: a student may have progress
against that id, and withdrawing it takes a correction record and an alias
(card-corrections.json, cardAliases.ts), never a silent rewrite.

--check exits non-zero unless the deck already holds exactly what the
generator emits, byte for byte, which is how a reviewer confirms the committed
cards are reproducible from the committed scripts.
"""
import argparse
import importlib
import json
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
DECK = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'chemistry.json')
sys.path.insert(0, DIR)

EMPTY = {'stem': '', 'figureKey': '', 'labelKey': [], 'notes': ''}


def lean(card):
    return {k: v for k, v in card.items() if not (k in EMPTY and v == EMPTY[k])}


def merged(year, lvl):
    mod = importlib.import_module(f'chem_{year}_{lvl}')
    problems = mod.make_audit(mod.MAX_OPTIONS)(mod.C.cards)
    if problems:
        raise SystemExit('audit refused:\n  ' + '\n  '.join(problems))
    cards = [lean(c) for c in mod.C.finish()]
    prefix = f'chem-{year}-{lvl}-'
    deck = json.load(open(DECK))
    made = {c['id']: c for c in cards}
    if len(made) != len(cards):
        raise SystemExit('the generator emits a duplicate id')
    held = [c['id'] for c in deck if c['id'].startswith(prefix)]
    gone = [i for i in held if i not in made]
    if gone:
        raise SystemExit(f'refusing to drop {len(gone)} card(s) already in the deck: {gone}')
    out, placed = [], set()
    for c in deck:
        if c['id'] in made:
            out.append(made[c['id']])
            placed.add(c['id'])
        else:
            out.append(c)
    out += [c for c in cards if c['id'] not in placed]
    return out, len(cards), len(cards) - len(placed)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('lvl', choices=['hl', 'ol'])
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    out, n, new = merged(args.year, args.lvl)
    text = json.dumps(out, ensure_ascii=False, indent=1)
    if args.check:
        same = open(DECK).read() == text
        print(f'{"ok" if same else "DIFFERS"}: {n} {args.year} {args.lvl.upper()} cards')
        sys.exit(0 if same else 1)
    with open(DECK, 'w') as f:
        f.write(text)
    print(f'{n} {args.year} {args.lvl.upper()} cards written ({new} new); deck holds {len(out)}')


if __name__ == '__main__':
    main()
