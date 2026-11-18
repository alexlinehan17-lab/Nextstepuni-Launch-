#!/usr/bin/env python3
"""Independent 2019 Higher inventory after all 48 original pages were viewed.

No cards or authored manifests are read. Required pools and tables are whole
tasks; separate published tariffs retain their source boundaries.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2019-hl-000-paper.pdf', 'c1127796075df825e5e7e676529d14e9ab3d9db3b9dae7a909e9e91abd6653c1'),
    ('aural', 'examiner-reports/japanese/papers/2019-hl-A00-paper.pdf', '6b36a5c5ab891adf5c9ed0634f559d19cc08ef9699f6a658dbb6d44023cc95e4'),
    ('scheme', 'examiner-reports/japanese/schemes/2019-hl.pdf', '272b8bc5bc9e6fd7adcb43a02abed17768cc0c35e02fce8b6271e00da3fc525c'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None, letter=None):
    component = 'aural' if section.startswith('L') else 'paper'
    item = {'key': [section, q, letter, roman], 'marks': marks, 'component': component,
            'paperPages': [pp], 'schemePages': sp,
            'atlas': {'fileid': f'LC058ALP{"A00" if component == "aural" else "000"}BV.pdf', 'questionNumber': str(atlas)}}
    if roman and letter:
        item['paperRef'] = f'2019 HL Section {section}' + (f' Q{q}' if q else '') + f'({roman})({letter})'
    TASKS.append(item)


def build():
    task('1A', 1, 6, 3, [7], 1)
    for q, marks in [(2, [1, 2]), (3, [1, 1]), (5, [4, 1, 1])]:
        for roman, mark in zip(['i', 'ii', 'iii'], marks):
            task('1A', q, mark, 3, [7], q, roman)
    task('1A', 4, 1, 3, [7], 4)
    for q in [1, 2, 3]:
        for roman in ['i', 'ii']:
            task('1B', q, 2, 4, [8], q + 5, roman)
    task('2A', 1, 8, 7, [8], 9)
    for roman in ['i', 'ii', 'iii']:
        task('2A', 2, 2, 7, [8], 10, roman)
    for roman, marks in zip(['i', 'ii', 'iii', 'iv'], [4, 3, 2, 2]):
        task('2A', 3, marks, 7, [9], 11, roman)
    task('2A', 4, 5, 7, [9], 12)
    for q in [1, 2]:
        task('2B', q, 5, 8, [9], 12 + q)
        task('2C', q, 5, 9, [10], 14 + q)
    for q in [1, 2, 3, 4]:
        for roman in ['i', 'ii']:
            task('3A', q, 2, 11, [10] if q < 4 else [11], 16 + q, roman)
        task('3B', q, 1, 11, [11], 20 + q)
    task('3C', None, 10, 12, [11], 25)
    task('3D', None, 10, 12, [11], 26)
    task('4', None, 40, 14, [12, 13], 27)
    task('5', None, 60, 16, [14, 15], 28)
    task('LA', None, 18, 2, [4], 1)
    for q, marks in [(1, [2, 3, 3, 4, 3]), (2, [3, 2, 3])]:
        for roman, mark in zip(['i', 'ii', 'iii', 'iv', 'v'], marks):
            task('LB', q, mark, 3, [4] if q == 1 else [5], 2, roman)
    for q, marks in [(1, [4, 2, 4, 4]), (2, [2, 3, 2])]:
        for roman, mark in zip(['i', 'ii', 'iii', 'iv'], marks):
            task('LC', q, mark, 4, [5], 3, roman)
    for roman in ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']:
        if roman in ['ii', 'v']:
            for letter in ['a', 'b']:
                task('LD', None, 2, 5, [6], 4, roman, letter)
        else:
            task('LD', None, 2, 5, [6], 4, roman)
    assert len(TASKS) == 69, len(TASKS)
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}, totals
    assert sum(t['key'][0][0] in '123' for t in TASKS) == 42
    assert sum(t['component'] == 'aural' for t in TASKS) == 25
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2019, 'level': 'hl', 'reviewedAt': '2026-11-09',
            'method': 'Independent full visual sweep of all 20 written, eight aural and 20 scheme physical pages before authoring. Required pools and tables remain whole tasks; separately priced responses retain their source boundaries.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'candidateMaximum': {'written': 220, 'listening': 80, 'total': 300,
                                 'writingChoice': 'The original paper requires all five questions. Q4 chooses one of two 40-mark presentation prompts; Q5 is a 60-mark email covering any four of six headings.'},
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 21)), [
                    'cover: written220, answer all five questions',
                    'Q1A original Tokyo Paralympic website links, historical sport table, event facts and vocabulary',
                    'Q1A required six-link task and eight separately priced responses',
                    'Q1B three original athlete profiles, photographs and six separately priced responses',
                    'explicit blank',
                    'Q2 original Japanese uniform history, summer/winter changes, survey and CONOMI awards; pictures and underlined translation',
                    'Q2A required uniform table, three Japanese responses, four English responses and translation',
                    'Q2B five required meanings and five required hiragana readings',
                    'Q2C five required past forms and five required verb forms, original underlines',
                    'Q3 original Dara diary with four dated entries, photographs and vocabulary',
                    'Q3A eight English and Q3B four Japanese responses',
                    'Q3C five required reading/meaning pairs; Q3D ten required particle blanks across seven sentences',
                    'explicit blank',
                    'Q4 one of two presentations about holiday or party, approximately200 characters, two content prompts each',
                    'Q4 answer grid',
                    'Q5 email to visiting Japanese friend, approximately320 characters, any four of six headings',
                    'Q5 answer grid', 'Q5 answer grid', 'additional answer grid', 'explicit blank back cover'])),
                'aural': dict(zip(map(str, range(1, 9)), [
                    'cover: listening80, answer all questions in English',
                    'Part A one required three-club/four-column table',
                    'Part B Hotel Okura five tasks and Kyoto weather three tasks, including whole phone grid',
                    'Part C Yoshiko and mother: four morning tasks, three lunchtime tasks',
                    'Part D Yuri and Kenta: nine separately priced tasks, with letters nested under(ii) and(v)',
                    'explicit blank', 'explicit blank', 'explicit blank back cover'])),
                'scheme': dict(zip(map(str, range(1, 21)), [
                    'cover', 'general examiner guidance', 'internal Higher cover',
                    'listening Japanese/romaji/script half-credit rule; Part A18 complete table and Part B1 hotel15',
                    'Part B2 weather8; Part C21 with sickness-zero instruction and printed partial components',
                    'Part D18, nine priced tasks including Languages-only1 partial and encouragement1+1',
                    'Q1A18: all six links, exact dated-event2+2 and other response tariffs; scheme repeats3(ii)',
                    'Q1B12 local Japanese half credit and sister-only1 partial; Q2A table8 and three Japanese responses6 with extraneous-material rule only',
                    'Q2A3 English11, translation5, Q2B five meanings/five readings10; no language penalty printed here',
                    'Q2C required grammar10, Q3A first six responses12; diary question called blog in scheme',
                    'Q3A last two responses4, Q3B four Japanese answers4, Q3C reading-letter/meaning10 and Q3D ten particles10; grammar mislabelledC and final(vii) repeats(vi)',
                    'Q4 two presentation choices, each two content9 plus opening1/closing1 and expression20',
                    'Q4 exact normal/lower expression bands; cap15 if content<=10 or length<150',
                    'Q5 four headings6 each, opening1/closing1 and four discretionary content marks, expression30',
                    'Q5 exact normal/lower expression bands; cap20 if content<=15 or length<200',
                    'tapescript Part A', 'tapescript Part B', 'tapescript Part C', 'tapescript Part D', 'blank back cover'])),
            },
            'sourceDiscrepancies': [
                {'taskKey': ['1A', 3, None, 'i'], 'paperPages': [3], 'schemePages': [7],
                 'evidence': 'The year question is3(i) in the original paper; the scheme repeats(ii). Retain the actual question identity and its2000 answer1.'},
                {'taskKey': ['3A', 1, None, 'ii'], 'paperPages': [11], 'schemePages': [10],
                 'evidence': 'The paper asks who told Dara to write a diary and why; the scheme calls it a blog. The corresponding teacher1 and writing-practice1 answer is explicit. Preserve the actual paper wording.'},
                {'taskKey': ['3D', None, None, None], 'paperPages': [12], 'schemePages': [11],
                 'evidence': 'The paper labels grammarD and final sentence(vii); the scheme repeatsC and(vi). Preserve the printed paper citation and all ten priced particle blanks.'},
            ],
            'choiceBoundaries': [
                'Q1A1 is one required six-link task,1 each. Date endpoints each carry2, not an invented per-component split. All other separately priced responses remain distinct.',
                'Q1B2(i) older sister earns2; sister alone1. Q1B1(i) sight1 plus left eye1 and Q1B2(ii) bronze1 plus Rio1 remain exact components. Six Q1B tasks carry the local Japanese-half rule.',
                'Q2A table is one task8: each row has three unfilled answer cells; boys and Kyoto Heisei Jogakkuin are printed examples and earn no new marks. Uniform descriptions each allow two details1 each. Required kanji and grammar pools each contain all five items.',
                'Q2A2 extraneous-material half credit applies to three answers. No incorrect-English clause is printed; do not inherit one from another year. No all-paper language or writing penalty is printed.',
                'Q3C five required pairs each carry the correct reading-letter1 plus meaning1; retain all original paper options. Q3D has ten required blanks across seven sentences,1 each, retaining alternatives and correcting only paper/scheme label mismatches.',
                'Q4 one40-mark choice: two content9, opening1, closing1, expression20; lowerE15 if C<=10 or fewer than150 characters. Q5 one60-mark email: four headings6, opening1, closing1, discretionary4, expression30; lowerE20 if C<=15 or fewer than200 characters. Both writing questions are required.',
                'Listening A is one18-mark required table with12 cells. Tuesday1/Thursday1 and every day1/from4to6 one mark are distinct. Third club Monday1/Wednesday1 has a separately printed three-times-a-week1 alternative; do not combine its generic partial with a complete route.',
                'Listening B has eight tasks; north exit1, go straight about five minutes1 and end of road1 are all required. Phone03-3562-9704 is whole3, not per-digit. Listening C has seven tasks, preserves feels-sick-zero, and exact yakiniku1/restaurant1 plus out-with-friend1 partial guidance under its total2.',
                'Listening D has nine tasks; English1+Chinese1 versus generic Languages1 are alternative routes, not additive. Four roman-then-letter tasks retain literal paper references and canonical letter/roman keys. All25 listening tasks carry the namedJapanese/romaji/script half-credit rule.',
                'Preserve all28 original written and four aural Atlas identities, labels, pages and regions. Correct scheme upper bounds21→20, and append a required continuation only if independent source review proves it missing.',
            ]}


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2019-hl-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
