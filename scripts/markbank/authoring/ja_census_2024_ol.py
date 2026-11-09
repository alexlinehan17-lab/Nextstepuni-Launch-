#!/usr/bin/env python3
"""Independent 41-page original-source sweep, before 2024 Ordinary authoring.

Complete printed tasks and published tariffs; no card data is read.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2024-ol-000-paper.pdf', '4b98a657a87bff55e83fe8419ed2d9f0926738f2bab6820c976637a0bde1b14e'),
    ('aural', 'examiner-reports/japanese/papers/2024-ol-A00-paper.pdf', '466dda0e3f2d8e38475be8c3fd9d636db7d7490e80f99187ab9659d274750abc'),
    ('scheme', 'examiner-reports/japanese/schemes/2024-ol.pdf', '998990bd6cfdec27155f064a23766c1797503ac9afa11ccfa273fa2783d1dfea'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058GLP{"A00" if component == "aural" else "000"}BV.pdf', 'questionNumber': str(atlas)}})


def build():
    for q, marks in enumerate([10, 3, 2, 3, 3, 6, 3], 1):
        task('1', q, marks, 3, [5], q)
    for q, marks in enumerate([2, 2, 3, 2, 2, 2], 1):
        task('2A', q, marks, 5, [6], q + 7)
    task('2B', None, 15, 5, [6], 14)
    task('2C', None, 10, 6, [7], 15)
    task('2D', None, 4, 7, [7], 16)
    task('3A', 1, 2, 9, [8], 17)
    task('3A', 2, 4, 9, [8], 18)
    for roman in ['i', 'ii']:
        task('3A', 3, 2, 9, [8], 19, roman)
    for roman in ['i', 'ii', 'iii', 'iv']:
        task('3A', 4, 3, 9, [8], 20, roman)
    task('3A', 5, 6, 10, [8], 21)
    task('3B', 1, 10, 10, [9], 22)
    task('3B', 2, 10, 11, [9], 23)
    task('4', None, 30, 12, [10], 24)
    task('5', None, 50, 13, [10, 11], 25)
    for q, allocations in [(1, [4, 4]), (2, [2, 4, 4]), (3, [4, 2, 4])]:
        for roman, marks in zip(['i', 'ii', 'iii'], allocations):
            task('LA', q, marks, 2, [3], q, roman)
    for q, marks in enumerate([4, 4, 2, 2, 4, 4, 2, 4], 1):
        task('LB', q, marks, 3, [3], q + 8 if q < 4 else q)
    for q, allocations in [(1, [4, 2, 4, 4]), (2, [2, 2, 4])]:
        for roman, marks in zip(['i', 'ii', 'iii', 'iv'], allocations):
            task('LC', q, marks, 4, [4], q + 11, roman)
    for q, allocations in [(1, [2, 2, 4]), (2, [4, 4]), (3, [4, 4])]:
        for roman, marks in zip(['i', 'ii', 'iii'], allocations):
            task('LD', q, marks, 5, [4], q + 13, roman)
    assert len(TASKS) == 59
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 80, 'listening': 100, 'total': 300}, totals
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2024, 'level': 'ol', 'reviewedAt': '2026-11-09',
            'method': 'Independent visual sweep of all16 written,8 listening and17 scheme physical pages before authoring; complete tasks, separately priced responses, quotas and partial tariffs counted directly from the originals.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 17)), ['cover', 'Q1 original Tokyo Dome website and membership table', 'Q1 matching, comprehension and required membership table', 'Q2 original ramen article and museum details', 'Q2A six responses and Q2B any-five T/F-plus-quote pool', 'Q2C any-ten-of-thirteen meaning pool', 'Q2D two Japanese diet reasons', 'Q3 original Mia/Sarah conversation', 'Q3A1-4 comprehension, separately priced mother/brother and four MC responses', 'Q3A5 any-three pool and Q3B1 any-five negative forms', 'Q3B2 any-five particle pool', 'Q4 any-ten-of-twelve travel cloze and complete word bank', 'Q5 any-five-of-eight friend responses and vocabulary', 'explicit blank', 'explicit blank', 'copyright and back cover'])),
                'aural': dict(zip(map(str, range(1, 9)), ['cover and English-answer instructions', 'Part A eight separately priced hobby tasks', 'Part B eight separately priced Sky Brown tasks', 'Part C seven separately priced festival/weather tasks', 'Part D seven tasks and phone grid with four missing digits', 'explicit blank', 'explicit blank', 'back cover with explicit blank'])),
                'scheme': dict(zip(map(str, range(1, 18)), ['cover', 'general examiner guidance', 'listening language rule and Parts A28/B26 tariffs; A2 third item mislabelledii', 'listening Parts C22/D24 tariffs; C2 third item mislabelledii; phone one mark per missing digit', 'reading language rule and Q1 tables/comprehension30', 'Q2A13 and Q2B any-five T/F-plus-quote15', 'Q2C10 and Q2D4 mislabelledB/C; no diet model answer', 'Q3A1-4 total22 and Q3A5 any-three6', 'Q3B two any-five grammar pools10each', 'Q4 any-ten cloze30 and Q5 content bands', 'Q5 per-response expression5 bands', 'Part A recording transcript', 'Part B recording transcript', 'Part C transcript and beginning Part D', 'Part D transcript continuation', 'blank', 'back cover'])),
            },
            'sourceDiscrepancies': [
                {'paperPages': [2], 'schemePages': [3], 'taskKey': ['LA', 2, None, 'iii'], 'evidence': 'Scheme repeats(ii) for A ninja game; exact question/answer wording binds paperLA2(iii).'},
                {'paperPages': [4], 'schemePages': [4], 'taskKey': ['LC', 2, None, 'iii'], 'evidence': 'Scheme repeats(ii) for Jumper; exact question/answer wording binds paperLC2(iii).'},
                {'paperPages': [6, 7], 'schemePages': [7], 'evidence': 'Scheme titles the meaning poolPartB and diet responsePartC, after its actualB truth/quote table. Paper labels areC andD; matching wording and totals bind the tasks without changing paper references.'},
            ],
            'choiceBoundaries': [
                'Q1.1 is one required five-cell matching task at2each. Q1.6 is one membership table with three missing cells at2each; Silver eight visits is the given example.',
                'Q1.2 requires three sports at1each. Q1.4/5/7 andQ2A3 use the published descending2+1 quota for two accepted details.',
                'Q2B stays one any-five-of-six pool with truth1 and exact supporting quote2 separately claimable. Q2C stays one any-ten-of-thirteen pool at1each.',
                'Q2D prices two diet reasons at2each but supplies no answer text. Retain one unprinted4 criterion with two2-mark parts, without inventing nutrition claims.',
                'Q3A3(i)mother and(ii)brother are separately priced2-mark responses, sharing their printed stem. Q3A4 has four separate3-mark MC tasks.',
                'Q3A5 is one any-three-of-four Japanese response pool at2each. Q3B1/B2 are each one any-five-of-six grammar pool at2each; retain examples and underlines.',
                'Q4 is one any-ten-of-twelve cloze pool at3each, with the complete word bank and each word used once. Q5 is one any-five-of-eight pool with independent content5/expression5 per selected response.',
                'Listening A8/B8/C7/D7 tasks. D1iii keeps its prefilled grid and four missing digits5,4,1,9 at1each; no credit for given digits. D1i gives a whole2-mark6:30 answer, unlike Higher separate time/pm.',
                'Reading physicalp5 has a general appropriate-language half-credit rule on27tasks. Listening physicalp3 names Japanese/romaji/script on30tasks. Writing has no language reduction; no extraneous-material condition is printed.',
                'Original Atlas anchors remain1–25 written and1–16 listening. Written Q5 anchor25 requires expression physicalp11 added beside its existing contentp10; numbering and topics remain stable.',
            ]}


if __name__ == '__main__':
    census = build()
    (Path(__file__).parent / 'reviews/japanese-2024-ol-census.json').write_text(json.dumps(census, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {census["checksums"]}')
