#!/usr/bin/env python3
"""Review every 2023 Ordinary Section C response; preserve its existing ID."""
from copy import deepcopy
import hashlib
import json
import re
import sys
import fitz
from he_review_2023_hl import ROOT, between, criterion
from he_review_2023_hl_section_b_rest import paragraphs
from he_review_2023_ol import PAPER_BC, SCHEME, HASHES, page_text

FIGURE = 'home-economics-2023-ol-sc-q2ai-fashion'
FIGURE_SHA = 'abc4a18b3ad50a66911277a8dec4db76641d17e6255b082fd81337a068934ae7'
SELECTORS = {
    5: ['or', 'one', 'or', 'either', 'or', 'either', 'or', 'three', 'three', 'three', 'one', 'or', 'following', 'three'],
    6: ['either', 'or', 'one', 'one', 'or', 'two'],
    7: ['either', 'or', 'one', 'three', 'three', 'or', 'three'],
    8: ['either', 'or', 'three', 'or', 'following', 'three', 'three', 'or', 'each'],
}


def build():
    for path in [PAPER_BC, SCHEME]:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == HASHES[path]
    paper, scheme = fitz.open(ROOT / PAPER_BC), fitz.open(ROOT / SCHEME)
    p = {n: page_text(paper, n) for n in range(5, 9)}
    for n, text in p.items():
        assert re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b', text, re.I) == SELECTORS[n]
    # Outer a + either b/c applies to all electives/core; all offered tasks
    # are practised. One renewable source, design method, fabric finish and
    # statutory scheme are open choices. Required headings stay together.
    # "and/or" accepts mixed lifestyle/dietary answers; "each other" is prose.
    questions, stems = {}, {}
    for q in range(1, 5):
        text = p[q + 4]
        for part, next_part in [('a', 'b'), ('b', 'c'), ('c', None)]:
            block = text.split(f'{q}.({part})', 1)[1]
            if next_part: block = block.split(f'{q}.({next_part})', 1)[0]
            matches = list(re.finditer(r'\((i{1,3}|iv)\)\s+(.*?)\((\d+) marks\)', block))
            expect = ['i', 'ii', 'iii'] + (['iv'] if q == 3 else []) if part == 'a' else ['i', 'ii']
            if q == 2 and part == 'a': expect = ['i', 'ii']
            assert [m[1] for m in matches] == expect, (q, part, matches)
            stem = block[:matches[0].start()].strip()
            if q == 1 and part == 'a': stem = stem.split('(www.victoriaplum.com)', 1)[0].strip()
            if q == 2 and part == 'a': stem = stem.split('(www.pinterest.com)', 1)[0].strip()
            for m in matches:
                questions[(q, part + m[1])] = (m[2].strip(), int(m[3]))
                stems[(q, part + m[1])] = stem
    assert len(questions) == 28
    s = {n: page_text(scheme, n) for n in range(16, 25)}
    fixes = {}

    def put(q, part, rows, notation, variants=None, **extra):
        key = f'he-2023-ol-sc-q{q}{part}'
        question, marks = questions[(q, part)]
        value = dict(questionText=question, stem=stems[(q, part)], totalMarks=marks,
                     rows=rows, tariffModel=dict(kind='fixed', notation=notation),
                     sourceMaterial=dict(kind='source-question', label='OFFICIAL QUESTION', title='Source and question', pages=[q + 4],
                                         attribution='SEC Home Economics 2023 Ordinary Level examination paper — © State Examinations Commission.',
                                         presentationNote='Open the original examination page to review this task in context.'),
                     notes='Full paper and scheme source review, including every required heading and published partial grade. See he_review_2023_ol_section_c.py.')
        if variants: value['answerVariants'] = variants
        value.update(extra)
        fixes[key] = dict(reason='2023 Ordinary Section C: preserve full source context, guidance, paired choices and exact grading steps on the existing identity.', set=value)

    def body(text, grade):
        answer = text.split(f'(graded {grade})', 1)[1].strip()
        assert answer.endswith('etc.'), answer
        return answer

    def points(q, part, heading, count, grade, text, **extra):
        steps = sorted(int(x) for x in grade.split(':'))
        assert text.endswith('etc.'), (q, part, text)
        put(q, part, [criterion('points', heading, count, steps,
                               f'{count} distinct points, each graded {grade}. Published 2023 scheme guidance: ' + text)],
            f'{count} points × {steps[-1]} ({grade})', **extra)

    points(1, 'ai', 'suitability of the bathroom space', 4, '5:3:0', body(between(s[16], '(i)', '(ii)'), '5:3:0'),
           figureKey='', questionFigureKey='home-economics-2023-ol-paper-p05-i0', questionFigureIncludesPrompt=False)
    points(1, 'aii', 'heating system', 3, '5:3:0', body(between(s[16], '(ii)', '(iii)'), '5:3:0'), figureKey='', stem='')
    points(1, 'aiii', 'safe use of electricity', 3, '5:3:0', body(s[16].split('(iii)', 1)[1], '5:3:0'), stem='')
    points(1, 'bi', 'energy efficiency', 3, '5:3:0', body(between(s[17].split('1.(b)', 1)[1].split('1.(c)', 1)[0], '(i)', '(ii)'), '5:3:0'))
    renewables = between(s[17], '2 advantages @ 5 marks (graded 5:3:0)', ' or 1.(c)')
    names = ['solar', 'wood', 'wind', 'hydropower', 'bio energy', 'geothermal']
    chunks = re.split(r'\b(' + '|'.join(names) + r')\s+', renewables)
    assert not chunks[0] and chunks[1::2] == names
    variants = []
    for name, detail in zip(chunks[1::2], chunks[2::2]):
        detail = detail.strip()
        assert detail.endswith('etc.') or name == 'bio energy'
        variants.append(dict(id=name.replace(' ', '-'), label=name.capitalize(), rows=[
            criterion('name', name, 1, [0, 3, 5], 'Name the renewable source, graded 5:3:0.'),
            criterion('advantages', 'advantages', 2, [0, 3, 5], 'Two advantages of this source, each graded 5:3:0. Published 2023 example guidance: ' + detail)]))
    variants.append(dict(id='another-source', label='Another renewable source', rows=[
        criterion('name', 'renewable energy source', 1, [0, 3, 5], 'Name one renewable energy source, graded 5:3:0. The paper leaves this choice open.'),
        criterion('advantages', 'advantages', 2, [0, 3, 5], 'Outline two accurate advantages of your source, each graded 5:3:0. The other routes reproduce the six printed examples; the scheme prints no model for another source.')]))
    put(1, 'bii', deepcopy(variants[0]['rows']), 'Name 5; 2 advantages × 5 (all 5:3:0)', variants)
    water = between(s[17], '1.(c)', '(ii)')
    water = paragraphs(water.split('(15 marks)', 1)[1], ['stopcock:', 'storage tank:', 'overflow pipe:'])
    put(1, 'ci', [criterion(f'part-{i}', name.rstrip(':'), 1, [0, 3, 5],
                           'Explain this required function, graded 5:3:0. Published guidance: ' + text) for i, (name, text) in enumerate(water, 1)],
        '3 required functions × 5 (5:3:0)')
    water_use = s[17].split('1.(c)', 1)[1].split('(ii)', 1)[1]
    points(1, 'cii', 'reduce water usage', 3, '5:3:0', body(water_use, '5:3:0'))

    clothes = paragraphs(between(s[18], '(18 marks)', '(ii)'), ['comfort:', 'function:', 'aesthetic appeal:'])
    put(2, 'ai', [criterion(f'heading-{i}', name.rstrip(':'), 2, [0, 2, 3],
                           'Two points on this required heading, each graded 3:2:0. Published guidance: ' + text) for i, (name, text) in enumerate(clothes, 1)],
        '3 required headings × 2 points × 3 (3:2:0)', figureKey='', questionFigureKey=FIGURE, questionFigureIncludesPrompt=False)
    design = between(s[18], '(ii)', ' and 2.(b)')
    assert '1 points @ 4 marks (graded 4:2:0), 1 points @ 3 marks (graded 3:2:0)' in design
    names = design.split('1 points @ 3 marks (graded 3:2:0)', 1)[1].strip()
    assert names.endswith('appliqué; etc.')
    put(2, 'aii', [dict(id='method', kind='criterion', verbatim='method of applying a design', marks=7,
        permittedMarks=[0, 2, 3, 4, 5, 6, 7], parts=[
            dict(id='first', verbatim='First point', marks=4, permittedMarks=[0, 2, 4]),
            dict(id='second', verbatim='Second point', marks=3, permittedMarks=[0, 2, 3])],
        contextNote='Describe one method. The scheme allocates one point at 4:2:0 and one at 3:2:0; it does not assign these to name versus description. It lists method names but prints no worked description. Published examples: ' + names)],
        '1 point × 4 (4:2:0); 1 point × 3 (3:2:0)')
    points(2, 'bi', 'fabric finishes', 2, '3:2:0', body(s[18].split('2.(b)', 1)[1], '3:2:0'))
    finishes = paragraphs(between(s[19], 'Example:1 point @ 2marks (graded 2:0)', ' or 2.(c)'),
                          ['waterproofing:', 'anti-static:', 'stain resistant:', 'crease resistant:', 'mercerising:', 'flame retardant:'])
    variants = []
    for label, detail in finishes:
        description, example = re.split(r'[;,]\s*e\.g\.', detail, maxsplit=1)
        name = label.rstrip(':')
        variants.append(dict(id=name.replace(' ', '-'), label=name.capitalize(), rows=[
            criterion('name', name, 1, [0, 2, 4], 'Name this finish, graded 4:2:0.'),
            criterion('description', 'Description', 1, [0, 2, 3], 'Describe the finish, graded 3:2:0. Published guidance: ' + description.strip()),
            criterion('example', 'Example', 1, [0, 2], 'Give one clothing use, graded 2:0. Published example: ' + example.strip())]))
    variants.append(dict(id='another-finish', label='Another fabric finish', rows=[
        criterion('name', 'fabric finish', 1, [0, 2, 4], 'Name one finish, graded 4:2:0. This is an open choice.'),
        criterion('description', 'Description', 1, [0, 2, 3], 'Give an accurate description of your finish, graded 3:2:0. The other routes show all six source examples.'),
        criterion('example', 'Example', 1, [0, 2], 'Give a suitable use of that finish in clothing, graded 2:0.')]))
    put(2, 'bii', deepcopy(variants[0]['rows']), 'Name 4 (4:2:0); description 3 (3:2:0); example 2 (2:0)', variants)
    designers = s[19].split('2.(c)', 1)[1]
    points(2, 'ci', 'contribution of Irish fashion designers', 3, '3:2:0', body(between(designers, '(i)', '(ii)'), '3:2:0'))
    points(2, 'cii', 'fashion accessories', 2, '3:2:0', body(designers.split('(ii)', 1)[1], '3:2:0'))

    points(3, 'ai', 'unemployment', 2, '3:2:0', body(between(s[20], '(i)', '(ii)'), '3:2:0'))
    unemployment = paragraphs(between(s[20], '(24 marks)', '(iii)'), ['the individual:', 'the family:', 'society:'])
    put(3, 'aii', [criterion(f'heading-{i}', h.rstrip(':'), 2, [0, 2, 4],
                            'Two points on this required heading, each graded 4:2:0. Published guidance: ' + text) for i, (h, text) in enumerate(unemployment, 1)],
        '3 required headings × 2 points × 4 (4:2:0)')
    points(3, 'aiii', 'role of education', 3, '4:2:0', body(between(s[20], '(iii)', '(iv)'), '4:2:0'))
    # a(iv) name+detail was source-reviewed by he_review_2023_ol.py.
    development = body(between(s[21].split('3.(b)', 1)[1].split('3.(c)', 1)[0], '(i)', '(ii)'), '5:3:0')
    points(3, 'bi', 'primary school education', 3, '5:3:0', development)
    achievement = between(s[21], '(ii)', ' or 3.(c)')
    points(3, 'bii', 'educational achievement', 3, '5:3:0', body(achievement, '5:3:0'))
    change = paragraphs(s[21].split('3 points @ 5 marks (graded 5:3:0)', 1)[1],
                        ['reduction in working hours:', 'increased participation of women in the workforce:', 'equal pay and employment opportunities:'])
    put(3, 'ci', [criterion(f'heading-{i}', h.rstrip(':'), 1, [0, 3, 5],
                           'Discuss this required heading, graded 5:3:0. Published guidance: ' + text) for i, (h, text) in enumerate(change, 1)],
        '3 required headings × 5 (5:3:0)')
    points(3, 'cii', 'benefits of voluntary work', 3, '5:3:0', body(s[22], '5:3:0'))

    bones = paragraphs(between(s[23], '(1 cause, 1 effect, plus 2 others)', '(ii) Evaluate'), ['causes:', 'effects:'])
    rows = [criterion(f'heading-{i}', h.rstrip(':'), 1, [0, 3, 5],
                      'One required point, graded 5:3:0. Published 2023 scheme guidance: ' + text) for i, (h, text) in enumerate(bones, 1)]
    rows.append(criterion('others', 'plus 2 others', 2, [0, 3, 5], 'Two further distinct points on either heading, each graded 5:3:0. Do not reuse a point scored above.'))
    put(4, 'ai', rows, '4 × 5 (5:3:0): cause 1, effect 1, other 2')
    points(4, 'aii', 'lifestyle and/or dietary guidelines', 3, '5:3:0', body(between(s[23], '(ii) Evaluate', '(iii)'), '5:3:0'))
    points(4, 'aiii', 'food labelling', 3, '5:3:0', body(s[23].split('(iii)', 1)[1], '5:3:0'))
    income = s[24].split('4.(b)', 1)[1].split('4.(c)', 1)[0]
    points(4, 'bi', 'factors that affect household income', 3, '5:3:0', body(between(income, '(i)', '(ii)'), '5:3:0'))
    points(4, 'bii', 'family budget plan', 3, '5:3:0', body(income.split('(ii)', 1)[1].rsplit(' or', 1)[0], '5:3:0'))
    family = s[24].split('4.(c)', 1)[1]
    points(4, 'ci', 'role of the adolescent', 3, '5:3:0', body(between(family, '(i)', '(ii)'), '5:3:0'))
    support = body(family.split('(ii)', 1)[1], '5:3:0')
    put(4, 'cii', [criterion('support', 'physical and emotional development', 3, [0, 3, 5],
        'Explain physical and emotional support, in three points graded 5:3:0. Both headings are required; the scheme does not reserve an exact number for each. Published guidance: ' + support)],
        '3 points × 5 (5:3:0); address physical and emotional development')
    assert len(fixes) == 27
    return fixes


def write():
    fixes = build()
    path = ROOT / 'scripts/markbank/card-corrections.json'; saved = json.loads(path.read_text());saved['home-economics'].update(fixes)
    path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + '\n')
    target = ROOT / f'public/exam-figures/home-economics/{FIGURE}.png'
    if not target.exists():
        fitz.open(ROOT / PAPER_BC)[5].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(132, 123, 515, 332)).save(target)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == FIGURE_SHA
    path = ROOT / 'components/MarkBank/figures-home-economics.json'; manifest = json.loads(path.read_text())
    manifest[FIGURE] = dict(src=f'/exam-figures/home-economics/{FIGURE}.png', md5=hashlib.md5(target.read_bytes()).hexdigest(),
                           alt='Three festival-fashion photographs. Left: two people wearing layered tops, shorts or a skirt, sunglasses and tall boots. Centre: a person in a sleeveless top, shorts, trainers and sunglasses, with a shirt tied around the waist. Right: a person in a blazer, long-sleeved top, trousers, boots and sunglasses.',
                           attribution='SEC Home Economics 2023 Ordinary Level examination paper, page 6 — © State Examinations Commission.',
                           sourceNote='All original fashion photographs and source credit, visually inspected at 2×; source bounds [132, 123, 515, 332]. No neighbouring question fragments or answers.')
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print('Section C: 27 existing cards corrected; statutory-scheme task retained from earlier review.')


if __name__ == '__main__':
    if '--write' in sys.argv: write()
    else: print(json.dumps(build(), ensure_ascii=False, indent=2))
