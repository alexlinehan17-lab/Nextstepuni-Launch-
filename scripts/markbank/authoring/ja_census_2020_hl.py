#!/usr/bin/env python3
"""Independent 2020 Higher census after a full 48-page visual sweep.

No authored cards or generated manifests are read. Whole tables and finite
pools remain complete tasks; separately priced answers retain their boundaries.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2020-hl-000-paper.pdf', 'c41d53e7ce61e3e1423578dc19d969c157961a36291dabd817062bf91d06c35a'),
    ('aural', 'examiner-reports/japanese/papers/2020-hl-A00-paper.pdf', '801f709a01d0f50873eb68b7d8c8dd47630c61922dc114e2eae061d3a149db52'),
    ('scheme', 'examiner-reports/japanese/schemes/2020-hl.pdf', 'a30e9c6ccc490940127d6052a15c4642f685d20df7e5a269ac88619886c217db'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058ALP{"A00" if component == "aural" else "000"}BV.pdf',
                            'questionNumber': str(atlas)}})


def build():
    task('1A', 1, 6, 3, [7], 1)
    for q, marks in [(2, [3, 2, 2]), (3, [2, 3, 2])]:
        for roman, mark in zip(['i', 'ii', 'iii'], marks):
            task('1A', q, mark, 3, [7], q, roman)
    task('1A', 4, 1, 3, [7], 4)
    task('1B', 1, 2, 4, [8], 5)
    task('1B', 2, 3, 4, [8], 6)
    for roman in ['i', 'ii']:
        task('1B', 3, 2, 4, [8], 7, roman)
    task('2A', 1, 8, 7, [8], 8)
    for roman in ['i', 'ii', 'iii']:
        task('2A', 2, 2, 7, [8], 9, roman)
    for roman, marks in zip(['i', 'ii', 'iii', 'iv'], [2, 4, 2, 4]):
        task('2A', 3, marks, 7, [9], 10, roman)
    task('2A', 4, 4, 7, [9], 11)
    for q in [1, 2]:
        task('2B', q, 5, 8, [9], 21)
        task('2C', q, 5, 9, [9] if q == 1 else [10], 22)
    for q, marks in enumerate([3, 2, 2, 2, 3, 2], 1):
        task('3A', q, marks, 11, [10], q + 11)
    for q in [1, 2, 3]:
        task('3B', q, 2, 11, [10], q + 17)
    task('3C', None, 10, 12, [11], 23)
    task('3D', None, 10, 12, [11], 24)
    task('4', None, 40, 14, [12, 13], 25)
    task('5', None, 60, 16, [14, 15], 26)
    task('LA', None, 21, 2, [4], 1)
    for roman, marks in zip(['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii'], [3, 2, 2, 3, 2, 2, 3, 3]):
        task('LB', None, marks, 3, [4] if roman not in ['vii', 'viii'] else [5], 2, roman)
    for q, marks in [(1, [2, 2, 3]), (2, [3, 3, 2]), (3, [2, 2, 2])]:
        for roman, mark in zip(['i', 'ii', 'iii'], marks):
            task('LC', q, mark, 4, [5], 3, roman)
    for roman in ['i', 'ii', 'iii', 'iv', 'v', 'vi']:
        task('LD', None, 3, 5, [6], 4, roman)
    assert len(TASKS) == 62
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'),
        ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}, totals
    assert sum(t['key'][0][0] in '123' for t in TASKS) == 36
    assert sum(t['component'] == 'aural' for t in TASKS) == 24
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {
        'subjectId': 'japanese', 'year': 2020, 'level': 'hl', 'reviewedAt': '2026-11-09',
        'method': 'Independent full visual sweep of all20 written, eight aural and20 scheme physical pages before authoring. Required tables and finite pools count as whole tasks; every separately priced response remains represented.',
        'sources': sources, 'tasks': TASKS, 'checksums': totals,
        'candidateMaximum': {'written': 220, 'listening': 80, 'total': 300,
                             'writingChoice': 'The original paper requires all five questions. Q4 is one40-mark choose-A-or-B email; Q5 is one60-mark speech with any four of six headings.'},
        'pageRoles': {
            'paper': dict(zip(map(str, range(1, 21)), [
                'cover: written220, answer all five questions',
                'Q1A original KitKat shop: ten links, sale ranking, regional products, shipping table and vocabulary',
                'Q1A complete six-link match, six separately priced subresponses and shipping question',
                'Q1B original custom KitKat advertisement, both gift types, three named customer comments and four response tasks',
                'explicit blank',
                'Q2 original Kate Hokkaido travel diary for three dates, photograph, underlined translation and vocabulary',
                'Q2A complete two-day activity table, three Japanese responses, four English responses and translation',
                'Q2B five required kanji meanings and five required hiragana readings, each a complete task',
                'Q2C five required negative forms and five required verb forms, all original underlines',
                'Q3 original Hatsune Miku article, illustration, underlined forms and vocabulary',
                'Q3A six English responses and Q3B three Japanese responses',
                'Q3C complete five paired readings/meanings; Q3D ten required particle blanks across seven sentences',
                'explicit blank',
                'Q4 choose one of two email tasks, two content prompts each, minimum200 characters',
                'Q4 answer grid',
                'Q5 Ireland speech: any four of six headings, minimum320 characters',
                'Q5 answer grid', 'Q5 answer grid', 'additional answer grid', 'back cover explicitly without examination material'])),
            'aural': dict(zip(map(str, range(1, 9)), [
                'cover, listening80 and English-answer instruction',
                'Part A required three-resident/four-heading table',
                'Part B eight separately priced tennis-interview responses',
                'Part C three Olympics, three multicultural-party and three weather tasks, including whole phone grid',
                'Part D six separately priced house-share responses; paper(v) asks two negative comments',
                'explicit no examination material', 'explicit no examination material', 'back cover without examination material'])),
            'scheme': dict(zip(map(str, range(1, 21)), [
                'cover', 'general examiner guidance', 'internal Higher cover',
                'listening named Japanese/romaji/script half credit; Part A21 complete table; first six Part B tasks',
                'Part B final two tasks; Part C21 with required east exit and whole phone2',
                'Part D18; scheme(v) anythree1each conflicts with paper request for two',
                'Q1A21 with all six links and exact local/partial tariffs',
                'Q1B9 named Japanese half credit, source-confirmed Mari birthday-party answer; Q2A table8; Q2A2 three responses with English and extraneous-material half credit',
                'Q2A3 plus translation16 named Japanese half credit; Q2B ten required kanji cells; Q2C1 five negative forms, mislabelled D',
                'Q2C2 five verb forms; Q3A14 Japanese half credit and Q3B6 English half credit',
                'Q3C five reading1/meaning1 pairs; Q3D ten required particle answers with alternatives',
                'Q4 two email choices: content2×9 plus opening1/closing1, expression20',
                'Q4 exact expression bands; cap15 if content<=10 or length<150',
                'Q5 speech four headings6each, discretionary4 plus opening/closing2, expression30',
                'Q5 exact expression bands; cap20 if content<=15 or length<200',
                'tapescript Part A', 'tapescript Part B', 'tapescript Part C', 'tapescript Part D', 'back cover'])),
        },
        'sourceDiscrepancies': [
            {'taskKey': ['3D', None, None, None], 'paperPages': [12], 'schemePages': [11],
             'evidence': 'The final particle sentence is (vii) in the original paper; its corresponding final scheme line repeats (vi). Preserve paper identity and all ten exact answers.'},
            {'taskKey': ['LD', None, None, 'v'], 'paperPages': [5], 'schemePages': [6],
             'evidence': 'Paper requests two negative comments; scheme explicitly says anythree details1each and total3. Keep both statements visible and the exact published scheme allocation, without pretending paper and scheme agree.'},
            {'taskKey': ['2C', 1, None, None], 'paperPages': [9], 'schemePages': [9],
             'evidence': 'Paper grammar is C; scheme labels the same negative-form section D. Preserve paper citation and exact answer bindings.'},
        ],
        'choiceBoundaries': [
            'Q1A six-link match is one required task6. Separately priced products and regional responses stay separate. Descending detail pools retain2+1, product names retain printed1+1 splits and shipping is whole1.',
            'Q1B2 is one choice of gift box or gift bag, with two reasons about the chosen product for2+1; never combine reasons across different product choices. Its source-derived manual totals0/1/1.5/2/2.5/3 apply the local Japanese half-credit rule separately to each reason, including mixed-language2.5, without a second whole-response reduction. Q1B3(ii) asks Mari and correctly maps to the final birthday-party comment; the wedding comment is attributed to Satoshi. Independently confirmed at full original resolution.',
            'Q2A table is one required two-day task8, each day weather1 + centre2 + activity1. Translation has four printed one-mark components. Required kanji meanings/readings and grammar pools remain four complete five-item tasks, with no invented optional quota.',
            'Q3C has five required pairs, reading1 and meaning1 each. Q3D has ten required blanks across seven sentences,1each, retaining all alternatives. No choose-N instruction is printed for these pools.',
            'Q4 is one40-mark choose-A-or-B email task; Q5 is one60-mark speech with any four of six headings. Distinct printed content thresholds and character limits govern their expression caps.',
            'Listening Part A is one21-mark table with all12 printed cells; cells use printed complete answers or explicit anytwo detail pools. Part B8, Part C9 and Part D6 tasks remain separately priced. Route requires east exit1 plus anytwo other directions1each. Phone03-7285-1966 is whole2, with no invented per-digit allocation.',
            'Language rules are local: listening on scheme4; Q1B Japanese on8; Q2A2 English and extraneous on8; Q2A3 plus translation Japanese on9; Q3A Japanese and Q3B English on10. Do not inherit a general reading or writing penalty from another year.',
            'Preserve all26 original written and four aural Atlas identities, labels, pages and regions. Correct scheme upper bound21→20 only unless the visual sweep identifies a missing required continuation.',
        ],
    }


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2020-hl-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')


