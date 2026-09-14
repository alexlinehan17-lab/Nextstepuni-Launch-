#!/usr/bin/env python3
"""Refresh only the reproducible Business completion layer."""
import json
import os
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
AUTHORED = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'business.json')
OWNED = os.path.join(
    ROOT, 'scripts', 'markbank', 'authored', 'business-completion-ids.json')

proc = subprocess.run(
    [sys.executable, os.path.join(DIR, 'bus_completion.py')],
    cwd=ROOT, text=True, capture_output=True)
if proc.stderr:
    print(proc.stderr, file=sys.stderr, end='')
if proc.returncode:
    raise SystemExit(proc.returncode)
fresh = json.loads(proc.stdout)
existing = json.load(open(AUTHORED, encoding='utf-8'))
owned = set(json.load(open(OWNED))) if os.path.exists(OWNED) else set()
fresh_ids = [card['id'] for card in fresh]
if len(fresh_ids) != len(set(fresh_ids)):
    raise SystemExit('Business completion generator emitted duplicate ids')
kept = [card for card in existing if card['id'] not in owned]
collisions = set(fresh_ids) & {card['id'] for card in kept}
if collisions:
    raise SystemExit(f'completion ids collide with preserved cards: {sorted(collisions)[:8]}')
merged = kept + fresh
print(f'{len(kept)} preserved + {len(fresh)} completion = {len(merged)}',
      file=sys.stderr)
if '--write' in sys.argv:
    with open(AUTHORED, 'w', encoding='utf-8') as fh:
        json.dump(merged, fh, ensure_ascii=False, indent=1)
    with open(OWNED, 'w', encoding='utf-8') as fh:
        json.dump(sorted(fresh_ids), fh, indent=1)
    print(f'wrote {AUTHORED}', file=sys.stderr)
else:
    print('report only; pass --write to update authored files', file=sys.stderr)
