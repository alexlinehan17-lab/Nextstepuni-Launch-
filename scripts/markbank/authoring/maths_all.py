#!/usr/bin/env python3
"""Run every Mathematics paper script and write the authored file.

    python3 scripts/markbank/authoring/maths_all.py --write

Refuses on a duplicate id and on two cards asking the same question of the same
paper, for the reasons econ_all.py gives.
"""
import json
import os
import re
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
OUT = os.path.join(ROOT, 'scripts/markbank/authored/maths.json')

scripts = sorted(f for f in os.listdir(DIR) if re.fullmatch(r'maths_\d{4}_(hl|ol)\.py', f))
cards, seen, failed = [], {}, []
for name in scripts:
    proc = subprocess.run([sys.executable, os.path.join(DIR, name)],
                          capture_output=True, text=True, cwd=ROOT)
    if proc.returncode != 0:
        tail = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else 'no output'
        failed.append(f'{name}: {tail}')
        continue
    batch = json.loads(proc.stdout)
    for c in batch:
        if c['id'] in seen:
            failed.append(f"{name}: id {c['id']} already emitted by {seen[c['id']]}")
        seen[c['id']] = name
    cards.extend(batch)
    print(f'{name:<22} {len(batch):>3} cards', file=sys.stderr)

asked = {}
for c in cards:
    k = (c['year'], c['level'], ' '.join(c['questionText'].split()).lower())
    if k in asked:
        failed.append(f"{c['id']} asks the same question as {asked[k]}: {k[2][:60]}")
    asked[k] = c['id']

if failed:
    for f in failed:
        print('REFUSING', f, file=sys.stderr)
    raise SystemExit('maths.json NOT written')
print(f'{"TOTAL":<22} {len(cards):>3} cards from {len(scripts)} script(s)', file=sys.stderr)
if '--write' in sys.argv:
    with open(OUT, 'w') as fh:
        json.dump(cards, fh, ensure_ascii=False, indent=1)
    print(f'wrote {OUT}', file=sys.stderr)
else:
    print(json.dumps(cards, ensure_ascii=False, indent=1))
