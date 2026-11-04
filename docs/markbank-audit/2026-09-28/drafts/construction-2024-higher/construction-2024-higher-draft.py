"""Draft the 2024 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Question wording is lifted from the SEC paper: a narrowed task only deletes printed words, and a task
named only by reference to a printed list carries the scheme's own heading after ' — '. Every row's
verbatim is printed in the scheme's mark tables (pages 36-46) or model pages, checked against rendered
pages. Unbanded components accept any whole mark up to the published maximum; the printed
excellent/good/fair drafting band is kept as printed. Figures are exact 2x crops of the original PDFs;
a solution figure spanning several scheme pages is a composite of exact page crops.

The printed choice Q10(a) (any two of three) is ONE card with an anyN group (choice is not a route);
Q4(b) "select your preferred site" is one task, the scheme marking either site with the same rows.
The 22 pre-audit 2024 Higher cards keep their IDs and concept IDs and are corrected in place; each
correction records the SHA-256 of the card it replaces.
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

P = 'paper-trail-corpus/exampapers/2024/LC029ALP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2024/LC029ALP000EV.pdf'
HASHES = {P: 'a236712dcac010ce50b394d73de5ebe0683267809ab53bca86e8678987966aeb',
          S: 'e3359c9c16e5e5e3fa55e04f64df714d982d4872cda62bcefd667250b0a89887'}
for f, h in HASHES.items():
    assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f
ATTRIBUTION = 'SEC Leaving Certificate Construction Studies 2024 Higher Level — © State Examinations Commission.'
FP = 'construction-studies-2024-HL-'
PREFIX = 'cons-2024-hl-'
CROSS = 'construction-studies-higher-'
BAND8 = [0, 4, 6, 8]

# The pre-audit cards are snapshotted before integration so the draft regenerates byte-identically afterwards.
LEGACY_FILE = HERE / 'prior-2024-higher-cards.json'
if not LEGACY_FILE.exists():
    AUTHORED = json.loads((R / 'scripts/markbank/authored/construction-studies.json').read_text())
    LEGACY_FILE.write_text(json.dumps([c for c in AUTHORED if c['id'].startswith(PREFIX)], ensure_ascii=False, indent=2) + '\n')
LEGACY = {c['id']: c for c in json.loads(LEGACY_FILE.read_text())}
assert len(LEGACY) == 22, sorted(LEGACY)


def card_hash(c):
    return hashlib.sha256(json.dumps(c, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def composite(*panels):
    return construction_figures.composite([(S, p, r) for p, r in panels])


FIGURES = {
    'q1-original': (P, 2, [45, 53, 580, 375], False),
    'q1-section': (S, 4, [50, 51, 552, 760], True),
    'q1-ventilation': (S, 5, [51, 506, 531, 796], True),
    'q2-original': (P, 2, [45, 390, 580, 762], False),
    'q2-guidelines': composite((6, [51, 51, 546, 778]), (7, [51, 50, 539, 593])),
    'q2-layouts': (S, 8, [51, 50, 543, 792], True),
    'q2-justify': (S, 9, [51, 50, 545, 794], True),
    'q3-original': (P, 3, [45, 53, 580, 411], False),
    'q3-layout': composite((10, [51, 51, 545, 591]), (11, [51, 60, 545, 587])),
    'q3-external': composite((11, [51, 591, 545, 761]), (12, [51, 50, 547, 590])),
    'q4-original': (P, 3, [45, 431, 580, 731], False),
    'q4-sites': (S, 14, [51, 50, 539, 800], True),
    'q4-site-plans': (S, 15, [51, 50, 535, 715], True),
    'q5-original': (P, 4, [45, 48, 580, 735], False),
    'q5-calculation': (S, 16, [51, 51, 540, 791], True),
    'q6-original': (P, 5, [45, 51, 580, 423], False),
    'q6-low-impact': (S, 18, [51, 51, 549, 725], True),
    'q6-features': (S, 19, [51, 50, 546, 739], True),
    'q7-original': (P, 5, [45, 430, 580, 740], False),
    'q7-section': (S, 21, [51, 51, 527, 801], True),
    'q7-airtightness': (S, 22, [51, 71, 509, 381], True),
    'q8-original': (P, 6, [45, 53, 580, 402], False),
    'q8-system': (S, 23, [51, 51, 545, 743], True),
    'q8-renewables': (S, 24, [51, 50, 544, 789], True),
    'q9-original': (P, 6, [45, 434, 580, 722], False),
    'q9-requirements': (S, 26, [51, 51, 545, 644], True),
    'q9-sound': (S, 27, [51, 50, 543, 789], True),
    'q10-original': (P, 7, [45, 53, 580, 399], False),
    'q10-items': composite((29, [51, 51, 544, 789]), (30, [51, 50, 543, 728])),
    'q10-upgrade': (S, 31, [51, 50, 543, 791], True),
    'q10-scheme': composite((29, [51, 51, 544, 789]), (30, [51, 50, 543, 728]), (31, [51, 50, 543, 791])),
    'q10-alt-original': (P, 7, [45, 465, 580, 702], False),
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
    '1': dict(page=2, title='Lean-to porch roof and wall section', concept='entrance-porch-section',
              stem='An entrance porch with a lean-to roof projects 1.8 metres from the external wall of a house. The walls of the porch and of the house are of 450 mm concrete block construction with a full-fill insulated cavity. The external wall of the porch is finished with a rainscreen of 20 mm vertical larch cladding. The highly insulated lean-to roof has a pitch of 30° with a slate finish. The rafters are 200 mm × 50 mm with insulated plasterboard fixed to the underside of the sloping rafters.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the ventilation detail in (b) is marked separately.'),
    '2': dict(page=2, title='Designing a house for lifetime use', concept='lifetime-use-design',
              stem='The design of a house should be flexible to meet the changing needs of the occupants over their lifetime.',
              note='Original question and draft bedroom plan retained. Both areas in (a) and all five items in (b) and (c) are required. The scheme shows two model en suite layouts; any well-reasoned layout is acceptable.'),
    '3': dict(page=3, title='Converting a disused forge', concept='forge-renovation',
              stem='The drawing shows the front elevation and ground floor plan of a house with an adjoining disused forge. The forge was built using natural local stone with a red corrugated steel pitched roof. The wall A-A is south facing and the wall B-B has views to the mountains. The owners intend to convert the forge into an open-plan kitchen/dining and living space. Consideration at the design stage is to be given to: linking the existing kitchen to the forge; optimising natural daylight; maximising the views to the mountains.',
              note='Original elevation and plan retained. All three design considerations are required in one layout. The scheme’s sketches are examples, not required designs.'),
    '4': dict(page=3, title='Planning control and choosing a site', concept='site-selection-and-layout', stem='',
              note='Original site location map retained. In (b) the candidate selects site A or B and the same three considerations are marked either way; (c) sketches the selected site.'),
    '5': dict(page=4, title='ICF wall U-value, heat-loss cost and wood pellet heating', concept='icf-wall-heat-loss',
              stem='The sketch shows a proposed external wall design for a new house. The external wall is constructed using Insulated Concrete Formwork (ICF).',
              note='All printed data are retained in the original question. Part (b) uses the U-value from (a); the scheme’s worked answers are U = 0.142 W/m²°C and an annual cost of €31.71.'),
    '6': dict(page=5, title='Low environmental impact urban house', concept='energy-efficient-urban-house',
              stem='The elevation and ground floor plan of a house constructed in an urban area are shown. The external walls are of timber frame construction with a rendered concrete block and brick finish. Space heating is provided using a renewable heat source. The house was designed to be energy-efficient and to have a low environmental impact.',
              note='Original elevation and plan retained. Features, added features and advantages are open responses; the scheme lists typical examples.'),
    '7': dict(page=5, title='Timber-frame wall, window head and first-floor section', concept='window-head-first-floor-section',
              stem='A window is fitted in the external wall of a two-storey dwelling house. The thermally broken window frame is 120 mm × 70 mm. The wall is of timber frame construction with an external rendered concrete block leaf. The internal timber frame leaf is 250 mm × 50 mm and has a 50 mm service cavity provided at the internal surface. The wall supports the first floor joists. The first floor is a 25 mm hardwood tongued and grooved floor, on a 20 mm OSB deck, on 225 mm × 50 mm wooden joists, with a plasterboard ceiling beneath.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the airtightness detail in (b) is marked separately.'),
    '8': dict(page=6, title='Wood-burning stove: hot water and zoned heating', concept='stove-heating-layout',
              stem='The sketch shows a wood burning stove used to provide hot water and central heating for a two-storey house.',
              note='Original sketch retained. The scheme’s system diagram is an exam model; the renewable method in (b) is an open choice.'),
    '9': dict(page=6, title='Attic home office and sound insulation', concept='attic-office-sound',
              stem='Homeowners wish to convert an existing attic space into a home office. They wish to carry out refurbishment works to reduce the level of sound transmission between the proposed office in the attic and the rooms beneath.',
              note='Original sketch retained. Part (b) requires both the floor and the stud wall, each separately marked. Requirements and approaches are open responses.'),
    '10': dict(page=7, title='EnerPHit retrofit of a bungalow', concept='enerphit-retrofit',
               stem='The sketch shows a bungalow which has been retrofitted. The owners have engaged skilled labour in the upgrade of their bungalow to meet the EnerPHit Passive House design standard.',
               note='Original sketch retained. Part (a) chooses any two of three printed items, each keeping its own 12 marks; part (b) requires both printed items.'),
}
ALT = dict(page=7, title='Buildings across their lifecycle (alternative Question 10)', concept='whole-life-carbon',
           stem='“Buildings have an impact on the environment at every stage of their lifecycle. Materials have to be quarried, mined or harvested, transported to factories and manufactured. The final products have to be transported to site, lifted into place and fixed in position. The buildings have to be operated, heated and cooled. Over a 60 year life cycle, components fail, roof finishes fail and need replacement, finishes spoil and need repainting and replacement. Eventually the building ceases to provide its function and needs to be deconstructed and all its components disposed by landfill, incineration, recycling or direct reuse.” Adapted from: Towards a circular economy in construction. Published by: Irish Green Building Council.',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the EnerPHit question.')
SCHEME_PAGES = {'1': [4, 5, 36], '2': [6, 7, 8, 9, 37], '3': [10, 11, 12, 13, 38], '4': [13, 14, 15, 39], '5': [16, 17, 40],
                '6': [18, 19, 20, 41], '7': [21, 22, 42], '8': [23, 24, 25, 43], '9': [26, 27, 28, 44], '10': [29, 30, 31, 32, 45],
                '10-alt': [33, 34, 46]}

tasks, bindings, cards = [], [], {}


def add(q, key, ref, text, rows, nodes, topics, figure, review, boundary, selection, groups=None, total=None, alt=False):
    meta = ALT if alt else QUESTIONS[q]
    qkey = '10-alt' if alt else q
    cid = f'{PREFIX}q{qkey}-{key}'
    concept = LEGACY[cid]['conceptId'] if cid in LEGACY else f"{meta['concept']}-{key}"
    card = dict(id=cid, subjectId='construction-studies', year=2024, level='higher', section='B',
                topicId=nodes[0], conceptId=concept, questionRef=f'2024 HL Q{qkey}{ref}',
                stem=meta['stem'], questionText=text, tariffModel={'kind': 'fixed'},
                totalMarks=total if total is not None else sum(r['marks'] for r in rows), rows=rows,
                questionFigureKey=f'{FP}q{qkey}-original', questionFigureIncludesPrompt=True)
    if figure:
        card['figureKey'] = FP + figure
    card['sourceMaterial'] = dict(kind='source-illustration', label=f"ORIGINAL QUESTION 10{' — ALTERNATIVE' if alt else ''}" if q == '10' else f'ORIGINAL QUESTION {q}',
                                  title=meta['title'], pages=[1, meta['page']], attribution=ATTRIBUTION, presentationNote=meta['note'])
    if groups:
        card['taskGroups'] = groups
    tasks.append(dict(questionNumber=q, alternative=alt, correction=cid in LEGACY, card=card,
                      sourceChecks=checks(meta['page'], SCHEME_PAGES[qkey]), boundaryReview=boundary, selectionReview=selection,
                      requiredQuestionFigures=[card['questionFigureKey']], requiredSolutionFigures=[FP + figure] if figure else []))
    bindings.append(dict(cardId=cid, markBankTopicId=nodes[0], canonicalTopicIds=nodes, canonicalTopicReview=review,
                         questionNumber=q, atlasTopicIds=[CROSS + t for t in topics]))
    cards[cid] = card
    return card


def compose(q, key, ref, children, figure, boundary, selection, text, labels=None, alt=False):
    qkey = '10-alt' if alt else q
    rows, groups = [], []
    for i, child in enumerate(children):
        prefix = child['id'].removeprefix(f'{PREFIX}q{qkey}-')
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
               boundary, selection, groups=groups, total=sum(c['totalMarks'] for c in children), alt=alt)


def parts(*cs):
    return '\n\n'.join(f'({letter}) {c["questionText"]}' for letter, c in zip('abc', cs))


# ---------------------------------------------------------------- Q1
B1 = 'Scheme p36 (printed 34): (a) external wall and eaves 4 × 4, roof 4 × 4, front wall of house and abutment 4 × 4 (3 for drawing, 1 for annotation) = 48, scale 4 + drafting 4 banded excellent 8/good 6/fair 4 = 56; (b) ventilation detail 4. Complete 60. The scale/drafting allowance assesses the section drawn in (a), so it stays with (a).'
S1 = 'One required section and one required ventilation detail. The scheme detail lists are marking menus, not printed choices.'
A1 = add('1', 'a', '(a)',
         'To a scale of 1:10, draw a vertical section through the entrance porch showing the external wall of the porch, the sloping roof, and the front wall of the house. Include the typical construction details of the porch from a point 300 mm below the wall plate, through the sloping rafters, to a level 350 mm above the abutment of the porch roof with the front wall of the house. Show three courses of slate at eaves.',
         [row('external-wall', 'External wall and eaves - typical detailing', 16, 'Best four details, 4 each (3 for drawing, 1 for annotation). Marking menu: larch cladding rain screen; battens/counter battens; cavity wall blockwork and low-conductivity wall ties; full-fill insulation; cavity closer; wallplates; skim/plaster.'),
          row('roof', 'Lean - To roof - typical detailing', 16, 'Best four details, 4 each (3 for drawing, 1 for annotation). Marking menu: fascia/soffit/gutter (any two); three courses of slate; slating battens 50 × 30 mm at 400 mm centres and counter battens; roof breather membrane; ventilation; rafter and insulation; air barrier membrane and airtightness taping; insulated plasterboard (50 mm insulation + 12.5 mm plasterboard).'),
          row('front-wall', 'Front wall of house and abutment - typical detailing', 16, 'Best four details, 4 each (3 for drawing, 1 for annotation). Marking menu: external and internal render; full-fill cavity blockwork and low-conductivity wall ties; concrete lintels; cavity closer; rafter support; stepped DPC; lead flashing (under and apron).'),
          row('presentation', 'Scale - 4 marks Drafting - 4 marks', 8, 'Scale 4 and drafting 4, assessed together: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-3-10', 'cons-3-9', 'cons-3-3', 'cons-3-4'], ['question-1-drawing-questions', 'roofs', 'walls'], 'q1-section',
         'Scaled drawing (1.5) of a lean-to roof abutting a wall (3.10) with its slate covering and insulation (3.9), the cavity walls (3.3) and the stepped DPC, lintels and flashing (3.4).',
         B1, S1)
B1b = add('1', 'b', '(b)', 'On your drawing, show the typical design detailing to ensure adequate ventilation of the roof structure.',
          [row('ventilation', 'Design detailing identified to ensure ventilation of the roof', 4,
               'Show and identify the ventilation route, as in the scheme’s model detail: air entering at the eaves, through the vented soffit, and moving up the ventilated space above the insulation and breather membrane, between the counter battens, to the abutment.')],
          ['cons-3-9', 'cons-6-5'], ['roofs', 'wood-rot-ventilation'], 'q1-ventilation',
          'Ventilation (6.5) of the roof covering and insulation zone (3.9).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p37 (printed 35): (a) kitchen two details and bedroom two details, each notes 3 + sketches 3 = 24; (b) line diagram 4, annotated sketch with access, shower area, W.C., wash basin and grab rails 3 each = 15, two dimensions 2 = 21; (c) each of the five items 1 for point + 2 for discussion = 15. Complete 60.'
S2 = 'Both printed areas in (a) and all five printed items in (b) and (c) are required, not choices. Guidelines and layouts are open responses; the scheme gives two model layouts.'
A2 = add('2', 'a', '(a)',
         'Discuss in detail, using notes and freehand sketches, two best practice guidelines for each of the following areas when designing a house for lifetime use: kitchen; bedroom.',
         [row('kitchen-1', 'Kitchen - (2 details) Detail 1', 6, 'Notes 3 and sketches 3. Such as: 1200–1500 mm between opposing work surfaces; angled or pop-up sockets that are easy to see and reach; D-handles at least 100 mm long; cupboard doors opening to at least 135 degrees; hot water to the sink no hotter than 40 °C with sensor or lever taps.'),
          row('kitchen-2', 'Detail 2', 6, 'A second, different kitchen guideline: notes 3 and sketches 3. Such as: clear knee space beneath the sink and hob for a seated user; oven and fridge in a housing at an accessible height; worktops adjustable between 760 and 900 mm; at least 300 mm beside the hob; pull-out drawers in deep base units; a level threshold to the garden.'),
          row('bedroom-1', 'Bedroom - (2 details) Detail 1', 6, 'Notes 3 and sketches 3. Such as: at least 800 mm clear either side of the bed and more at its end; a 1500 mm turning circle; sockets and switches 400–1000 mm above floor level; switches at the door and both sides of the bed.'),
          row('bedroom-2', 'Detail 2', 6, 'A second, different bedroom guideline: notes 3 and sketches 3. Such as: windows operable with one hand, levers 800–1200 mm high; a ground-floor room usable as a bedroom; a soft spot in the wall to the bathroom for a future en suite door; hard spots for a future hoist.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q2-guidelines', 'Designing a dwelling for lifetime use within the built environment (1.2).', B2, S2)
B2b = add('2', 'b', '(b)',
          'A draft design for a bedroom and an en suite bathroom is shown. The en suite bathroom at A, is to be accessed from the bedroom. Using notes and a freehand sketch, show a preferred layout for the en suite to ensure ease of use by a person with limited mobility. On your design sketch, show the location of the following: access to the en suite from the bedroom; shower area; water closet (W.C.); wash basin; grab rails. Include two typical dimensions.',
          [row('line-diagram', 'Line diagram of bedroom and en suite', 4, 'A line diagram of the bedroom and the en suite at A, as in the scheme’s two model layouts.'),
           row('items', 'Annotated sketch to include:', 15, 'All five printed items, 3 each, located and annotated on the sketch: access to the en suite from the bedroom; shower area; water closet (W.C.); wash basin; grab rails.'),
           row('dimensions', 'Dimensions - Any two', 2, 'Two typical dimensions, such as a 900 mm clear door width, a 1500 mm turning circle, a 1 m × 1 m minimum shower area or a 1100 mm × 700 mm clear zone in front of the W.C.')],
          ['cons-1-2', 'cons-5-6'], ['planning-sustainability-environment', 'drainage'], 'q2-layouts',
          'Accessible design (1.2) of the sanitary fitments (5.6).', B2, S2)
C2 = add('2', 'c', '(c)', 'Justify your preferred location for each of the bathroom items listed at 2(b) above.',
         [row('access', 'Access to en suite (1 for point, 2 for discussion)', 3, 'Point 1 and discussion 2. Such as: a 900 mm clear door width for a wheelchair; a door opening out of the en suite to give more space for moving and turning.'),
          row('shower', 'Shower area (1 for point, 2 for discussion)', 3, 'Point 1 and discussion 2. Such as: a level wet-room shower with no tray, a fall to the drain and a non-slip floor; in a corner so grab rails and a folding seat can be fixed to the walls; at least 1 m × 1 m.'),
          row('wc', 'Water closet (W.C.) (1 for point, 2 for discussion)', 3, 'Point 1 and discussion 2. Such as: its centre 450–500 mm from the wall so rails can be installed; a clear 1100 mm × 700 mm zone in front; not opposite the door, for privacy; a lever cistern handle.'),
          row('basin', 'Wash basin (1 for point, 2 for discussion)', 3, 'Point 1 and discussion 2. Such as: at 750–800 mm above the floor with at least 600 mm knee space and no pedestal; a clear 1100 mm × 700 mm access zone; lever or sensor taps; support in the stud for an adjustable basin.'),
          row('grab-rails', 'Grab rails (1 for point, 2 for discussion)', 3, 'Point 1 and discussion 2. Such as: horizontal and vertical rails at the fixtures; drop rails beside the W.C., with a 400 mm fold-up rail on its open side; 35 mm diameter rails in the shower area.')],
         ['cons-1-2', 'cons-5-6'], ['planning-sustainability-environment', 'drainage'], 'q2-justify',
         'Accessible design (1.2) of the sanitary fitments (5.6).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-layouts', B2, S2, parts(A2, B2b, C2))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p38 (printed 36): (a) revised layout 14, linking the kitchen 3, optimising daylight 3, maximising the views 3, justification 3 = 26; (b) notes 12 + sketch 12 = 24; (c) two advantages × (2 for point + 3 for discussion) = 10. Complete 60.'
S3 = 'The three design considerations are all required in one layout, not a choice. Layouts, external designs and advantages are open responses; the scheme gives model sketches.'
A3 = add('3', 'a', '(a)', 'Using notes and freehand sketches, show a revised internal layout for the proposed renovation of the forge shown, that incorporates each of the above requirements. Justify your design choices.',
         [row('layout', 'Revised internal layout for the kitchen/dining and living area', 14, 'Notes and freehand sketches of a coherent open-plan kitchen/dining and living layout in the forge. Such as: structural steel in the gable at the junction of the house and forge, making the kitchen and forge one space, or keeping a section of the gable wall to define the spaces; a kitchen island at the centre of the new space; the dining table beside the large glazing.'),
          row('linking', 'Linking existing kitchen to the forge', 3, 'The existing kitchen linked to the forge, for example by opening the gable at the junction with structural steel, keeping the kitchen in place to save moving services.'),
          row('daylight', 'Optimising natural daylight', 3, 'Daylight optimised, for example glass doors in wall A-A for southern light, floor-to-ceiling south glazing, or ridge/roof glazing units.'),
          row('views', 'Maximising the views to the mountain', 3, 'The mountain views maximised, for example large high-performance glazing in the gable towards wall B-B.'),
          row('justification', 'Justification', 3, 'The design choices justified, for example heat and light flowing through one open space, solar gain from the south, retained window positions keeping the vernacular character, triple or quadruple low-e glazing for comfort and less glare.')],
         ['cons-1-1', 'cons-1-2', 'cons-7-4'], ['conservation-restoration', 'windows-light'], 'q3-layout',
         'Renovating a vernacular building (1.1) within the built environment (1.2) for good daylighting (7.4).', B3, S3)
B3b = add('3', 'b', '(b)', 'Using notes and freehand sketches, show an external design for your forge renovation that will respect and enhance the overall visual appearance of the house.',
          [row('notes', 'Notes', 12, 'Such as: materials like those of the forge (corrugated metal and stone) so it still reads as a separate building without pastiche; salvaged materials of similar age and style; retained and repaired stonework re-pointed with lime mortar; the opening sizes and proportions kept on the front; glazing added to the gable, which is set back from the house; a ridge glazing system that lets light in without altering the vernacular form.'),
           row('sketch', 'Sketch', 12, 'Freehand sketch of the external design of the renovated forge beside the house.')],
          ['cons-1-1', 'cons-1-2'], ['conservation-restoration'], 'q3-external',
          'External design that respects the historic building (1.1) and its setting (1.2).', B3, S3)
C3 = add('3', 'c', '(c)', 'Discuss two advantages of respecting Irish vernacular architecture when renovating an old building.',
         [row('advantage-1', 'Advantage 1 (2 for point, 3 for discussion)', 5, 'Point 2 and discussion 3. Such as: the character of old buildings contributes to the local and national landscape and shows how the building and area were used in the past; respecting the original design keeps historical continuity, authenticity and integrity.'),
          row('advantage-2', 'Advantage 2 (2 for point, 3 for discussion)', 5, 'A second, different advantage: point 2 and discussion 3. Such as: the local design, craft and materials give a sense of place; local, green and sustainable materials — the greenest building is the one already built; unique aesthetics blending old and new; Ireland’s built heritage supports tourism.')],
         ['cons-1-1'], ['conservation-restoration'], None, 'Historical development and appearance of buildings (1.1).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-layout', B3, S3, parts(A3, B3b, C3))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p39 (printed 37): (a) three reasons × (2 for point + 4 for discussion) = 18; (b) three considerations × (2 for point + 4 for discussion) = 18; (c) sketch of selected site 6, house location and orientation 5, outdoor living space 5, road entrance and driveway 5, justification 3 = 24. Complete 60.'
S4 = 'Selecting site A or B in (b) is part of the answer: the scheme marks the three considerations alike for either site, so it is one task, not two routes. The three items in (c) are required content in one sketch.'
A4 = add('4', 'a', '(a)', 'Discuss in detail three reasons why local planning authorities regulate the design and location of all proposed new dwellings.',
         [row(f'reason-{i}', f'Reason {i} (2 for point, 4 for discussion)', 6, note) for i, note in [
             (1, 'Point 2 and discussion 4. Such as: safety standards protect occupants and the public from structural instability, fire risk and poor emergency access; the impact on infrastructure, transport and public services is managed, preventing overdevelopment.'),
             (2, 'A second, different reason: point 2 and discussion 4. Such as: the visual character and historical significance of an area are safeguarded and heritage buildings preserved; environmental impact is minimised through sustainable, energy-efficient design and zoning that protects habitats.'),
             (3, 'A third, different reason: point 2 and discussion 4. Such as: quality of life — access to green space, light, privacy and amenities; traffic and parking are controlled with access roads and parking spaces; new dwellings follow the long-term development plan for the area.')]],
         ['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'], None,
         'Controls over the built environment (1.2) and planning permission (1.3).', B4, S4)
B4b = add('4', 'b', '(b)', 'Shown is an extract from a site location map. A and B are possible sites for a new dwelling house. Select your preferred site and discuss three considerations you took into account when selecting your site.',
          [row(f'consideration-{i}', f'Consideration {i} (2 for point, 4 for discussion)', 6, note) for i, note in [
              (1, 'Point 2 and discussion 4, for the selected site. Such as, site A: less visual impact beside existing buildings; a cluster development favoured by planners; cost-effective public services nearby. Site B: not overlooked; safer access off the busy road; less noise and air pollution.'),
              (2, 'A second, different consideration: point 2 and discussion 4. Such as, site A: neighbouring buildings increase security; a long southern axis for solar gain. Site B: more creative designs possible with no buildings close by; greater privacy away from the main road.'),
              (3, 'A third, different consideration: point 2 and discussion 4. Such as, site A: existing utilities reduce new mains, ESB and broadband work. Site B: larger windows without loss of privacy; better scenic views of the countryside.')]],
          ['cons-1-3'], ['planning-sustainability-environment'], 'q4-sites', 'Choosing a site (1.3).', B4, S4)
C4 = add('4', 'c', '(c)', 'Draw a well-proportioned sketch of your selected site and immediate boundaries. On your sketch, show a preferred: location and orientation of a house on the site; outdoor living space; layout of the road entrance and driveway to the house. For each of the above, justify your design choices.',
         [row('sketch', 'Sketch of selected site', 6, 'A well-proportioned sketch of the selected site and its immediate boundaries.'),
          row('house', 'House location and Orientation', 5, 'Such as: the long axis east-west with the largest elevation facing south for solar gain and daylight; living spaces on the south, ideally one room deep; set back from the road; hedges and trees kept for shelter; close to the road where services run.'),
          row('outdoor', 'Outdoor living space', 5, 'Such as: placed for sunlight through the day, scenic views and privacy; easily reached from inside the house; sheltered from the weather by trees or the house itself.'),
          row('road', 'Road entrance and Driveway', 5, 'Such as: a short driveway to the north of the house, keeping the south clear; an entrance set back 5 metres with splayed walls at 45° for clear vision; as few hedges and trees removed as possible; minimal hard surfaces.'),
          row('justification', 'Justification', 3, 'The design choices justified for each of the three items.')],
         ['cons-1-3', 'cons-6-4'], ['planning-sustainability-environment'], 'q4-site-plans',
         'Site layout (1.3) with orientation for solar gain (6.4).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-site-plans', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p40 (printed 38): (a) eleven points × 3 = 33 (tabulation, the two surface resistances, the six material layers, total resistance, U-value); (b) five steps × 3 = 15; (c) two advantages and two disadvantages × (1 for point + 2 for discussion) = 12. Complete 60.'
S5 = 'No printed choice. Part (c) requires both two advantages and two disadvantages, separately marked: two required tasks composed into (c).'
DATA5A = ('Acrylic external render thickness 12 mm; external insulation thickness 150 mm; concrete thickness 150 mm; internal insulation thickness 50 mm; '
          'internal plasterboard thickness 12.5 mm; internal skim coat thickness 4 mm.\n'
          'Thermal data of the external wall: resistance of external surface (R) 0.048 m² °C/W; conductivity of acrylic external render (k) 0.670 W/m °C; '
          'conductivity of external insulation (k) 0.030 W/m °C; conductivity of concrete (k) 1.280 W/m °C; conductivity of internal insulation (k) 0.030 W/m °C; '
          'conductivity of plasterboard (k) 0.250 W/m °C; resistivity of skim coat (r) 5.550 m °C/W; resistance of internal surface (R) 0.122 m² °C/W.')
A5 = add('5', 'a', '(a)', 'Calculate the U-value of the wall, given the construction has the following sequence and data: ' + DATA5A,
         [row('tabulation', 'Tabulation', 3, 'A clear table of the materials with their conductivity or resistivity, thickness in metres and resistance.'),
          row('resistances', 'Formulae: R=T/k R=T × r', 24, 'Eight resistances, 3 each, by R = T/k (or R = T × r for the skim coat): external surface 0.048 (given); acrylic render 0.012/0.670 = 0.018; external insulation 0.150/0.030 = 5.000; concrete 0.150/1.280 = 0.117; internal insulation 0.050/0.030 = 1.667; plasterboard 0.0125/0.250 = 0.050; skim coat 0.004 × 5.550 = 0.022; internal surface 0.122 (given). All in m²°C/W.', list(range(0, 25, 3))),
          row('total-resistance', 'Total resistance', 3, 'Total resistance Rt = 7.044 m²°C/W (the sum of all the resistances).', [0, 3]),
          row('u-value', 'Calculation of U-value (w/m2 °C or w/m2k)', 3, 'U = 1 ÷ Rt = 1 ÷ 7.044 = 0.142 W/m²°C, with units.', [0, 3])],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Thermal resistance, conductivity and transmittance (6.1).', B5, S5)
B5b = add('5', 'b', '(b)', 'Using the U-value of the wall obtained at 5(a) above and the following data, calculate the cost of heat lost annually through this wall: area of external wall 110 m²; average internal temperature 20 °C; average external temperature 6 °C; heating period 6 hours daily for 32 weeks per annum; cost of wood pellets 52 cent per kg; calorific value of wood pellets 17350 kJ per kg; 1000 watts: 1 kJ per second.',
          [row('heat-loss', 'Heat loss formula and calculation', 3, 'Heat loss = U-value × area × temperature difference = 0.142 × 110 × (20 − 6) = 218.6269 watts (joules per second).'),
           row('duration', 'Heating duration for one year', 3, 'Heating period = 60 × 60 × 7 × 6 × 32 = 4,838,400 seconds (1,344 hours).'),
           row('energy', 'k/Joules calculation for one year', 3, 'Energy = 4,838,400 × 218.627 ÷ 1000 = 1,057,804 kJ per year.'),
           row('pellets', 'Kgs of wood pellets for one year', 3, 'Wood pellets = 1,057,804 ÷ 17,350 = 60.96 kg per year.'),
           row('cost', 'Annual cost of heat loss', 3, 'Annual cost = 60.96 × €0.52 = €31.71. The scheme’s alternative one-line method gives the same €31.71.')],
          ['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Heat loss calculation and running costs (6.3) from the U-value (6.1).', B5, S5)
T5C = 'Discuss two advantages and two disadvantages of designing a domestic heating system to incorporate a wood pellet boiler stove.'
C5a = add('5', 'c-advantages', '(c) — advantages', 'Discuss two advantages of designing a domestic heating system to incorporate a wood pellet boiler stove.',
          [row('advantage-1', 'Advantage 1 (1 for point, 2 for discussion)', 3, 'Point 1 and discussion 2. Such as: a renewable, carbon-neutral fuel made from sawdust and shavings; relatively cheap and price-stable fuel; up to 90% efficiency from controlled air-to-fuel ratios.'),
           row('advantage-2', 'Advantage 2 (1 for point, 2 for discussion)', 3, 'A second, different advantage: point 1 and discussion 2. Such as: eco-design certification with lower emissions than a log stove; ease of use, with programmable thermostats and self-cleaning burners.')],
          ['cons-5-3'], ['hot-water-space-heating'], None, 'Heating systems and heat conservation (5.3).', B5, S5)
C5d = add('5', 'c-disadvantages', '(c) — disadvantages', 'Discuss two disadvantages of designing a domestic heating system to incorporate a wood pellet boiler stove.',
          [row('disadvantage-1', 'Disadvantage 1 (1 for point, 2 for discussion)', 3, 'Point 1 and discussion 2. Such as: a high purchase price and complex, costly installation with suitable ventilation; pellets need dry, safe storage to avoid moisture damage.'),
           row('disadvantage-2', 'Disadvantage 2 (1 for point, 2 for discussion)', 3, 'A second, different disadvantage: point 1 and discussion 2. Such as: regular maintenance — ash cleaning, servicing, filling the hopper; uncertain pellet supply in some regions; it cannot run without electricity for ignition, feed and controls.')],
          ['cons-5-3'], ['hot-water-space-heating'], None, 'Heating systems and heat conservation (5.3).', B5, S5)
C5 = compose('5', 'c', '(c)', [C5a, C5d], None, B5, S5, T5C, labels=['Advantages', 'Disadvantages'])
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(A5, B5b, C5))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p41 (printed 39): (a) three design features × (notes 5 + sketches 5) = 30; (b) two added features × (notes 5 + sketches 5) = 20; (c) two advantages × (2 for point + 3 for discussion) = 10. Complete 60.'
S6 = 'Features, added features and advantages are open responses with no printed list; the scheme lists typical examples.'
A6 = add('6', 'a', '(a)', 'Discuss using notes and freehand sketches, three features of the design that contribute to the house having a low environmental impact.',
         [row(f'feature-{i}', f'Design Feature {i}', 10, note) for i, note in [
             (1, 'Notes 5 and sketches 5. Such as: timber frame from local sources — less transport, lower embodied energy than block, and carbon stored in the timber.'),
             (2, 'A second, different feature: notes 5 and sketches 5. Such as: large south-facing glazed openings filling the living spaces with light and solar heat; high-performance glazing (U-value at least 0.8 W/m²K).'),
             (3, 'A third, different feature: notes 5 and sketches 5. Such as: high insulation levels in floor, walls and roof; a one-room-deep plan lit from three sides; no chimney, so fewer draughts and better airtightness.')]],
         ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-low-impact',
         'Low-impact design of the built environment (1.2), solar gain (6.4) and insulation (6.2).', B6, S6)
B6b = add('6', 'b', '(b)', 'Discuss using notes and freehand sketches, two features that could be added to the house that would further increase the energy efficiency of the house.',
          [row(f'feature-{i}', f'Feature {i}', 10, note) for i, note in [
              (1, 'Notes 5 and sketches 5. Such as: photovoltaic panels or evacuated tubes on the pitched roof generating renewable electricity or heating the hot-water cylinder; a storm lobby as a buffer zone that cuts heat loss at the entrance.'),
              (2, 'A second, different feature: notes 5 and sketches 5. Such as: an interior sliding door to zone off and heat a smaller space; solar shading (brise soleil or balconies) against summer overheating; larger high-performance south glazing for more solar gain.')]],
          ['cons-6-3', 'cons-6-4', 'cons-6-2'], ['heat-loss-insulation', 'sustainability-the-environment'], 'q6-features',
          'Reducing heating demand and running costs (6.3) through solar gain (6.4) and the building fabric (6.2).', B6, S6)
C6 = add('6', 'c', '(c)', 'Discuss two advantages of designing energy efficient new homes.',
         [row(f'advantage-{i}', f'Advantage {i} (2 for point, 3 for discussion)', 5, note) for i, note in [
             (1, 'Point 2 and discussion 3. Such as: reduced energy costs and bills; environmental sustainability, with a lower carbon footprint and greenhouse gas emissions; improved year-round comfort.'),
             (2, 'A second, different advantage: point 2 and discussion 3. Such as: increased property value; health benefits from better indoor air; compliance with regulations and access to a green mortgage.')]],
         ['cons-6-3', 'cons-1-2'], ['heat-loss-insulation', 'sustainability-the-environment'], None,
         'Running costs (6.3) and the sustainable built environment (1.2).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-low-impact', B6, S6, parts(A6, B6b, C6))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p42 (printed 40): (a) external wall 5 × 4, head of the window 4 × 4, first floor 3 × 4 (3 for drawing, 1 for annotation) = 48, scale 4 + drafting 4 banded excellent 8/good 6/fair 4 = 56; (b) airtightness design detail 4. Complete 60.'
S7 = 'One required section and one required airtightness detail. The scheme detail lists are marking menus, not printed choices.'
A7 = add('7', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the external wall, window, and first floor. Show the typical construction details from a level 200 mm below the head of the window, to a level 200 mm above the finished first floor.',
         [row('external-wall', 'External wall', 20, 'Best five details, 4 each (3 for drawing, 1 for annotation). Marking menu: external render; concrete block; air space/residual cavity; breather membrane; OSB racking board; 250 × 50 mm stud and insulation; air barrier; insulated service cavity; plasterboard/skim.'),
          row('window-head', 'Window Frame', 16, 'Best four details at the head of the window, 4 each (3 for drawing, 1 for annotation). Marking menu: concrete lintel; timber lintel; fire stop/cavity closer; stepped DPC; thermally broken frame; triple glazing; airtightness tape at the window frame head.'),
          row('first-floor', 'Floor', 12, 'Best three first-floor details, 4 each (3 for drawing, 1 for annotation). Marking menu: joist supported at the wall; tongued and grooved flooring/skirting board; OSB decking; 225 × 50 mm joist; sound insulation; plasterboard ceiling.'),
          row('presentation', 'Scale - 4 marks Drafting - 4 marks', 8, 'Scale 4 and drafting 4, assessed together: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-3-3', 'cons-3-6', 'cons-4-3'], ['question-1-drawing-questions', 'walls', 'windows-light', 'floors'], 'q7-section',
         'Scaled drawing (1.5) of a timber-frame external wall (3.3), the window head (3.6) and the upper floor (4.3).', B7, S7)
B7b = add('7', 'b', '(b)', 'On your drawing, indicate the typical design detailing to ensure airtightness at the junction of the first floor joist and timber frame inner leaf.',
          [row('detail', 'Design detail', 4, 'Such as: an airtightness barrier around the joists where they meet the timber-frame inner leaf, with the junctions and corners sealed with airtightness tape.')],
          ['cons-6-5', 'cons-4-3'], ['condensation-air-tightness', 'floors'], 'q7-airtightness',
          'Airtightness (6.5) at the upper-floor junction (4.3).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(A7, B7b))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p43 (printed 41): (a) best seven system items × 4 = 28 + typical sizes of pipework (any two) 4 = 32; (b) notes 6 + sketches 6 = 12; (c) two advantages and two disadvantages × (1 for point + 3 for discussion) = 16. Complete 60.'
S8 = 'One required system layout. The renewable method in (b) is an open choice with no printed list; the scheme gives two examples.'
A8 = add('8', 'a', '(a)', 'Using notes and a single-line diagram, show a typical design layout for both the hot water system and the heating system. On the diagram, show two independently controlled heating zones, one on each floor. Include two radiators on each floor and give typical sizes of the pipework.',
         [row('layout', 'Typical design layout to provide hot water and central heating (7 × 4 marks)', 28, 'Best seven items, 4 each. Marking menu: wood-burning stove; radiators on the ground and first floors; zone control panel; zone thermostats; cylinder and coil; header/expansion/storage tank; rising main; feed to the expansion tank; overflow pipe; cold feed from the expansion tank; expansion pipe or vessel; flow pipe to the radiators; pump; return pipe from the radiators; control valves (isolating or drain-off, any two).'),
          row('sizes', 'Typical sizes of pipework - any two', 4, 'Two typical pipe sizes, 2 each. Such as: Ø15 mm cold-water rising main; Ø22 mm primary flow and return; Ø15 mm pipes to radiators; Ø22 mm cold feed to the cylinder; Ø28 mm hot-water feed; Ø28 mm overflow.', [0, 2, 4])],
         ['cons-5-2', 'cons-5-3'], ['hot-water-space-heating'], 'q8-system', 'Hot and cold water (5.2) and zoned heating controls (5.3).', B8, S8)
B8b = add('8', 'b', '(b)', 'On-site renewable energy generation can be used to heat water in the hot water cylinder of a house. Using notes and freehand sketches, discuss one method of incorporating such renewable technology into a hot water system.',
          [row('notes', 'Notes', 6, 'Such as: a solar collector — tubes absorb solar energy, the heated fluid passes heat at the manifold to water circulated through the cylinder coil, with a control panel, pump and expansion vessel; or photovoltaic panels with an inverter and a solar immersion diverter that sends surplus electricity, sensed by a CT clamp, to the immersion.'),
           row('sketches', 'Sketches', 6, 'Freehand sketches of the chosen method connected to the hot-water cylinder.')],
          ['cons-5-2', 'cons-6-4'], ['hot-water-space-heating', 'sustainability-the-environment'], 'q8-renewables',
          'Heating hot water (5.2) from solar energy (6.4).', B8, S8)
C8 = add('8', 'c', '(c)', 'Underfloor heating is often installed in dwellings to provide space heating. Discuss two advantages and two disadvantages of incorporating an underfloor heating system into a dwelling house.',
         [row('advantage-1', 'Advantage 1 (1 for point, 3 for discussion)', 4, 'Point 1 and discussion 3. Such as: even, constant heat distribution; no radiators taking up wall space.'),
          row('advantage-2', 'Advantage 2 (1 for point, 3 for discussion)', 4, 'A second, different advantage. Such as: energy efficiency and lower running costs; design flexibility in layout and furniture; low maintenance.'),
          row('disadvantage-1', 'Disadvantage 1 (1 for point, 3 for discussion)', 4, 'Point 1 and discussion 3. Such as: higher installation cost, especially when retrofitting; time-consuming installation; some floor finishes are not compatible.'),
          row('disadvantage-2', 'Disadvantage 2 (1 for point, 3 for discussion)', 4, 'A second, different disadvantage. Such as: slow response when heating up and cooling down; repairs are difficult and disruptive; limited zoning control.')],
         ['cons-5-3'], ['hot-water-space-heating'], None, 'Heating systems and temperature control (5.3).', B8, S8)
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-system', B8, S8, parts(A8, B8b, C8))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p44 (printed 42): (a) two functional requirements × (notes 4 + sketches 4) = 16; (b) floor detail notes 8 + sketches 8, stud wall detail notes 8 + sketches 8 = 32; (c) two approaches × (approach 4 + associated principle 2) = 12. Complete 60.'
S9 = 'Part (b) requires both the floor and the stud wall, each separately marked, in one task. Requirements and approaches are open responses.'
A9 = add('9', 'a', '(a)', 'Using notes and freehand sketches, discuss in detail, two functional requirements of an attic space suitable for use as a home office.',
         [row(f'requirement-{i}', f'Functional requirement {i}', 8, note) for i, note in [
             (1, 'Notes 4 and sketches 4. Such as: sufficient lighting from skylights, dormer windows or well-placed artificial light; effective insulation and ventilation for year-round comfort; adequate heating.'),
             (2, 'A second, different requirement: notes 4 and sketches 4. Such as: sufficient storage under the eaves or in built-in units; electrical outlets, networking and cable management; ergonomic furniture and layout.')]],
         ['cons-1-2', 'cons-7-4', 'cons-6-5'], ['planning-sustainability-environment', 'windows-light', 'condensation-air-tightness'], 'q9-requirements',
         'Designing a room within the dwelling (1.2) for good illumination (7.4) and comfort and ventilation (6.5).', B9, S9)
B9b = add('9', 'b', '(b)', 'The first floor of the attic consists of 18 mm OSB sheeting on 200 mm × 50 mm timber joists with plasterboard fixed beneath. The side walls are of standard stud construction. Using notes and freehand sketches, show a revised design detailing that will reduce the transmission of sound through both the floor and the stud wall.',
          [row('floor-notes', 'Floor detail Notes', 8, 'Such as: added mass with dry sand pugging (80 kg/m²) on a false bottom between the joists; absorbent quilt packed tightly between the joists; a floating floor on 25 mm resilient acoustic matting; a soft floor finish (carpet, rubber, cork); a second staggered layer of plasterboard to the ceiling; a viscoelastic damping compound.'),
           row('floor-sketches', 'Sketches', 8, 'Freehand sketch of the revised floor detail.'),
           row('wall-notes', 'Stud wall detail Notes', 8, 'Such as: extra layers of plasterboard with staggered joints; sealed sockets and switches; decoupling rubber fixings or resilient clips and channels (a floating wall); quilt insulation tightly fitted between the studs; airtight tape and sealants at junctions.'),
           row('wall-sketches', 'Sketches', 8, 'Freehand sketch of the revised stud wall detail.')],
          ['cons-8-3', 'cons-4-3', 'cons-4-1'], ['sound', 'floors', 'walls'], 'q9-sound',
          'Airborne and impact sound insulation (8.3) of the upper floor (4.3) and the internal stud wall (4.1).', B9, S9)
C9 = add('9', 'c', '(c)', 'Discuss two approaches used to reduce the transmission of sound in the design of a dwelling house. Identify the sound insulation principle associated with each approach.',
         [row('approach-1', 'Approach 1', 4, 'One approach discussed. Such as: concrete upper floors or 215 mm blocks for mass; airtight tape and rubber seals around openings; acoustic panels or underlay; cavities and floating floors (room within a room).'),
          row('principle-1', 'Associated sound principle', 2, 'Its principle named, such as heaviness (mass — doubling the mass adds about 5 dB), completeness (airtightness and no gaps), flexibility or isolation (discontinuous construction).'),
          row('approach-2', 'Approach 2', 4, 'A second, different approach discussed.'),
          row('principle-2', 'Associated sound principle', 2, 'Its principle named, different where the approach differs.')],
         ['cons-8-3'], ['sound'], None, 'Airborne and impact sound insulation (8.3).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-sound', B9, S9, parts(A9, B9b, C9))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p45 (printed 43): (a) any two of three printed items, each notes 6 + sketches 6 = 12; (a) 24. (b) indoor air quality notes 6 + sketches 6, space heating notes 6 + sketches 6 = 24; (c) two advantages × (2 for point + 4 for discussion) = 12. Complete 60.'
S10 = 'Choice is not a route: part (a) (any two of three printed items) is ONE card with an any-two group. Part (b) requires both printed items, each separately marked, so each is its own task and (b) composes them. The OR alternative is a separate Question 10 route.'
ITEMS10 = [('airtightness', 'Airtightness',
            'Air leakage prevented with airtightness membranes, airtight boards and tapes in timber frame and roofs, and a sand-cement scratch coat, plaster and airtightness paint in block walls; checks for leakage at each stage and a full airtightness test at the end; the EnerPHit target is under 1.0 air changes per hour at 50 Pascals (Passive House 0.6); without airtightness the insulation cannot perform.'),
           ('windows', 'Windows',
            'Passive House triple-glazed windows of 0.80 W/m²K or less (EnerPHit, installed, 0.85 W/m²K or less); frames in line with the external insulation to avoid a thermal bridge; shading and ventilation planned against summer overheating.'),
           ('building-fabric', 'Building fabric',
            'Insulation increased to roof, floor and walls (U-value 0.120 W/m²K or less for EnerPHit) by cavity, external or internal insulation; quality workmanship to avoid thermal bridges; external insulation continued below ground level; airtightness and insulation achieved together.')]
A10 = add('10', 'a', '(a)', 'Using notes and freehand sketches, discuss the importance of any two of the following when carrying out a retrofit to achieve the EnerPHit Passive House design standard: airtightness; windows; building fabric.',
          [dict(id='items', kind='anyN', verbatim='Discuss the importance of any two in EnerPHit design standard', marks=24,
                contextNote='Any two of the three, each notes 6 and sketches 6 = 12. EnerPHit is reached through the five Passive House principles (insulation, limited thermal bridging, triple glazing, airtightness, MVHR), modelled in the PHPP design tool; its space heating demand limit is 25 kWh/m² per year (Passive House 15). '
                + ' '.join(f'{h}: {n}' for _, h, n in ITEMS10),
                group=dict(claimMax=2, perOption=12, options=[h for _, h, _ in ITEMS10]))],
          ['cons-6-5', 'cons-3-5', 'cons-6-2', 'cons-6-4'], ['passive-design', 'condensation-air-tightness', 'windows-light', 'heat-loss-insulation'], 'q10-items',
          'The union of the three printed items: airtightness (6.5), windows (3.5) and the insulated building fabric (6.2) in passive design (6.4).', B10, S10)
T10B = 'Using notes and freehand sketches, discuss in detail how each of the following could be improved, when upgrading an existing building to meet the EnerPHit standard: indoor air quality; space heating.'
B10i = add('10', 'b-indoor-air-quality', '(b) — indoor air quality', T10B + ' — Indoor air quality',
           [row('notes', 'Notes', 6, 'Such as: mechanical ventilation with heat recovery (MVHR) supplying fresh air and recovering heat, with regular filter changes; low-VOC materials, finishes and furnishings; humidity kept at 30–50% with humidity-controlled ventilation; air-quality sensors; openable windows in every room.'),
            row('sketches', 'Sketches', 6, 'Freehand sketches of the improvement, such as the MVHR supply and extract routes.')],
           ['cons-6-5'], ['passive-design', 'condensation-air-tightness'], 'q10-upgrade', 'Indoor air quality and ventilation (6.5).', B10, S10)
B10s = add('10', 'b-space-heating', '(b) — space heating', T10B + ' — Space heating',
           [row('notes', 'Notes', 6, 'Such as: continuous high-quality insulation without thermal bridges; high-performance glazing and doors with sealed junctions; an air-source or ground-source heat pump (coefficient of performance about 5:1) with underfloor heating; MVHR heat recovery; passive solar gain and thermal mass, with shading against overheating, for a steady 20 °C.'),
            row('sketches', 'Sketches', 6, 'Freehand sketches of the improvement.')],
           ['cons-5-3', 'cons-6-2'], ['hot-water-space-heating', 'passive-design'], 'q10-upgrade', 'Space heating (5.3) and reduced heat loss through the fabric (6.2).', B10, S10)
B10b = compose('10', 'b', '(b)', [B10i, B10s], 'q10-upgrade', B10, S10, T10B, labels=['Indoor air quality', 'Space heating'])
C10 = add('10', 'c', '(c)', 'Discuss two advantages of using qualified skilled labour when retrofitting a house to meet EnerPHit Passive House standards.',
          [row(f'advantage-{i}', f'Advantage {i} (2 for point, 4 for discussion)', 6, note) for i, note in [
              (1, 'Point 2 and discussion 4. Such as: expertise in the complex EnerPHit requirements and best practice; quality workmanship so every component is installed correctly and the energy targets are met.'),
              (2, 'A second, different advantage: point 2 and discussion 4. Such as: efficient, on-time completion; compliance with regulations, including airtightness; problem solving on site; long-term performance, so the disruptive retrofit need not be repeated.')]],
          ['cons-6-5', 'cons-6-2'], ['passive-design'], None,
          'Skilled workmanship delivers the airtightness (6.5) and continuous insulation without thermal bridges (6.2) that EnerPHit requires.', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-scheme', B10, S10, parts(A10, B10b, C10))

BALT = 'Scheme p46 (printed 44): (a) three discussion points × (4 for point + 6 for discussion) = 30; (b) three guidelines × (4 + 6) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the EnerPHit question. Its parts are open responses.'
AA = add('10', 'a', '(a)', 'Discuss the above statement in detail.',
         [row(f'point-{i}', f'Discussion Point {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: the environmental impact of a dwelling at every stage of its lifecycle; weighing the embodied energy of materials against their operational energy — short-lived components carry a higher carbon footprint.'),
             (2, 'Point 4 and discussion 6. Such as: Environmental Product Declarations (EPD), “cradle to grave”, measuring global warming potential and other impacts, with the Irish EPD programme of the Irish Green Building Council.'),
             (3, 'Point 4 and discussion 6. Such as: the circular economy — materials kept in loops of reuse, remanufacture and recycling at their highest value, the opposite of take-make-dispose; careful design that needs less heating and cooling over the building’s life. Three distinct, well-argued points are needed.')]],
         ['cons-1-2'], ['sustainability-the-environment'], None, 'The sustainable built environment (1.2).', BALT, SALT, alt=True)
AB = add('10', 'b', '(b)', 'Propose three best practice guidelines when selecting materials at the design and construction stages, to reduce the whole of life carbon impact of a dwelling house.',
         [row(f'guideline-{i}', f'Guideline {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: calculate cradle-to-grave carbon with the PHribbon package; use only products with Environmental Product Declarations; reduce, reuse, recycle.'),
             (2, 'Point 4 and discussion 6. Such as: standard sizes and lean design to cut material and waste; design for disassembly and reuse, with mechanical fixings rather than bonding and short-lived parts kept accessible; a site waste management plan.'),
             (3, 'Point 4 and discussion 6. Such as: design for flexibility and adaptability so buildings last longer; support for reusing and repurposing existing buildings, with clear planning guidance and grants for reusing materials. Three distinct guidelines are needed.')]],
         ['cons-1-2'], ['sustainability-the-environment'], None, 'Sustainable choice of materials in the built environment (1.2).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, parts(AA, AB), alt=True)

# ---------------------------------------------------------------- ledgers
ledger_rows = [
    (1, 'Answer any', 'Whole-exam selection: any five of the ten questions; all question banks retained, no full-exam Cartesian cards.'),
    (3, 'Select', 'Q4(b) select site A or B: one task, the scheme marking the three considerations alike for either site.'),
    (7, 'any two', 'Q10(a) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
    (7, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.'),
    (7, 'or', 'Quotation narrative (“quarried, mined or harvested”), not an answer directive.'),
    (7, 'or', 'Quotation narrative (“recycling or direct reuse”), not an answer directive.'),
]
pattern = r'\b(?:choose|select|one\s+of|any\s+\w+|either|or|answer\s+\w+)\b'
observed = []
with fitz.open(R / P) as pdf:
    for i, p in enumerate(pdf):
        text = ' '.join(p.get_text().split())
        observed.extend((i + 1, m.start(), m.group(), text[max(0, m.start() - 80):m.end() + 80]) for m in re.finditer(pattern, text, re.I))
assert [(o[0], o[2]) for o in observed] == [(r[0], r[1]) for r in ledger_rows], [(o[0], o[2]) for o in observed]
selection_ledger = dict(pattern=pattern, unclassified=0, sourceHashes=HASHES,
                        rows=[dict(page=o[0], start=o[1], match=o[2], context=o[3], classification=r[2]) for o, r in zip(observed, ledger_rows)],
                        finiteQuestionChoices={'10a': dict(choose=2, options=[i[0] for i in ITEMS10], cardId=A10['id'], groupRowId='items')},
                        optionSelectionsMarkedAlike={'4b': dict(options=['site A', 'site B'], cardId=B4b['id'])})
whole = {}
for t in tasks:
    c = t['card']
    if '-complete' in c['id']:
        whole.setdefault('10-alt' if t['alternative'] else t['questionNumber'], []).append(dict(id=c['id'], parts=[g['label'] for g in c['taskGroups']], marks=c['totalMarks']))

REASONS = {
    'q1-a': 'Rows rebuilt to the printed table with the scale and drafting allowance (8, banded 8/6/4) it prints: 48 → 56. Wording lifted from the paper.',
    'q1-b': 'Reshaped to the printed criterion row; tariff unchanged (4).',
    'q2-a': 'Replaces an any-two pool that mixed a stray scheme phrase (“waterfall lip”) in with the two areas: both printed areas are required, two details each at notes 3 + sketches 3; tariff unchanged (24).',
    'q3-b': 'Replaces an any-two pool of scheme bullets with the printed notes 12 + sketch 12; tariff unchanged (24).',
    'q3-c': 'Split into the two printed advantages (2 for point + 3 for discussion); tariff unchanged (10).',
    'q4-a': 'Split into the three printed reasons (2 for point + 4 for discussion); tariff unchanged (18).',
    'q4-b': 'Replaces a pool of thirteen scheme bullets from both sites with the three printed considerations, marked alike for either site; tariff unchanged (18).',
    'q5-c-advantages': 'Split into the two printed advantages (1 for point + 2 for discussion); tariff unchanged (6).',
    'q5-c-disadvantages': 'Split into the two printed disadvantages (1 for point + 2 for discussion); tariff unchanged (6).',
    'q6-a': 'Split into three design features, each notes 5 + sketches 5; tariff unchanged (30).',
    'q6-b': 'Split into two added features, each notes 5 + sketches 5; tariff unchanged (20).',
    'q6-c': 'Split into the two printed advantages (2 for point + 3 for discussion); tariff unchanged (10).',
    'q7-a': 'Rows rebuilt to the printed table with the scale and drafting allowance (8, banded 8/6/4): 48 → 56.',
    'q7-b': 'Reshaped to the printed design-detail row; tariff unchanged (4).',
    'q8-a': 'Adds the printed pipework sizes (any two, 4) to the seven system items: 28 → 32.',
    'q8-b': 'Replaces two one-of-many scheme pools with the printed notes 6 + sketches 6; tariff unchanged (12).',
    'q8-c': 'Split into the two printed advantages and two disadvantages (1 for point + 3 for discussion); tariff unchanged (16).',
    'q9-c': 'Adds the printed associated-principle marks (2 each) to the two approaches (4 each): 8 → 12.',
    'q10-a': 'Now one card printing all three items with an any-two group over the scheme headings (notes 6 + sketches 6 each), replacing a pool that mixed in a principle list and an unrelated EPD phrase; tariff unchanged (24).',
    'q10-b-indoor-air-quality': 'Reshaped to the printed notes 6 + sketches 6; tariff unchanged (12).',
    'q10-b-space-heating': 'Reshaped to the printed notes 6 + sketches 6; tariff unchanged (12).',
    'q10-c': 'Split into the two printed advantages (2 for point + 4 for discussion); tariff unchanged (12); filed under passive design.',
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
                                reason='Question wording lifted from the paper. ' + REASONS[c['id'].removeprefix(PREFIX)]))
assert len(corrections) == 22

out = dict(schemaVersion=1, subjectId='construction-studies', year=2024, level='higher', lang='ev', sitting='main', paperKey='single',
           fileid='LC029ALP000EV.pdf', component='theory', status='Q1–Q10 and alternative Q10 source-reviewed draft; integration pending.',
           sourceHashes=HASHES, tasks=tasks, bindings=bindings, questionFigures=question_figures,
           addedIds=[t['card']['id'] for t in tasks if not t['correction']], corrections=corrections,
           selectionLedger=selection_ledger, questionRouteLedgers={q: dict(wholeRoutes=w) for q, w in whole.items()}, taxonomyGaps=[],
           questionsReviewed=[str(n) for n in range(1, 11)], unreviewedQuestions=[], alternativeQuestions=['10'])
(HERE / 'higher-2024-draft.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(tasks=len(tasks), added=len(out['addedIds']), corrected=len(corrections), figures=len(question_figures),
                      perQuestion={q: sum(1 for t in tasks if t['questionNumber'] == q and not t['alternative']) for q in QUESTIONS},
                      alternative=sum(1 for t in tasks if t['alternative']), wholeRoutes={q: len(w) for q, w in whole.items()})))
