"""Independent physical-paper Japanese task census, only for swept sittings.

This input contains addresses, page roles and printed tariffs. It does not read
authored cards, so an authoring omission cannot shrink the required task set.
Unreviewed sittings continue through the existing parser, including its flags.
"""
import hashlib
import json
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[3]


def reviewed_census(year, level):
    path = Path(__file__).parent / 'reviews' / f'japanese-{year}-{level}-census.json'
    if not path.exists():
        return None
    review = json.loads(path.read_text())
    assert (review['subjectId'], review['year'], review['level']) == ('japanese', year, level)
    for source in review['sources']:
        original = ROOT / source['path']
        assert hashlib.sha256(original.read_bytes()).hexdigest() == source['sha256'], f'{path}: source changed'
        page_count = len(fitz.open(original))
        roles = review['pageRoles'][source['component']]
        assert set(roles) == {str(i) for i in range(1, page_count + 1)}, f'{path}: source page not reviewed'
        assert all(roles.values()), f'{path}: missing page disposition'
    tasks = review['tasks']
    keys = {tuple(task['key']) for task in tasks}
    assert len(keys) == len(tasks), f'{path}: duplicate task'
    for task in tasks:
        assert isinstance(task['marks'], int) and task['marks'] > 0
        assert task['paperPages'] and task['schemePages']
        assert all(str(p) in review['pageRoles'][task['component']] for p in task['paperPages'])
        assert all(str(p) in review['pageRoles']['scheme'] for p in task['schemePages'])
    totals = {
        'reading': sum(t['marks'] for t in tasks if t['key'][0][0] in '123'),
        'writing': sum(t['marks'] for t in tasks if t['key'][0][0] in '45'),
        'listening': sum(t['marks'] for t in tasks if t['component'] == 'aural'),
        'total': sum(t['marks'] for t in tasks),
    }
    if (year, level) == (2010, 'hl'):
        # This original paper explicitly has SIX questions: Q1–3 reading100,
        # Q4 grammar20, Q5–6 writing100, plus the separate listening80 booklet.
        # Later sittings' five-question checksum remains exactly as before.
        totals['grammar'] = sum(t['marks'] for t in tasks if t['key'][0][0] == '4')
        totals['writing'] = sum(t['marks'] for t in tasks if t['key'][0][0] in '56')
    assert totals == review['checksums'], f'{path}: printed totals do not reconcile'
    return review
