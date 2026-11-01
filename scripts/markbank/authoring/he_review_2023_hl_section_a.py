#!/usr/bin/env python3
"""Source-reviewed partial credit and boundaries for 2023 Higher Section A.

Original IDs remain. Q4 and Q8 each contain two separate written prompts and
two published tariffs; their second prompts gain additive IDs. Examples and
required table headings remain within their original response.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys

import fitz
from he_review_2023_hl import ROOT, SCHEME, HASHES, tidy, between, criterion

PAPER = 'examiner-reports/home-economics/papers/2023-hl-014-paper.pdf'
PAPER_HASH = '8a1dceedb76a3c4aadeaa57ecc94c59d23b78c07dbbec75bd679f6e30e0c5243'
FIGURE = 'home-economics-2023-hl-sa-q3-scheme'
FIGURE_SHA256 = 'd6ce01b372724821cea8324fb00ed0e8c6e8b0d9408a951d78a53bb988299a65'
SELECTION_TOKENS = {
    1: ['two'], 2: ['one'], 3: ['two', 'each'], 4: ['two'], 5: ['one'],
    6: ['two'], 7: ['two'], 8: ['one', 'two', 'or', 'two'], 9: [], 10: [],
    11: ['two'], 12: ['following'], 13: ['each', 'following'], 14: [],
}


def build():
    assert hashlib.sha256((ROOT / PAPER).read_bytes()).hexdigest() == PAPER_HASH
    assert hashlib.sha256((ROOT / SCHEME).read_bytes()).hexdigest() == HASHES[SCHEME]
    paper = fitz.open(ROOT / PAPER)
    paper_text = '\n'.join(paper[p].get_text(clip=fitz.Rect(0, 0, 595, 745)) for p in range(2, 7))
    paper_headers = list(re.finditer(r'(?m)^(\d{1,2})\.\s*\n', paper_text))
    assert [int(m[1]) for m in paper_headers] == list(range(1, 15))
    for i, marker in enumerate(paper_headers):
        prompt = paper_text[marker.end():paper_headers[i + 1].start() if i + 1 < len(paper_headers) else len(paper_text)]
        tokens = re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b', prompt, re.I)
        assert [token.lower() for token in tokens] == SELECTION_TOKENS[int(marker[1])], 'Unclassified paper selection'
    source = fitz.open(ROOT / SCHEME)
    text = '\n'.join('\n'.join(line for line in source[p - 1].get_text().splitlines()
                               if line.strip() != str(p)) for p in range(6, 10))
    text = re.sub(r'(?<=\w)-\s*\n(?=\w)', '-', text)
    headers = list(re.finditer(r'(?m)^(\d{1,2})\.\s*\n', text))
    assert [int(m[1]) for m in headers] == list(range(1, 15))
    blocks = {int(m[1]): tidy(text[m.end():headers[i + 1].start() if i + 1 < len(headers) else len(text)])
              for i, m in enumerate(headers)}
    assert all(block.endswith('etc.') for block in blocks.values()), 'Unclassified source tail'
    authored = json.loads((ROOT / 'scripts/markbank/authored/home-economics.json').read_text())
    old = {c['id']: c for c in authored}
    fixes = {}
    added = []

    def fix(n, rows, notation, **extra):
        key = f'he-2023-hl-sa-q{n}'
        fixes[key] = dict(reason='2023 Higher Section A independently checked against paper pp3–7 and scheme pp6–9: preserve the printed question, complete guidance and actual partial-credit steps. See he_review_2023_hl_section_a.py.',
                          set=dict(rows=rows, tariffModel=dict(kind='fixed', notation=notation), **extra))

    def graded_body(n):
        return re.split(r'\(graded\s+[^)]*\)', blocks[n], maxsplit=1)[1].strip()

    for n, heading in [(1, 'biological functions of lipids'), (6, 'benefits'),
                       (9, 'role of public analyst laboratories'), (10, 'Working Family Payment'),
                       (11, 'measures'), (14, 'benefits the consumer')]:
        fix(n, [criterion('points', heading, 2, [0, 2, 3],
                          'Two distinct points, each graded 3:2:0. Published guidance: ' + graded_body(n))],
            '2 points × 3 marks (3:2:0)')
    # The PAPER says "adults"; "Irish adults" appears only in the scheme.
    fixes['he-2023-hl-sa-q6']['set']['questionText'] = 'Outline two benefits of including high fibre foods in the diet of adults.'
    fix(2, [criterion('definition', 'Gelatinisation', 2, [0, 1, 2],
                       'Two explanation points, each graded 2:1:0. Published guidance: ' + between(blocks[2], 'Gelatinisation –', 'Culinary example')),
            criterion('example', 'Culinary example', 1, [0, 2],
                      'One example, graded 2:0. Published examples: ' + blocks[2].split('Example -', 1)[1].strip())],
        'Explanation 2 × 2 (2:1:0); example 2 (2:0)')

    # The answer is a genuine two-column table. Keep its associations intact in
    # the original crop, with two paired name/food slots instead of all-or-none 3s.
    fix(3, [dict(id='pairs', kind='criterion', verbatim='Name of bacteria', marks=6,
                 permittedMarks=list(range(7)),
                 contextNote='Name two different bacteria and give a different associated high-risk food for each. Each name is graded 2:1:0; each food is graded 1:0. The complete published associations are in the table.',
                 parts=[dict(id=f'{kind}-{i}', verbatim=f'{"Name of bacteria" if kind == "name" else "High-risk food"} {i}',
                             marks=2 if kind == 'name' else 1,
                             permittedMarks=[0, 1, 2] if kind == 'name' else [0, 1])
                        for i in (1, 2) for kind in ('name', 'food')])],
        'Two pairs: name 2 (2:1:0), associated food 1 (1:0)', figureKey=FIGURE)

    bmr = blocks[4].split('Give two factors', 1)[0].split('(graded 1:0)', 1)[1].strip()
    answer = bmr.split('etc.', 1)[0].strip()
    options = [x.strip() for x in answer.split(';') if x.strip()]
    assert options[0] == 'the minimum' and len(options) == 5
    factor_text = blocks[4].split('2 points @ 1 mark (graded 1:0)', 1)[1].strip()
    fix(4, [dict(id='minimum', kind='point', verbatim='the minimum', marks=1,
                 contextNote='The scheme explicitly says minimum is an essential point in the answer.'),
            dict(id='definition', kind='anyN', verbatim='Basal Metabolic Rate', marks=3,
                 openList=True, group=dict(claimMax=3, perOption=1, options=options[1:]),
                 contextNote='Three further points at 1 mark each. This keeps the essential minimum point separate, rather than permitting four other points to receive full marks.')],
        '4 points × 1 mark (1:0); minimum is essential', totalMarks=4,
        questionText='Explain the term Basal Metabolic Rate (BMR).', questionRef='2023 HL Section A Q4 — BMR definition')
    factors = deepcopy(old['he-2023-hl-sa-q4'])
    factors.update(id='he-2023-hl-sa-q4-factors', conceptId='basal-metabolic-rate-factors',
                   questionText='Give two factors that affect a person’s basal metabolic rate.',
                   questionRef='2023 HL Section A Q4 — factors', totalMarks=2,
                   tariffModel=dict(kind='fixed', notation='2 points × 1 mark (1:0)'),
                   rows=[dict(id='factors', kind='anyN', verbatim='factors', marks=2, openList=True,
                              group=dict(claimMax=2, perOption=1,
                                         options=[x.strip() for x in factor_text.split(';') if x.strip() and x.strip() != 'etc.']))],
                   notes='Second separately priced prompt of Section A Q4; 2 marks. Original Q4 ID retains the 4-mark definition.')
    added.append(factors)

    fix(5, [criterion('description', 'roux-based sauce', 2, [0, 1, 2],
                      'Two description points, graded 2:1:0. Published guidance: ' + graded_body(5).split('Culinary example', 1)[0].strip()),
            criterion('example', 'Culinary example', 1, [0, 1, 2],
                      'One culinary example, graded 2:1:0. Published examples: ' + blocks[5].split('Culinary example 1 @ 2 marks (graded 2:1:0)', 1)[1].strip())],
        'Description 2 × 2 (2:1:0); example 2 (2:1:0)')
    fix(7, [criterion('changes', 'chemical changes', 2, [0, 1, 2, 3],
                      'Two distinct changes, each graded 3:2:1:0. Published guidance: ' + graded_body(7))],
        '2 points × 3 marks (3:2:1:0)')

    test_examples = blocks[8].split('Describe two different uses', 1)[0].split('(2:1:0)', 1)[1].strip()
    fix(8, [criterion('test', 'sensory analysis test', 1, [0, 1, 2],
                      'One test, graded 2:1:0. Published examples: ' + test_examples)],
        '1 test × 2 marks (2:1:0)', totalMarks=2,
        questionText='Name one sensory analysis test used to determine a preferred product from two or more samples.',
        questionRef='2023 HL Section A Q8 — test')
    uses = deepcopy(old['he-2023-hl-sa-q8'])
    uses.update(id='he-2023-hl-sa-q8-uses', conceptId='sensory-analysis-uses',
                questionText='Describe two different uses of sensory analysis in the food industry.',
                questionRef='2023 HL Section A Q8 — uses', totalMarks=4,
                tariffModel=dict(kind='fixed', notation='2 points × 2 marks (2:1:0)'),
                rows=[criterion('uses', 'uses of sensory analysis', 2, [0, 1, 2],
                                'Two different uses, each graded 2:1:0. Published guidance: ' + blocks[8].split('2 points @ 2 marks (graded 2:1:0)', 1)[1].strip())],
                notes='Second separately priced prompt of Section A Q8; 4 marks. Original Q8 ID retains the 2-mark naming task.')
    added.append(uses)

    for n, headings in [(12, ['Fixed Rate', 'Variable Rate']), (13, ['Interest payable', 'Access to funds'])]:
        rows = []
        for i, heading in enumerate(headings):
            guidance = blocks[n].split(heading, 1)[1].split(headings[i + 1], 1)[0] if i == 0 else blocks[n].split(heading, 1)[1]
            rows.append(criterion(f'heading-{i+1}', heading, 1, [0, 2, 3],
                                  'One explanation, graded 3:2:0. Published guidance: ' + guidance.strip()))
        fix(n, rows, 'Two required headings × 3 marks (3:2:0)')

    assert len(fixes) == 14 and len(added) == 2
    return fixes, added


def write():
    fixes, added = build()
    correction_path = ROOT / 'scripts/markbank/card-corrections.json'
    corrections = json.loads(correction_path.read_text())
    corrections['home-economics'].update(fixes)
    correction_path.write_text(json.dumps(corrections, ensure_ascii=False, indent=1) + '\n')
    authored_path = ROOT / 'scripts/markbank/authored/home-economics.json'
    authored = json.loads(authored_path.read_text())
    by_id = {c['id']: i for i, c in enumerate(authored)}
    for card in added:
        if card['id'] in by_id:
            assert authored[by_id[card['id']]] == card
        else:
            authored.append(card)
    authored_path.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
    path = ROOT / f'public/exam-figures/home-economics/{FIGURE}.png'
    # This exact crop was visually inspected before binding the manifest.
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        fitz.open(ROOT / SCHEME)[5].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(55, 472, 548, 712)).save(path)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == FIGURE_SHA256, 'Inspected figure changed'
    manifest_path = ROOT / 'components/MarkBank/figures-home-economics.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    manifest[FIGURE] = dict(src=f'/exam-figures/home-economics/{FIGURE}.png',
                            md5=hashlib.md5(path.read_bytes()).hexdigest(), solution=True,
                            alt='Official table of food-poisoning bacteria and associated high-risk foods. Salmonella: eggs, meat, fish, poultry, milk, cheese. E-coli: milk, cheese, meat, polluted water. Listeria: cheese, pâté, cook chill foods, coleslaw, milk, meat, ice cream, seafood. Clostridium botulinum: canned fish/food, vacuum packed meat, milk, cheese, yoghurt. Clostridium perfringens/welchii: vegetables. Staphylococcus aureus: meat, milk, cheese. Bacillus cereus: cooked rice, cereals, herbs. Campylobacter: milk, poultry, shellfish. Each published list is non-exhaustive.',
                            attribution='SEC Home Economics 2023 Higher Level marking scheme, page 6 — © State Examinations Commission.',
                            sourceNote='Inspected crop from the hash-pinned official scheme; bounds [55, 472, 548, 712], rendered at 2×.')
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print('14 existing Section A cards corrected; 2 separately priced prompts added; all original IDs retained.')


if __name__ == '__main__':
    if '--write' in sys.argv:
        write()
    else:
        fixes, added = build()
        print(json.dumps(dict(corrections=fixes, added=added), ensure_ascii=False, indent=2))
