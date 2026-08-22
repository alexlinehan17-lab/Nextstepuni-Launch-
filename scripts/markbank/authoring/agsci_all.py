#!/usr/bin/env python3
"""Merge the script-authored Agricultural Science cards into the authored file.

    python3 scripts/markbank/authoring/agsci_all.py            # report only
    python3 scripts/markbank/authoring/agsci_all.py --write    # merge and write

The deck's original 790 cards were written by hand and have no script behind
them, so this cannot regenerate the file the way econ_all.py does. It merges
instead, and the sidecar agricultural-science-script-ids.json records which ids
the scripts own. On each run those are dropped and re-emitted, so running twice
changes nothing and a card removed from a script disappears from the deck.

An id that collides with a hand-authored card is refused rather than merged: a
script quietly replacing hand-written work is the one failure here that would
leave no trace.
"""
import json
import os
import re
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
AUTHORED = os.path.join(ROOT, 'scripts/markbank/authored/agricultural-science.json')
OWNED = os.path.join(ROOT, 'scripts/markbank/authored/agricultural-science-script-ids.json')

scripts = sorted(f for f in os.listdir(DIR)
                 if re.fullmatch(r'agsci_\d{4}_(hl|ol)\.py', f))

existing = json.load(open(AUTHORED))
owned = set(json.load(open(OWNED))) if os.path.exists(OWNED) else set()

fresh, seen, failed = [], {}, []
for name in scripts:
    proc = subprocess.run([sys.executable, os.path.join(DIR, name)],
                          capture_output=True, text=True, cwd=ROOT)
    if proc.returncode != 0:
        tail = proc.stderr.strip().splitlines()
        failed.append(f'{name}: {tail[-1] if tail else "no output"}')
        continue
    for line in proc.stderr.strip().splitlines():
        if line.strip():
            print(f'{name}: {line}', file=sys.stderr)
    batch = json.loads(proc.stdout)
    for c in batch:
        if c['id'] in seen:
            failed.append(f"{name}: id {c['id']} already emitted by {seen[c['id']]}")
        seen[c['id']] = name
    fresh.extend(batch)
    print(f'{name:<22} {len(batch):>3} cards', file=sys.stderr)

kept = [c for c in existing if c['id'] not in owned]
hand = {c['id'] for c in kept}
for c in fresh:
    if c['id'] in hand:
        failed.append(f"{c['id']} collides with a hand-authored card — "
                      f"rename it or adopt the existing card into a script")

merged = kept + fresh

# Two cards asking the same question of the same paper is a duplicate whatever
# their ids say. Checked on the text a student actually reads — question and
# stem together, because these papers ask 'Explain the underlined term.'
# repeatedly and it is the stem that carries which term is underlined.
asked = {}
for c in merged:
    k = (c['year'], c['level'],
         ' '.join((c['questionText'] + ' ' + (c.get('stem') or '')).split()).lower())
    if k in asked:
        failed.append(f"{c['id']} asks the same question as {asked[k]}: {k[2][:70]}")
    asked[k] = c['id']

if failed:
    for f in failed:
        print('REFUSING', f, file=sys.stderr)
    raise SystemExit('agricultural-science.json NOT written')

print(f'\n{len(kept)} hand-authored + {len(fresh)} script-authored = {len(merged)}',
      file=sys.stderr)
if '--write' in sys.argv:
    with open(AUTHORED, 'w') as fh:
        json.dump(merged, fh, ensure_ascii=False, indent=1)
    with open(OWNED, 'w') as fh:
        json.dump(sorted(c['id'] for c in fresh), fh, indent=1)
    print(f'wrote {AUTHORED}', file=sys.stderr)
