#!/usr/bin/env python3
"""Independent 2018 Ordinary inventory after all forty original pages were viewed.

No card output or parser is read. Complete required pools and tables stay whole.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2018-ol-000-paper.pdf', 'd4350996bef8795c53d2fb0f1e68f763a27bcdb6a4980e30a4ce83127208cef0'),
    ('aural', 'examiner-reports/japanese/papers/2018-ol-A00-paper.pdf', '6f7464db7f617ae9c35aea8f4891b4ec0d7518c2ab5d9e893910b2b4d86c455b'),
    ('scheme', 'examiner-reports/japanese/schemes/2018-ol.pdf', '8140e430a7c93568637fba566e37a27e6928a56eddb2272264b0d93fe195f8a5'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058GLP{"A00" if component == "aural" else "000"}EV.pdf', 'questionNumber': str(atlas)}})


def build():
    for q, marks in enumerate([12, 2, 8, 2, 6, 6], 1):
        task('1', q, marks, 3, [5], 1)
    for q, marks in enumerate([3, 2, 2, 3, 2], 1):
        task('2A', q, marks, 5, [6], 2)
    task('2B', None, 15, 5, [6], 2)
    task('2C', None, 10, 6, [7], 6)
    task('2D', None, 4, 7, [7], 7)
    for q in [1, 2]:
        task('3A', q, 2, 9, [8], 3)
    for roman in ['i', 'ii']:
        task('3A', 3, 2, 9, [8], 3, roman)
    for roman in ['i', 'ii', 'iii']:
        task('3A', 4, 2, 9, [8], 3, roman)
    for q in [1, 2, 3]:
        task('3B', q, 3, 9, [8], 3)
    for q in [1, 2]:
        task('3C', q, 10, 10, [9], 8)
    task('4', None, 30, 11, [10], 4)
    task('5', None, 50, 12, [10, 11], 5)
    for section, questions, pp, sp, atlas in [
        ('LA', [(1, [2, 4, 4]), (2, [2, 4, 4]), (3, [2, 4])], 2, 3, 1),
        ('LB', [(1, [2, 4, 4]), (2, [2, 4, 2]), (3, [4, 4])], 3, 3, 2),
        ('LC', [(1, [2, 4, 4, 4]), (2, [4, 4, 2])], 4, 4, 3),
        ('LD', [(1, [4, 4, 4]), (2, [4, 4, 4])], 5, 4, 4),
    ]:
        for q, marks in questions:
            for roman, mark in zip(['i', 'ii', 'iii', 'iv'], marks):
                task(section, q, mark, pp, [sp], atlas, roman)
    assert len(TASKS) == 57
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 80, 'listening': 100, 'total': 300}, totals
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2018, 'level': 'ol', 'reviewedAt': '2026-11-09',
            'method': 'Independent full visual sweep of all sixteen written, eight aural and sixteen scheme physical pages before authoring. Required pools and tables stay whole; separately priced responses retain source boundaries.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'candidateMaximum': {'written': 200, 'listening': 100, 'total': 300,
                                 'writingChoice': 'Answer all five written questions. Q4 requires all ten cloze answers; Q5 chooses five of seven responses.'},
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 17)), [
                    'cover: written200, answer all five questions',
                    'Q1 Kyoto tourist-guide website: ten links, six events, seven restaurant and seven shopping categories',
                    'Q1 six-link required pool, city, complete event table, night film festival and two choose-three category pools',
                    'Q2 original One Piece/Baby Metal/TV recommendations and vocabulary',
                    'Q2A five questions including one required three-name task; Q2B five required truth/Japanese-evidence pairs',
                    'Q2C all ten required kanji meanings with full Irish and English distractors',
                    'Q2D describe two traditional Japanese culture areas, no printed model answers',
                    'Q3 Kenta blog entries April29/May2/May3/May4 with vocabulary',
                    'Q3A seven separately priced English tasks; Q3B three separate Japanese questions',
                    'Q3C five required past-tense forms and five required particle selections',
                    'Q4 ten-blank cloze, full word bank and use-once direction',
                    'Q5 seven friend questions, choose five; first prompt asks name and age; full vocabulary',
                    'explicit blank', 'explicit blank', 'explicit blank', 'explicit blank back cover'])),
                'aural': dict(zip(map(str, range(1, 9)), [
                    'cover: listening100, answer all questions in English',
                    'A eight phone-survey tasks and all multiple-choice options',
                    'B eight news tasks, four-blank phone and complete multiple-choice options',
                    'C seven travel tasks and complete multiple-choice options',
                    'D six exam-conversation tasks and complete multiple-choice options',
                    'explicit blank', 'explicit blank', 'explicit blank back cover'])),
                'scheme': dict(zip(map(str, range(1, 17)), [
                    'cover', 'general examiner guidance',
                    'listening half credit for Japanese/romaji/script; A26 and B26 with iPhone1+8model1, phone1permissingnumber4, typhoon4/wind2',
                    'C24 and D24 listening answers',
                    'reading appropriate-language half credit; Q1 total36 with complete tariffs and date/day components',
                    'Q2A12 with three required names1each and Baby Metal choose-two ladder2+1; Q2B15 truth1/evidence2 each',
                    'Q2C ten meanings1each; Q2D two points2each, no discretionary mark',
                    'Q3A14 and Q3B9 complete source answers',
                    'Q3C two required five-item grammar pools10each',
                    'Q4 ten cloze answers3each; Q5 choose-five C5/E5, first response name2+age2+discretionary1, content bands1/2–3/4–5; source restates likes atiii and repeats age ativ, omitting the actual do-together prompt',
                    'Q5 expression bands1/2–3/4–5 and Ecap3 when content<=3, exact guidance and global-language note',
                    'tapescript A', 'tapescript A continuation and B', 'tapescript C and D before-exams start',
                    'tapescript D remainder and after exams', 'back cover'])),
            },
            'sourceDiscrepancies': [
                {'taskKey': ['5', None, None, None], 'paperPages': [12], 'schemePages': [10],
                 'evidence': 'The paper asks do-together(iii) and likes(iv). The scheme restates likes at(iii), then repeats age at(iv), already asked in(i), omitting do-together from its prompt restatement. Retain all seven actual paper prompts and the explicit common5content/5expression tariff; visibly disclose the restatement mismatch without inventing a replacement age question.'},
            ],
            'choiceBoundaries': [
                'Q1 six required links2each stay one task12. The two-event table is one task8, with day/date1+month1 and weekday2 for each event. Night1 and film festival1 are independent. Each category pool chooses three of seven2each; Kimono/yukata is one printed shopping category.',
                'Q2A1 is one required three-name task1each. Q2A4 chooses two of three band members with printed2+1 descending tariff. Q2B requires all five truth1/evidence2 pairs. Q2C requires all ten meanings1each. Q2D permits two culture points2each; do not inherit2019 discretionary1.',
                'Q3A mother/father and multiple choices are separately priced. Three Japanese answers each3 remain separate. Each grammar pool requires all five answers2each.',
                'Q4 is the complete ten-blank cloze3each. Q5 chooses five of seven independent C5/E5 responses; first response has name2, age2 and discretionary1. Each response expression cap3 applies when that response content<=3. No inferred cap on another selected response.',
                'Listening29 tasks A8/B8/C7/D6. iPhone1 and model8 number1 are separate printed components. Phone03-3573-8205 has four blank digits5,7,8,2, each1; all given digits unpriced. Typhoon4/wind2 is a mutually exclusive full/partial answer, no score2+4.',
                'Reading appropriate-language half credit applies to all26 reading tasks; listening namedJapanese/romaji/script half credit applies to all29 listening tasks. No writing-language or extraneous-material reduction printed.',
                'Preserve all eight original written and four aural Atlas identities/labels/crops. Scheme upper bound17→16 only.',
            ]}


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2018-ol-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
