#!/usr/bin/env python3
"""Review 2023 Ordinary Section B: full guidance, headings and exact tariffs."""
from copy import deepcopy
import hashlib
import json
import re
import sys
import fitz
from he_review_2023_hl import ROOT, tidy, between, criterion
from he_review_2023_hl_section_b_rest import paragraphs
from he_review_2023_ol import PAPER_BC, SCHEME, HASHES, page_text

SOURCE_CLARIFICATIONS = {
    'pollution': dict(url='https://www.epa.ie/environment-and-you/freshwater-and-marine/water-quality-and-agriculture/',
                      checked='2026-11-01', note='EPA identifies excess phosphorus as a pressure on water quality. The scheme phrase “use phosphate detergents” appears to be an error; retain it as source wording and distinguish the clarification.'),
    'detergents': dict(url='https://www.hsa.ie/eng/your_industry/chemicals/legislation_enforcement/detergents/',
                       checked='2026-11-01', note='HSA describes restrictions on phosphorus compounds in consumer detergents.'),
    'intestacy': dict(url='https://www.courts.ie/guides/explaining-probate', checked='2026-11-01',
                      note='Courts Service explains that without a will the rules of intestacy determine distribution among family members. No automatic sizeable State share follows merely from not making a will.'),
}


def build():
    for path in [PAPER_BC, SCHEME]:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == HASHES[path]
    paper, scheme = fitz.open(ROOT / PAPER_BC), fitz.open(ROOT / SCHEME)
    p = {n: page_text(paper, n) for n in [2, 3, 4]}
    directives = re.findall(r'\b(?:choose|one\s+(?:of|type)|any\s+\w+|either|or|answer\s+\w+\s+of)\b', ' '.join(p.values()), re.I)
    # Outer question choice; buying OR renting; "one of the best places" is
    # introductory prose, not a selection. Bar selection already has one card.
    assert directives == ['any other', 'or', 'one of'], directives
    qs = {1: p[2].rsplit('Question 1', 1)[1], 2: between(p[3], 'Question 2', 'Question 3'),
          3: p[3].split('Question 3', 1)[1], 4: between(p[4], 'Question 4', 'Question 5'),
          5: p[4].split('Question 5', 1)[1]}
    s = {n: page_text(scheme, n) for n in range(11, 16)}
    fixes, added = {}, []
    old = {c['id']: c for c in json.loads((ROOT / 'scripts/markbank/authored/home-economics.json').read_text())}

    def put(q, part, marks, notation, rows):
        question = between(qs[q], f'({part})', f'({marks} marks)')
        assert not re.search(r'\([abcd]\)', question), question
        stem = qs[q].split('(a)', 1)[0].strip()
        if q == 1: stem = stem.split('The table below', 1)[0].strip()
        values = dict(questionText=question, stem=stem, totalMarks=marks,
                      tariffModel=dict(kind='fixed', notation=notation), rows=rows,
                      sourceMaterial=dict(kind='source-question', label='OFFICIAL QUESTION', title='Source and question', pages=[2 if q == 1 else 3 if q in (2, 3) else 4],
                                          attribution='SEC Home Economics 2023 Ordinary Level examination paper — © State Examinations Commission.',
                                          presentationNote='Open the original examination page to review this task in context.'),
                      notes='Paper and complete scheme independently reviewed, including required headings and partial marks. See he_review_2023_ol_section_b.py.')
        fixes[f'he-2023-ol-sb-q{q}{part}'] = dict(reason='2023 Ordinary Section B source review: complete question wording and guidance, exact per-point grades and published response boundaries.', set=values)

    def body(text, grade):
        result = text.split(f'(graded {grade})', 1)[1].strip()
        assert result.endswith('etc.'), result
        return result

    protein = between(s[11], '(b)', '(c)')
    classes = body(protein.split('• dietary sources', 1)[0], '3:2:0')
    sources = body(between(protein, '• dietary sources', '• functions in the body'), '4:2:0')
    functions = body(protein.split('• functions in the body', 1)[1], '4:2:0')
    put(1, 'b', 26, '2 classes × 3 (3:2:0); 3 sources × 4; 2 functions × 4 (4:2:0)', [
        criterion('classes', 'classification', 2, [0, 2, 3], 'Two classifications, graded 3:2:0. Published guidance: ' + classes),
        criterion('sources', 'dietary sources', 3, [0, 2, 4], 'Three sources, graded 4:2:0. Published guidance: ' + sources),
        criterion('functions', 'functions in the body', 2, [0, 2, 4], 'Two functions, graded 4:2:0. Published guidance: ' + functions)])
    put(1, 'c', 10, '2 points × 5 (5:3:0)', [criterion('water', 'importance of including water', 2, [0, 3, 5],
        'Two points explaining its importance to someone who plays sport, each graded 5:3:0. Published guidance: ' + body(between(s[11], '(c)', '(d)'), '5:3:0'))])
    put(1, 'd', 20, '4 guidelines × 5 (5:3:0)', [criterion('costs', 'reduce household costs', 4, [0, 3, 5],
        'Four distinct guidelines, each graded 5:3:0. Published guidance: ' + body(s[11].split('(d)', 1)[1], '5:3:0'))])
    tender = s[12].split('(c)', 1)[1].split('Spaghetti Bolognese', 1)[0].strip()
    put(2, 'c', 10, '2 methods × 5 (5:3:0)', [criterion('methods', 'methods of tenderising meat', 2, [0, 3, 5],
        'Two different methods, each graded 5:3:0. Published guidance: ' + body(tender, '5:3:0'))])
    hygiene = paragraphs(between(s[13], '(1 reference to preparation, 1 reference to storage + 2 other points)', '(b)'), ['preparation:', 'storage:'])
    rows = [criterion(f'heading-{i}', heading.rstrip(':'), 1, [0, 2, 4],
                      'One required point, graded 4:2:0. Published guidance: ' + text) for i, (heading, text) in enumerate(hygiene, 1)]
    rows.append(criterion('other', '2 other points', 2, [0, 2, 4], 'Two further distinct points on either heading, each graded 4:2:0. Do not count a point already used above again.'))
    put(3, 'a', 16, '4 × 4 (4:2:0): preparation 1, storage 1, other 2', rows)
    fridge = between(s[13], '(b)', '(c)')
    names = body(fridge.split('• guidelines for use', 1)[0], '2:1:0')
    use = body(between(fridge, '• guidelines for use', '• care and cleaning'), '4:2:0')
    care = body(fridge.split('• care and cleaning', 1)[1], '4:2:0')
    put(3, 'b', 26, 'Type 2 (2:1:0); use 3 × 4; care/cleaning 3 × 4 (4:2:0)', [
        criterion('type', 'type of refrigeration appliance', 1, [0, 1, 2], 'Name the type studied, graded 2:1:0. Published examples: ' + names),
        criterion('use', 'guidelines for use', 3, [0, 2, 4], 'Three guidelines for the appliance studied, each graded 4:2:0. Published guidance: ' + use),
        criterion('care', 'care and cleaning', 3, [0, 2, 4], 'Three guidelines for the same appliance, each graded 4:2:0. Published guidance: ' + care)])
    put(3, 'c', 8, '2 points × 4 (4:2:0)', [criterion('technology', 'technology', 2, [0, 2, 4],
        'Two points, each graded 4:2:0. Published guidance: ' + body(s[13].split('(c)', 1)[1], '4:2:0'))])
    housing = paragraphs(between(s[14], '(grades 5:3:0)', '(b)'), ['family needs:', 'cost:', 'location:', 'trends in housing development:'])
    put(4, 'a', 20, '4 required factors × 5 (5:3:0)', [criterion(f'factor-{i}', heading.rstrip(':'), 1, [0, 3, 5],
        'Explain this required factor, graded 5:3:0. Published guidance: ' + text) for i, (heading, text) in enumerate(housing, 1)])
    put(4, 'b', 15, '3 advantages × 5 (5:3:0)', [criterion('insurance', 'advantages', 3, [0, 3, 5],
        'Three advantages, each graded 5:3:0. Published guidance: ' + body(between(s[14], '(b)', '(c)'), '5:3:0'))])
    pollution = body(s[14].split('(c)', 1)[1], '5:3:0')
    assert pollution.startswith('use phosphate detergents;')
    put(4, 'c', 15, '3 ways × 5 (5:3:0)', [criterion('pollution', 'reduce pollution', 3, [0, 3, 5],
        'Three different ways, each graded 5:3:0.\n\nSource clarification: the printed phrase “use phosphate detergents” appears to be an error. Excess phosphorus contributes to water pollution; reducing it is the relevant principle. The original wording is preserved below so the distinction is clear.\n\nPublished 2023 scheme wording: ' + pollution)])
    roles = body(between(s[15], '(a)', '(b)'), '5:3:0')
    put(5, 'a', 20, '4 points × 5 (5:3:0)', [criterion('roles', 'roles and responsibilities', 4, [0, 3, 5],
        'Discuss four points, each graded 5:3:0. The paper requires roles and responsibilities; the scheme does not reserve a fixed number for either heading. Published guidance: ' + roles)])
    causes = body(between(s[15], '(i)', '(ii)'), '5:3:0')
    ways = body(between(s[15], '(ii)', '(c)'), '5:3:0')
    put(5, 'b', 20, '2 causes × 5 (5:3:0)', [criterion('causes', 'causes of conflict', 2, [0, 3, 5],
        'Identify two causes, each graded 5:3:0. Published guidance: ' + causes)])
    c = fixes['he-2023-ol-sb-q5b']['set']
    c.update(totalMarks=10, questionRef='2023 OL Section B Q5(b)(i)', questionText=between(qs[5], '(i)', '(ii)'))
    resolution = deepcopy(old['he-2023-ol-sb-q5b'])
    resolution.update(id='he-2023-ol-sb-q5bii', conceptId='dealing-with-family-conflict', totalMarks=10,
                      questionRef='2023 OL Section B Q5(b)(ii)', questionText=between(qs[5], '(ii)', '(20 marks)'),
                      stem=c['questionText'], tariffModel=dict(kind='fixed', notation='2 ways × 5 (5:3:0)'),
                      rows=[criterion('ways', 'ways of dealing with this conflict', 2, [0, 3, 5],
                                      'Two ways of dealing with conflict between teenagers and adults, each graded 5:3:0. Published guidance: ' + ways)],
                      sourceMaterial=deepcopy(c['sourceMaterial']),
                      notes='Separately priced 10-mark task. Carry the teenage/adult conflict context from (i); original Q5b ID retains causes.')
    added.append(resolution)
    will = body(s[15].split('(c)', 1)[1], '5:3:0')
    put(5, 'c', 10, '2 reasons × 5 (5:3:0)', [criterion('will', 'reasons', 2, [0, 3, 5],
        'Two reasons, each graded 5:3:0.\n\nSource clarification: the scheme’s statement that a sizeable portion automatically goes to the State without a will is not a general rule. Intestacy rules determine distribution among family members. The historical wording is reproduced below; use accurate reasons such as recording wishes and appointing an executor.\n\nPublished 2023 scheme wording: ' + will)])
    return fixes, added


def write():
    fixes, added = build()
    path = ROOT / 'scripts/markbank/card-corrections.json'; saved = json.loads(path.read_text());saved['home-economics'].update(fixes)
    path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + '\n')
    path = ROOT / 'scripts/markbank/authored/home-economics.json'; saved = json.loads(path.read_text())
    for c in added:
        i = next((i for i, old in enumerate(saved) if old['id'] == c['id']), None)
        if i is None: saved.append(c)
        else: saved[i] = c
    path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + '\n')
    print(f'Section B: {len(fixes)} existing cards corrected, one separately priced conflict-resolution task added.')


if __name__ == '__main__':
    if '--write' in sys.argv: write()
    else: print(json.dumps(build(), ensure_ascii=False, indent=2))
