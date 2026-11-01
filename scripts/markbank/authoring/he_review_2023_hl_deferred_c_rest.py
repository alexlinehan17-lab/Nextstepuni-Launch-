#!/usr/bin/env python3
"""Nineteen source-reviewed tasks: 2023 deferred Electives 2/3 and Core Q4."""
from copy import deepcopy
import hashlib
import json
import re
import sys
import fitz
from he_review_2023_hl import ROOT, tidy, between, criterion
from he_review_2023_hl_deferred import documents, deferred_card, BASE, SOURCES
from he_review_2023_hl_deferred_c1 import after, named_sections

FIGURE = 'home-economics-2023-hl-deferred-sc-q2a-graduation'
BOUNDS = [160, 161, 428, 311]
CROP_SHA256 = '756c366c95b636987d74c3a9b0f838955bd5f0f8f4da2f79ad8b4eda7c9f6fab'
CONSENT = dict(checked='2026-11-01',
    sources=['https://www.irishstatutebook.ie/eli/1990/act/32/section/5/enacted/en/html',
             'https://www2.hse.ie/services/sexual-health/what-is/'],
    note='Marriage does not remove the requirement for freely given consent to sexual activity. Consent can be withdrawn. Ireland abolished the marital rape exemption in 1990.')


def build():
    docs = documents()
    def text(doc, n): return tidy(doc[n - 1].get_text(clip=fitz.Rect(0, 0, 595, 760 if doc is docs['bc'] else 775)))
    p = {n: text(docs['bc'], n + 4) for n in range(2, 5)}
    s = {n: text(docs['scheme'], n) for n in range(22, 31)}
    marks = {2: dict(ai=10, aii=15, b=15, ci=9, cii=6),
             3: dict(ai=10, aii=20, aiii=20, bi=20, bii=10, ci=20, cii=10),
             4: dict(ai=20, aii=20, aiii=10, bi=14, bii=16, ci=15, cii=15)}
    selections = {2: dict(ai=[], aii=['each', 'following'], b=['one'], ci=[], cii=[]),
                  3: dict(ai=[], aii=[], aiii=[], bi=[], bii=['one'], ci=[], cii=['one']),
                  4: dict(ai=[], aii=[], aiii=[], bi=['two', 'one', 'one', 'each'], bii=[], ci=['three'], cii=[])}
    cards = []
    def add(n, part, topic, concept, rows, notation):
        letter = part[0]
        outer = between(p[n], f'{n}.({letter})', f'{n}.({chr(ord(letter)+1)})') if letter != 'c' else after(p[n], f'{n}.(c)')
        outer = re.sub(r'\s+(?:and|or)$', '', outer)
        if part == 'b' and n == 2:
            question = 'Write a profile ' + between(outer, 'Write a profile', '(15 marks)')
            stem = outer.split('Write a profile', 1)[0].strip()
            ref = 'E2 Q2(b)'
        else:
            question = between(outer, f'({part[1:]})', f'({marks[n][part]} marks)')
            stem = outer.split('(i)', 1)[0].strip()
            ref = (f'E{n} ' if n < 4 else '') + f'Q{n}({letter})({part[1:]})'
        assert re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b', question, re.I) == selections[n][part], (n, part, question)
        c = deferred_card(f'sc-q{n}{part}', 'C', ref, topic, concept, question, stem, marks[n][part], notation, rows, n + 4)
        cards.append(c)
        return c

    sketch = add(2, 'ai', '3-8', 'graduation-outfit-sketch', [
        criterion('sketch', 'Sketch', 1, [0, 1, 2, 3, 4], 'Sketch an outfit suitable for a graduation ball. Graded 4:3:2:1:0. The scheme supplies no model sketch.'),
        criterion('description', 'Description', 1, [0, 2, 4, 6], 'Describe the same outfit. Graded 6:4:2:0. The scheme supplies no model description.'),
    ], 'Sketch 4 (4:3:2:1:0); description 6 (6:4:2:0)')
    sketch.update(questionFigureKey=FIGURE, questionFigureIncludesPrompt=False)
    headings = ['Comfort –', 'Aesthetic appeal -', 'Suitability for purpose:']
    guidance = named_sections(s[22].split('and 2.(b)', 1)[0], headings)
    evaluation = add(2, 'aii', '3-8', 'graduation-outfit-evaluation', [criterion(key, name, 1, [0, 3, 5], 'Required heading, graded 5:3:0. Evaluate your own outfit from part (i). Published guidance: ' + body)
        for key, name, body in zip(['comfort', 'aesthetic', 'purpose'], ['Comfort', 'Aesthetic appeal', 'Suitability for purpose'], guidance)], '3 required headings × 5 (5:3:0)')
    evaluation['stem'] += '\n\nEarlier task (i): ' + sketch['questionText'] + ' Use that outfit for this evaluation; sketch marks are awarded in the earlier task.'
    evaluation.update(questionFigureKey=FIGURE, questionFigureIncludesPrompt=False)
    fabrics = named_sections(s[23].split('or 2.(c)', 1)[0], ['Cotton Fibre production:', 'Linen Fibre production:', 'Wool Fibre production:', 'Silk Fibre production:'])
    variants = []
    for name, body in zip(['Cotton', 'Linen', 'Wool', 'Silk'], fabrics):
        production = body.split('Properties:', 1)[0].strip()
        properties = between(body, 'Properties:', 'Fibre identification test:')
        identification = after(body, 'Fibre identification test:')
        variants.append(dict(id=name.lower(), label=name, rows=[
            criterion('production', 'fibre production', 3, [0, 2], 'Three points for ' + name + ', each graded 2:0. Published guidance: ' + production),
            criterion('properties', 'fabric properties', 2, [0, 2], 'Two properties for the same fabric, each graded 2:0. Published guidance: ' + properties),
            criterion('test', 'fibre identification test', 1, [0, 3, 5], 'One test for the same fibre, graded 5:3:0. Published guidance: ' + identification),
        ]))
    variants.append(dict(id='another-fabric', label='Another valid natural fabric', rows=[
        criterion('production', 'fibre production', 3, [0, 2], 'Three accurate production points for your chosen natural fabric, each graded 2:0. The scheme supplies examples for cotton, linen, wool and silk only.'),
        criterion('properties', 'fabric properties', 2, [0, 2], 'Two accurate properties of the same fabric, each graded 2:0. No model for another fabric is printed.'),
        criterion('test', 'fibre identification test', 1, [0, 3, 5], 'An accurate identification test for the same fibre, graded 5:3:0. No model for another fabric is printed.'),
    ]))
    fabric = add(2, 'b', '3-7', 'natural-fabric-profile', deepcopy(variants[0]['rows']), 'Production 3 × 2; properties 2 × 2 (2:0); test 5 (5:3:0)')
    fabric['answerVariants'] = variants
    factors = after(s[23], '3 points @ 3 marks (graded 3:2:0)')
    add(2, 'ci', '3-8', 'socioeconomic-fashion-factors', [criterion('factors', 'socio-economic factors', 3, [0, 2, 3], 'Three points, each graded 3:2:0. Address the social and economic influences asked for; the scheme does not assign a fixed number to each. Published guidance: ' + factors)], '3 points × 3 (3:2:0)')
    add(2, 'cii', '3-8', 'social-media-fashion-influence', [criterion('influence', 'social media influence', 2, [0, 2, 3], 'Two points, each graded 3:2:0. Published guidance: ' + after(s[24], '2 points @ 3 marks each (graded 3:2:0)'))], '2 points × 3 (3:2:0)')

    work = named_sections(s[25].split('(ii)', 1)[0], ['Paid work:', 'Unpaid work:'])
    add(3, 'ai', '3-9', 'paid-unpaid-work', [criterion(key, name, 1, [0, 3, 5], 'Required comparison heading, graded 5:3:0. Published guidance: ' + body)
        for key, name, body in zip(['paid', 'unpaid'], ['Paid work', 'Unpaid work'], work)], '2 required headings × 5 (5:3:0)')
    participation = after(between(s[25], '(ii)', '(iii)'), '4 points @ 5 marks (graded 5:3:0)')
    add(3, 'aii', '3-9', 'women-workforce-participation', [criterion('factors', 'factors', 4, [0, 3, 5], 'Four points, each graded 5:3:0. Published 2023 guidance: ' + participation)], '4 points × 5 (5:3:0)')
    attitudes = after(s[25].split('(iii)', 1)[1], '4 points @ 5 marks (graded 5:3:0)') + ' ' + s[26].split('and 3.(b)', 1)[0].strip()
    assert attitudes.endswith('peer pressure; etc.')
    add(3, 'aiii', '3-9', 'attitudes-to-work', [criterion('attitudes', 'attitude to work', 4, [0, 3, 5], 'Four points, each graded 5:3:0. Complete published 2023 guidance (general examples, not predictions about an individual): ' + attitudes)], '4 points × 5 (5:3:0)')
    demand = after(between(s[26], '3.(b)', '(ii)'), '4 points @ 5 marks (graded 5:3:0)')
    add(3, 'bi', '3-10', 'adult-education-demand', [criterion('demand', 'adult and second chance education', 4, [0, 3, 5], 'Four points, each graded 5:3:0. Published 2023 guidance: ' + demand)], '4 points × 5 (5:3:0)')
    initiatives = after(s[26], 'Explanation: 2 points @ 4 marks (graded 4:2:0)') + ' ' + s[27].split('or 3.(c)', 1)[0].strip()
    assert initiatives.endswith('universities etc.')
    add(3, 'bii', '3-10', 'second-chance-education-initiative', [
        criterion('name', 'Name', 1, [0, 1, 2], 'Name one initiative, graded 2:1:0. This is an open choice; do not combine details from different initiatives. “Contemporary” refers to the 2023 examination.'),
        criterion('details', 'Explanation', 2, [0, 2, 4], 'Two matching details, each graded 4:2:0. The following are the published 2023 examination examples, not current eligibility or funding advice: ' + initiatives),
    ], 'Name 2 (2:1:0); details 2 × 4 (4:2:0)')
    childcare = after(between(s[27], '3.(c)', '(ii)'), '4 points @ 5 marks (graded 5:3:0)')
    add(3, 'ci', '3-11', 'childcare-requirements', [criterion('requirements', 'requirements for childcare', 4, [0, 3, 5], 'Four points, each graded 5:3:0. Use the original paper’s request to analyse key requirements when choosing childcare; the scheme paraphrases that request. Published guidance: ' + childcare)], '4 points × 5 (5:3:0)')
    childcare_options = after(s[27], 'Evaluate: 4 points @ 2 marks (graded 2:1:0)')
    add(3, 'cii', '3-11', 'childcare-option-evaluation', [
        criterion('name', 'Name', 1, [0, 2], 'Name one suitable childcare option, graded 2:0. Use that same option throughout.'),
        criterion('evaluation', 'Evaluation', 4, [0, 1, 2], 'Four evaluative points, each graded 2:1:0. The scheme gives option names and evaluation criteria, not a complete model evaluation for each: ' + childcare_options),
    ], 'Name 2 (2:0); evaluation 4 × 2 (2:1:0)')

    nutrition = after(s[28].split('(ii)', 1)[0], '5 points @ 4 marks (graded 4:3:2:1:0)')
    add(4, 'ai', '0-9', 'cheese-nutritional-significance', [criterion('nutrition', 'nutritional significance', 5, list(range(5)), 'Five points, each graded 4:3:2:1:0. The scheme groups its examples by nutrient but does not print a quota of one point per nutrient. Full published guidance: ' + nutrition)], '5 points × 4 (4:3:2:1:0)')
    production, packaging, labelling = named_sections('Stages of production: ' + after(s[28], 'Stages of production:'), ['Stages of production:', 'Packaging:', 'Labelling:'])
    add(4, 'aii', '0-9', 'cheese-production', [
        criterion('production', 'stages of production', 6, [0, 1, 2], 'Six points, each graded 2:1:0. Source correction: the heading says “9 points”, but the detailed allocation is 6 + 2 + 2 points, matching the paper’s 20 marks. Published guidance: ' + production),
        criterion('packaging', 'packaging', 2, [0, 2], 'Two points, each graded 2:0. Published guidance: ' + packaging),
        criterion('labelling', 'labelling', 2, [0, 2], 'Two points, each graded 2:0. Published guidance: ' + labelling),
    ], 'Production 6 × 2 (2:1:0); packaging 2 × 2; labelling 2 × 2 (2:0) = 20')
    fsai = after(s[29].split('and 4.(b)', 1)[0], '2 points @ 5 marks (graded 5:3:0)')
    add(4, 'aiii', '0-11', 'fsai-role', [criterion('role', 'Food Safety Authority of Ireland', 2, [0, 3, 5], 'Two points, each graded 5:3:0. Published 2023 guidance: ' + fsai)], '2 points × 5 (5:3:0)')
    outlets = between(s[29], 'Retail Outlets:', '(ii)')
    rows = []
    for i in range(1, 3):
        row = criterion(f'outlet-{i}', 'Retail Outlets', 1, list(range(8)), 'Name a different outlet (3:0), then give a matching advantage and disadvantage (each 2:1:0). ' + ('Full published examples: ' + outlets if i == 1 else 'Use the full published examples listed above.'))
        row['parts'] = [dict(id='name', verbatim='Name', marks=3, permittedMarks=[0, 3]),
                        dict(id='advantage', verbatim='Advantage', marks=2, permittedMarks=[0, 1, 2]),
                        dict(id='disadvantage', verbatim='Disadvantage', marks=2, permittedMarks=[0, 1, 2])]
        rows.append(row)
    add(4, 'bi', '1-2', 'household-technology-retail-outlets', rows, '2 outlets × (name 3 (3:0) + advantage 2 + disadvantage 2 (2:1:0))')
    management = after(s[29], '4 points @ 4 marks (graded 4:2:0)')
    add(4, 'bii', '1-0', 'management-shopping', [criterion('management', 'components of management', 4, [0, 2, 4], 'Four points, each graded 4:2:0. Address inputs, throughputs and outputs as asked. The scheme does not assign a fixed quota to each heading. Published guidance: ' + management)], '4 points × 4 (4:2:0)')
    variations = after(s[30].split('(ii)', 1)[0], '3 points @ 5 marks (graded 5:3:0)')
    add(4, 'ci', '2-1', 'cultural-marital-arrangements', [criterion('variations', 'cultural variations', 3, [0, 3, 5], 'Describe three different cultural variations, each graded 5:3:0, as the original paper specifies. The scheme uses the shorter instruction “Outline”. Published guidance: ' + variations)], '3 different variations × 5 (5:3:0)')
    rights = after(s[30].split('(ii)', 1)[1], '3 points @ 5 marks (graded 5:3:0)')
    add(4, 'cii', '2-1', 'marital-rights-responsibilities', [criterion('rights', 'rights and responsibilities', 3, [0, 3, 5],
        'Three points, each graded 5:3:0. Source clarification: marriage never removes the requirement for freely given consent to sexual activity. Consent can be withdrawn; marriage creates no entitlement to sex. Ireland abolished the marital rape exemption in 1990. The wording and Acts below are historical examination guidance, not current legal advice. Published 2023 scheme wording: ' + rights)], '3 points × 5 (5:3:0)')
    assert len(cards) == 19 and sum(c['totalMarks'] for c in cards) == 275
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
    docs['bc'][5].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(BOUNDS)).save(target)
    sha = hashlib.sha256(target.read_bytes()).hexdigest(); assert sha == CROP_SHA256
    path = ROOT / 'components/MarkBank/figures-home-economics.json'; manifest = json.loads(path.read_text())
    manifest[FIGURE] = dict(src=f'/exam-figures/home-economics/{FIGURE}.png', md5=hashlib.md5(target.read_bytes()).hexdigest(),
        alt='Original graduation-ball photograph: a group wearing formal dresses and suits at a celebration.',
        attribution='SEC Home Economics 2023 Higher Level deferred examination paper, page 6; photograph credited to www.etiquettejulie.com — © State Examinations Commission.',
        sourceNote=f'Original image, bounds {BOUNDS}, rendered at 2×. Source SHA256 {SOURCES["bc"]["sha256"]}.')
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    path = ROOT / BASE / '2023-hl-deferred-review.json'; review = json.loads(path.read_text())
    review['tasks'] = [t for t in review['tasks'] if t['id'] not in {c['id'] for c in cards}] + [dict(id=c['id'], status='carded', section='C', questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    review['sectionCQuestion2Review'] = dict(paperPages=[6], schemePages=[22, 23, 24], tasks=5, offeredMarks=55, candidateMarks=40,
        decisions=['Sketch/description remain one 10-mark response; evaluation is a separate 15-mark task carrying the earlier prompt and original photo.', 'Natural fabric is one open profile with four complete source routes and an open other route; no combination expansion.', 'All three evaluation headings required; social/economic factors have no invented heading quota.'], figure=dict(key=FIGURE, bounds=BOUNDS, scale=2, sha256=sha))
    review['sectionCQuestion3Review'] = dict(paperPages=[7], schemePages=[25, 26, 27], tasks=7, offeredMarks=110, candidateMarks=80,
        decisions=['All open factors, initiative and childcare choices remain one response per published mark boundary.', 'Retain both pages of attitudes and initiative guidance, with 2023 eligibility examples labelled historical.', 'C(i) follows the full original paper wording, which differs from the scheme.', 'C(ii) distinguishes the source list and generic evaluation criteria from unprinted model evaluations.'])
    review['sectionCQuestion4Review'] = dict(paperPages=[8], schemePages=[28, 29, 30], tasks=7, offeredMarks=110, candidateMarks=80,
        decisions=['A(ii): paper 20 and the detailed 12+4+4 allocation govern over the scheme’s erroneous 9-points heading.', 'A(i): five graded points; no invented one-per-nutrient quota.', 'B(i): two outlets, each keeping its name/advantage/disadvantage together.', 'B(ii): all three named management components; four graded points without invented per-heading quotas.', 'C(i) retains the paper’s three different cultural variations instruction.'], sourceClarification=CONSENT)
    assert len(review['tasks']) == 58 and sum(t['marks'] for t in review['tasks']) == 749
    review['sectionStatus'] = dict(A='All 15 tasks carded; 84 offered marks.', B='All 17 tasks carded; 280 offered marks.', C='All 26 tasks carded; 385 offered marks.')
    review['status'] = 'source-review-complete; all-source-pages-visually-reviewed; browser-QA-pending'
    review['completion'] = dict(tasks=58, offeredPracticeMarks=749, note='All alternatives included for practice. Offered marks must not be confused with the candidate total. Full source sweep recorded above; browser QA remains pending.')
    path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
    print('2023 Higher deferred C2–C4: 19 tasks, 275 offered marks. All C: 26 tasks / 385; full sitting: 58 / 749.')


if __name__ == '__main__':
    if '--write' in sys.argv: write()
    else: print(json.dumps(build(), ensure_ascii=False, indent=2))
