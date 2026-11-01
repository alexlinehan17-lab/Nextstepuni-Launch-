#!/usr/bin/env python3
"""Source-reviewed 2023 deferred B2–B5: twelve complete practice tasks."""
from copy import deepcopy
import json
import re
import sys
import fitz
from he_review_2023_hl import ROOT, tidy, between, criterion
from he_review_2023_hl_deferred import documents, deferred_card, BASE

CLARIFICATIONS = {
    'infant-gluten': dict(checked='2026-11-01', source='https://www.espghan.org/knowledge-center/publications/Gastroenterology/2024-Early-Life-Gluten-Free-Diet',
        note='The 2024 ESPGHAN position paper finds that introduction between completed 4 and 12 months does not change cumulative coeliac-disease incidence. The scheme’s before-six-months statement is historical examination wording, not a general current conclusion.'),
    'oats': dict(checked='2026-11-01', source='https://www2.hse.ie/conditions/coeliac-disease/treatment/',
        note='HSE distinguishes contamination of oats and individual sensitivity to avenin. Most people with coeliac disease tolerate avenin; HSE advises discussing oats with a dietitian. The scheme’s blanket “avoid oats” wording is retained as 2023 marking guidance.'),
}


def build():
    docs = documents()
    def text(doc, n): return tidy(doc[n - 1].get_text(clip=fitz.Rect(0, 0, 595, 770)))
    p3, p4 = text(docs['bc'], 3), text(docs['bc'], 4)
    p = {2: between(p3, 'Question 2', 'Question 3'), 3: p3.split('Question 3', 1)[1].strip(),
         4: between(p4, 'Question 4', 'Question 5'), 5: p4.split('Question 5', 1)[1].strip()}
    s = {n: text(docs['scheme'], n) for n in range(10, 18)}
    cards = []; questions = {}; stems = {}
    tariffs = {2: [22, 16, 12], 3: [24, 18, 8], 4: [16, 24, 10], 5: [20, 20, 10]}
    directives = {2: [[], ['one'], ['two', 'two']], 3: [['one'], ['one'], []], 4: [['four'], [], ['one']], 5: [['following'], [], []]}
    for n in range(2, 6):
        stems[n] = p[n].split('(a)', 1)[0].strip()
        # Scope to the printed part first: B5(a)/(b) share the same mark total.
        heads = list(re.finditer(r'\(([abc])\)', p[n])); assert [h[1] for h in heads] == list('abc')
        for i, h in enumerate(heads):
            body = p[n][h.end():heads[i + 1].start() if i + 1 < len(heads) else len(p[n])]
            question = body.split(f'({tariffs[n][i]} marks)', 1)[0].strip()
            assert f'({tariffs[n][i]} marks)' in body
            assert re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b', question, re.I) == directives[n][i]
            questions[(n, h[1])] = question
    def add(n, part, topic, concept, rows, notation):
        c = deferred_card(f'sb-q{n}{part}', 'B', f'Q{n}({part})', topic, concept, questions[n, part], stems[n],
                          tariffs[n]['abc'.index(part)], notation, rows, 3 if n <= 3 else 4)
        cards.append(c); return c
    def after(text, marker):
        assert text.count(marker) == 1, marker
        return text.split(marker, 1)[1].strip()
    def split_guidance(text, labels):
        result = []
        for i, label in enumerate(labels):
            assert text.count(label) == 1, label
            body = text.split(label, 1)[1]
            if i + 1 < len(labels): body = body.split(labels[i + 1], 1)[0]
            result.append(body.strip())
        return result

    # One account under three required headings, not three unrelated cards.
    causes = between(s[10], 'coeliac disease is an autoimmune', '• symptoms')
    causes = 'coeliac disease is an autoimmune ' + causes
    symptoms = between(s[10], 'abdominal pain;', '• specific dietary guidelines')
    symptoms = 'abdominal pain; ' + symptoms
    diet = between(s[10], 'choose gluten free foods;', '(b)')
    diet = 'choose gluten free foods; ' + diet
    add(2, 'a', '0-1', 'coeliac-disease-account', [
        criterion('causes', 'causes', 2, [0, 2, 4], 'Two cause points, each graded 4:2:0. Source clarification (ESPGHAN, 2024): introduction of gluten between completed four and twelve months has not been shown to change cumulative coeliac-disease incidence. The before-six-months statement below is historical examination wording. Published 2023 scheme guidance: ' + causes),
        criterion('symptoms', 'symptoms', 3, [0, 2], 'Three symptoms, each graded 2:0. Published guidance: ' + symptoms),
        criterion('diet', 'specific dietary guidelines', 2, [0, 2, 4], 'Two dietary points, each graded 4:2:0. Source clarification (HSE): ordinary oats can be contaminated; most people with coeliac disease tolerate avenin, but some react. HSE advises discussing oats with a dietitian. The broad “avoid oats” wording below is retained as 2023 marking guidance. Published guidance: ' + diet),
    ], 'Causes 2 × 4 (4:2:0); symptoms 3 × 2 (2:0); diet 2 × 4 (4:2:0)')
    aspect = after(s[10], 'aspect -')
    continuation = s[11].split('(c)', 1)[0]
    cause, effect, correction = split_guidance(continuation, ['cause-', 'cffect-', 'correction-'])
    add(2, 'b', '0-1', 'malnutrition-profile', [criterion(key, heading, 1, [0, 2, 4],
        'One aspect of malnutrition throughout: the cause, effect and correction must match your chosen aspect. This heading is graded 4:2:0. “Current” refers to the 2023 examination. Published examples: ' + body)
        for key, heading, body in [('aspect', 'aspect of malnutrition', aspect), ('cause', 'cause', cause), ('effect', 'effect', effect), ('correction', 'correction', correction)]],
        'Aspect 4; cause 4; effect 4; correction 4 (all 4:2:0)')
    agents = after(s[11], '2 Functions @ 4 marks (graded 4:2:0); 2 examples @ 2 marks (graded 2:0)')
    assert agents.endswith('Cesar salad; etc.')
    rows = []
    for i in range(1, 3):
        row = dict(id=f'pair-{i}', kind='criterion', verbatim='Functions', marks=6, permittedMarks=[0, 2, 4, 6],
            contextNote=f'Pair {i}: describe a different function and give a matching example of its use. Function graded 4:2:0; example graded 2:0. ' + ('Complete published guidance: ' + agents if i == 1 else 'Use the complete published guidance above.'),
            parts=[dict(id='function', verbatim='Function', marks=4, permittedMarks=[0, 2, 4]), dict(id='example', verbatim='Example of use', marks=2, permittedMarks=[0, 2])])
        rows.append(row)
    add(2, 'c', '0-11', 'physical-conditioning-agents', rows, '2 pairs: function 4 (4:2:0) + use 2 (2:0)')

    # Open methods and packaging materials use one profile with answer routes.
    method_text = after(s[12], '5 points @ 2 marks (graded 2:1:0)')
    methods = split_guidance(method_text, ['jam/ chutney making:', 'Bottling:', 'Drying:'])
    principle_text = between(s[13], 'Jam/chutney making', '(b)')
    jam, bottling, drying = split_guidance('Jam/chutney making ' + principle_text, ['Jam/chutney making', 'Bottling kills', 'Drying –'])
    jam, bottling_intro = jam.rsplit('bottling –', 1)
    principles = [jam.strip(), bottling_intro.strip() + ' Bottling kills ' + bottling, drying]
    variants = []
    for key, name, method, principle in zip(['jam-chutney', 'bottling', 'drying'], ['Jam/chutney making', 'Bottling', 'Drying'], methods, principles):
        variants.append(dict(id=key, label=name, rows=[
            criterion('name', 'name', 1, [0, 2], 'Name the method you describe, graded 2:0. Published example: ' + name),
            criterion('method', 'method of preservation', 5, [0, 1, 2], 'Five method points, each graded 2:1:0. Published examination outline (recipe-specific processing times are not supplied): ' + method),
            criterion('principle', 'underlying principle', 3, [0, 2, 4], 'Three principle points, each graded 4:2:0. Published guidance: ' + principle),
        ]))
    variants.append(dict(id='another-method', label='Another valid heat method', rows=[
        criterion('name', 'name', 1, [0, 2], 'Name a home food-preservation method involving heat. The printed examples end in “etc.”.'),
        criterion('method', 'method of preservation', 5, [0, 1, 2], 'Five accurate method points for your chosen method, each graded 2:1:0. The scheme supplies model guidance for jam/chutney making, bottling and drying only.'),
        criterion('principle', 'underlying principle', 3, [0, 2, 4], 'Three accurate principle points for the same method, each graded 4:2:0. No model for another method is printed.'),
    ]))
    preservation = add(3, 'a', '0-4', 'heat-preservation-profile', deepcopy(variants[0]['rows']), 'Name 2 (2:0); method 5 × 2 (2:1:0); principle 3 × 4 (4:2:0)')
    preservation['answerVariants'] = variants
    suitability = after(s[13], '• suitability of purpose 2 points @ 4 marks (graded 4:2:0)')
    impacts = between(s[14], '• environmental impact 2 points @ 4 marks (graded 4:2:0)', '(c)')
    suitability = split_guidance(suitability, ['Glass-', 'Plastic-', 'Metal-', 'Paper-'])
    impacts = split_guidance(impacts, ['Glass-', 'Plastic–', 'Metal-', 'Paper-'])
    variants = []
    for name, purpose, impact in zip(['Glass', 'Plastic', 'Metal', 'Paper'], suitability, impacts):
        variants.append(dict(id=name.lower(), label=name, rows=[
            criterion('name', 'Name', 1, [0, 2], 'Name one packaging material, graded 2:0. Published example: ' + name),
            criterion('purpose', 'suitability of purpose', 2, [0, 2, 4], 'Two points about your chosen material, each graded 4:2:0. Published 2023 guidance: ' + purpose),
            criterion('environment', 'environmental impact', 2, [0, 2, 4], 'Two points about the same material, each graded 4:2:0. Published 2023 guidance: ' + impact),
        ]))
    variants.append(dict(id='another-material', label='Another valid material', rows=[
        criterion('name', 'Name', 1, [0, 2], 'Name a suitable packaging material. The source list is open, not a compulsory choice between four.'),
        criterion('purpose', 'suitability of purpose', 2, [0, 2, 4], 'Two accurate suitability points, each graded 4:2:0. The scheme supplies models for glass, plastic, metal and paper only.'),
        criterion('environment', 'environmental impact', 2, [0, 2, 4], 'Two accurate environmental-impact points for the same material, each graded 4:2:0. No model for another material is printed.'),
    ]))
    packaging = add(3, 'b', '0-11', 'food-packaging-profile', deepcopy(variants[0]['rows']), 'Name 2 (2:0); suitability 2 × 4; environment 2 × 4 (4:2:0)')
    packaging['answerVariants'] = variants
    acts = after(s[14].split('(c)', 1)[1], '2 points @ 4 marks (graded 4:2:0)')
    add(3, 'c', '0-4', 'historical-food-drugs-acts', [criterion('protection', 'protection', 2, [0, 2, 4], 'Two points, each graded 4:2:0. This task concerns the historical Acts named in the question. Published 2023 examination guidance: ' + acts)], '2 points × 4 (4:2:0)')

    responsibilities = between(s[15], '4 points @ 4 marks (graded 4:2:0)', '(b)')
    add(4, 'a', '1-2', 'appliance-consumer-responsibilities', [criterion('responsibilities', 'responsibilities', 4, [0, 2, 4], 'Four distinct responsibilities, each graded 4:2:0. Published guidance: ' + responsibilities)], '4 responsibilities × 4 (4:2:0)')
    design, principle, use = split_guidance(s[15], ['• modern design features 2 points @ 3 marks (graded 3:2:0)', '• working principle 3 points @ 4 marks (graded 4:2:0)', '• guidelines for using the appliance 2 points @ 3 marks (graded 3:2:0)'])
    add(4, 'b', '1-3', 'microwave-study', [
        criterion('design', 'modern design features', 2, [0, 2, 3], 'Two design points, each graded 3:2:0. Published guidance: ' + design),
        criterion('principle', 'working principle', 3, [0, 2, 4], 'Three working-principle points, each graded 4:2:0. Published guidance: ' + principle),
        criterion('use', 'guidelines for using the appliance', 2, [0, 2, 3], 'Two use points, each graded 3:2:0. Published guidance: ' + use),
    ], 'Design 2 × 3 (3:2:0); principle 3 × 4 (4:2:0); use 2 × 3 (3:2:0)')
    names = ['Competition and Consumer Protection Commission', 'Office of the Ombudsman', 'Citizens Information Board', 'National Standards Authority of Ireland', 'European Consumer Centre']
    explanations = split_guidance(s[16], [name + (' –' if name == names[-1] else '-') for name in names])
    variants = [dict(id=re.sub(r'[^a-z]+', '-', name.lower()), label=name, rows=[
        criterion('name', 'Name', 1, [0, 1, 2], 'Name the agency you describe, graded 2:1:0. Published 2023 example: ' + name),
        criterion('explanation', 'Explanation', 2, [0, 2, 4], 'Two details about the same agency, each graded 4:2:0. Published 2023 guidance: ' + explanation),
    ]) for name, explanation in zip(names, explanations)]
    variants.append(dict(id='another-agency', label='Another valid statutory agency', rows=[
        criterion('name', 'Name', 1, [0, 1, 2], 'Name a statutory agency that protects consumers, graded 2:1:0. The paper does not restrict you to the examples in the scheme.'),
        criterion('explanation', 'Explanation', 2, [0, 2, 4], 'Two accurate details about that agency, each graded 4:2:0. No model for another agency is printed.'),
    ]))
    agency = add(4, 'c', '1-2', 'statutory-consumer-agency', deepcopy(variants[0]['rows']), 'Name 2 (2:1:0); explanation 2 × 4 (4:2:0)')
    agency['answerVariants'] = variants

    terms = between(s[17], 'Culture:', '(b)')
    term_names = ['Culture', 'Norms', 'Role', 'Social mobility']
    bodies = split_guidance('Culture: ' + terms, [name + ':' for name in term_names])
    add(5, 'a', '2-0', 'sociological-terms', [criterion(name.lower().replace(' ', '-'), name, 1, [0, 3, 5], 'Required term, graded 5:3:0. Published guidance: ' + body) for name, body in zip(term_names, bodies)], '4 required terms × 5 (5:3:0)')
    assert s[17].count('(b)') == 2  # source mislabels the final (c)
    changes = s[17].split('(b)', 1)[1].rsplit('(b)', 1)[0]
    economic, technological = split_guidance(changes, ['Economic:', 'Technological:'])
    add(5, 'b', '2-0', 'economic-technological-family-change', [
        criterion('economic', 'economic', 1, [0, 3, 5], 'At least one economic point, graded 5:3:0. Published 2023 guidance: ' + economic),
        criterion('technological', 'technological', 1, [0, 3, 5], 'At least one technological point, graded 5:3:0. Published 2023 guidance: ' + technological),
        criterion('other', 'other points', 2, [0, 3, 5], 'Two further distinct points from either heading, each graded 5:3:0. Do not score a point already used above again.'),
    ], '4 points × 5 (5:3:0): economic 1; technological 1; other 2')
    communication = after(s[17].rsplit('(b)', 1)[1], '2 points @ 5 marks (graded 5:3:0)')
    add(5, 'c', '2-0', 'family-communication', [criterion('communication', 'good communication', 2, [0, 3, 5], 'Two points, each graded 5:3:0. The paper labels this task (c); the scheme accidentally repeats (b). Published guidance: ' + communication)], '2 points × 5 (5:3:0)')
    assert len(cards) == 12 and sum(c['totalMarks'] for c in cards) == 200
    return cards


def write():
    cards = build(); path = ROOT / 'scripts/markbank/authored/home-economics.json'; authored = json.loads(path.read_text())
    for c in cards:
        i = next((i for i, old in enumerate(authored) if old['id'] == c['id']), None)
        if i is None: authored.append(c)
        else: authored[i] = c
    path.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
    path = ROOT / BASE / '2023-hl-deferred-review.json'; review = json.loads(path.read_text())
    review['tasks'] = [t for t in review['tasks'] if t['id'] not in {c['id'] for c in cards}] + [dict(id=c['id'], status='carded', section='B', questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    review['sectionStatus']['B'] = 'All 17 tasks carded; 280 offered marks. C remains open.'
    review['sectionBRemainingReview'] = dict(paperPages=[3, 4], schemePages=list(range(10, 18)), tasks=12, offeredMarks=200,
        decisions=['Required coeliac headings remain one 22-mark account (8+6+8).', 'Malnutrition remains one dependent four-heading profile.', 'Two physical-agent functions keep their paired examples in one task.', 'Heat method, packaging material and statutory agency are open choices with answer routes, not separate scheduled cards.', 'All microwave and sociological headings required.', 'Economic/technological change reserves one point per heading plus two others.', 'Paper B5(c) is authoritative despite the scheme’s repeated (b) label.'],
        sourceClarifications=CLARIFICATIONS)
    path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
    print('2023 Higher deferred B2–B5: twelve tasks, 200 offered marks; all B now carded.')


if __name__ == '__main__':
    if '--write' in sys.argv: write()
    else: print(json.dumps(build(), ensure_ascii=False, indent=2))
