#!/usr/bin/env python3
"""Independent 52-page visual inventory, before 2025 Higher card authoring.

This counts complete printed tasks and their published tariffs. It does not
read any card file or use the legacy marker parser as its denominator.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2025-hl-000-paper.pdf', 'ee65b1a62840d44091078fcfa7838c93ebe561dc70bc5729d2fd64cd829f1ac2'),
    ('aural', 'examiner-reports/japanese/papers/2025-hl-A00-paper.pdf', '978fe00bd2976087f3e0ddede26c9c346b94af6a6fe430b466e6075d18dc16c8'),
    ('scheme', 'examiner-reports/japanese/schemes/2025-hl.pdf', 'da1b0a337677d064eae660437ef2f6cf6ac9da574b03426de0d63f75cddf5454'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, letter=None, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, letter, roman], 'marks': marks,
                  'component': component, 'paperPages': [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058ALP{"A00" if component == "aural" else "000"}BV.pdf', 'questionNumber': str(atlas)}})


def build():
    task('1A', 1, 5, 3, [7], 1)
    for q in [2, 3]:
        for letter in 'ab':
            task('1A', q, 2, 3, [7], q, letter)
    for q in [4, 5, 6]:
        task('1A', q, 2, 3, [7], q)
    task('1A', 7, 5, 3, [7], 7)
    for q in [1, 2]:
        for letter in 'ab':
            task('1B', q, 2, 4, [8], q + 7, letter)
    task('1B', 3, 2, 4, [8], 10)
    for letter in 'abcd':
        task('2A', 1, 2, 7, [8], 11, letter)
    for letter, roman, marks in [('a', None, 3), ('b', None, 2), ('c', 'i', 3), ('c', 'ii', 3), ('d', None, 3)]:
        task('2A', 2, marks, 7, [9], 12, letter, roman)
    task('2A', 3, 4, 7, [9], 13)
    for section, page, schemes, anchors in [('2B', 8, [9, 10], [14, 15]), ('2C', 9, [10, 10], [16, 17])]:
        for q in [1, 2]:
            task(section, q, 5, page, [schemes[q - 1]], anchors[q - 1])
    for q, marks in enumerate([2, 3, 3, 3, 3], 1):
        task('3A', q, marks, 11, [11], q + 17)
    for q, marks in enumerate([1, 2, 2, 1], 1):
        task('3B', q, marks, 11, [11], q + 22)
    task('3C', None, 10, 12, [12], 27)
    task('3D', None, 10, 12, [12], 28)
    task('4', None, 40, 14, [13, 14], 29)
    task('5', None, 60, 16, [15, 16], 30)
    for q in [1, 2, 3]:
        task('LA', q, 7, 2, [3], q)
    for q, entries in [(1, [('a', 1), ('b', 2), ('c', 3), ('d', 2), ('e', 4), ('f', 2)]), (2, [('a', 2), ('b', 2), ('c', 2)])]:
        for letter, marks in entries:
            task('LB', q, marks, 3, [4], q + 7, letter)
    for q, marks in enumerate([3, 2, 2, 3, 3, 3, 3], 1):
        task('LC', q, marks, 4, [5], q + 9 if q <= 3 else q)
    for letter in 'ab':
        task('LD', 1, 2, 5, [6], 13, letter)
    for letter, roman, marks in [('a', 'i', 2), ('a', 'ii', 2), ('b', 'i', 3), ('b', 'ii', 2)]:
        task('LD', 2, marks, 5, [6], 14, letter, roman)
    for letter, marks in [('a', 3), ('b', 2), ('c', 2)]:
        task('LD', 3, marks, 5, [6], 15, letter)
    assert len(TASKS) == 69, len(TASKS)
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}, totals
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2025, 'level': 'hl', 'reviewedAt': '2026-11-09',
            'method': 'Independent visual sweep of all 20 written, 8 aural and 24 scheme pages before authoring. Printed complete tasks, choice pools, separately priced responses and published tariffs counted directly from the originals.',
            'sources': sources,
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 21)), ['cover', 'Q1A original Don Quijote website', 'Q1A tasks, matching and mascot table', 'Q1B customer reviews and tasks', 'explicit blank', 'Q2 EXPO25 source article and vocabulary', 'Q2A Japanese/English comprehension and translation', 'Q2B two any-five kanji pools', 'Q2C two any-five grammar pools', 'Q3 Ronan blog source and vocabulary', 'Q3A English and Q3B Japanese responses', 'Q3C any-five paired kanji and Q3D any-ten particle blanks', 'explicit blank', 'Q4 choose one of three writing prompts', 'writing answer grid', 'Q5 choose four of eight headings', 'writing answer grid', 'writing answer grid', 'writing answer grid', 'acknowledgements'])),
                'aural': dict(zip(map(str, range(1, 9)), ['cover and English-answer instructions', 'Part A three required seven-mark profile rows', 'Part B hotel and weather tasks including phone grid', 'Part C interview tasks and ingredient table', 'Part D conversations and tasks', 'explicit blank', 'explicit blank', 'back cover with explicit blank'])),
                'scheme': dict(zip(map(str, range(1, 25)), ['cover', 'general examiner guidance', 'listening language rule and Part A profile tariff table', 'Part B hotel and weather', 'Part C interview and ingredient table', 'Part D with published alternative partial answer', 'Q1A matching, comprehension and mascot table', 'Q1B and Q2A1 with extraneous-material/language half-credit rule', 'Q2A2/translation and Q2B1 kanji', 'Q2B2 and Q2C grammar', 'Q3A/B with source-scoped half-credit rules', 'Q3C/D finite pools', 'Q4 content allocation and all alternatives', 'Q4 expression normal/lower bands and thresholds', 'Q5 headings and content allocation', 'Q5 expression normal/lower bands and thresholds', 'recording transcript Part A', 'recording transcript Part B', 'recording transcript Part C', 'recording transcript Part D', 'blank', 'blank', 'blank', 'back cover'])),
            }, 'tasks': TASKS, 'checksums': totals,
            'parserReconciliation': {
                'previousParserLeaves': 113, 'previousCoveredFragments': 71,
                'previousExcludedFragments': 41, 'previousOpenAddresses': ['Section 2A Q2(c)'],
                'independentCompleteTasks': 69,
                'explanation': 'The 71 previously served reading fragments comprise 29 retained task identities and 42 fragments now aliased to seven whole printed pools. The independent sweep adds the missing mascot table and two separately priced Q2A2(c) responses, yielding 39 reading tasks. Two complete writing tasks and 28 listening tasks replace the legacy parser/exclusion treatment. All 52 physical pages and the same three original PDF hashes remain accounted for; no exclusions count as completion.',
            },
            'choiceBoundaries': [
                'Q1A1 is one required five-cell matching task; Q1A7 is one required mascot table priced 2+1+2. Preserve old identities through explicit audited aliases, not duplicate scheduling.',
                'Q2B1/2 and Q2C1/2 are each one any-five-of-six pool. Q3C is one any-five-of-six reading-and-meaning pool (1+1 per selected kanji).',
                'Q3D is one any-ten-of-twelve blank pool. Seven printed sentence numbers do not define seven different cards.',
                'Q4 is one choice of three writing tasks with the same C20/E20 grid, including opening1, two content9 placements and closing1; lower E15 if C<=10 or fewer than150characters.',
                'Q5 is one response covering any four of eight headings:7 per heading plus opening1 and closing1, then E30; lower E20 if C<=15 or fewer than200characters.',
                'Listening A retains each profile as a separately priced seven-mark task with all four required columns. Named components and whole-answer alternatives follow the printed allocations.',
                'Listening B1e is north-exit1 plus any two remaining directions at2+1. Listening C5 is one required three-cell ingredient table.',
                'Listening D3a retains its published1-mark alternative about the speaker’s own school alongside the full2+1 tariff, without adding it as a bonus.',
                'Extraneous-material half credit applies only to Q2A1(a-d) and Q3B1-4. Language rules are separately scoped by printed headings; no general all-paper rule or quarter-credit compounding is published.',
            ]}


if __name__ == '__main__':
    review = build()
    (ROOT / 'scripts/markbank/authoring/reviews/japanese-2025-hl-census.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {review["checksums"]}')
