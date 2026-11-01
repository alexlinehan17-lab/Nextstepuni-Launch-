#!/usr/bin/env python3
"""Seven tasks in deferred Elective 1, at their printed mark boundaries."""
import json
import re
import sys
import fitz
from he_review_2023_hl import ROOT, tidy, between, criterion
from he_review_2023_hl_deferred import documents, deferred_card, BASE

CLARIFICATION = dict(checked='2026-11-01',
    sources=['https://www.hsa.ie/eng/your_industry/agriculture_forestry/other_hazards/fire_electricity_chemicals/',
             'https://www.se.com/nz/en/faqs/FAQ000218859/'],
    note='An ordinary MCB provides overcurrent protection. An RCBO combines overcurrent and residual-current protection; the scheme’s statement that MCBs contain RCDs is too broad.')


def after(text, marker):
    assert text.count(marker) == 1, marker
    return text.split(marker, 1)[1].strip()


def named_sections(text, labels):
    result = []
    for i, label in enumerate(labels):
        assert text.count(label) == 1, label
        body = text.split(label, 1)[1]
        if i + 1 < len(labels): body = body.split(labels[i + 1], 1)[0]
        result.append(body.strip())
    return result


def build():
    docs = documents()
    def text(doc, n): return tidy(doc[n - 1].get_text(clip=fitz.Rect(0, 0, 595, 770)))
    paper = text(docs['bc'], 5)
    outer = {'a': between(paper, '1.(a)', '1.(b)'), 'b': between(paper, '1.(b)', '1.(c)'), 'c': after(paper, '1.(c)')}
    s = {n: text(docs['scheme'], n) for n in range(18, 22)}
    cards = []
    marks = {'ai': 20, 'aii': 15, 'aiii': 15, 'bi': 12, 'bii': 18, 'ci': 12, 'cii': 18}
    selection = {'ai': [], 'aii': [], 'aiii': [], 'bi': ['each', 'following'], 'bii': ['three', 'each'], 'ci': ['each', 'following'], 'cii': ['three', 'each']}
    def add(part, topic, concept, rows, notation):
        group = outer[part[0]]
        question = between(group, f'({part[1:]})', f'({marks[part]} marks)')
        assert re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b', question, re.I) == selection[part]
        stem = group.split('(i)', 1)[0].strip()
        c = deferred_card(f'sc-q1{part}', 'C', f'E1 Q1({part[0]})({part[1:]})', topic, concept, question, stem, marks[part], notation, rows, 5)
        cards.append(c)
        return c
    history = after(s[18], '5 points @ 4 marks (graded 4:2:0)')
    assert history.startswith('Early Nineteenth Century:') and history.endswith('small living space and outdoor areas; etc.')
    add('ai', '3-3', 'housing-history', [criterion('history', 'historical development', 5, [0, 2, 4], 'Five points, each graded 4:2:0. Cover the historical development asked for. “Present day” refers to this 2023 examination. Complete published guidance: ' + history)], '5 points × 4 (4:2:0)')
    requirements = after(s[19].split('(iii)', 1)[0], '3 points @ 5 marks (graded 5:3:0)')
    add('aii', '3-3', 'accessible-housing', [criterion('needs', 'housing requirements', 3, [0, 3, 5], 'Three points, each graded 5:3:0. Explain the housing features in relation to the relevant needs. Published guidance: ' + requirements)], '3 points × 5 (5:3:0)')
    distribution = after(s[19], '3m provision 2m distribution')
    add('aiii', '3-3', 'housing-provision-distribution', [criterion('distribution', 'distribution of housing provision', 3, [0, 3, 5],
        'Three points, each using the published 5:3:0 total ladder. The scheme notes 3 marks for provision and 2 for distribution within each point; it does not print a standalone 2-mark grade. The three housing sectors below are guidance, not a printed requirement to choose one point from each. Figures and “today” refer to 2023. Published guidance: ' + distribution)],
        '3 points × 5 (5:3:0), each noting provision 3 / distribution 2')
    interior = s[20].split('(ii)', 1)[0]
    labels = ['Aesthetic and comfort factors -', 'Function of the room –', 'Environmental awareness-']
    bodies = named_sections(interior, labels)
    add('bi', '3-4', 'interior-design-factors', [criterion(key, label, 1, [0, 2, 4], 'Required heading, graded 4:2:0. Published 2023 examples: ' + body)
        for key, label, body in zip(['aesthetic', 'function', 'environment'], ['Aesthetic and comfort factors', 'Function of the room', 'Environmental awareness'], bodies)], '3 required headings × 4 (4:2:0)')
    principle_names = ['Balance', 'Proportion', 'Emphasis', 'Rhythm']
    principles = named_sections(s[20], [name + ':' for name in principle_names])
    guide = '\n\n'.join(name + ': ' + body for name, body in zip(principle_names, principles))
    rows = []
    for i in range(1, 4):
        row = criterion(f'principle-{i}', 'principles of design', 3, [0, 2], f'Principle {i}: identify, explain and give a matching application. Each element is graded 2:0; total 6:4:2:0. Use three different principles. ' + ('Complete published examples:\n\n' + guide if i == 1 else 'Use the published examples listed above.'))
        for part, label in zip(row['parts'], ['Identify', 'Explain', 'Application']): part['verbatim'] = label
        rows.append(row)
    add('bii', '3-4', 'interior-design-principles', rows, '3 principles × (identify 2 + explain 2 + application 2), all 2:0')
    electricity = s[21].split('(ii)', 1)[0]
    names = ['Ring circuit', 'Miniature circuit breakers', 'Earth wire']
    bodies = named_sections(electricity, [name + ':' for name in names])
    rows = []
    for i, (name, body) in enumerate(zip(names, bodies)):
        note = ('Source clarification: an ordinary MCB provides overcurrent protection. An RCBO combines overcurrent and residual-current protection. The scheme’s statement that MCBs contain RCDs is too broad. ' if i == 1 else '')
        rows.append(criterion(name.lower().replace(' ', '-'), name, 1, [0, 2, 4], 'Required term, graded 4:2:0. ' + note + 'Published 2023 scheme wording: ' + body))
    add('ci', '3-5', 'household-electrical-protection', rows, '3 required terms × 4 (4:2:0)')
    inefficient = after(s[21], 'Inefficient use @ 3 marks, reduction in energy use @ 3 marks')
    assert inefficient.endswith('using tumble dryers to dry clothes etc.')
    rows = []
    for i in range(1, 4):
        row = criterion(f'use-{i}', 'Inefficient use', 2, [0, 3], f'Pair {i}: identify a different inefficient use (3:0) and describe a matching reduction (3:0). Total 6:3:0. The scheme prints example inefficient uses but no model reduction descriptions. ' + ('Complete source examples: ' + inefficient if i == 1 else 'Use the example inefficient uses listed above; the reduction must match the use you identified.'))
        for part, label in zip(row['parts'], ['Inefficient use', 'Reduction in energy use']): part['verbatim'] = label
        rows.append(row)
    add('cii', '3-6', 'household-electricity-efficiency', rows, '3 pairs × (inefficient use 3 + reduction 3), both 3:0')
    assert len(cards) == 7 and sum(c['totalMarks'] for c in cards) == 110
    return cards


def write():
    cards = build(); path = ROOT / 'scripts/markbank/authored/home-economics.json'; authored = json.loads(path.read_text())
    for c in cards:
        i = next((i for i, old in enumerate(authored) if old['id'] == c['id']), None)
        if i is None: authored.append(c)
        else: authored[i] = c
    path.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
    path = ROOT / BASE / '2023-hl-deferred-review.json'; review = json.loads(path.read_text())
    review['tasks'] = [t for t in review['tasks'] if t['id'] not in {c['id'] for c in cards}] + [dict(id=c['id'], status='carded', section='C', questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    if len([t for t in review['tasks'] if t['section'] == 'C']) == 26:
        review['sectionStatus']['C'] = 'All 26 tasks carded; 385 offered marks.'
    else:
        review['sectionStatus']['C'] = '7 of 26 tasks carded (Elective 1); 110 of 385 offered marks. Electives 2/3 and Core Q4 remain open.'
    review['sectionCQuestion1Review'] = dict(paperPages=[5], schemePages=[18, 19, 20, 21], tasks=7, offeredMarks=110, candidateMarks=80,
        decisions=['A(i) uses the full paper wording: from the nineteenth century.', 'A(iii) keeps the exact 5:3:0 per-point ladder; no invented standalone 2 despite the provision/distribution annotation.', 'B(i) and C(i) required headings remain one task each.', 'B(ii) is one open response with three paired principle/explanation/application slots and all four published example principles.', 'C(ii) is one open response with three paired inefficiency/reduction slots. No unprinted model reduction is presented as official.'], sourceClarification=CLARIFICATION)
    path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
    print('2023 Higher deferred C1: seven tasks, 110 offered marks (80 candidate marks).')


if __name__ == '__main__':
    if '--write' in sys.argv: write()
    else: print(json.dumps(build(), ensure_ascii=False, indent=2))
