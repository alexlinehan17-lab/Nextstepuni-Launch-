"""Draft the 2023 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Question wording and stems are lifted from the SEC paper (a narrowed task only deletes printed
words); every row's verbatim is printed in the scheme's mark tables (pages 16-24), checked against
rendered pages. Unbanded components accept any whole mark up to the published maximum; printed
excellent/good/fair bands are kept as printed. Sources are the byte-identical paper-trail-corpus
copies, pinned by SHA-256. Figures are exact 2x crops; the Q8 solution figure is a composite of the
three scheme pages that carry every term's notes and sketch.

The 27 pre-audit 2023 Ordinary cards: 19 keep their IDs (and concept IDs) and are corrected in place,
each correction recording the SHA-256 of the card it replaces. Q8 "any five of nine" is ONE card
(choice is not a route): it keeps the pre-audit concrete-mixer ID, and the other eight per-term IDs
are withdrawn into it through progress aliases. Every other prior card stays byte-identical.
"""
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
R = HERE.parents[4]
sys.path.insert(0, str(R / 'scripts/markbank/authoring'))
import construction_figures  # noqa: E402

P = 'paper-trail-corpus/exampapers/2023/LC029GLP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2023/LC029GLP000EV.pdf'
HASHES = {P: 'e0a846a2ce2454b807ef95754ed579c79a7a6cb468a158e68ad50991441e8db9',
          S: '1018b8c0eada563d4713dab8ec9b219d47a1cec60e2b84b56e536f9222195025'}
ATTRIBUTION = 'SEC Leaving Certificate Construction Studies 2023 Ordinary Level — © State Examinations Commission.'
FP = 'construction-studies-2023-OL-'
PREFIX = 'cons-2023-ol-'
CROSS = 'construction-studies-ordinary-'
BAND8 = [0, 4, 6, 8]
BAND6 = [0, 2, 4, 6]

for f, h in HASHES.items():
    assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f

# The pre-audit cards are snapshotted before integration so the draft regenerates byte-identically afterwards.
LEGACY_FILE = HERE / 'prior-2023-ordinary-cards.json'
if not LEGACY_FILE.exists():
    AUTHORED = json.loads((R / 'scripts/markbank/authored/construction-studies.json').read_text())
    LEGACY_FILE.write_text(json.dumps([c for c in AUTHORED if c['id'].startswith(PREFIX)], ensure_ascii=False, indent=2) + '\n')
LEGACY = {c['id']: c for c in json.loads(LEGACY_FILE.read_text())}
assert len(LEGACY) == 27, sorted(LEGACY)
Q8_KEPT = 'q8-None-concrete-mixer'
CONSOLIDATED = {f'q8-None-{t}': Q8_KEPT for t in ['smart-radiator-valve', 'ridge-tile', 'triple-glazing', 'balusters', 'cedar-cladding',
                                                  'bridle-joint', 'wood-pellet-stove', 'floor-screed']}


def card_hash(c):
    return hashlib.sha256(json.dumps(c, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def composite(*panels):
    return construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [45, 39, 580, 288], False), 'q2-original': (P, 2, [45, 288, 580, 530], False),
    'q3-original': (P, 2, [45, 530, 580, 767], False), 'q4-original': (P, 3, [45, 39, 580, 312], False),
    'q5-original': (P, 3, [45, 312, 580, 585], False), 'q6-original': (P, 3, [45, 585, 580, 767], False),
    'q7-original': (P, 4, [45, 39, 580, 386], False), 'q8-original': (P, 4, [45, 386, 580, 480], False),
    'q9-original': (P, 4, [45, 527, 580, 767], False),
    'q1-scheme': (S, 4, [51, 58, 545, 722], True),
    'q2-reasons': (S, 5, [51, 58, 540, 188], True), 'q2-method': (S, 5, [51, 188, 540, 566], True),
    'q2-upgrade': (S, 5, [51, 566, 540, 770], True),
    'q3-system': (S, 6, [51, 58, 545, 560], True), 'q3-locations': (S, 6, [51, 588, 545, 768], True),
    'q4-advantages': (S, 7, [51, 58, 545, 198], True), 'q4-fixing': (S, 7, [51, 198, 545, 472], True),
    'q4-finishes': (S, 7, [51, 474, 552, 782], True),
    'q5-section': (S, 8, [51, 58, 545, 615], True), 'q5-closer': (S, 8, [51, 615, 545, 792], True),
    'q6-classroom': (S, 9, [51, 58, 545, 334], True), 'q6-lathe': (S, 9, [51, 334, 545, 610], True),
    'q6-tidy': (S, 9, [51, 610, 545, 780], True),
    'q7-advantages': (S, 10, [51, 58, 545, 210], True),
    'q7-layout': composite((10, [51, 212, 545, 712]), (11, [51, 50, 545, 392])),
    'q7-covering': (S, 11, [51, 394, 545, 740], True),
    'q8-terms': composite((12, [51, 58, 545, 797]), (13, [51, 50, 545, 722]), (14, [51, 50, 545, 764])),
    'q9-materials': (S, 15, [51, 58, 545, 340], True), 'q9-modifications': (S, 15, [51, 340, 545, 566], True),
    'q9-reasons': (S, 15, [51, 566, 545, 776], True),
}
question_figures = [construction_figures.entry(FP + key, spec, HERE / f'{FP}{key}.png') for key, spec in FIGURES.items()]


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
    '1': dict(page=2, title='External wall and timber first floor section', concept='first-floor-wall-section',
              stem='The sketch shows the external wall and timber first floor of a dwelling house. The external wall is a 400 mm concrete block wall with a full-fill insulated cavity. The wall is plastered on both sides. The first floor joists are 225 mm × 50 mm and are fixed to the external wall using joist hangers. The floor is finished with a tongued and grooved hardwood floor, on 20 mm plywood decking with a plasterboard ceiling beneath.',
              note='Original sketch and specification retained. Construction details, dimensions and draughting belong to part (a); the wall-tie detail in (b) is marked separately. Any alternative detailing that complies with current Building Regulations is acceptable.'),
    '2': dict(page=2, title='Energy upgrades to an old house', concept='energy-upgrades',
              stem='The sketch shows an old uninsulated dwelling house. The homeowner has received a grant to carry out energy upgrades to their house. They have decided to start by adding external insulation to the walls of the house.',
              note='Original sketch retained. The insulation method and type, and the other upgrade in (c), are open choices; the scheme lists typical examples.'),
    '3': dict(page=2, title='Solar collector hot water pipework', concept='solar-hot-water',
              stem='The sketch shows a dwelling house which has a solar collector on the roof. The solar collector provides hot water for the household.',
              note='Original sketch retained. The listed components are required content, not a choice. The scheme diagram is one acceptable layout; any alternative that complies with current Building Regulations is acceptable.'),
    '4': dict(page=3, title='Prefabricated trussed rafters', concept='trussed-rafter-roof',
              stem='The sketch shows the roof of a house under construction. The homeowners have decided to construct the roof using prefabricated trussed rafters.',
              note='Original sketch retained. All five printed items in (b) are required in one sketch; the roof finish in (c) is an open choice.'),
    '5': dict(page=3, title='External wall and flat roof eaves section', concept='flat-roof-eaves-section',
              stem='The sketch shows the eaves of a flat roof. The roof is covered with a waterproof membrane, on 150 mm rigid insulation, on a 20 mm plywood deck supported by sloping firring pieces. The 200 mm × 50 mm timber joists have a plasterboard ceiling beneath. The roof is supported on a 400 mm concrete block wall with a full-fill insulated cavity. The wall is rendered on both sides.',
              note='Original sketch and specification retained. Construction details and draughting belong to part (a); the cavity-closer detail in (b) is marked separately.'),
    '6': dict(page=3, title='Safety in the Construction Studies room', concept='classroom-safety', stem='',
              note='Original question retained. Both printed situations in (a) are required, two precautions each. Precautions and reasons are open responses; the scheme lists typical examples.'),
    '7': dict(page=4, title='Utility room design', concept='utility-room',
              stem='The draft design for a utility room in a new dwelling house is shown. The positions of the external door, window and a door to the kitchen are included.',
              note='Original plan retained. All four printed items in (b) are required in one sketch; locations, reasons and the floor covering are open, well-reasoned responses.'),
    '8': dict(page=4, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=4, title='An accessible front entrance', concept='accessible-front-entrance',
              stem='The sketch shows a front entrance to a semi-detached house. The owners wish to modify the front entrance to make it fit for use by a person with limited mobility.',
              note='Original sketch retained. The door material, modifications and reasons are open responses; the scheme lists typical examples.'),
}
SCHEME_PAGES = {'1': [4, 16], '2': [5, 17], '3': [6, 18], '4': [7, 19], '5': [8, 20], '6': [9, 21],
                '7': [10, 11, 22], '8': [12, 13, 14, 23], '9': [15, 24]}

tasks, bindings, cards = [], [], {}


def add(q, key, ref, text, rows, nodes, topics, figure, review, boundary, selection, groups=None):
    meta = QUESTIONS[q]
    cid = f'{PREFIX}q{q}-{key}'
    concept = LEGACY[cid]['conceptId'] if cid in LEGACY else f"{meta['concept']}-{key}"
    card = dict(id=cid, subjectId='construction-studies', year=2023, level='ordinary', section='B',
                topicId=nodes[0], conceptId=concept, questionRef=f'2023 OL Q{q}{ref}',
                stem=meta['stem'], questionText=text, tariffModel={'kind': 'fixed'},
                totalMarks=sum(r['marks'] for r in rows), rows=rows,
                questionFigureKey=f'{FP}q{q}-original', questionFigureIncludesPrompt=True)
    if figure:
        card['figureKey'] = FP + figure
    card['sourceMaterial'] = dict(kind='source-illustration', label=f'ORIGINAL QUESTION {q}', title=meta['title'],
                                  pages=[1, meta['page']], attribution=ATTRIBUTION, presentationNote=meta['note'])
    if groups:
        card['taskGroups'] = groups
    tasks.append(dict(questionNumber=q, correction=cid in LEGACY, card=card, sourceChecks=checks(meta['page'], SCHEME_PAGES[q]),
                      boundaryReview=boundary, selectionReview=selection,
                      requiredQuestionFigures=[f'{FP}q{q}-original'], requiredSolutionFigures=[FP + figure] if figure else []))
    bindings.append(dict(cardId=cid, markBankTopicId=nodes[0], canonicalTopicIds=nodes, canonicalTopicReview=review,
                         questionNumber=q, atlasTopicIds=[CROSS + t for t in topics]))
    cards[cid] = card
    return card


def compose(q, key, ref, children, figure, boundary, selection, text, labels=None):
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
               boundary, selection, groups=groups)


def parts(*cs):
    return '\n\n'.join(f'({letter}) {c["questionText"]}' for letter, c in zip('abc', cs))


# ---------------------------------------------------------------- Q1
B1 = 'Scheme p16 (printed 14): (a) best 7 of 10 listed details × 5 = 35, four typical dimensions 4, draughting/accuracy/scale 8 (8/6/4), all printed within part (a): 47; (b) wall tie 3. Complete 50.'
S1 = 'One required section and one required wall-tie detail. The best-seven detail list is a marking menu, not a printed choose-seven task.'
A1 = add('1', 'a', '(a)',
         'To a scale of 1:5, draw a vertical section through the external wall and first floor. On your drawing show the typical construction details from a level 400 mm below the plasterboard ceiling to a level 400 mm above the hardwood floor. Show an internal floor width of 900 mm. Include four typical dimensions.',
         [row('details', 'Any 7 x 5 marks', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: concrete block outer leaf with render; full-fill cavity with wall tie; concrete block inner leaf with internal plaster; joist hanger; joist; airtight tape; plasterboard; plywood decking; tongue and groove flooring; skirting board. The model specifies 19 mm render, 100 mm leaves, a 200 mm full-fill cavity, 15 mm plaster, 225 × 50 mm joists and 20 mm plywood decking.', list(range(0, 36, 5))),
          row('dimensions', 'Any 4 typical dimensions', 4, 'Four appropriate typical dimensions on the section.'),
          row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the section: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-3-3', 'cons-4-3'], ['question-one-drawing-questions', 'foundations-floors-walls'], 'q1-scheme',
         'Scaled drawing (1.5) of a cavity wall (3.3) supporting a timber upper floor (4.3).', B1, S1)
B1b = add('1', 'b', '(b)', 'On your drawing, show the typical design detailing to connect the inner and outer leaves of the external wall.',
          [row('wall-tie', 'Wall tie clearly identified', 3, 'Show and identify the wall tie connecting the two leaves across the cavity, as in the scheme’s model section.', [0, 3])],
          ['cons-3-3'], ['foundations-floors-walls'], 'q1-scheme', 'Cavity walls and their ties (3.3).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-scheme', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p17 (printed 15): (a) two reasons × 6 = 12; (b) method note & sketch 8 + 8 = 16, insulation type 4, thickness 4 = 24; (c) other upgrade note & sketch 7 + 7 = 14. Complete 50.'
S2 = '"one suitable method" and "one other possible energy upgrade" are open choices with no printed list; each part stays one response.'
A2 = add('2', 'a', '(a)', 'Discuss two reasons why energy upgrade grants are available for old houses.',
         [row('reason-1', 'Reason 1', 6, 'Such as: to improve the BER of the house; to reduce the energy use of the home and so its carbon emissions.'),
          row('reason-2', 'Reason 2', 6, 'A second, different reason. Such as: to encourage owners to upgrade existing houses instead of building new ones; to make older houses energy efficient, sustainable and economical to heat; to encourage greener living.')],
         ['cons-6-3', 'cons-1-2'], ['heat-loss-insulation', 'planning-sustainability-environment'], 'q2-reasons',
         'Running costs (6.3) and a sustainable built environment (1.2).', B2, S2)
B2b = add('2', 'b', '(b)', 'Using notes and freehand sketches, show one suitable method of applying an external insulation system to a house. Specify the type and thickness of insulation.',
          [row('method', 'Method of insulating external walls note & sketch (8 + 8 marks)', 16, 'Note 8 and sketch 8 of one method. Such as: clean the wall; fix starter tracks at DPC level; apply adhesive to the back and perimeter of the boards and stagger their joints; fix with mechanical anchors; apply a 6–10 mm polymer-modified base render with glass-fibre mesh lapped at least 100 mm; then a final finish.'),
           row('type', 'Preferred insulation type for external wall', 4, 'Such as: expanded polystyrene (EPS), phenolic, polyisocyanurate (PIR) or extruded polystyrene (XPS).'),
           row('thickness', 'Thickness of insulation', 4, 'The scheme recommends a 200 mm insulation thickness.')],
          ['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q2-method', 'Insulating materials (6.2) applied to an external wall (3.3).', B2, S2)
C2 = add('2', 'c', '(c)', 'On a separate sketch show, using notes and freehand sketches, one other possible energy upgrade the homeowner could carry out to their house.',
         [row('upgrade', 'Possible energy upgrade note & sketch (7 + 7 marks)', 14, 'Note 7 and sketch 7 of one other upgrade. Such as: more insulation at roof level; solar panels to supplement grid electricity; a more energy-efficient heating system; a wood-burning stove in place of an open fire; high-performance windows.')],
         ['cons-6-2', 'cons-5-3'], ['heat-loss-insulation', 'hot-water-space-heating'], 'q2-upgrade',
         'Upgrading the insulated fabric (6.2) or the heating system (5.3).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-method', B2, S2, parts(A2, B2b, C2))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p18 (printed 16): (a) best 8 of 11 listed items × 5 = 40; (b) two considerations × 5 = 10. Complete 50.'
S3 = 'The printed component list is required content, not a choice; the best-eight list is a marking menu.'
A3 = add('3', 'a', '(a)', 'Draw a large freehand sketch of the given house. On your sketch, show the pipework necessary to connect the solar collector to the hot water cylinder and supply hot water to a shower. Include the following in your sketch: flow and return pipes; expansion vessel; pipework to shower; all necessary valves.',
         [row('details', 'Any 8 x 5 marks', 40, 'Credit the best EIGHT acceptable items at 5 marks each, capped at 40. Marked items: solar collector; cold feed to collector; hot return to cylinder; cylinder; circulation pump; solar expansion vessel; storage tank; cold feed to cylinder; expansion pipe; hot water to shower and shower unit; valves. Typical sizes: Ø22 mm feed and return, a 250 l cylinder, a 24 l solar expansion vessel, a Ø28 mm expansion pipe, Ø22 mm hot water to the shower.', list(range(0, 41, 5)))],
         ['cons-5-2', 'cons-6-4'], ['hot-water-space-heating', 'planning-sustainability-environment'], 'q3-system',
         'Hot water supply (5.2) from solar heat gain (6.4).', B3, S3)
B3b = add('3', 'b', '(b)', 'Discuss two considerations when deciding the location of solar panels on a house.',
          [row('consideration-1', 'Consideration 1', 5, 'Such as: the orientation of the roof; the position and proximity of neighbouring buildings; the pitch of the roof.'),
           row('consideration-2', 'Consideration 2', 5, 'A second, different consideration. Such as: whether the roof can support and secure the panels; the usable roof area; shading from trees; ease of maintenance and cleaning.')],
          ['cons-6-4', 'cons-3-9'], ['planning-sustainability-environment', 'roofs'], 'q3-locations', 'Solar heat gain (6.4) on the roof covering (3.9).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-system', B3, S3, parts(A3, B3b))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p19 (printed 17): (a) two advantages × 4 = 8; (b) external wall, wallplate, trussed rafter, nail plate and truss clip, each sketch 4 + note 2 = 30; (c) suitable material 4, two reasons × 4 = 12. Complete 50.'
S4 = 'All five printed items in (b) are required in one sketch, not a choice. The roof finish in (c) is an open choice with no printed list.'
A4 = add('4', 'a', '(a)', 'Discuss two advantages of using prefabricated trussed rafters to construct a roof.',
         [row('advantage-1', 'Advantage 1', 4, 'Such as: less waste than a cut roof; quicker roof construction on site.'),
          row('advantage-2', 'Advantage 2', 4, 'A second, different advantage. Such as: more efficient use of material; open-plan layouts, as the truss does not rely on internal walls for support.')],
         ['cons-3-8'], ['roofs'], 'q4-advantages', 'Trussed rafters (3.8).', B4, S4)
B4b = add('4', 'b', '(b)', 'Using notes and a freehand sketch, show the typical construction details of how a trussed rafter is secured on the external wall of a house. Include the following in your sketch: external wall; wallplate; trussed rafter; nail plate; truss clip.',
          [row('wall', 'external wall sketch & note (4 + 2 marks)', 6, 'Sketch 4 and note 2. Such as: the insulated external wall finished with a cavity closer.'),
           row('wallplate', 'wallplate sketch & note (4 + 2 marks)', 6, 'Sketch 4 and note 2. Such as: a 100 mm × 75 mm wallplate fixed to the wall with 1200 mm galvanised steel straps.'),
           row('rafter', 'trussed rafter sketch & note (4 + 2 marks)', 6, 'Sketch 4 and note 2. Such as: trussed rafters prefabricated off site, lifted onto the truss clips and secured.'),
           row('nail-plate', 'nail plate sketch & note (4 + 2 marks)', 6, 'Sketch 4 and note 2. Such as: nail plates mechanically fixed at all joints for strength and rigidity.'),
           row('truss-clip', 'truss clip sketch & note (4 + 2 marks)', 6, 'Sketch 4 and note 2. Such as: truss clips fixed to the wallplate at 400 mm intervals.')],
          ['cons-3-8', 'cons-3-10', 'cons-3-3'], ['roofs', 'foundations-floors-walls'], 'q4-fixing',
          'Securing trussed rafters (3.8) at the eaves (3.10) on the external wall (3.3).', B4, S4)
C4 = add('4', 'c', '(c)', 'Specify a suitable roof finish material for the house, and give two reasons for your choice.',
         [row('material', 'Suitable material', 4, 'Such as: slate, tiles, photovoltaic slates or zinc sheeting.'),
          row('reason-1', 'Reason 1', 4, 'A reason matching the finish. Such as, slate: attractive, durable, low maintenance, long lasting; tiles: long life span, low maintenance, recyclable, cheaper.'),
          row('reason-2', 'Reason 2', 4, 'A second, different reason. Such as, photovoltaic slates: generate energy on site and are more discreet than panels; zinc: modern, easily shaped, more choice of colour.')],
         ['cons-3-9'], ['roofs'], 'q4-finishes', 'Roof coverings (3.9).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-fixing', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p20 (printed 18): (a) best 8 of 12 listed details × 5 = 40, draughting/accuracy/scale 6 (6/4/2), both printed within part (a): 46; (b) cavity closer 4. Complete 50.'
S5 = 'One required section and one required cavity-closer detail. The best-eight detail list is a marking menu, not a printed choose-eight task.'
A5 = add('5', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the external wall and the eaves of the flat roof. On your drawing, show the typical construction details from a level 450 mm below the wallplate, through the external wall and eaves. Show 900 mm length of roof joist.',
         [row('details', 'Any 8 x 5 marks', 40, 'Credit the best EIGHT acceptable details at 5 marks each, capped at 40. Marked details: concrete block outer leaf with external render; full-fill insulated cavity with wall tie; concrete block inner leaf with internal plaster; wallplate with cavity closer; waterproof membrane; insulation; plywood decking with breather membrane; firring piece; insulated ceiling joist; insulated plasterboard ceiling with airtight membrane; fascia and soffit; gutter. The model specifies 19 mm render, 100 mm leaves, a 200 mm cavity, 15 mm plaster, a 100 × 75 mm wallplate, 150 mm insulation, 20 mm plywood, 200 × 50 mm joists and a 50 mm insulated plasterboard ceiling.', list(range(0, 41, 5))),
          row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 6, 'Draughting, accuracy and scale of the section: excellent 6, good 4, fair 2.', BAND6)],
         ['cons-1-5', 'cons-3-10', 'cons-3-3', 'cons-6-2'], ['question-one-drawing-questions', 'roofs', 'foundations-floors-walls', 'heat-loss-insulation'], 'q5-section',
         'Scaled drawing (1.5) of a flat roof at the eaves (3.10) on a cavity wall (3.3) with an insulated cavity (6.2).', B5, S5)
B5b = add('5', 'b', '(b)', 'On your drawing show the typical design detailing to ensure that the cavity is closed at wallplate level.',
          [row('closer', 'Cavity closer', 4, 'Show and identify the cavity closer at wallplate level, as in the scheme’s model detail. Any other suitable detail is accepted.', [0, 4])],
          ['cons-3-3', 'cons-6-2'], ['foundations-floors-walls', 'heat-loss-insulation'], 'q5-closer', 'Closing the cavity wall (3.3) against a thermal bridge (6.2).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-section', B5, S5, parts(A5, B5b))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p21 (printed 19): (a) two precautions for each of the two situations × 4 = 16; (b) three precautions each with a reason (3 + 3 + 2) = 24; (c) two reasons × 5 = 10. Complete 50.'
S6 = 'Both printed situations in (a) are required, each with two precautions, not a choice. Precautions and reasons are open responses; the scheme lists typical examples.'
A6 = add('6', 'a', '(a)', 'State two specific safety precautions to be observed in the Construction Studies classroom in each of the following situations: using a jigsaw; using epoxy adhesive.',
         [row('jigsaw-1', 'Using a jigsaw - Safety precaution 1', 4, 'Such as: wear a dust mask; wear ear protection; wear eye protection against dust and flying chips.'),
          row('jigsaw-2', 'Using a jigsaw - Safety precaution 2', 4, 'A second, different jigsaw precaution. Such as: keep leads from being a trip hazard; secure the work piece against movement.'),
          row('epoxy-1', 'Using epoxy adhesive - Safety precaution 1', 4, 'Such as: work in a well-ventilated zone; protect skin and clothing.'),
          row('epoxy-2', 'Using epoxy adhesive - Safety precaution 2', 4, 'A second, different epoxy precaution. Such as: a respirator mask against the vapours; eye protection; keep the work area clear to avoid slips if the epoxy leaks.')],
         ['cons-9-4'], ['site-safety'], 'q6-classroom', 'Safety with tools and equipment (9.4).', B6, S6)
B6b = add('6', 'b', '(b)', 'Using notes and freehand sketches, describe three specific safety precautions to be observed when woodturning on a lathe. Give one reason for each safety precaution outlined.',
          [row(f'precaution-{i}', f'Safety precautions {i} and reason (3 + 3 + 2 marks)', 8, note) for i, note in [
              (1, 'A precaution in notes and sketch with its reason, marked 3 + 3 + 2. Such as: close-fitting protective clothing; long or loose hair tied back.'),
              (2, 'A second, different precaution with its reason, 3 + 3 + 2. Such as: a face visor; a dust mask or breathing protection.'),
              (3, 'A third, different precaution with its reason, 3 + 3 + 2. Such as: the tool rest at the correct height and distance from the work piece; the correct speed (RPM) for the size of the work piece.')]],
          ['cons-9-4'], ['site-safety'], 'q6-lathe', 'Safety with tools and equipment (9.4).', B6, S6)
C6 = add('6', 'c', '(c)', 'Discuss two reasons why it is important to maintain an organised and tidy environment in a Construction Studies room.',
         [row('reason-1', 'Reason 1', 5, 'Such as: fewer trip hazards; tools and materials are easier to find.'),
          row('reason-2', 'Reason 2', 5, 'A second, different reason. Such as: less time lost locating tools; less damage to tools and machines; off-cuts stored for reuse, reducing waste; neat, correct working procedure.')],
         ['cons-9-4'], ['site-safety'], 'q6-tidy', 'Safety with tools and equipment (9.4).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-lathe', B6, S6, parts(A6, B6b, C6))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p22 (printed 20): (a) two advantages × 5 = 10; (b) sketch 8 and four items, each location 3 + reason 2 = 5, = 28; (c) floor covering 4 and two reasons × 4 = 12. Complete 50.'
S7 = 'All four printed items in (b) are required in one sketch, not a choice. The floor covering in (c) is an open choice with no printed list.'
A7 = add('7', 'a', '(a)', 'Discuss two advantages of including a large utility room in the design of a new home.',
         [row('advantage-1', 'Advantage 1', 5, 'Such as: extra usable kitchen space; a place to store outdoor shoes and clothing, keeping the house hygienic.'),
          row('advantage-2', 'Advantage 2', 5, 'A second, different advantage. Such as: the washing machine away from the kitchen to reduce noise; storage for bulky items; a secure space for a pet; space to hang and air washed clothes.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q7-advantages', 'Layout design within the built environment (1.2).', B7, S7)
B7b = add('7', 'b', '(b)', 'Draw a large freehand sketch of the given design and show your preferred location for each of the following in the utility room: sink; washing machine; storage units; seating / boot area. Give one reason for selecting each location.',
          [row('sketch', 'Sketch', 8, 'A large freehand sketch of the given utility room design.'),
           row('sink', 'Location and valid reason for sink (3 + 2 marks)', 5, 'Location 3 and reason 2. Such as: by the window for natural light and a view out; on an external wall for the wastewater connection.'),
           row('washing-machine', 'Location and valid reason for washing machine (3 + 2 marks)', 5, 'Location 3 and reason 2. Such as: on an external wall for wastewater disposal and water supply; near electrical sockets.'),
           row('storage', 'Location and valid reason for storage units (3 + 2 marks)', 5, 'Location 3 and reason 2. Such as: against a wall so they do not block the doors and can be fixed securely; beside the washing machine for laundry and detergents.'),
           row('seating', 'Location and valid reason for seating / boot area (3 + 2 marks)', 5, 'Location 3 and reason 2. Such as: against a wall so it can be fixed securely; close to the external door for removing and storing shoes and boots.')],
          ['cons-1-2'], ['planning-sustainability-environment'], 'q7-layout', 'Layout design within the built environment (1.2).', B7, S7)
C7 = add('7', 'c', '(c)', 'Specify a suitable floor covering for the utility room and give two reasons for your choice.',
         [row('covering', 'Suitable floor covering', 4, 'Such as: ceramic tiles, vinyl, polished concrete, wood laminate or linoleum.'),
          row('reason-1', 'Reason 1', 4, 'A reason matching the covering. Such as, ceramic tiles: hard wearing, resistant to water damage, easy to maintain; vinyl: easy to install, water resistant.'),
          row('reason-2', 'Reason 2', 4, 'A second, different reason. Such as, polished concrete: transfers underfloor heating well, highly durable; wood laminate: durable and less expensive; linoleum: hardwearing and waterproof.')],
         ['cons-4-2', 'cons-1-2'], ['foundations-floors-walls', 'planning-sustainability-environment'], 'q7-covering', 'A ground-floor finish (4.2) chosen for the room (1.2).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-layout', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p23 (printed 21): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination. It keeps the pre-audit concrete-mixer ID; the other eight per-term IDs alias to it.'
TERMS = [
    ('concrete-mixer', 'concrete mixer', 'Concrete mixer', ['cons-2-7'], ['concrete'],
     'a rotating drum that turns raw materials into concrete without segregation; small on-site batch mixers (electric, petrol or diesel) are hand loaded and make up to 200 litres per batch, so quality control is difficult; larger quantities come from a mixing plant in a ready-mix truck of 4–6 cubic metres, better regulated and poured directly into the work area.',
     'Site and ready-mixed concrete (2.7).'),
    ('smart-radiator-valve', 'smart radiator valve', 'Smart radiator valve', ['cons-5-3'], ['hot-water-space-heating', 'services-water-gas-electrical'],
     'fitted to new or existing radiators; integrated sensors measure the room temperature and signal to reduce or increase the flow of hot water; controlled from smart devices when the owners are away; each room can have its own temperature; reduces energy cost and use.',
     'Heating systems and temperature control (5.3).'),
    ('ridge-tile', 'ridge tile', 'Ridge tile', ['cons-3-9'], ['roofs'],
     'sits on the apex of the roof and seals the intersection of the two roof planes; traditionally bedded in mortar, now often fixed with integrated dry-fix systems; made from materials like the roof covering, in a variety of colours and profiles.',
     'Roof coverings (3.9).'),
    ('triple-glazing', 'triple glazing', 'Triple glazing', ['cons-3-6', 'cons-6-2'], ['windows-doors', 'heat-loss-insulation'],
     'three panes of glass with cavities usually filled with an inert gas (argon, xenon or krypton); reduces noise and insulates better than double glazing; heavier and thicker, so it may not suit all frames; it can reduce solar gain, so some owners avoid it on the southern elevation.',
     'Glass and glazing (3.6) against heat loss (6.2).'),
    ('balusters', 'balusters', 'Balusters', ['cons-4-4'], ['foundations-floors-walls'],
     'vertical members between the handrail and string of a stairs, also called spindles; moulded, square or lathe-turned; must not let a 100 mm diameter sphere pass between them; made of wood, iron or plastic.',
     'Stairs (4.4). The Ordinary reference taxonomy has no stairs heading; as in the reviewed reference topics for this question, the term keeps the Foundations, Floors & Walls association, and 4.4 is declared outside that heading’s crosswalk.'),
    ('cedar-cladding', 'cedar cladding', 'Cedar cladding', ['cons-3-2'], ['foundations-floors-walls', 'wood-rot-ventilation'],
     'naturally durable, lasting over 60 years without preservative treatment, which is only needed to avoid the weathered silver-grey colour; fixed horizontally or vertically to battens with stainless steel or galvanised fixings, as cedar reacts with ferrous metals; low embodied energy.',
     'The external envelope (3.2), finished in a naturally durable timber.'),
    ('bridle-joint', 'bridle joint', 'Bridle joint', ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'],
     'a common, strong woodworking joint with a large gluing area; a tee or corner bridle, removing one third of the material from one piece and two thirds from the other; used in frame construction and to join table rails to uprights.',
     'Joints (10.1) and the choice of joint (10.4). The Ordinary reference taxonomy has no joinery heading; the term keeps the Wood, Rot & Ventilation association used for joinery, and 10.1/10.4 are declared outside that heading’s crosswalk.'),
    ('wood-pellet-stove', 'wood pellet stove', 'Wood pellet stove', ['cons-5-3', 'cons-1-2'], ['hot-water-space-heating', 'planning-sustainability-environment'],
     'heats a home by burning renewable pellets of compressed sawdust and waste wood; an auger feeds fuel steadily from a hopper for a constant flame needing little adjustment; a low-cost heating alternative with very low emissions and a smaller environmental impact.',
     'Heating systems (5.3) with a renewable fuel in a sustainable built environment (1.2).'),
    ('floor-screed', 'floor screed', 'Floor screed', ['cons-4-2'], ['foundations-floors-walls'],
     'the final layer of the floor on which a floor finish is laid; traditionally sand and cement at 3:1 to 5:1, levelled with a tamping board; modern free-flowing calcium sulphate screeds self-level and suit underfloor heating, at 50–75 mm over pipes clipped to the rigid insulation.',
     'Ground floors (4.2).'),
]
Q8 = add('8', Q8_KEPT.removeprefix('q8-'), '', 'Explain, with the aid of notes and freehand sketches, any five of the following: ' + '; '.join(t[1] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Construction Terms', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{t[2]}: {t[5]}' for t in TERMS),
               group=dict(claimMax=5, perOption=10, options=[t[2] for t in TERMS]))],
         list(dict.fromkeys(n for t in TERMS for n in t[3])), list(dict.fromkeys(a for t in TERMS for a in t[4])), 'q8-terms',
         'The union of the nine printed terms: ' + ' '.join(t[6] for t in TERMS), B8, S8)

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p24 (printed 22): (a) suitable material 4, two reasons × 4 = 12; (b) two modifications, each notes + sketch 8 + 5 = 13, = 26; (c) two reasons × 6 = 12. Complete 50.'
S9 = 'The door material, modifications and reasons are open responses with no printed list; the scheme lists typical examples.'
A9 = add('9', 'a', '(a)', 'Specify a suitable material for a new front door, and give two reasons for your choice.',
         [row('material', 'Suitable material', 4, 'Such as: cedar, larch, oak, teak, uPVC or aluminium.'),
          row('reason-1', 'Reason 1', 4, 'A reason matching the material. Such as: durability; some wood species need no preservative because of their natural oils.'),
          row('reason-2', 'Reason 2', 4, 'A second, different reason. Such as: natural resistance to insect attack or moisture; aluminium and uPVC need no regular maintenance.')],
         ['cons-3-7'], ['windows-doors'], 'q9-materials', 'External doors (3.7).', B9, S9)
B9b = add('9', 'b', '(b)', 'Using notes and freehand sketches, show two modifications to the front entrance area that would allow access to the house for a person with limited mobility.',
          [row('modification-1', 'Modification 1 to entrance notes + sketch (8 + 5 marks)', 13, 'Notes and sketch, 8 + 5. Such as: a ramp to the main entrance at a 1:20 slope, at least 1200 mm wide, with a level landing and turning circle; a smooth, slip-resistant surface in place of loose driveway material.'),
           row('modification-2', 'Modification 2 to entrance notes + sketch (8 + 5 marks)', 13, 'Notes and sketch, 8 + 5, for a second, different modification. Such as: a doorway widened to a 1000 mm clear opening; a low-level threshold; a glass panel to see who is at the door; high- and low-level lighting; a weather canopy.')],
          ['cons-1-2', 'cons-3-7'], ['planning-sustainability-environment', 'windows-doors'], 'q9-modifications',
          'Accessible design of the built environment (1.2) at the entrance door (3.7).', B9, S9)
C9 = add('9', 'c', '(c)', 'Discuss two reasons why the owners would wish to create a front entrance that is accessible for all.',
         [row('reason-1', 'Reason 1', 6, 'Such as: a higher resale value, with costly modifications already done; a home future-proofed for prams, buggies, walking aids and wheelchairs.'),
          row('reason-2', 'Reason 2', 6, 'A second, different reason. Such as: fewer costly renovations later; more sustainable living, as retrofitting later uses more resources and energy.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q9-reasons', 'Accessible design of the built environment (1.2).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-modifications', B9, S9, parts(A9, B9b, C9))

# ---------------------------------------------------------------- ledgers
pattern = r'\b(?:choose|select|one\s+of|any\s+\w+|either|or|answer\s+\w+)\b'
observed = []
with fitz.open(R / P) as pdf:
    for i, p in enumerate(pdf):
        text = ' '.join(p.get_text().split())
        observed.extend((i + 1, m.start(), m.group(), text[max(0, m.start() - 80):m.end() + 80]) for m in re.finditer(pattern, text, re.I))
classes = {(1, 'Answer any'): 'Whole-exam selection: any four of the nine questions; all question banks retained, no full-exam Cartesian cards.',
           (4, 'any five'): 'Q8 closed choose-five of nine printed terms: one card with an any-five group over all nine terms (choice is not a route).'}
assert [(o[0], o[2]) for o in observed] == list(classes), [(o[0], o[2]) for o in observed]
selection_ledger = dict(pattern=pattern, unclassified=0, sourceHashes=HASHES,
                        rows=[dict(page=o[0], start=o[1], match=o[2], context=o[3], classification=classes[(o[0], o[2])]) for o in observed],
                        finiteQuestionChoices={'8': dict(choose=5, options=[t[0] for t in TERMS], cardId=Q8['id'], groupRowId='terms',
                                                         wholeQuestionMarks=50, termMarks=10)})
whole = {}
for t in tasks:
    c = t['card']
    if '-complete' in c['id'] or c['id'] == Q8['id']:
        whole.setdefault(t['questionNumber'], []).append(dict(id=c['id'], parts=[g['label'] for g in c.get('taskGroups', [])] or ['any five of nine terms'], marks=c['totalMarks']))
taxonomy_gaps = [dict(cardId=Q8['id'], canonicalTopicIds=['cons-4-4'], atlasTopicId=CROSS + 'foundations-floors-walls',
                      reason='No Ordinary outgoing reference heading covers stairs (4.4, balusters); the term keeps the Foundations, Floors & Walls association of the reviewed reference topics.'),
                 dict(cardId=Q8['id'], canonicalTopicIds=['cons-10-1', 'cons-10-4'], atlasTopicId=CROSS + 'wood-rot-ventilation',
                      reason='No Ordinary outgoing reference heading covers joinery (10.1, 10.4, bridle joint); the term keeps the Wood, Rot & Ventilation association used for joinery.')]
REASONS = {
    'q1-a': 'Adds the four typical dimensions (4) and draughting/accuracy/scale (8/6/4) printed within part (a): 35 → 47.',
    'q1-b': 'Reshaped to the printed all-or-nothing row "Wall tie clearly identified" (0 or 3); tariff unchanged.',
    'q2-a': 'Split into the two printed reasons (6 each); total unchanged (12).',
    'q2-c': 'Reshaped to the printed note & sketch row (7 + 7); total unchanged (14).',
    'q3-a': 'Reshaped to the printed best-eight row (8 × 5); total unchanged (40).',
    'q3-b': 'Split into the two printed considerations (5 each); total unchanged (10).',
    'q4-a': 'Split into the two printed advantages (4 each); total unchanged (8).',
    'q4-b': 'Split into the five printed sketch & note rows (4 + 2 each); total unchanged (30).',
    'q5-a': 'Adds the draughting/accuracy/scale allowance (6/4/2) printed within part (a): 40 → 46.',
    'q5-b': 'Reshaped to the printed all-or-nothing row "Cavity closer" (0 or 4); tariff unchanged.',
    'q6-a': 'Split into the four printed rows, two precautions for each situation (4 each); total unchanged (16).',
    'q6-b': 'Split into the three printed precaution-and-reason rows (3 + 3 + 2 each); total unchanged (24).',
    'q6-c': 'Split into the two printed reasons (5 each); total unchanged (10).',
    'q7-a': 'Split into the two printed advantages (5 each); total unchanged (10).',
    'q7-b': 'Adds the printed sketch (8) to the four location-and-reason rows (3 + 2 each): 20 → 28.',
    'q9-a': 'Split into the printed material (4) and two reasons (4 each); total unchanged (12).',
    'q9-b': 'Split into the two printed modifications (notes + sketch 8 + 5 each); total unchanged (26).',
    'q9-c': 'Split into the two printed reasons (6 each); total unchanged (12).',
    Q8_KEPT: 'Now the whole of Question 8: one card printing all nine terms with an any-five group (10 each, 50), kept under this ID; the other eight per-term IDs alias to it (choice is not a route): 10 → 50.',
}
assert set(REASONS) | set(CONSOLIDATED) == {k.removeprefix(PREFIX) for k in LEGACY}
corrections = []
for t in tasks:
    c = t['card']
    if c['id'] in LEGACY:
        old = LEGACY[c['id']]
        assert old['conceptId'] == c['conceptId'], c['id']
        corrections.append(dict(cardId=c['id'], priorSha256=card_hash(old), correctedSha256=card_hash(c),
                                priorTotalMarks=old['totalMarks'], correctedTotalMarks=c['totalMarks'],
                                priorTopicId=old['topicId'], correctedTopicId=c['topicId'],
                                reason='Question wording lifted from the paper. ' + REASONS[c['id'].removeprefix(PREFIX)]))
assert len(corrections) == 19
consolidated = [dict(cardId=PREFIX + k, aliasOf=PREFIX + v, preCorrectionSha256=card_hash(LEGACY[PREFIX + k])) for k, v in CONSOLIDATED.items()]
out = dict(schemaVersion=1, subjectId='construction-studies', year=2023, level='ordinary', lang='ev', sitting='main', paperKey='single',
           fileid='LC029GLP000EV.pdf', component='theory', status='Q1–Q9 source-reviewed draft; integration pending.',
           sourceHashes=HASHES, tasks=tasks, bindings=bindings, questionFigures=question_figures,
           addedIds=[t['card']['id'] for t in tasks if not t['correction']], corrections=corrections, consolidatedLegacy=consolidated,
           selectionLedger=selection_ledger, questionRouteLedgers={q: dict(wholeRoutes=w) for q, w in whole.items()},
           taxonomyGaps=taxonomy_gaps, questionsReviewed=list(QUESTIONS), unreviewedQuestions=[])
(HERE / 'ordinary-2023-draft.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(tasks=len(tasks), added=len(out['addedIds']), corrected=len(corrections), consolidated=len(consolidated),
                      figures=len(question_figures), perQuestion={q: sum(1 for t in tasks if t['questionNumber'] == q) for q in QUESTIONS})))
