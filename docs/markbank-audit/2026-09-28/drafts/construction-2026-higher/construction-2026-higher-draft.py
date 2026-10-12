"""Draft the 2026 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Question wording is lifted from the SEC paper: a narrowed task only deletes printed words.
Where the paper identifies a choice only by a circle on its drawing (Q9), the card names the
location after ' — ' using the marking scheme's own heading for it. Every row's verbatim is
printed in the scheme's mark tables (pages 43-53), checked against rendered pages. Unbanded
components (including point/discussion splits, which the notes describe) accept any whole
mark up to the published maximum; printed excellent/good/fair bands are kept as printed. Figures are exact 2x crops of the original PDFs.
"""
import copy
import hashlib
import json
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
R = HERE.parents[4]
P = 'paper-trail-corpus/exampapers/2026/LC029ALP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2026/LC029ALP000EV.pdf'
HASHES = {P: 'c470bc9009af7f39b2f4bd6c5e1182dd9ccf3190daa15ea8e3c4b75c3cebe0a4',
          S: 'e78fab89d53f74c61721efaee0e3371312bc52080ecfa45e5008e98c6905cd0d'}
ATTRIBUTION = 'SEC Leaving Certificate Construction Studies 2026 Higher Level — © State Examinations Commission.'
FP = 'construction-studies-2026-HL-'
PREFIX = 'cons-2026-hl-'
CROSS = 'construction-studies-higher-'
BAND8 = [0, 4, 6, 8]
PAGE = [48, 52, 568, 803]

for f, h in HASHES.items():
    assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f

FIGURES = {
    'q1-original': (P, 2, [45, 50, 575, 362], False),
    'q1-roof-section': (S, 4, PAGE, True),
    'q1-airtightness': (S, 5, [48, 482, 540, 722], True),
    'q2-original': (P, 2, [45, 362, 580, 765], False),
    'q2-entrance-access': (S, 6, PAGE, True),
    'q2-bathroom': (S, 7, PAGE, True),
    'q2-kitchen-plan': (S, 9, [176, 124, 450, 667], True),
    'q3-original': (P, 3, [45, 50, 580, 420], False),
    'q3-option-1': (S, 11, PAGE, True),
    'q3-option-2': (S, 12, PAGE, True),
    'q4-original': (P, 3, [45, 420, 580, 765], False),
    'q5-original': (P, 4, [45, 50, 575, 720], False),
    'q5-calculation': (S, 21, PAGE, True),
    'q5-moisture': (S, 22, PAGE, True),
    'q6-original': (P, 5, [45, 40, 580, 526], False),
    'q6-low-impact': (S, 23, PAGE, True),
    'q6-nature': (S, 25, PAGE, True),
    'q7-original': (P, 5, [45, 526, 580, 760], False),
    'q7-stairs': (S, 28, PAGE, True),
    'q8-original': (P, 6, [45, 50, 575, 395], False),
    'q8-stack': (S, 30, [250, 320, 568, 778], True),
    'q8-traps': (S, 31, [284, 296, 586, 708], True),
    'q9-original': (P, 6, [45, 395, 575, 770], False),
    'q9-details': (S, 33, [140, 100, 470, 752], True),
    'q10-original': (P, 7, [45, 50, 575, 400], False),
    'q10-areas': (S, 35, PAGE, True),
    'q10-retrofit': (S, 36, PAGE, True),
    'q10-blower-door': (S, 38, [240, 480, 552, 690], True),
    'q10-alt-original': (P, 7, [45, 440, 575, 705], False),
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
    '1': dict(page=2, title='Traditional cut roof section', concept='cut-roof-section',
              stem='The sketch shows a dwelling house with a traditional slated cut roof. The roof has a pitch of 30° and is highly insulated at ceiling joist level. The internal span of the house is 5.8 metres. The walls of the house are of 450 mm rendered concrete block construction with a full-fill insulated cavity.',
              note='Original sketch and specification retained. Construction, dimension and scale/drafting marks belong to part (a); the airtightness detail in (b) is marked separately. Any alternative detailing that meets current Building Regulations is acceptable.'),
    '2': dict(page=2, title='Designing for lifetime use', concept='lifetime-use',
              stem='Lifetime use of a dwelling should be a key consideration at the design stage.',
              note='Original garage-conversion plan retained. Both areas in (a) are required. The scheme guidelines and dimensions are typical best practice, not an exhaustive list.'),
    '3': dict(page=3, title='Revising a 1920s farmhouse layout', concept='farmhouse-layout',
              stem='The drawing shows the front elevation and ground floor plan of a farmhouse built in the 1920’s. The wall A-A is south-facing and the wall B-B is load-bearing. The owners wish to build a single-storey extension, no greater than 15 m² in area, to increase and revise the ground floor layout. Consideration at the design stage is to be given to: creating an open-plan kitchen/dining and living space; optimising daylight; retaining a bedroom and family bathroom on the ground floor.',
              note='Original elevation and plan retained. The scheme shows two acceptable layouts (a rear/north-west extension and a south extension); any well-reasoned layout meeting all three requirements is acceptable.'),
    '4': dict(page=3, title='Railway keeper’s cottage: thermal upgrade and heritage', concept='heritage-cottage',
              stem='The sketch shows a railway keepers cottage built over 130 years ago. These traditional cottages can be seen at railway crossing points throughout our rural landscape. They form an important part of our built heritage.',
              note='Original sketch retained. Part (a) chooses any two of three printed areas and part (b) any two of three printed principles: every finite route is kept, and an unchosen item never adds marks.'),
    '5': dict(page=4, title='Timber-frame wall: U-value, heat-loss cost and moisture', concept='timber-frame-wall',
              stem='Shown in the sketch is the proposed external wall design detail for a new house of timber frame construction.',
              note='All printed data are retained in the original question. Part (b) uses the U-value from part (a); the scheme’s worked answers are U = 0.136 W/m²°C and an annual cost of €40.27.'),
    '6': dict(page=5, title='Low-impact house connected to nature', concept='nature-connected-house',
              stem='The elevation and ground floor plan of a house are shown. The external walls are of timber frame construction with a rendered concrete block, locally sourced timber cladding, and stone finish. Space heating is provided using a renewable heat source. The house is designed to increase the occupants’ connection with nature and to have a low environmental impact.',
              note='Original elevation and plan retained. Features are open choices; the scheme lists typical examples. Its environmental and health statements are model points, not universal guarantees.'),
    '7': dict(page=5, title='Open riser stairs section', concept='open-riser-stairs',
              stem='The main hallway of a two-storey dwelling has an open riser wooden stairs. The newel post is 120 mm × 120 mm. The rise of the step should not exceed 175 mm.',
              note='Original sketch retained. Construction, dimension and scale/drafting marks belong to part (a); the two safety details in (b) are marked separately.'),
    '8': dict(page=6, title='First-floor en-suite drainage', concept='first-floor-drainage',
              stem='A bedroom with an en-suite bathroom is located on the first floor of a dwelling house.',
              note='Original sketch retained. All three appliances are required in part (b). Pipe sizes and gradients in the scheme are typical values.'),
    '9': dict(page=6, title='Preventing thermal bridging', concept='thermal-bridging',
              stem='A continuous thermal envelope is essential to prevent thermal bridging in a dwelling. The drawing shows a vertical section through the external leaf of a bungalow having a 450 mm concrete block wall with a 250 mm full-fill insulated cavity. The house has a truss roof and an insulated concrete ground floor. The window frame is thermally broken.',
              note='Original drawing with four circled locations retained. Part (a) chooses any three: every combination is kept, and each location keeps its own 16 marks. Locations are named with the marking scheme’s headings.'),
    '10': dict(page=7, title='EnerPHit retrofit', concept='enerphit-retrofit',
               stem='EnerPHit is a certified standard that can be achieved when retrofitting an older house to improve its energy efficiency. The sketch shows a bungalow which has been retrofitted to the EnerPHit Passive House standard.',
               note='Original sketch retained. The three building-fabric areas are an open choice, not a printed list; part (b) retrofits the same three areas chosen in (a).'),
}
ALT = dict(page=7, title='Indoor air quality (alternative Question 10)', concept='indoor-air-quality',
           stem='“It would be reasonable to assume that ensuring good indoor air quality would be a key factor when designing and constructing buildings. The term sick building syndrome became well known in the 1980’s and still lingers today, though largely associated with poorly air-conditioned offices. However, the health impacts of buildings are still poorly understood and rarely taken into account as a key priority when buildings are designed or renovated. Architects, when specifying building materials are mainly concerned with cost, availability, robustness and aesthetics, not their impacts on health.” Adapted from: Building Materials, Health and Indoor Air Quality: No Breathing Space by Tom Wooley',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the EnerPHit question.')
SCHEME_PAGES = {'1': [4, 5, 43], '2': [6, 7, 8, 9, 10, 44], '3': [11, 12, 13, 14, 15, 45], '4': [16, 17, 18, 19, 20, 46],
                '5': [21, 22, 47], '6': [23, 24, 25, 26, 27, 48], '7': [28, 49], '8': [29, 30, 31, 32, 50],
                '9': [33, 34, 51], '10': [35, 36, 37, 38, 39, 52], '10-alt': [40, 41, 53]}

tasks, bindings, cards = [], [], {}


def add(q, key, ref, text, rows, nodes, topics, figure, review, boundary, selection, groups=None, total=None, alt=False):
    meta = ALT if alt else QUESTIONS[q]
    qkey = '10-alt' if alt else q
    card = dict(id=f'{PREFIX}q{qkey}-{key}', subjectId='construction-studies', year=2026, level='higher', section='B',
                topicId=nodes[0], conceptId=f"{meta['concept']}-{key}", questionRef=f"2026 HL Q{'10-alt' if alt else q}{ref}",
                stem=meta['stem'], questionText=text, tariffModel={'kind': 'fixed'},
                totalMarks=total if total is not None else sum(r['marks'] for r in rows), rows=rows,
                questionFigureKey=f'{FP}q{qkey}-original', questionFigureIncludesPrompt=True)
    if figure:
        card['figureKey'] = FP + figure
    card['sourceMaterial'] = dict(kind='source-illustration', label=f"ORIGINAL QUESTION 10{' — ALTERNATIVE' if alt else ''}" if q == '10' else f'ORIGINAL QUESTION {q}',
                                  title=meta['title'], pages=[1, meta['page']], attribution=ATTRIBUTION, presentationNote=meta['note'])
    if groups:
        card['taskGroups'] = groups
    tasks.append(dict(questionNumber=q, alternative=alt, card=card, sourceChecks=checks(meta['page'], SCHEME_PAGES[qkey]),
                      boundaryReview=boundary, selectionReview=selection,
                      requiredQuestionFigures=[card['questionFigureKey']], requiredSolutionFigures=[FP + figure] if figure else []))
    bindings.append(dict(cardId=card['id'], markBankTopicId=nodes[0], canonicalTopicIds=nodes, canonicalTopicReview=review,
                         questionNumber=q, atlasTopicIds=[CROSS + t for t in topics]))
    cards[card['id']] = card
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
B1 = 'Scheme p43: (a) external wall 3 × 4, roof structure 4 × 4, eaves 4 × 4 (each 3 drawing + 1 annotation) = 44, four typical dimensions 4, scale 4 + drafting 4 banded excellent 8/good 6/fair 4 = 56; (b) airtightness detail 4. Complete 60. The scale/drafting allowance is printed within (a), so it stays with (a).'
S1 = 'One required half-roof section and one required airtightness detail. The scheme detail lists are indicative menus, not printed choices.'
A1 = add('1', 'a', '(a)',
         'To a scale of 1:10, draw a vertical section through one half of the roof structure, from just below eaves up to the ridge. Show one external wall and one rafter length. Include the typical construction details from 600 mm below the ceiling joists up to the ridge, and include three courses of slate at eaves. Include four typical dimensions.',
         [row('external-wall', 'External Wall – typical detailing', 12, 'Three external-wall details, 4 each (3 for drawing, 1 for annotation). Typical: external and internal render; 100 mm external and internal block leaves; wall ties; 250 mm full-fill insulated cavity; cavity closer; 100 mm × 75 mm wallplate(s).'),
          row('roof-structure', 'Roof Structure – typical detailing', 16, 'Four roof-structure details, 4 each (3 drawing, 1 annotation). Typical: 200 mm × 50 mm rafters at 400 mm centres; ceiling joists at 400 mm centres; 225 mm × 75 mm purlin; strut supporting the purlin; hanger; collar tie at each couple or at 1200 mm centres; ridge board; plasterboard with 350 mm insulation laid in three layers.'),
          row('eaves', 'Eaves detail – typical detailing', 16, 'Four eaves details, 4 each (3 drawing, 1 annotation). Typical: tilting fillet; fascia board, soffit and gutter (any two); 25 mm fascia ventilator and 50 mm proprietary eaves ventilator; wind-tightness barrier; breather membrane laid over the rafters; 50 mm × 30 mm slating battens; three courses of slates.'),
          row('dimensions', 'Four typical dimensions', 4, 'Four appropriate typical dimensions on the section.'),
          row('presentation', 'Scale - 4 marks Drafting - 4 marks', 8, 'Scale 4 and drafting 4, assessed together: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-3-8', 'cons-3-9', 'cons-3-10', 'cons-3-3', 'cons-6-2'],
         ['question-1-drawing-questions', 'roofs', 'walls', 'heat-loss-insulation'], 'q1-roof-section',
         'Scaled drawing (1.5) of a traditional cut roof (3.8) with slate covering and ceiling insulation (3.9), eaves (3.10), the cavity external wall (3.3) and insulation (6.2).',
         B1, S1)
B1b = add('1', 'b', '(b)',
          'On your drawing, show the typical design detailing that will ensure airtightness at the junction of the ceiling and the external wall.',
          [row('airtightness', 'Design detailing identified to ensure airtightness at the junction of the ceiling and the external wall.', 4,
               'Show and identify a detail that makes the ceiling-to-external-wall junction airtight, such as airtightness tape sealing the ceiling airtightness layer to the wall. Any other valid airtight detail is acceptable.')],
          ['cons-6-6', 'cons-6-5'], ['condensation-air-tightness'], 'q1-airtightness',
          'Airtight/vapour control layer at the ceiling junction (6.6) limiting uncontrolled air movement (6.5).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-roof-section', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p44: (a) entrance access 2 details × (notes 4 + sketches 4) = 16 and bathroom 2 details × (notes 4 + sketches 4) = 16; (a) 32. (b) three considerations × (notes 3 + sketches 3) = 18 plus dimensions (any two) 2 = 20. (c) two reasons × (2 point + 2 discussion) = 8. Complete 60.'
S2 = 'Part (a) asks for two guidelines at EACH printed area: both areas are required, separately marked tasks, not a choice. Guidelines, considerations and reasons are open responses.'
ENTRANCE = 'Such as: a level threshold (maximum 15 mm upstand, chamfered or rounded edges) with a recessed drainage channel and the internal floor flush; a 1000 mm minimum clear door opening; a slip-resistant approach path at 1:20 or flatter (ramps no steeper than 1:12, with level landings); a level landing of at least 1500 mm × 1500 mm outside the door and 300 mm clear space at the leading edge; a canopy or recess at least 900 mm deep; lever handles 800–1050 mm above floor level and low door-closer force; a vision panel; motion-sensor lighting.'
BATHROOM = 'Such as: an accessible bathroom on the entry level; a clear turning circle of at least Ø1500 mm (ideally Ø1800 mm); walls reinforced with 18 mm plywood or noggins for future grab rails; a level-access (wet-room) shower graded to a gully; a door opening outwards or sliding with at least 800 mm clear opening; a WC 450–480 mm high and a wall-hung basin; lever taps; large rocker switches or pull cords 900–1200 mm above floor level; slip-resistant flooring.'
a2 = []
for slug, item, verbatim, examples, nodes, topics, review in [
        ('entrance-access', 'entrance access', 'Entrance access', ENTRANCE, ['cons-1-2', 'cons-3-7'], ['planning-sustainability-environment', 'doors'],
         'Designing the built environment for lifetime use (1.2) at the entrance door, threshold and ironmongery (3.7).'),
        ('bathroom', 'bathroom', 'Bathroom', BATHROOM, ['cons-1-2'], ['planning-sustainability-environment'],
         'Designing the built environment for lifetime use (1.2); the scheme’s bathroom points are accessibility and layout, not drainage.')]:
    a2.append(add('2', f'a-{slug}', f'(a) — {item}',
                  f'Using notes and freehand sketches, discuss two best-practice guidelines that should be followed when designing for lifetime use at each of the following areas of a dwelling: {item}.',
                  [row('guideline-1', verbatim, 8, f'First guideline for the {item}: notes 4 and sketches 4. ' + examples),
                   row('guideline-2', verbatim, 8, f'Second, different guideline for the {item}: notes 4 and sketches 4. Do not credit the same guideline twice.')],
                  nodes, topics, f'q2-{slug}', review, B2, S2))
A2 = compose('2', 'a', '(a)', a2, 'q2-entrance-access', B2, S2,
             'Using notes and freehand sketches, discuss two best-practice guidelines that should be followed when designing for lifetime use at each of the following areas of a dwelling: entrance access; bathroom.',
             labels=['entrance access', 'bathroom'])
B2b = add('2', 'b', '(b)',
          'The drawing shows the ground floor plan of a draft design for an adjoining garage conversion. The homeowner wishes to convert the garage, so that a family member with reduced mobility can live independently. With reference to the design shown, using notes and freehand sketches, discuss three specific design considerations for the open-plan kitchen/dining and living area, that ensures ease of use by a person with reduced mobility. Indicate on your sketches, typical dimensions as appropriate.',
          [row('consideration-1', 'Design consideration 1', 6, 'Notes 3 and sketches 3, related to the plan shown. Such as: Ø1500 mm (ideally Ø1800 mm) turning circles and 1200 mm clear routes between furniture and units.'),
           row('consideration-2', 'Design consideration 2', 6, 'Notes 3 and sketches 3. Such as: worktops lowered to 760–820 mm with knee space (minimum 700 mm high × 600 mm deep) under the sink and hob; pull-out or pull-down storage within the 400–1200 mm reach zone.'),
           row('consideration-3', 'Design consideration 3', 6, 'Notes 3 and sketches 3. Such as: dining table with 1200 mm clearance and 700 mm clear underside; firm slip-resistant level floors (transitions no more than 5 mm); level threshold to the folding doors; sockets at least 400 mm and switches/thermostats no higher than 1200 mm. Three distinct considerations are needed.'),
           row('dimensions', 'Dimensions - Any two', 2, 'Two appropriate typical dimensions shown on the sketches.')],
          ['cons-1-2'], ['planning-sustainability-environment'], 'q2-kitchen-plan',
          'Accessible design of the built environment for a person with reduced mobility (1.2).', B2, S2)
C2 = add('2', 'c', '(c)', 'Discuss in detail two reasons why it is important to consider lifetime use at the design stage of a dwelling.',
         [row('reason-1', 'Reason 1 (2 for point, 2 for discussion)', 4, 'Point 2 and discussion 2. Such as: future-proofing so occupants can age in place; accessible features are far cheaper built in than retrofitted.'),
          row('reason-2', 'Reason 2 (2 for point, 2 for discussion)', 4, 'A second, different reason: point 2 and discussion 2. Such as: inclusivity for visitors and families with young children; fewer trips and falls; an adaptable house lasts longer and needs less new construction; wider market appeal and resale value.')],
         ['cons-1-2'], ['planning-sustainability-environment'], None, 'Lifetime-use design of the built environment (1.2).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-kitchen-plan', B2, S2, parts(A2, B2b, C2))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p45: (a) revised layout including extension, notes 18 + open-plan 3 + daylight 3 + bedroom/bathroom 3 = 27; (b) three reasons × (3 point + 4 discussion) = 21; (c) two benefits × (3 point + 3 discussion) = 12. Complete 60.'
S3 = 'The three design requirements are all required in one layout, not a choice. The scheme shows two alternative model layouts; layouts, reasons and benefits are open responses.'
A3 = add('3', 'a', '(a)', 'Using notes and freehand sketches, show a revised ground floor layout, that incorporates the proposed extension, and each of the above design requirements.',
         [row('layout', 'Revised internal layout for the ground floor including extension', 18, 'Notes and freehand sketch of a coherent revised plan with the extension (no more than 15 m²), respecting south-facing wall A-A and load-bearing wall B-B. The scheme shows a rear/north-west extension and a south extension as alternatives.'),
          row('open-plan', 'Create an open-plan kitchen/dining and living area', 3, 'An open-plan kitchen/dining and living space, for example zoned by a kitchen island.'),
          row('daylight', 'Optimising daylight into the ground floor', 3, 'Daylight optimised, for example living spaces on the south side with large south-facing openings, or glazing on three sides of a south extension.'),
          row('bedroom-bathroom', 'Retaining a downstairs bathroom and bedroom', 3, 'A bedroom and family bathroom retained on the ground floor, for example as a private wing near the existing plumbing.')],
         ['cons-1-2', 'cons-7-4', 'cons-6-4'], ['planning-sustainability-environment', 'windows-light'], 'q3-option-1',
         'Layout design within the built environment (1.2), good daylighting (7.4) and solar gain (6.4).', B3, S3)
B3b = add('3', 'b', '(b)', 'Discuss three reasons for your proposed design layout.',
          [row(f'reason-{i}', f'Reason {i} (3 for point, 4 for discussion)', 7, note) for i, note in [
              (1, 'Point 3 and discussion 4. Such as: environmental performance and passive solar gain from the south-facing wall A-A, with light reaching deep into the plan.'),
              (2, 'Point 3 and discussion 4. Such as: functional zoning and social connection in one open space, with no wasted hallway.'),
              (3, 'Point 3 and discussion 4. Such as: privacy and acoustic separation of the bedroom wing; services grouped near existing plumbing; ground-floor bedroom and bathroom for lifetime use. Three distinct reasons are needed.')]],
          ['cons-1-2', 'cons-6-4', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'], 'q3-option-2',
          'Reasons drawn from layout design (1.2), solar gain (6.4) and daylight (7.4).', B3, S3)
C3 = add('3', 'c', '(c)', 'Discuss two benefits to the occupants of revising the internal layout of an existing house.',
         [row(f'benefit-{i}', f'Benefit {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: better use of space and flow with fewer partitions and dark hallways; more daylight and ventilation.'),
             (2, 'A second, different benefit: point 3 and discussion 3. Such as: thermal comfort and lower bills from south-facing living zones; adaptability for changing needs; quieter, more private zones; higher property value.')]],
         ['cons-1-2'], ['planning-sustainability-environment'], None, 'Benefits of revising the layout of an existing dwelling (1.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-option-1', B3, S3, parts(A3, B3b, C3))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p46: (a) two selected areas, each notes 8 + sketches 12 = 20; (a) 40. (b) two selected principles, each discussion/notes 10; (b) 20. Complete 60.'
S4 = 'Choice is not a route: part (a) (any two of three printed areas) and part (b) (any two of three printed principles) are each ONE card printing every item, with one any-two group over the scheme headings; the complete question composes the two.'
AREAS = [
    ('stone-wall', '500 mm solid external wall of stone construction, uninsulated, with an internal lime render', 'stone wall',
     'Such as: keep the wall breathable, with layers more vapour-permeable towards the outside and no impermeable vapour barriers; use hygroscopic natural insulation (hemp/hempcrete, lime, wood fibre, cork, sheep’s wool); rake out and repoint with lime mortar by hand (joints raked to twice their width, dampened first, filled in stages, protected with hessian while it carbonates); apply hempcrete internally and allow 4–6 weeks to dry, then lime render, or a three-coat lime plaster (scud coat, haired scratch coat, float coat, lime-putty finish).',
     ['cons-1-1', 'cons-3-3', 'cons-6-2'], ['conservation-restoration', 'walls', 'heat-loss-insulation'], 'q4-stone-wall',
     'Conserving an historic building (1.1) by upgrading its solid external wall (3.3) with breathable insulation (6.2).'),
    ('cut-roof', 'uninsulated traditional cut roof with natural slate', 'cut roof',
     'Such as: remove and set aside the slates, cleaning only their undersides; check and repair decayed rafters, wallplate and fascia in the same species and profile with traditional joints; treat new timber (boron); fit a vapour-permeable breathable membrane with counter-battens for ventilation; insulate with hygroscopic materials (sheep’s wool between rafters, wood fibre board above or below); keep the roof ventilated; re-lay the slates with the heaviest at the eaves, replacing broken ones with reclaimed slate; period cast-iron rainwater goods.',
     ['cons-1-1', 'cons-3-9', 'cons-6-2'], ['conservation-restoration', 'roofs', 'heat-loss-insulation'], 'q4-cut-roof',
     'Conserving an historic roof (1.1) while adding breathable roof insulation under natural slate (3.9, 6.2).'),
    ('sash-windows', 'single-glazed, softwood sliding sash windows', 'sash windows',
     'Such as: repair rather than replace the original sashes, using a specialist conservation joiner; remove sashes and glass carefully, recording positions; replace only rotten timber in the same species and profiles with traditional joints and animal glue; free the pulleys, renew the sash cords and reuse the weights; reglaze with linseed-oil putty (salvaged or sourced float glass); repaint with non-toxic paint; add discreet secondary glazing to cut heat loss; record the repair.',
     ['cons-1-1', 'cons-3-5', 'cons-3-6'], ['conservation-restoration', 'windows-light'], 'q4-sash-windows',
     'Conserving historic windows (1.1): sash window repair (3.5) and glazing upgrades (3.6).'),
]
PRINCIPLES = [
    ('conservation-original-materials', 'conservation of original materials',
     'Such as: preserves authenticity and significance; traditional materials have qualities modern replacements cannot match; repair is usually more sustainable than replacement; original fabric records the building’s age and history.',
     ['cons-1-1'], ['conservation-restoration'], 'Conservation of historic fabric (1.1).'),
    ('breathable-structure', 'breathable structure',
     'Such as: moisture is not trapped in walls, floors and roofs; less risk of damp, mould and timber decay; protects masonry from freeze–thaw and salt damage; healthier indoor environment; the building performs as originally intended.',
     ['cons-1-1', 'cons-6-6'], ['conservation-restoration', 'condensation-air-tightness'], 'Conservation (1.1) of a vapour-open fabric that avoids condensation (6.6).'),
    ('respect-built-heritage', 'respect for our built heritage',
     'Such as: understand the building’s significance before work; preserve distinctive features and craftsmanship; make sympathetic alterations; follow conservation principles and guidelines; heritage buildings are irreplaceable cultural resources.',
     ['cons-1-1'], ['conservation-restoration'], 'Respect for historic buildings (1.1).'),
]
AREA_HEADINGS = ['Thermal upgrading of solid stone external wall', 'Thermal upgrading of traditional cut roof',
                 'Original sliding sash windows-softwood and single glazed']
PRINCIPLE_HEADINGS = ['Conservation of Original Materials', 'Breathable Structure', 'Respect for Our Built Heritage']
A4 = add('4', 'a', '(a)',
         'A survey of the cottage reveals: ' + '; '.join(a[1] for a in AREAS) + '. Select any two of the above areas and, using notes and freehand sketches, describe in detail the steps involved in upgrading the thermal performance of each area selected in a manner that respects the original character of the cottage.',
         [dict(id='areas', kind='anyN', verbatim='Steps involved in upgrading the thermal performance of each area selected', marks=40,
               contextNote='Any two of the three areas, each notes 8 and sketches 12 = 20, respecting the cottage’s character. ' + ' '.join(f'{a[2].capitalize()}: ' + a[3].removeprefix('Such as: ') for a in AREAS),
               group=dict(claimMax=2, perOption=20, options=AREA_HEADINGS))],
         list(dict.fromkeys(n for a in AREAS for n in a[4])), list(dict.fromkeys(t for a in AREAS for t in a[5])), None,
         'The union of the three printed areas: ' + ' '.join(a[7] for a in AREAS), B4, S4)
B4b = add('4', 'b', '(b)',
          'Discuss the importance of any two of the following when restoring traditional heritage buildings: ' + '; '.join(p[1] for p in PRINCIPLES) + '.',
          [dict(id='principles', kind='anyN', verbatim='Importance when restoring traditional heritage buildings', marks=20,
                contextNote='Any two of the three principles, each discussion/notes 10. ' + ' '.join(f'{p[1].capitalize()}: ' + p[2].removeprefix('Such as: ') for p in PRINCIPLES),
                group=dict(claimMax=2, perOption=10, options=PRINCIPLE_HEADINGS))],
          list(dict.fromkeys(n for p in PRINCIPLES for n in p[3])), list(dict.fromkeys(t for p in PRINCIPLES for t in p[4])), None,
          'The union of the three printed principles: ' + ' '.join(p[5] for p in PRINCIPLES), B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b], None, B4, S4, parts(A4, B4b))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p47: (a) tabulation 3, external and internal surface resistances 3 + 3, seven material/cavity resistances 7 × 3 = 21, total resistance 3, U-value 3 = 36; (b) heat-loss formula 3, heating duration 3, kJ per year 3, kg of pellets 3, annual cost 3 = 15; (c) notes/discussion 3 + sketch 6 = 9. Complete 60.'
S5 = 'Required calculations and one required detail; no printed choice. Part (b) depends on the U-value from (a); the scheme marks each later step on the candidate’s own value.'
A5 = add('5', 'a', '(a)',
         'Calculate the U-value of the proposed wall, given the construction has the following sequence and data: External render thickness 16 mm External concrete block thickness 100 mm Clear cavity width 60 mm Oriented Strand Board (OSB) thickness 12 mm Timber stud thickness 250 mm Insulation between studs thickness 250 mm Oriented Strand Board (OSB) thickness 12 mm Plasterboard thickness 12.5 mm. Thermal data of the external wall: Resistance of external surface (R) 0.048 m2 ºC/W; Resistivity of external render (r) 2.170 m ºC/W; Conductivity of concrete block (k) 1.440 W/m ºC; Resistance of clear cavity (R) 0.440 m2 ºC/W; Conductivity of OSB (k) 0.130 W/m ºC; Conductivity of insulation (k) 0.039 W/m ºC; Conductivity of OSB (k) 0.130 W/m ºC; Conductivity of plasterboard (k) 0.250 W/m ºC; Resistance of internal surface (R) 0.130 m2 ºC/W. Note: The timber studs need not be considered in your calculations.',
         [row('tabulation', 'Tabulation', 3, 'Set out the layers, thicknesses (in metres), k or r values and resistances in a table.'),
          row('surfaces', 'External surface resistance', 6, 'External surface resistance 0.048 and internal surface resistance 0.130 m²°C/W, 3 each.'),
          row('layers', 'Formulae: R=T/k R=T × r', 21, 'Seven layer resistances, 3 each: render 0.016 × 2.170 = 0.035; concrete block 0.100 ÷ 1.440 = 0.069; clear cavity 0.440 (given); OSB 0.012 ÷ 0.130 = 0.092; insulation 0.250 ÷ 0.039 = 6.410; OSB 0.092; plasterboard 0.0125 ÷ 0.250 = 0.050 m²°C/W. The studs are ignored, as the question states.'),
          row('total-resistance', 'Total resistance', 3, 'Total resistance Rt = 7.367 m²°C/W (sum of all resistances).'),
          row('u-value', 'Calculation of U-value (w/m2 °C or w/m2k)', 3, 'U = 1 ÷ Rt = 1 ÷ 7.367 = 0.136 W/m²°C, with units.')],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Thermal resistance and U-value calculation (6.1).', B5, S5)
B5b = add('5', 'b', '(b)',
          'Using the U-value of the wall obtained at 5(a) above and the following data, calculate the cost of heat lost annually through this wall: area of external wall 144 m2; average internal temperature 20 ºC; average external temperature 7 ºC; heating period 6 hours daily for 33 weeks per annum; cost of wood pellets 55 cent per kg; calorific value of wood pellets 17350 kJ per kg; 1000 watts 1 kJ per second.',
          [row('heat-loss', 'Heat loss formula and calculation', 3, 'Heat loss = U × area × temperature difference = 0.136 × 144 × (20 − 7) = 254.592 W (J/s).'),
           row('duration', 'Heating duration for one year', 3, 'Heating time = 60 × 60 × 6 × 7 × 33 = 4,989,600 seconds per year.'),
           row('energy', 'k/Joules calculation for one year', 3, 'Energy = 254.592 × 4,989,600 ÷ 1000 = 1,270,312.243 kJ per year.'),
           row('pellets', 'Kgs of wood pellets for one year', 3, 'Wood pellets = 1,270,312.243 ÷ 17,350 = 73.2168 kg per year.'),
           row('cost', 'Annual cost of heat loss', 3, 'Cost = 73.2168 × €0.55 = €40.27 per year. The single-formula method (U × area × ΔT × seconds × cost ÷ (calorific value × 1000)) gives the same €40.27.')],
          ['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation',
          'Heat-loss and running-cost calculation (6.3) from the U-value (6.1).', B5, S5)
C5 = add('5', 'c', '(c)', 'Using notes and freehand sketches, show the typical design detailing that will prevent the build-up of moisture within the timber frame structure.',
         [row('notes', 'Notes/discussion', 3, 'Such as: a breather membrane on the outer face that lets vapour escape but sheds external water, with taped joints; a vapour control layer on the warm (inner) side, continuous and sealed at every lap, so warm humid air cannot reach the frame and cause interstitial condensation and rot.'),
          row('sketch', 'Sketch', 6, 'Sketch of the wall section locating the breather membrane outside the frame and the vapour control layer on the warm side.')],
         ['cons-6-6', 'cons-3-3'], ['condensation-air-tightness', 'walls'], 'q5-moisture',
         'Vapour control and interstitial condensation (6.6) in a timber-frame external wall (3.3).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(A5, B5b, C5))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p48: (a) three features × (notes 6 + sketches 6) = 36; (b) two features × (notes 4 + sketches 4) = 16; (c) two advantages × (2 point + 2 discussion) = 8. Complete 60.'
S6 = 'Open design features and advantages; no printed choice pool. Features must relate to the design shown.'
A6 = add('6', 'a', '(a)', 'With reference to the design shown, discuss using notes and freehand sketches, three features of the design that contribute to the house having a low environmental impact.',
         [row(f'feature-{i}', f'Design Feature {i}', 12, note) for i, note in [
             (1, 'Notes 6 and sketches 6. Such as: sustainable materials — locally sourced timber cladding with low transport emissions, timber frame as a renewable carbon store, durable low-maintenance natural stone.'),
             (2, 'Notes 6 and sketches 6. Such as: passive solar gain from extensive south-facing glazing, reducing space-heating demand; or a compact form with a low surface-to-volume ratio.'),
             (3, 'Notes 6 and sketches 6. Such as: a renewable heat source (heat pump or geothermal) in a well-insulated envelope; or indoor–outdoor living with cross-ventilation and daylight; or planting and permeable surfaces for drainage and biodiversity. Three distinct features are needed.')]],
         ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-low-impact',
         'Low environmental impact of the built environment (1.2) through solar gain (6.4) and an insulated envelope (6.2).', B6, S6)
B6b = add('6', 'b', '(b)', 'Discuss using notes and freehand sketches, two features of the design that contribute to increasing the occupants’ connection with nature.',
          [row(f'feature-{i}', f'Design Feature {i}', 8, note) for i, note in [
              (1, 'Notes 4 and sketches 4. Such as: the central courtyard garden at the heart of the plan, with views of greenery from living and circulation areas.'),
              (2, 'Notes 4 and sketches 4. Such as: large floor-to-ceiling glazing and folding doors framing the landscape; natural local stone and timber; daylight throughout; level access to terraces; cross-ventilation; the courtyard water feature. Two distinct features are needed.')]],
          ['cons-1-2', 'cons-7-4'], ['sustainability-the-environment', 'windows-light'], 'q6-nature',
          'Design of the built environment (1.2) using daylight and views (7.4).', B6, S6)
C6 = add('6', 'c', '(c)', 'Discuss in detail two advantages of designing a house that will enhance the connection to nature for the occupants.',
         [row(f'advantage-{i}', f'Advantage {i} (2 for point, 2 for discussion)', 4, note) for i, note in [
             (1, 'Point 2 and discussion 2. Such as: improved mental health and well-being; daylight regulating circadian rhythms and sleep.'),
             (2, 'A second, different advantage: point 2 and discussion 2. Such as: natural ventilation and cooling; passive solar savings; a richer sensory environment; more outdoor living and activity; a sense of more space; appreciation of biodiversity.')]],
         ['cons-1-2'], ['sustainability-the-environment'], None, 'Benefits of nature-connected design (1.2).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-low-impact', B6, S6, parts(A6, B6b, C6))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p49: (a) best eight construction details × 5 (4 drawing + 1 annotation) = 40, three dimensions 6, scale 4 + drafting 4 banded excellent 8/good 6/fair 4 = 54; (b) two safety design details × 3 = 6. Complete 60.'
S7 = 'One required section and two required safety details; the detail list is a marking menu, not a printed choice.'
A7 = add('7', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the centre of the stairs. The section should show the typical construction details through the bottom three steps of the stairs, showing the newel post, balusters, string, and handrail. Include the typical dimensions of three structural members of the stairs.',
         [row('construction', 'Vertical section through centre of an open riser stairs', 40, 'Best eight details, 5 each (4 drawing + 1 annotation). Marking menu: closed string; string capping; newel post (120 mm × 120 mm); riser; tread; handrail; balusters; nosing; pitch line; jointing of handrail to newel post, string to newel post, riser to tread, and baluster to handrail/string. Keep the rise at or below 175 mm.'),
          row('dimensions', 'Three dimensions', 6, 'Typical dimensions of three structural members (6 marks).'),
          row('presentation', 'Scale - 4 marks Drafting - 4 marks', 8, 'Scale 4 and drafting 4, assessed together: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-4-4', 'cons-10-1'], ['stairs'], 'q7-stairs', 'Stair construction (4.4) and its joints (10.1).', B7, S7)
B7b = add('7', 'b', '(b)', 'On your drawing, show two design details of an open riser stairs that will ensure the stairs is safe for all users.',
          [row('detail-1', 'Design detail 1', 3, 'One safety detail on the drawing. Such as: gaps between treads and between balusters that will not let a 100 mm sphere pass; handrail 840–900 mm above the pitch line.'),
           row('detail-2', 'Design detail 2', 3, 'A second, different safety detail. Such as: going at least 220 mm and rise no more than 175 mm here, 2R + G between 550 and 700 mm, pitch no more than 42°, guarding that is not easily climbed, 2 m headroom.')],
          ['cons-4-4'], ['stairs'], 'q7-stairs', 'Stair safety requirements (4.4).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-stairs', B7, S7, parts(A7, B7b))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p50: (a) two considerations × (4 point + 4 discussion) = 16; (b) one above-ground layout including shower, wash basin and W.C.: notes 12, sketch 16, any four dimensions 4 = 32; (c) one odour-prevention detail: notes 6 + sketches 6 = 12. Complete 60.'
S8 = 'All three printed appliances are required in one layout, marked as a whole: not a choice and not separately priced. Considerations and the odour detail are open.'
A8 = add('8', 'a', '(a)', 'Discuss two considerations that should be taken into account when planning the drainage layout of a bathroom located on the first floor of a house.',
         [row(f'consideration-{i}', f'Consideration {i}', 8, note) for i, note in [
             (1, 'Point 4 and discussion 4. Such as: place the bathroom above or near ground-floor wet areas for a short run to the SVP; run pipes parallel to joists and limit notching (or use engineered joists).'),
             (2, 'A second, different consideration: point 4 and discussion 4. Such as: self-cleansing falls (waste 1:18–1:40, soil 1:40–1:80); acoustic lagging of pipes; access for cleaning; venting to prevent siphonage; deep-seal traps; floor depth for shower traps and tanking.')]],
         ['cons-5-6'], ['drainage'], None, 'Planning above-ground sanitary drainage (5.6).', B8, S8)
B8b = add('8', 'b', '(b)', 'Using notes and freehand sketches, show the above-ground pipework necessary for the safe removal of waste from the following appliances: shower; water closet (W.C.); wash basin. Include on your sketch typical sizes of the soil and vent pipe (svp) and the waste pipe from each appliance.',
          [row('notes', 'Typical layout above-ground', 12, 'Notes on a single-stack layout: 110 mm uPVC SVP vented above the roof (or an air admittance valve); W.C. connected by a short 110 mm branch at 1:40–1:80 with its integral 75 mm seal; shower waste 40–50 mm with a 75 mm deep-seal trap at 1:18–1:40; basin waste (typically 32 mm) with a deep-seal trap; small branches not entering the SVP within 200 mm of the W.C. connection.'),
           row('sketch', 'Above-ground pipework necessary for the safe removal of waste', 16, 'Sketch showing all three appliances connected to the stack.'),
           row('dimensions', 'Typical dimensions - Any four', 4, 'Any four typical sizes, such as SVP 110 mm, W.C. branch 110 mm, shower waste 40–50 mm, basin waste 32 mm.')],
          ['cons-5-6'], ['drainage'], 'q8-stack', 'Single-stack above-ground drainage (5.6).', B8, S8)
C8 = add('8', 'c', '(c)', 'Using notes and freehand sketches, outline one design detail in above-ground pipework that will prevent foul odours entering a dwelling.',
         [row('notes', 'Design detailing to prevent foul odours entering the building', 6, 'Notes on one detail. Such as: a deep-seal trap holding a 75 mm water seal; a vented stack; correct branch gradients and diameters; an air admittance valve; anti-siphon traps; avoiding cross-flow; airtight joints tested during construction.'),
          row('sketches', 'Sketches', 6, 'Sketch of the chosen detail, for example a trap with its water seal.')],
         ['cons-5-6'], ['drainage'], 'q8-traps', 'Traps and venting in sanitary pipework (5.6).', B8, S8)
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-stack', B8, S8, parts(A8, B8b, C8))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p51: (a) three selected locations, each note 8 + sketches 8 = 16; (a) 48. (b) two benefits × (3 point + 3 discussion) = 12. Complete 60.'
S9 = 'Choice is not a route: part (a) (any three of the FOUR circled locations) is ONE card with one any-three group over the four locations, named by the scheme headings; the complete question composes (a) and (b).'
LOCATIONS = [
    ('wall-roof', 'Wall and roof junction', ['cons-6-2', 'cons-3-10', 'cons-3-3'], ['heat-loss-insulation', 'roofs', 'walls'],
     'Such as: wall and roof insulation meeting to keep the envelope continuous; a thermal break at the wallplate (insulated barrier or thermal blocks); cavity insulation continued and the eaves detailed to avoid a cold bridge; no direct structural or steel connections bridging the insulation.',
     'Thermal bridging (6.2) at the eaves (3.10) of the external wall (3.3).'),
    ('window-head', 'Window Head', ['cons-6-2', 'cons-3-6', 'cons-3-4'], ['heat-loss-insulation', 'windows-light', 'walls'],
     'Such as: wall insulation continuous with the window frame insulation; thermally broken frame and insulated cavity closers at the opening; insulated lintels or thermal-break details above the window; airtight seals around the frame.',
     'Thermal bridging (6.2) at the window head (3.6) and lintel (3.4).'),
    ('window-cill', 'Window cill', ['cons-6-2', 'cons-3-6'], ['heat-loss-insulation', 'windows-light'],
     'Such as: wall insulation and cavity closers continued around the opening; an insulated cill detail or insulation behind the concrete cill; thermally broken frame with insulated perimeter seals; airtight frame-to-wall junction.',
     'Thermal bridging (6.2) at the window cill (3.6).'),
    ('wall-floor', 'Wall and floor junction', ['cons-6-2', 'cons-4-2', 'cons-3-3'], ['heat-loss-insulation', 'floors', 'walls'],
     'Such as: floor and wall insulation continuous; insulated slab-edge (perimeter) detail; cavity insulation taken down to meet the floor insulation; thermal blocks where the slab abuts the external wall, with no exposed concrete bridging inside to outside.',
     'Thermal bridging (6.2) at the ground floor (4.2) to external wall (3.3) junction.'),
]
STEM9A = 'Using notes and freehand sketches, show best practice design detailing that will prevent the formation of a thermal bridge at'
A9 = add('9', 'a', '(a)', STEM9A + ' any three locations circled on the drawing.',
         [dict(id='locations', kind='anyN', verbatim='Best practice design detailing to prevent thermal bridging', marks=48,
               contextNote='Any three of the four circled locations, each note 8 and sketches 8 = 16, showing the continuous insulation line. ' + ' '.join(f'{loc[1]}: ' + loc[4].removeprefix('Such as: ') for loc in LOCATIONS),
               group=dict(claimMax=3, perOption=16, options=[loc[1] for loc in LOCATIONS]))],
         list(dict.fromkeys(n for loc in LOCATIONS for n in loc[2])), list(dict.fromkeys(t for loc in LOCATIONS for t in loc[3])), 'q9-details',
         'The union of the four circled locations: ' + ' '.join(loc[5] for loc in LOCATIONS), B9, S9)
B9b = add('9', 'b', '(b)', 'Discuss in detail two benefits to the homeowner of eliminating thermal bridging.',
          [row(f'benefit-{i}', f'Benefit {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
              (1, 'Point 3 and discussion 3. Such as: less heat loss at junctions and better thermal comfort; lower heating bills and fuel use.'),
              (2, 'A second, different benefit: point 3 and discussion 3. Such as: no cold-spot condensation, damp and mould, so a healthier home; lower carbon emissions; a better BER and market value; longer-lasting building materials; a more efficient heating system.')]],
          ['cons-6-2', 'cons-6-6'], ['heat-loss-insulation', 'condensation-air-tightness'], None,
          'Benefits of eliminating thermal bridges (6.2), including avoiding surface condensation (6.6).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b], 'q9-details', B9, S9, parts(A9, B9b))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p52: (a) three areas × (1 selection + 5 reason) = 18; (b) three retrofits × (notes 5 + sketches 5) = 30; (c) one test: notes 6 + sketches 6 = 12. Complete 60.'
S10 = '"Select any three areas of the building fabric" names no printed list: an open choice, kept as one response. Part (b) retrofits the areas chosen in (a). The OR alternative is a separate Question 10 route.'
A10 = add('10', 'a', '(a)', 'Select any three areas of the building fabric of an older house that would need to be retrofitted to achieve the EnerPHit Passive House standard. Give a reason for each area selected.',
          [row(f'selection-{i}', f'Selection {i} (1 for selection, 5 for reason)', 6, note) for i, note in [
              (1, 'Area 1 and its reason (1 + 5). Such as: external walls — external wall insulation or pumped cavity bead to cut the U-value and junction thermal bridges.'),
              (2, 'Area 2 and its reason (1 + 5). Such as: ground floor — sub-floor insulation under a new slab; or the roof/attic — 400 mm+ insulation.'),
              (3, 'Area 3 and its reason (1 + 5). Such as: windows and doors — triple-glazed, airtight units; the airtightness layer — sealed membrane and tapes for a low air-change rate; thermal-bridge elimination at junctions. Three distinct areas are needed.')]],
          ['cons-6-2', 'cons-6-5'], ['passive-design'], 'q10-areas', 'Retrofitting insulation (6.2) and airtightness/ventilation (6.5) for a passive standard.', B10, S10)
B10b = add('10', 'b', '(b)', 'Discuss in detail, using notes and freehand sketches, how you would retrofit each of the areas you specified at 10(a) above, to achieve the EnerPHit Passive House standard.',
           [row(f'retrofit-{i}', f'Retrofit area {i} (5 for notes, 5 for sketches)', 10, note) for i, note in [
               (1, 'Notes 5 and sketches 5 for the first area. Such as: 200 mm+ EPS or mineral-wool external insulation, adhesive and mechanical fixings, meshed base coat and breathable render, taken below the DPC to the footing.'),
               (2, 'Notes 5 and sketches 5 for the second area. Such as: excavate and relay the floor with radon barrier/DPM, 150–200 mm PIR/EPS and a perimeter upstand meeting the wall insulation; or an airtight membrane under the ceiling joists with 400 mm cross-laid insulation and eaves ventilation.'),
               (3, 'Notes 5 and sketches 5 for the third area. Such as: Passive House certified triple glazing moved out into the insulation line and taped airtight inside and out; or a continuous airtight layer with tapes and grommets at every junction and penetration, needed for MVHR to work.')]],
           ['cons-6-2', 'cons-6-5'], ['passive-design'], 'q10-retrofit', 'Retrofit insulation (6.2) and airtightness (6.5) details.', B10, S10)
C10 = add('10', 'c', '(c)', 'Describe using notes and freehand sketches, one test that could be carried out to determine the efficiency of the retrofit.',
          [row('notes', 'Testing method to determine efficiency of the retrofit', 6, 'Such as the blower door test: a calibrated fan in a temporary door frame, with a manometer, depressurises or pressurises the house to 50 Pa with external openings closed, internal doors open and vents sealed; the airflow needed gives the leakage rate (EnerPHit target 1.0 air change per hour at 50 Pa); leaks are found with thermal imaging or smoke pencils.'),
           row('sketches', 'Sketches', 6, 'Sketch of the test set-up.')],
          ['cons-6-5'], ['condensation-air-tightness', 'passive-design'], 'q10-blower-door', 'Airtightness testing of the envelope (6.5).', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-retrofit', B10, S10, parts(A10, B10b, C10))

BALT = 'Scheme p53: (a) three discussion points × (5 point + 5 discussion) = 30; (b) three guidelines × (5 point + 5 discussion) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the EnerPHit question. Its parts are open responses.'
AA = add('10', 'a', '(a)', 'Discuss the above statement in detail.',
         [row(f'point-{i}', f'Discussion Point {i}', 10, note) for i, note in [
             (1, 'Point 5 and discussion 5. Such as: people spend most of their lives indoors, yet health is often overlooked behind cost, appearance, durability and availability; sick building syndrome symptoms linked to poor ventilation, mould and chemical emissions.'),
             (2, 'Point 5 and discussion 5. Such as: more airtight buildings need carefully designed ventilation; VOCs and formaldehyde from paints, adhesives, finishes and composite boards; condensation and mould from poor detailing, especially in Ireland’s damp climate.'),
             (3, 'Point 5 and discussion 5. Such as: health impacts are harder to measure and appear later, while healthier materials can cost more; Passive House/EnerPHit ventilation with heat recovery, low-VOC materials, daylight and newer certification standards show a growing focus on wellbeing. Three distinct, well-argued points are needed.')]],
         ['cons-6-5', 'cons-6-6'], ['condensation-air-tightness', 'wood-rot-ventilation'], None,
         'Indoor air quality: ventilation rates (6.5) and condensation/mould (6.6).', BALT, SALT, alt=True)
AB = add('10', 'b', '(b)', 'Propose three best practice guidelines that would ensure a healthy indoor environment in our homes.',
         [row(f'guideline-{i}', f'Guideline {i}', 10, note) for i, note in [
             (1, 'Point 5 and discussion 5. Such as: continuous balanced ventilation (demand-controlled or MVHR) removing moisture and pollutants.'),
             (2, 'Point 5 and discussion 5. Such as: control moisture at source with vapour control, airtightness and extract ventilation; low-VOC, non-toxic materials.'),
             (3, 'Point 5 and discussion 5. Such as: good daylight without glare; stable temperatures with insulation and no thermal bridges; acoustic comfort; filtration; occupant control of heating and ventilation. Three distinct guidelines are needed.')]],
         ['cons-6-5', 'cons-6-6'], ['condensation-air-tightness', 'wood-rot-ventilation'], None,
         'Healthy indoor environment through ventilation (6.5) and moisture control (6.6).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, parts(AA, AB), alt=True)

# ---------------------------------------------------------------- ledgers
ledger_rows = [
    (1, 'Answer any', 'Whole-exam selection: any five of the ten questions; all question banks retained, no full-exam Cartesian cards.'),
    (3, 'Select', 'Q4(a) closed choose-two of three printed areas: one card with an any-two group (choice is not a route).'),
    (3, 'any two', 'Q4(a) closed choose-two of three printed areas (same directive as the preceding Select).'),
    (3, 'any two', 'Q4(b) closed choose-two of three printed principles: one card with an any-two group (choice is not a route).'),
    (6, 'any three', 'Q9(a) closed choose-three of the four circled locations: one card with an any-three group (choice is not a route).'),
    (7, 'Select', 'Q10(a) open selection: "any three areas of the building fabric" prints no finite list; one open response.'),
    (7, 'any three', 'Q10(a) open selection (same directive as the preceding Select).'),
    (7, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.'),
    (7, 'or', 'Prose inside the quoted passage ("designed or renovated"), not a selection directive.'),
]
import re  # noqa: E402
pattern = r'\b(?:choose|select|one\s+of|any\s+\w+|either|or|answer\s+\w+)\b'
observed = []
with fitz.open(R / P) as pdf:
    for i, p in enumerate(pdf):
        text = ' '.join(p.get_text().split())
        observed.extend((i + 1, m.start(), m.group(), text[max(0, m.start() - 80):m.end() + 80]) for m in re.finditer(pattern, text, re.I))
assert [(o[0], o[2]) for o in observed] == [(r[0], r[1]) for r in ledger_rows], observed
selection_ledger = dict(pattern=pattern, unclassified=0, sourceHashes=HASHES,
                        rows=[dict(page=o[0], start=o[1], match=o[2], context=o[3], classification=r[2]) for o, r in zip(observed, ledger_rows)],
                        finiteQuestionChoices={
                            '4a': dict(choose=2, options=[a[0] for a in AREAS], cardId=A4['id'], groupRowId='areas'),
                            '4b': dict(choose=2, options=[p[0] for p in PRINCIPLES], cardId=B4b['id'], groupRowId='principles'),
                            '9a': dict(choose=3, options=[loc[0] for loc in LOCATIONS], cardId=A9['id'], groupRowId='locations')})
whole = {}
for t in tasks:
    c = t['card']
    if '-complete' in c['id']:
        whole.setdefault('10-alt' if t['alternative'] else t['questionNumber'], []).append(dict(id=c['id'], parts=[g['label'] for g in c['taskGroups']], marks=c['totalMarks']))
out = dict(schemaVersion=1, subjectId='construction-studies', year=2026, level='higher', lang='ev', sitting='main', paperKey='single',
           fileid='LC029ALP000EV.pdf', component='theory', status='Q1–Q10 and alternative Q10 source-reviewed draft; integration pending.',
           sourceHashes=HASHES, tasks=tasks, bindings=bindings, questionFigures=question_figures,
           addedIds=[t['card']['id'] for t in tasks], selectionLedger=selection_ledger,
           questionRouteLedgers={q: dict(wholeRoutes=w) for q, w in whole.items()}, taxonomyGaps=[],
           questionsReviewed=[str(n) for n in range(1, 11)], unreviewedQuestions=[], alternativeQuestions=['10'])
(HERE / 'higher-2026-draft.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(tasks=len(tasks), figures=len(question_figures),
                      perQuestion={q: sum(1 for t in tasks if t['questionNumber'] == q and not t['alternative']) for q in QUESTIONS},
                      alternative=sum(1 for t in tasks if t['alternative']), wholeRoutes={q: len(w) for q, w in whole.items()})))
