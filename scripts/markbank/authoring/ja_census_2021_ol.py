#!/usr/bin/env python3
"""Independent 2021 Ordinary census after viewing every original physical page.

This script reads no authored cards. Required tables and finite pools are each
one task; each separately priced question remains separate.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2021-ol-000-paper.pdf', '9e08378aa046efa6aa546be9a143a6ed4c42037cccc146c1638a65b91af75063'),
    ('aural', 'examiner-reports/japanese/papers/2021-ol-A00-paper.pdf', 'cd02fd8088e72e5f54b8eb89d238be0eec8e8252fc48ce2b5be7cfdbb2f44110'),
    ('scheme', 'examiner-reports/japanese/schemes/2021-ol.pdf', 'ddc4b5bd8045f44a4a86664c7fc4c4981ed659cb1f14b83c4801cb5a4fb0b30b'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': pp if isinstance(pp, list) else [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058GLP{"A00" if component == "aural" else "000"}BV.pdf',
                            'questionNumber': str(atlas)}})


def build():
    for q, marks in enumerate([10, 3, 3, 3, 3, 3], 1):
        task('1', q, marks, 3, [5], q)
    task('1', 7, 2, 3, [5], 7, 'i')
    task('1', 7, 3, 3, [5], 7, 'ii')
    for q, marks in enumerate([2, 3, 2, 2, 4], 1):
        task('2A', q, marks, 5, [5] if q < 3 else [6], q + 7)
    task('2B', None, 15, 5, [6], 13)
    task('2C', None, 10, [6, 7], [7], 14)
    task('2D', None, 4, 7, [7], 22)
    for q, marks in enumerate([3, 3, 4], 1):
        task('3A', q, marks, 9, [7] if q < 3 else [8], q + 14)
    for roman in ['i', 'ii', 'iii', 'iv']:
        task('3A', 4, 3, 9, [8], 18, roman)
    task('3A', 5, 6, 10, [8], 19)
    task('3B', 1, 10, 10, [8], 20)
    task('3B', 2, 10, 10, [9], 21)
    task('4', None, 40, 11, [9], 23)
    task('5', None, 40, 12, [10, 11], 24)
    for section, questions, pp, sp, atlas in [
        ('LA', [(1, [2, 4, 4]), (2, [2, 4]), (3, [4, 4, 2])], 2, 3, 1),
        ('LB', [(1, [4, 2, 4, 2, 4]), (2, [4, 4])], 3, 3, 2),
        ('LC', [(None, [4, 2, 4, 4, 4, 4, 4])], 4, 4, 3),
        ('LD', [(None, [4, 2, 4, 4, 4, 2, 4])], 5, 4, 4),
    ]:
        for q, marks in questions:
            for roman, mark in zip(['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii'], marks):
                task(section, q, mark, pp, [sp], atlas, roman)
    assert len(TASKS) == 57
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'),
        ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 80, 'listening': 100, 'total': 300}, totals
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {
        'subjectId': 'japanese', 'year': 2021, 'level': 'ol', 'reviewedAt': '2026-11-09',
        'method': 'Independent full visual sweep of all 16 written, eight aural and 16 scheme physical pages before authoring. Count whole independently priced tasks and preserve every printed choice and local tariff.',
        'sources': sources, 'tasks': TASKS, 'checksums': totals,
        'candidateMaximum': {'publishedWritten': 160, 'publishedListening': 100, 'publishedTotal': 260,
                             'writingChoice': 'Answer either Q4 or Q5, each40. Both remain offered practice tasks, so offered coverage totals300.'},
        'pageRoles': {
            'paper': dict(zip(map(str, range(1, 17)), [
                'cover; adjusted examination answers Q1–3 and either Q4 or Q5',
                'Q1 original Universal Studios Japan website: ten links, attractions, foods and ticket-price table',
                'Q1 complete five-link match, five English tasks and two separately priced ticket questions',
                'Q2 original LINE social-media article, photographs and vocabulary',
                'Q2A five English responses and Q2B any-five-of-six truth/evidence pairs',
                'Q2C any-ten-of-thirteen kanji pool: all Irish choices and first eight English choices',
                'Q2C final five English choices, Q2D open two-company culture task',
                'Q3 original Akira, Ichika and Kenta club profiles, photographs and vocabulary',
                'Q3A three English responses and four separately priced multiple-choice tasks',
                'Q3A5 any-three-of-four Japanese responses; Q3B1 negative-form and B2 particle any-five-of-six pools',
                'Q4 complete introduction cloze, twelve blanks and full word bank; any ten; either Q4 or Q5',
                'Q5 eight independent summer-holiday responses; any five, with answer grids and vocabulary',
                'explicit blank', 'explicit blank', 'explicit blank', 'back cover'])),
            'aural': dict(zip(map(str, range(1, 9)), [
                'cover and English-answer instruction',
                'Part A eight separate self-introduction tasks with all multiple-choice options',
                'Part B five Naomi Watanabe tasks and two weather tasks',
                'Part C seven Robot Restaurant tasks including four-blank phone grid',
                'Part D seven school and host-family tasks with all multiple-choice options',
                'explicit blank', 'explicit blank', 'back cover'])),
            'scheme': dict(zip(map(str, range(1, 17)), [
                'cover', 'general examiner guidance',
                'listening Japanese/romaji/script half credit, Part A26 and Part B24',
                'Part C26, including phone1mark per correct missing number, and Part D24',
                'reading general language half credit; Q1 tariffs30; Q2A first two responses',
                'Q2A remaining responses total13 and Q2B any-five-of-six truth1/evidence2 pairs',
                'Q2C any-ten-of-thirteen kanji10, Q2D culture4 with no model answers, Q3A first two responses',
                'Q3A remainder including any-three Japanese pool6, Q3B1 any-five-of-six negative forms10',
                'Q3B2 any-five-of-six particles10; Q4 any-ten-of-twelve cloze40',
                'Q5 any-five-of-eight C4/E4, exact content bands and expression cannot exceed content',
                'Q5 expression bands1,2–3,4 and global language-use guidance',
                'tapescript Part A', 'tapescript Part B', 'tapescript Part C', 'tapescript Part D', 'back cover'])),
        },
        'sourceDiscrepancies': [
            {'taskKey': ['LD', None, None, 'iv'], 'paperPages': [5], 'schemePages': [4],
             'evidence': 'Disliked-subject response is paper(iv), misprinted(vi) in scheme. Bind by exact question and Maths answer; preserve paper citation.'},
            {'taskKey': ['4', None, None, None], 'paperPages': [11], 'schemePages': [9],
             'evidence': 'Scheme accepts サッカー/えいが in blank(v), and 大学生/四年生 in blank(xi); retain both published alternatives even though word-bank use can distinguish them.'},
        ],
        'choiceBoundaries': [
            'Q1 required five-link task is one card10. Foods use any two with descending2+1. Child-age range has separate endpoints1+1; adult price is whole3.',
            'Q2A2 devices use any two with2+1, stickers two2each. Q2B is one any-five-of-six pool: truth1 and Japanese evidence2 per chosen response. Q2C is one complete13-item pool, choose ten1each, spanning paper6–7. Culture asks two company descriptions2each with no printed model answers.',
            'Q3A1 is third year2 plus high school1. Club description chooses two2each. Q3A4 has four independently priced items3each, including source-verified(iv). Q3A5 is one any-three-of-four pool2each. Negative forms and particles are separate any-five-of-six pools2each.',
            'Q4 is one complete12-blank cloze pool, choose ten4each. Q5 is one eight-response pool, choose five, with independent C4/E4 bands and each expression award capped at its own content award. No aggregate expression assessment.',
            'Listening has29 separate tasks; full multiple-choice alternatives remain. Phone03-4160-9725 has four missing digits4/6/9/2, one mark each, with no conflict between paper and scheme.',
            'General reading wrong-language half credit applies before all26 reading tasks; listening named Japanese/romaji/script half credit applies before all29 listening tasks. No writing language penalty or extraneous-material condition is printed.',
            'Preserve every original24 written and four aural Atlas identity, page and source crop. Correct upper scheme page bounds17→16 and append the omitted Q5 expression bands on scheme11 without replacing the original scheme10 crop. Unshipped legacy candidates Q2B(ii) and Q3A4(iv) must be source-verified, never restored from legacy alone.',
        ],
    }


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2021-ol-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
