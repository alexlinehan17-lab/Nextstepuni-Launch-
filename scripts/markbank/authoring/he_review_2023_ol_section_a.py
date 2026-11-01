#!/usr/bin/env python3
"""Source-reviewed partial credit and response boundaries, 2023 Ordinary A.

Q4 has two independent prompts with separate tariffs. Keep functions on the
original ID and add its dietary-source task. Required table rows and the
credit-name/dependent-disadvantages task remain single responses.
"""
from copy import deepcopy
import hashlib
import json
import re
import sys
import fitz
from he_review_2023_hl import ROOT, tidy, criterion, between
from he_review_2023_ol import PAPER_A, SCHEME, HASHES

SELECTION_TOKENS = {
    1: ['each', 'following', 'or'], 2: ['three'], 3: ['following'],
    4: ['two', 'one'], 5: ['each', 'following', 'or'],
    6: ['one', 'each', 'following'], 7: ['three'],
    8: ['one', 'each', 'following'], 9: ['three'],
    10: ['each', 'following', 'or'], 11: ['one', 'two'],
    12: ['three'], 13: ['three'], 14: ['each', 'following'],
}


def build():
    for path in [PAPER_A, SCHEME]:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == HASHES[path]
    paper, scheme = fitz.open(ROOT / PAPER_A), fitz.open(ROOT / SCHEME)
    raw = '\n'.join(paper[n].get_text(clip=fitz.Rect(0, 0, 595, 745)) for n in range(2, 7))
    heads = list(re.finditer(r'(?m)^(\d{1,2})\.\s*\n', raw))
    assert [int(h[1]) for h in heads] == list(range(1, 15))
    for i, h in enumerate(heads):
        prompt = raw[h.end():heads[i + 1].start() if i + 1 < len(heads) else len(raw)]
        assert re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b', prompt, re.I) == SELECTION_TOKENS[int(h[1])]
    # True/false are required statements; word bank uses all three words;
    # cereal/product and baked-product/agent are required paired table rows.
    # Other counts request open examples, not choices among a finite list.
    raw = '\n'.join(scheme[n].get_text(clip=fitz.Rect(0, 0, 595, 810)) for n in range(5, 9))
    heads = list(re.finditer(r'(?m)^(\d{1,2})\.\s*\n', raw))
    assert [int(h[1]) for h in heads] == list(range(1, 16))  # source's stray 15 is inside Q14
    blocks = {int(h[1]): tidy(raw[h.end():heads[i + 1].start()]) for i, h in enumerate(heads[:13])}
    old = {c['id']: c for c in json.loads((ROOT / 'scripts/markbank/authored/home-economics.json').read_text())}
    fixes = {}

    def fix(n, rows, notation, **extra):
        fixes[f'he-2023-ol-sa-q{n}'] = dict(
            reason='2023 Ordinary Section A: paper pp3–7 and scheme pp6–9 independently reviewed. Preserve all source guidance and actual graded values. See he_review_2023_ol_section_a.py.',
            set=dict(rows=rows, tariffModel=dict(kind='fixed', notation=notation), **extra))

    def guidance(n):
        return blocks[n].split('(graded 2:1:0)', 1)[1].strip()

    for n, label in [(2, 'energy requirements'), (7, 'fibre'), (9, 'grilling'), (12, 'functions of textiles'), (13, 'microwave oven')]:
        text = guidance(n)
        assert text.endswith('etc.')
        extra = ' Use three different ways; do not count the same idea twice.' if n == 7 else ''
        fix(n, [criterion('points', label, 3, [0, 1, 2],
                          'Three distinct points, each graded 2:1:0.' + extra + ' Published guidance: ' + text)],
            '3 points × 2 (2:1:0)')
    assert 'brand;' in guidance(13) and guidance(13).endswith('after sales service; etc.')

    functions = guidance(4).split('Name one dietary source', 1)[0].strip()
    sources = guidance(4).split('(graded 2:1:0)', 1)[1].strip()
    assert functions.endswith('etc.') and sources.endswith('fish; etc.')
    fix(4, [criterion('functions', 'functions of iron', 2, [0, 1, 2],
                      'Two functions, each graded 2:1:0. Published guidance: ' + functions)],
        '2 functions × 2 (2:1:0)', totalMarks=4, questionText='State two functions of iron in the body.',
        questionRef='2023 OL Section A Q4 — functions')
    source = deepcopy(old['he-2023-ol-sa-q4'])
    source.update(id='he-2023-ol-sa-q4-source', conceptId='dietary-source-of-iron',
                  questionText='Name one dietary source of iron.', questionRef='2023 OL Section A Q4 — dietary source',
                  totalMarks=2, tariffModel=dict(kind='fixed', notation='1 source × 2 (2:1:0)'),
                  rows=[criterion('source', 'dietary source of iron', 1, [0, 1, 2],
                                  'One dietary source, graded 2:1:0. Published examples: ' + sources)],
                  notes='Separate printed prompt and separate 2-mark tariff. Original Q4 identity retains the 4-mark functions task.')

    table = between(blocks[8], 'Sponge cake', 'Lemon drizzle cake')
    sponge, bread = [x.strip() for x in table.split('Bread', 1)]
    lemon = blocks[8].split('Lemon drizzle cake', 1)[1].strip()
    examples = [('Sponge cake', sponge), ('Bread', bread), ('Lemon drizzle cake', lemon)]
    assert all(text.endswith('etc.') for _, text in examples)
    fix(8, [criterion(f'product-{i}', name, 1, [0, 1, 2],
                      'One suitable raising agent, graded 2:1:0. Use a different agent for each product. Published examples: ' + text)
            for i, (name, text) in enumerate(examples, 1)],
        '3 different agents × 2 (2:1:0)', stem='',
        questionText='Name one different raising agent suitable for each of the following baked products.\nSponge cake\nBread\nLemon drizzle cake')
    names = guidance(11).split('Outline two disadvantages', 1)[0].strip()
    disadvantages = guidance(11).split('(graded 2:1:0)', 1)[1].strip()
    assert names.endswith('etc.') and disadvantages.endswith('etc.')
    fix(11, [criterion('name', 'type of credit', 1, [0, 1, 2],
                       'Name one type, graded 2:1:0. Published examples: ' + names),
             criterion('disadvantages', 'disadvantages', 2, [0, 1, 2],
                       'Two disadvantages of the type you named, each graded 2:1:0. Use only guidance relevant to your chosen type. Published guidance: ' + disadvantages)],
        'Name 2; 2 disadvantages × 2 (all 2:1:0)')

    # True/false grids retain their verified answer identities. Remove earlier
    # extra commentary that could read as current social-benefit advice.
    for n in [1, 5, 10]:
        rows = deepcopy(old[f'he-2023-ol-sa-q{n}']['rows'])
        for row in rows:
            row['contextNote'] = 'Published 2023 examination answer. Graded 2:0; no partial credit.'
        fix(n, rows, '3 statements × 2 (2:0)')
    return fixes, [source]


def write():
    fixes, added = build()
    path = ROOT / 'scripts/markbank/card-corrections.json'; saved = json.loads(path.read_text())
    saved['home-economics'].update(fixes); path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + '\n')
    path = ROOT / 'scripts/markbank/authored/home-economics.json'; saved = json.loads(path.read_text())
    for c in added:
        i = next((i for i, old in enumerate(saved) if old['id'] == c['id']), None)
        if i is None: saved.append(c)
        else: saved[i] = c
    path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + '\n')
    print(f'Section A: {len(fixes)} corrected cards, one separate iron-source task; Q3, Q6 and recovered Q14 verified unchanged.')


if __name__ == '__main__':
    if '--write' in sys.argv: write()
    else: print(json.dumps(build(), ensure_ascii=False, indent=2))
