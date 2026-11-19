#!/usr/bin/env python3
"""Review Textiles 2023 Higher: linked outfit context and one open blend profile."""
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
    p6 = tidy(paper[5].get_text())
    tasks = p6.split('2.(a)', 1)[1]
    directives = re.findall(r'\b(?:choose|one\s+(?:of|design principle|blended fabric|career opportunity)|any\s+\w+|either|or|answer\s+\w+\s+of)\b', tasks, re.I)
    assert directives == ['one design principle', 'one blended fabric', 'or', 'one career opportunity'], directives
    a, b, c = between(p6, '2.(a)', '2.(b)'), between(p6, '2.(b)', '2.(c)'), p6.split('2.(c)', 1)[1]
    s21, s22 = [tidy('\n'.join(line for line in scheme[n - 1].get_text().splitlines()
                               if line.strip() != str(n))) for n in [21, 22]]
    fixes = {}
    outfit = between(a, '(i)', '(12 marks)')
    def put(key, question, stem, notation, rows, variants=None):
        value = dict(questionText=question, stem=stem, tariffModel=dict(kind='fixed', notation=notation), rows=rows,
                     sourceMaterial=dict(kind='source-question', label='OFFICIAL QUESTION', title='Source and question', pages=[6],
                                         attribution='SEC Home Economics 2023 Higher Level examination paper — © State Examinations Commission.',
                                         presentationNote='Open the original examination page to review this task in context.'),
                     notes='Independently reviewed against the paper and full scheme. Required headings and open choices remain one response. See he_review_2023_hl_elective2.py.')
        if variants:
            value.update(answerVariants=variants, questionRef='2023 HL Section C E2 Q2(b)' if key.endswith('b-wool-nylon') else '2023 HL Section C E2 Q2(a)(iii)')
        fixes['he-2023-hl-sc-q2' + key] = dict(reason='Independent 2023 Higher Elective 2 review: original linked context, complete source guidance and published partial marks.', set=value)

    stem = a.split('(i)', 1)[0].strip()
    sketch = between(s21, 'sketch should show', 'description colour;')
    description = 'colour; ' + between(s21, 'description colour;', '(ii)')
    put('ai', outfit, stem, 'Sketch 6 (6:4:2:0), description 3 × 2 (2:1:0)', [
        criterion('sketch', 'Sketch', 1, [0, 2, 4, 6], 'The sketch is graded as one response, using 6:4:2:0. Published guidance: sketch should show ' + sketch),
        criterion('description', 'description', 3, [0, 1, 2], 'Describe three distinct features of your own outfit, each graded 2:1:0. Published guidance: ' + description)])
    # The independent card must retain the earlier prompt that defines "outfit".
    linked_stem = stem + '\n\n' + outfit
    fabric = between(s21, 'fabric silk;', 'reason lightweight;')
    reason = 'lightweight; ' + between(s21, 'reason lightweight;', '(iii)')
    put('aii', between(a, '(ii)', '(6 marks)'), linked_stem, 'Fabric 3 (3:0), reason 3 (3:2:0)', [
        criterion('fabric', 'fabric', 1, [0, 3], 'Suggest one suitable fabric for the outfit you designed. Published guidance: silk; ' + fabric),
        criterion('reason', 'reason', 1, [0, 2, 3], 'Give a reason that applies to the fabric and outfit you chose, graded 3:2:0. Published guidance: ' + reason)])
    principles = paragraphs(between(s21, 'Name 2 marks (graded 2:0), evaluate 5 marks (graded 5:3:0)', 'and 2.(b)'),
                            ['balance can', 'emphasis achieved', 'proportion relationship', 'rhythm associated'])
    principles = [(h.split(' ', 1)[0], h.split(' ', 1)[1] + ' ' + body) for h, body in principles]
    variants = [dict(id=h, label=h.capitalize(), rows=[
        dict(id='name', kind='point', verbatim=h, marks=2),
        criterion('evaluate', 'evaluate', 1, [0, 3, 5], 'Evaluate how this principle applies to your own outfit, graded 5:3:0. Published guidance: ' + body)])
        for h, body in principles]
    variants.append(dict(id='another-principle', label='Another design principle', rows=[
        criterion('name', 'Name', 1, [0, 2], 'Name the design principle you evaluated. The paper leaves the choice open.'),
        criterion('evaluate', 'evaluate', 1, [0, 3, 5], 'Evaluate how that principle applies to your own outfit, graded 5:3:0. The scheme gives examples for balance, emphasis, proportion and rhythm; it gives no model for another principle.')]))
    put('aiii', between(a, '(iii)', '(7 marks)'), linked_stem, 'Name 2 (2:0), evaluate 5 (5:3:0)', deepcopy(variants[0]['rows']), variants)

    production = s21.split('Production Blend: Wool and Nylon', 1)[1] + ' ' + s22.split('Properties', 1)[0]
    wool = 'wool ' + between(production, 'wool ', 'nylon two chemicals')
    nylon = 'nylon two chemicals ' + between(production, 'nylon two chemicals', 'Blend Cotton and Polyester')
    cotton = 'cotton boll ' + between(production, 'cotton boll ', 'polyester viscous liquid')
    polyester = 'polyester viscous liquid ' + between(production, 'polyester viscous liquid', 'Blending')
    blending = 'Blending ' + production.split('Blending', 1)[1].strip()
    properties = dict(paragraphs(between(s22, 'Properties', 'Uses'), ['wool', 'nylon', 'cotton', 'polyester']))
    uses = between(s22, 'Uses', 'or 2.(c)')
    assert uses.endswith('bed linen; etc.')
    variants = []
    for identity, label, first, second, guidance in [
        ('wool-nylon', 'Wool and nylon', 'wool', 'nylon', wool + '\n\n' + nylon),
        ('cotton-polyester', 'Cotton and polyester', 'cotton', 'polyester', cotton + '\n\n' + polyester),
    ]:
        variants.append(dict(id=identity, label=label, rows=[
            criterion('production', 'fabric production', 3, [0, 2, 3], 'Three distinct production points for your chosen blend, each graded 3:2:0. Published component and blending guidance:\n\n' + guidance + '\n\n' + blending),
            criterion('properties', 'fabric properties', 3, [0, 1], 'Three properties of the blend, each graded 1:0. Published component properties:\n\n' + first + ' ' + properties[first] + '\n\n' + second + ' ' + properties[second]),
            criterion('uses', 'uses', 3, [0, 1], 'Three uses, each graded 1:0. Published guidance: ' + uses)]))
    variants.append(dict(id='another-blend', label='Another blended fabric', rows=[
        criterion('production', 'fabric production', 3, [0, 2, 3], 'Three accurate production points for the blend you chose, each graded 3:2:0. The scheme prints examples for wool/nylon and cotton/polyester only. General blending guidance: ' + blending),
        criterion('properties', 'fabric properties', 3, [0, 1], 'Three accurate properties of the blend you chose, each graded 1:0. The other routes contain the printed component examples.'),
        criterion('uses', 'uses', 3, [0, 1], 'Three valid uses of the blend, each graded 1:0. Published guidance: ' + uses)]))
    put('b-wool-nylon', 'Write a profile ' + between(b, 'Write a profile', '(15 marks)'), b.split('Write a profile', 1)[0].strip(),
        'Production 3 × 3 (3:2:0), properties 3 × 1 (1:0), uses 3 × 1 (1:0)', deepcopy(variants[0]['rows']), variants)
    fixes['he-2023-hl-sc-q2b-wool-nylon']['set']['conceptId'] = 'blended-fabric-profile'
    fashion = paragraphs(between(s22, '3 points @ 3 marks (graded 3:2:0)', '(ii)'), ['pattern bold', 'influences contemporary', 'accessories draws'])
    fashion = [(h.split(' ', 1)[0], h.split(' ', 1)[1] + ' ' + body) for h, body in fashion]
    put('ci', between(c, '(i)', '(9 marks)'), c.split('(i)', 1)[0].strip(), '3 required headings × 3 (3:2:0)', [
        criterion(f'heading-{i}', h, 1, [0, 2, 3], 'Discuss this required heading, graded 3:2:0. Published guidance: ' + body)
        for i, (h, body) in enumerate(fashion, 1)])
    # Q2(c)(ii) was recovered and independently reviewed in he_review_2023_hl.py.
    assert len(fixes) == 5
    return fixes


def write():
    path = ROOT / 'scripts/markbank/card-corrections.json'
    saved = json.loads(path.read_text()); saved['home-economics'].update(build())
    # Replaces the old unreviewed row sources on the one live blend card.
    # All withdrawn IDs and their replacementId mappings remain unchanged.
    path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + '\n')
    print('Elective 2: five existing tasks corrected; previously reviewed career task retained.')


if __name__ == '__main__':
    if '--write' in sys.argv:
        write()
    else:
        print(json.dumps(build(), ensure_ascii=False, indent=2))
