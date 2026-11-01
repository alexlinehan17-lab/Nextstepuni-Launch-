#!/usr/bin/env python3
"""Five separately priced nutrition tasks, 2023 Higher deferred B1."""
import hashlib
import json
import re
import sys
import fitz
from he_review_2023_hl import ROOT, tidy, between, criterion
from he_review_2023_hl_deferred import documents, deferred_card, SOURCES, BASE

FIGURE = 'home-economics-2023-hl-deferred-sb-q1a-chart'
BOUNDS = [77, 216, 523, 465]
CROP_SHA256 = '7d276c03c8566f8c9e76fb0cbcf9498f3a92f56e75562d7c8423778fbc9ca542'
ALT = ('Consumption of potatoes, pasta and rice at the evening meal among Irish adults. '
       'Age groups: 18–24, 25–34, 35–44, 45–54, 55–64, 65+ years. '
       'Potatoes: 14%, 21%, 26%, 33%, 38%, 43%. '
       'Pasta: 18%, 16%, 14%, 13%, 10%, 10%. Rice: 16%, 12%, 11%, 12%, 11%, 6%. '
       'Vertical axis: consumption rate, 0–50%; horizontal axis: age group.')


def build():
    docs = documents()
    p = tidy(docs['bc'][1].get_text(clip=fitz.Rect(0, 0, 595, 770)))
    s8 = tidy(docs['scheme'][7].get_text(clip=fitz.Rect(0, 0, 595, 775)))
    s9 = tidy(docs['scheme'][8].get_text(clip=fitz.Rect(0, 0, 595, 775)))
    questions = {}
    for letter, marks in zip('abcde', [18, 12, 18, 12, 20]):
        questions[letter] = between(p, f'({letter})', f'({marks} marks)')
    directives = dict(a=[], b=['one', 'each'], c=['each', 'following'], d=['three'], e=[])
    for letter, question in questions.items():
        assert re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b', question, re.I) == directives[letter]
    stem = 'The following infographic shows ' + between(p, 'The following infographic shows', 'Thinking House)') + ' Thinking House)'
    cards = []
    def add(part, topic, concept, marks, notation, rows, stem=''):
        c = deferred_card(f'sb-q1{part}', 'B', f'Q1({part})', topic, concept, questions[part], stem, marks, notation, rows, 2)
        cards.append(c)
        return c
    foods = [('Potatoes', between(s8, 'Potatoes:', 'Pasta:')), ('Pasta', between(s8, 'Pasta:', 'Rice:')),
             ('Rice', between(s8, 'Rice:', 'curries etc.') + ' curries etc.')]
    chart = add('a', '0-6', 'carbohydrate-food-consumption', 18, '3 comments × 6 (6:5:4:3:2:1:0)',
        [criterion(name.lower(), name, 1, list(range(7)), 'Comment and elaborate using the chart. This food receives one point graded 6:5:4:3:2:1:0. Published guidance: ' + body) for name, body in foods], stem)
    chart.update(questionFigureKey=FIGURE, questionFigureIncludesPrompt=False)
    classes = [('Monosaccharide', 'Glucose; Fructose; Galactose'), ('Disaccharide', 'Sucrose; Lactose; Maltose'), ('Polysaccharide', 'Starch; Cellulose; Glycogen; Pectin')]
    rows = []
    for name, examples in classes:
        assert name in s9 and examples in s9
        row = criterion(name.lower(), name, 2, [0, 2], 'Classification 2 marks (2:0); one matching example 2 marks (2:0). Published examples: ' + examples)
        row['parts'][0]['verbatim'] = 'Classification'; row['parts'][1]['verbatim'] = 'Matching example'
        rows.append(row)
    add('b', '0-6', 'carbohydrate-classes', 12, '3 pairs: classification 2 + example 2 (all 2:0)', rows)
    props = between(s9, '(c)', '(d)')
    guidance = [('Gelatinisation', between(props, 'Gelatinisation:', 'Dextrinisation:')),
                ('Dextrinisation', between(props, 'Dextrinisation:', 'Maillard Reaction:')),
                ('Maillard Reaction', props.split('Maillard Reaction:', 1)[1].strip())]
    add('c', '0-6', 'carbohydrate-properties', 18, '3 required properties: 2 points × 3 each (3:2:0)',
        [criterion(name.lower().replace(' ', '-'), name, 2, [0, 2, 3], 'Two explanation points for this required property, each graded 3:2:0. Published guidance: ' + body) for name, body in guidance])
    energy = between(s9, '(d)', '(e)').split('(graded 4:2:0)', 1)[1].strip()
    assert energy.endswith('climate; etc.')
    add('d', '0-1', 'adult-energy-requirements', 12, '3 factors × 4 (4:2:0)',
        [criterion('factors', 'energy requirements', 3, [0, 2, 4], 'Describe three distinct factors, each graded 4:2:0. The scheme lists factor names, but no model descriptions: ' + energy)])
    guidelines = s9.split('1 point on planning meals & 1 point on purchasing foods + 3 other points', 1)[1].strip()
    assert guidelines.endswith('consider food miles; etc.')
    add('e', '0-3', 'environmental-meal-planning', 20, '5 points × 4 (4:2:0): planning 1; purchasing 1; other 3', [
        criterion('planning', 'planning meals', 1, [0, 2, 4], 'At least one point must address planning meals. Graded 4:2:0. Complete published guidance pool; use relevant ideas for each heading: ' + guidelines),
        criterion('purchasing', 'purchasing foods', 1, [0, 2, 4], 'At least one point must address purchasing foods. Graded 4:2:0. Use the complete published guidance pool above.'),
        criterion('other', 'other points', 3, [0, 2, 4], 'Three further distinct points on either heading, each graded 4:2:0. Do not score an idea already used above again. Use the complete published guidance pool above.'),
    ])
    assert len(cards) == 5 and sum(c['totalMarks'] for c in cards) == 80
    return cards


def write():
    cards = build(); docs = documents()
    path = ROOT / 'scripts/markbank/authored/home-economics.json'; authored = json.loads(path.read_text())
    for c in cards:
        i = next((i for i, old in enumerate(authored) if old['id'] == c['id']), None)
        if i is None: authored.append(c)
        else: authored[i] = c
    path.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
    target = ROOT / f'public/exam-figures/home-economics/{FIGURE}.png'
    docs['bc'][1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(BOUNDS)).save(target)
    sha = hashlib.sha256(target.read_bytes()).hexdigest()
    assert sha == CROP_SHA256, 'Inspected original chart changed'
    manifest_path = ROOT / 'components/MarkBank/figures-home-economics.json'; manifest = json.loads(manifest_path.read_text())
    manifest[FIGURE] = dict(src=f'/exam-figures/home-economics/{FIGURE}.png', md5=hashlib.md5(target.read_bytes()).hexdigest(), alt=ALT,
        attribution='SEC Home Economics 2023 Higher Level deferred examination paper, page 2 — © State Examinations Commission.',
        sourceNote=f'Original question chart, bounds {BOUNDS}, rendered at 2×. All axes, age groups, data labels and legend retained. Source SHA256 {SOURCES["bc"]["sha256"]}.')
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    path = ROOT / BASE / '2023-hl-deferred-review.json'; review = json.loads(path.read_text())
    review['tasks'] = [t for t in review['tasks'] if t['id'] not in {c['id'] for c in cards}] + [dict(id=c['id'], status='carded', section='B', questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    if len([t for t in review['tasks'] if t['section'] == 'B']) == 17:
        review['sectionStatus']['B'] = 'All 17 tasks carded; 280 offered marks. C remains open.'
    else:
        review['sectionStatus']['B'] = '5 of 17 tasks carded (Question 1); 80 of 280 offered marks. Questions 2–5 open.'
    review['sectionBQuestion1Review'] = dict(paperPages=[2], schemePages=[8, 9], tasks=5, offeredMarks=80,
        boundaries='Five independently priced tasks. B1(a) all three foods required; B1(b) all three classifications and paired examples required; B1(c) all three properties required. B1(d) open factors. B1(e) requires one planning point, one purchasing point and three others. No combination expansion.',
        figure=dict(key=FIGURE, bounds=BOUNDS, scale=2, sha256=sha),
        detail='Full source guidance retained. B1(d) has factor names only; its reveal explicitly distinguishes those from unprinted model descriptions.')
    path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
    print('2023 Higher deferred B1: five tasks, 80 offered marks, original chart.')


if __name__ == '__main__':
    if '--write' in sys.argv: write()
    else: print(json.dumps(build(), ensure_ascii=False, indent=2))
