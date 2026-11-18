"""Prove the boxed-heading strip changed nothing but the pinned headings (run against the commit before the fix).
usage: heading_strip_audit.py BASE
Every Irish card file and card id is unchanged; every card is byte-identical except guidance strings where
strip_text(old) == new with at least one exact heading removed; Atlas, answer maps and topic tags are unchanged."""
import json, subprocess, sys, os
from collections import Counter
from pathlib import Path
os.chdir(Path(__file__).resolve().parents[4])
sys.path.insert(0, 'scripts/markbank/authoring')
from irish_furniture import strip_text
base = sys.argv[1]
DIR = 'components/MarkBank/cards/irish'
old_files = sorted(p for p in subprocess.check_output(['git', 'ls-tree', '--name-only', base, DIR + '/'], text=True).split() if p.endswith('.json'))
new_files = sorted(str(p) for p in Path(DIR).glob('*.json'))
assert old_files == new_files, (set(old_files) ^ set(new_files))
same = changed = removed = 0
per_paper = Counter()
for path in old_files:
    old = json.loads(subprocess.check_output(['git', 'show', f'{base}:{path}']))
    new = json.load(open(path))
    assert {k: v for k, v in old.items() if k != 'cards'} == {k: v for k, v in new.items() if k != 'cards'}, path
    assert [c['id'] for c in old['cards']] == [c['id'] for c in new['cards']], path
    for a, b in zip(old['cards'], new['cards']):
        if a == b:
            same += 1
            continue
        assert {k: v for k, v in a.items() if k != 'criteria'} == {k: v for k, v in b.items() if k != 'criteria'}, a['id']
        assert len(a['criteria']) == len(b['criteria']), a['id']
        n_card = 0
        for ca, cb in zip(a['criteria'], b['criteria']):
            assert {k: v for k, v in ca.items() if k != 'guidance'} == {k: v for k, v in cb.items() if k != 'guidance'}, (a['id'], ca['id'])
            assert len(ca['guidance']) == len(cb['guidance']), (a['id'], ca['id'])
            for ga, gb in zip(ca['guidance'], cb['guidance']):
                stripped, n = strip_text(ga)
                assert stripped == gb, (a['id'], ca['id'])
                n_card += n
        assert n_card > 0, a['id']
        changed += 1
        removed += n_card
        per_paper[(a['year'], a['level'], a['paper'])] += n_card
outputs = ['data/examTopics', 'data/paperTrail', 'public/paper-anchors', 'public/paper-answers', 'scripts/paper-trail', 'scripts/markbank/authored']
assert subprocess.run(['git', 'diff', '--quiet', base, '--'] + outputs).returncode == 0, 'non-card Irish outputs changed'
print(f'PASS: {same} cards byte-identical; {changed} cards differ only by {removed} exact pinned headings removed from guidance; '
      f'Atlas, answer maps, topic tags and review records unchanged. Per paper: ' + ', '.join(f'{y} {l} P{p} {n}' for (y, l, p), n in sorted(per_paper.items())))
