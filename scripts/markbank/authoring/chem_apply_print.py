#!/usr/bin/env python3
"""Write one sitting's reviewed Chemistry cards into the deck, with their record.

    python3 scripts/markbank/authoring/chem_apply_print.py 2025 hl          # write
    python3 scripts/markbank/authoring/chem_apply_print.py 2025 hl --check  # verify

The cards come from the sitting's generator -- chem_audit_<year>_<lvl>.py for
a sitting carded before the audit, chem_<year>_<lvl>.py for one carded fresh
(2026) -- which lifts every string from the paper and the scheme. This file
only places them, and records what it did:

  * a card whose id is already in the deck is replaced where it stands
    (corrected in place: the id, and so every student's progress on it, is
    kept);
  * a new card is appended (so is a pre-audit card the base build never
    shipped, which the ledger records as added, `shipped: false`);
  * a pre-audit card the generator names in WITHDRAWN -- a duplicate, or a
    piece of a task the scheme prices as one -- stays in the deck untouched
    and is withdrawn at build time by a card-corrections.json "drop" naming
    its replacement, with a cardAliases.ts entry so its review history is read
    by the card that replaces it;
  * anything else under the sitting's prefix that the generator does not
    emit stops the run. A student may have progress on it.

The ledger, scripts/markbank/authored/chemistry-audit-ledger.json, records
every id of the sitting as added, corrected, unchanged or withdrawn, with the
hash of the card before the audit (read from the audit's base commit, so a
re-run records the same thing) and after it, and which fields changed. A
withdrawn card also records whether the base build shipped it; the
preservation test reads the ledger to rebuild the frozen pre-audit id set.

--check exits non-zero unless the deck, the corrections, the aliases and the
ledger already hold exactly what this would write: the committed cards are
reproducible from the committed scripts.
"""
import argparse
import hashlib
import importlib
import json
import os
import re
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
DECK = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'chemistry.json')
LEDGER = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'chemistry-audit-ledger.json')
CORRECTIONS = os.path.join(ROOT, 'scripts', 'markbank', 'card-corrections.json')
ALIASES = os.path.join(ROOT, 'components', 'MarkBank', 'cardAliases.ts')
sys.path.insert(0, DIR)

EMPTY = {'stem': '', 'figureKey': '', 'labelKey': [], 'notes': ''}
FIELDS = ['topicId', 'conceptId', 'section', 'questionRef', 'stem', 'questionText', 'tariffModel',
          'totalMarks', 'rows', 'notes', 'figureKey', 'questionFigureKey', 'labelKey']


def lean(card):
    return {k: v for k, v in card.items() if not (k in EMPTY and v == EMPTY[k])}


def digest(card):
    return hashlib.sha256(json.dumps(card, sort_keys=True, ensure_ascii=False)
                          .encode('utf-8')).hexdigest()[:16]


def generator(year, lvl):
    for name in (f'chem_audit_{year}_{lvl}', f'chem_{year}_{lvl}'):
        if os.path.exists(os.path.join(DIR, name + '.py')):
            return importlib.import_module(name)
    raise SystemExit(f'no generator for {year} {lvl}')


def plan(year, lvl):
    mod = generator(year, lvl)
    problems = mod.make_audit(mod.MAX_OPTIONS)(mod.C.cards)
    if problems:
        raise SystemExit('audit refused:\n  ' + '\n  '.join(problems))
    from chem_print import prior_deck
    cards = [lean(c) for c in mod.C.finish()]
    withdrawn = getattr(mod, 'WITHDRAWN', {})
    prefix = f'chem-{year}-{lvl}-'
    made = {c['id']: c for c in cards}
    if len(made) != len(cards):
        raise SystemExit('the generator emits a duplicate id')
    deck = json.load(open(DECK))
    held = {c['id']: c for c in deck if c['id'].startswith(prefix)}
    prior = {i: c for i, c in prior_deck().items() if i.startswith(prefix)}
    for old, (new, _reason) in withdrawn.items():
        if old not in prior:
            raise SystemExit(f'{old}: withdrawn but not a pre-audit card')
        if old in made:
            raise SystemExit(f'{old}: both emitted and withdrawn')
        if new not in made:
            raise SystemExit(f'{old}: its replacement {new} is not emitted')
    gone = [i for i in held if i not in made and i not in withdrawn]
    if gone:
        raise SystemExit(f'refusing to drop {len(gone)} card(s) already in the deck: {gone}')

    out, placed = [], set()
    for c in deck:
        if c['id'] in made:
            out.append(made[c['id']])
            placed.add(c['id'])
        elif c['id'] in withdrawn:
            out.append(prior[c['id']])           # untouched; withdrawn at build
        else:
            out.append(c)
    out += [c for c in cards if c['id'] not in placed]

    record = {}
    shipped = base_built_ids()
    for c in cards:
        before = prior.get(c['id'])
        if before is None:
            record[c['id']] = {'status': 'added', 'after': digest(c)}
            continue
        if c['id'] not in shipped:
            # In the base's authored file but never built (the build kept
            # another card with the same citation): no student can have
            # progress on it, so to the preservation test it is an addition.
            record[c['id']] = {'status': 'added', 'before': digest(before), 'after': digest(c),
                               'shipped': False}
            continue
        changed = [f for f in FIELDS if lean(before).get(f) != c.get(f)]
        record[c['id']] = {'status': 'corrected' if changed else 'unchanged',
                           'before': digest(before), 'after': digest(c),
                           **({'changed': changed} if changed else {})}
    for old, (new, reason) in withdrawn.items():
        # "shipped": whether the base build carried this card, so whether any
        # student can have progress on it. The preservation test restores
        # exactly the shipped withdrawals when it rebuilds the frozen set.
        record[old] = {'status': 'withdrawn', 'before': digest(prior[old]),
                       'replacementId': new, 'reason': reason, 'shipped': old in shipped}
    return out, record, withdrawn


def base_built_ids():
    """The Chemistry card ids the audit's base commit BUILT (its generated
    decks), as distinct from the ids its authored file held: the build drops a
    card it cannot keep, such as the second of two cards with one citation."""
    from chem_print import AUDIT_BASE
    ids = set()
    for level in ('higher', 'ordinary'):
        ts = subprocess.run(['git', 'show', f'{AUDIT_BASE}:components/MarkBank/cards/chemistry/{level}.ts'],
                            cwd=ROOT, capture_output=True, text=True, check=True).stdout
        ids |= set(re.findall(r'\bid: "(chem-[^"]+)"', ts))
    if not ids:
        raise SystemExit('could not read the base build')
    return ids


def no_longer_withdrawn(year, lvl, withdrawn):
    """Ids this sitting's ledger last recorded as withdrawn that the generator
    now emits again: their build-time drop and progress alias are stale."""
    if not os.path.exists(LEDGER):
        return set()
    paper = json.load(open(LEDGER)).get('papers', {}).get(f'{year} {lvl.upper()}', {})
    return {i for i, r in paper.items() if r['status'] == 'withdrawn'} - set(withdrawn)


def corrections_text(withdrawn, stale=()):
    data = json.load(open(CORRECTIONS))
    chem = data.setdefault('chemistry', {})
    for old in stale:
        if chem.get(old, {}).get('drop'):
            del chem[old]
    for old, (new, reason) in withdrawn.items():
        chem[old] = {'reason': reason, 'drop': True, 'replacementId': new}
    return json.dumps(data, ensure_ascii=False, indent=1) + '\n'


def aliases_text(withdrawn, stale=()):
    text = open(ALIASES).read()
    lines = [l for l in text.split('\n')
             if not any(l.startswith(f'  "{old}": ') for old in stale)]
    text = '\n'.join(lines)
    have = dict(re.findall(r'^  "([^"]+)": "([^"]+)",$', text, re.M))
    for old, (new, _reason) in sorted(withdrawn.items()):
        if old in have:
            if have[old] != new:
                raise SystemExit(f'{old}: already aliased to {have[old]}, not {new}')
            continue
        # Chemistry's aliases are kept together, in id order.
        at = max((i for i, l in enumerate(lines) if l.startswith('  "chem-')),
                 default=next(i for i, l in enumerate(lines) if l.startswith('export const')))
        for i, l in enumerate(lines):
            m = re.match(r'^  "(chem-[^"]+)":', l)
            if m and m.group(1) > old:
                at = i - 1
                break
        lines.insert(at + 1, f'  "{old}": "{new}",')
    return '\n'.join(lines)


def ledger_text(year, lvl, record):
    data = json.load(open(LEDGER)) if os.path.exists(LEDGER) else {}
    from chem_print import AUDIT_BASE
    data['base'] = AUDIT_BASE
    papers = data.setdefault('papers', {})
    papers[f'{year} {lvl.upper()}'] = dict(sorted(record.items()))
    data['papers'] = dict(sorted(papers.items()))
    return json.dumps(data, ensure_ascii=False, indent=1) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('lvl', choices=['hl', 'ol'])
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    out, record, withdrawn = plan(args.year, args.lvl)
    files = {DECK: json.dumps(out, ensure_ascii=False, indent=1),
             LEDGER: ledger_text(args.year, args.lvl, record)}
    stale = no_longer_withdrawn(args.year, args.lvl, withdrawn)
    if withdrawn or stale:
        files[CORRECTIONS] = corrections_text(withdrawn, stale)
        files[ALIASES] = aliases_text(withdrawn, stale)
    counts = {s: sum(r['status'] == s for r in record.values())
              for s in ('added', 'corrected', 'unchanged', 'withdrawn')}
    if args.check:
        bad = [os.path.relpath(p, ROOT) for p, t in files.items()
               if not os.path.exists(p) or open(p).read() != t]
        print(('ok' if not bad else 'DIFFERS ' + ', '.join(bad)) + f': {args.year} '
              f'{args.lvl.upper()} {counts}')
        sys.exit(1 if bad else 0)
    for p, t in files.items():
        with open(p, 'w') as f:
            f.write(t)
    print(f'{args.year} {args.lvl.upper()}: {counts}; deck holds {len(out)}')


if __name__ == '__main__':
    main()
