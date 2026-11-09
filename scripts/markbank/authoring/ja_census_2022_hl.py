#!/usr/bin/env python3
"""Independent census of all 48 physical source pages, before authoring.

The adjusted 2022 paper offers both Q4 and Q5 but requires only one; offered
coverage therefore totals 300 marks, while the written/listening sitting is250.
No generated card data is read.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2022-hl-000-paper.pdf', '39206c2a7866abe770cd11ab26e442750b77d9846b67c25749f5525f2d212120'),
    ('aural', 'examiner-reports/japanese/papers/2022-hl-A00-paper.pdf', 'bf2cf1aa89ac7b0a2df950367a91db0b0af0a0c71fa174380ccd7a22644fa970'),
    ('scheme', 'examiner-reports/japanese/schemes/2022-hl.pdf', '99f3a19d2594fb1d0832877f21f018d07f6947900f20003cada3c34ca25083a0'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None, letter=None):
    component = 'aural' if section.startswith('L') else 'paper'
    item = {'key': [section, q, letter, roman], 'marks': marks, 'component': component,
            'paperPages': [pp], 'schemePages': sp,
            'atlas': {'fileid': f'LC058ALP{"A00" if component == "aural" else "000"}BV.pdf', 'questionNumber': str(atlas)}}
    if letter and roman:
        item['paperRef'] = f'2022 HL Section {section} Q{q}({roman})({letter})'
    TASKS.append(item)


def build():
    for q, marks in enumerate([6, 3, 2, 1], 1):
        task('1A', q, marks, 3, [7], q)
    task('1A', 5, 1, 3, [7], 5, 'i')
    task('1A', 5, 2, 3, [7], 5, 'ii')
    task('1A', 6, 8, 3, [7], 6)
    task('1B', 1, 2, 4, [8], 7)
    task('1B', 2, 3, 4, [8], 8, 'i')
    task('1B', 2, 2, 4, [8], 8, 'ii')
    task('1B', 3, 2, 4, [8], 9)
    task('2A', 1, 9, 7, [8], 10)
    for roman in ['i', 'ii', 'iii', 'iv']:
        task('2A', 2, 2, 7, [8], 11, roman)
    for roman in ['i', 'ii', 'iii']:
        task('2A', 3, 3, 7, [9], 12, roman)
    task('2A', 4, 4, 7, [9], 13)
    for q in [1, 2]:
        task('2B', q, 5, 8, [9], 23)
        task('2C', q, 5, 9, [10], 24)
    for q, marks in enumerate([3, 2, 2, 3, 2], 1):
        task('3A', q, marks, 11, [10], q + 13)
    for q, marks in enumerate([1, 1, 2, 2], 1):
        task('3B', q, marks, 11, [11], q + 18)
    task('3C', None, 10, 12, [11], 25)
    task('3D', None, 10, 12, [11], 26)
    task('4', None, 50, 14, [12, 14], 27)
    task('5', None, 50, 16, [13, 14], 28)
    for q in [1, 2, 3]:
        task('LA', q, 7, 2, [3], 1)
    for q, allocations in [(1, [3, 1, 3, 3, 2]), (2, [4, 2, 2])]:
        for roman, marks in zip(['i', 'ii', 'iii', 'iv', 'v'], allocations):
            task('LB', q, marks, 3, [4], 2, roman)
    for q, allocations in [(1, [2, 3]), (2, [2, 2, 2, 2]), (3, [2, 2, 2])]:
        for roman, marks in zip(['i', 'ii', 'iii', 'iv'], allocations):
            task('LC', q, marks, 4, [5], 3, roman)
    for roman, letter, marks, sp in [('i', None, 2, 5), ('ii', None, 3, 5), ('iii', 'a', 1, 6), ('iii', 'b', 3, 6), ('iv', None, 2, 6)]:
        task('LD', 1, marks, 5, [sp], 4, roman, letter)
    for roman, marks in zip(['i', 'ii', 'iii', 'iv'], [2, 2, 3, 2]):
        task('LD', 2, marks, 5, [6], 4, roman)
    assert len(TASKS) == 66, len(TASKS)
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}, totals
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2022, 'level': 'hl', 'reviewedAt': '2026-11-09',
            'method': 'Independent full visual sweep of 20 written, eight listening and20scheme physical pages before authoring. Count complete priced responses directly from original sources; all alternatives remain covered.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'candidateMaximum': {'written': 170, 'listening': 80, 'total': 250, 'writingChoice': 'Answer either Question4orQuestion5, each50marks. Offered-task coverage includes both.'},
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 21)), ['cover and adjusted one-of-two writing instruction', 'Q1A original Peppy pet-products website', 'Q1A matching, four individual comprehension asks including splitQ5, complete competition table', 'Q1B original pet-owner reviews and four responses', 'explicit blank', 'Q2 original Kamikatsu recycling article, map, plan and vocabulary', 'Q2A required town table, four Japanese and three English responses, translation', 'Q2B two any-five-of-six kanji pools', 'Q2C two any-five-of-six grammar pools', 'Q3 original Mika school-newspaper interview and vocabulary', 'Q3A five English and Q3B four Japanese responses', 'Q3C paired kanji any-five and Q3D twelve particle blanks any-ten', 'explicit blank', 'Q4 one-of-three writing prompts with200character minimum and eitherQ4orQ5instruction', 'writing grid', 'Q5 one composition any-four-of-eight locality headings, minimum320characters', 'writing grid', 'writing grid', 'writing grid', 'back cover'])),
                'aural': dict(zip(map(str, range(1, 9)), ['cover and English-answer instructions', 'PartA three independently numbered student profiles with four required columns', 'PartB five Taiko tasks and three weather tasks with Saturday/Sunday pair', 'PartC nine school-reception tasks', 'PartD five arranging-lunch tasks including nested directions plus four roman cafe orders', 'explicit blank', 'explicit blank', 'back cover'])),
                'scheme': dict(zip(map(str, range(1, 21)), ['cover', 'general examiner guidance', 'listening Japanese half-credit and three profile rows7each', 'PartB20: Taiko12, weather8, phonewhole2', 'PartC19 and firstPartD responses2plus3', 'remainingPartD6 plus cafeorders9; paper numbering differs', 'Q1A23 Japanese half-credit, six-item match and complete competition table8', 'Q1B9 Japanese half-credit; Q2A1town table9 Japanese half-credit; Q2A2Japanese8 with English/extraneous half-credit', 'Q2A3English9 and translation4 under13mark heading with Japanese half-credit; Q2B two kanji pools', 'Q2C two grammar pools and Q3AEnglish12 Japanese half-credit', 'Q3B printed row tariffs1+1+2+2 despite heading8; English half-credit, Q3Cpairedkanji10 andQ3Dparticles10', 'Q4three alternativeprompts C25/E25 with three discretionary marks', 'Q5anyfourheadings C25/E25 with per-heading discretionary and opening-or-closing1', 'sharedQ4/Q5expression bands25or19 atC<=13orlength<150', 'tapescriptPartAandTaiko', 'tapescriptweatherandPartC', 'tapescriptPartD', 'explicit blank', 'explicit blank', 'back cover'])),
            },
            'sourceDiscrepancies': [
                {'paperPages': [3], 'schemePages': [7], 'taskKey': ['1A', 1, None, None], 'evidence': 'Paper prompt says links1–6, but website prints links1–10 and correct Pet hotel/Salon answers8/7. Keep full website and scheme answers; do not truncate valid links.'},
                {'paperPages': [11], 'schemePages': [11], 'evidence': 'Q3B heading prints8marks, but explicit row tariffs are1+1+2+2=6. Those6 reconcile Q3=38 and reading=120 withQ3A12+C10+D10. Retain exact priced rows and disclose discrepancy; do not inflate the first two tasks.'},
                {'paperPages': [5], 'schemePages': [5, 6], 'evidence': 'PartD1 scheme labels birthday1, ingredients(i), directions(ii)a/b and time(iii); paper labels(i),(ii),(iii)a/b,(iv). Bind by literal question wording and preserve paper labels.'},
                {'paperPages': [16], 'schemePages': [13], 'taskKey': ['5', None, None, None], 'evidence': 'Q5 scheme reorders locality headings: weather is8instead ofpaper2, subsequent headings shift. Keep all eight printed paper headings and match shared5plus1content tariff by wording.'},
                {'paperPages': [14, 16], 'schemePages': [14], 'evidence': 'Paper minimums200and320 differ from the common published lower-expression threshold less than150characters. Preserve distinct instructions and the exact shared C<=13orlength<150 trigger; capE19 instead of25.'},
            ],
            'choiceBoundaries': [
                'Complete six-cell matching and four-heading competition table remain one task each. Q1A5i/ii andQ1B2i/ii remain independently priced responses.',
                'Q2A1 one required town table: name2, any-two description2each, any-two reasons descending2+1. Q2A3ii opening and closing times use published descending2+1, not invented fixed2foropening.',
                'Q2B1/2 andQ2C1/2 whole any-five-of-six pools1each. Q3C whole any-five-of-six paired reading1/meaning1 pool. Q3D one any-ten-of-twelve blank pool acrossseven sentences; acceptedwa/ga alternatives retained.',
                'Q4 same-grid choice ofthree prompts C25/E25: two content11plus opening1closing1and discretionary1in either content point. Q5 one any-four-of-eight composition: each selectedheading5plusdiscretionary1, plus suitableopening-orclosing1 andE25. Both use common lowerE19condition andremain separatepractice tasks despite examchooseoneinstruction.',
                'Listening A three complete independently numbered student rows7each with allfourrequired headings; internalchoice pools stayinsideeachrow. ListeningB2i Saturday/Sunday is one required pair4 withtwo details1eachperday.',
                'Phone0120-923-915 iswhole2 withoutfabricateddigitpartial. C3i teacher-only1partial retainedagainstfullTanaka2; allprintedcomponentmarksretained.',
                'D1ii isone capped3markresponse: any3details butmaximumtwoingredientexamples amongmeat/vegetables/butter. Render the full exact list and constraint withnumericpublishedsubtotal; do not allow threeingredientexamples alone toscore3.',
                'D2 four explicitroman responses priced2/2/3/2, ratherthanoneundividedtable. Foodanddessertrequiredcomponents each1, drinksdescending2+1.',
                'Language conditions scopedtolocalprintedheaders; listening29Japanese, Q1A7/Q1B4/Q2A1/Q2A3and4/Q3A5Japanese, Q2A2fourandQ3BfourEnglish. OnlyQ2A2fourresponses haveextraneous-materialhalfcredit; no writingpenalty.',
                'AlloriginalAtlasIDs retained: written1–28,listening1–4. ListeningDanchor4requires itsomittedphysicalscheme6inadditiontopage5; no newanchororrenumbering.',
            ]}


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2022-hl-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
