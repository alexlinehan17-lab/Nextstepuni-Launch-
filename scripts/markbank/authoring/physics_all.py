#!/usr/bin/env python3
"""Refresh only the reproducible Physics completion layer."""
import json
import os
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
AUTHORED = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'physics.json')
OWNED = os.path.join(
    ROOT, 'scripts', 'markbank', 'authored', 'physics-completion-ids.json')

# Historical authoring waves occasionally emitted a prose-only card and a
# later, source-complete figure card for the same published task.  The deck
# builder correctly keeps the figure-bearing winner; remove the known losers
# here as well so the authored source and the shipped deck have no deliberate
# supersession drops.
SUPERSEDED_IDS = {
    'phys-2021-ol-q6-i',
    'phys-2021-ol-q9-iii',
    'phys-2024-hl-q6-h',
    'phys-2024-ol-q6-c',
    'phys-2025-ol-q10-vii',
    'phys-2025-ol-q10-viii',
    'phys-2021-ol-q9ix-fig',
    'phys-2021-ol-q14d-iii-fig',
    'phys-2025-ol-q6a-fig',
}

proc = subprocess.run(
    [sys.executable, os.path.join(DIR, 'physics_completion.py')],
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
    raise SystemExit('Physics completion generator emitted duplicate ids')
kept, seen_ids = [], set()
for card in existing:
    card_id = card['id']
    if (card_id in owned or card_id in SUPERSEDED_IDS
            or card_id in seen_ids):
        continue
    kept.append(card)
    seen_ids.add(card_id)
collisions = set(fresh_ids) & {card['id'] for card in kept}
if collisions:
    raise SystemExit(
        f'completion ids collide with preserved cards: {sorted(collisions)[:8]}')
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
