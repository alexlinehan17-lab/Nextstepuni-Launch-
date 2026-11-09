#!/usr/bin/env python3
"""Independent census after visually reviewing all 40 original source pages.

This module reads no generated card data. Local published tariffs sum to 301
offered marks: Q2's explicit 14+15+10+4 disagrees with its heading of 42.
The phone row has an unresolved partial-credit conflict, recorded below.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2022-ol-000-paper.pdf', 'f74fee39f437d293d101cb9f8ee3743eb1c268f7bc01950fa3016f59baaa32f1'),
    ('aural', 'examiner-reports/japanese/papers/2022-ol-A00-paper.pdf', '0967cbf965a69d1d695174b6104824c174b13ff582c7cb379a39e8c209de5ad8'),
    ('scheme', 'examiner-reports/japanese/schemes/2022-ol.pdf', 'e348bdf1ac02f46c9c73350d1b7fbde4505a8d4f0dc0ff406ed4ac2d4e11093d'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058GLP{"A00" if component == "aural" else "000"}BV.pdf',
                            'questionNumber': str(atlas)}})


def build():
    for q, marks in enumerate([12, 2, 2, 3], 1):
        task('1', q, marks, 3, [5], q)
    for roman in ['i', 'ii']:
        task('1', 5, 2, 3, [5], 5, roman)
    task('1', 6, 7, 3, [5], 6)
    for q, marks in enumerate([2, 4, 2, 2, 2, 2], 1):
        task('2A', q, marks, 5, [6], q + 6)
    task('2B', None, 15, 5, [6], 13)
    task('2C', None, 10, 6, [7], 14)
    task('2D', None, 4, 7, [7], 22)
    for q, marks in enumerate([2, 3, 2], 1):
        task('3A', q, marks, 9, [7], q + 14)
    for roman in ['i', 'ii', 'iii', 'iv']:
        task('3A', 4, 3, 9, [7], 18, roman)
    task('3A', 5, 9, 10, [8], 19)
    task('3B', 1, 10, 10, [8], 20)
    task('3B', 2, 10, 11, [8], 21)
    task('4', None, 40, 12, [9], 23)
    task('5', None, 40, 13, [9, 10], 24)
    for section, questions, pp, sp, atlas in [
        ('LA', [(1, [4, 4, 2]), (2, [4, 2]), (3, [4, 2, 4])], 2, 3, 1),
        ('LB', [(1, [4, 2, 4, 4, 4]), (2, [2, 4])], 3, 3, 2),
        ('LC', [(1, [4, 4]), (2, [4, 2]), (3, [4, 4, 4])], 4, 4, 3),
        ('LD', [(1, [2, 4, 2, 2]), (2, [3, 3, 4, 4])], 5, 4, 4),
    ]:
        for q, marks in questions:
            for roman, mark in zip(['i', 'ii', 'iii', 'iv', 'v'], marks):
                task(section, q, mark, pp, [sp], atlas, roman)
    assert len(TASKS) == 58
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'),
        ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 121, 'writing': 80, 'listening': 100, 'total': 301}, totals
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {
        'subjectId': 'japanese', 'year': 2022, 'level': 'ol', 'reviewedAt': '2026-11-09',
        'method': 'Independent full visual sweep of all 16 written, eight aural and 16 scheme physical pages before authoring. Count complete independently priced tasks, retaining all printed alternatives and exact local tariffs.',
        'sources': sources, 'tasks': TASKS, 'checksums': totals,
        'candidateMaximum': {'publishedWritten': 160, 'publishedListening': 100, 'publishedTotal': 260,
                             'sumOfLocalTariffs': 261,
                             'writingChoice': 'Answer either Q4 or Q5, each 40 marks. Both remain offered practice tasks.'},
        'pageRoles': {
            'paper': dict(zip(map(str, range(1, 17)), [
                'cover; adjusted examination answers Q1–3 and either Q4 or Q5',
                'Q1 original Zozo shopping website and sale advertisement',
                'Q1 complete six-link match; three English responses; two Japanese sports links; complete sale table',
                'Q2 original Akihabara shopping article, photographs and vocabulary',
                'Q2A six English responses and Q2B any-five-of-six truth/evidence pairs',
                'Q2C any-ten-of-thirteen kanji multiple-choice pool, all English and Irish choices',
                'Q2D open culture task: two details about manga and anime',
                'Q3 original Cian school interview, photographs and vocabulary',
                'Q3A three English responses and four individually priced multiple-choice items',
                'Q3A5 any-three-of-four Japanese responses and Q3B1 any-five-of-six past-tense pool',
                'Q3B2 any-five-of-six particle-choice pool',
                'Q4 complete summer-job cloze, twelve blanks and word bank; answer any ten; either Q4 or Q5',
                'Q5 eight independent weekend responses with answer grids and vocabulary; choose any five',
                'explicit blank', 'explicit blank', 'back cover']),),
            'aural': dict(zip(map(str, range(1, 9)), [
                'cover and English-answer instructions',
                'Part A eight separately priced student responses with all multiple-choice options',
                'Part B five Taiko Centre tasks including phone grid, then two weather tasks',
                'Part C seven school-reception responses with all multiple-choice options',
                'Part D four lunch-arrangement responses and four cafe-order responses',
                'explicit blank', 'explicit blank', 'back cover'])),
            'scheme': dict(zip(map(str, range(1, 17)), [
                'cover', 'general examiner guidance',
                'listening Japanese/romaji/script half credit; Part A26 and Part B24; phone partial wording conflicts with four-mark total',
                'Part C26 and Part D24; C3(iii) printed as (vii)',
                'reading language half credit and Q1 local tariffs30 with complete sale table',
                'Q2 heading42, local A14 and B15 with six truth/evidence answers',
                'Q2C10 and D4; Q3A19 with separately priced multiple-choice items',
                'Q3 Japanese pool9 labelled B despite paper A5; two grammar pools20 labelled C despite paper B',
                'Q4 any-ten-of-twelve cloze40; Q5 any-five-of-eight C4/E4 responses40 and content bands',
                'Q5 independent expression bands out of4',
                'tapescript Part A and Taiko Centre', 'tapescript weather and Part C',
                'tapescript Part D', 'explicit blank', 'explicit blank', 'back cover'])),
        },
        'sourceDiscrepancies': [
            {'paperPages': [4, 5, 6, 7], 'schemePages': [6, 7],
             'evidence': 'Q2 heading42 conflicts with explicit A14+B15+C10+D4=43. Reading local totals30+43+48=121 conflict with printed120. Retain each local tariff and disclose the discrepancy; never silently subtract a mark from a real task.'},
            {'taskKey': ['LB', 1, None, 'v'], 'paperPages': [3], 'schemePages': [3],
             'evidence': 'Phone0120-923-915 has eight missing digits in the paper. Scheme prints (any two digits, 1 mark each) beside a four-mark total. This is a real internal conflict, not four one-mark blanks; partial-credit interpretation requires explicit review.'},
            {'taskKey': ['LC', 3, None, 'iii'], 'paperPages': [4], 'schemePages': [4],
             'evidence': 'Volleyball match uses paper(iii), printed(vii) in scheme; bind by exact wording.'},
            {'paperPages': [10, 11], 'schemePages': [8],
             'evidence': 'Paper Japanese-response pool is Q3A5, not scheme B. Paper grammar is Q3B1/2, not scheme C1/2. Preserve paper citations and original Atlas identities.'},
        ],
        'choiceBoundaries': [
            'Q1 six-link match is one required task; complete sale table is one task with date1+1, time1+1, login1 and discounted item2. Q1 sports links i/ii are separately priced2 each.',
            'Q2B is one any-five-of-six truth1/evidence2 pool. Q2C is one any-ten-of-thirteen kanji pool1 each. Q2D is one open culture response with two details2 each and no printed model answers.',
            'Q3A4 four multiple-choice items are separately priced3 each. Q3A5 is one any-three-of-four response pool3 each. Q3B1/2 are separate complete any-five-of-six grammar pools2 each.',
            'Q4 is one any-ten-of-twelve cloze pool4 each with the complete passage and word bank. Q5 is one any-five-of-eight pool with independent C4/E4 assessment per selected response, no shared aggregate expression score.',
            'Listening has 30 separate priced tasks; every multiple-choice prompt retains all printed alternatives. Descending school description uses2+1. Food and dessert each choose one accepted example for3.',
            'Reading half-credit instruction appears before all26 reading tasks; listening Japanese/romaji/script instruction appears before all30 listening tasks. Numeric-only phone retains that instruction visibly but no language scoring control while its partial tariff remains unresolved. No writing language reduction or extraneous-material rule is published.',
            'All original24 written and four listening Atlas identities remain; correct only inaccurate labels/page bounds or missing exact source regions after visual review.',
        ],
    }


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2022-ol-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
