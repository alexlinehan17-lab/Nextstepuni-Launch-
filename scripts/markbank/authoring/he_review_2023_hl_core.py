#!/usr/bin/env python3
"""Review the 2023 Higher core option, retaining consolidated progress IDs."""
from copy import deepcopy
import hashlib
import json
import re
import sys

import fitz
from he_review_2023_hl import ROOT, PAPER, SCHEME, HASHES, tidy, between, criterion
from he_review_2023_hl_section_b_rest import paragraphs


def build():
    for path, sha in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha
    paper, scheme = fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)
    p8 = tidy(paper[7].get_text())
    tasks = p8.split('4.(a)', 1)[1]
    directives = re.findall(r'\b(?:choose|one\s+(?:of|method)|a type of material|any\s+\w+|either|or|answer\s+\w+\s+of)\b', tasks, re.I)
    # "one of the most important industries" is source prose, not a choice.
    assert directives == ['one of', 'one method', 'a type of material', 'or'], directives
    sections = {'a': between(p8, '4.(a)', '4.(b)'), 'b': between(p8, '4.(b)', '4.(c)'), 'c': p8.split('4.(c)', 1)[1]}
    s = {n: tidy('\n'.join(line for line in scheme[n - 1].get_text().splitlines() if line.strip() != str(n))).replace('non- biodegradable', 'non-biodegradable')
         for n in [26, 27, 28]}
    fixes = {}
    def put(part, roman, marks, notation, rows, variants=None, suffix=''):
        q = sections[part]
        text = between(q, f'({roman})', f'({marks} marks)')
        assert not re.search(r'\((?:i|ii|iii)\)', text)
        value = dict(questionText=text, stem=q.split('(i)', 1)[0].strip(), tariffModel=dict(kind='fixed', notation=notation), rows=rows,
                     sourceMaterial=dict(kind='source-question', label='OFFICIAL QUESTION', title='Source and question', pages=[8],
                                         attribution='SEC Home Economics 2023 Higher Level examination paper — © State Examinations Commission.',
                                         presentationNote='Open the original examination page to review this task in context.'),
                     notes='Independently reviewed against the paper and full scheme. Open choices stay one response with source-backed answer routes. See he_review_2023_hl_core.py.')
        if variants:
            value.update(answerVariants=variants, questionRef=f'2023 HL Section C Q4({part})({roman})',
                         conceptId='evaluating-one-method-of-cooking-meat' if roman == 'ii' else 'packaging-perishable-foods')
        fixes[f'he-2023-hl-sc-q4{part}{roman}{suffix}'] = dict(
            reason='Independent 2023 Higher core review: original context, complete source guidance and partial marks; consolidated identities and withdrawn-card aliases retained.', set=value)

    safety = between(s[26], '3 points @ 4 marks (graded 4:2:0)', '(ii)')
    assert safety.endswith('ensure full traceability; etc.')
    put('a', 'i', 12, '3 points × 4 (4:2:0)', [criterion('measures', 'measures that have been implemented in the Irish food industry', 3, [0, 2, 4],
        'Discuss three distinct measures, graded 4:2:0. Published guidance: ' + safety)])
    cooking = s[26].split('(24 marks)', 1)[1] + ' ' + s[27].split('(iii)', 1)[0]
    methods = paragraphs(cooking, ['Boiling', 'Poaching', 'Steaming', 'Stewing', 'Braising', 'Pressure cooking', 'Roasting', 'Grilling/Barbecuing', 'Frying'])
    variants = []
    for name, detail in methods:
        principle, effects = detail.split('affects', 1)
        assert principle.strip().endswith('etc.') and effects.strip().endswith('etc.')
        variants.append(dict(id=re.sub(r'[^a-z]+', '-', name.lower()), label=name, rows=[
            dict(id='name', kind='point', verbatim=name, marks=3),
            criterion('principle', 'underlying principle', 3, [0, 2, 3], 'Three distinct points for your chosen method, each graded 3:2:0. Published guidance: ' + principle.strip()),
            criterion('effects', 'how the cooking method chosen affects the meat', 4, [0, 2, 3], 'Four distinct effects of the same method, each graded 3:2:0. Published guidance: ' + effects.strip())]))
    variants.append(dict(id='another-method', label='Another cooking method', rows=[
        criterion('name', 'name of cooking method', 1, [0, 3], 'Name the method you evaluated. The question leaves the choice open.'),
        criterion('principle', 'underlying principle', 3, [0, 2, 3], 'Three accurate points for your method, each graded 3:2:0. The nine other routes contain the printed examples; no model is supplied for another method.'),
        criterion('effects', 'how the cooking method chosen affects the meat', 4, [0, 2, 3], 'Four accurate effects on meat, each graded 3:2:0. Keep the effects tied to the same method; the scheme gives no model for another method.')]))
    put('a', 'ii', 24, 'Name 3 (3:0); principle 3 × 3, effects 4 × 3 (3:2:0)', deepcopy(variants[0]['rows']), variants, '-boiling')
    packaging = paragraphs(between(s[27], '1 reference to suitability for purpose, 1 reference to environmental impact', 'and 4.(b)'),
                           ['Glass', 'Metal', 'Paper', 'Plastic'])
    variants = []
    for name, detail in packaging:
        purpose, environment = detail.split('etc.', 1)
        assert environment.strip().endswith('etc.')
        variants.append(dict(id=name.lower(), label=name, rows=[
            criterion('name', name, 1, [0, 2, 4], 'Identify the material you assessed, graded 4:2:0.'),
            criterion('purpose', 'suitability for purpose', 1, [0, 3, 5], 'One point on suitability for purpose, graded 5:3:0. Published guidance: ' + purpose.strip() + ' etc.'),
            criterion('environment', 'environmental impact', 1, [0, 3, 5], 'One point on environmental impact, graded 5:3:0. Published guidance: ' + environment.strip())]))
    variants.append(dict(id='another-material', label='Another packaging material', rows=[
        criterion('name', 'Name', 1, [0, 2, 4], 'Identify a material suitable for packaging perishable foods, graded 4:2:0.'),
        criterion('purpose', 'suitability for purpose', 1, [0, 3, 5], 'Assess the suitability of that material, graded 5:3:0. The scheme prints examples for glass, metal, paper and plastic; it gives no model for another material.'),
        criterion('environment', 'environmental impact', 1, [0, 3, 5], 'Assess the environmental impact of the same material, graded 5:3:0. The scheme gives no model for another material.')]))
    put('a', 'iii', 14, 'Name 4 (4:2:0), suitability 5 and environment 5 (5:3:0)', deepcopy(variants[0]['rows']), variants, '-glass')
    expenditure = paragraphs(s[27].split('3 points @ 5 marks (graded 5:3:0)', 1)[1],
                             ['family stage', 'family circumstances', 'gender', 'social class', 'culture some'])
    expenditure = [(h.removesuffix(' some'), ('some ' if h.endswith(' some') else '') + body) for h, body in expenditure]
    put('b', 'i', 15, '3 points × 5 (5:3:0)', [criterion('factors', 'socio-economic factors', 3, [0, 3, 5],
        'Evaluate three distinct points, each graded 5:3:0. Published guidance:\n\n' + '\n\n'.join(h + ' ' + body for h, body in expenditure))])
    support = between(s[28].split('4.(c)', 1)[0], '3 points @ 5 marks (graded 5:3:0)', ' or')
    assert support.endswith('fuel allowances; etc.')
    put('b', 'ii', 15, '3 points × 5 (5:3:0)', [criterion('state', 'economic function in society', 3, [0, 3, 5],
        'Describe three distinct points, each graded 5:3:0. Published 2023 marking guidance: ' + support)])
    microwave = s[28].split('4.(c)', 1)[1]
    contribution = between(microwave, '3 points @ 5 marks (graded 5:3:0)', '(ii)')
    assert contribution.endswith('food can be defrosted; etc.')
    put('c', 'i', 15, '3 points × 5 (5:3:0)', [criterion('contribution', 'contribution of the microwave oven', 3, [0, 3, 5],
        'Evaluate three distinct points, each graded 5:3:0. Published guidance: ' + contribution)])
    principle = microwave.split('5 points @ 3marks (graded 3:2:0)', 1)[1].strip()
    assert principle.endswith('incorporated grill browns food by radiation; etc.')
    put('c', 'ii', 15, '5 points × 3 (3:2:0)', [criterion('principle', 'working principle of the microwave oven', 5, [0, 2, 3],
        'Describe five distinct points, each graded 3:2:0. Published guidance: ' + principle)])
    assert len(fixes) == 7
    return fixes


def write():
    path = ROOT / 'scripts/markbank/card-corrections.json'
    saved = json.loads(path.read_text()); saved['home-economics'].update(build())
    # Update only live cards; existing drop/replacement records are untouched.
    path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + '\n')
    print('Core option: seven existing tasks corrected; all 110 offered marks retained.')


if __name__ == '__main__':
    if '--write' in sys.argv:
        write()
    else:
        print(json.dumps(build(), ensure_ascii=False, indent=2))
