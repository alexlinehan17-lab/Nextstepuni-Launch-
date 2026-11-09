#!/usr/bin/env python3
"""Independent 2019 Ordinary census after viewing every original physical page.

This script reads no authored cards. Required tables and finite pools are each
one task; each separately priced question remains separate.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2019-ol-000-paper.pdf', '00e95d69d8ba77dcdb1e9650678e2120708bbba9fdf9cd1c395845ad11cd38e0'),
    ('aural', 'examiner-reports/japanese/papers/2019-ol-A00-paper.pdf', 'da32fc28efe1458022116587a0b9cf72cff589496459bfdab41457458e752639'),
    ('scheme', 'examiner-reports/japanese/schemes/2019-ol.pdf', 'be1782b438ce07304d7c624fde74c23d533b6f4a3ba0522613b38571d6c4b0f8'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': pp if isinstance(pp, list) else [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058GLP{"A00" if component == "aural" else "000"}BV.pdf',
                            'questionNumber': str(atlas)}})


def build():
    for q, marks in enumerate([10, 3, 2, 3, 6], 1):
        task('1', q, marks, 3, [4], q)
    for roman in ['i', 'ii', 'iii']:
        task('1', 6, 2, 3, [4], 6, roman)
    for q, marks in enumerate([2, 3, 2, 4, 4], 1):
        task('2A', q, marks, 5, [5], q + 6)
    task('2B', None, 15, 5, [5], 12)
    task('2C', None, 10, 6, [5], 13)
    task('2D', None, 5, 7, [6], 21)
    for q, marks in enumerate([2, 3, 3], 1):
        task('3A', q, marks, 9, [6], q + 13)
    for roman in ['i', 'ii', 'iii', 'iv']:
        task('3A', 4, 2, 9, [6], 17, roman)
    task('3A', 5, 9, 10, [6], 18)
    for q in [1, 2]:
        task('3B', q, 10, 10, [7], q + 18)
    task('4', None, 30, 11, [8], 22)
    task('5', None, 50, 12, [8, 9], 23)
    for section, questions, pp, sp, atlas in [
        ('LA', [(1, [2, 4, 4]), (2, [2, 4, 4]), (3, [2, 4])], 2, 10, 1),
        ('LB', [(1, [4, 4, 4, 4, 4]), (2, [4, 4])], 3, 10, 2),
        ('LC', [(1, [4, 4, 4, 4]), (2, [4, 4])], 4, 11, 3),
        ('LD', [(None, [4, 2, 4, 4, 4, 2, 4])], 5, 11, 4),
    ]:
        for q, marks in questions:
            for roman, mark in zip(['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii'], marks):
                task(section, q, mark, pp, [sp], atlas, roman)
    assert len(TASKS) == 56
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 80, 'listening': 102, 'total': 302}, totals
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2019, 'level': 'ol', 'reviewedAt': '2026-11-09',
            'method': 'Independent full visual sweep of all 16 written, eight aural and 16 scheme physical pages before authoring. Complete required pools and tables remain whole; separately priced responses retain actual paper boundaries.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'candidateMaximum': {'publishedWritten': 200, 'publishedListening': 100, 'publishedTotal': 300,
                                 'sumOfLocalTariffs': 302,
                                 'sourceConflict': 'Part B1 heading18 conflicts with five separately printed4-mark answers, totaling20. Part B heading26 conflicts with its local28. Preserve the explicit response tariffs; do not arbitrarily deduct2 from a task.',
                                 'writingChoice': 'The original cover requires all five questions. Q4 is the complete ten-blank cloze30; Q5 chooses five of seven responses50.'},
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 17)), [
                    'cover: written200 and answer all five questions',
                    'Q1 original wear.jp website, ten links, clothing categories and summer fashion-show calendar/prices',
                    'Q1 required five-link task, three separate clothing questions, required two-event table and three separately priced event responses',
                    'Q2 original Hello Kitty collector article, photographs and vocabulary',
                    'Q2A five English responses; Q2B five required truth/evidence pairs',
                    'Q2C ten required kanji meanings with all Irish and English options',
                    'Q2D describe two other popular Japanese characters',
                    'Q3 original Kevin/Sarah/Michael school and college profiles, photographs and vocabulary',
                    'Q3A first three English responses and four separate multiple-choice tasks',
                    'Q3A5 three required Japanese answers; Q3B five required negative forms and five required particles',
                    'Q4 whole birthday cloze, ten blanks, complete word bank and use-each-word-once instruction',
                    'Q5 seven questions about Japanese study, answer any five, all response grids and vocabulary',
                    'explicit blank', 'explicit blank', 'explicit blank', 'explicit blank back cover'])),
                'aural': dict(zip(map(str, range(1, 9)), [
                    'cover: listening100, all questions and English-answer instruction',
                    'Part A eight school-club tasks with complete multiple-choice options',
                    'Part B five hotel tasks including four-blank phone and two weather tasks',
                    'Part C six Yoshiko/mother tasks, morning and lunchtime',
                    'Part D seven Yuri/Kenta tasks and complete multiple-choice options',
                    'explicit blank', 'explicit blank', 'explicit blank back cover'])),
                'scheme': dict(zip(map(str, range(1, 17)), [
                    'cover', 'general examiner guidance', 'Japanese Ordinary2019 title page',
                    'reading appropriate-language half credit and Q1 complete tariff30 including six table components',
                    'Q2A15, Q2B15 truth1/evidence2 per required item, Q2C10 one mark per meaning',
                    'Q2D two descriptions2each plus discretionary1; Q3A25 including three required Japanese answers3each',
                    'Q3B two five-item required grammar pools10each',
                    'Q4 cloze30 with10answers3each; Q5 anyfiveofseven content5/expression5 and content bands',
                    'Q5 expression bands1/2–3/4–5 and global language-use guidance; no content cap printed',
                    'listening Japanese/romaji/script half credit; Parts A26 and B28 (heading26 conflicts with explicit local tariffs); phone1permissingdigit4',
                    'Parts C24 and D24',
                    'tapescript Part A', 'tapescript Part B', 'tapescript Part C', 'tapescript Part D', 'back cover'])),
            },
            'sourceDiscrepancies': [
                {'taskKey': ['LB', 1, None, None], 'paperPages': [3], 'schemePages': [10],
                 'evidence': 'Part B1 heading18 but all five responses explicitly carry4 each, including four missing phone digits1each. This makes B28 instead of its heading26 and listening102 instead of100. Preserve all local tariffs and disclose the aggregate discrepancy; no response is arbitrarily reduced.'},
                {'taskKey': ['4', None, None, None], 'paperPages': [11], 'schemePages': [8],
                 'evidence': 'The scheme accepts shopping/party at(viii) and party at(ix), while the paper says use each word once. Preserve both published alternatives and the one-use instruction; do not award the same party token twice.'},
                {'taskKey': ['LB', 1, None, 'v'], 'paperPages': [3], 'schemePages': [10],
                 'evidence': 'The scheme labels the phone(vi) although the paper prints(v). Match the exact03-3562-9704 grid and its four missing digits5,6,9,7, one mark each.'},
            ],
            'choiceBoundaries': [
                'Q1 five required links2each stay one task10. Clothing pools2 and4 each choose two at2+1. The event table contains six one-mark components: day/date/month for each of two prefilled event titles. Event start and finish are1each.',
                'Q2B is one required five-pair task: truth1 and Japanese evidence2 each. Q2C is one required ten-item meaning pool1each. Q2D asks two character descriptions2each with one discretionary mark; no model character answers are printed.',
                'Q3A2 prices dad1 and car2 separately. Four multiple-choice tasks each2 remain separately priced. Q3A5 is one required three-response pool3each. Each grammar pool requires all five answers2each.',
                'Q4 requires all ten cloze answers3each, using each bank word once. Retain full source alternatives and visible duplicate-token restriction. Q5 chooses five of seven independent responses, each content5/expression5, with separate published bands and no inherited2021 E<=C rule.',
                'Listening has28 separately priced tasks. A8/B7/C6/D7. The original phone grid has exactly four missing digits5,6,9,7, each1; no marks for the given digits.',
                'Reading general appropriate-language half credit is source-bound to all26 reading tasks. Listening named Japanese/romaji/script half credit applies to all28 listening tasks. No writing language reduction or extraneous-material condition is printed.',
                'Preserve all23 original written and four aural Atlas identities, labels, pages and crops. Correct only scheme upper bounds17→16 unless a required continuation is independently shown absent.',
            ]}


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2019-ol-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
