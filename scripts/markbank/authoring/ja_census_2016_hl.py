#!/usr/bin/env python3
"""Independent 2016 Higher inventory after all 48 original pages were viewed.

No authored cards, served outputs or parser fragments are read.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2016-hl-000-paper.pdf', '18c4e6e4695bc5e2db4ea074e674927cdde6918ba95a3995e6b6227bfa908523'),
    ('aural', 'examiner-reports/japanese/papers/2016-hl-A00-paper.pdf', '37e7f13202e852e6ab0209ad8cf4d1bb02a6c356477333355d770c9e76defb52'),
    ('scheme', 'examiner-reports/japanese/schemes/2016-hl.pdf', '9b8fda5225ae55e5dfb9682a76defaab104d836b7e8d10c9cab8ab928bcdab06'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058ALP{"A00" if component == "aural" else "000"}EV.pdf', 'questionNumber': str(atlas)}})


def build():
    task('1A', 1, 6, 3, [7], 1)
    task('1A', 2, 2, 3, [7], 2)
    for roman in ['i', 'ii']:
        task('1A', 3, 4, 3, [7], 3, roman)
        task('1A', 4, 2, 3, [7], 4, roman)
    task('1A', 5, 2, 3, [7], 5)
    for q in range(1, 5):
        task('1B', q, 2, 4, [7], q + 5)
    task('2A', 1, 11, 7, [8], 10)
    for roman in ['i', 'ii', 'iii']:
        task('2A', 2, 2, 7, [8], 11, roman)
    for roman, mark in zip(['i', 'ii', 'iii', 'iv'], [2, 3, 2, 2]):
        task('2A', 3, mark, 7, [8], 12, roman)
    task('2A', 4, 4, 7, [9], 13)
    task('2B', None, 10, 8, [9], 14)
    task('2C', None, 10, 8, [9], 15)
    task('3A', 1, 3, 11, [9], 16)
    task('3A', 2, 3, 11, [9], 17)
    task('3A', 3, 3, 11, [9], 18, 'i')
    task('3A', 3, 2, 11, [9], 18, 'ii')
    task('3A', 4, 3, 11, [10], 19)
    for q, mark in [(1, 2), (2, 4)]:
        task('3B', q, mark, 11, [10], 20)
    for q in [1, 2]:
        task('3C', q, 5, 12, [10], 21)
        task('3D', q, 5, 13, [10], 22)
    task('4', None, 40, 14, [11, 12], 23)
    task('5', None, 60, 16, [13, 14], 24)
    task('LA', None, 18, 2, [3], 1)
    for q, marks in [(1, [2, 2, 4, 1]), (2, [4, 3, 2])]:
        for roman, mark in zip(['i', 'ii', 'iii', 'iv'], marks):
            task('LB', q, mark, 3, [4], 2, roman)
    for roman, mark in zip(['i', 'ii', 'iii', 'iv'], [4, 2, 2, 4]):
        task('LC', 1, mark, 4, [5], 3, roman)
    task('LC', 2, 8, 4, [5], 3)
    task('LC', 3, 4, 4, [5], 3)
    for roman, mark in zip(['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii'], [2, 4, 4, 2, 2, 2, 4]):
        task('LD', None, mark, 5, [6], 4, roman)
    assert len(TASKS) == 56
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}, totals
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2016, 'level': 'hl', 'reviewedAt': '2026-11-09',
            'method': 'Independent full visual sweep of all 20 written, eight aural and 20 scheme physical pages before authoring. Required pools/tables remain whole; all separately priced actual paper responses retained.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'candidateMaximum': {'written': 220, 'listening': 80, 'total': 300,
                                 'writingChoice': 'All five written questions mandatory. Q4 choose (a) or (b); Q5 cover any four of six headings.'},
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 21)), [
                    'cover written220/allfive questions',
                    'Q1A complete Yodobashi-Akiba floor guide, products/services/hours',
                    'Q1A six required floor numbers and six other separately priced responses, including two two-detail pools',
                    'Q1B four original customer recommendations and four English responses',
                    'explicit blank', 'Q2 full randoseru history/comments/JOICFP passage and vocabulary',
                    'Q2A required eight-cell table, three Japanese responses, four English responses, translation',
                    'Q2B five required reading/meaning pairs; Q2C ten required particles in seven sentences',
                    'explicit blank', 'Q3 full Haruna email from Ireland and vocabulary',
                    'Q3A five English responses; Q3B two Japanese responses',
                    'Q3C five required kanji meanings and five required hiragana readings',
                    'Q3D five required positive forms and five required verb forms',
                    'Q4 two alternative diary prompts, about200characters',
                    'Q4 answer grid', 'Q5 email to incoming exchange student, anyfour ofsix headings, about320characters',
                    'Q5 answer grid', 'Q5 answer grid continuation', 'Q5 answer grid continuation', 'explicit blank backcover'])),
                'aural': dict(zip(map(str, range(1, 9)), [
                    'cover80/English/allquestions', 'A winning-the-lotto table: twelve required cells across three interviews',
                    'B seven concert responses',
                    'C six news tasks, including wholephonegrid and two weather-table rows',
                    'D seven Daniel interview responses',
                    'explicit blank', 'explicit blank', 'explicit blank backcover'])),
                'scheme': dict(zip(map(str, range(1, 21)), [
                    'cover', 'general examiner guidance',
                    'listening half credit Japanese/romaji/script; A18 table, three rowtotals6 each',
                    'B18 including event1+1, directions2+1+1, anytwo2+1 negativecomments',
                    'C24: hotel12 with wholephone4, Sharran8 with Guinness-only1 partial, two weatherrows2 each',
                    'D20: family anytwo2each, routine anytwo2each with place/time1each, souvenirs anytwo item/person1each',
                    'Q1A22 floor pool and all tariffs/partials; Q1B8 local Japanese halfcredit',
                    'Q2A30: table11, three Japanese responses6/extraneoushalfcredit, four English responses9',
                    'Q2A translation4 with two alternative routes; Q2B10; Q2C10; Q3A1–3 elevenmarks',
                    'Q3A4 three marks; Q3B6 with no extraneous clause; Q3C10 and Q3D10',
                    'Q4 two content responses8each plus four discretionary marks, totalC20',
                    'Q4expression20/Lower15, C<10 orlength<150, full normal/lowerbands and correction guidance',
                    'Q5 four chosen headings6each plus six discretionary marks, totalC30',
                    'Q5expression30/Lower20, C<=15 orlength<200, full normal/lowerbands and correction guidance',
                    'tapescript A', 'tapescript B', 'tapescript C', 'tapescript D',
                    'explicit blank', 'backcover'])),
            },
            'choiceBoundaries': [
                'Q1A six required floor numbers stay one task6. Q1A3i is one choose-two pool of four full instruments2each; piano/drums/guitar each have a one-mark partial tied to their full electric/silent concept. Never count full and partial as different instruments. Sports choose two of four2each. All paired item/name/time components remain under their actual task.',
                'Q2A table has eight unfilled cells11 total: Hitomi acquisition struck/unpriced, three detail pools choose two1each, five acquisition/time cells1each. Preserve all details including whole fits-textbooks-copies-pencilcase concept.',
                'Q2A2ii fashion model2/model1 is one exclusive response. Extraneous-material halfcredit applies only to the three Q2A2 responses. Q2A3ii is anytwo2+1. Both Japanese/English source quotations accepted in Q2A3iii and Q3A4; never attach a language penalty there.',
                'Q2A4 translation has two complete alternative2+2 routes; never combine their marks. Q2B five required reading/meaning pairs1+1 and Q2C ten required particles remain whole. Q3C/D are four whole five-item pools.',
                'Q3A1 retains every separately printed family detail under the choose-three quota; named person labels stay with their answers. Q3A2 uses alternative three-mark Cambridge preparation versus English-with-friends2 plus one activity1; cap alternative routes at3. Q3A4 chooses two bilingual ideas at2+1.',
                'Q4 is one choice40: two content criteria8each, opening1/closing1 and one discretionary under each point, E20 with Lower15 only if C<10 orcharacters<150. Q5 one60: choosefour headings6each, opening1/closing1 and discretionary1 under each, E30 with Lower20 if C<=15 orcharacters<200. Do not inherit2017 tariffs or Q4 inclusive threshold.',
                'ListeningA is one required twelve-celltable18, each interview6. First action is new/red/Toyota1 plus sports car1; second action is travelAsia1 plus liveVietnam1. Why responses for interviews2/3 choose two1each. Other cells retain their whole published tariffs.',
                'B1 directions north exit2 + straight1 + three minutes1. B2 two negativecomments use descending2+1. Internal at back/far from stage remains inside the single seats-not-good concept, never an extra option.',
                'C1phone0570-064-110 is wholeanswer4; no per-digit allocation printed. C2 all nine full facts2each remain under choosefour; Guinness-book-only1 is the partial of the largest-sportswoman concept, not an extra independent fact. Original transcriptp17 explicitly makes that association; independently peer-reviewed. This is a source-context interpretation, not an explicit bracket in the printed pool. C3 one required weather table with two city responses, each choose two of three1each.',
                'D3 daily routine choices preserve explicit location1/time1 components within at most two responses. Studies10hours is a separately printed full2 option with no invented location. D7 at most two souvenirs, each item1/person1; full and partials share the same response group.',
                'Only25 namedJapanese language rules: fourQ1B and21listening. Onlythree extraneous rules:2A2i/ii/iii. No genericreading, English-answer, Q3B extraneous or writing-language penalties printed.',
                'Preserve all24 original written and4aural Atlas identities/labels/regions. Correct only scheme bounds21to20.',
            ],
            'sourceDiscrepancies': [
                {'taskKey': ['1A', 5, None, None], 'paperPage': 3, 'issue': 'The general instruction says answer questions1–4, but the same page explicitly prints separately priced question5. Retain its actual prompt and original instruction; no omitted task.'}
            ]}


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2016-hl-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
