#!/usr/bin/env python3
"""Independent 2018 Higher inventory after all 48 original pages were viewed.

This census does not import cards, authored outputs or a paper parser. Required
tables and pools stay whole; separately priced questions retain their boundaries.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2018-hl-000-paper.pdf', 'c357e069eadb294aaca01c3a7e9968d0e91074e5afa1c34d0946fa38cfacfe26'),
    ('aural', 'examiner-reports/japanese/papers/2018-hl-A00-paper.pdf', '3443cedcdc08f388158250787723b5d91b8d28d4559381fd240a48403be42baf'),
    ('scheme', 'examiner-reports/japanese/schemes/2018-hl.pdf', 'b945fb41c6b24288c864e28808ba4f632eaf92ab2f943d200e6717baa6d34c74'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058ALP{"A00" if component == "aural" else "000"}EV.pdf', 'questionNumber': str(atlas)}})


def build():
    task('1A', 1, 6, 3, [6], 1)
    task('1A', 2, 2, 3, [6], 2)
    for q in [3, 4]:
        for roman in ['i', 'ii']:
            task('1A', q, 2, 3, [7] if (q, roman) == (4, 'ii') else [6], q, roman)
    for q in [5, 6]:
        task('1A', q, 2, 3, [7], q)
    for q, marks in [(1, 2), (2, 4), (3, 2), (4, 2)]:
        task('1B', q, marks, 4, [7], q + 6)
    task('2A', None, 11, 7, [7], 11)
    for roman, marks in zip(['i', 'ii', 'iii'], [1, 2, 2]):
        task('2A', 1, marks, 7, [8], 12, roman)
    for roman, marks in zip(['i', 'ii', 'iii', 'iv'], [2, 2, 4, 2]):
        task('2A', 2, marks, 7, [8], 13, roman)
    task('2A', 3, 4, 7, [8], 14)
    task('2B', None, 10, 8, [9], 26)
    task('2C', None, 10, 8, [9], 27)
    for roman in ['i', 'ii']:
        task('3A', 1, 2, 11, [10], 15, roman)
    for q, marks in [(2, 2), (3, 2), (4, 2), (5, 3), (6, 2)]:
        task('3A', q, marks, 11, [10], q + 14)
    for q, marks in [(1, 1), (2, 2), (3, 2)]:
        task('3B', q, marks, 11, [10], q + 20)
    for q in [1, 2]:
        task('3C', q, 5, 12, [11], 28)
        task('3D', q, 5, 13, [11], 29)
    task('4', None, 40, 14, [12, 13], 24)
    task('5', None, 60, 16, [14, 15], 25)
    task('LA', None, 18, 2, [3], 1)
    for q, marks in [(1, [2, 4, 2, 2]), (2, [2, 4, 2]), (3, [2, 2])]:
        for roman, mark in zip(['i', 'ii', 'iii', 'iv'], marks):
            task('LB', q, mark, 3, [4], 2, roman)
    for q, marks in [(1, [2, 6, 2]), (2, [2, 4, 4])]:
        for roman, mark in zip(['i', 'ii', 'iii'], marks):
            task('LC', q, mark, 4, [5], 3, roman)
    for q, marks in [(1, [2, 4, 4]), (2, [4, 4, 2])]:
        for roman, mark in zip(['i', 'ii', 'iii'], marks):
            task('LD', q, mark, 5, [5] if q == 1 else [6], 4, roman)
    assert len(TASKS) == 61, len(TASKS)
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}, totals
    assert sum(t['key'][0][0] in '123' for t in TASKS) == 37
    assert sum(t['component'] == 'aural' for t in TASKS) == 22
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2018, 'level': 'hl', 'reviewedAt': '2026-11-09',
            'method': 'Independent full visual sweep of all 20 written, eight aural and 20 scheme physical pages before authoring. Required pools and tables remain whole; separately priced responses retain their source boundaries.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'candidateMaximum': {'written': 220, 'listening': 80, 'total': 300,
                                 'writingChoice': 'The original cover requires all five questions. Q4 chooses one of two 40-mark recommended-place articles; Q5 is one 60-mark thank-you email, any four of six headings.'},
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 21)), [
                    'cover: written220, answer all five questions',
                    'Q1A original Baskin Robbins website, navigation, flavours, green-tea collaboration, pizza and birthday cakes',
                    'Q1A six required links and seven separately priced responses',
                    'Q1B original FAQ source and four separately priced English responses',
                    'explicit blank',
                    'Q2 original Airbnb reviews by Yuri, Scott and Maki; photographs, underlined translation and vocabulary',
                    'Q2A nine unfilled table cells, three Japanese responses, four English responses and translation',
                    'Q2B five required reading/meaning pairs; Q2C ten required particle blanks across seven sentences',
                    'explicit blank',
                    'Q3 original interview with Ken, photograph and vocabulary',
                    'Q3A seven separately priced English responses; Q3B three Japanese responses',
                    'Q3C five required meanings and five required readings',
                    'Q3D five required negative forms and five required verb forms, exact underlines',
                    'Q4 one of two recommended-place articles, approximately200 Japanese characters, two prompts each',
                    'Q4 answer grid',
                    'Q5 thank-you email after Japanese homestay, approximately320 characters, any four of six headings',
                    'Q5 answer grid', 'Q5 answer grid', 'additional answer grid', 'explicit blank back cover'])),
                'aural': dict(zip(map(str, range(1, 9)), [
                    'cover: listening80, answer all questions in English',
                    'Part A one complete three-phone/four-column table',
                    'Part B volunteers four tasks, Chie Hanawa three tasks, Tokyo weather two tasks; original whole phone grid',
                    'Part C trip planning three tasks and Osaka station three tasks',
                    'Part D Hayato and mother before exams three tasks and after exams three tasks',
                    'explicit blank', 'explicit blank', 'explicit blank back cover'])),
                'scheme': dict(zip(map(str, range(1, 21)), [
                    'cover', 'general examiner guidance',
                    'listening Japanese/romaji/script half-credit rule; Part A18 table',
                    'Part B22, nine tasks; Rugby/World Cup1 partial, guitar1 partial, whole phone2',
                    'Part C20 six tasks; Part D before exams10 three tasks',
                    'Part D after exams10 three tasks; Q1A links6 and first four ordinary responses',
                    'Q1A final three responses; Q1B10 local Japanese-half rule; Q2A complete table11',
                    'Q2A Japanese responses5 and extraneous rule; English10 including sunrise-only1 partial; translation4',
                    'Q2B required reading/meaning pairs10 and Q2C ten required particle blanks10',
                    'Q3A English15 with exact component and reason tariffs; Q3B Japanese5',
                    'Q3C required meanings5/readings5; Q3D negative forms5/verb forms5',
                    'Q4 recommended restaurant/place choices, each content9+9, discretionary1 per prompt, expression20',
                    'Q4 exact normal/lower expression bands; lower15 if content<=10 or length<150',
                    'Q5 four content headings6, discretionary4, opening1/closing1, expression30',
                    'Q5 exact normal/lower expression bands; lower20 if content<=15 or length<200',
                    'tapescript Part A', 'tapescript Part B and start of C', 'tapescript rest of C and start of D',
                    'tapescript rest of D', 'blank back cover'])),
            },
            'sourceDiscrepancies': [],
            'choiceBoundaries': [
                'Q1A links are one required six-answer task1 each. Flavours, cakes and other one-detail alternatives stay one response. Two colours is any2 of pink/blue/white1 each. Q1B has four locally priced responses and the printed Japanese-only half rule.',
                'Q2A table is one task11 with nine missing cells. Yuri location, Scott alone and Maki host lives abroad are prefilled examples. Host details for Yuri/Scott each earn2; every other missing cell1. Q2A1 has three extraneous-material rules; no English or general-reading penalty is printed.',
                'Q2A2(iii) accepts any two location details2 each, with sunrise-only1 as a partial for the sea concept. Preserve this inside one concept slot; do not count sea and sunrise as two independent full answers. Translation has four explicit1-mark components.',
                'Q2B requires all five reading-letter/meaning pairs1+1; retain every original option. Q2C requires all ten one-mark particle blanks across seven sentences. Q3C/D each retain two five-answer pools with every exact alternative and original underlines.',
                'Q3A3 awards event1 and principal/pupils description1. Q3A5 awards Japanese system1 and one explanation2. No generic reading or Japanese-answer language penalty is printed for Q3.',
                'Q4 one40-mark choice: two content9, discretionary1 for each prompt, expression20; lowerE15 if C<=10 or fewer than150 characters. Q5 one60-mark email: four headings6, discretionary4, opening1/closing1, expression30; lowerE20 if C<=15 or fewer than200 characters. Both are required.',
                'Listening A is one18-mark required12-cell table. Each row is type1, timing1, anytwo activities1 each and one negative2. All22 listening tasks use the namedJapanese/romaji/script half rule. Phone03-3573-8205 earns2 whole, no per-digit tariff.',
                'Listening B Rugby World Cup2 versus Rugby/World Cup1 and Japanese instrument2 versus guitar1 retain exact partial controls. Chie music detail requires two types for its one detail slot. C trip advantages choose3 at2each; its two direction details each2. D who2 and reason2 remain independent, with no invented splitting of its individual reasons.',
                'Preserve all29 original written and four aural Atlas identities, labels and existing crops. Correct scheme upper bounds21→20. Append verified physical page6 to aural D for after-exams tasks; do not replace the original page5 crop.',
            ]}


if __name__ == '__main__':
    result = build()
    path = Path(__file__).parent / 'reviews/japanese-2018-hl-census.json'
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f"Independent 2018 HL census: {len(TASKS)} tasks, {result['checksums']}")
