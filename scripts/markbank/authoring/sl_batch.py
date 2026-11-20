#!/usr/bin/env python3
"""Card one classic sitting of a small language into its authored file.

    python3 scripts/markbank/authoring/sl_batch.py review dutch 2010
    python3 scripts/markbank/authoring/sl_batch.py write dutch 2010

The small-languages lane's merge step (20 Nov 2026). A sitting's new cards come
from its reviewed specs (sl_specs_<subject>.py, built by sl_lib); every card
already in scripts/markbank/authored/<subject>.json is kept BYTE FOR BYTE (the
generator no longer reproduces every live card, so the file is never
regenerated). New cards are inserted after the last card of an earlier or the
same year. An exclusions entry whose ask a new card now answers is removed in
the same write, so the ledger never claims a carded ask is excluded.
"""
import collections
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

import sl_lib                                                       # noqa: E402


def authored_path(subject):
    return os.path.join(ROOT, 'scripts', 'markbank', 'authored', f'{subject}.json')


def exclusions_path(subject):
    return os.path.join(HERE, 'exclusions', f'{subject}.json')


def sitting_cards(subject, year, level='hl'):
    mod = importlib.import_module(f'sl_specs_{subject.replace("-", "_")}')
    spec_list = mod.specs(year)
    if not spec_list:
        raise KeyError(f'no specs for {subject} {year}')
    scheme = not all(isinstance(s, sl_lib.NoScheme) for s in spec_list)
    new = sl_lib.cards(subject, year, spec_list, level, scheme=scheme)
    with open(authored_path(subject), encoding='utf-8') as fh:
        authored = json.load(fh)
    have = {c['id'] for c in authored}
    ids = [c['id'] for c in new]
    dup = [i for i, n in collections.Counter(ids).items() if n > 1]
    if dup:
        raise ValueError(f'{subject} {year}: duplicate new ids {dup}')
    clash = [i for i in ids if i in have]
    if clash:
        raise ValueError(f'{subject} {year}: new ids already live {clash}')
    return authored, new


ADDITIONS = os.path.join(HERE, 'sl_additions.json')


def record_additions(subject, year, ids):
    """Every card this lane adds, by subject and sitting: what
    test/markBankCardPreservation.test.ts holds apart from each deck's frozen
    pre-lane identity (and pins, sitting by sitting, by count and id hash)."""
    data = {}
    if os.path.exists(ADDITIONS):
        with open(ADDITIONS, encoding='utf-8') as fh:
            data = json.load(fh)
    sitting = data.setdefault(subject, {}).setdefault(str(year), [])
    sitting.extend(i for i in ids if i not in sitting)
    sitting.sort()
    data = {k: dict(sorted(v.items())) for k, v in sorted(data.items())}
    with open(ADDITIONS, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write('\n')


def write(subject, year, level='hl'):
    authored, new = sitting_cards(subject, year, level)
    at = 0
    for i, c in enumerate(authored):
        if c['year'] <= year:
            at = i + 1
    out = authored[:at] + new + authored[at:]
    with open(authored_path(subject), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    record_additions(subject, year, [c['id'] for c in new])
    refs = {c['questionRef'] for c in new}
    path = exclusions_path(subject)
    dropped = 0
    if os.path.exists(path):
        with open(path, encoding='utf-8') as fh:
            excl = json.load(fh)
        kept = [e for e in excl if e.get('ref') not in refs]
        dropped = len(excl) - len(kept)
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(kept, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
    print(f'{subject} {year}: {len(new)} card(s) added ({len(authored)} -> {len(out)}); '
          f'{dropped} exclusion(s) answered')


def review(subject, year, level='hl'):
    _authored, new = sitting_cards(subject, year, level)
    for c in new:
        print(f"{c['id']}  [{c['tariffModel']['kind']} {c['totalMarks']}]  {c['questionRef']}")
        print(f"    Q: {c['questionText']}")
        for r in c['rows']:
            mk = r.get('marks')
            print(f"    - {r['kind']} {mk}: {r['verbatim']}")
            for p in r.get('parts') or []:
                print(f"        * {p['marks']}: {p['verbatim']}")
            if r.get('group'):
                g = r['group']
                print(f"        any {g['claimMax']} x {g['perOption']}: {g['options']}")
            if r.get('contextNote'):
                print(f"        note: {r['contextNote']}")
        if c.get('sourceMaterial'):
            print(f"    source pages {c['sourceMaterial']['pages']}")
    print(f'{len(new)} card(s)')


if __name__ == '__main__':
    cmd, subject, year = sys.argv[1], sys.argv[2], int(sys.argv[3])
    {'review': review, 'write': write}[cmd](subject, year)
