#!/usr/bin/env python3
"""All sixteen Section B tasks from the independently reviewed 2022 sitting."""
from copy import deepcopy
import hashlib
import json
import re
import sys
import fitz
from he_review_2023_hl import ROOT, tidy, between, criterion
from he_review_2023_hl_deferred import deferred_card, BASE
from he_review_2023_hl_deferred_c1 import after, named_sections
from he_review_2022_hl_deferred import documents, SOURCES

FIGURE = 'home-economics-2022-hl-deferred-sb-q1a-labels'
BOUNDS = [82, 187, 534, 419]
CROP_SHA256 = '6a6c879bfebfbf2ff2f26fbfe9c96b0b28322f13a3b474f1d869d49ff2d0a986'
CLARIFICATIONS = {
    'glycerol': dict(source='https://pubchem.ncbi.nlm.nih.gov/compound/Glicerol', note='Glycerol has three hydroxyl groups, not three OH molecules.'),
    'smoke-point': dict(source='https://lod.nal.usda.gov/nalt/en/page/287706', note='Smoke point depends on the fat/oil composition; 200°C and 250°C in the scheme are not universal values.'),
    'aeration': dict(source='https://www.ifst.org/lovefoodlovescience/resources/protein-foam-formation', note='Whisking incorporates air and unfolds protein at the air/water interface; later heating sets the foam. Frictional heat is not the explanation for foam formation.'),
    'fsai': dict(source='https://www.fsai.ie/our-role', note='FSAI is the Food Safety Authority of Ireland; the scheme calls it an Association.'),
}


def build():
    docs = documents()
    def text(doc, n): return tidy(doc[n - 1].get_text(clip=fitz.Rect(0, 0, 595, 775 if doc is docs['scheme'] else 760)))
    p = {n: text(docs['bc'], n) for n in range(2, 5)}; s = {n: text(docs['scheme'], n) for n in range(9, 16)}
    pq = {1: p[2].rsplit('Question 1', 1)[1].strip(), 2: between(p[3], 'Question 2', 'Question 3'), 3: after(p[3], 'Question 3'), 4: between(p[4], 'Question 4', 'Question 5'), 5: after(p[4], 'Question 5')}
    marks = {1: [20, 28, 12, 20], 2: [16, 22, 12], 3: [20, 18, 12], 4: [20, 20, 10], 5: [18, 20, 12]}
    selections = {1: [ ['four'], [], ['each', 'following'], [] ], 2: [['four'], ['one'], ['one']], 3: [[], [], []], 4: [[], ['four'], ['one']], 5: [[], [], []]}
    cards = []
    def add(n, part, topic, concept, rows, notation):
        index = ord(part) - ord('a'); m = marks[n][index]
        question = between(pq[n], f'({part})', f'({m} marks)')
        assert re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b', question, re.I) == selections[n][index], (n, part, question)
        stem = pq[n].split('(a)', 1)[0].strip() if n != 1 else ''
        c = deferred_card(f'sb-q{n}{part}', 'B', f'Q{n}({part})', topic, concept, question, stem, m, notation, rows, 2 if n == 1 else 3 if n < 4 else 4)
        c['id'] = c['id'].replace('2023', '2022'); c['year'] = 2022; c['questionRef'] = c['questionRef'].replace('2023', '2022')
        c['sourceMaterial']['attribution'] = c['sourceMaterial']['attribution'].replace('2023', '2022')
        c['notes'] = '2022 deferred paper and scheme independently reviewed; he_review_2022_hl_deferred_b.py and home-economics/2022-hl-deferred-review.json record complete boundaries and clarifications. Open choices remain one response.'
        cards.append(c); return c
    # The chart's embedded text is extracted after the prose on scheme page 9.
    label_guide = between(s[9], '(graded 5:4:3:2:1:0)', '3% 3% 13%')
    assert label_guide.endswith('Irish made products; etc.')
    for label in ['calorie content:', 'specific ingredients:', 'allergen information:', 'food additives:', 'origin:']:
        assert label_guide.count(label) == 1
        label_guide = label_guide.replace(' ' + label, '\n\n' + label)
    chart = add(1, 'a', '0-11', 'food-label-reasons', [criterion(f'reason-{i}', 'reasons', 1, list(range(6)),
        f'Reason {i} of four: choose a different category from the chart, comment and elaborate; graded 5:4:3:2:1:0. ' + ('All six published guidance categories: ' + label_guide if i == 1 else 'Use the full six-category guidance above. Do not repeat a category already scored.')) for i in range(1, 5)], '4 chosen reasons × 5 (5:4:3:2:1:0)')
    chart['stem'] = 'The chart below presents information on the reasons why consumers consult food labels. (adapted from a Research Study into Consumers’ Attitudes to Food Labelling - FSAI)'
    chart.update(questionFigureKey=FIGURE, questionFigureIncludesPrompt=False)
    lipid = s[10].split('(c)', 1)[0]
    structure = after(lipid.split('• biological function', 1)[0], '(graded 4:2:0)')
    biological = after(lipid.split('• biological function', 1)[1], '(graded 4:2:0)')
    add(1, 'b', '0-7', 'lipids-structure-functions', [
        criterion('structure', 'structure', 3, [0, 2, 4], 'Three points, each graded 4:2:0. Source clarification: glycerol contains three hydroxyl (–OH) groups, not three separate OH molecules. Complete scheme guidance, including the accepted labelled-diagram route: ' + structure),
        criterion('functions', 'biological function', 4, [0, 2, 4], 'Four points, each graded 4:2:0. Published guidance: ' + biological),
    ], 'Structure 3 × 4; biological functions 4 × 4 (4:2:0)')
    fat_terms = after(between(s[10], '(c)', '(d)'), '(graded: 6:4:2:0)')
    rancid = between(fat_terms, 'Rancidity', 'Smoke point'); smoke = after(fat_terms, 'Smoke point')
    add(1, 'c', '0-7', 'rancidity-smoke-point', [criterion('rancidity', 'Rancidity', 1, [0, 2, 4, 6], 'Required term, graded 6:4:2:0. Published guidance: ' + rancid),
        criterion('smoke', 'Smoke point', 1, [0, 2, 4, 6], 'Required term, graded 6:4:2:0. Source clarification: the temperature at which visible smoke appears varies with the oil/fat composition; the printed 200°C/250°C values are not universal. Historical scheme wording: ' + smoke)], '2 required terms × 6 (6:4:2:0)')
    health = after(s[10].split('(d)', 1)[1], '(graded 4:2:0)')
    add(1, 'd', '0-1', 'health-food-purchasing', [criterion('health', 'health status', 5, [0, 2, 4], 'Five points, each graded 4:2:0. Published 2022 guidance: ' + health)], '5 points × 4 (4:2:0)')

    factors = after(between(s[11], '(a)', '(b)'), '(graded: 4:2:0)')
    add(2, 'a', '0-11', 'irish-food-industry-success', [criterion('factors', 'factors', 4, [0, 2, 4], 'Four discussed factors, each graded 4:2:0. The scheme lists factor names without model discussions: ' + factors)], '4 factors × 4 (4:2:0)')
    processes = after(s[11], 'Process – Freezing, Refrigeration.')
    freezing = between(processes, 'Freezing:', 'Refrigeration:')
    refrigeration = between(processes, 'Refrigeration:', 'Underlying principle freezing / refrigeration:')
    cold_principle = between(processes, 'Underlying principle freezing / refrigeration:', 'Process - Vacuum Packing / Modified Atmospheric Packaging:')
    packing = between(processes, 'Process - Vacuum Packing / Modified Atmospheric Packaging:', 'Process – Curing/Salting:')
    curing = between(processes, 'Process – Curing/Salting:', 'Process: Canning:')
    canning = between(processes, 'Process: Canning:', 'Process - Dehydration:')
    drying = after(processes, 'Process - Dehydration:')
    route_data = [('freezing', 'Freezing', freezing, 'The shared paragraph includes refrigeration and freezing; ice formation applies to freezing. ' + cold_principle),
                  ('refrigeration', 'Refrigeration', refrigeration, 'The shared paragraph includes refrigeration and freezing; do not apply its ice-crystal points to refrigeration. ' + cold_principle)]
    for key, name, body in [('packing', 'Vacuum packing / modified atmosphere packaging', packing), ('curing', 'Curing / salting', curing), ('canning', 'Canning', canning), ('drying', 'Dehydration', drying)]:
        method, principle = body.split('Underlying principle:', 1)
        route_data.append((key, name, method.strip(), principle.strip()))
    variants = []
    for key, name, method, principle in route_data:
        variants.append(dict(id=key, label=name, rows=[
            criterion('name', 'name of process', 1, [0, 2], 'Name one process, graded 2:0. Published example: ' + name),
            criterion('method', 'how the process is carried out', 3, [0, 2, 4], 'Three points for your chosen process, each graded 4:2:0. Published examination examples, not a validated preservation recipe: ' + method),
            criterion('principle', 'underlying principle', 2, [0, 2, 4], 'Two matching points, each graded 4:2:0. Complete published 2022 guidance: ' + principle),
        ]))
    variants.append(dict(id='another-process', label='Another valid process', rows=[
        criterion('name', 'name of process', 1, [0, 2], 'Name one suitable process, graded 2:0. The source examples are not an exhaustive option list.'),
        criterion('method', 'how the process is carried out', 3, [0, 2, 4], 'Three accurate details of the same process, each graded 4:2:0. No model for another process is printed.'),
        criterion('principle', 'underlying principle', 2, [0, 2, 4], 'Two accurate principles for the same process, each graded 4:2:0. No model for another process is printed.'),
    ]))
    preservation = add(2, 'b', '0-4', 'meat-preservation-profile', deepcopy(variants[0]['rows']), 'Name 2 (2:0); method 3 × 4; principle 2 × 4 (4:2:0)')
    preservation['answerVariants'] = variants
    agencies = after(s[12], 'Details: 2 points @ 4 marks (graded: 4:2:0)')
    add(2, 'c', '0-11', 'national-food-safety-agency', [
        criterion('name', 'Name', 1, [0, 2, 4], 'Name one agency, graded 4:2:0. Source correction: FSAI is the Food Safety Authority of Ireland, not “Association”. Published 2022 examples: ' + agencies),
        criterion('details', 'Details', 2, [0, 2, 4], 'Two accurate details of the role of the same agency, each graded 4:2:0. This deferred scheme gives names only; it prints no model role descriptions.'),
    ], 'Name 4; details 2 × 4 (all 4:2:0)')

    egg_nutrition = after(between(s[13], '(a)', '(b)'), '(graded: 4:3:2:1:0)')
    add(3, 'a', '0-9', 'eggs-nutritional-value', [criterion('nutrition', 'nutritive value', 5, list(range(5)), 'Five points, each graded 4:3:2:1:0. Discuss nutritive value and contribution to the diet; no fixed quota per nutrient is printed. “HBV 100%” is a biological-value description, not a claim that eggs are 100% protein. Published guidance: ' + egg_nutrition)], '5 points × 4 (4:3:2:1:0)')
    egg_properties = after(between(s[13], '(b)', '(c)'), 'Properties:')
    for label in ['Coagulation –', 'Emulsification -']: egg_properties = egg_properties.replace(' ' + label, '\n\n' + label)
    rows = []
    for i in range(1, 4):
        row = criterion(f'property-{i}', 'properties of eggs', 3, [0, 2], f'Property {i}: name (2:0), explanation (2:0) and matching culinary use (2:0). Use three different properties. ' + ('Source clarification: whisking introduces air and unfolds proteins; later heating sets the foam. The scheme’s frictional-heat account is misleading. Complete source guidance: ' + egg_properties if i == 1 else 'Use the complete source guidance and clarification above.'))
        for part, label in zip(row['parts'], ['Name', 'Explanation', 'Culinary use']): part['verbatim'] = label
        rows.append(row)
    add(3, 'b', '0-9', 'egg-properties-culinary-uses', rows, '3 properties × (name 2 + explanation 2 + culinary use 2), all 2:0')
    egg_safety = after(s[13].split('(c)', 1)[1], '(graded: 4:2:0)')
    add(3, 'c', '0-11', 'egg-quality-assurance', [criterion('quality', 'quality', 3, [0, 2, 4], 'Three points, each graded 4:2:0. Published 2022 guidance: ' + egg_safety)], '3 points × 4 (4:2:0)')
    shopping = after(between(s[14], '(a)', '(b)'), '(graded: 4:2:0)')
    add(4, 'a', '1-2', 'shopping-pattern-changes', [criterion('changes', 'changes', 5, [0, 2, 4], 'Five points, each graded 4:2:0. Identify changes and discuss their reasons, following the original paper wording. No fixed change/reason split is printed. Complete 2022 guidance: ' + shopping)], '5 points × 4 (4:2:0)')
    techniques = after(between(s[14], '(b)', '(c)'), '(graded: 5:4:3:0)')
    add(4, 'b', '1-2', 'supermarket-spending-techniques', [criterion('techniques', 'in-store techniques', 4, [0, 3, 4, 5], 'Four discussed techniques, each using the exact 5:4:3:0 ladder (no 1 or 2). The paper says “Discuss”; the scheme paraphrases it as “Describe”. Source examples are names rather than model discussions: ' + techniques)], '4 points × 5 (5:4:3:0)')
    voluntary = after(s[14], 'Role: 2 points @ 3 marks (graded: 3:2:0)')
    add(4, 'c', '1-2', 'voluntary-consumer-agency', [
        criterion('name', 'Name', 1, [0, 2, 4], 'Name one voluntary consumer-protection agency, graded 4:2:0. The scheme’s examples are open, not a compulsory two-option choice.'),
        criterion('role', 'Role', 2, [0, 2, 3], 'Two role details about the same agency, each graded 3:2:0. Full published 2022 examples and names: ' + voluntary),
    ], 'Name 4 (4:2:0); role 2 × 3 (3:2:0)')
    family_changes = after(between(s[15], '(a)', '(b)'), '(graded: 6:4:2:0)')
    add(5, 'a', '2-0', 'family-structure-changes', [criterion('changes', 'changes', 3, [0, 2, 4, 6], 'Three changes, each graded 6:4:2:0. “Today” refers to the 2022 examination. Published guidance: ' + family_changes)], '3 changes × 6 (6:4:2:0)')
    family_b = between(s[15], '(b)', '(c)')
    labels = ['Social:', 'Economic:', 'Technological:']; bodies = named_sections(family_b, labels)
    rows = [criterion(label[:-1].lower(), label[:-1], 1, [0, 2, 4], 'One point required on this heading, graded 4:2:0. Published 2022 guidance: ' + body) for label, body in zip(labels, bodies)]
    rows.append(criterion('others', 'others', 2, [0, 2, 4], 'Two further distinct points across the three headings, each graded 4:2:0. Do not score a point already used above again.'))
    add(5, 'b', '2-0', 'social-economic-technological-family-change', rows, '5 points × 4 (4:2:0): social 1; economic 1; technological 1; others 2')
    maintenance = after(s[15].split('(c)', 1)[1], '(graded: 4:2:0)')
    add(5, 'c', '2-1', 'family-maintenance-act', [criterion('protection', 'protection', 3, [0, 2, 4], 'Three points, each graded 4:2:0. This question concerns the named historical Act. Published 2022 examination guidance, not current legal advice: ' + maintenance)], '3 points × 4 (4:2:0)')
    assert len(cards) == 16 and sum(c['totalMarks'] for c in cards) == 280
    return cards


def write():
    cards = build(); docs = documents(); path = ROOT / 'scripts/markbank/authored/home-economics.json'; authored = json.loads(path.read_text())
    for c in cards:
        i = next((i for i, old in enumerate(authored) if old['id'] == c['id']), None)
        if i is None: authored.append(c)
        else: authored[i] = c
    path.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
    target = ROOT / f'public/exam-figures/home-economics/{FIGURE}.png'; docs['bc'][1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(BOUNDS)).save(target)
    sha = hashlib.sha256(target.read_bytes()).hexdigest(); assert sha == CROP_SHA256
    path = ROOT / 'components/MarkBank/figures-home-economics.json'; manifest = json.loads(path.read_text())
    manifest[FIGURE] = dict(src=f'/exam-figures/home-economics/{FIGURE}.png', md5=hashlib.md5(target.read_bytes()).hexdigest(),
        alt='Why consumers consult food labels: nutrient information 37%; calorie content 35%; specific ingredients 34%; allergen information 13%; food additives 3%; origin 3%. Horizontal axis: 0–40%.',
        attribution='SEC Home Economics 2022 Higher Level deferred examination paper, page 2; adapted from FSAI research — © State Examinations Commission.',
        sourceNote=f'Original chart, bounds {BOUNDS}, rendered at 2×. Source SHA256 {SOURCES["bc"]["sha256"]}. All six bars, values, labels and axis retained.')
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    path = ROOT / BASE / '2022-hl-deferred-review.json'; review = json.loads(path.read_text())
    review['tasks'] = [t for t in review['tasks'] if t['id'] not in {c['id'] for c in cards}] + [dict(id=c['id'], status='carded', section='B', questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    review['sectionStatus']['B'] = 'All 16 tasks carded; 280 offered marks.'
    review['sectionBReview'] = dict(paperPages=[2, 3, 4], schemePages=list(range(9, 16)), tasks=16, offeredMarks=280,
        decisions=['B1(a): one choose-four card with four 5-mark slots and the original six-category chart.', 'B1(b/c), B3(b) and B5(b) retain their required/dependent headings.', 'B2(b) is one open meat-preservation profile; all source processes and their complete guidance are available as routes.', 'B2(a/c) and B4(b) distinguish source lists from unprinted model explanations.', 'B4(a/b) retain the original paper’s verbs despite scheme paraphrases.', 'B4(b) uses the exact 5:4:3:0 ladder.', 'B5(b) reserves social/economic/technological points and two others.'], sourceClarifications=CLARIFICATIONS,
        figure=dict(key=FIGURE, bounds=BOUNDS, scale=2, sha256=sha))
    review['sectionBReview']['sourceDifferences'] = ['The paper’s B2 stem gives beef exports as €2.25 billion; the scheme says €2.5 billion. The card preserves the original paper stem.']
    review['sectionBReview']['clarificationsChecked'] = '2026-11-01'
    path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
    print('2022 Higher deferred B: all 16 tasks, 280 offered marks, original chart.')


if __name__ == '__main__':
    if '--write' in sys.argv: write()
    else: print(json.dumps(build(), ensure_ascii=False, indent=2))
