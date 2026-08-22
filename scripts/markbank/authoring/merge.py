#!/usr/bin/env python3
"""Merge script-authored cards into a subject's authored file.

    python3 scripts/markbank/authoring/merge.py biology            # report only
    python3 scripts/markbank/authoring/merge.py biology --write    # merge and write

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
SUBJECT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else None
if not SUBJECT:
    raise SystemExit('name a subject: merge.py <subject> [--write]')
PREFIX = {'agricultural-science': 'agsci', 'biology': 'bio', 'business': 'bus',
          'chemistry': 'chem', 'economics': 'econ', 'home-economics': 'hem',
          'physics': 'phys'}[SUBJECT]
AUTHORED = os.path.join(ROOT, f'scripts/markbank/authored/{SUBJECT}.json')
OWNED = os.path.join(ROOT, f'scripts/markbank/authored/{SUBJECT}-script-ids.json')

scripts = sorted(f for f in os.listdir(DIR)
                 if re.fullmatch(rf'{PREFIX}_\d{{4}}_(hl|ol)(_\w+)?\.py', f))

# Ids a script deliberately takes over from the hand-authored set, because it
# writes a better card for the same part — usually the same question now
# carrying the figure it refers to. Listed here rather than inferred, so a
# script cannot quietly replace hand-written work: that is the one failure in
# this merge that would leave no trace. Removing an id from this list puts the
# hand-authored card back.
ADOPTED = set(json.load(open(os.path.join(
    ROOT, 'scripts/markbank/authored/adopted-ids.json')))) if os.path.exists(
    os.path.join(ROOT, 'scripts/markbank/authored/adopted-ids.json')) else set()

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
    if c['id'] in hand and c['id'] not in ADOPTED:
        failed.append(f"{c['id']} collides with a hand-authored card — "
                      f"rename it, or add it to ADOPTED to mean the takeover")
adopted = {c['id'] for c in fresh} & ADOPTED
if adopted:
    kept = [c for c in kept if c['id'] not in adopted]
    for i in sorted(adopted):
        print(f'  adopting {i} from the hand-authored set', file=sys.stderr)

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
        # A '-fig' twin is deliberate: the same question carded twice, once
        # plain and once carrying its figure, and the build supersedes one with
        # the other. Not a duplicate to refuse.
        pair = {c['id'], asked[k]}
        twin = any(a + '-fig' == b for a in pair for b in pair)
        if not twin:
            failed.append(f"{c['id']} asks the same question as {asked[k]}: {k[2][:70]}")
    asked[k] = c['id']

if failed:
    for f in failed:
        print('REFUSING', f, file=sys.stderr)
    raise SystemExit(f'{SUBJECT}.json NOT written')

print(f'\n{len(kept)} hand-authored + {len(fresh)} script-authored = {len(merged)}',
      file=sys.stderr)
if '--write' in sys.argv:
    with open(AUTHORED, 'w') as fh:
        json.dump(merged, fh, ensure_ascii=False, indent=1)
    with open(OWNED, 'w') as fh:
        json.dump(sorted(c['id'] for c in fresh), fh, indent=1)
    print(f'wrote {AUTHORED}', file=sys.stderr)
