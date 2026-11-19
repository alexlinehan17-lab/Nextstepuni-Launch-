#!/usr/bin/env python3
"""Independent 2017 Higher inventory after all48 original pages were viewed.

No authored cards, served outputs or parser fragments are read.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2017-hl-000-paper.pdf', 'e96083ac6d83286da7ad5e1172a3094819339d01cfe1acda36e4abeed1762a0e'),
    ('aural', 'examiner-reports/japanese/papers/2017-hl-A00-paper.pdf', 'e41a80ce4085d666477710f6b43d95d6be317c11949c1ca0e98c52a29d53d0ab'),
    ('scheme', 'examiner-reports/japanese/schemes/2017-hl.pdf', '601de9e56949ad7147ce4a6ffcb2ed009d4656898b15b84a269e9d9ca82535d1'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None, letter=None):
    component = 'aural' if section.startswith('L') else 'paper'
    item = {'key': [section, q, letter, roman], 'marks': marks, 'component': component,
            'paperPages': [pp], 'schemePages': sp,
            'atlas': {'fileid': f'LC058ALP{"A00" if component == "aural" else "000"}EV.pdf', 'questionNumber': str(atlas)}}
    if roman and letter:
        item['paperRef'] = f'2017 HL Section {section} Q{q}({roman})({letter})'
    TASKS.append(item)


def build():
    task('1A', 1, 6, 3, [6], 1)
    task('1A', 2, 2, 3, [6], 2, 'i')
    for letter in ['a', 'b']:
        task('1A', 2, 2, 3, [6], 2, 'ii', letter)
    for roman in ['i', 'ii']:
        task('1A', 3, 2, 3, [6], 3, roman)
    for roman in ['i', 'ii', 'iii']:
        task('1A', 4, 2, 3, [6], 4, roman)
    for q, mark in enumerate([2, 2, 1, 3], 1):
        task('1B', q, mark, 4, [7], q + 4)
    task('2A', 1, 14, 7, [7], 9)
    for roman in ['i', 'ii', 'iii']:
        task('2A', 2, 2, 7, [7], 10, roman)
    for roman, mark in zip(['i', 'ii', 'iii'], [2, 3, 1]):
        task('2A', 3, mark, 7, [8], 11, roman)
    task('2A', 4, 4, 7, [8], 12)
    for q in [1, 2]:
        task('2B', q, 5, 8, [8], 17)
        task('2C', q, 5, 9, [8 if q == 1 else 9], 18)
    for q, mark in enumerate([2, 1, 2, 2, 2, 2, 3], 1):
        task('3A', q, mark, 11, [9], 13)
    for q in [1, 2, 3]:
        task('3B', q, 2, 11, [9], 14)
    task('3C', None, 10, 12, [10], 19)
    task('3D', None, 10, 12, [10], 20)
    task('4', None, 40, 14, [11, 12], 15)
    task('5', None, 60, 16, [13, 14], 16)
    task('LA', None, 18, 2, [3], 1)
    for section, questions, pp, atlas in [
        ('LB', [(1, [2, 3, 4, 2, 4]), (2, [4, 4, 2])], 3, 2),
        ('LC', [(1, [4, 2]), (2, [4, 2]), (3, [3, 2, 3])], 4, 3),
        ('LD', [(1, [4, 3, 2, 2]), (2, [2, 4])], 5, 4),
    ]:
        for q, marks in questions:
            sp = 3 if section == 'LB' and q == 1 else 5 if section == 'LD' else 4
            for roman, mark in zip(['i', 'ii', 'iii', 'iv', 'v'], marks):
                task(section, q, mark, pp, [sp], atlas, roman)
    assert len(TASKS) == 61
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}, totals
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2017, 'level': 'hl', 'reviewedAt': '2026-11-09',
            'method': 'Independent full visual sweep of all20 written,8 aural and20 scheme physical pages before authoring. Required pools and tables remain whole, with separately priced actual paper boundaries retained.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'candidateMaximum': {'written': 220, 'listening': 80, 'total': 300,
                                 'writingChoice': 'All five written questions mandatory. Q4choose(a)or(b); Q5cover anyfour ofsix headings.'},
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 21)), [
                    'cover written220/allfive questions',
                    'Q1A Pokemon website, ten links, two full event descriptions',
                    'Q1A six required links and eight separately priced event responses, including roman(ii)thenletter(a)/(b)',
                    'Q1B four original gaming forum profiles and four English responses',
                    'explicit blank', 'Q2 full SMAP article, photograph and vocabulary',
                    'Q2A members table, three Japanese responses, three English responses, translation',
                    'Q2B five required kanji meanings and five required hiragana readings',
                    'Q2C five required plain forms and five required verb forms',
                    'Q3 full Satomi school-clubs letter and vocabulary',
                    'Q3A seven English responses; Q3B three Japanese responses',
                    'Q3C five required reading/meaning pairs; Q3D ten required particles in seven sentences',
                    'explicit blank', 'Q4 two alternative short-speech prompts, about200characters',
                    'Q4 answer grid', 'Q5 email after movinghouse, anyfour ofsix headings, about320characters',
                    'Q5 answer grid', 'Q5 answer grid continuation', 'Q5 answer grid continuation', 'explicit blank backcover'])),
                'aural': dict(zip(map(str, range(1, 9)), [
                    'cover80/English/allquestions', 'A summer-holiday table twelve required cells across three interviews',
                    'B eight cafe/weather tasks with full phonegrid011prefilled and seven blanks',
                    'C seven school-reception tasks', 'D six restaurant tasks',
                    'explicit blank', 'explicit blank', 'explicit blank backcover'])),
                'scheme': dict(zip(map(str, range(1, 21)), [
                    'cover', 'general examiner guidance',
                    'listening half credit Japanese/romaji/script; A18table; B1cafe15 with2+1 choice, directions2+1+1 and wholephone4',
                    'B2weather10; C20 including separately priced full/partial concepts',
                    'D17 with happyhour-only1 partial and birthday18th1+party1+reason2',
                    'Q1A22 complete links/events tariffs',
                    'Q1B8/localJapanese halfcredit; Q2A1table14 and Q2A2threeJapanese2each/extraneoushalfcredit',
                    'Q2A3English6/translation4; Q2Btwofive-itempools5each; Q2C1plainforms5',
                    'Q2C2verbforms5; Q3A14 and Q3B6/extraneoushalfcredit',
                    'Q3Cfive reading/meaning pairs10 and Q3Dten particles10',
                    'Q4content9+9+opening1+closing1 for either choice',
                    'Q4expression20/Lower15, C<=10 orlength<150, full normal/lowerbands and correction guidance',
                    'Q5four chosen headings7each+opening1+ending1',
                    'Q5expression30/Lower20, C<=15 orlength<200, full normal/lowerbands and correction guidance',
                    'tapescript A', 'tapescript B and C1/C2', 'tapescript C3 and D',
                    'explicit blank', 'explicit blank', 'backcover'])),
            },
            'choiceBoundaries': [
                'Q1A six links1each stay one task6. Q2(ii)(a)/(b) are separately priced actual paper responses2each, canonical letter/roman keys retain literal roman-then-letter paperRef. Required drink/game and ticket/membercard components1each stay in their whole questions.',
                'Q1B4 Sarah chooses two of five printed details at2+1. Q2Atable has ten unfilled cells14 total, three given examples and two struck birthdays unpriced; each date is one printed mark, never split into separate date/month awards.',
                'Q2B meanings/readings and Q2C plainforms/verbforms are four complete five-item pools. Q3C requires five reading/meaning pairs1+1; Q3D requires all ten particle blanks across seven sentences.',
                'Q4 is one choice40: two content criteria9each, opening1/closing1, E20withLower15 when C<=10 orcharacters<150. Q5 one60: choosefour headings7each, opening1/ending1, E30withLower20 when C<=15 orcharacters<200. Do not inherit2018 discretionary allocations.',
                'ListeningA is one twelve-celltable18: row totals5/7/6, with row2two-or-college1 plusfriends1 inside its companion cell and two activitydetails1each for every interview.',
                'PartA third activity pool retains meet sister, bus tour, sightseeing and art gallery/museum. The single transcript美術館 supports treating its two English renderings as one concept; this is source-context interpretation, not an explicit bracket in the slash-delimited scheme. Bus tour and sightseeing remain separate printed options; choose two at1each.',
                'B1specialpack anytwoofthree2+1; directionsExit1=2,turnright1,walkstraight3minutes1. Completephone011-547-1929 has wholeanswer4; no per-digit tariff is printed. B2weather eachchoose2x2.',
                'C2i musicaltickets2 plus one printed detail2. C3i jacket2 plus onecolour/contents1. C3ii before1+PE1. C3iii askPEteacher2/teacher1 plus comebackaftercleaning/later1. Preserve mutually exclusive partials; never count full andpartial as separate answers.',
                'D1iv happyhouruntil7/dessertfree2 versus happyhouralone1 is one exclusive full/partial concept. D2ii is one question4 containing age18th1+party/birthday1+one reason2.',
                'Only26 namedJapanese language rules: fourQ1B and22listening. Six extraneous rules:2A2i/ii/iii and3B1/2/3. No genericreading, English-answer or writing-language penalties printed.',
                'Preserve all20 original written and4auralAtlas identities/labels/regions. Correct only scheme bounds21to20.',
            ]}


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2017-hl-census.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
