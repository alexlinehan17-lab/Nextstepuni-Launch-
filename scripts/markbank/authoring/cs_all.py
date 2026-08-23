#!/usr/bin/env python3
"""Run every Construction Studies paper script and write the authored file.

    python3 scripts/markbank/authoring/cs_all.py            # to stdout
    python3 scripts/markbank/authoring/cs_all.py --write    # to authored/...

Modelled on econ_all.py, and refuses for the same two reasons: a duplicate id
is a merge that would silently drop a paper's worth of work, and two cards
asking the same question of the same paper is a duplicate whatever their ids
say. The second check is the one that matters here, because a part can be
reached under more than one group and the ids would differ.
"""
import json
import os
import re
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
OUT = os.path.join(ROOT, 'scripts/markbank/authored/construction-studies.json')

scripts = sorted(f for f in os.listdir(DIR) if re.fullmatch(r'cs_\d{4}_(hl|ol)\.py', f))

cards, seen, failed = [], {}, []
for name in scripts:
    proc = subprocess.run([sys.executable, os.path.join(DIR, name)],
                          capture_output=True, text=True, cwd=ROOT)
    if proc.returncode != 0:
        tail = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else 'no output'
        failed.append(f'{name}: {tail}')
        continue
    for line in proc.stderr.strip().splitlines():
        if line:
            print(f'{name}: {line}', file=sys.stderr)
    batch = json.loads(proc.stdout)
    for c in batch:
        if c['id'] in seen:
            failed.append(f"{name}: id {c['id']} already emitted by {seen[c['id']]}")
        seen[c['id']] = name
    cards.extend(batch)
    print(f'{name:<20} {len(batch):>3} cards', file=sys.stderr)

asked = {}
for c in cards:
    k = (c['year'], c['level'], ' '.join(c['questionText'].split()).lower())
    if k in asked:
        failed.append(f"{c['id']} asks the same question as {asked[k]}: {k[2][:70]}")
    asked[k] = c['id']

if failed:
    for f in failed:
        print('REFUSING', f, file=sys.stderr)
    raise SystemExit('construction-studies.json NOT written')

print(f'{"TOTAL":<20} {len(cards):>3} cards from {len(scripts)} script(s)', file=sys.stderr)
if '--write' in sys.argv:
    with open(OUT, 'w') as fh:
        json.dump(cards, fh, ensure_ascii=False, indent=1)
    print(f'wrote {OUT}', file=sys.stderr)
else:
    print(json.dumps(cards, ensure_ascii=False, indent=1))
