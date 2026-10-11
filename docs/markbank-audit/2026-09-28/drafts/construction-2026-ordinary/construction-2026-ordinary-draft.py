"""Draft the 2026 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Question wording and stems are lifted from the SEC paper (a narrowed task only deletes
printed words); every row's verbatim is printed in the scheme's mark tables (pages
18-26), checked against rendered pages. Unbanded components accept any whole mark
up to the published maximum; printed excellent/good/fair bands are kept as printed.
Sources are the byte-identical paper-trail-corpus copies, pinned by SHA-256. Figures
are exact 2x crops. Writes ordinary-2026-draft.json and the PNGs beside this file.
"""
import copy
import hashlib
import itertools
import json
import re
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
R = HERE.parents[4]
P = 'paper-trail-corpus/exampapers/2026/LC029GLP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2026/LC029GLP000EV.pdf'
HASHES = {P: '3c68a9431babde5a5ba814a72fdd790ffbe44fbc3e00444dc37867e20a3003c6',
          S: '4d5b0f5d024e248e2d1398ceb6641d3800f1c880bf01a1327977d648637a0011'}
ATTRIBUTION = 'SEC Leaving Certificate Construction Studies 2026 Ordinary Level — © State Examinations Commission.'
FP = 'construction-studies-2026-OL-'
PREFIX = 'cons-2026-ol-'
CROSS = 'construction-studies-ordinary-'
BAND8 = [0, 4, 6, 8]
PAGE = [48, 52, 568, 790]

for f, h in HASHES.items():
    assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f

FIGURES = {
    'q1-original': (P, 2, [45, 38, 580, 282], False), 'q2-original': (P, 2, [45, 282, 580, 524], False),
    'q3-original': (P, 2, [45, 524, 580, 784], False), 'q4-original': (P, 3, [45, 36, 580, 310], False),
    'q5-original': (P, 3, [45, 310, 580, 552], False), 'q6-original': (P, 3, [45, 552, 580, 785], False),
    'q7-original': (P, 4, [45, 38, 580, 346], False), 'q8-original': (P, 4, [45, 346, 580, 480], False),
    'q9-original': (P, 4, [45, 480, 580, 785], False),
    'q1-section': (S, 4, [50, 138, 545, 492], True), 'q1-scheme': (S, 4, PAGE, True),
    'q2-scheme': (S, 5, PAGE, True), 'q2-upgrade': (S, 5, [436, 616, 574, 766], True),
    'q3-system': (S, 6, [50, 125, 575, 524], True), 'q3-water-butt': (S, 6, [450, 562, 548, 764], True),
    'q4-site-plan': (S, 7, [84, 398, 545, 752], True), 'q4-site-notice': (S, 8, [410, 540, 568, 786], True),
    'q5-section': (S, 9, [50, 102, 572, 578], True), 'q5-wall-tie': (S, 9, [96, 660, 470, 748], True),
    'q6-precautions': (S, 10, [86, 128, 545, 414], True), 'q6-pillar-drill': (S, 10, [345, 530, 545, 752], True),
    'q7-garden-plan': (S, 12, [145, 347, 486, 790], True),
    'q8-triple-glazing': (S, 14, [383, 98, 538, 267], True), 'q8-wind-turbine': (S, 14, [419, 285, 543, 490], True),
    'q8-carbon-monoxide-alarm': (S, 15, [314, 564, 543, 724], True),
    'q8-mortise-and-tenon-joint': (S, 15, [371, 85, 562, 291], True), 'q8-butt-hinge': (S, 14, [336, 523, 537, 689], True),
    'q8-ball-valve': (S, 16, [346, 322, 559, 518], True), 'q8-cordless-circular-saw': (S, 15, [334, 350, 556, 528], True),
    'q8-fascia-board': (S, 16, [414, 87, 542, 290], True), 'q8-smart-meter': (S, 16, [392, 549, 543, 779], True),
    'q9-extension': (S, 17, [213, 288, 577, 532], True), 'q9-cladding': (S, 17, [433, 557, 546, 780], True),
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
    '1': dict(page=2, title='Strip foundation, external wall and ground floor', concept='foundation-wall-floor-section',
              stem='The sketch shows an external wall and traditional strip foundation of a dwelling house. The wall is a 400 mm concrete block wall with a full-fill insulated cavity. The wall is plastered on both sides. The insulated concrete ground floor is finished with a 20 mm tongue and groove floating timber floor as shown.',
              note='Original sketch and specification retained. Construction details, dimensions and draughting belong to part (a); the damp-prevention detail in (b) is marked separately. Any alternative detailing that complies with current Building Regulations is acceptable.'),
    '2': dict(page=2, title='Upgrading the thermal performance of external walls', concept='wall-thermal-upgrade',
              stem='The sketch shows a dwelling house that was built in the 1970’s. The external walls of the house are of concrete block construction with a 100 mm uninsulated cavity. The homeowners wish to install insulation to improve the thermal performance of the external walls.',
              note='Original sketch retained. The insulation method and the other upgrade area are open choices; the scheme lists typical examples.'),
    '3': dict(page=2, title='Cold water supply to a two-storey house', concept='cold-water-supply', stem='',
              note='The listed components are required content, not a choice. The scheme diagram is one acceptable layout; any alternative that complies with current Building Regulations is acceptable.'),
    '4': dict(page=3, title='Planning a rural site', concept='site-planning',
              stem='The sketch shows a portion of a site location map. Site A is located on the outskirts of a rural town. The owners wish to build a new dwelling house on the site.',
              note='Original site map retained. Positions and reasons are open, well-reasoned responses; the scheme sketch is one acceptable layout.'),
    '5': dict(page=3, title='Section through an external door and lintel', concept='door-lintel-section',
              stem='The sketch shows the external wooden door of a dwelling house. The external wall is a 400 mm concrete block wall with a full-fill insulated cavity which is plastered on both sides. A thermally broken doorframe 130 mm × 75 mm is fixed in the wall. The door is 90 mm in thickness with 15 mm timber sheeting on both sides and is highly insulated.',
              note='Original sketch and specification retained. Construction details, dimensions and draughting belong to part (a); the wall tie in (b) is marked separately.'),
    '6': dict(page=3, title='Safety in the Construction Studies room', concept='workshop-safety', stem='',
              note='Both printed situations in (a) are required. The scheme precautions are examples; any other suitable specific precaution is acceptable.'),
    '7': dict(page=4, title='Designing a south-facing rear garden', concept='rear-garden-design',
              stem='The drawing shows the plan of a south facing rear garden. The homeowners wish to redesign the garden to make better use of the space and contribute to their wellbeing.',
              note='Original garden plan retained. All four printed features are required in one sketch; locations and reasons are open, well-reasoned responses.'),
    '8': dict(page=4, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=4, title='Extension to a traditional farmhouse', concept='farmhouse-extension',
              stem='The sketch shows a traditional Irish farmhouse with a proposed single storey extension to the side. The extension is to be finished externally with timber cladding.',
              note='Original sketch retained. Reasons, modifications and the timber species are open responses; the scheme lists typical examples.'),
}
SCHEME_PAGES = {'1': [4, 18], '2': [5, 19], '3': [6, 20], '4': [7, 8, 21], '5': [9, 22], '6': [10, 11, 23],
                '7': [12, 13, 24], '9': [17, 26]}

tasks, bindings, cards = [], [], {}


def add(q, key, ref, text, rows, nodes, topics, figure, review, boundary, selection, scheme_pages=None, groups=None):
    meta = QUESTIONS[q]
    card = dict(id=f'{PREFIX}q{q}-{key}', subjectId='construction-studies', year=2026, level='ordinary', section='B',
                topicId=nodes[0], conceptId=f"{meta['concept']}-{key}", questionRef=f'2026 OL Q{q}{ref}',
                stem=meta['stem'], questionText=text, tariffModel={'kind': 'fixed'},
                totalMarks=sum(r['marks'] for r in rows), rows=rows,
                questionFigureKey=f'{FP}q{q}-original', questionFigureIncludesPrompt=True)
    if figure:
        card['figureKey'] = FP + figure
    card['sourceMaterial'] = dict(kind='source-illustration', label=f'ORIGINAL QUESTION {q}', title=meta['title'],
                                  pages=[1, meta['page']], attribution=ATTRIBUTION, presentationNote=meta['note'])
    if groups:
        card['taskGroups'] = groups
    tasks.append(dict(questionNumber=q, card=card, sourceChecks=checks(meta['page'], scheme_pages or SCHEME_PAGES[q]),
                      boundaryReview=boundary, selectionReview=selection,
                      requiredQuestionFigures=[f'{FP}q{q}-original'], requiredSolutionFigures=[FP + figure] if figure else []))
    bindings.append(dict(cardId=card['id'], markBankTopicId=nodes[0], canonicalTopicIds=nodes, canonicalTopicReview=review,
                         questionNumber=q, atlasTopicIds=[CROSS + t for t in topics]))
    cards[card['id']] = card
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
B1 = 'Scheme p18: (a) best 7 of 12 listed details × 5 = 35, any 3 typical dimensions 3, draughting/accuracy/scale 8 (8/6/4) = sub-total 46 printed within part (a); (b) radon barrier clearly identified 4. Complete 50.'
S1 = 'One required section and one required damp-prevention detail. The best-seven detail list is a marking menu, not a printed choose-seven task.'
A1 = add('1', 'a', '(a)',
         'To a scale of 1:5, draw a vertical section through the foundation, external wall, and ground floor. On your drawing, show the typical construction details from the bottom of the foundation to a level 300 mm above the finished floor. Show 1.0 m width of floor. Include three typical dimensions on your drawing.',
         [row('details', 'Any 7 x 5 marks', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: reinforced concrete foundation; hardcore (maximum 225 mm layers); sand blinding; radon barrier; concrete subfloor; 200–300 mm rigid floor insulation; screed; 20 mm T&G flooring; outer leaf with external render; concrete fill; full-fill insulated cavity; inner leaf with internal plaster; airtightness tape. The model also shows a DPC, 100 mm leaves and 15 mm internal plaster.', list(range(0, 36, 5))),
          row('dimensions', 'Any 3 typical dimensions', 3, 'Three appropriate typical dimensions on the section.'),
          row('presentation', 'Draughting, accuracy, and scale', 8, 'Draughting, accuracy and scale of the section: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-2-4', 'cons-3-3', 'cons-4-2', 'cons-3-4', 'cons-6-2'],
         ['question-one-drawing-questions', 'foundations-floors-walls', 'heat-loss-insulation'], 'q1-scheme',
         'Scaled drawing (1.5) of a strip foundation (2.4), cavity external wall (3.3), insulated solid ground floor (4.2), membranes and DPC (3.4) and insulation (6.2).', B1, S1)
B1b = add('1', 'b', '(b)', 'On your drawing, show the typical design detailing that prevents dampness entering the building through the floor.',
          [row('damp-prevention', 'Radon barrier clearly identified', 4, 'Identify the radon barrier (or damp proof membrane) laid continuously under the floor and linked to the DPC, so ground moisture cannot rise through the floor.', [0, 4])],
          ['cons-3-4', 'cons-4-2'], ['foundations-floors-walls'], 'q1-section', 'Damp-proof membrane / radon barrier (3.4) in the solid ground floor (4.2).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-scheme', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p19: (a) two advantages × 6 = 12; (b) method note & sketch 8 + 8 = 16, insulation type 4, thickness 4 = 24; (c) area 2 and two reasons × 6 = 14. Complete 50.'
S2 = '"one suitable method" and "one other area" are open choices with no printed list; each part stays one response.'
A2 = add('2', 'a', '(a)', 'Give two advantages of improving the thermal performance of the external walls.',
         [row('advantage-1', 'Advantage 1', 6, 'Such as: reduced heat loss, so the house is more energy efficient; lower energy bills.'),
          row('advantage-2', 'Advantage 2', 6, 'A second, different advantage. Such as: a smaller carbon footprint; more comfortable rooms; walls are the largest surface for heat loss; the work can cause minimal disruption.')],
         ['cons-6-2', 'cons-6-3'], ['heat-loss-insulation'], None, 'Benefits of insulation (6.2) through reduced heat loss and running costs (6.3).', B2, S2)
B2b = add('2', 'b', '(b)', 'Using notes and freehand sketches, show one suitable method of insulating the external walls. Show on your sketch, how the wall is finished after installing the insulation. Specify the type and thickness of insulation.',
          [row('method', 'Method of insulating the walls', 16, 'Notes 8 and sketch 8, including how the wall is finished. Such as cavity fill: drill 22–25 mm holes through the outer leaf about 1 m apart in a grid, blow bonded bead with adhesive into the cavity until full, then fill and decorate the holes. Alternatives: an external insulation system, or internal insulated plasterboard, fixed with adhesive and mechanical anchors.'),
           row('type', 'Preferred insulation type for external wall', 4, 'A suitable type, such as expanded polystyrene (EPS), phenolic, polyisocyanurate (PIR) or extruded polystyrene (XPS).'),
           row('thickness', 'Thickness of insulation', 4, 'A suitable thickness: the scheme gives 100–200 mm as a minimum range.')],
          ['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q2-scheme',
          'Insulating material and method (6.2) applied to the existing external wall (3.3).', B2, S2)
C2 = add('2', 'c', '(c)', 'Identify one other area of a house that could be upgraded to improve its overall thermal performance. Give two reasons for your choice.',
         [row('area', 'Area', 2, 'One other area, such as high-performance windows and doors, roof-space insulation, ground-floor insulation, airtightness at key junctions, or heat recovery ventilation replacing wall vents.'),
          row('reason-1', 'Reason 1', 6, 'A reason for the choice, such as cost efficiency or a large reduction in heat loss.'),
          row('reason-2', 'Reason 2', 6, 'A second, different reason, such as a quick job with minimal disruption, or savings on heating.')],
         ['cons-6-2', 'cons-6-3'], ['heat-loss-insulation'], 'q2-upgrade', 'Thermal upgrading of the envelope (6.2) and its running-cost benefit (6.3).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-scheme', B2, S2, parts(A2, B2b, C2))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p20: (a) best 8 of 11 listed details × 5 = 40; (b) two uses × 5 = 10. Complete 50.'
S3 = 'The five bulleted diagram contents are required, not a choice; the best-eight list is a marking menu. Uses in (b) are open.'
A3 = add('3', 'a', '(a)', 'Draw a large freehand sketch of the given house, and on your sketch show the pipework necessary to supply cold water to the kitchen sink on the ground floor, wash basin, toilet cistern, and bath on the first floor. Include the following in your sketch: rising main; insulated cold water storage tank; pipework to kitchen sink; pipework to bathroom fixtures; all necessary valves.',
         [row('details', 'Any 8 x 5 marks', 40, 'Credit the best EIGHT correct details at 5 marks each, capped at 40. Marked details: 15 mm rising main; 15 mm cold water feed to the kitchen sink (from the rising main); kitchen sink; insulated water storage tank; ball valve in the tank; overflow pipe (about Ø28 mm); bathroom fixtures; cold feeds to the wash basin and toilet cistern (Ø15 mm) and to the bath; valves (stop valves and drain valve).', list(range(0, 41, 5)))],
         ['cons-5-2', 'cons-5-1'], ['services-water-gas-electrical'], 'q3-system',
         'Cold water supply with storage cistern (5.2) and protection of the installation (5.1).', B3, S3)
B3b = add('3', 'b', '(b)', 'A rainwater butt is used to collect rainwater from the roof. Give two possible uses for the collected rainwater.',
          [row('use-1', 'Use 1', 5, 'Such as: watering gardens, lawns or plants; washing cars or bicycles.'),
           row('use-2', 'Use 2', 5, 'A second, different use, such as: cleaning outdoor equipment, patios or driveways; flushing toilets if correctly plumbed; an emergency non-drinking supply.')],
          ['cons-5-4'], ['drainage'], 'q3-water-butt', 'Rainwater collected from roof drainage (5.4).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-system', B3, S3, parts(A3, B3b))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p21: (a) two reasons × 5 = 10; (b) site outline, house position, entrance, driveway and garage position × 6 = 30 on one sketch; (c) two items × 5 = 10. Complete 50.'
S4 = 'Part (b) is one integrated site sketch: the four printed positions are all required, so it stays one task with a row each. Reasons and items in (a)/(c) are open.'
A4 = add('4', 'a', '(a)', 'Discuss two reasons why it is necessary to apply for planning permission to build a new dwelling house.',
         [row('reason-1', 'Reason 1', 5, 'Such as: planning permission is a legal requirement for all new dwellings in Ireland; it ensures the house complies with planning law and the local development plan.'),
          row('reason-2', 'Reason 2', 5, 'A second, different reason, such as: safe road access; no negative impact on the environment or neighbours; suitable wastewater treatment and drainage; safe, sustainable building.')],
         ['cons-1-3'], ['planning-sustainability-environment'], None, 'Planning permission (1.3).', B4, S4)
B4b = add('4', 'b', '(b)', 'Draw a large freehand sketch of the given site A. On your sketch, include your preferred: house position; entrance to the site; driveway to the house; garage position.',
          [row('site', 'Site outline', 6, 'Sketch the outline of site A with its boundaries and the road.'),
           row('house', 'House position', 6, 'Such as: positioned for a south-facing façade and maximum solar gain, leaving front and rear gardens, using the hedgerows for shelter.'),
           row('entrance', 'Entrance to the site', 6, 'Such as: easy access to the road, splayed for clear sight lines, to one side to reduce visual impact, in keeping with neighbouring entrances.'),
           row('driveway', 'Driveway to the house', 6, 'Such as: a simple layout to one side, giving access to the garage and parking at the side and back.'),
           row('garage', 'Garage position', 6, 'Such as: in a corner or at the rear to minimise impact on the garden and views, away from the house if used as a workshop, accessible by car.')],
          ['cons-1-3'], ['planning-sustainability-environment'], 'q4-site-plan', 'Site layout for a new dwelling (1.3).', B4, S4)
C4 = add('4', 'c', '(c)', 'Identify two items which must be submitted as part of a planning application when applying for permission to build a dwelling house.',
         [row('item-1', 'Item 1', 5, 'Such as: the completed, signed application form; the application fee; the newspaper notice page; a copy of the site notice.'),
          row('item-2', 'Item 2', 5, 'A second, different item, such as: six copies of the site location map, site layout plans or architectural drawings; environmental reports where required; ownership details or landowner consent.')],
         ['cons-1-3'], ['planning-sustainability-environment'], 'q4-site-notice', 'Planning application requirements (1.3).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-site-plan', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p22: (a) best 7 of 11 listed details × 5 = 35, three typical dimensions 3 × 1, draughting/accuracy/scale 8 (8/6/4) = sub-total 46 printed within part (a); (b) wall tie 4. Complete 50.'
S5 = 'One required section and one required cavity-tie detail. The best-seven detail list is a marking menu, not a printed choice.'
A5 = add('5', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the external wall, concrete lintels, doorframe, and door. On your drawing show the typical construction details from 400 mm below to 400 mm above the lintels. Include three typical dimensions on your drawing.',
         [row('details', 'Any 7 x 5 marks', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: external render (19 mm); concrete block outer leaf (100 mm); full-fill insulated cavity (200 mm) with wall tie; concrete block inner leaf (100 mm); internal plaster (15 mm); cavity closer; stepped DPC; concrete lintels (100 mm × 75 mm); thermally broken door frame; insulated door; airtightness (tape).', list(range(0, 36, 5))),
          row('dimensions', 'Three typical dimensions', 3, 'Three appropriate typical dimensions, 1 mark each.'),
          row('presentation', 'Draughting, accuracy, and scale', 8, 'Draughting, accuracy and scale of the section: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-3-7', 'cons-3-3', 'cons-3-4', 'cons-6-2'], ['windows-doors', 'foundations-floors-walls', 'heat-loss-insulation'], 'q5-section',
         'External door and frame (3.7) in a cavity wall (3.3) with lintels and stepped DPC (3.4) and insulation (6.2).', B5, S5)
B5b = add('5', 'b', '(b)', 'On your drawing, show the typical design detailing to link the inner and outer leaves of the cavity wall.',
          [row('wall-tie', 'Wall tie.', 4, 'Show a wall tie bridging the cavity, built into both leaves. Any other suitable detail is accepted.', [0, 4])],
          ['cons-3-3'], ['foundations-floors-walls'], 'q5-wall-tie', 'Cavity wall ties (3.3).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-section', B5, S5, parts(A5, B5b))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p23: (a) two precautions × 4 for EACH of scroll saw and spray finish = 16; (b) three precautions with reasons × 8 = 24; (c) two reasons × 5 = 10. Complete 50.'
S6 = 'Part (a) asks for two precautions in EACH printed situation: both are required, separately marked tasks, not a choice. Precautions and reasons are open.'
SAFE = ['cons-9-4']
SITUATIONS = [('scroll-saw', 'using a scroll saw', 'Using a scroll saw',
               'Such as: wear safety glasses or goggles; ensure the blade is installed correctly and tightened; remove jewellery and loose clothing and tie back long hair; use ear protection; keep fingers a safe distance from the blade; know where the emergency stop is.'),
              ('spray-finish', 'applying a spray finish to an artefact', 'Applying a spray finish',
               'Such as: a well-ventilated work zone; a respirator mask against vapours; exhaust fans or a spray booth; long sleeves or protective clothing; goggles or a face shield; never spray near open flames.')]
a6 = []
for slug, item, label, examples in SITUATIONS:
    a6.append(add('6', f'a-{slug}', f'(a) — {item}',
                  f'State two specific safety precautions to be observed in the Construction Studies classroom in each of the following situations: {item}.',
                  [row('precaution-1', f'{label} – Safety precaution 1', 4, f'One specific precaution when {item}. ' + examples),
                   row('precaution-2', f'{label} – Safety precaution 2', 4, f'A second, different specific precaution when {item}.')],
                  SAFE, ['site-safety'], 'q6-precautions', 'Safe use of tools and equipment in the Construction Studies room (9.4).', B6, S6))
A6 = compose('6', 'a', '(a)', a6, 'q6-precautions', B6, S6,
             'State two specific safety precautions to be observed in the Construction Studies classroom in each of the following situations: using a scroll saw; applying a spray finish to an artefact.',
             labels=[s[1] for s in SITUATIONS])
B6b = add('6', 'b', '(b)', 'Using notes and freehand sketches, describe three specific safety precautions that should be observed when using a pillar drill. Give one reason for each safety precaution outlined.',
          [row(f'precaution-{i}', f'Safety precaution {i} and reason', 8, note) for i, note in [
              (1, 'A precaution and its reason, with notes and sketches. Such as: wear safety glasses to protect the eyes from chips; tie back long hair and remove loose clothing and jewellery so nothing is caught.'),
              (2, 'A second, different precaution and reason. Such as: close the safety guard before use; use the correct drill bit and speed for the material.'),
              (3, 'A third, different precaution and reason. Such as: keep hands clear of rotating parts; clamp the work piece securely; know where the emergency stop button is.')]],
          SAFE, ['site-safety'], 'q6-pillar-drill', 'Safe use of a pillar drill (9.4).', B6, S6)
C6 = add('6', 'c', '(c)', 'Discuss two reasons why it is essential that students receive safety training before using tools and machinery in the Construction Studies room.',
         [row('reason-1', 'Reason 1', 5, 'Such as: it reduces the risk of accidents and injuries from incorrect use of tools; it teaches safe procedures.'),
          row('reason-2', 'Reason 2', 5, 'A second, different reason, such as: correct use of PPE; confidence and competence; recognising hazards; preventing damage to tools and equipment.')],
         SAFE, ['site-safety'], None, 'Safety training for tools and machinery (9.4).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-precautions', B6, S6, parts(A6, B6b, C6))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p24: (a) two ways × 5 = 10; (b) sketch 8 plus location and reason (3 + 2) for each of four features = 28; (c) two benefits × 6 = 12. Complete 50.'
S7 = 'Part (b) is one sketch locating all four printed features, each with its own location-and-reason mark: required content, not a choice, kept as one task. Ways and benefits are open.'
A7 = add('7', 'a', '(a)', 'Discuss two ways in which a garden can contribute to a family’s wellbeing.',
         [row('way-1', 'Example 1', 5, 'Such as: a space to relax and relieve stress; physical activity through play, exercise or gardening.'),
          row('way-2', 'Example 2', 5, 'A second, different way, such as: space for children to play and adults to socialise; growing vegetables and herbs for healthier eating; family bonding; outdoor cooking and eating.')],
         ['cons-1-2'], ['planning-sustainability-environment'], None, 'Design of the external environment of a dwelling (1.2).', B7, S7)
B7b = add('7', 'b', '(b)', 'Draw a large freehand sketch of the given design and show your preferred location for each of the following in the garden space: outdoor living space; cooking area; children’s play area; flowerbed and trees. Give one reason for selecting each location.',
          [row('sketch', 'Sketch', 8, 'A large freehand sketch of the given garden design.'),
           row('outdoor-living', 'Location and valid reason for outdoor living space', 5, 'Location 3 and reason 2. Such as: close to the house for indoor–outdoor living, on the sunny side, near the cooking area with a view of the garden.'),
           row('cooking', 'Location and valid reason for cooking area', 5, 'Location 3 and reason 2. Such as: beside the outdoor living space for serving, close to the house, along a wall that gives shelter and a route for services.'),
           row('play', 'Location and valid reason for children’s play area', 5, 'Location 3 and reason 2. Such as: in a clear open area, in view of the house for safety, to one side so it does not block the garden view.'),
           row('planting', 'Location and valid reason for flowerbed and trees', 5, 'Location 3 and reason 2. Such as: in sight of the house, where it catches sunlight, along the boundary for privacy.')],
          ['cons-1-2'], ['planning-sustainability-environment'], 'q7-garden-plan', 'Layout of the external environment of a dwelling (1.2).', B7, S7)
C7 = add('7', 'c', '(c)', 'Discuss two benefits of having a south facing garden.',
         [row('benefit-1', 'Benefit 1', 6, 'Such as: sunlight all day for outdoor living; a warmer, brighter, more comfortable garden.'),
          row('benefit-2', 'Benefit 2', 6, 'A second, different benefit, such as: more use by the family; healthy growth of plants and vegetables; natural heat and light for the house; higher property value.')],
         ['cons-6-4', 'cons-1-2'], ['planning-sustainability-environment'], None, 'Solar gain and orientation (6.4) in the design of the dwelling’s surroundings (1.2).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-garden-plan', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p25: five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five pool of nine printed terms: nine separately practicable 10-mark term tasks plus all C(9,5) = 126 complete 50-mark routes.'
TERMS = [
    ('triple-glazing', 'triple glazing', 14, ['cons-3-6', 'cons-6-2'], ['windows-doors', 'heat-loss-insulation'],
     'Such as: three panes of glass separated by insulating gaps, often argon-filled; more energy efficient than single or double glazing; high thermal and sound insulation; typically dearer than double glazing.',
     'Glazing (3.6) and its insulating performance (6.2).'),
    ('wind-turbine', 'wind turbine', 14, ['cons-1-2'], ['planning-sustainability-environment'],
     'Such as: converts the kinetic energy of wind into electricity; renewable, emission-free generation; on land or offshore, singly or in wind farms; Ireland produces a large share of its energy from wind.',
     'Renewable energy and the built environment (1.2). The outgoing syllabus has no renewable-electricity node; 1.2 matches the Planning, Sustainability & Environment reference heading.'),
    ('carbon-monoxide-alarm', 'carbon monoxide alarm', 15, ['cons-1-9', 'cons-5-7'], ['fire-places-fire-prevention'],
     'Such as: detects carbon monoxide, a colourless, odourless, poisonous gas from fuel-burning appliances (boilers, stoves, fires, heaters), and sounds a warning; mandatory when installing new or replacement fossil-fuel appliances; test it regularly.',
     'Building regulations (1.9) for fuel-burning appliances and flues (5.7).'),
    ('mortise-and-tenon-joint', 'mortise and tenon joint', 15, ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'],
     'Such as: a tenon cut on the end of one piece fits a mortise cut in the other; very strong with a large gluing area; used for chair and table legs and rails, doors and windows; a stopped joint hides the tenon.',
     'Joints (10.1) and the choice of joint for strength (10.4). The Ordinary reference taxonomy has no joinery heading; the question keeps its existing Wood, Rot & Ventilation association and 10.1/10.4 are declared outside that heading\'s crosswalk.'),
    ('butt-hinge', 'butt hinge', 14, ['cons-4-5', 'cons-3-7'], ['windows-doors'],
     'Such as: a common hinge joining a door to its frame; two rectangular leaves joined by knuckles and a pin; the leaves sit flush when the door closes; for interior or exterior doors, cabinets and lids; strong and affordable.',
     'Door ironmongery and second fixing (4.5, 3.7).'),
    ('ball-valve', 'ball valve', 16, ['cons-5-2'], ['services-water-gas-electrical'],
     'Such as: controls flow with a rotating ball with a hole through it; open when the hole lines up with the pipe, closed when it is at right angles; the handle shows open, closed or partly open; used to isolate plumbing for maintenance or emergencies.',
     'Water-supply valves (5.2).'),
    ('cordless-circular-saw', 'cordless circular saw', 15, ['cons-9-2', 'cons-9-4'], ['site-safety'],
     'Such as: a portable battery-powered (usually lithium-ion) saw for cutting wood, and sometimes metal or plastic, without a mains cable; can make rip, cross and bevel cuts.',
     'Power tools (9.2) and safety with electricity (9.4). The Ordinary reference taxonomy has no tools heading; 9.2 is declared outside the Site Safety crosswalk, which covers 9.4.'),
    ('fascia-board', 'fascia board', 16, ['cons-3-10'], ['roofs'],
     'Such as: a horizontal board fixed to the ends of the rafters along the lower edge of the roof; timber or uPVC; protects the rafter ends and supports the gutter; closes the roof against moisture and pests; available in colours and decorative profiles.',
     'Eaves detail (3.10).'),
    ('smart-meter', 'smart meter', 16, ['cons-5-8'], ['services-water-gas-electrical'],
     'Such as: an electricity meter that records use automatically and sends readings to the supplier, ending manual and estimated readings; splits use into day, night and peak times; shows usage patterns to help choose a tariff and save energy.',
     'Domestic electrical installation (5.8).'),
]
term_cards = []
for slug, item, page, nodes, topics, content, review in TERMS:
    term_cards.append(add('8', slug, f' — {item}', f'Explain, with the aid of notes and freehand sketches: {item}.',
                          [row('primary', 'Primary communication of relevant information', 6, f'Explain the {item} with notes and freehand sketches; the main relevant explanation earns up to 6. ' + content),
                           row('other', 'Other communication of relevant information', 4, f'Further relevant information about the {item}, in notes or sketches, earns up to 4. The scheme does not reserve fixed marks for notes versus sketches.')],
                          nodes, topics, f'q8-{slug}', review, B8, S8, scheme_pages=[page, 25]))
routes = []
for combo in itertools.combinations(range(9), 5):
    names = [TERMS[i][1] for i in combo]
    routes.append(compose('8', 'complete-' + '--'.join(TERMS[i][0] for i in combo), ' — complete: ' + ', '.join(names),
                          [term_cards[i] for i in combo], None, B8, S8,
                          'Explain, with the aid of notes and freehand sketches, any five of the following: ' + '; '.join(names) + '.',
                          labels=names, scheme_pages=sorted({TERMS[i][2] for i in combo}) + [25]))
assert len(routes) == 126

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p26: (a) two reasons × 6 = 12; (b) two modifications, each sketch 8 + note 5 = 26; (c) suitable timber 4 and two reasons × 4 = 12. Complete 50.'
S9 = 'Part (b) asks for two modifications that together allow for the two printed purposes; the scheme marks Modification 1 and 2 without tying either to a purpose, so it stays one task. Reasons and timber are open.'
A9 = add('9', 'a', '(a)', 'Discuss two reasons why the homeowners may wish to build an extension to their house.',
         [row('reason-1', 'Reason 1', 6, 'Such as: more living space; rearranging the living spaces; more light into the existing farmhouse.'),
          row('reason-2', 'Reason 2', 6, 'A second, different reason, such as: staying rather than buying a bigger house; increasing the value of the home; a more enjoyable place to live.')],
         ['cons-1-2'], ['planning-sustainability-environment'], None, 'Adapting an existing dwelling (1.2).', B9, S9)
B9b = add('9', 'b', '(b)', 'Using notes and freehand sketches, show two modifications to the proposed extension that would allow for the following: additional natural light; access to the garden.',
          [row('modification-1', 'Modification 1', 13, 'Sketch 8 and note 5. Such as: additional or larger windows on the front façade; skylights in the roof.'),
           row('modification-2', 'Modification 2', 13, 'Sketch 8 and note 5, a second, different modification. Such as: a large glazed door, slider or double doors to the garden. Together the two modifications should address both printed purposes.')],
          ['cons-3-5', 'cons-3-7'], ['windows-doors'], 'q9-extension', 'Windows (3.5) and external doors (3.7) added to the extension.', B9, S9)
C9 = add('9', 'c', '(c)', 'Specify a suitable timber for the external cladding, and give two reasons why timber is a suitable cladding material.',
         [row('timber', 'Suitable timber', 4, 'A suitable cladding timber, such as larch, cedar, spruce or charred timber.'),
          row('reason-1', 'Reason 1', 4, 'Such as: a natural material that can be locally sourced and is environmentally friendly.'),
          row('reason-2', 'Reason 2', 4, 'A second, different reason, such as: durable and long-lasting; attractive warm colour; charred timber has a distinctive, durable finish.')],
         ['cons-3-2', 'cons-10-3'], ['foundations-floors-walls', 'wood-rot-ventilation'], 'q9-cladding',
         'External envelope cladding (3.2) in timber (10.3).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-extension', B9, S9, parts(A9, B9b, C9))

# ---------------------------------------------------------------- ledgers
pattern = r'\b(?:choose|select|one\s+of|any\s+\w+|either|or|answer\s+\w+)\b'
observed = []
with fitz.open(R / P) as pdf:
    for i, p in enumerate(pdf):
        text = ' '.join(p.get_text().split())
        observed.extend((i + 1, m.start(), m.group(), text[max(0, m.start() - 80):m.end() + 80]) for m in re.finditer(pattern, text, re.I))
classes = ['Whole-exam selection: any four of the nine questions; all question banks retained, no full-exam Cartesian cards.',
           'Q8 closed choose-five pool of nine printed terms: all C(9,5) = 126 whole-question routes plus nine 10-mark term tasks.']
assert [(o[0], o[2]) for o in observed] == [(1, 'Answer any'), (4, 'any five')], observed
selection_ledger = dict(pattern=pattern, unclassified=0, sourceHashes=HASHES,
                        rows=[dict(page=o[0], start=o[1], match=o[2], context=o[3], classification=c) for o, c in zip(observed, classes)],
                        finiteQuestionChoices={'8': dict(choose=5, options=[t[0] for t in TERMS],
                                                         routes=[[TERMS[i][0] for i in c] for c in itertools.combinations(range(9), 5)],
                                                         wholeRouteMarks=50, termMarks=10)})
whole = {}
for t in tasks:
    c = t['card']
    if '-complete' in c['id']:
        whole.setdefault(t['questionNumber'], []).append(dict(id=c['id'], parts=[g['label'] for g in c['taskGroups']], marks=c['totalMarks']))
taxonomy_gaps = [
    dict(cardId=PREFIX + 'q8-mortise-and-tenon-joint', canonicalTopicIds=['cons-10-1', 'cons-10-4'], atlasTopicId=CROSS + 'wood-rot-ventilation',
         reason='No Ordinary outgoing reference heading covers joinery (10.1, 10.4).'),
    dict(cardId=PREFIX + 'q8-cordless-circular-saw', canonicalTopicIds=['cons-9-2'], atlasTopicId=CROSS + 'site-safety',
         reason='No Ordinary outgoing reference heading covers tools (9.2).'),
]
out = dict(schemaVersion=1, subjectId='construction-studies', year=2026, level='ordinary', lang='ev', sitting='main', paperKey='single',
           fileid='LC029GLP000EV.pdf', component='theory', status='Q1–Q9 source-reviewed draft; integration pending.',
           sourceHashes=HASHES, tasks=tasks, bindings=bindings, questionFigures=question_figures,
           addedIds=[t['card']['id'] for t in tasks], selectionLedger=selection_ledger,
           questionRouteLedgers={q: dict(wholeRoutes=w) for q, w in whole.items()}, taxonomyGaps=taxonomy_gaps,
           questionsReviewed=list(QUESTIONS), unreviewedQuestions=[])
(HERE / 'ordinary-2026-draft.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(tasks=len(tasks), figures=len(question_figures),
                      perQuestion={q: sum(1 for t in tasks if t['questionNumber'] == q) for q in QUESTIONS})))
