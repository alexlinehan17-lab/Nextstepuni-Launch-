"""Independent visual task census. Never derives a denominator from cards.

2026HL: all16 written pages,8 aural pages and30 scheme pages inspected.
Printed task count46;320marks across all practice alternatives; selecting one
of each10-mark language-awareness pair gives the cover's220+80=300marks.
GWpp13–14 has six prompts under one40-mark grid. Its numbered genres are not
separate questions; the legacy reader stops before the sixth prompt onp14.
"""
import hashlib
from pathlib import Path


def reviewed_keys(year, level):
    if year != 2026 or level not in ('hl', 'ol'):
        return None
    root = Path(__file__).resolve().parents[3]
    sources = {
        'papers/2026-hl-000-paper.pdf': 'e9fd3cede429b88a1f530fe18a494af3e2cdeb98ba218c932c3d4a72fe147992',
        'papers/2026-hl-A00-paper.pdf': 'c0c4ed2e47c5476de8d68179f90acf383c79d2648e77b7bc34589d32caeccb6d',
        'schemes/2026-hl.pdf': 'e56810faf2cb2b34e30216c07b4ff771d1cc6f99b91fb6fcf1d47d045d8265be',
    } if level == 'hl' else {
        'papers/2026-ol-000-paper.pdf': '118ab2d6814246c2a9f071945a888fd1ec7be42a46d2d9cf996a25703103f070',
        'papers/2026-ol-A00-paper.pdf': 'd6a8bb9334a155937d15c2287001e5e5e9bd0606993df7f449185cb3837df966',
        'schemes/2026-ol.pdf': '7fb47439b0e1322e592da32dc160f2f164a84c8ac4810d02b18e7a17d3d89047',
    }
    for relative, digest in sources.items():
        path = root / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
    keys = []
    if level == 'ol':
        # Original paper pp3–4: eight asks; pp7–8: seven asks, including one
        # four-heading table. pp13–14: ten comprehension asks. Each complete
        # LA, matching, dialogue or writing choice pool is one task.
        keys += [('IR1', q, None, r) for q in (1, 2, 3, 4) for r in ('i', 'ii')]
        keys += [('IR2', q, None, None) for q in (1, 2, 3, 4, 5, 6, 7)]
        keys += [('CD', q, None, r) for q in (1, 2) for r in ('i', 'ii')]
        keys += [('CD', q, None, r) for q in (3, 4) for r in ('i', 'ii', 'iii')]
        keys += [(unit, None, None, None) for unit in ('LA1', 'LA2', 'MM', 'SD', 'SA', 'EW')]
        assert len(keys) == 31
        for unit in ('L1', 'L3'):
            keys += [(unit, q, None, r) for q in (1, 2, 3) for r in ('i', 'ii')]
        keys += [('L1', 1, None, 'iii'), ('L3', 2, None, 'iii')]
        keys += [('L2', q, None, r) for q in (1, 2) for r in ('i', 'ii')]
        keys += [('L2', 3, None, None)]
        keys += [('L4', q, None, r) for q in (1, 2, 3) for r in ('i', 'ii')]
        assert len(keys) == len(set(keys)) == 56
        return set(keys)
    for question, romans in [(1, ('i','ii','iii')), (2, ('i','ii')), (3, ('i','ii')), (4, ('i','ii','iii'))]:
        keys += [('C1', question, None, roman) for roman in romans]
    keys += [('C2', q, None, None) for q in (1,2,3,4)]
    keys += [(unit, None, None, roman) for unit in ('LA1','LA2') for roman in ('i','ii')]
    keys += [(unit, question, None, None) for unit, question in [('SD',3),('GR',1),('SE',2),('GW',3)]]
    for unit in ('L1','L3','L4'):
        keys += [(unit,q,None,r) for q in (1,2,3) for r in ('i','ii')]
    keys += [('L2',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,'i'),(2,'ii'),(2,'iii'),(3,None)]]
    assert len(keys) == len(set(keys)) == 46
    return set(keys)
