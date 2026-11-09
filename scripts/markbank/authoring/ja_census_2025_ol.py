#!/usr/bin/env python3
"""Independent 40-page original-paper sweep, before 2025 Ordinary authoring.

This inventories complete tasks and published tariffs without reading cards.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2025-ol-000-paper.pdf', 'f0c17ece1c7896e680f84903d780fa51bceec23638ad249f37953e61e39c0f3e'),
    ('aural', 'examiner-reports/japanese/papers/2025-ol-A00-paper.pdf', '272e54c3ce42b5689fdd94b090713bd248d43e4ae71579d4c31a638354b81df6'),
    ('scheme', 'examiner-reports/japanese/schemes/2025-ol.pdf', 'a11b7c790c76827cbd049d0ccea42c9f6c33f109c027db0a566e84ddb954cabc'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, letter=None, roman=None, anchors=None):
    component = 'aural' if section.startswith('L') else 'paper'
    item = {'key': [section, q, letter, roman], 'marks': marks,
            'component': component, 'paperPages': [pp], 'schemePages': sp,
            'atlas': {'fileid': f'LC058GLP{"A00" if component == "aural" else "000"}BV.pdf', 'questionNumber': str(atlas)}}
    if anchors:
        item['atlas']['additionalQuestionNumbers'] = list(map(str, anchors))
    TASKS.append(item)


def build():
    for q, marks in enumerate([10, 4, 4, 4, 6, 2], 1):
        task('1', q, marks, 3, [5], q)
    for q, allocations in [(1, [2, 4]), (2, [2, 3]), (3, [2, 2])]:
        for letter, marks in zip('ab', allocations):
            task('2A', q, marks, 5, [6], q + 6, letter)
    task('2B', None, 15, 5, [6], 10, anchors=[11, 12, 13, 14, 15])
    task('2C', None, 10, 6, [7], 16)
    task('2D', None, 4, 7, [7], 17)
    for q, marks in enumerate([3, 3, 2], 1):
        task('3A', q, marks, 9, [7], q + 17)
    for roman in ['i', 'ii', 'iii', 'iv']:
        task('3A', 4, 3, 9, [7], 21, roman=roman)
    task('3A', 5, 6, 10, [8], 22)
    task('3B', 1, 10, 10, [8], 23)
    task('3B', 2, 10, 11, [8], 24)
    task('4', None, 30, 12, [9], 25)
    task('5', None, 50, 13, [9, 10], 26)
    for q, allocations in [(1, [2, 4, 4]), (2, [4, 4]), (3, [4, 4])]:
        for roman, marks in zip(['i', 'ii', 'iii'], allocations):
            task('LA', q, marks, 2, [3], q, roman=roman)
    for q, allocations in [(1, [4, 2, 4, 2, 2, 4]), (2, [4, 2])]:
        for roman, marks in zip(['i', 'ii', 'iii', 'iv', 'v', 'vi'], allocations):
            task('LB', q, marks, 3, [3], q + 7, roman=roman)
    for q, marks in enumerate([4, 4, 4, 6, 2, 2, 4], 1):
        task('LC', q, marks, 4, [4], q + 9 if q <= 3 else q)
    for q in [1, 2, 3]:
        for roman in ['i', 'ii']:
            task('LD', q, 4, 5, [4], q + 12, roman=roman)
    assert len(TASKS) == 55
    totals = {name: sum(task['marks'] for task in TASKS if condition(task)) for name, condition in [
        ('reading', lambda task: task['key'][0][0] in '123'), ('writing', lambda task: task['key'][0][0] in '45'),
        ('listening', lambda task: task['component'] == 'aural'), ('total', lambda task: True)]}
    assert totals == {'reading': 120, 'writing': 80, 'listening': 100, 'total': 300}, totals
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2025, 'level': 'ol', 'reviewedAt': '2026-11-09',
            'method': 'Independent visual sweep of all 16 written, 8 listening and 16 scheme pages before authoring; complete printed tasks, choice quotas, separately priced responses and partial tariffs counted directly from the originals.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 17)), ['cover', 'Q1 Tokyo Treat original website', 'Q1 matching and comprehension with two complete tables', 'Q2 three fashion profiles', 'Q2A six comprehension tasks and Q2B any-five T/F-plus-quote pool', 'Q2C any-ten-of-thirteen meaning pool', 'Q2D two cultural aspects', 'Q3 original Kate poster', 'Q3A1-4 comprehension and four separately priced MC responses', 'Q3A5 any-three pool and Q3B1 any-five negative forms', 'Q3B2 any-five particle pool', 'Q4 any-ten-of-twelve cloze and word bank', 'Q5 any-five-of-eight short responses with C/E', 'explicit blank', 'explicit blank', 'acknowledgements and copyright'])),
                'aural': dict(zip(map(str, range(1, 9)), ['cover and English-answer instructions', 'Part A seven separately priced tasks', 'Part B eight tasks and prefilled phone grid', 'Part C seven tasks including required three-cell table', 'Part D six separately priced MC tasks', 'explicit blank', 'explicit blank', 'back cover with explicit blank'])),
                'scheme': dict(zip(map(str, range(1, 17)), ['cover', 'general examiner guidance', 'listening language rule and Parts A/B tariffs', 'listening Parts C/D tariffs and ingredient table', 'reading language rule and Q1 tariffs with matching and membership tables', 'Q2A comprehension and Q2B T/F-plus-quote table', 'Q2C meanings, Q2D criterion only, Q3A1-4 tariffs', 'Q3A5 and Q3B finite pools', 'Q4 cloze and Q5 content bands', 'Q5 expression bands', 'Part A recording transcript', 'Part B recording transcript', 'Part C recording transcript', 'Part D recording transcript', 'blank', 'back cover'])),
            },
            'choiceBoundaries': [
                'Q1 matching is one required five-cell task (2 each); Q1.4 retains both named snack cells (2 each); Q1.5 is one membership table with Silver2, Gold2 and price1+duration1.',
                'Q2B is one any-five-of-six pool, with independently claimable truth1 and exact supporting quote2; original Atlas anchors10–15 remain attached.',
                'Q2C is one any-ten-of-thirteen meaning pool (1 each). Q2D prices any two cultural aspects at2each but gives no model answer; retain one unprinted4 criterion with two2-mark parts.',
                'Q3A4 has four separately priced3-mark MC tasks; Q3A5 is one any-three-of-four Japanese response pool,2each.',
                'Q3B1 and Q3B2 are each one any-five-of-six grammar pool at2each; preserve printed example and underlines.',
                'Q4 is one any-ten-of-twelve cloze pool at3each. The paper requires each bank word only once; scheme alternatives for blanks3/7 and9 are retained.',
                'Q5 is one any-five-of-eight pool, each chosen response with independent content5 and expression5. No model responses are printed; use the original content and expression bands.',
                'Listening A has7, B8, C7 and D6 tasks. C4 is one required three-cell table at2each; B1vi retains all prefilled phone digits.',
                'Reading p5 halves answers not in the appropriate language. Listening p3 specifically halves Japanese/romaji/Japanese-script answers. No published writing-language or extraneous-material reduction appears in this scheme.',
            ]}


if __name__ == '__main__':
    census = build()
    (Path(__file__).parent / 'reviews/japanese-2025-ol-census.json').write_text(json.dumps(census, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {census["checksums"]}')
