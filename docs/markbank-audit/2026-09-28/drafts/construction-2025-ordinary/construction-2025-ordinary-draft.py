"""Draft the 2025 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Question wording and stems are lifted from the SEC paper (a narrowed task only deletes printed
words); every row's verbatim is printed in the scheme's mark tables (pages 17-25), checked against
rendered pages. Unbanded components accept any whole mark up to the published maximum; printed
excellent/good/fair bands are kept as printed. Sources are the byte-identical paper-trail-corpus
copies, pinned by SHA-256. Figures are exact 2x crops.

The 21 pre-audit 2025 Ordinary cards keep their IDs (and concept IDs) and are corrected in place
to the reviewed boundaries and tariffs; each correction records the SHA-256 of the card it
replaces. Every other prior card stays byte-identical.
"""
import copy
import hashlib
import json
import re
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
R = HERE.parents[4]
P = 'paper-trail-corpus/exampapers/2025/LC029GLP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2025/LC029GLP000EV.pdf'
HASHES = {P: '6aca987b0c66e490252998240bde8e2ca6f30f992a425db364bb2ec643b2fa4d',
          S: 'ea1b7818d3caac4ff8e7b712e4abe3899245c7051ba66520d6ff81c9ca5612d9'}
ATTRIBUTION = 'SEC Leaving Certificate Construction Studies 2025 Ordinary Level — © State Examinations Commission.'
FP = 'construction-studies-2025-OL-'
PREFIX = 'cons-2025-ol-'
CROSS = 'construction-studies-ordinary-'
BAND8 = [0, 4, 6, 8]
BAND5 = [0, 1, 3, 5]
PAGE = [48, 46, 578, 800]

for f, h in HASHES.items():
    assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f

# The pre-audit cards are snapshotted before integration so the draft regenerates byte-identically afterwards.
LEGACY_FILE = HERE / 'prior-2025-ordinary-cards.json'
if not LEGACY_FILE.exists():
    AUTHORED = json.loads((R / 'scripts/markbank/authored/construction-studies.json').read_text())
    LEGACY_FILE.write_text(json.dumps([c for c in AUTHORED if c['id'].startswith(PREFIX)], ensure_ascii=False, indent=2) + '\n')
LEGACY = {c['id']: c for c in json.loads(LEGACY_FILE.read_text())}
assert len(LEGACY) == 21, sorted(LEGACY)


def card_hash(c):
    return hashlib.sha256(json.dumps(c, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


FIGURES = {
    'q1-original': (P, 2, [45, 40, 580, 262], False), 'q2-original': (P, 2, [45, 280, 580, 500], False),
    'q3-original': (P, 2, [45, 515, 580, 775], False), 'q4-original': (P, 3, [45, 40, 580, 290], False),
    'q5-original': (P, 3, [45, 300, 580, 510], False), 'q6-original': (P, 3, [45, 520, 580, 772], False),
    'q7-original': (P, 4, [45, 50, 580, 368], False), 'q8-original': (P, 4, [45, 380, 580, 482], False),
    'q9-original': (P, 4, [45, 495, 580, 770], False),
    'q1-scheme': (S, 4, PAGE, True), 'q1-section': (S, 4, [80, 108, 480, 568], True),
    'q2-method': (S, 5, [48, 222, 578, 654], True), 'q2-light': (S, 5, [48, 655, 578, 790], True),
    'q3-system': (S, 6, [30, 118, 560, 570], True), 'q3-zoning': (S, 6, [48, 598, 578, 790], True),
    'q4-sites': (S, 7, [48, 100, 578, 420], True), 'q4-site-a': (S, 7, [48, 425, 578, 790], True),
    'q5-section': (S, 9, [48, 84, 578, 575], True), 'q5-glue-blocks': (S, 9, [48, 580, 578, 790], True),
    'q6-signs': (S, 10, [48, 84, 578, 352], True), 'q6-risks': (S, 10, [48, 356, 578, 530], True),
    'q6-access': (S, 10, [48, 540, 578, 795], True), 'q7-office-plan': (S, 11, [48, 290, 578, 790], True),
    'q9-modifications': (S, 16, [48, 243, 578, 535], True), 'q9-uses': (S, 16, [48, 547, 578, 790], True),
}
question_figures = []
for key, (f, page, rect, solution) in FIGURES.items():
    with fitz.open(R / f) as pdf:
        px = pdf[page - 1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(rect), alpha=False)
    path = HERE / f'{FP}{key}.png'
    px.save(path)
    question_figures.append(dict(key=FP + key, source=f, page=page, rect=rect, renderScale=2, solution=solution,
                                 sha256=hashlib.sha256(path.read_bytes()).hexdigest(), visuallyInspected=True))


def page_hash(f, page):
    with fitz.open(R / f) as pdf:
        return hashlib.sha256(' '.join(pdf[page - 1].get_text().split()).encode()).hexdigest()


def checks(paper_page, scheme_pages):
    return ([dict(file=P, page=p, textSha256=page_hash(P, p)) for p in (1, paper_page)]
            + [dict(file=S, page=p, textSha256=page_hash(S, p)) for p in [2, 3, *scheme_pages]])


def row(rid, verbatim, marks, note, steps=None):
    steps = steps or list(range(marks + 1))
    assert steps[0] == 0 and steps[-1] == marks
    return dict(id=rid, kind='criterion', verbatim=verbatim, marks=marks, contextNote=note, permittedMarks=steps)


QUESTIONS = {
    '1': dict(page=2, title='External wall and window head section', concept='window-head-section',
              stem='The sketch shows the external wall and window of a dwelling house. The wall is a 400 mm concrete block wall with full-fill insulated cavity and is plastered on both sides. The fixed frame of the window is 120 mm × 80 mm and is thermally broken.',
              note='Original sketch and specification retained. Construction details, dimensions and draughting belong to part (a); the window-head detail in (b) is marked separately. Any alternative detailing that complies with current Building Regulations is acceptable.'),
    '2': dict(page=2, title='Insulating a sloped ceiling', concept='sloped-ceiling-insulation',
              stem='The sketch shows a living area with a sloped ceiling under construction. The homeowners wish to have a high level of insulation in the sloped ceiling.',
              note='Original sketch retained. The method, insulation type and the daylight feature are open choices; the scheme lists typical examples.'),
    '3': dict(page=2, title='Wood pellet stove heating and hot water', concept='pellet-stove-heating',
              stem='A wood pellet stove is used to heat radiators and supply hot water in a dwelling house.',
              note='Original sketch retained. The listed components are required content, not a choice. The scheme diagram is one acceptable layout; any alternative that complies with current Building Regulations is acceptable.'),
    '4': dict(page=3, title='Choosing a site in the countryside', concept='countryside-site',
              stem='The image shows a portion of a site location map. A and B are two sites being considered for a new dwelling house in the countryside.',
              note='Original site map retained. Choosing site A or B is part of the answer and is itself marked; reasons, positions and the sketch follow the chosen site.'),
    '5': dict(page=3, title='Closed string stairs and landing section', concept='closed-string-stairs-section',
              stem='The sketch shows portion of a closed string wooden stairs and first floor landing. The rise of each step is 170 mm. The landing has a 20 mm tongue and groove floor on 225 mm × 50 mm timber joists.',
              note='Original sketch and specification retained. Construction details, dimensions and draughting belong to part (a); the anti-creak detail in (b) is marked separately.'),
    '6': dict(page=3, title='Personal protective equipment and working at height', concept='ppe-working-at-height', stem='',
              note='All three printed PPE items in (a) are required and separately marked. Risks and the safety measure are open; the scheme lists typical examples.'),
    '7': dict(page=4, title='Designing a garden office', concept='garden-office',
              stem='A draft design for a garden office room is shown. The office room is of timber frame construction and has an exterior timber decking.',
              note='Original plan retained. All four printed items in (b) are required in one sketch; locations and reasons are open, well-reasoned responses.'),
    '8': dict(page=4, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=4, title='Outdoor living for a 1970s bungalow', concept='bungalow-outdoor-living',
              stem='The sketch shows the rear of a 1970’s bungalow. The bungalow overlooks a large rear garden. The homeowners wish to make better use of their large garden by adding an outdoor dining/living space.',
              note='Original sketch retained. Reasons, modifications and uses are open responses; the scheme lists typical examples.'),
}
SCHEME_PAGES = {'1': [4, 17], '2': [5, 18], '3': [6, 19], '4': [7, 8, 20], '5': [9, 21], '6': [10, 22],
                '7': [11, 12, 23], '9': [16, 25]}

tasks, bindings, cards = [], [], {}


def add(q, key, ref, text, rows, nodes, topics, figure, review, boundary, selection, scheme_pages=None, groups=None):
    meta = QUESTIONS[q]
    cid = f'{PREFIX}q{q}' + (f'-{key}' if key else '')
    concept = LEGACY[cid]['conceptId'] if cid in LEGACY else meta['concept'] + (f'-{key}' if key else '')
    card = dict(id=cid, subjectId='construction-studies', year=2025, level='ordinary', section='B',
                topicId=nodes[0], conceptId=concept, questionRef=f'2025 OL Q{q}{ref}',
                stem=meta['stem'], questionText=text, tariffModel={'kind': 'fixed'},
                totalMarks=sum(r['marks'] for r in rows), rows=rows,
                questionFigureKey=f'{FP}q{q}-original', questionFigureIncludesPrompt=True)
    if figure:
        card['figureKey'] = FP + figure
    card['sourceMaterial'] = dict(kind='source-illustration', label=f'ORIGINAL QUESTION {q}', title=meta['title'],
                                  pages=[1, meta['page']], attribution=ATTRIBUTION, presentationNote=meta['note'])
    if groups:
        card['taskGroups'] = groups
    tasks.append(dict(questionNumber=q, correction=cid in LEGACY, card=card,
                      sourceChecks=checks(meta['page'], scheme_pages or SCHEME_PAGES[q]),
                      boundaryReview=boundary, selectionReview=selection,
                      requiredQuestionFigures=[f'{FP}q{q}-original'], requiredSolutionFigures=[FP + figure] if figure else []))
    bindings.append(dict(cardId=cid, markBankTopicId=nodes[0], canonicalTopicIds=nodes, canonicalTopicReview=review,
                         questionNumber=q, atlasTopicIds=[CROSS + t for t in topics]))
    cards[cid] = card
    return card


def compose(q, key, ref, children, figure, boundary, selection, text, labels=None, scheme_pages=None):
    rows, groups = [], []
    for i, child in enumerate(children):
        prefix = child['id'].removeprefix(f'{PREFIX}q{q}-')
        rs = copy.deepcopy(child['rows'])
        for r in rs:
            r['id'] = f"{prefix}-{r['id']}"
        rows += rs
        groups.append(dict(sourceCardId=child['id'], label=labels[i] if labels else prefix, marks=child['totalMarks'],
                           rowIds=[r['id'] for r in rs]))
    kids = [next(b for b in bindings if b['cardId'] == c['id']) for c in children]
    nodes = list(dict.fromkeys(n for b in kids for n in b['canonicalTopicIds']))
    topics = list(dict.fromkeys(t.removeprefix(CROSS) for b in kids for t in b['atlasTopicIds']))
    return add(q, key, ref, text, rows, nodes, topics, figure, 'Keeps the union of its separately reviewed constituent tasks.',
               boundary, selection, scheme_pages=scheme_pages, groups=groups)


def parts(*cs):
    return '\n\n'.join(f'({letter}) {c["questionText"]}' for letter, c in zip('abc', cs))


# ---------------------------------------------------------------- Q1
B1 = 'Scheme p17 (printed 15): (a) best 7 of 11 listed details × 5 = 35, any 3 typical dimensions 3, draughting/accuracy/scale 8 (8/6/4) = sub-total 11, both printed within part (a): 46; (b) stepped DPC clearly identified 4. Complete 50.'
S1 = 'One required section and one required window-head detail. The best-seven detail list is a marking menu, not a printed choose-seven task.'
A1 = add('1', 'a', '(a)',
         'To a scale of 1:5, draw a vertical section through the external wall and top portion of the window. Show the wall, the concrete lintels, and the top fixed frame of the window. On your drawing, show the typical construction details from a level 400 mm below to a level 400 mm above the concrete lintels. Include three typical dimensions on your drawing.',
         [row('details', 'Any 7 x 5 marks', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: external render; concrete block outer leaf; full-fill insulated cavity with wall tie; concrete block inner leaf; internal plaster; cavity closer; stepped DPC; concrete lintels; thermally broken window frame; triple glazing; airtightness. The model specifies 19 mm render, 100 mm leaves, a 200 mm insulated cavity, 100 mm × 75 mm concrete lintels, 15 mm plaster and airtightness tape.', list(range(0, 36, 5))),
          row('dimensions', 'Any 3 typical dimensions', 3, 'Three appropriate typical dimensions on the section.'),
          row('presentation', 'Draughting, accuracy, and scale', 8, 'Draughting, accuracy and scale of the section: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-3-3', 'cons-3-4', 'cons-3-6', 'cons-6-2'],
         ['question-one-drawing-questions', 'foundations-floors-walls', 'windows-doors', 'heat-loss-insulation'], 'q1-scheme',
         'Scaled drawing (1.5) of a cavity external wall (3.3) with lintels and DPC (3.4) at a window head (3.6) and an insulated cavity (6.2).', B1, S1)
B1b = add('1', 'b', '(b)', 'On your drawing, show the typical design detailing that prevents the penetration of rainwater at the window head.',
          [row('stepped-dpc', 'Stepped DPC clearly identified', 4, 'Show and identify the stepped DPC over the concrete lintels at the window head, as in the scheme’s model section.', [0, 4])],
          ['cons-3-4', 'cons-3-6'], ['foundations-floors-walls', 'windows-doors'], 'q1-section', 'Damp-proof course (3.4) at the window head (3.6).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-scheme', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p18 (printed 16): (a) two advantages × 6 = 12; (b) method note & sketch 8 + 8 = 16, insulation type 4, thickness 4 = 24; (c) note 7 + sketch 7 = 14. Complete 50.'
S2 = '"one suitable method" and "one feature" are open choices with no printed list; each part stays one response.'
A2 = add('2', 'a', '(a)', 'Discuss two advantages of highly insulating the sloped ceiling of the living area.',
         [row('advantage-1', 'Advantage 1', 6, 'Such as: less heat loss, so the house is more energy efficient; lower energy bills.'),
          row('advantage-2', 'Advantage 2', 6, 'A second, different advantage. Such as: a smaller carbon footprint and lower carbon emissions; more comfortable rooms; less noise from outside; less condensation in the roof.')],
         ['cons-6-2', 'cons-6-3'], ['heat-loss-insulation'], None, 'Benefits of insulation (6.2) through reduced heat loss and running costs (6.3).', B2, S2)
B2b = add('2', 'b', '(b)', 'Using notes and freehand sketches, show one suitable method of highly insulating the sloped ceiling. Show on your sketch how the ceiling is to be finished internally. Specify the type and thickness of insulation.',
          [row('method', 'Method of insulating the sloped ceiling note & sketch (8 + 8 marks)', 16, 'Note 8 and sketch 8 of one method, showing the internal finish. Such as: insulation cut to fit between the rafters with a ventilation space below the breather membrane, an airtight membrane over the insulated rafters, then plasterboard or insulated plasterboard fixed to the rafters and skimmed or taped and filled; or a ventilation card between the rafters with spray-foam insulation trimmed flush, then plasterboard and skim.'),
           row('type', 'Preferred insulation type for sloped ceiling', 4, 'Such as: expanded polystyrene (EPS), phenolic, polyisocyanurate (PIR) or extruded polystyrene (XPS); the method notes also name wood fibre and sheep’s wool.'),
           row('thickness', 'Thickness of insulation', 4, 'At least 200 mm of insulation.')],
          ['cons-3-9', 'cons-6-2'], ['roofs', 'heat-loss-insulation'], 'q2-method', 'Roof insulation (3.9) and insulating materials (6.2).', B2, S2)
C2 = add('2', 'c', '(c)', 'Using notes and a freehand sketch, suggest one feature which could be included in the sloped ceiling to allow additional natural light into the living area.',
         [row('note', 'Note', 7, 'Such as: a skylight, a dormer window, a ridge roof-light or a sun tunnel.'),
          row('sketch', 'Sketch', 7, 'Freehand sketch of the chosen feature in the sloped ceiling.')],
         ['cons-3-5', 'cons-3-9'], ['windows-doors', 'roofs'], 'q2-light', 'A roof window (3.5) in the roof covering (3.9).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-method', B2, S2, parts(A2, B2b, C2))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p19 (printed 17): (a) best 8 of 13 listed items × 5 = 40 and quality of sketch 5 (5/3/1), both printed within part (a): 45; (b) one advantage 5. Complete 50.'
S3 = 'The printed component list is required content, not a choice; the best-eight list is a marking menu.'
A3 = add('3', 'a', '(a)', 'Draw a large freehand sketch of the given house and, on your sketch, show the pipework necessary to supply hot water from the stove to the radiators and to heat the water in the cylinder. Include the following in your sketch: wood pellet stove; hot water cylinder; pipework to and from the cylinder; expansion tank / vessel; pipework to radiators; all necessary pumps and valves.',
         [row('details', 'Any 8 x 5 marks', 40, 'Credit the best EIGHT acceptable items at 5 marks each, capped at 40. Marked items: draw the given sketch; 15 mm cold feed to stove; 22 mm flow to radiators; 22 mm return from radiators; radiators; cold feed to cylinder; 22 mm primary flow to cylinder; 22 mm primary return from cylinder; 22 mm expansion pipe; expansion tank/vessel; hot feed from cylinder; 22 mm overflow pipe; pump and valves.', list(range(0, 41, 5))),
          row('quality', 'Quality of sketch', 5, 'Quality of the sketch: excellent 5, good 3, fair 1.', BAND5)],
         ['cons-5-3', 'cons-5-2'], ['hot-water-space-heating'], 'q3-system', 'Heating system (5.3) and hot water cylinder (5.2).', B3, S3)
B3b = add('3', 'b', '(b)', 'Discuss one advantage of installing a zoned heating system so the radiators and hot water can be heated separately.',
          [row('advantage', 'Advantage', 5, 'One advantage. Such as: heating only the zone you need is more energy efficient and avoids unnecessary energy use; lower cost; more control over the heating; less wear when only the water is heated; a modern system may add value to the home.')],
          ['cons-5-3'], ['hot-water-space-heating'], 'q3-zoning', 'Temperature control and heat conservation (5.3).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-system', B3, S3, parts(A3, B3b))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p20 (printed 18): (a) select site 2 + two reasons × 6 = 14; (b) site outline 6, house position 6, entrance to the site 6, driveway to the house 6 = 24; (c) advantage 6 + disadvantage 6 = 12. Complete 50.'
S4 = 'Choosing site A or B is part of the answer and is itself marked ("Select site" 2), with the reasons and the sketch following the chosen site: one task, not two routes. All three printed items in (b) are required in one sketch.'
A4 = add('4', 'a', '(a)', 'Select your preferred site A or B, and give two reasons for your choice.',
         [row('select', 'Select site', 2, 'Select site A or site B.'),
          row('reason-1', 'Reason 1', 6, 'One reason for the chosen site. Such as, for site A: a south-facing façade for solar gain; direct access to the main road for services; close to existing houses; hedgerow shelter; a well-proportioned site.'),
          row('reason-2', 'Reason 2', 6, 'A second, different reason. Such as, for site B: safer access from a secondary road; off the main road for privacy, with less noise and air pollution; close to existing houses and services.')],
         ['cons-1-3'], ['planning-sustainability-environment'], 'q4-sites', 'Choosing a site (1.3).', B4, S4)
B4b = add('4', 'b', '(b)', 'Draw a large freehand sketch of your chosen site. On your sketch include your preferred: house position; entrance to the site; driveway to the house.',
          [row('site', 'Site outline', 6, 'A large freehand sketch outlining the chosen site.'),
           row('house', 'House position', 6, 'Such as: placed for a south-facing façade and solar gain, with room for front and rear gardens, existing trees as shelter, privacy, set back from the road.'),
           row('entrance', 'Entrance to the site', 6, 'Such as: off the secondary road for safe entry and exit, clear of existing trees, with a clear line of sight both ways and sidewalls splayed at 45°.'),
           row('driveway', 'Driveway to the house', 6, 'Such as: short to save materials and cost, gently curved to reduce visual impact, to the north of the house, allowing parking to the rear.')],
          ['cons-1-3'], ['planning-sustainability-environment'], 'q4-site-a', 'Site layout (1.3).', B4, S4)
C4 = add('4', 'c', '(c)', 'Give one advantage and one disadvantage of building a house in the countryside.',
         [row('advantage', 'Advantage', 6, 'Such as: quieter, cleaner air, nature and views, more space and privacy for the money, more affordable sites.'),
          row('disadvantage', 'Disadvantage', 6, 'Such as: amenities and services far away; car dependence and a larger carbon footprint; limited public transport; weaker internet or phone connections; isolation.')],
         ['cons-1-3'], ['planning-sustainability-environment'], None, 'Rural siting (1.3).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-site-a', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p21 (printed 19): (a) best 7 of 11 listed details × 5 = 35, three typical dimensions 3 × 1, draughting/accuracy/scale 8 (8/6/4) = sub-total 11, both printed within part (a): 46; (b) glue blocks 4. Complete 50.'
S5 = 'One required section and one required anti-creak detail. The best-seven detail list is a marking menu, not a printed choose-seven task.'
A5 = add('5', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the centre of the top three steps of the stairs and the landing. Show the steps, trimmer joist, and a portion of the landing. Show 600 mm length of the landing. Include three typical dimensions on your drawing.',
         [row('details', 'Any 7 x 5 marks', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: string 250 mm × 50 mm; tread 250 mm × 25 mm; riser 170 mm × 20 mm; joint between tread and riser; nosing (16 mm minimum); vertical and horizontal wedges; glue blocks 60 mm × 60 mm; pitch line/nosing line (maximum 42°); trimmer joist 225 mm × 75 mm; first floor joist 225 mm × 50 mm; tongue and groove floor.', list(range(0, 36, 5))),
          row('dimensions', 'Three typical dimensions', 3, 'Three typical dimensions, 1 mark each.'),
          row('presentation', 'Draughting, accuracy and scale', 8, 'Draughting, accuracy and scale of the section: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-4-4', 'cons-4-3', 'cons-10-1'], ['question-one-drawing-questions', 'foundations-floors-walls', 'wood-rot-ventilation'], 'q5-section',
         'Scaled drawing (1.5) of a stairs (4.4) at a timber landing floor (4.3), with its joints (10.1). The Ordinary reference taxonomy has no stairs or joinery heading; 4.4 and 10.1 are declared outside the crosswalk and the question keeps its existing Wood, Rot & Ventilation association.', B5, S5)
B5b = add('5', 'b', '(b)', 'On your drawing, show one design detail which will ensure that the stairs will not creak when in use.',
          [row('glue-blocks', 'Glue blocks', 4, 'Glue blocks in the angle between tread and riser, shown and identified. Any other suitable detail is accepted.', [0, 4])],
          ['cons-4-4', 'cons-10-1'], ['wood-rot-ventilation'], 'q5-glue-blocks',
          'Stair construction (4.4) and its glued joints (10.1). The Ordinary reference taxonomy has no stairs or joinery heading; both are declared outside the crosswalk.', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-section', B5, S5, parts(A5, B5b))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p22 (printed 20): (a) three PPE items, each sign 5 + specific reason 3 = 8; (a) 24. (b) two risks × 6 = 12; (c) notes 7 + sketch 7 = 14. Complete 50.'
S6 = 'Part (a) requires all three printed PPE items, each separately marked, so each is its own 8-mark task and (a) composes them; not a choice. Risks and the safety measure are open responses.'
PPE = [
    ('high-visibility-vest', 'high-visibility vest', 'High-visibility vest sign and specific reason (5+3 marks)',
     'Sign 5 and reason 3. Such as: workers are clearly visible on site, so vehicle operators see them and avoid accidents.'),
    ('safety-boots', 'safety boots', 'Safety boots sign and specific reason (5+3 marks)',
     'Sign 5 and reason 3. Such as: protects the feet from heavy materials or objects being dropped; the sole protects against sharp objects.'),
    ('ear-defenders', 'ear defenders', 'Ear defenders sign and specific reason (5+3 marks)',
     'Sign 5 and reason 3. Such as: protects workers’ hearing from the noise of machinery.'),
]
STEM6A = 'Using a large freehand sketch, show the safety sign for each of the following personal protective equipment (PPE) items: {items}. Give one specific reason why each item of personal protective equipment must be worn.'
a6 = [add('6', f'a-{slug}', f'(a) — {item}', STEM6A.format(items=item), [row('sign-reason', verbatim, 8, note)],
          ['cons-1-8'], ['site-safety'], 'q6-signs', 'Personal protective equipment and safety signs (1.8).', B6, S6)
      for slug, item, verbatim, note in PPE]
A6 = compose('6', 'a', '(a)', a6, 'q6-signs', B6, S6, STEM6A.format(items='; '.join(p[1] for p in PPE)), labels=[p[1] for p in PPE])
B6b = add('6', 'b', '(b)', 'Describe two potential risks to construction workers when working at height on a construction site.',
          [row('risk-1', 'Risk 1', 6, 'Such as: slipping and falling from scaffolding or a roof; a ladder or platform giving way.'),
           row('risk-2', 'Risk 2', 6, 'A second, different risk. Such as: power tools harder to use safely at height; tools or materials falling on workers below; rain or gusts of wind causing a fall.')],
          ['cons-1-8'], ['site-safety'], 'q6-risks', 'Safety precautions on site (1.8).', B6, S6)
C6 = add('6', 'c', '(c)', 'Using notes and freehand sketches, describe one safety measure that should be in place to ensure construction workers can safely access a roof when installing solar panels.',
         [row('notes', 'Notes', 7, 'Such as: safe, stable scaffolding and ladders for access; guardrails around the roof perimeter; a safety harness attached to secure anchor points; ladders at the correct angle extending enough to give a secure handhold onto the roof; an inspection of the roof structure by a qualified worker; non-slip boots.'),
          row('sketch', 'Sketch', 7, 'Freehand sketch of the chosen safety measure.')],
         ['cons-1-8'], ['site-safety'], 'q6-access', 'Safety precautions on site (1.8).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-signs', B6, S6, parts(A6, B6b, C6))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p23 (printed 21): (a) two advantages × 5 = 10; (b) sketch 8 (8/6/4) and four items, each location 3 + reason 2 = 5, = 28; (c) advantage 6 + disadvantage 6 = 12. Complete 50.'
S7 = 'All four printed items in (b) are required in one sketch, not a choice. Part (c) requires one advantage and one disadvantage, each separately marked: the two pre-audit single-item tasks are kept and (c) composes them.'
A7 = add('7', 'a', '(a)', 'Discuss two advantages of using timber frame for the construction of the garden office.',
         [row('advantage-1', 'Advantage 1', 5, 'Such as: quicker to construct than concrete block; can be prefabricated in a factory, with less time on site.'),
          row('advantage-2', 'Advantage 2', 5, 'A second, different advantage. Such as: a renewable material with a low embodied energy; less expensive than steel or concrete; its light weight needs smaller foundations; an attractive appearance.')],
         ['cons-3-3', 'cons-1-2'], ['foundations-floors-walls', 'planning-sustainability-environment'], None,
         'Timber-frame external walls (3.3) and sustainable building (1.2).', B7, S7)
B7b = add('7', 'b', '(b)', 'Draw a large freehand sketch of the given design and show your preferred location for each of the following in the garden office: corner desk; two windows; bookcase unit; seating area. Give one reason for selecting each location.',
          [row('sketch', 'Sketch', 8, 'Large freehand sketch of the given design: excellent 8, good 6, fair 4.', BAND8),
           row('corner-desk', 'Location and valid reason for corner desk (3 + 2 marks)', 5, 'Location 3 and reason 2. Such as: close to a window for a view and light, away from the door.'),
           row('two-windows', 'Location and valid reason for two windows (3 + 2 marks)', 5, 'Location 3 and reason 2. Such as: near the desk for a view while working; at the front to see people approach; on two walls for dual aspect.'),
           row('bookcase', 'Location and valid reason for bookcase unit (3 + 2 marks)', 5, 'Location 3 and reason 2. Such as: on the back wall, leaving space for the desk; near the seating area; away from the windows so it does not block light.'),
           row('seating', 'Location and valid reason for seating area (3 + 2 marks)', 5, 'Location 3 and reason 2. Such as: a separate zone away from the desk; near the door so as not to disturb the desk; leaving the brightest area for the desk.')],
          ['cons-1-2'], ['planning-sustainability-environment'], 'q7-office-plan', 'Layout design within the built environment (1.2).', B7, S7)
STEM7C = 'Discuss one {item} of constructing a garden office separate from the home.'
c7 = [add('7', f'c-{slug}', f'(c) — {slug}', STEM7C.format(item=slug),
          [row(slug, slug.capitalize(), 6, note)], ['cons-1-2'], ['planning-sustainability-environment'], None,
          'A separate building within the built environment (1.2).', B7, S7)
      for slug, note in [('advantage', 'Such as: a clear boundary between work and home life; fewer household interruptions; adds value to the home; frees space in the house.'),
                         ('disadvantage', 'Such as: the cost of building it and providing electricity and internet; it may need planning permission; it can be cold if not built to a high standard; a smaller garden; ongoing maintenance.')]]
C7 = compose('7', 'c', '(c)', c7, None, B7, S7, 'Discuss one advantage and one disadvantage of constructing a garden office separate from the home.',
             labels=['advantage', 'disadvantage'])
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-office-plan', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p24 (printed 22): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination.'
TERMS = [
    ('raft-foundation', 'raft foundation', 13, ['cons-2-4', 'cons-2-2'], ['foundations-floors-walls'],
     'Such as: a large, continuous reinforced concrete slab supporting the whole structure, "floating" like a raft; spreads the load over the whole footprint, reducing pressure on the soil; suits soils of low bearing capacity; needs more steel and concrete than a strip foundation.',
     'Raft foundations (2.4) and the choice of foundation (2.2).'),
    ('housing-joint', 'housing joint', 14, ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'],
     'Such as: a groove or slot cut across the width of one piece receives the end of another; a medium gluing area; used for shelves, cabinets and bookcases; a through housing runs fully across and shows at both ends, a stopped housing hides the joint at the front edge.',
     'Joints (10.1) and the choice of joint (10.4). The Ordinary reference taxonomy has no joinery heading; the term keeps the Wood, Rot & Ventilation association used for joinery, and 10.1/10.4 are declared outside that heading\'s crosswalk.'),
    ('rainwater-butt', 'rainwater butt', 15, ['cons-5-4'], ['drainage'],
     'Such as: a container that collects and stores rainwater from the roof via gutters and downpipes; reuses water for plants, lawns or washing the car; reduces reliance on treated tap water and lowers metered water use.',
     'Surface water, gutters and rainwater pipes (5.4).'),
    ('stud-wall', 'stud wall', 13, ['cons-4-5'], ['windows-doors'],
     'Such as: an internal wall framed with vertical timber or metal studs covered with plasterboard on both sides; lighter and faster to build than a block wall; load-bearing or non-load-bearing; houses electrical and plumbing services; poorer sound insulation and bearing capacity than a block wall.',
     'Stud partitions (4.5), which the crosswalk files under Windows & Doors.'),
    ('laser-level', 'laser level', 14, ['cons-10-7', 'cons-9-2'], ['wood-rot-ventilation'],
     'Such as: a tool projecting a laser beam to give a straight, level reference line, vertical and/or horizontal; a rotary laser projects a 360° beam for large or outdoor work; more accurate than a spirit level; can be mounted on tripods or clamps.',
     'Measuring for accuracy (10.7) with a tool (9.2). The Ordinary reference taxonomy has no tools heading; 9.2 is declared outside the crosswalk.'),
    ('damp-proof-course', 'damp-proof course', 15, ['cons-3-4'], ['foundations-floors-walls'],
     'Such as: a barrier stopping moisture rising through walls and floors by capillary action; polythene, bitumen felt, lead or copper, or slate; laid horizontally between courses, typically 150 mm above ground level, and around window and door openings; protects finishes and reduces mould and decay.',
     'Damp proof courses (3.4).'),
    ('door-threshold', 'door threshold', 13, ['cons-3-7'], ['windows-doors'],
     'Such as: the strip of wood, metal or plastic at the bottom of a doorway where the door closes; bridges two floor surfaces and seals the doorway; external thresholds keep out weather and draughts; internal ones cover changes in floor level; must meet building regulations so they are not a trip hazard.',
     'Door details (3.7).'),
    ('baluster', 'baluster', 14, ['cons-4-4'], ['wood-rot-ventilation'],
     'Such as: a short vertical post, often decorative, supporting the handrail of a stairs; a row of balusters is a balustrade; a safety element preventing falls, especially by children; also on balconies and terraces; wood, metal, glass or concrete.',
     'Stairs (4.4). The Ordinary reference taxonomy has no stairs heading; 4.4 is declared outside the crosswalk and the term keeps the Wood, Rot & Ventilation association the 2025 stairs question already carries.'),
    ('room-thermostat', 'room thermostat', 15, ['cons-5-3'], ['hot-water-space-heating'],
     'Such as: controls room temperature by switching the heating on below the set point and off above it; keeps rooms comfortable efficiently; manual dial or digital models; smart thermostats connect to Wi-Fi and a smartphone.',
     'Heating systems and temperature control (5.3).'),
]
TERM_HEADINGS = ['Raft foundation', 'Housing joint', 'Rainwater butt', 'Stud wall', 'Laser level', 'Damp-proof course',
                 'Door threshold', 'Baluster', 'Room thermostat']
Q8 = add('8', '', '', 'Explain, with the aid of notes and freehand sketches, any five of the following: ' + '; '.join(t[1] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Construction Terms', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{h}: ' + t[5].removeprefix('Such as: ') for h, t in zip(TERM_HEADINGS, TERMS)),
               group=dict(claimMax=5, perOption=10, options=TERM_HEADINGS))],
         list(dict.fromkeys(n for t in TERMS for n in t[3])), list(dict.fromkeys(a for t in TERMS for a in t[4])), None,
         'The union of the nine printed terms: ' + ' '.join(t[6] for t in TERMS), B8, S8, scheme_pages=[13, 14, 15, 24])

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p25 (printed 23): (a) two reasons × 6 = 12; (b) two modifications, each sketch 8 + notes 5 = 13, = 26; (c) two uses × 6 = 12. Complete 50.'
S9 = 'Both printed purposes in (b) are served by the two modifications the scheme marks as Modification 1 and 2; reasons, modifications and uses are open responses.'
A9 = add('9', 'a', '(a)', 'Discuss two reasons why the homeowners wish to create an outdoor dining/living space.',
         [row('reason-1', 'Reason 1', 6, 'Such as: extra usable living space without much cost; a space for entertaining, dining and relaxing in good weather, BBQs and parties.'),
          row('reason-2', 'Reason 2', 6, 'A second, different reason. Such as: adds value to the home; being outdoors reduces stress and supports mental health; easier to enjoy fresh air and greenery.')],
         ['cons-1-2'], ['planning-sustainability-environment'], None, 'Design of the built environment for wellbeing (1.2).', B9, S9)
B9b = add('9', 'b', '(b)', 'Using notes and freehand sketches, show two possible modifications that could be made at the rear of the house that would allow for the following: access to the garden from the house; an outdoor dining/living space.',
          [row('modification-1', 'Modification 1 sketch + notes (8 + 5 marks )', 13, 'Sketch 8 and notes 5. Such as: replace windows with a large glazed, sliding or bifold door for access to the garden.'),
           row('modification-2', 'Modification 2 sketch + notes (8 + 5 marks )', 13, 'Sketch 8 and notes 5 for a second, different modification. Such as: a patio along the back wall; part of the lawn changed to decking or slabs; a BBQ area.')],
          ['cons-3-7', 'cons-1-2'], ['windows-doors', 'planning-sustainability-environment'], 'q9-modifications',
          'External doors (3.7) and the outdoor built environment (1.2).', B9, S9)
C9 = add('9', 'c', '(c)', 'Discuss two other possible family uses of a large garden.',
         [row('use-1', 'Suggested use 1', 6, 'Such as: a safe play area for children, with slides or trampolines; growing plants and flowers.'),
          row('use-2', 'Suggested use 2', 6, 'A second, different use. Such as: growing vegetables and herbs; bird feeders to bring nature closer; a shed or extra storage; space for a family pet.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q9-uses', 'Use of the outdoor built environment (1.2).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-modifications', B9, S9, parts(A9, B9b, C9))

# ---------------------------------------------------------------- ledgers
pattern = r'\b(?:choose|select|one\s+of|any\s+\w+|either|or|answer\s+\w+)\b'
observed = []
with fitz.open(R / P) as pdf:
    for i, p in enumerate(pdf):
        text = ' '.join(p.get_text().split())
        observed.extend((i + 1, m.start(), m.group(), text[max(0, m.start() - 80):m.end() + 80]) for m in re.finditer(pattern, text, re.I))
classes = ['Whole-exam selection: any four of the nine questions; all question banks retained, no full-exam Cartesian cards.',
           'Q4(a) answer-content choice: selecting site A or B is itself marked (Select site 2) and the reasons and (b) sketch follow it; one task, not two routes.',
           'Q4(a) "A or B" (same answer-content choice as the preceding Select).',
           'Q8 closed choose-five of nine printed terms: one card with an any-five group over all nine terms (choice is not a route).']
assert [(o[0], o[2]) for o in observed] == [(1, 'Answer any'), (3, 'Select'), (3, 'or'), (4, 'any five')], observed
selection_ledger = dict(pattern=pattern, unclassified=0, sourceHashes=HASHES,
                        rows=[dict(page=o[0], start=o[1], match=o[2], context=o[3], classification=c) for o, c in zip(observed, classes)],
                        finiteQuestionChoices={'8': dict(choose=5, options=[t[0] for t in TERMS], cardId=Q8['id'], groupRowId='terms',
                                                         wholeQuestionMarks=50, termMarks=10)})
whole = {}
for t in tasks:
    c = t['card']
    if '-complete' in c['id'] or c['id'] == PREFIX + 'q8':
        whole.setdefault(t['questionNumber'], []).append(dict(id=c['id'], parts=[g['label'] for g in c.get('taskGroups', [])] or ['any five of nine terms'], marks=c['totalMarks']))
taxonomy_gaps = [
    dict(cardId=PREFIX + 'q5-a', canonicalTopicIds=['cons-4-4', 'cons-10-1'], atlasTopicId=CROSS + 'wood-rot-ventilation',
         reason='No Ordinary outgoing reference heading covers stairs (4.4) or joinery (10.1).'),
    dict(cardId=PREFIX + 'q5-b', canonicalTopicIds=['cons-4-4', 'cons-10-1'], atlasTopicId=CROSS + 'wood-rot-ventilation',
         reason='No Ordinary outgoing reference heading covers stairs (4.4) or joinery (10.1).'),
    dict(cardId=PREFIX + 'q8', canonicalTopicIds=['cons-10-1', 'cons-10-4', 'cons-9-2', 'cons-4-4'], atlasTopicId=CROSS + 'wood-rot-ventilation',
         reason='No Ordinary outgoing reference heading covers joinery (10.1, 10.4, housing joint), tools (9.2, laser level) or stairs (4.4, baluster).'),
]
REASONS = {
    'q1-a': 'Adds the three typical dimensions (3) and draughting/accuracy/scale (8/6/4) printed within part (a): 35 → 46.',
    'q1-b': 'Reshaped to the printed all-or-nothing row "Stepped DPC clearly identified" (0 or 4); tariff unchanged.',
    'q2-a': 'Split into the two printed advantages (6 each); total unchanged (12).',
    'q2-b': 'Adds the printed insulation type (4) and thickness (4) rows: 16 → 24.',
    'q2-c': 'Split into the printed note 7 and sketch 7; total unchanged (14).',
    'q3-a': 'Adds the printed quality-of-sketch allowance (5/3/1): 40 → 45; best eight items at 5 each.',
    'q3-b': 'Reshaped to the printed single advantage row; tariff unchanged (5).',
    'q4-a': 'Adds the printed "Select site" mark (2): 12 → 14.',
    'q4-b': 'Rows named by the scheme (site outline, house position, entrance, driveway); total unchanged (24).',
    'q4-c': 'Rows named by the scheme (advantage, disadvantage); total unchanged (12).',
    'q5-a': 'Adds the three typical dimensions (3) and draughting/accuracy/scale (8/6/4) printed within part (a): 35 → 46.',
    'q5-b': 'Reshaped to the printed all-or-nothing glue-blocks row (0 or 4); tariff unchanged.',
    'q6-a': 'Now the whole of part (a), built from its three separately marked PPE items (sign 5 + reason 3 each); total unchanged (24).',
    'q6-b': 'Split into the two printed risks (6 each); total unchanged (12).',
    'q6-c': 'Split into the printed notes 7 and sketch 7; total unchanged (14).',
    'q7-a': 'Split into the two printed advantages (5 each); total unchanged (10).',
    'q7-b': 'Adds the printed sketch band (8/6/4) and the four location-and-reason rows (3 + 2 each): 20 → 28.',
    'q7-c-advantage': 'Reshaped to the printed advantage row; tariff unchanged (6). Its build-time override is retired.',
    'q7-c-disadvantage': 'Reshaped to the printed disadvantage row; tariff unchanged (6).',
    'q9-b': 'Split into the two printed modifications (sketch 8 + notes 5 each); total unchanged (26).',
    'q9-c': 'Split into the two printed suggested uses (6 each); total unchanged (12).',
}
assert set(REASONS) == {k.removeprefix(PREFIX) for k in LEGACY}
corrections = []
for t in tasks:
    c = t['card']
    if c['id'] in LEGACY:
        old = LEGACY[c['id']]
        corrections.append(dict(cardId=c['id'], priorSha256=card_hash(old), correctedSha256=card_hash(c),
                                priorTotalMarks=old['totalMarks'], correctedTotalMarks=c['totalMarks'],
                                priorTopicId=old['topicId'], correctedTopicId=c['topicId'],
                                reason=REASONS[c['id'].removeprefix(PREFIX)]))
assert len(corrections) == 21
out = dict(schemaVersion=1, subjectId='construction-studies', year=2025, level='ordinary', lang='ev', sitting='main', paperKey='single',
           fileid='LC029GLP000EV.pdf', component='theory', status='Q1–Q9 source-reviewed draft; integration pending.',
           sourceHashes=HASHES, tasks=tasks, bindings=bindings, questionFigures=question_figures,
           addedIds=[t['card']['id'] for t in tasks if not t['correction']], corrections=corrections,
           selectionLedger=selection_ledger, questionRouteLedgers={q: dict(wholeRoutes=w) for q, w in whole.items()},
           taxonomyGaps=taxonomy_gaps, questionsReviewed=list(QUESTIONS), unreviewedQuestions=[])
(HERE / 'ordinary-2025-draft.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(tasks=len(tasks), added=len(out['addedIds']), corrected=len(corrections), figures=len(question_figures),
                      perQuestion={q: sum(1 for t in tasks if t['questionNumber'] == q) for q in QUESTIONS})))
