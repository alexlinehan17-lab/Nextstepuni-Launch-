#!/usr/bin/env python3
"""Independent visual census of all 52 physical pages, before authoring.

Task boundaries and tariffs come from the originals; this module reads no cards.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2023-hl-000-paper.pdf', 'c67da4e231677defa459f6e4989a291d9d68ca8375dbdc59edd159c2392c9aab'),
    ('aural', 'examiner-reports/japanese/papers/2023-hl-A00-paper.pdf', 'd7b4c83a1a8140baea8f11a586f3b8921002bac161c8850ff369f2cba0832ce2'),
    ('scheme', 'examiner-reports/japanese/schemes/2023-hl.pdf', 'be69f009c1fda57635c653bc07ccff23c88fa8be5fc3816da8ad7383f782a5ce'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None, letter=None):
    component = 'aural' if section.startswith('L') else 'paper'
    item = {'key': [section, q, letter, roman], 'marks': marks, 'component': component,
            'paperPages': [pp], 'schemePages': sp,
            'atlas': {'fileid': f'LC058ALP{"A00" if component == "aural" else "000"}BV.pdf', 'questionNumber': str(atlas)}}
    if roman and letter:
        item['paperRef'] = f'2023 HL Section {section}' + (f' Q{q}' if q is not None else '') + f'({roman})({letter})'
    TASKS.append(item)


def build():
    for q, marks in enumerate([6, 2, 2, 1, 2, 2, 1, 6], 1):
        task('1A', q, marks, 3, [7], q)
    for q, marks in enumerate([3, 3, 2], 1):
        task('1B', q, marks, 4, [8], q + 8)
    task('2A', 1, 10, 7, [8], 12)
    for roman in ['i', 'ii', 'iii']:
        task('2A', 2, 2, 7, [9], 13, roman)
    for roman in ['i', 'ii', 'iii', 'iv', 'v']:
        task('2A', 3, 2, 7, [9], 14, roman)
    task('2A', 4, 4, 7, [9], 15)
    task('2B', 1, 5, 8, [10], 16)
    task('2B', 2, 5, 8, [10], 17)
    task('2C', 1, 5, 9, [10], 18)
    task('2C', 2, 5, 9, [11], 19)
    for q, marks in enumerate([3, 4, 1, 2, 2], 1):
        task('3A', q, marks, 11, [11], q + 19)
    for q in range(1, 5):
        task('3B', q, 2, 11, [12], q + 24)
    task('3C', None, 10, 12, [12], 29)
    task('3D', None, 10, 12, [12], 30)
    task('4', None, 40, 14, [13, 14, 15], 31)
    task('5', None, 60, 16, [16, 17, 18], 32)
    for q in [1, 2, 3]:
        task('LA', q, 6, 2, [3], 1)
    for roman, letter, marks in [('i', None, 1), ('ii', None, 3), ('iii', 'a', 1), ('iii', 'b', 3), ('iv', 'a', 1), ('iv', 'b', 1), ('v', None, 3)]:
        task('LB', 1, marks, 3, [4], 2, roman, letter)
    for roman in ['i', 'ii']:
        task('LB', 2, 3, 3, [4], 2, roman)
    for q, allocations in [(1, [4, 3]), (2, [2, 4, 2]), (3, [3, 3])]:
        for roman, marks in zip(['i', 'ii', 'iii'], allocations):
            task('LC', q, marks, 4, [5], 3, roman)
    for roman, letter, marks in [('i', None, 3), ('ii', None, 2), ('iii', None, 3), ('iv', 'a', 2), ('iv', 'b', 2), ('v', None, 2), ('vi', None, 2), ('vii', None, 2), ('viii', None, 3), ('ix', None, 1)]:
        task('LD', None, marks, 5, [6], 4, roman, letter)
    assert len(TASKS) == 67, len(TASKS)
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}, totals
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2023, 'level': 'hl', 'reviewedAt': '2026-11-09',
            'method': 'Independent visual sweep of all 20 written, eight listening and 24 scheme physical pages before authoring. Complete printed tasks and published tariffs counted directly from originals; no generated card data read.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 21)), ['cover', 'Q1A Big Echo source website and offers', 'Q1A matching, six comprehension asks and branch table', 'Q1B three customer comments and three responses', 'explicit blank', 'Q2 original Terunofuji/Shimizu profiles and vocabulary', 'Q2A required profile table, three Japanese and five English responses, translation', 'Q2B two any-five-of-six kanji pools', 'Q2C two any-five-of-six grammar pools', 'Q3 Anna school blog and vocabulary', 'Q3A five English and Q3B four Japanese responses', 'Q3C paired reading/meaning any-five pool and Q3D any-ten-of-twelve particle blanks', 'explicit blank', 'Q4 same-grid choice of three prompts, printed minimum200characters', 'writing grid', 'Q5 any-four-of-eight trip headings, printed minimum320characters', 'writing grid', 'writing grid', 'writing grid', 'copyright/back cover'])),
                'aural': dict(zip(map(str, range(1, 9)), ['cover and English-answer instructions', 'Part A three numbered teacher profile rows, complete four headings each', 'Part B museum tasks with nested letter responses, phone grid and gift table', 'Part C job ranking table, walking tour and weather pair', 'Part D camp interview with nested morning/afternoon and partial uniform tariff', 'explicit blank', 'explicit blank', 'copyright/back cover'])),
                'scheme': dict(zip(map(str, range(1, 25)), ['cover', 'general examiner guidance', 'listening language rule and Part A three profile rows6each', 'Part B19 including phone3 and three-cell gift table3', 'Part C21 including ranking4 and Saturday2/Sunday1 pair', 'Part D22 with uniform partial1 alternative', 'Q1A22 matching/comprehension/branch table', 'Q1B8 Japanese half-credit and Q2A1 required athlete table10', 'Q2A2 Japanese6 extraneous-material half-credit; Q2A3 English10 and translation4', 'Q2B two kanji pools5each and Q2C1 negative pool5', 'Q2C2 conjugation5 and Q3A English12', 'Q3B Japanese8, Q3C paired kanji10 mislabelledB, Q3D particles10 mislabelledC', 'Q4 three prompts C20/E20 with opening/closing', 'Q4 expression lower thresholds and first/middle bands', 'Q4 middle-band continuation and top band, holistic expression note', 'Q5 any-four headings7each and discretionary2, C30/E30', 'Q5 expression lower thresholds and first/middle bands', 'Q5 middle-band continuation and top band, holistic expression note', 'recording transcript Part A', 'recording transcript Part B', 'recording transcript Part C', 'recording transcript Part D', 'blank', 'back cover'])),
            },
            'sourceDiscrepancies': [
                {'paperPages': [8], 'schemePages': [10], 'taskKey': ['2B', 1, None, None], 'evidence': 'Paper fourth kanji入学 is labelled(vi), repeated on sixth話す; source crop confirms the printed error. Keep all six original labels in the whole pool; match fourth answer enter/start school and sixth speak/talk by the kanji, not duplicate labels.'},
                {'paperPages': [3], 'schemePages': [7], 'taskKey': ['1A', 1, None, None], 'evidence': 'Matching item(vi) is Request ranking on paper; scheme labels the same answer6 This month’s news. Keep the paper wording and its printed answer6, which matches the source website ranking link.'},
                {'paperPages': [12], 'schemePages': [12], 'evidence': 'Paper Q3C Kanji and Q3D Grammar appear under repeated scheme headings B/C. Match the identical items and tariffs, retaining paper C/D references.'},
                {'paperPages': [14], 'schemePages': [14], 'taskKey': ['4', None, None, None], 'evidence': 'Paper minimum is200characters; scheme lower-expression condition explicitly uses less than150characters or content10orless. Display both source instructions exactly, without substituting the paper minimum into the grading rule.'},
                {'paperPages': [16], 'schemePages': [17], 'taskKey': ['5', None, None, None], 'evidence': 'Paper minimum is320characters; scheme lower-expression condition explicitly uses less than200characters or content15orless. Keep both, with source-bound grading threshold.'},
            ],
            'choiceBoundaries': [
                'Q1A1 one required six-cell matching task; Q1A8 one required two-branch table, exit1 and any-two details1each for each branch. Q2A1 one required two-athlete table with origin1, description2 and hobbies2 per athlete.',
                'Q1A2/5/6 any-two details1each; Q1B1/2 descending2+1, Q1B3 any-two1each. Q1A3 family discount is two separately claimable1-mark components, not alternative total2 routes.',
                'Q2B1/2 and Q2C1/2 four complete any-five-of-six pools1each. Q3C one any-five-of-six pool, each reading1 plus meaning1. Q3D one any-ten-of-twelve blanks across seven sentences; sentenceiii second blank accepts ga/wa.',
                'Q2A3ii right leg2 versus leg1 is one response with a capped partial-credit alternative. Q3A2 total4 retains circumstances2 plus confiscation1 and one-week consequence1; the printed slash does not create a fourth bonus route.',
                'Q4 one same-grid choice of three prompts: two content9 plus opening1/closing1 and E20; lowerE15 atC<=10 or fewer than150characters. Q5 one composition any-four-of-eight content7each plus discretionary2 and E30; lowerE20 atC<=15 or fewer than200characters. Neither writing task carries an invented language penalty.',
                'Listening A keeps three complete numbered profile rows6each, matching independent Claire/Ben/Pam recordings; required time/place/positive/negative headings do not fan out. All internal positive/negative pools stay any-two1each.',
                'Listening B has nine separately priced tasks. Its gift table remains one3-mark task, phone one whole3-mark number without a fabricated per-digit allocation. Four roman-then-letter tasks preserve the printed order.',
                'Listening C has seven tasks. Ranking table one4-mark task; Saturday/Sunday are required headings inside C3i, one3-mark response retaining Saturday any-two1each and Sunday1. No fan-out of required headings.',
                'Listening D has ten tasks, including two separately priced morning/afternoon letter responses. Uniform any-two details uses descending2+1, with distinct source alternative three correct colours1; cap at3 and do not award the partial alternative in addition.',
                'Language half credit is source-scoped to29 listening tasks physicalp3 andthree Q1B tasks p8, explicitly Japanese. Onlythree Q2A2 Japanese responses p9 have extraneous-material half credit. No general reading, Q3B or writing language/extraneous rule is printed.',
                'Original Atlas anchors1–32written and1–4listening retained, including original multi-page writing expression regions.',
            ]}


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2023-hl-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
