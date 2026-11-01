#!/usr/bin/env python3
"""Review all seven tasks in 2023 Higher Home Design and Management."""
from copy import deepcopy
import hashlib
import json
import re
import sys

import fitz
from he_review_2023_hl import ROOT, PAPER, SCHEME, HASHES, tidy, between, criterion
from he_review_2023_hl_section_b_rest import paragraphs

FIGURE = 'home-economics-2023-hl-sc-q1bi-scheme'
FIGURE_SHA = '791e8bda439450346ad4169e71c3494c674270547cd58238a25a2316645a960f'


def build():
    for path, sha in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha
    paper, scheme = fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)
    p5 = tidy(paper[4].get_text())
    tasks = p5.split('1.(a)', 1)[1]
    # Selection of the elective / b-or-c is outside each independently
    # practicable task. Within tasks, lighting is an open choose-one response.
    directives = re.findall(r'\b(?:choose|one\s+(?:of|type)|any\s+\w+|either|or|answer\s+\w+\s+of)\b', tasks, re.I)
    assert directives == ['one type', 'or'], directives
    sections = {'a': between(p5, '1.(a)', '1.(b)'), 'b': between(p5, '1.(b)', '1.(c)'),
                'c': p5.split('1.(c)', 1)[1]}
    s = {n: tidy('\n'.join(line for line in scheme[n - 1].get_text().splitlines()
                           if line.strip() != str(n))) for n in [18, 19, 20]}
    fixes = {}

    def put(part, roman, marks, notation, rows, variants=None, figure=None):
        key = f'he-2023-hl-sc-q1{part}{roman}'
        q = sections[part]
        text = between(q, f'({roman})', f'({marks} marks)')
        assert not re.search(r'\((?:i|ii|iii)\)', text), key
        value = dict(questionText=text, stem=q.split('(i)', 1)[0].strip(),
                     tariffModel=dict(kind='fixed', notation=notation), rows=rows,
                     sourceMaterial=dict(kind='source-question', label='OFFICIAL QUESTION', title='Source and question',
                                         pages=[5], attribution='SEC Home Economics 2023 Higher Level examination paper — © State Examinations Commission.',
                                         presentationNote='Open the original examination page to review this task in context.'),
                     notes='Reviewed against the full paper and marking scheme. Published mark boundaries and open choices retained; no combination expansion. See he_review_2023_hl_elective1.py.')
        if variants:
            value['answerVariants'] = variants
        if figure:
            value['figureKey'] = figure
        fixes[key] = dict(reason='Independent 2023 Higher Elective 1 review: full guidance, paired responses and published partial-credit steps.', set=value)

    design = paragraphs(between(s[18], '2 points on each heading + 1 other', '(ii)'),
                        ['aesthetic and comfort factors', 'environmental awareness'])
    rows = [criterion(f'heading-{i}', h, 2, [0, 2, 4],
                      'Two distinct points on this required heading, each graded 4:2:0. Published guidance: ' + body)
            for i, (h, body) in enumerate(design, 1)]
    rows.append(criterion('additional', '1 other', 1, [0, 2, 4],
                          'One further distinct point on either heading, graded 4:2:0. Do not score a point already used above again.'))
    put('a', 'i', 20, '5 × 4 (4:2:0): two points on each heading and one other', rows)
    thermal = 'depends on room function ' + between(s[18], 'depends on room function', '(iii)')
    assert thermal.endswith('elderly people; etc.')
    rows = []
    for i in range(1, 3):
        row = dict(id=f'room-{i}', kind='criterion', verbatim='room', marks=6, permittedMarks=[0, 2, 4, 6],
                   contextNote=f'Living space {i}: identify the room (2:0) and discuss its thermal comfort (4:2:0). The two spaces must be different.' +
                               (' Published guidance: ' + thermal if i == 1 else ' Use the guidance above for this second space.'),
                   parts=[dict(id='room', verbatim='Identify room', marks=2, permittedMarks=[0, 2]),
                          dict(id='discussion', verbatim='Discussion', marks=4, permittedMarks=[0, 2, 4])])
        rows.append(row)
    put('a', 'ii', 12, '2 rooms × (identify 2 (2:0) + discussion 4 (4:2:0))', rows)
    thermostat = s[18].split('underlying principle based on', 1)[1]
    principle, uses = thermostat.split('use in the home', 1)
    put('a', 'iii', 18, 'Underlying principle 4 × 3; use 2 × 3 (3:2:0)', [
        criterion('principle', 'underlying principle', 4, [0, 2, 3], 'Four distinct points, graded 3:2:0. Published guidance: based on ' + principle.strip()),
        criterion('uses', 'use in the home', 2, [0, 2, 3], 'Two distinct points, graded 3:2:0. Published guidance: ' + uses.strip())])

    # The source is a three-column table, so preserve its original layout.
    # Four chosen properties each carry their OWN name, explanation and example.
    rows = []
    for i in range(1, 5):
        rows.append(dict(id=f'property-{i}', kind='criterion', verbatim='Property', marks=5,
                         permittedMarks=[0, 1, 2, 3, 4, 5],
                         contextNote=f'Property {i} of the four you chose. Use a different property for each row, with its matching explanation and home example. The complete scheme table is shown above.',
                         parts=[dict(id='name', verbatim='Name', marks=2, permittedMarks=[0, 2]),
                                dict(id='description', verbatim='Description', marks=2, permittedMarks=[0, 1, 2]),
                                dict(id='example', verbatim='Example', marks=1, permittedMarks=[0, 1])]))
    put('b', 'i', 20, 'Four properties: name 2 (2:0), description 2 (2:1:0), example 1 (1:0)', rows, figure=FIGURE)
    lighting = between(s[19], 'Name 4 marks (graded 4:2:0), underlying principle 2 points @ 3 marks (graded 3:2:0)', 'or 1.(c)')
    variants = []
    for name, detail in paragraphs(lighting, ['CFL/Fluorescents', 'LED (Light Emitting Diode)']):
        variants.append(dict(id='cfl' if name.startswith('CFL') else 'led', label=name, rows=[
            criterion('name', name, 1, [0, 2, 4], 'Name the type you explained, graded 4:2:0.'),
            criterion('principle', 'underlying principle', 2, [0, 2, 3], 'Two distinct points for this type, each graded 3:2:0. Published guidance: ' + detail)]))
    variants.append(dict(id='another-type', label='Another energy-efficient type', rows=[
        criterion('name', 'Name', 1, [0, 2, 4], 'Name the energy-efficient lighting type you explained, graded 4:2:0. The paper leaves this choice open.'),
        criterion('principle', 'underlying principle', 2, [0, 2, 3], 'Explain two accurate principle points for the same type, each graded 3:2:0. The printed scheme supplies models for CFL/fluorescent lighting and LED only.')]))
    put('b', 'ii', 10, 'Name 4 (4:2:0), principle 2 × 3 (3:2:0)', deepcopy(variants[0]['rows']), variants)
    housing = paragraphs(s[19].split('expect 1 point to refer to each factor', 1)[1],
                         ['environmental factors', 'economic factors', 'social factors'])
    put('c', 'i', 18, '3 required factors × 6 (6:4:2:0)', [
        criterion(f'factor-{i}', h, 1, [0, 2, 4, 6], 'One point on this required factor, graded 6:4:2:0. Published guidance: ' + body)
        for i, (h, body) in enumerate(housing, 1)])
    emissions = paragraphs(s[20].split('(12 marks)', 1)[1],
                           ['Emissions', 'effects on the environment', 'a strategy households could implement in order to reduce emissions'])
    put('c', 'ii', 12, 'Emission 3 (3:0), effects 2 × 3 (3:2:0), strategy 3 (3:2:0)', [
        criterion('emission', 'Emissions', 1, [0, 3], 'Identify one emission. Published guidance: ' + emissions[0][1]),
        criterion('effects', 'effects on the environment', 2, [0, 2, 3], 'Two distinct effects, graded 3:2:0. Published guidance: ' + emissions[1][1]),
        criterion('strategy', 'a strategy households could implement in order to reduce emissions', 1, [0, 2, 3], 'One strategy, graded 3:2:0. Published guidance: ' + emissions[2][1])])
    assert len(fixes) == 7
    return fixes


def write():
    fixes = build()
    path = ROOT / 'scripts/markbank/card-corrections.json'
    saved = json.loads(path.read_text()); saved['home-economics'].update(fixes)
    path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + '\n')
    image_path = ROOT / f'public/exam-figures/home-economics/{FIGURE}.png'
    if not image_path.exists():
        fitz.open(ROOT / SCHEME)[18].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(53, 153, 547, 376)).save(image_path)
    assert hashlib.sha256(image_path.read_bytes()).hexdigest() == FIGURE_SHA
    # Full table text, with column associations checked independently on the
    # rendered source, is also available to screen-reader users.
    alt = ('SEC scheme: Property; Explanation; Example. Reflected: rays bounce off a shiny surface; mirrors, polished porcelain, light colours on walls, gloss paint, glazed wall tiles. '
           'Diffused: rays scatter through translucent substances or on a non-reflecting surface; net curtains, frosted glass, translucent lampshades. '
           'Absorbed: dark and matt surfaces absorb light; dark painted walls, brick walls, stone. '
           'Dispersed: a prism or crystal splits rays into component colours; chandeliers. '
           'Refracted: thick or ridged glass bends rays; glass bricks, double glazing.')
    path = ROOT / 'components/MarkBank/figures-home-economics.json'
    manifest = json.loads(path.read_text())
    manifest[FIGURE] = dict(src=f'/exam-figures/home-economics/{FIGURE}.png', md5=hashlib.md5(image_path.read_bytes()).hexdigest(),
                            alt=alt, solution=True,
                            attribution='SEC Home Economics 2023 Higher Level marking scheme, page 19 — © State Examinations Commission.',
                            sourceNote='Original three-column table; all five rows, headers and borders visually verified. Bounds [53,153,547,376], 2×.')
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print('Elective 1: seven existing tasks reviewed; all 110 offered marks retained.')


if __name__ == '__main__':
    if '--write' in sys.argv:
        write()
    else:
        print(json.dumps(build(), ensure_ascii=False, indent=2))
