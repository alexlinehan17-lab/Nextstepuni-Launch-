#!/usr/bin/env python3
"""Refresh only the reproducible Home Economics completion layer."""
import json
import os
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
AUTHORED = os.path.join(ROOT, 'scripts/markbank/authored/home-economics.json')
OWNED = os.path.join(
    ROOT, 'scripts/markbank/authored/home-economics-completion-ids.json')
CORRECTIONS = os.path.join(ROOT, 'scripts/markbank/card-corrections.json')

proc = subprocess.run(
    [sys.executable, os.path.join(DIR, 'he_completion.py')],
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
    raise SystemExit('completion generator emitted duplicate ids')
fresh_id_set = set(fresh_ids)
corrections = json.load(open(CORRECTIONS, encoding='utf-8')).get(
    'home-economics', {})
retired = {cid for cid, correction in corrections.items()
           if correction.get('drop')}
# Keep an old completion card when the shared correction ledger explicitly
# withdraws it.  The raw id must survive long enough for build-deck to emit the
# progress alias to its replacement; silently deleting it here would lose
# students' saved review history even though the new boundary is correct.
kept = [card for card in existing
        if card['id'] not in owned
        or (card['id'] in retired and card['id'] not in fresh_id_set)]

collisions = set(fresh_ids) & {card['id'] for card in kept}
if collisions:
    raise SystemExit(f'completion ids collide with preserved cards: {sorted(collisions)[:5]}')

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
