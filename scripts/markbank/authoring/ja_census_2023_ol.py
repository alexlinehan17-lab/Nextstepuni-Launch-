#!/usr/bin/env python3
"""Independent 40-page source census, completed before 2023 Ordinary authoring.

No generated cards are read: task boundaries come from the original paper and
scheme, including every complete choice pool and required table.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2023-ol-000-paper.pdf', '2307421a7a512bf54cee23213875bc1545b5616ffd7cc877aa28034232a27e3b'),
    ('aural', 'examiner-reports/japanese/papers/2023-ol-A00-paper.pdf', 'bc4052eb76ca8ca4f0e552c4e79a1475f73ac5d223207abfb199efd32e89f9eb'),
    ('scheme', 'examiner-reports/japanese/schemes/2023-ol.pdf', '360f0300ec60d4920a5831f01f53f9dce2ed9169eb2f569c3f0a6760a4932425'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058GLP{"A00" if component == "aural" else "000"}BV.pdf', 'questionNumber': str(atlas)}})


def build():
    for q, marks in enumerate([10, 4, 2, 2, 4, 2, 4, 2], 1):
        task('1', q, marks, 3, [5], q)
    for q, marks in enumerate([4, 2, 2, 2, 3], 1):
        task('2A', q, marks, 5, [6], q + 8)
    task('2B', None, 15, 5, [6], 14)
    task('2C', None, 10, 6, [7], 15)
    task('2D', None, 10, 7, [7], 16)
    for q, marks in enumerate([4, 2, 4], 1):
        task('3A', q, marks, 9, [8], q + 16)
    for roman in ['i', 'ii', 'iii', 'iv']:
        task('3A', 4, 3, 9, [8], 20, roman)
    task('3A', 5, 6, 10, [8], 21)
    task('3B', None, 4, 10, [8], 25)
    task('3C', None, 10, 10, [9], 22)
    task('4', None, 30, 11, [9], 23)
    task('5', None, 50, 12, [10, 11], 24)
    for q, allocations in [(1, [2, 4, 4]), (2, [2, 4, 2]), (3, [4, 4])]:
        for roman, marks in zip(['i', 'ii', 'iii'], allocations):
            task('LA', q, marks, 2, [3], 1, roman)
    for q, allocations in [(1, [2, 4, 2, 4, 4]), (2, [4, 2, 4])]:
        for roman, marks in zip(['i', 'ii', 'iii', 'iv', 'v'], allocations):
            task('LB', q, marks, 3, [3], 2, roman)
    for q, allocations in [(1, [4, 3, 4]), (2, [4]), (3, [3, 4])]:
        for roman, marks in zip(['i', 'ii', 'iii'], allocations):
            task('LC', q, marks, 4, [4], 3, roman)
    for roman, marks in zip(['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii'], [4, 4, 2, 4, 2, 4, 4, 2]):
        task('LD', None, marks, 5, [4], 4, roman)
    assert len(TASKS) == 58
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 80, 'listening': 100, 'total': 300}, totals
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2023, 'level': 'ol', 'reviewedAt': '2026-11-09',
            'method': 'Independent visual sweep of all 16 written, eight listening and 16 scheme physical pages before authoring; complete tasks and published tariffs counted directly from originals.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 17)), ['cover', 'Q1 original KFC website, menu and Christmas offers', 'Q1 required five-item link match, six comprehension responses and any-two item/quantity table', 'Q2 original Yonezu Kenshi and Aimyon articles with vocabulary', 'Q2A four-cell artist profile table and four comprehension tasks, Q2B any-five T/F-plus-quote pool', 'Q2C any-ten-of-thirteen meanings', 'Q2D any-five-of-six particles', 'Q3 original Ian exchange-student blog and vocabulary', 'Q3A1-3 comprehension and Q3A4 four separately priced multiple-choice responses', 'Q3A5 any-three-of-four, Q3B school comparison and Q3C any-five-of-six past forms', 'Q4 any-ten-of-twelve school cloze and complete word bank', 'Q5 any-five-of-eight hobby responses and vocabulary', 'explicit blank', 'explicit blank', 'explicit blank', 'copyright/back cover'])),
                'aural': dict(zip(map(str, range(1, 9)), ['cover and English-answer instructions', 'Part A eight teacher-listening tasks', 'Part B eight museum tasks including four-blank phone grid', 'Part C six job-ranking, walking-tour and weather tasks', 'Part D eight roman tasks without question numbers', 'explicit blank', 'explicit blank', 'copyright/back cover'])),
                'scheme': dict(zip(map(str, range(1, 17)), ['cover', 'general examiner guidance', 'listening language rule, Part A26 and Part B26', 'Part C22 and Part D26', 'reading general language rule and Q1 30', 'Q2A13 and Q2B15 with truth1/quote2 for any five', 'Q2C10 and Q2D10', 'Q3A28 and Q3B4 without model answers', 'Q3C10 and Q4 school cloze30 with mismatched blank(ix)', 'Q5 independent response C5/E5, source prompts(vii)/(viii) differ from paper', 'Q5 content and expression bands, holistic expression note', 'recording transcript Part A', 'recording transcript Part B', 'recording transcript Part C', 'recording transcript Part D', 'back cover'])),
            },
            'sourceDiscrepancies': [
                {'paperPages': [11], 'schemePages': [9], 'taskKey': ['4', None, None, None], 'evidence': 'Scheme blank(ix) prints 四年生, absent from the original word bank; paper bank includes トレーニング. Preserve both original sources and render the discrepancy, without inventing a corrected official answer.'},
                {'paperPages': [12], 'schemePages': [10, 11], 'taskKey': ['5', None, None, None], 'evidence': 'Paper(vii) asks そのしゅみはどうですか。 and(viii) asks あたらしいしゅみがしたいですか。; scheme(vii) repeats the latter and(viii) says なつ休みが好きですか。. Keep the eight paper prompts with the common published per-response C5/E5 grid.'},
                {'paperPages': [5], 'schemePages': [4], 'taskKey': ['LD', None, None, 'iv'], 'evidence': 'Morning activities is paper(iv); the scheme labels this row(vi), then later repeats(vi) for the start date. Preserve paper(iv) with its matching Sports answer and4marks.'},
            ],
            'choiceBoundaries': [
                'Q1 matching is one required five-cell task at2marks each. Q1(7) is one any-two-of-four item-and-quantity task at2marks per complete item; no separate one-mark component tariff is printed.',
                'Q2A1 is one required four-cell table at1mark each. Given Lemon and Hyougo are context, not mark-bearing cells.',
                'Q2B one any-five-of-six truth1/quote2 pool. Q2C one any-ten-of-thirteen meaning pool1each. Q2D one any-five-of-six particle pool2each.',
                'Q3A4 four independently priced multiple-choice responses3each; Q3A5 one any-three-of-four response pool2each. Q3B one open two-point comparison2each with no model answers, not a finite-topic choice. Q3C one any-five-of-six past-form pool2each.',
                'Q4 one any-ten-of-twelve blank pool3each with every word-bank item retained. Scheme blank(ix) discrepancy is explicit, not excluded.',
                'Q5 one any-five-of-eight writing pool, each selected answer independently content5/expression5; no global shared expression score or extra model answers.',
                'Listening tasks split only at printed response tariffs. Four phone blanks remain one task; scheme gives4marks for the complete number without a separate per-digit tariff. Given digits remain stimulus only.',
                'Language half credit applies to all26reading tasks under schemep5 and all30listening tasks under schemep3 Japanese/romaji/script rule; no writing or extraneous-material rule is printed.',
            ]}


if __name__ == '__main__':
    result = build()
    path = Path(__file__).parent / 'reviews/japanese-2023-ol-census.json'
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f"Independent census: {len(TASKS)} tasks, {result['checksums']}")
