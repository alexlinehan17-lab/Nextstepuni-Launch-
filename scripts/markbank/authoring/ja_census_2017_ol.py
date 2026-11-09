#!/usr/bin/env python3
"""Independent 2017 Ordinary inventory after all forty original pages were viewed.

No card output or parser is read. Complete required pools and tables stay whole.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2017-ol-000-paper.pdf', '9922a1801afe3fb3647800e0d09bac6c079a59f3f7fb5a40e6aed4bf8b738bf2'),
    ('aural', 'examiner-reports/japanese/papers/2017-ol-A00-paper.pdf', '3918ea5765a059289b06f22201c958a6a876369edb66b62eec976018288864ce'),
    ('scheme', 'examiner-reports/japanese/schemes/2017-ol.pdf', 'bd72510e1ac85538e0c4fca9c479ec95ce3edec7255e00421e65243420b662af'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058GLP{"A00" if component == "aural" else "000"}EV.pdf', 'questionNumber': str(atlas)}})


def build():
    for q, marks in enumerate([10, 6, 4, 4], 1):
        task('1', q, marks, 3, [5], q)
    task('1', 5, 6, 3, [5], 5, 'i')
    task('1', 5, 2, 3, [5], 5, 'ii')
    for q, marks in enumerate([3, 4, 3], 1):
        task('2A', q, marks, 5, [6], q + 5)
    for roman in ['i', 'ii']:
        task('2A', 4, 3, 5, [6], 9, roman)
    task('2B', None, 15, 5, [6], 10)
    task('2C', None, 10, 6, [6], 11)
    task('2D', None, 4, 7, [7], 20)
    for q in [1, 2]:
        task('3A', q, 2, 9, [7], q + 11)
    for roman in ['i', 'ii', 'iii', 'iv']:
        task('3A', 3, 3, 9, [7], 14, roman)
    for roman, marks in zip(['i', 'ii', 'iii'], [2, 3, 2]):
        task('3A', 4, marks, 9, [7], 15, roman)
    for q in [1, 2]:
        task('3B', q, 10, 10, [8], q + 15)
    task('4', None, 30, 11, [9], 18)
    task('5', None, 50, 12, [9, 10], 19)
    for section, questions, pp, sp, atlas in [
        ('LA', [(1, [3, 4, 4]), (2, [2, 4, 4]), (3, [3, 4])], 2, 3, 1),
        ('LB', [(1, [4, 4, 4, 4, 4]), (2, [4, 4])], 3, 3, 2),
        ('LC', [(1, [4, 4]), (2, [4, 4]), (3, [4, 4])], 4, 4, 3),
        ('LD', [(1, [4, 4, 4]), (2, [2, 2, 4])], 5, 4, 4),
    ]:
        for q, marks in questions:
            for roman, mark in zip(['i', 'ii', 'iii', 'iv', 'v'], marks):
                task(section, q, mark, pp, [sp], atlas, roman)
    assert len(TASKS) == 54
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 80, 'listening': 100, 'total': 300}, totals
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2017, 'level': 'ol', 'reviewedAt': '2026-11-09',
            'method': 'Independent full visual sweep of all sixteen written, eight aural and sixteen scheme physical pages before authoring. Required pools and tables stay whole; separately priced responses retain source boundaries.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'candidateMaximum': {'written': 200, 'listening': 100, 'total': 300,
                                 'writingChoice': 'Answer all five written questions. Q4 requires all ten cloze answers; Q5 chooses five of seven responses.'},
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 17)), [
                    'cover: written200, answer all five questions',
                    'Q1 Oricon webpage: eight links, three six-category menus, four concerts and ticket-sale date',
                    'Q1 five-link required pool, choose-three singles genres, two required album categories, choose-two film genres, two-event table and ticket question',
                    'Q2 original Mango ChaCha, Onigirazu and Melon Pan Ice food passages and vocabulary',
                    'Q2A five questions including choose-two ingredients and choose-one occasion/reason; Q2B five required truth/Japanese-evidence pairs',
                    'Q2C all ten required kanji meanings with full Irish and English distractors',
                    'Q2D two challenges associated with Japanese food/culture, no printed model answers',
                    'Q3 Jack email with dates, classes, teacher, trips and gifts, with vocabulary',
                    'Q3A six separately priced English tasks and three separate Japanese tasks',
                    'Q3B five required negative forms and five required particle selections',
                    'Q4 ten-blank birthday cloze, full word bank and use-once direction',
                    'Q5 seven hobby questions, choose five; actual final prompt asks other hobby; full vocabulary',
                    'explicit blank', 'explicit blank', 'explicit blank', 'explicit blank back cover'])),
                'aural': dict(zip(map(str, range(1, 9)), [
                    'cover: listening100, answer all questions in English',
                    'A eight summer-holiday tasks and all multiple-choice options',
                    'B seven news tasks, four-blank phone and complete multiple-choice options',
                    'C six school-reception tasks and complete multiple-choice options',
                    'D six restaurant tasks; second English heading misnumbered(iv), Irish and scheme2, all complete options',
                    'explicit blank', 'explicit blank', 'explicit blank back cover'])),
                'scheme': dict(zip(map(str, range(1, 17)), [
                    'cover', 'general examiner guidance',
                    'listening half credit for Japanese/romaji/script; A28 and B28, phone1permissingnumber4',
                    'C24 and D20 listening answers',
                    'reading appropriate-language half credit; Q1 total32; table heading8 conflicts with six explicit1-mark components',
                    'Q2A16 with namedJapanese half credit; Q2B15 truth1/evidence2 each; Q2C10 meanings1each',
                    'Q2D two points2each; Q3A23 complete answers including start/end time1each and returnmonth/day1each',
                    'Q3B two required five-item grammar pools10each',
                    'Q4 ten cloze answers3each; Q5 choose-five C5/E5 and content bands1/2–3/4–5; final prompt restatement differs from paper',
                    'Q5 expression bands1/2–3/4–5 and Ecap3 when content<=3, exact guidance and global-language note',
                    'tapescript A', 'tapescript B and C first two conversations',
                    'tapescript C continuation and D', 'explicit blank', 'explicit blank', 'back cover'])),
            },
            'sourceDiscrepancies': [
                {'taskKey': ['1', 5, None, 'i'], 'paperPages': [3], 'schemePages': [5],
                 'evidence': 'Q1.5(i) heading says8 marks, but both events have day1, month1 and weekday1, six explicit components total6. The other Q1 tasks total26, so the component total agrees with Q1 heading32. Retain all six printed one-mark components and disclose the8-versus6 difference; no invented extra marks.'},
                {'taskKey': ['5', None, None, None], 'paperPages': [12], 'schemePages': [9],
                 'evidence': 'Paper(vii) asks 他のしゅみは何ですか。 The scheme restates もう一つのしゅみがほしいですか。何をしたいですか。 (wanting another hobby and what one would like to do). Preserve all seven actual paper prompts and common5content/5expression tariff; disclose the different final prompt without inventing a replacement.'},
                {'taskKeys': [['LD', 2, None, roman] for roman in ['i', 'ii', 'iii']], 'paperPages': [5], 'schemePages': [4],
                 'evidence': 'The English At the restaurant heading is misnumbered(iv), while the facing Irish heading and the scheme number it2. Its three roman prompts match by full wording and order; canonicalQ2 follows the paired printed heading and preserves the literal English heading with a visible note.'},
            ],
            'choiceBoundaries': [
                'Q1 five required links2each stay one task10. Choose-three singles genres and choose-two film genres retain all six options. Required categoriesc/d2each stay one task4. Two-event table has six explicitly priced1-mark components, despite heading8; no division of the discrepant heading.',
                'Q2A chooses two ingredients2each, one occasion3 and one reason3. Q2B requires all five truth1/evidence2 pairs. Q2C requires all ten meanings1each. Q2D permits two culture points2each with no model answers or discretionary mark.',
                'Q3A four multiple choices3each are separately priced; three Japanese tasks remain separate. Start/end times and returnmonth/day retain1each; culture answer has total3 without an invented per-item split. Each grammar pool requires all five answers2each.',
                'Q4 is the complete ten-blank cloze3each, word bank used once. Q5 chooses five of seven independent C5/E5 responses; each response expression cap3 applies when that response content<=3. No inherited name/age/discretionary allocation. Actual final paper prompt remains despite different scheme restatement.',
                'Listening27 tasks A8/B7/C6/D6. Phone011-547-1929 has four missing digits5,7,9,2, each1; all given digits unpriced. D1 and D2 prompts retained despite English heading misnumbering.',
                'Reading appropriate-language half credit applies to all25 reading tasks; Q2A additionally names Japanese. Listening namedJapanese/romaji/script half credit applies to all27 listening tasks. No writing-language or extraneous-material reduction printed.',
                'Preserve all twenty original written and four aural Atlas identities/labels/crops. Scheme upper bound17→16 only.',
            ]}


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2017-ol-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
