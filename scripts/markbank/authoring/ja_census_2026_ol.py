#!/usr/bin/env python3
"""Independent inventory from the 44 visually swept 2026 Ordinary pages.

This file enumerates printed task boundaries and tariffs before the authoring
manifest exists. It never imports cards or asks a card parser for its count.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2026-ol-000-paper.pdf', '3e426ef7ef17020d89b812e13eabaf47efb18d3b0b97e6dd4810d966551634b7'),
    ('aural', 'examiner-reports/japanese/papers/2026-ol-A00-paper.pdf', '19c7f71b7308c47f20207f7f90845456ea9c445e5e64e6ba1e72f56a878181d1'),
    ('scheme', 'examiner-reports/japanese/schemes/2026-ol.pdf', '1781dbc10f0f34043655b1ee9a093f368726a8caa5203dad214d0c63051321cc'),
]
TASKS = []


def task(section, question, marks, paper_page, scheme_pages, atlas, letter=None, roman=None, additional_atlas=None):
    component = 'aural' if section.startswith('L') else 'paper'
    record = {'key': [section, question, letter, roman], 'marks': marks,
              'component': component, 'paperPages': [paper_page], 'schemePages': scheme_pages,
              'atlas': {'fileid': f'LC058GLP{"A00" if component == "aural" else "000"}BV.pdf', 'questionNumber': str(atlas)}}
    if additional_atlas:
        record['atlas']['additionalQuestionNumbers'] = list(map(str, additional_atlas))
    TASKS.append(record)


def build():
    # Q1: matching table, four short tasks, two drinks and three offer tasks.
    for q, marks in [(1, 10), (2, 3), (3, 3)]:
        task('1', q, marks, 3, [6], q)
    for letter in 'ab':
        task('1', 4, 1, 3, [6], 4, letter)
    task('1', 5, 2, 3, [6], 5)
    for letter, marks in [('a', 2), ('b', 3), ('c', 5)]:
        task('1', 6, marks, 3, [7], 6, letter)
    # Q2: 6 comprehension tasks and 3 complete printed pools/responses.
    for q, marks in enumerate([2, 2, 2, 2, 3, 4], 1):
        task('2A', q, marks, 5, [7], q + 6)
    task('2B', None, 15, 5, [8], 13, additional_atlas=range(14, 19))
    task('2C', None, 10, 6, [8], 19)
    task('2D', None, 4, 7, [8], 20)
    # Q3: seven fixed comprehension tasks, one choose-three and two grammar pools.
    for q, marks in enumerate([2, 4, 2], 1):
        task('3A', q, marks, 9, [9], q + 20)
    for letter in 'abcd':
        task('3A', 4, 3, 9, [9], 24, letter)
    task('3A', 5, 6, 10, [9], 25)
    task('3B', 1, 10, 10, [10], 26)
    task('3B', 2, 10, 11, [10], 27)
    # The cloze is one choose-ten task. Writing is one choose-five pool.
    task('4', None, 30, 12, [11], 28)
    task('5', None, 50, 13, [11, 12], 29)
    # Listening: every printed separately priced task, including MC options.
    for q, values in [(1, [4, 4]), (2, [2, 4, 2]), (3, [2, 4, 4])]:
        for roman, marks in zip(['i', 'ii', 'iii'], values):
            task('LA', q, marks, 2, [4], q, roman=roman)
    for q, values in [(1, [4, 4]), (2, [4, 2]), (3, [4, 4, 4])]:
        for roman, marks in zip(['i', 'ii', 'iii'], values):
            task('LB', q, marks, 3, [4], q + 7, roman=roman)
    for roman, marks in zip(['i', 'ii', 'iii', 'iv', 'v'], [2, 4, 4, 2, 4]):
        task('LC', 1, marks, 4, [5], 11, roman=roman)
    task('LC', 2, 4, 4, [5], 12, roman='i')
    task('LC', 2, 4, 4, [5], 12, roman='ii')
    for q, marks in enumerate([4, 4, 2, 2, 4, 4, 4], 1):
        task('LD', q, marks, 5, [5], q + 12 if q <= 3 else q)
    assert len(TASKS) == 59
    totals = {kind: sum(t['marks'] for t in TASKS if predicate(t)) for kind, predicate in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 80, 'listening': 100, 'total': 300}
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2026, 'level': 'ol', 'reviewedAt': '2026-11-06',
            'method': 'Independent visual sweep of all 16 written, 8 aural and 20 scheme pages. Printed question boundaries, finite pools and published tariffs counted independently before authoring.',
            'sources': sources,
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 17)), ['cover', 'Q1 original restaurant website/menu', 'Q1 tasks and offer table', 'Q2 TikTok source article', 'Q2A comprehension and Q2B any-five T/F+quote pool', 'Q2C any-ten-of-thirteen kanji', 'Q2D culture response', 'Q3 Grace and Ryan source texts', 'Q3A1–4 tasks', 'Q3A5 any-three and Q3B1 any-five grammar', 'Q3B2 any-five particles', 'Q4 any-ten cloze', 'Q5 any-five-of-eight independent writing responses', 'explicit blank', 'explicit blank', 'acknowledgements'])),
                'aural': dict(zip(map(str, range(1, 9)), ['cover and instructions', 'Part A three profiles and tasks', 'Part B three conversations and tasks, prefilled phone number', 'Part C two news items and tasks', 'Part D interview tasks', 'explicit blank', 'explicit blank', 'back cover'])),
                'scheme': dict(zip(map(str, range(1, 21)), ['cover', 'general examiner guidance', 'answer conventions and wrong-language half credit', 'listening Parts A and B', 'listening Parts C and D', 'reading Q1 tasks 1–5', 'reading Q1 task6 and Q2A', 'Q2B/C/D', 'Q3A', 'Q3B grammar', 'Q4 cloze and Q5 content bands', 'Q5 expression bands', 'recording script Parts A and B', 'recording script Parts B and C', 'recording script Part D', 'blank', 'blank', 'blank', 'blank', 'back cover'])),
            }, 'tasks': TASKS, 'checksums': totals,
            'parserReconciliation': {
                'legacyFragments': 111, 'reviewedTasks': 59, 'difference': -52,
                'groupingReductions': {'Q1.1 matching table': 4, 'Q2B any-five': 5, 'Q2C any-ten': 12, 'Q3A5 any-three': 3, 'Q3B1 any-five': 5, 'Q3B2 any-five': 5, 'Q4 any-ten': 11, 'Q5 any-five': 7},
                'addressCorrection': 'The parser misreads the restaurant menu link10 as Section1Q10 and misses the actual Q1.6(c) table. The source census restores the printed table task, with no net count change from that address correction.',
                'sourceInventory': 'All16written,8aural and20scheme pages retained. All older sitting ledgers and the66-component subject source inventory remain unchanged.',
            },
            'choiceBoundaries': [
                'Q1.1 is one required five-cell matching table, with printed 2 marks per cell.',
                'Q1.6(c) is one required three-cell completion table priced 2+1+2.',
                'Q2B is one any-five-of-six pool with True/False1 and supporting quote2 per chosen response. Preserve Atlas anchors13–18.',
                'Q2C is one any-ten-of-thirteen kanji pool, not thirteen separate cards.',
                'Q2D requests two reasons, priced2 each without model answers; one4-mark response, no invented answers.',
                'Q3A5 is one any-three-of-four response pool, priced2 per answer.',
                'Q3B1 and Q3B2 each choose five of six, priced2 per answer.',
                'Q4 is one any-ten-of-twelve cloze pool, priced3 per blank.',
                'Q5 is one any-five-of-eight writing pool with independent C5/E5 per selected response.',
                'Listening C2(i) retains Saturday and Sunday as two required rows in the one printed weather task, priced2 each.',
            ]}


if __name__ == '__main__':
    result = build()
    path = ROOT / 'scripts/markbank/authoring/reviews/japanese-2026-ol-census.json'
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
