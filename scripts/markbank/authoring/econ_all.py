#!/usr/bin/env python3
"""Run every Economics paper script and write the authored file.

    python3 scripts/markbank/authoring/econ_all.py            # to stdout
    python3 scripts/markbank/authoring/econ_all.py --write    # to authored/economics.json

The authored file is therefore DERIVED, not edited: every card in it can be
traced to the slice of the marking scheme its script took it from, and a hand
edit is lost the next time this runs. Home Economics merged each paper by hand
and the merge was the one step nothing checked.

Refuses on a duplicate card id, because two scripts claiming one id is a merge
that would silently drop a paper's worth of work.
"""
import json
import os
import re
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
# scripts/markbank/authoring -> repo root is three levels up, and the paper
# scripts resolve their scheme paths relative to it.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
OUT = os.path.join(ROOT, 'scripts/markbank/authored/economics.json')

scripts = sorted(
    f for f in os.listdir(DIR)
    if re.fullmatch(r'econ_\d{4}_(hl|ol)(_sec[ab])?\.py', f)
)

cards, seen, failed = [], {}, []
for name in scripts:
    proc = subprocess.run([sys.executable, os.path.join(DIR, name)],
                          capture_output=True, text=True, cwd=ROOT)
    if proc.returncode != 0:
        failed.append(f'{name}: {proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "no output"}')
        continue
    if proc.stderr.strip():
        for line in proc.stderr.strip().splitlines():
            print(f'{name}: {line}', file=sys.stderr)
    batch = json.loads(proc.stdout)
    for c in batch:
        if c['id'] in seen:
            failed.append(f"{name}: id {c['id']} already emitted by {seen[c['id']]}")
        seen[c['id']] = name
    cards.extend(batch)
    print(f'{name:<22} {len(batch):>3} cards', file=sys.stderr)

# Two cards asking the same question of the same paper is a duplicate whatever
# their ids say, and the id guard above cannot see it: the second pass writes a
# card from a block of scheme the first pass already used, under a part path one
# numeral out, so both ids are unique and both cards are the same card. Checked
# on the text a student actually reads.
asked = {}
for c in cards:
    k = (c['year'], c['level'], ' '.join(c['questionText'].split()).lower())
    if k in asked:
        failed.append(f"{c['id']} asks the same question as {asked[k]}: {k[2][:70]}")
    asked[k] = c['id']

if failed:
    for f in failed:
        print('REFUSING', f, file=sys.stderr)
    raise SystemExit('economics.json NOT written')

print(f'{"TOTAL":<22} {len(cards):>3} cards from {len(scripts)} script(s)', file=sys.stderr)
if '--write' in sys.argv:
    with open(OUT, 'w') as fh:
        json.dump(cards, fh, ensure_ascii=False, indent=1)
    print(f'wrote {OUT}', file=sys.stderr)
else:
    print(json.dumps(cards, ensure_ascii=False, indent=1))
