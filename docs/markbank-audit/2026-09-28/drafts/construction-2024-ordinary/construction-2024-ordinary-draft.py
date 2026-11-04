"""Draft the 2024 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Question wording and stems are lifted from the SEC paper (a narrowed task only deletes printed
words); every row's verbatim is printed in the scheme's mark tables (pages 16-24), checked against
rendered pages. Unbanded components accept any whole mark up to the published maximum; printed
excellent/good/fair bands are kept as printed. Sources are the byte-identical paper-trail-corpus
copies, pinned by SHA-256. Figures are exact 2x crops; the Q8 solution figure is a composite of the
three scheme pages that carry every term's notes and sketch.

The 25 pre-audit 2024 Ordinary cards: 17 keep their IDs (and concept IDs) and are corrected in place,
each correction recording the SHA-256 of the card it replaces. Q8 "any five of nine" is ONE card
(choice is not a route): it keeps the pre-audit site-planning-notice ID, and the other eight per-term
IDs are withdrawn into it through progress aliases. Every other prior card stays byte-identical.
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

P = 'paper-trail-corpus/exampapers/2024/LC029GLP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2024/LC029GLP000EV.pdf'
HASHES = {P: 'b9be60e59ed4af7f1674036721850d9dba68e1c2bc8e5cf26fc5a09b4511ba2a',
          S: '98af6f3b1e0b30be09b447f1bd61f1f3f6ce4a69dc89ac9dd56a505703d6a8f7'}
ATTRIBUTION = 'SEC Leaving Certificate Construction Studies 2024 Ordinary Level — © State Examinations Commission.'
FP = 'construction-studies-2024-OL-'
PREFIX = 'cons-2024-ol-'
CROSS = 'construction-studies-ordinary-'
BAND8 = [0, 4, 6, 8]
BAND6 = [0, 2, 4, 6]

for f, h in HASHES.items():
    assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f

# The pre-audit cards are snapshotted before integration so the draft regenerates byte-identically afterwards.
LEGACY_FILE = HERE / 'prior-2024-ordinary-cards.json'
if not LEGACY_FILE.exists():
    AUTHORED = json.loads((R / 'scripts/markbank/authored/construction-studies.json').read_text())
    LEGACY_FILE.write_text(json.dumps([c for c in AUTHORED if c['id'].startswith(PREFIX)], ensure_ascii=False, indent=2) + '\n')
LEGACY = {c['id']: c for c in json.loads(LEGACY_FILE.read_text())}
assert len(LEGACY) == 25, sorted(LEGACY)
Q8_KEPT = 'q8-None-site-planning-notice'
CONSOLIDATED = {f'q8-None-{t}': Q8_KEPT for t in ['gulley-trap', 'smart-lighting', 'halving-joint', 'cordless-drill', 'cavity-closer',
                                                  'faceplate-turning', 'plywood', 'heat-pump']}


def card_hash(c):
    return hashlib.sha256(json.dumps(c, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


FIGURES = {
    'q1-original': (P, 2, [45, 39, 580, 300], False), 'q2-original': (P, 2, [45, 307, 580, 549], False),
    'q3-original': (P, 2, [45, 556, 580, 767], False), 'q4-original': (P, 3, [45, 39, 580, 282], False),
    'q5-original': (P, 3, [45, 294, 580, 524], False), 'q6-original': (P, 3, [45, 524, 580, 761], False),
    'q7-original': (P, 4, [45, 39, 580, 351], False), 'q8-original': (P, 4, [45, 380, 580, 475], False),
    'q9-original': (P, 4, [45, 510, 580, 759], False),
    'q1-scheme': (S, 4, [51, 58, 568, 757], True),
    'q2-advantages': (S, 5, [58, 58, 525, 215], True), 'q2-method': (S, 5, [58, 220, 526, 585], True),
    'q2-reasons': (S, 5, [58, 593, 500, 796], True),
    'q3-system': (S, 6, [51, 58, 545, 565], True), 'q3-features': (S, 6, [51, 585, 513, 797], True),
    'q4-stone': (S, 7, [51, 58, 533, 230], True), 'q4-foundation': (S, 7, [51, 229, 547, 423], True),
    'q5-section': (S, 8, [51, 58, 531, 633], True), 'q5-drip': (S, 8, [51, 638, 536, 797], True),
    'q6-precautions': (S, 9, [51, 58, 545, 279], True), 'q6-ppe': (S, 9, [51, 283, 544, 600], True),
    'q6-training': (S, 9, [51, 605, 528, 786], True),
    'q7-layout': (S, 10, [51, 230, 529, 762], True),
    'q8-terms': construction_figures.composite([(S, 12, [51, 58, 544, 771]), (S, 13, [51, 58, 545, 700]), (S, 14, [51, 55, 543, 742])]),
    'q9-zinc': (S, 15, [50, 58, 539, 262], True), 'q9-modifications': (S, 15, [48, 262, 539, 649], True),
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
    '1': dict(page=2, title='Trussed-roof eaves and external wall section', concept='trussed-eaves-section',
              stem='The sketch shows portion of the eaves of a pitched roof constructed using prefabricated trussed rafters. The roof is supported on a 400 mm concrete block wall with a full-fill insulated cavity. The roof has a pitch of 30° and the trussed rafters are 200 mm × 40 mm. The slates are fixed to 50 mm × 30 mm battens, on a breather membrane. The roof is highly insulated at ceiling joist level.',
              note='Original sketch and specification retained. Construction details, dimensions and draughting belong to part (a); the wallplate detail in (b) is marked separately. Any alternative detailing that complies with current Building Regulations is acceptable.'),
    '2': dict(page=2, title='Improving a home’s Building Energy Rating', concept='ber-upgrade',
              stem='New homeowners wish to improve the Building Energy Rating (BER) of their home which was built over 30 years ago. The external wall is a concrete block wall with a partially insulated cavity. It is proposed to fix insulation to the inside surface of the external walls, and to install new windows.',
              note='Original question retained. The insulation method and type are open choices; the scheme lists typical examples.'),
    '3': dict(page=2, title='Bathroom hot and cold water supply', concept='bathroom-water-supply',
              stem='The sketch shows a bathroom with a shower area suitable for a person with limited mobility.',
              note='Original sketch retained. The listed components are required content, not a choice. The scheme diagram is one acceptable layout; any alternative that complies with current Building Regulations is acceptable.'),
    '4': dict(page=3, title='Entrance wall, strip foundation and driveway', concept='entrance-wall-foundation',
              stem='The sketch shows a front entrance wall and driveway under construction. The entrance wall is a 215 mm concrete block wall and is finished with 200 mm natural stone on one side.',
              note='Original sketch retained. All four printed items in (b) are required in one sketch; the driveway finish in (c) is an open choice.'),
    '5': dict(page=3, title='External wall and window cill section', concept='window-cill-section',
              stem='A triple glazed window with a wooden frame, is fixed in a 400 mm external block wall with a full-fill insulated cavity. The wall is rendered on both sides. The fixed frame of the window is 120 mm × 80 mm and is thermally broken.',
              note='Original specification retained. Construction details and draughting belong to part (a); the cill detail in (b) is marked separately.'),
    '6': dict(page=3, title='Site dumper safety and PPE', concept='site-dumper-safety',
              stem='The sketch shows a site dumper in operation on a construction site.',
              note='Original sketch retained. Precautions, PPE items and reasons are open responses; the scheme lists typical examples.'),
    '7': dict(page=4, title='Attic bedroom conversion', concept='attic-bedroom',
              stem='A draft design for an attic conversion to include a bedroom with an en suite bathroom is shown. The position of the stairs, en suite bathroom, and a door to the bedroom are included.',
              note='Original plan retained. All four printed items in (b) are required in one sketch; locations, reasons and the floor covering are open, well-reasoned responses.'),
    '8': dict(page=4, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=4, title='Zinc-clad family room extension', concept='zinc-family-room',
              stem='The sketch shows the rear of a modern semi-detached house with a family room extension. The walls and roof of the family room are finished externally with zinc cladding.',
              note='Original sketch retained. Reasons, modifications and advantages are open responses; the scheme lists typical examples.'),
}
SCHEME_PAGES = {'1': [4, 16], '2': [5, 17], '3': [6, 18], '4': [7, 19], '5': [8, 20], '6': [9, 21],
                '7': [10, 11, 22], '8': [12, 13, 14, 23], '9': [15, 24]}

tasks, bindings, cards = [], [], {}


def add(q, key, ref, text, rows, nodes, topics, figure, review, boundary, selection, groups=None):
    meta = QUESTIONS[q]
    cid = f'{PREFIX}q{q}-{key}'
    concept = LEGACY[cid]['conceptId'] if cid in LEGACY else f"{meta['concept']}-{key}"
    card = dict(id=cid, subjectId='construction-studies', year=2024, level='ordinary', section='B',
                topicId=nodes[0], conceptId=concept, questionRef=f'2024 OL Q{q}{ref}',
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
B1 = 'Scheme p16 (printed 14): (a) best 7 of 12 listed details × 5 = 35, any 3 typical dimensions 3, draughting/accuracy/scale 8 (8/6/4) = sub-total 11, both printed within part (a): 46; (b) wallplate strap clearly identified 4. Complete 50.'
S1 = 'One required section and one required wallplate detail. The best-seven detail list is a marking menu, not a printed choose-seven task.'
A1 = add('1', 'a', '(a)',
         'To a scale of 1:5, draw a vertical section through the external wall of the house and through the eaves of the trussed roof. On your drawing, show the typical construction details from a level 400 mm below the wallplate, through the wall and eaves of the roof. Include the first three courses of slate at eaves. Include three typical dimensions on your drawing.',
         [row('details', 'Any 7 x 5 marks', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: concrete block outer leaf with external render; full-fill cavity with wall tie; concrete block inner leaf with internal plaster; cavity closer; wallplate 100 mm × 75 mm; prefabricated roof truss; insulation and airtight membrane; plasterboard with skim coat; fascia, soffit and gutter; ventilation; breather membrane; slates and battens. The model specifies 19 mm render, 100 mm leaves, a 200 mm full-fill cavity, 15 mm plaster, a tilting fillet and 50 × 30 mm battens.', list(range(0, 36, 5))),
          row('dimensions', 'Any 3 typical dimensions', 3, 'Three appropriate typical dimensions on the section.'),
          row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the section: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-3-8', 'cons-3-10', 'cons-3-9', 'cons-3-3', 'cons-6-2'],
         ['question-one-drawing-questions', 'roofs', 'foundations-floors-walls', 'heat-loss-insulation'], 'q1-scheme',
         'Scaled drawing (1.5) of a trussed roof (3.8) at the eaves (3.10) with its covering and insulation (3.9) on a cavity wall (3.3) with an insulated cavity (6.2).', B1, S1)
B1b = add('1', 'b', '(b)', 'On your drawing, show how the wallplate is secured to the external wall.',
          [row('strap', 'Wallplate strap clearly identified', 4, 'Show and identify the wallplate strap fixing the wallplate down to the inner leaf, as in the scheme’s model section.', [0, 4])],
          ['cons-3-8', 'cons-3-10'], ['roofs'], 'q1-scheme', 'Securing the roof structure (3.8) at the eaves (3.10).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-scheme', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p17 (printed 15): (a) two advantages × 6 = 12; (b) method note & sketch 8 + 8 = 16, insulation type 4, thickness 4 = 24; (c) two reasons × 7 = 14. Complete 50.'
S2 = '"one suitable method" is an open choice with no printed list; each part stays one response.'
A2 = add('2', 'a', '(a)', 'Discuss two advantages of improving the Building Energy Rating (BER) of a home.',
         [row('advantage-1', 'Advantage 1', 6, 'Such as: reduced energy bills; less heat loss.'),
          row('advantage-2', 'Advantage 2', 6, 'A second, different advantage. Such as: increased comfort; the value of the home increases; better for the environment.')],
         ['cons-6-3', 'cons-6-2'], ['heat-loss-insulation'], 'q2-advantages', 'Running costs (6.3) and the insulated fabric (6.2).', B2, S2)
B2b = add('2', 'b', '(b)', 'Using notes and freehand sketches, show one suitable method of applying insulation to the internal surface of the walls. Show on your sketch how the wall is to be finished internally. Specify the type and thickness of insulation.',
          [row('method', 'Method of insulating external walls note & sketch (8 + 8 marks)', 16, 'Note 8 and sketch 8 of one method, showing the internal finish. Such as: clean the wall of wallpaper or gloss paint, cut insulated plasterboard to size and fix it with mechanical fixings (adhesive dabs may also be used), then skim with plaster or tape and fill; or fix timber battens to the wall, fill between them with insulation, then fix plasterboard to the battens and skim.'),
           row('type', 'Preferred insulation type for external wall', 4, 'Such as: expanded polystyrene (EPS), phenolic, polyisocyanurate (PIR) or extruded polystyrene (XPS); the method notes also name wood fibre and sheep’s wool.'),
           row('thickness', 'Thickness of insulation', 4, 'At least 50 mm of insulation.')],
          ['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q2-method', 'Insulating materials (6.2) applied to an external wall (3.3).', B2, S2)
C2 = add('2', 'c', '(c)', 'Discuss two reasons why external wall and window upgrades should be carried out at the same time.',
         [row('reason-1', 'Reason 1', 7, 'Such as: a more complete finish with better airtightness; more cost-effective to carry out several upgrades together.'),
          row('reason-2', 'Reason 2', 7, 'A second, different reason. Such as: greater comfort; lower energy use and carbon emissions; less disruption for the homeowner; additional grants for multiple upgrades.')],
         ['cons-6-2', 'cons-3-5'], ['heat-loss-insulation', 'windows-doors'], 'q2-reasons', 'Upgrading the insulated fabric (6.2) and the windows (3.5) together.', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-method', B2, S2, parts(A2, B2b, C2))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p18 (printed 16): (a) best 8 of 12 listed items × 5 = 40; (b) two features × 5 = 10. Complete 50.'
S3 = 'The printed component list is required content, not a choice; the best-eight list is a marking menu.'
A3 = add('3', 'a', '(a)', 'Using a single-line labelled sketch, show the pipework required to provide hot and cold water to a mixer-shower and wash basin, and to provide cold water to a toilet cistern. Include the following in your sketch: rising main; insulated cold water storage tank; hot water cylinder; pipework to bathroom fixtures; all necessary valves.',
         [row('details', 'Any 8 x 5 marks', 40, 'Credit the best EIGHT acceptable items at 5 marks each, capped at 40. Marked items: rising main; insulated storage tank; overflow; cylinder; cold feed to cylinder; expansion pipe; bathroom fixtures; cold feed to toilet cistern; hot and cold feed to wash basin; hot and cold feed to mixer shower; valves; labels. Typical sizes: 15 mm rising main, 250 l cylinder, Ø22 mm cold feed to the cylinder, Ø28 mm expansion pipe, Ø15 mm feeds to the cistern, basin and shower.', list(range(0, 41, 5)))],
         ['cons-5-2', 'cons-5-6'], ['hot-water-space-heating', 'drainage'], 'q3-system', 'Hot and cold water supply (5.2) to the sanitary fitments (5.6).', B3, S3)
B3b = add('3', 'b', '(b)', 'Discuss two features that should be included to ensure a shower area is suitable for a person with limited mobility.',
          [row('feature-1', 'Feature 1', 5, 'Such as: safe, comfortable access; a large shower area; a non-slip shower area without a step.'),
           row('feature-2', 'Feature 2', 5, 'A second, different feature. Such as: a curtain or screen instead of doors; a wall-mounted folding seat; controls within easy reach, preferably lever taps; grab rails.')],
          ['cons-5-6', 'cons-1-2'], ['drainage', 'planning-sustainability-environment'], 'q3-features', 'Accessible sanitary fitments (5.6) in the built environment (1.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-system', B3, S3, parts(A3, B3b))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p19 (printed 17): (a) two advantages × 6 = 12; (b) strip foundation, steel reinforcement and position of wall, each sketch 4 + note 2, and typical dimensions 3 + 3 = 24; (c) suitable material 6, two reasons × 4 = 14. Complete 50.'
S4 = 'All four printed items in (b) are required in one sketch, not a choice. The driveway finish in (c) is an open choice with no printed list.'
A4 = add('4', 'a', '(a)', 'Discuss two advantages of choosing a natural stone finish for an entrance wall.',
         [row('advantage-1', 'Advantage 1', 6, 'Such as: an attractive finish; it helps the wall blend in with the natural landscape; durable, hardwearing material.'),
          row('advantage-2', 'Advantage 2', 6, 'A second, different advantage. Such as: very low maintenance; sourced locally with low embodied energy; keeps stone masonry, an important heritage craft skill, alive.')],
         ['cons-3-3', 'cons-1-2'], ['foundations-floors-walls', 'planning-sustainability-environment'], 'q4-stone', 'A stone-faced wall (3.3) in its landscape (1.2).', B4, S4)
B4b = add('4', 'b', '(b)', 'Using notes and freehand sketches, show the typical design detailing of the strip foundation for this wall. Include the following in your sketch: strip foundation; steel reinforcement; position of wall on foundation; typical dimensions of the foundation.',
          [row('foundation', 'Strip foundation sketch & note (4 + 2 marks)', 6, 'Sketch 4 and note 2. Such as: a strip foundation, the most common and suitable foundation for a boundary wall, usually three times wider than the wall, with the load spread at 45°.'),
           row('reinforcement', 'Steel reinforcement sketch & note (4 + 2 marks)', 6, 'Sketch 4 and note 2. Such as: steel reinforcement at the bottom of the foundation for tensile strength, with at least 50 mm of concrete cover.'),
           row('position', 'Position of wall sketch & note (4 + 2 marks)', 6, 'Sketch 4 and note 2. Such as: the wall built on the centre of the foundation.'),
           row('dimensions', 'Typical dimensions (3 + 3 marks)', 6, 'Two typical dimensions, 3 each. Such as: a 1350 mm × 450 mm foundation for a 450 mm wall.')],
          ['cons-2-4', 'cons-2-2'], ['foundations-floors-walls'], 'q4-foundation', 'Strip foundations (2.4) and the choice of foundation (2.2).', B4, S4)
C4 = add('4', 'c', '(c)', 'Specify a suitable surface finish for the driveway, and give two reasons for your choice.',
         [row('material', 'Suitable material', 6, 'Such as: tarmac, concrete, gravel/ornamental stone, block paving or resin.'),
          row('reason-1', 'Reason 1', 4, 'A reason matching the chosen finish. Such as, tarmac: attractive, durable, low maintenance, long lasting; concrete: long life span, low maintenance, recyclable.'),
          row('reason-2', 'Reason 2', 4, 'A second, different reason. Such as, gravel: cheaper and blends with a rural landscape; block paving: modern, easy to repair, more colour choice; resin: modern, low maintenance, long lasting.')],
         ['cons-1-2'], ['planning-sustainability-environment'], None, 'External works in the built environment (1.2).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-foundation', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p20 (printed 18): (a) best 8 of 11 listed details × 5 = 40, draughting/accuracy/dimensions/scale 6 (6/4/2), both printed within part (a): 46; (b) DPC and drip 4. Complete 50.'
S5 = 'One required section and one required cill detail. The best-eight detail list is a marking menu, not a printed choose-eight task.'
A5 = add('5', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the external wall and the bottom of the window. Show the typical construction details from a level 400 mm below, to a level 300 mm above, the concrete window cill. Include three typical dimensions on your drawing.',
         [row('details', 'Any 8 x 5 marks', 40, 'Credit the best EIGHT acceptable details at 5 marks each, capped at 40. Marked details: concrete block outer leaf with external render; full-fill insulated cavity with wall tie; concrete block inner leaf with internal plaster; cavity closer; concrete cill; drip/throating; DPC; thermally broken window frame; triple glazing; airtightness; window board. The model specifies 19 mm render, 100 mm leaves, a 200 mm cavity, 15 mm plaster and a 120 × 80 mm frame.', list(range(0, 41, 5))),
          row('presentation', 'Draughting, accuracy, dimensions and scale (excellent, good, fair)', 6, 'Draughting, accuracy, dimensions and scale of the section: excellent 6, good 4, fair 2.', BAND6)],
         ['cons-1-5', 'cons-3-3', 'cons-3-6', 'cons-3-4'], ['question-one-drawing-questions', 'foundations-floors-walls', 'windows-doors'], 'q5-section',
         'Scaled drawing (1.5) of a cavity wall (3.3) at the window cill (3.6) with its DPC (3.4).', B5, S5)
B5b = add('5', 'b', '(b)', 'On your drawing show how to prevent moisture penetration at the window cill.',
          [row('dpc-drip', 'DPC and drip', 4, 'Show and identify the DPC under the cill and the drip (throating) on its underside, as in the scheme’s model detail. Any other suitable detail is accepted.', [0, 4])],
          ['cons-3-6', 'cons-3-4'], ['windows-doors', 'foundations-floors-walls'], 'q5-drip', 'The window cill (3.6) and its damp proof course (3.4).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-section', B5, S5, parts(A5, B5b))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p21 (printed 19): (a) two safety precautions × 6 = 12; (b) three PPE items, each item 5 + specific reason 3 = 24; (c) two reasons × 7 = 14. Complete 50.'
S6 = 'Precautions, PPE items and reasons are open responses with no printed list; the scheme lists typical examples.'
A6 = add('6', 'a', '(a)', 'Describe two safety precautions that the driver must observe when operating a site dumper.',
         [row('precaution-1', 'Safety precaution 1', 6, 'Such as: wear suitable PPE (hard hat, steel-toe boots, hi-visibility clothing); inspect the vehicle before use; always wear the seatbelt; check the area for obstacles, holes or overhead power lines.'),
          row('precaution-2', 'Safety precaution 2', 6, 'A second, different precaution. Such as: cordon off the area where the dumper operates; be trained in its use; never jump on or off — three points of contact; stay vigilant of the surroundings and others.')],
         ['cons-1-8'], ['site-safety'], 'q6-precautions', 'Safety precautions on site (1.8).', B6, S6)
B6b = add('6', 'b', '(b)', 'Using notes and freehand sketches, show three items of personal protective equipment (PPE) which should be worn by workers when working with construction vehicles. Give one specific reason why each item of personal protective equipment must be worn.',
          [row(f'ppe-{i}', f'Item of PPE {i} and specific reason (5 + 3 marks)', 8, note) for i, note in [
              (1, 'Item 5 and specific reason 3. Such as: a hard hat, protecting the head from impacts or falling material.'),
              (2, 'A second, different item: 5 + 3. Such as: a high-visibility vest, so vehicle operators see workers and avoid accidents.'),
              (3, 'A third, different item: 5 + 3. Such as: ear defenders against machinery noise; safety glasses against flying debris; safety boots against dropped heavy materials.')]],
          ['cons-1-8'], ['site-safety'], 'q6-ppe', 'Personal protective equipment (1.8).', B6, S6)
C6 = add('6', 'c', '(c)', 'Give two reasons why vehicle operators must undertake a specific training course prior to operating a vehicle on a construction site.',
         [row('reason-1', 'Reason 1', 7, 'Such as: regulations require specific certifications or licences; training teaches safety protocols, reducing accidents.'),
          row('reason-2', 'Reason 2', 7, 'A second, different reason. Such as: the knowledge to operate the equipment effectively; identifying and mitigating risks; greater efficiency; proper maintenance that extends the vehicle’s life.')],
         ['cons-1-8'], ['site-safety'], 'q6-training', 'Safety precautions on site (1.8).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-ppe', B6, S6, parts(A6, B6b, C6))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p22 (printed 20): (a) two advantages × 5 = 10; (b) sketch 8 and four items, each location 3 + reason 2 = 5, = 28; (c) floor covering 4 and two reasons × 4 = 12. Complete 50.'
S7 = 'All four printed items in (b) are required in one sketch, not a choice. The floor covering in (c) is an open choice with no printed list.'
A7 = add('7', 'a', '(a)', 'Discuss two advantages of converting an attic space into a bedroom.',
         [row('advantage-1', 'Advantage 1', 5, 'Such as: a cost-effective way of adding living space; an extra bedroom; increases the value of the home.'),
          row('advantage-2', 'Advantage 2', 5, 'A second, different advantage. Such as: versatility for other uses; no need to extend the house; better sound separation from living spaces; the chance to insulate the roof to a higher standard.')],
         ['cons-1-2', 'cons-3-9'], ['planning-sustainability-environment', 'roofs'], None, 'Adapting a dwelling (1.2) within its roof (3.9).', B7, S7)
B7b = add('7', 'b', '(b)', 'Draw a large freehand sketch of the given design and show your preferred location for each of the following in the attic bedroom: access to en suite; double bed; clothes storage unit; study space. Give one reason for selecting each location.',
          [row('sketch', 'Sketch', 8, 'A large freehand sketch of the given attic design.'),
           row('access', 'Location and valid reason for access to en suite (3 + 2 marks)', 5, 'Location 3 and reason 2. Such as: beside the shower, giving more room inside the en suite and more bedroom wall space, or opposite the sink for privacy from the bed.'),
           row('bed', 'Location and valid reason for double bed (3 + 2 marks)', 5, 'Location 3 and reason 2. Such as: against a wall with room for bedside tables, near sockets and the light switch, away from the eaves for head height.'),
           row('storage', 'Location and valid reason for clothes storage unit (3 + 2 marks)', 5, 'Location 3 and reason 2. Such as: against a wall to leave space around the bed and fix the unit securely, or in an alcove to use underused space.'),
           row('study', 'Location and valid reason for study space (3 + 2 marks)', 5, 'Location 3 and reason 2. Such as: away from the bed as a separate zone, out of the corner for good light, or in an alcove.')],
          ['cons-1-2'], ['planning-sustainability-environment'], 'q7-layout', 'Layout design within the built environment (1.2).', B7, S7)
C7 = add('7', 'c', '(c)', 'Specify a suitable floor covering for the bedroom and give two reasons for your choice.',
         [row('covering', 'Suitable floor covering', 4, 'Such as: carpet, wood laminate, vinyl, solid wood or linoleum.'),
          row('reason-1', 'Reason 1', 4, 'A reason matching the covering. Such as, carpet: comfortable and absorbs sound; laminate: durable and less expensive.'),
          row('reason-2', 'Reason 2', 4, 'A second, different reason. Such as, vinyl: easy to install and water resistant; solid wood: attractive and can be sanded and refinished; linoleum: hardwearing and waterproof.')],
         ['cons-4-3', 'cons-1-2'], ['foundations-floors-walls', 'planning-sustainability-environment'], None, 'An upper-floor finish (4.3) chosen for the room (1.2).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-layout', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p23 (printed 21): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination. It keeps the pre-audit site-planning-notice ID; the other eight per-term IDs alias to it.'
TERMS = [
    ('site-planning-notice', 'site planning notice', 'Site planning notice', ['cons-1-3'], ['planning-sustainability-environment'],
     'a public notice the applicant erects at the site when applying for planning permission, clearly visible and legible from the road, giving the applicant’s name, site address, type of application and nature of the development; required by planning regulations so the public can make observations or objections; in place for the first five weeks after lodgement, or the application may be invalid.',
     'Planning permission (1.3).'),
    ('halving-joint', 'halving joint', 'Halving joint', ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'],
     'a common, strong woodworking joint with a medium gluing area, made by removing half the material from each piece at the joint; cross, corner, T- or dovetail halving; used in framing and furniture.',
     'Joints (10.1) and the choice of joint (10.4). The Ordinary reference taxonomy has no joinery heading; the term keeps the Wood, Rot & Ventilation association used for joinery, and 10.1/10.4 are declared outside that heading’s crosswalk.'),
    ('faceplate-turning', 'faceplate turning', 'Faceplate turning', ['cons-9-2', 'cons-10-7'], ['wood-rot-ventilation'],
     'a woodturning method for large, flat circular items such as bowls and plates; the work piece is mounted on a faceplate on the headstock of the lathe; the tool rest supports the chisel; start slowly until the piece is balanced, then increase the speed.',
     'Workshop equipment and its use (9.2) and surface finishing (10.7). The Ordinary reference taxonomy has no tools heading; 9.2 is declared outside the crosswalk.'),
    ('smart-lighting', 'smart lighting', 'Smart lighting', ['cons-5-8'], ['services-water-gas-electrical'],
     'lighting controlled remotely, often automatically, through a smartphone, tablet or voice commands over the internet; scheduling and timers; customised colour, brightness and ambiance; contributes to energy savings.',
     'Domestic electrical installation (5.8).'),
    ('cordless-drill', 'cordless drill', 'Cordless drill', ['cons-9-2'], ['wood-rot-ventilation'],
     'a portable power tool for drilling holes and driving screws, powered by rechargeable (usually lithium-ion) batteries; more convenient and versatile than a corded drill and usable where there is no power source; features such as an LED light and battery indicator.',
     'Power tools (9.2). The Ordinary reference taxonomy has no tools heading; as in the reviewed 2024 reference topics for this question, the term keeps the Wood, Rot & Ventilation association used for tools and craft, and 9.2 is declared outside that heading’s crosswalk.'),
    ('plywood', 'plywood', 'Plywood', ['cons-10-3'], ['wood-rot-ventilation'],
     'an engineered panel of thin wood veneers glued with the grain of each layer perpendicular to the next for strength; used in construction, furniture and cabinet-making; a strong, relatively low-cost alternative to solid wood; marine plywood for high-moisture use.',
     'Manufactured boards (10.3).'),
    ('gulley-trap', 'gulley trap', 'Gulley trap', ['cons-5-5'], ['drainage'],
     'a fitting in foul and rainwater drainage with a U-bend that holds water as a seal against sewer gases and odours entering the building; typically underground; needs regular maintenance.',
     'Underground drainage (5.5).'),
    ('cavity-closer', 'cavity closer', 'Cavity closer', ['cons-3-3', 'cons-6-2', 'cons-6-6'], ['foundations-floors-walls', 'heat-loss-insulation', 'air-tightness-condensation'],
     'closes the gap between the leaves of a cavity wall at wallplate level and around window and door openings; prevents thermal bridging, damp penetration, air infiltration and condensation; insulating foam or rigid board, 100–150 mm wide to suit the cavity.',
     'Cavity walls (3.3), thermal bridges (6.2) and condensation (6.6).'),
    ('heat-pump', 'heat pump', 'Heat pump', ['cons-5-3'], ['hot-water-space-heating'],
     'a device transferring heat from the air, water or ground into the home, distributed by underfloor heating or radiators; runs on electricity with a coefficient of performance of about 3–4; grants encourage the change from fossil-fuel heating.',
     'Heating systems (5.3).'),
]
Q8 = add('8', 'None-site-planning-notice', '', 'Explain, with the aid of notes and freehand sketches, any five of the following: ' + '; '.join(t[1] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Construction Terms', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{t[2]}: {t[5]}' for t in TERMS),
               group=dict(claimMax=5, perOption=10, options=[t[2] for t in TERMS]))],
         list(dict.fromkeys(n for t in TERMS for n in t[3])), list(dict.fromkeys(a for t in TERMS for a in t[4])), 'q8-terms',
         'The union of the nine printed terms: ' + ' '.join(t[6] for t in TERMS), B8, S8)

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p24 (printed 22): (a) two reasons × 6 = 12; (b) two modifications, each sketch 8 + notes 5 = 13, = 26; (c) two advantages × 6 = 12. Complete 50.'
S9 = 'Both printed purposes in (b) are served by the two modifications the scheme marks as Modification 1 and 2; reasons, modifications and advantages are open responses.'
A9 = add('9', 'a', '(a)', 'Discuss two reasons why zinc is a suitable cladding material for modern homes.',
         [row('reason-1', 'Reason 1', 6, 'Such as: a modern, attractive appearance; highly durable with a long lifespan.'),
          row('reason-2', 'Reason 2', 6, 'A second, different reason. Such as: minimal maintenance; sustainable and recyclable; non-combustible and corrosion resistant.')],
         ['cons-3-9', 'cons-1-2'], ['roofs', 'planning-sustainability-environment'], 'q9-zinc', 'Roof and wall coverings (3.9) in modern design (1.2).', B9, S9)
B9b = add('9', 'b', '(b)', 'Using notes and freehand sketches, show two modifications to the family room that would allow for the following: additional natural light; access to the rear garden.',
          [row('modification-1', 'Modification 1 (light/access) sketch + notes (8 + 5 marks )', 13, 'Sketch 8 and notes 5. Such as: roof lights; larger windows at the rear.'),
           row('modification-2', 'Modification 2 (light/access) sketch + notes (8 + 5 marks )', 13, 'Sketch 8 and notes 5 for a second, different modification. Such as: additional side or rear windows; a large glazed door; a large bi-fold or sliding door to the garden.')],
          ['cons-3-5', 'cons-3-7', 'cons-1-2'], ['windows-doors', 'planning-sustainability-environment'], 'q9-modifications',
          'Windows (3.5) and external doors (3.7) in the built environment (1.2).', B9, S9)
C9 = add('9', 'c', '(c)', 'Discuss two advantages of providing access to the rear garden from the family room for the occupants of the house.',
         [row('advantage-1', 'Advantage 1', 6, 'Such as: more usable space; a connection with nature that can improve mood and wellbeing.'),
          row('advantage-2', 'Advantage 2', 6, 'A second, different advantage. Such as: an outdoor living space; encourages use of the outdoors; increases resale value.')],
         ['cons-1-2'], ['planning-sustainability-environment'], None, 'Use of the outdoor built environment (1.2).', B9, S9)
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
taxonomy_gaps = [dict(cardId=Q8['id'], canonicalTopicIds=['cons-10-1', 'cons-10-4', 'cons-9-2'], atlasTopicId=CROSS + 'wood-rot-ventilation',
                      reason='No Ordinary outgoing reference heading covers joinery (10.1, 10.4, halving joint) or workshop tools (9.2, faceplate turning and cordless drill).')]
REASONS = {
    'q1-a': 'Adds the three typical dimensions (3) and draughting/accuracy/scale (8/6/4) printed within part (a): 35 → 46.',
    'q1-b': 'Reshaped to the printed all-or-nothing row "Wallplate strap clearly identified" (0 or 4); tariff unchanged.',
    'q2-a': 'Split into the two printed advantages (6 each); total unchanged (12).',
    'q2-c': 'Split into the two printed reasons (7 each); total unchanged (14).',
    'q3-a': 'Reshaped to the printed best-eight row (8 × 5); total unchanged (40).',
    'q3-b': 'Split into the two printed features (5 each); total unchanged (10).',
    'q4-a': 'Split into the two printed advantages (6 each); total unchanged (12).',
    'q4-b': 'Split into the four printed sketch-and-note rows (strip foundation, reinforcement, wall position, dimensions); total unchanged (24).',
    'q5-b': 'Reshaped to the printed all-or-nothing row "DPC and drip" (0 or 4); tariff unchanged.',
    'q6-a': 'Split into the two printed safety precautions (6 each); total unchanged (12).',
    'q6-b': 'Split into three PPE items, each item 5 + specific reason 3; total unchanged (24).',
    'q6-c': 'Split into the two printed reasons (7 each); total unchanged (14).',
    'q7-a': 'Split into the two printed advantages (5 each); total unchanged (10).',
    'q7-b': 'Adds the printed sketch (8) to the four location-and-reason rows (3 + 2 each): 20 → 28.',
    'q9-b': 'Split into the two printed modifications (sketch 8 + notes 5 each); total unchanged (26).',
    'q9-c': 'Split into the two printed advantages (6 each); total unchanged (12).',
    Q8_KEPT: 'Now the whole of Question 8: one card printing all nine terms with an any-five group (10 each, 50), kept under this ID; the other eight per-term IDs alias to it (choice is not a route): 10 → 50.',
}
assert set(REASONS) | set(CONSOLIDATED) == {k.removeprefix(PREFIX) for k in LEGACY}
corrections = []
for t in tasks:
    c = t['card']
    if c['id'] in LEGACY:
        old = LEGACY[c['id']]
        corrections.append(dict(cardId=c['id'], priorSha256=card_hash(old), correctedSha256=card_hash(c),
                                priorTotalMarks=old['totalMarks'], correctedTotalMarks=c['totalMarks'],
                                priorTopicId=old['topicId'], correctedTopicId=c['topicId'],
                                reason='Question wording lifted from the paper. ' + REASONS[c['id'].removeprefix(PREFIX)]))
assert len(corrections) == 17
consolidated = [dict(cardId=PREFIX + k, aliasOf=PREFIX + v, preCorrectionSha256=card_hash(LEGACY[PREFIX + k])) for k, v in CONSOLIDATED.items()]
out = dict(schemaVersion=1, subjectId='construction-studies', year=2024, level='ordinary', lang='ev', sitting='main', paperKey='single',
           fileid='LC029GLP000EV.pdf', component='theory', status='Q1–Q9 source-reviewed draft; integration pending.',
           sourceHashes=HASHES, tasks=tasks, bindings=bindings, questionFigures=question_figures,
           addedIds=[t['card']['id'] for t in tasks if not t['correction']], corrections=corrections, consolidatedLegacy=consolidated,
           selectionLedger=selection_ledger, questionRouteLedgers={q: dict(wholeRoutes=w) for q, w in whole.items()},
           taxonomyGaps=taxonomy_gaps, questionsReviewed=list(QUESTIONS), unreviewedQuestions=[])
(HERE / 'ordinary-2024-draft.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(tasks=len(tasks), added=len(out['addedIds']), corrected=len(corrections), consolidated=len(consolidated),
                      figures=len(question_figures), perQuestion={q: sum(1 for t in tasks if t['questionNumber'] == q) for q in QUESTIONS})))
