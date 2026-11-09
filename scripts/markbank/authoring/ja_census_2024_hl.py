#!/usr/bin/env python3
"""Independent 47-page visual inventory, before 2024 Higher authoring.

Complete source tasks and individual printed tariffs, without reading cards.
Physical PDF page numbers are used throughout (scheme printed page + 2).
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2024-hl-000-paper.pdf', '4e0c6178a0f00657cfefee31b38456b21ed6acdff8e249d7a143ea06d858a0c6'),
    ('aural', 'examiner-reports/japanese/papers/2024-hl-A00-paper.pdf', '84e83ebc5b2f4fdfdc2de0b05b31b43c581694211e053d7cf92279005845b3b5'),
    ('scheme', 'examiner-reports/japanese/schemes/2024-hl.pdf', 'c3eeadd3fca460b978cb366815b07b3cb303626626714481a1163247550a56b2'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None, letter=None):
    component = 'aural' if section.startswith('L') else 'paper'
    item = {'key': [section, q, letter, roman], 'marks': marks, 'component': component,
            'paperPages': [pp], 'schemePages': sp,
            'atlas': {'fileid': f'LC058ALP{"A00" if component == "aural" else "000"}BV.pdf', 'questionNumber': str(atlas)}}
    if roman and letter:
        # The physical listening paper nests a letter under a roman. Keep
        # that printed citation order; the canonical tuple remains L/R.
        item['paperRef'] = f'2024 HL Section {section} Q{q}({roman})({letter})'
    TASKS.append(item)


def build():
    task('1A', 1, 6, 3, [6], 1)
    for q, marks in [(2, [2, 1, 1]), (3, [2, 4]), (4, [2, 2])]:
        for roman, mark in zip(['i', 'ii', 'iii'], marks):
            task('1A', q, mark, 3, [6], q, roman)
    for q, marks in [(1, [3, 2]), (2, [2, 1, 2])]:
        for roman, mark in zip(['i', 'ii', 'iii'], marks):
            task('1B', q, mark, 4, [7], q + 4, roman)
    task('2A', 1, 7, 7, [7], 7)
    for roman, marks in zip(['i', 'ii', 'iii', 'iv', 'v'], [3, 3, 2, 3, 2]):
        task('2A', 2, marks, 7, [7], 8, roman)
    for roman in ['i', 'ii', 'iii']:
        task('2A', 3, 2, 7, [8], 9, roman)
    task('2A', 4, 4, 7, [8], 9)
    for section, page, scheme, offset in [('2B', 8, 8, 9), ('2C', 9, 9, 11)]:
        for q in [1, 2]:
            task(section, q, 5, page, [scheme], q + offset)
    for q, marks in enumerate([3, 2, 2, 3, 2, 2], 1):
        task('3A', q, marks, 11, [9], q + 13)
    for q, marks in enumerate([1, 1, 2, 2], 1):
        task('3B', q, marks, 11, [10], q + 19)
    task('3C', None, 10, 12, [10], 24)
    task('3D', None, 10, 12, [10], 25)
    task('4', None, 40, 14, [11, 12], 26)
    task('5', None, 60, 16, [13, 14], 27)
    for q, marks in enumerate([8, 8, 7], 1):
        task('LA', q, marks, 2, [3], q)
    for q, marks in enumerate([1, 2, 1, 1, 3, 2, 3, 2, 2], 1):
        task('LB', q, marks, 3, [4], q + 9 if q < 4 else q)
    for roman, letter, marks, sp in [('i', None, 3, [4]), ('ii', None, 3, [4]), ('iii', None, 2, [4]), ('iv', 'a', 1, [4]), ('iv', 'b', 2, [4, 5]), ('v', None, 2, [5]), ('vi', None, 1, [5])]:
        task('LC', 1, marks, 4, sp, 13, roman, letter)
    for roman, letter, marks in [('i', 'a', 2), ('i', 'b', 2), ('ii', None, 3)]:
        task('LC', 2, marks, 4, [5], 14, roman, letter)
    for q, allocations in [(1, [('i', None, 2), ('ii', None, 3), ('iii', None, 2)]), (2, [('i', None, 2), ('ii', None, 2)]), (3, [('i', None, 2), ('ii', 'a', 1), ('ii', 'b', 3), ('iii', None, 2)])]:
        for roman, letter, marks in allocations:
            task('LD', q, marks, 5, [5], q + 14, roman, letter)
    assert len(TASKS) == 72, len(TASKS)
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}, totals
    sources = []
    for component, path, expected in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        sources.append({'component': component, 'path': path, 'sha256': expected})
    return {'subjectId': 'japanese', 'year': 2024, 'level': 'hl', 'reviewedAt': '2026-11-09',
            'method': 'Independent visual sweep of all 20 written, 8 aural and 19 scheme physical pages before authoring. Complete tasks and separately priced responses counted directly from the originals, retaining printed discrepancies rather than silently rewriting the paper.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 21)), ['cover', 'Q1A original Pocky website, flavour ranking and campaign', 'Q1A matching, comprehension and required ranking table', 'Q1B two customer reviews and five separately priced responses', 'explicit blank', 'Q2 Tokyo Kart and kimono/tea source articles', 'Q2A required activity table, English/Japanese comprehension and translation', 'Q2B two any-five-of-six kanji pools', 'Q2C two any-five-of-six grammar pools', 'Q3 Aaron email source and vocabulary', 'Q3A six English and Q3B four Japanese responses', 'Q3C paired kanji any-five and Q3D any-ten of twelve blanks across eight sentences', 'explicit blank', 'Q4 choose one of three prompts, same C20/E20 grid', 'writing answer grid', 'Q5 scholarship application covering any four of eight headings', 'writing answer grid', 'writing answer grid', 'writing answer grid', 'copyright and back cover'])),
                'aural': dict(zip(map(str, range(1, 9)), ['cover and English-answer instructions', 'Part A Brian/Maeve/Chloe profile table, three required response rows', 'Part B Sky Brown interview and nine tasks', 'Part C snow festival and weather; separately priced nested letter tasks', 'Part D Yuji/Anna conversation; separately priced nested room-location/description tasks and phone grid', 'explicit blank', 'explicit blank', 'back cover with explicit blank'])),
                'scheme': dict(zip(map(str, range(1, 20)), ['cover', 'general examiner guidance', 'listening Japanese half-credit rule and Part A table, 23 marks', 'Part B 17 marks and Part C1 beginning; two/three-details source mismatch', 'Part C continuation/weather, Part D19 individual tariffs and D1 heading inconsistency', 'Q1A matching, comprehension and required ranking table', 'Q1B Japanese half-credit; Q2A activity table and English responses; extraneous-material condition for Q2A3', 'Q2A3 Japanese responses; translation misnumbered3; Q2B kanji pools', 'Q2C grammar pools and Q3A English comprehension', 'Q3B extraneous-material condition; Q3C paired kanji and Q3D12-blank grammar pool', 'Q4 all alternatives and C20/E20 allocation with opening/closing', 'Q4 normal/lower expression bands and length/content thresholds', 'Q5 any-four headings at7 each plus opening/closing, C30/E30', 'Q5 normal/lower expression bands and thresholds', 'recording transcript Part A', 'recording transcript Part B', 'recording transcript Part C and Part D beginning', 'recording transcript Part D continuation', 'blank back cover'])),
            },
            'sourceDiscrepancies': [
                {'paperPages': [4], 'schemePages': [4], 'taskKey': ['LC', 1, None, 'ii'], 'evidence': 'The paper asks two activities, while the published scheme says any three details, 1 mark each, total 3. Retain the exact printed ask and make the scheme quota visible; do not substitute a fabricated 2+1 tariff.'},
                {'paperPages': [5], 'schemePages': [5], 'taskKeys': [['LD', 1, None, 'i'], ['LD', 1, None, 'ii'], ['LD', 1, None, 'iii']], 'evidence': 'The Part D1 heading says 8 but the individual tariffs are 2+3+2=7. Together D2=4 and D3=8 reconcile to the printed Part D19 and the full listening80. Use individual tariffs, do not invent a missing mark.'},
                {'paperPages': [7], 'schemePages': [8], 'taskKey': ['2A', 4, None, None], 'evidence': 'The paper labels the translation 4; the scheme repeats 3 after its Q2A3 responses. Exact translation text aligns the task; keep paper citation Q4 and printed total4.'},
            ],
            'choiceBoundaries': [
                'Q1A1 is one required six-cell matching task (1 each); Q1A3(ii) is one required four-cell flavour-ranking table (1 each).',
                'Q2A1 is one required two-activity table, with Tokyo Kart3 and kimono/tea4 priced components. The example Akihabara earns no new mark.',
                'Q2B1/2 and Q2C1/2 each remain one any-five-of-six printed pool; Q3C one any-five-of-six paired reading/meaning pool, 1+1 per chosen item.',
                'Q3D is one any-ten-of-twelve-blank pool across eight sentences. The dependent second blank in sentence(ii) explicitly accepts made if no is used in its previous particle; preserve that rule visibly.',
                'Q4 is one same-grid choice of three prompts, C20/E20 with two content9 and opening1/closing1; lower E15 at C<=10 or fewer than150characters.',
                'Q5 is one application covering any four of eight headings,7each plus opening1/closing1 and E30; lower E20 at C<=15 or fewer than200characters.',
                'Listening A keeps three complete required profile rows, Brian8/Maeve8/Chloe7. B has9, C10 and D9 separately priced tasks, including six printed roman-then-letter subparts.',
                'Q2A2(i) allows a two-landmark route as one accepted detail alongside other tour details. Q2A2(ii) pairs sandals/heels as one fact; do not double-credit synonyms.',
                'Language half credit is source-scoped to31 listening tasks (scheme physicalp3) and5 Q1B responses (physicalp7). Extraneous-material half credit separately applies to three Q2A3 responses (physicalp7) and four Q3B responses (physicalp10). No all-paper language or writing penalty is printed.',
            ]}


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2024-hl-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
