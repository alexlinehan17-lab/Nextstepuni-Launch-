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
    if (year, level) == (2022, 'ol'):
        # Independent53-page sweep. Adjusted175written+100listening;
        # all practice alternatives305. Each complete choice pool is one task.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2022-ol-000-paper.pdf':'a706a1a3b4a1898ebe170609a5b699388178b8dd45461a60a546e4381b8882cd',
            'papers/2022-ol-A00-paper.pdf':'ed8dc696911237310a16ce4e7ed7bc2c16381aecf33ecc78fc976469119796fd',
            'schemes/2022-ol.pdf':'184ff292e15bf7702b94bdb4e7626d7bfb538bfb948bed4c85ae4efe01df7399',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys=[('IR1',q,None,None) for q in range(1,7)]
        keys += [('IR2',1,None,r) for r in ('i','ii','iii','iv')]
        keys += [('CD',q,None,r) for q,romans in [(1,(None,)),(2,('i','ii')),(3,(None,)),(4,('i','ii')),(5,(None,)),(6,(None,))] for r in romans]
        keys += [(unit,None,None,None) for unit in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys)==24
        keys += [(unit,q,None,r) for unit in ('L1','L2') for q,r in [(1,None),(2,None),(3,'i'),(3,'ii'),(4,None)]]
        keys += [('L3',q,None,None) for q in (1,2,3,4)]
        keys += [('L4',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None)]]
        assert len(keys)==len(set(keys))==42
        return set(keys)
    if (year, level) == (2022, 'hl'):
        # Independent51-page sweep (16written+8aural+27scheme). Adjusted
        # choice:170written+80listening; all practice alternatives320.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2022-hl-000-paper.pdf': '73b129f223b597be6e096ded274e54b6fbc43260ee0f0b4c356b9477e956b273',
            'papers/2022-hl-A00-paper.pdf': '86914ac9598814d8c89db30655a24271c4d5f97ddbfe1d0e976938d495f7bb6d',
            'schemes/2022-hl.pdf': '7f539dcb7b70c18e30b1047e463426bd2715926ddfe16a6daa0a93b995907071',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('C1',q,None,r) for q,romans in [(1,('i','ii','iii')),(2,('i','ii')),(3,('i','ii','iii')),(4,(None,))] for r in romans]
        keys += [('C2',q,None,None) for q in (1,2,3,4)]
        keys += [(unit,None,None,r) for unit in ('LA1','LA2') for r in ('i','ii')]
        keys += [(unit,q,None,None) for unit,q in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys)==21
        keys += [(unit,q,None,r) for unit in ('L1','L2') for q,r in [(1,'i'),(1,'ii'),(2,'i'),(2,'ii'),(3,None),(4,None)]]
        keys += [('L3',q,None,r) for q,r in [(1,None),(2,None),(3,None),(4,'i'),(4,'ii')]]
        keys += [('L4',q,None,r) for q in (1,2,3) for r in ('i','ii')]
        assert len(keys)==len(set(keys))==44
        return set(keys)
    if (year, level) == (2023, 'ol'):
        # Independent53-page visual census:20written+8aural+25scheme.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2023-ol-000-paper.pdf': '28b5a7cf5e15f3c2da6f6938f3b2f13abd888eab5dabd16f28b6966fb1e0e4ce',
            'papers/2023-ol-A00-paper.pdf': 'a5ecc7cb74169bcd00d5bc69fe2ce083c96019f449d31515ada7041d2a298b32',
            'schemes/2023-ol.pdf': 'da5064b6da1f3906e010bf0ae0610add8100a8b00964149bb6d2ca97593e1b5b',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [(unit,q,None,None) for unit in ('IR1','IR2') for q in range(1,8)]
        keys += [('CD',q,None,r) for q,romans in [(1,('i','ii')),(2,('i','ii')),(3,('i','ii','iii')),(4,('i','ii'))] for r in romans]
        keys += [(unit,None,None,None) for unit in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys) == 29
        keys += [(unit,q,None,r) for unit in ('L1','L2') for q,r in [(1,'i'),(1,'ii'),(2,None),(3,'i'),(3,'ii')]]
        keys += [('L3',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None)]]
        keys += [('L4',q,None,None) for q in (1,2,3,4)]
        assert len(keys) == len(set(keys)) == 47
        return set(keys)
    if (year, level) == (2024, 'ol'):
        # All20written+8aural+25scheme pages independently inspected.
        # CD booklet3(iii)/(iv) are misnumbered(iv)/(v) in the scheme.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2024-ol-000-paper.pdf': '7ca7754d00496ebdc9ce022665c6eba8f7378bf7325d02d46ceab168f3761970',
            'papers/2024-ol-A00-paper.pdf': '9384428ab46b24725f66f30afafdfb22048b4507de24e6307eb2df4fe1ea547c',
            'schemes/2024-ol.pdf': 'ecba77fed2ef00afe4503bb1d4ed4b5ea0c5803a53727338592764406fbee44a',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('IR1',q,None,r) for q,romans in [(1,('i','ii')),(2,('i','ii')),(3,('i','ii','iii')),(4,(None,))] for r in romans]
        keys += [('IR2',q,None,None) for q in range(1,8)]
        keys += [('CD',q,None,r) for q,romans in [(1,('i','ii')),(2,('i','ii','iii')),(3,('i','ii','iii','iv'))] for r in romans]
        keys += [(unit,None,None,None) for unit in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys) == 30
        keys += [(unit,q,None,r) for unit in ('L1','L2','L3') for q,r in [(1,'i'),(1,'ii'),(2,None),(3,'i'),(3,'ii')]]
        keys += [('L4',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,'i'),(3,'ii')]]
        assert len(keys) == len(set(keys)) == 50
        return set(keys)
    if (year, level) == (2024, 'hl'):
        # Independent original-PDF sweep:16written+8aural+28scheme pages.
        # Twelve comprehension asks; four whole summaries; each complete
        # writing choice pool and discourse exercise remains one task.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2024-hl-000-paper.pdf': 'c154f981d7a257665eb0a71e24e2246dc5e0e14431297819ff91017da79fc1c7',
            'papers/2024-hl-A00-paper.pdf': '98df8494df03f7ff48a5438d5202036813c4d9a7525d102ca75c9201c95a54c9',
            'schemes/2024-hl.pdf': '3fd5f06ee6dbc78e1ef53bcaa1e1e6f9a6d822c6ee898a69f16ec34cf0aac999',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('C1', q, None, r) for q, romans in [(1, ('i','ii')), (2, ('i','ii','iii','iv')), (3, ('i','ii','iii','iv')), (4, ('i','ii'))] for r in romans]
        keys += [('C2', q, None, None) for q in (1,2,3,4)]
        keys += [(unit, None, None, roman) for unit in ('LA1','LA2') for roman in ('i','ii')]
        keys += [(unit, question, None, None) for unit, question in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys) == 24
        keys += [(unit,q,None,r) for unit in ('L1','L2','L3','L4') for q in (1,2,3) for r in ('i','ii')]
        assert len(keys) == len(set(keys)) == 48
        return set(keys)
    if (year, level) == (2025, 'hl'):
        # Independent visual review: all16 written,8 aural,27 scheme pages.
        # Four complete summaries include their discretionary component;
        # five essay topics and six guided prompts remain two choice pools.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2025-hl-000-paper.pdf': '671650c672d92ab191f615700de4dfd7077835d86223a2e976a8818809c8d97f',
            'papers/2025-hl-A00-paper.pdf': 'edcc2149eddeababbeb62a5e471c22de654b4fb74bbf671b2e12c0e5abb921fe',
            'schemes/2025-hl.pdf': '3c74de1d1d5d35a4e0e9ada2b5e7754446722444003f480a2bd876c90c27a52b',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('C1', q, None, r) for q, romans in [(1, ('i','ii','iii')), (2, ('i','ii')), (3, ('i','ii','iii')), (4, (None,))] for r in romans]
        keys += [('C2', q, None, None) for q in (1,2,3,4)]
        keys += [(unit, None, None, roman) for unit in ('LA1','LA2') for roman in ('i','ii')]
        keys += [(unit, question, None, None) for unit, question in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys) == 21
        for unit in ('L1','L3'):
            keys += [(unit,q,None,r) for q in (1,2,3) for r in ('i','ii')]
        keys += [('L2',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,'i'),(3,'ii')]]
        keys += [('L4',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,'i'),(2,'ii'),(3,None)]]
        assert len(keys) == len(set(keys)) == 43
        return set(keys)
    if (year, level) == (2025, 'ol'):
        # Independent visual sweep:20written+8aural+26scheme pages. The
        # event table and each complete alternative pool are single tasks.
        root = Path(__file__).resolve().parents[3] / 'examiner-reports/russian'
        for relative, digest in {
            'papers/2025-ol-000-paper.pdf': 'a32ab3a53c7d4b97e511656c01384558307700f6d4874dc34337f067c988acc4',
            'papers/2025-ol-A00-paper.pdf': '5621c29b27d2a9b226e8f239a058e24cebe90aa904f18d6bb4fcab31f7454a77',
            'schemes/2025-ol.pdf': '2da580d0bece12bce51802feedb9117cc96d0a28ba5a334d61cd93055f3104d3',
        }.items():
            assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
        keys = [('IR1', q, None, r) for q in (1,2,3,4) for r in ('i','ii')]
        keys += [('IR2',1,None,r) for r in ('i','ii')]
        keys += [('IR2',q,None,None) for q in (2,3,4,5)]
        keys += [('CD',q,None,r) for q in (1,2) for r in ('i','ii','iii')]
        keys += [('CD',3,None,r) for r in ('i','ii')]
        keys += [('CD',4,None,r) for r in ('i','ii','iii','iv')]
        keys += [(unit,None,None,None) for unit in ('LA1','LA2','MM','SD','SA','EW')]
        assert len(keys) == 32
        keys += [(unit,q,None,r) for unit in ('L1','L2','L3','L4') for q in (1,2,3) for r in ('i','ii')]
        assert len(keys) == len(set(keys)) == 56
        return set(keys)
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
