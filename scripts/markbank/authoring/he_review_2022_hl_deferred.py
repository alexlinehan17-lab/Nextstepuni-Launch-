#!/usr/bin/env python3
"""Independently swept 2022 deferred sources; nineteen Section A tasks."""
import hashlib
import json
import re
import sys
import fitz
from he_review_2023_hl import ROOT, tidy, between, criterion
from he_review_2023_hl_deferred import a_regions, region_text, deferred_card, BASE
from he_review_2023_hl_deferred_c1 import after

SOURCES = {
    'a': dict(fileid='LC098ALP014EV.pdf', path='paper-trail-corpus/deferredexams/2022/LC098ALP014EV.pdf', sha256='5861dc717c7f278c4cc3f6b748349221c26a42789f72054442bfe4094ab14cb6', pages=40),
    'bc': dict(fileid='LC098ALP039EV.pdf', path='paper-trail-corpus/deferredexams/2022/LC098ALP039EV.pdf', sha256='8c0b8d9a47cc7bbdf52434650d64ba5a26f4e5e650985dfa0ed88cebf204de03', pages=12),
    'scheme': dict(fileid='LC098ALP000EV.pdf', path='paper-trail-corpus/deferredmarkingschemes/2022/LC098ALP000EV.pdf', sha256='8e9ff528232a53b0c03cd41d2a4f4a44fbcd294c0c2c3932182ae9a93e818e8f', pages=27),
}
CLARIFICATIONS = {
    'iron': dict(checked='2026-11-01', source='https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/',
        note='Haem/non-haem describes whether iron is part of haem. Ferrous/ferric describes its oxidation state. The scheme incorrectly treats these as synonymous pairs.'),
    'diabetes': dict(checked='2026-11-01', source='https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes',
        note='Diabetes involves raised blood glucose due to inadequate insulin production, impaired insulin action, or both; the scheme omits impaired insulin action.'),
}
SELECTION = {1: ['two'], 2: ['each', 'following'], 3: ['two'], 4: ['each'], 5: ['each', 'following'],
             6: ['two'], 7: ['following'], 8: ['two'], 9: ['each', 'following'], 10: ['three'],
             11: ['following'], 12: ['two'], 13: ['two'], 14: ['two']}


def documents():
    docs = {}
    for key, source in SOURCES.items():
        path = ROOT / source['path']; assert hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256']
        docs[key] = fitz.open(path); assert len(docs[key]) == source['pages']
    return docs


def build():
    docs = documents(); pr = a_regions(docs['a'], range(3, 8), body_bottom=760); sr = a_regions(docs['scheme'], range(4, 9), body_bottom=775)
    p = {n: region_text(docs['a'], r) for n, r in pr.items()}; s = {n: region_text(docs['scheme'], r) for n, r in sr.items()}
    for n, question in p.items():
        assert re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b', question, re.I) == SELECTION[n], (n, question)
    def clean(body): return re.sub(r'\(i{1,3}\)\s*', '', body).strip()
    table_items = {2: ['Maillard reaction', 'Carmelisation'], 4: ['Anaemia', 'Rickets', 'Beriberi'],
                   5: ['Haem iron', 'Non‐haem iron'], 7: ['Thick soups', 'Thin/Clear soups', 'Cold soups'],
                   9: ['Food contaminants', 'Cross contamination'], 11: ['Condenser', 'Thermostat']}
    def question(n):
        text = clean(re.sub(r'^\d+\.\s*', '', p[n]))
        if n in table_items:
            labels = table_items[n]
            for label in labels: assert label in text
            text = text.split(labels[0], 1)[0].strip()
            if n == 7: text = text.split('Classification Example', 1)[0].strip() + '\nClassification → Example:'
            text += '\n' + '\n'.join('• ' + label for label in labels)
        return text
    cards = []
    def add(n, topic, concept, rows, marks=6, suffix='', prompt=None, stem='', notation=''):
        label = {'-mycoprotein': 'mycoprotein', '-factors': 'energy factors', '-meal-factors': 'meal-planning factors', '-effects': 'irradiation effects', '-components': 'management components'}
        ref = f'Q{n}' + (' — ' + label[suffix] if suffix else '')
        if prompt: assert prompt in clean(re.sub(r'^\d+\.\s*', '', p[n])), prompt
        c = deferred_card(f'sa-q{n}{suffix}', 'A', ref, topic, concept, prompt or question(n), stem, marks, notation, rows, pr[n]['page'])
        c['id'] = c['id'].replace('2023', '2022'); c['year'] = 2022
        c['questionRef'] = c['questionRef'].replace('2023', '2022')
        c['sourceMaterial']['attribution'] = c['sourceMaterial']['attribution'].replace('2023', '2022')
        c['notes'] = '2022 deferred paper and scheme independently reviewed; see he_review_2022_hl_deferred.py and home-economics/2022-hl-deferred-review.json. Required headings and dependent profiles remain one response; independently priced tasks retain separate identities.'
        cards.append(c); return c
    properties = clean(between(s[1], '(graded 2:0)', 'What is mycoprotein?'))
    add(1, '0-5', 'protein-properties', [criterion('properties', 'properties of protein', 2, [0, 2], 'Two properties, each graded 2:0. Complete guidance: ' + properties)], 4, prompt='State two properties of protein.', notation='2 properties × 2 (2:0)')
    add(1, '0-5', 'mycoprotein-definition', [criterion('mycoprotein', 'mycoprotein', 1, [0, 1, 2], 'Definition graded 2:1:0. Published guidance: ' + after(s[1], '(graded 2:1:0)'))], 2, '-mycoprotein', prompt='What is mycoprotein?', notation='2 marks (2:1:0)')
    reactions = [('Maillard reaction', between(s[2], '(i) Maillard reaction', '(ii) Carmelisation')), ('Carmelisation', after(s[2], '(ii) Carmelisation'))]
    add(2, '0-6', 'carbohydrate-reactions', [criterion(key.lower().replace(' ', '-'), key, 1, [0, 1, 2, 3], 'Required term, graded 3:2:1:0. Published guidance: ' + body) for key, body in reactions], notation='2 required terms × 3 (3:2:1:0)')
    add(3, '0-1', 'basal-metabolic-rate', [criterion('bmr', 'Basal Metabolic Rate', 1, [0, 1, 2, 3, 4], 'Definition graded 4:3:2:1:0. Published guidance: ' + between(s[3], '(graded 4:3:2:1:0)', 'List two factors'))], 4, prompt='Explain Basal Metabolic Rate (BMR).', notation='4 marks (4:3:2:1:0)')
    add(3, '0-1', 'energy-requirement-factors', [criterion('factors', 'energy requirements', 2, [0, 1], 'Two factors, each graded 1:0. Complete guidance: ' + clean(after(s[3], '(graded 1:0)')))], 2, '-factors', prompt='List two factors that affect energy requirements.', notation='2 factors × 1 (1:0)')
    conditions = [('Anaemia', 'Vitamin C; Vitamin B12'), ('Rickets', 'Vitamin D'), ('Beriberi', 'Vitamin B1 (thiamine)')]
    add(4, '0-8', 'vitamin-deficiency-conditions', [criterion(name.lower(), name, 1, [0, 2], 'Identify one vitamin for this required condition; graded 2:0. Published accepted answer(s): ' + body) for name, body in conditions], notation='3 required conditions × 2 (2:0)')
    irons = [('Haem iron', between(s[5], '(i) Haem iron', '(ii) Non-haem iron')), ('Non-haem iron', after(s[5], '(ii) Non-haem iron'))]
    add(5, '0-8', 'haem-nonhaem-iron', [criterion(name.lower().replace(' ', '-'), name, 1, [0, 1, 2, 3],
        'Required term, graded 3:2:1:0. Source clarification (NIH): haem iron is bound within haem; non-haem iron is outside haem. Haem/non-haem is not another name for ferrous/ferric, which describes oxidation state. Haem iron is generally more readily absorbed. Historical scheme wording: ' + body) for name, body in irons], notation='2 required terms × 3 (3:2:1:0)')
    diabetes = between(s[6], '(graded 4:2:0)', 'State two factors')
    add(6, '0-1', 'diabetes-definition', [criterion('diabetes', 'diabetes', 1, [0, 2, 4], 'Definition graded 4:2:0. Source clarification (NIDDK): diabetes involves raised blood glucose due to inadequate insulin production, impaired insulin action, or both. The scheme omits impaired insulin action. Historical scheme wording: ' + diabetes)], 4, prompt='Define diabetes.', notation='4 marks (4:2:0)')
    diet_question = 'State two factors ' + between(p[6], 'State two factors', '(i)')
    add(6, '0-1', 'diabetes-meal-planning', [criterion('factors', 'planning meals', 2, [0, 1], 'Two factors, each graded 1:0. Published 2022 examination guidance: ' + clean(after(s[6], '(graded 1:0)')))], 2, '-meal-factors', prompt=diet_question, notation='2 factors × 1 (1:0)')
    soups = [('Thick soups', between(s[7], 'Thick soups', 'Thin/Clear soups')), ('Thin/Clear soups', between(s[7], 'Thin/Clear soups', 'Cold soups')), ('Cold soups', after(s[7], 'Cold soups'))]
    add(7, '0-3', 'soup-classification-examples', [criterion(str(i), name, 1, [0, 1, 2], 'Give one example for this required classification; graded 2:1:0. Published guidance: ' + body) for i, (name, body) in enumerate(soups, 1)], notation='3 examples × 2 (2:1:0)')
    add(8, '0-4', 'irradiated-food-definition', [criterion('irradiation', 'irradiated food', 1, [0, 1, 2], 'Definition graded 2:1:0. Published guidance: ' + after(s[8].split('State two effects', 1)[0], '(graded 2:1:0)'))], 2, prompt='What is irradiated food?', notation='2 marks (2:1:0)')
    effects = after(s[8].split('State two effects', 1)[1], '(graded 2:1:0)')
    add(8, '0-4', 'food-irradiation-effects', [criterion('effects', 'effects of irradiation', 2, [0, 1, 2], 'Two effects, each graded 2:1:0. Complete guidance: ' + clean(effects))], 4, '-effects', prompt='State two effects of irradiation on food.', notation='2 effects × 2 (2:1:0)')
    contaminants = [('Food contaminants', between(s[9], '(i) Food contaminants -', '(ii) Cross contamination -')), ('Cross contamination', after(s[9], '(ii) Cross contamination -'))]
    add(9, '0-4', 'food-contamination-terms', [criterion(str(i), name, 1, [0, 1, 2, 3], 'Required term, graded 3:2:1:0. Published guidance: ' + body) for i, (name, body) in enumerate(contaminants, 1)], notation='2 required terms × 3 (3:2:1:0)')
    purpose = between(s[10], '(graded 3:2:0)', 'List three components')
    add(10, '1-0', 'family-resource-management-purpose', [criterion('purpose', 'family resource management systems', 1, [0, 2, 3], 'Purpose graded 3:2:0. Published guidance: ' + purpose)], 3, prompt='State the purpose of family resource management systems.', notation='3 marks (3:2:0)')
    add(10, '1-0', 'family-resource-management-components', [criterion('components', 'components', 3, [0, 1], 'Three components, each graded 1:0. Published answers: Inputs; Throughputs; Outputs.')], 3, '-components', prompt='List three components of family resource management systems.', notation='3 components × 1 (1:0)')
    fridge = [('Condenser', between(s[11], '(i) Condenser -', '(ii) Thermostat -')), ('Thermostat', after(s[11], '(ii) Thermostat -'))]
    add(11, '1-3', 'refrigerator-components', [criterion(name.lower(), name, 1, [0, 1, 2, 3], 'Required component, graded 3:2:1:0. Published guidance: ' + body) for name, body in fridge], notation='2 required components × 3 (3:2:1:0)')
    name = after(s[12].split('Outline two effects', 1)[0], '(graded 2:0)')
    effects = clean(after(s[12].split('Outline two effects', 1)[1], '(graded 2:0)'))
    add(12, '1-4', 'flame-retardant-finish', [criterion('name', 'Name', 1, [0, 2], 'Name one finish, graded 2:0. Published examples: ' + name),
        criterion('effects', 'effects', 2, [0, 2], 'Two effects of the finish you named, each graded 2:0. Keep the name and effects together. Complete guidance: ' + effects)], notation='Name 2; effects 2 × 2 (all 2:0)')
    add(13, '1-1', 'working-family-payment-eligibility', [criterion('conditions', 'Working Family Payment', 2, [0, 2, 3], 'Two conditions, each graded 3:2:0. The eligibility wording below belongs to the 2022 examination, not current benefits advice. Published guidance: ' + clean(after(s[13], '(graded 3:2:0)')))], notation='2 conditions × 3 (3:2:0)')
    add(14, '1-1', 'mabs-functions', [criterion('functions', 'Money Advice and Budgeting Service', 2, [0, 2, 3], 'Two functions, each graded 3:2:0. Complete published guidance: ' + clean(after(s[14], '(graded 3:2:0)')))], notation='2 functions × 3 (3:2:0)')
    assert len(cards) == 19 and sum(c['totalMarks'] for c in cards) == 84
    return cards, pr, sr


def write():
    cards, pr, sr = build(); docs = documents()
    path = ROOT / 'scripts/markbank/authored/home-economics.json'; authored = json.loads(path.read_text())
    for c in cards:
        i = next((i for i, old in enumerate(authored) if old['id'] == c['id']), None)
        if i is None: authored.append(c)
        else: authored[i] = c
    path.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
    path = ROOT / 'examiner-reports/home-economics/schemes/2022-hl-deferred.md'
    path.write_text('# SEC Home Economics 2022 Higher deferred marking scheme\n\n' + '\n\n'.join(
        f'## Physical page {i+1}\n\n' + '\n'.join(line.rstrip() for line in p.get_text().splitlines()).strip()
        for i, p in enumerate(docs['scheme'])).rstrip() + '\n')
    review = dict(schemaVersion=1, year=2022, level='higher', sitting='deferred', language='ev',
        status='partial-carding; all-source-pages-visually-reviewed; browser-QA-pending', sources=SOURCES,
        visualSweep=dict(a='All 40 pages: cover 1, instructions 2, questions 3–7, answer instructions 8, ruled pages 9–39, back cover 40.',
                         bc='All 12 pages: cover 1, B 2–4, C 5–8, explicit blanks 9–11, back cover 12.',
                         scheme='All 27 pages: cover 1, deferred notice 2, candidate rubric 3, A 4–8, B 9–15, C 16–25, blank 26, back cover 27.'),
        sectionStatus=dict(A='All 19 tasks carded; 84 offered marks.', B='16 tasks open; 280 offered marks.', C='26 tasks open; 385 offered marks.'),
        offeredPracticeMarks=749, candidateMarks=[200, 240],
        boundaryDecisions=['A1: protein properties 4 and mycoprotein definition 2 are independent.', 'A3: BMR 4 and energy factors 2 are independent.', 'A6: diabetes definition 4 and meal factors 2 are independent.', 'A8: definition 2 and irradiation effects 4 are independent.', 'A10: management purpose 3 and components 3 are independent.', 'A12 is one dependent finish-name/effects response; table headings remain one response for A2/A4/A5/A7/A9/A11.', 'A13 eligibility is historical examination content.', 'A3 paper anchor must retain the second response row down to y=741.5; 2023’s shorter page cutoff is unsuitable.'],
        pendingDecisions=['B1(a): one choose-four response with the original six-category chart; no combinations.', 'C1(a)(i): original 2020 fuel table needed; paper night rate 9.60 differs from scheme 15.21. Use the paper data.', 'C1(a)(ii): one open heating-system profile, source guidance continues on p17; passive/active solar wording needs clarification.', 'C1(c)(ii): check carbon monoxide/global-warming and acid-rain wording before carding.', 'C2(a)(ii) carries the earlier sketch prompt; C2(b) is an open blended-fabric profile.', 'C3(b)(i): one family impact, one society impact and one further impact, plus two risk groups.', 'C4(c)(ii): four factors, scored as two at 5:3:0 plus two at 4:2:0; do not invent four equal shares.', 'B2(c) calls FSAI an Association; the correct body name is Food Safety Authority of Ireland. C4(b)(i) bacterial-growth simplifications need source clarifications.'],
        sourceErrors=['Scheme p4 heading says Section A 60; paper and rubric give 30 (five of fourteen 6-mark questions).', 'Scheme p9 heading says Section B 180; paper and rubric give 130 (80 plus one 50).'],
        sourceClarifications=CLARIFICATIONS, paperRegionsA=pr, schemeRegionsA=sr,
        tasks=[dict(id=c['id'], status='carded', section='A', questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards])
    path = ROOT / BASE / '2022-hl-deferred-review.json'
    if path.exists():
        old = json.loads(path.read_text()); review['tasks'] += [t for t in old.get('tasks', []) if t['section'] != 'A']
        for section in ['B', 'C']: review['sectionStatus'][section] = old.get('sectionStatus', {}).get(section, review['sectionStatus'][section])
        for key in old:
            if key.startswith(('sectionB', 'sectionC')) or key in ['completion', 'resolvedDecisions']: review[key] = old[key]
        if 'completion' in old:
            review['status'] = old['status']
            review['pendingDecisions'] = old['pendingDecisions']
    path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
    print('2022 Higher deferred Section A: 19 practice tasks, 84 offered marks; preserved existing B/C review.')


if __name__ == '__main__':
    if '--write' in sys.argv: write()
    else: print(json.dumps(build()[0], ensure_ascii=False, indent=2))
