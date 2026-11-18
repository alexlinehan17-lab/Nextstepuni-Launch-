#!/usr/bin/env python3
"""Independent 2021 Higher census after a full 48-page visual sweep.

No authored cards or generated manifests are read. Whole tables and finite
pools remain complete tasks; separately priced answers retain their boundaries.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2021-hl-000-paper.pdf', '906c9dc00db6e0b4f0ad0b7f63403046bad7533a09aa57a0f51767b9124e96fd'),
    ('aural', 'examiner-reports/japanese/papers/2021-hl-A00-paper.pdf', '760082f066675ec3cf2f60c9839dce035c2d0229eadf25450704ba79794efc7c'),
    ('scheme', 'examiner-reports/japanese/schemes/2021-hl.pdf', 'e9fb692a2c1046ef9c23e0a93a2334536885dc67ab5bb10298923cd51d462b7e'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058ALP{"A00" if component == "aural" else "000"}BV.pdf',
                            'questionNumber': str(atlas)}})


def build():
    for q, marks in enumerate([5, 8, 2, 2, 2], 1):
        task('1A', q, marks, 3, [7], q)
    for roman in ['i', 'ii']:
        task('1A', 6, 2, 3, [7], 6, roman)
    for q, marks in enumerate([2, 3, 2, 2], 1):
        task('1B', q, marks, 4, [8], q + 6)
    task('2A', 1, 10, 7, [8], 11)
    for roman in ['i', 'ii', 'iii']:
        task('2A', 2, 2, 7, [8], 12, roman)
    for roman, marks in zip(['i', 'ii', 'iii', 'iv'], [2, 1, 3, 3]):
        task('2A', 3, marks, 7, [9], 13, roman)
    task('2A', 4, 5, 7, [9], 14)
    task('2B', 1, 5, 8, [9], 24)
    task('2B', 2, 5, 8, [10], 24)
    for q in [1, 2]:
        task('2C', q, 5, 9, [10], 25)
    for q, marks in enumerate([2, 2, 3, 3, 2], 1):
        task('3A', q, marks, 11, [11], q + 14)
    for q, marks in enumerate([1, 2, 1, 2], 1):
        task('3B', q, marks, 11, [11], q + 19)
    task('3C', None, 10, 12, [12], 26)
    task('3D', None, 10, 12, [12], 27)
    task('4', None, 50, 14, [13, 15], 28)
    task('5', None, 50, 16, [14, 15], 29)
    task('LA', None, 21, 2, [3], 1)
    for roman, marks in zip(['i', 'ii', 'iii', 'iv', 'v'], [2, 3, 2, 3, 2]):
        task('LB', 1, marks, 3, [4], 2, roman)
    task('LB', 2, 8, 3, [4], 2)
    for section, marks, pp, sp, atlas in [
        ('LC', [2, 4, 2, 2, 2, 3, 4], 4, 5, 3),
        ('LD', [2, 2, 4, 4, 2, 3, 3], 5, 6, 4),
    ]:
        for roman, mark in zip(['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii'], marks):
            task(section, None, mark, pp, [sp], atlas, roman)
    assert len(TASKS) == 58
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'),
        ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}, totals
    assert sum(t['key'][0][0] in '123' for t in TASKS) == 35
    assert sum(t['component'] == 'aural' for t in TASKS) == 21
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {
        'subjectId': 'japanese', 'year': 2021, 'level': 'hl', 'reviewedAt': '2026-11-09',
        'method': 'Independent full visual sweep of all 20 written, eight aural and 20 scheme physical pages before authoring. Whole tables and finite answer pools count once; every separately priced response remains represented.',
        'sources': sources, 'tasks': TASKS, 'checksums': totals,
        'candidateMaximum': {'written': 170, 'listening': 80, 'total': 250,
                             'writingChoice': 'The adjusted paper requires either Q4 or Q5, not both. Both 50-mark writing tasks remain offered practice.'},
        'pageRoles': {
            'paper': dict(zip(map(str, range(1, 21)), [
                'cover; adjusted written maximum170; Q1–3 and either Q4 or Q5',
                'Q1A original Mercari shop screenshot with eight links, all products, categories and brands',
                'Q1A six-link pool; full two-item table; three short answers and two separately priced category/brand asks',
                'Q1B three original user comments, vocabulary and four English responses',
                'explicit blank',
                'Q2 original Rachel and Jun article with photographs, underlined translation and vocabulary',
                'Q2A complete two-person table, three Japanese responses, four English responses and whole translation',
                'Q2B two separate any-five-of-six kanji pools',
                'Q2C two separate any-five-of-six grammar pools with all prompts and examples',
                'Q3 original Peter shared-accommodation interview, photograph and vocabulary',
                'Q3A five English responses and Q3B four Japanese responses',
                'Q3C six paired readings/translations, choose five; Q3D twelve particle blanks, choose ten',
                'explicit blank',
                'Q4 one50-mark writing task with three complete alternatives; minimum200Japanese characters',
                'Q4 response grid',
                'Q5 one50-mark school-memories essay; anyfour of eight full headings; minimum320Japanese characters',
                'Q5 response grid', 'Q5 response grid', 'Q5 response grid', 'back cover; explicit blank'])),
            'aural': dict(zip(map(str, range(1, 9)), [
                'cover; listening maximum80; answer in English',
                'Part A complete three-person table: age, hobbies, reason and learning method',
                'Part B five Naomi Watanabe responses and complete two-day weather/advice table',
                'Part C seven robot-restaurant responses including complete phone grid and required route',
                'Part D seven school-exchange responses', 'explicit blank', 'explicit blank', 'back cover; explicit blank'])),
            'scheme': dict(zip(map(str, range(1, 21)), [
                'cover', 'general examiner guidance',
                'listening Japanese/romaji/script half credit; full Part A table21, every cell and Sophie partial1/2',
                'Part B20: five responses12 and weather/advice table8, all descending tariffs',
                'Part C19: seven responses; phone whole3; east exit1 required plus other two details2+1',
                'Part D20: seven responses; cat1 plus anytwo description details1each',
                'Q1 general wrong-language half credit; A23: five-of-six link pool5, full item table8 and local tariffs',
                'Q1B Japanese half credit9; Q2 general wrong-language half credit; full table10; three Japanese responses2each with extraneous-material half credit',
                'Q2A four English responses9 and translation5; first five-of-six kanji pool5',
                'second kanji pool5; two separate five-of-six grammar pools5each, all alternatives',
                'Q3 general wrong-language half credit; five English responses12 and four Japanese responses6 with all partial details',
                'Q3C paired reading/translation pool10 and Q3D twelve-blank pool10; scheme headings B/C disagree with paper C/D',
                'Q4 chooseone of three alternatives; content21+opening1+closing1+discretionary2, expression25',
                'Q5 choosefour of eight headings5each+opening1+closing1+discretionary3, expression25',
                'common expression bands; C<=13 or length<150 lowers expression maximum25to19',
                'tapescript Part A', 'tapescript Part B', 'tapescript Part C', 'tapescript Part D', 'back cover'])),
        },
        'sourceDiscrepancies': [
            {'taskKey': ['1A', 1, None, None], 'paperPages': [3], 'schemePages': [7],
             'evidence': 'Paper presents six links without a choose-five instruction. Adjusted scheme explicitly credits anyfive, maximum5. Preserve allsix prompts with visible source choice rule.'},
            {'taskKey': ['3C', None, None, None], 'paperPages': [12], 'schemePages': [12],
             'evidence': 'Paper calls the kanji pool C and grammar D; scheme labels them B and C. Bind using wording and retain paper citations.'},
            {'taskKey': ['5', None, None, None], 'paperPages': [16], 'schemePages': [14, 15],
             'evidence': 'Original Atlas29 is mislabelled Blog about your locality. The full original paper/scheme ask for a school-memories essay. Correct the label without changing the stable anchor.'},
        ],
        'choiceBoundaries': [
            'Q1A1 five-of-six links, Q1A2 complete two-item table, Q2A1 complete two-person table, listeningA complete three-person table and listeningB2 complete weather/advice table remain whole tasks.',
            'Q2B1/2 and Q2C1/2 are four distinct five-of-six pools. Q3C is one five-of-six pair pool, with reading1 and meaning1 separately within each chosen pair. Q3D is one ten-of-twelve blank pool across seven sentences.',
            'Q4 is one chooseone-of-three task with three required content points7each and discretionary4; Q5 is one choosefour-of-eight content pool5each with discretionary5. Both use one common expression score25 with published lowerE19 conditions.',
            'ListeningC(vii) requires east exit1 plus anytwo other route details2+1. Phone is a whole-number3-mark answer with no published digit split. D(vii) requires cat1 plus anytwo description details1each.',
            'Reading language instructions apply to all35 reading tasks; named Japanese listening rule appears before all21 listening tasks. Only Q2A2(i–iii) carries the extraneous-material reduction. No writing language penalty is published.',
            'All original29 written and four listening Atlas identities remain. Correct Q5 label and scheme upper bound21to20 after original-page verification.',
        ],
    }


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2021-hl-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
