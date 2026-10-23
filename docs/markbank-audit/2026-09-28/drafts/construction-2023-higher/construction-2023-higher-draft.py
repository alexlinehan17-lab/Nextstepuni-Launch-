"""Draft the 2023 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Question wording is lifted from the SEC paper: a narrowed task only deletes printed words, and a task
named only by reference to a printed list carries the scheme's own heading after ' — '. Every row's
verbatim is printed in the scheme's mark tables (pages 33-43) or model pages, checked against rendered
pages. Unbanded components accept any whole mark up to the published maximum. Figures are exact 2x
crops of the original PDFs; a solution figure spanning several scheme pages is a composite of exact
page crops, so every item of a one-card choice keeps its drawings.

The printed choices Q4(b) and Q10(a) (any two of three) are ONE card each with an anyN group (choice is
not a route). The 29 pre-audit 2023 Higher cards keep their IDs and concept IDs and are corrected in
place; each correction records the SHA-256 of the card it replaces.
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

P = 'paper-trail-corpus/exampapers/2023/LC029ALP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2023/LC029ALP000EV.pdf'
HASHES = {P: '194c14229122c30285677e2133d08f4855a6798893add82f3bc50e94b5ca38f5',
          S: 'fd7a1e74988a4af90cbb10c455f2cbe2c9ec8c724f9d690093e1b822db4fc0b4'}
for f, h in HASHES.items():
    assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f
ATTRIBUTION = 'SEC Leaving Certificate Construction Studies 2023 Higher Level — © State Examinations Commission.'
FP = 'construction-studies-2023-HL-'
PREFIX = 'cons-2023-hl-'
CROSS = 'construction-studies-higher-'

# The pre-audit cards are snapshotted before integration so the draft regenerates byte-identically afterwards.
LEGACY_FILE = HERE / 'prior-2023-higher-cards.json'
if not LEGACY_FILE.exists():
    AUTHORED = json.loads((R / 'scripts/markbank/authored/construction-studies.json').read_text())
    LEGACY_FILE.write_text(json.dumps([c for c in AUTHORED if c['id'].startswith(PREFIX)], ensure_ascii=False, indent=2) + '\n')
LEGACY = {c['id']: c for c in json.loads(LEGACY_FILE.read_text())}
assert len(LEGACY) == 29, sorted(LEGACY)


def card_hash(c):
    return hashlib.sha256(json.dumps(c, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def composite(*panels):
    return construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [45, 53, 580, 342], False), 'q2-original': (P, 2, [45, 430, 580, 688], False),
    'q3-original': (P, 3, [45, 53, 580, 410], False), 'q4-original': (P, 3, [45, 462, 580, 752], False),
    'q5-original': (P, 4, [45, 50, 580, 702], False), 'q6-original': (P, 5, [45, 53, 580, 432], False),
    'q7-original': (P, 5, [45, 481, 580, 757], False), 'q8-original': (P, 6, [45, 53, 580, 318], False),
    'q9-original': (P, 6, [45, 401, 580, 723], False), 'q10-original': (P, 7, [45, 53, 580, 466], False),
    'q10-alt-original': (P, 7, [45, 533, 580, 756], False),
    'q1-section': (S, 4, [51, 51, 550, 806], True), 'q1-ventilation': (S, 5, [51, 498, 520, 809], True),
    'q2-site-access': (S, 7, [51, 113, 540, 721], True), 'q2-ladder': (S, 8, [51, 50, 542, 484], True),
    'q2-guidelines': composite((7, [51, 113, 540, 721]), (8, [51, 50, 542, 484])),
    'q3-considerations': composite((9, [51, 51, 554, 796]), (10, [51, 50, 543, 232])),
    'q3-layout': composite((10, [51, 236, 539, 800]), (11, [51, 48, 542, 712])),
    'q4-features': composite((12, [51, 412, 544, 773]), (13, [51, 48, 554, 603])),
    'q4-refurbishment': composite((13, [51, 603, 545, 779]), (14, [51, 48, 546, 733])),
    'q4-scheme': composite((12, [51, 412, 544, 773]), (13, [51, 48, 554, 779]), (14, [51, 48, 546, 733])),
    'q5-calculation': composite((15, [51, 476, 540, 802]), (16, [51, 70, 471, 485])),
    'q5-thermal-bridge': (S, 16, [53, 485, 524, 791], True),
    'q6-low-impact': composite((17, [51, 51, 540, 709]), (18, [51, 48, 530, 361])),
    'q6-technologies': composite((18, [51, 367, 545, 767]), (19, [51, 50, 546, 803])),
    'q7-section': (S, 21, [51, 51, 531, 788], True), 'q7-threshold': (S, 22, [51, 315, 545, 741], True),
    'q8-system': composite((23, [51, 333, 532, 766]), (24, [51, 50, 526, 221])),
    'q9-requirements': composite((24, [51, 465, 552, 761]), (25, [51, 48, 537, 663])),
    'q9-calculation': (S, 26, [51, 50, 502, 438], True),
    'q10-features': composite((27, [51, 370, 549, 719]), (28, [51, 49, 563, 784]), (29, [46, 48, 543, 334])),
    'q10-mvhr': (S, 29, [46, 336, 543, 804], True),
    'q10-scheme': composite((27, [51, 370, 549, 719]), (28, [51, 49, 563, 784]), (29, [46, 48, 543, 804])),
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
    '1': dict(page=2, title='Trussed roof and timber-frame wall section', concept='trussed-roof-section',
              stem='The sketch shows a dwelling house with a roof constructed using prefabricated trussed rafters. The tiled roof has a pitch of 30° and an internal span of 5.6 metres. The external wall is of timber frame construction with an external rendered concrete block leaf. The internal timber frame is 250 mm × 50 mm. A 50 mm service cavity is also provided at the internal surface. The roof is highly insulated at ceiling joist level.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the ventilation detail in (b) is marked separately.'),
    '2': dict(page=2, title='A safe working environment on a construction site', concept='site-safety', stem='',
              note='Original question retained. All three printed items in (a) and both printed activities in (b) are required, each separately marked. The scheme lists typical points, not an exhaustive list.'),
    '3': dict(page=3, title='First-floor kitchen/dining and living area by the coast', concept='first-floor-living',
              stem='The drawing shows the elevation and first floor plan of a two-storey house located by the coast. The front wall A-A is south facing and the wall B-B has views to the sea. The owners wish to relocate their kitchen/dining and living area to the first floor to take advantage of the orientation and sea views from their house. They intend to retain two bedrooms on the first floor and also retain the position of the stairs.',
              note='Original elevation and plan retained. Design considerations and layouts are open responses; the scheme shows a model layout.'),
    '4': dict(page=3, title='Refurbishing a vernacular Irish homestead', concept='vernacular-homestead',
              stem='The sketch shows a vernacular Irish homestead built over 100 years ago. It was built in the vernacular tradition using local knowledge and skills which were related to its location and to the landscape. The owners wish to refurbish the cottage in a manner that respects the character of the original cottage.',
              note='Original sketch retained. Part (b) chooses any two of three printed items, each keeping its own 7 marks.'),
    '5': dict(page=4, title='Flat roof U-value, heat-loss cost and thermal bridge', concept='flat-roof-heat-loss',
              stem='An extension to a house has a highly insulated flat roof with a waterproof roof covering, as shown.',
              note='All printed data are retained in the original question. Part (b) uses the U-value from (a); the scheme’s worked answers are U = 0.104 W/m²°C and an annual cost of €12.53.'),
    '6': dict(page=5, title='Low environmental impact house and energy technologies', concept='low-impact-technologies',
              stem='The elevation and ground floor plan of a house are shown. The external walls are of timber frame construction with a rendered concrete block and stone finish. The house is designed to have low environmental impact.',
              note='Original elevation and plan retained. All three printed technologies in (b) are required, each separately marked.'),
    '7': dict(page=5, title='External door, wall and ground floor section', concept='external-door-section',
              stem='An external wooden door with vertical sheeting is the main entrance to a dwelling house, as shown. The thermally broken doorframe is 160 mm × 70 mm and the door is highly insulated. The 450 mm external wall of the house is of concrete block construction with a full-fill insulated cavity. The ground floor is a highly insulated solid concrete floor with a 20 mm tile finish.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the threshold detail in (b) is marked separately.'),
    '8': dict(page=6, title='Wastewater treatment for a rural house', concept='wastewater-treatment', stem='',
              note='Original sketch retained. Requirements and reasons are open responses; the scheme gives a model layout and typical dimensions.'),
    '9': dict(page=6, title='Glazing and daylight', concept='glazing-and-daylight',
              stem='The entry of light into rooms is a key consideration when designing a home.',
              note='Original sketch retained. The scheme’s worked answer for (b) is a window area of 9.45 m² by the degree of efficiency method; any other suitable method is accepted.'),
    '10': dict(page=7, title='Passive House design and MVHR', concept='passive-house-mvhr', stem='',
               note='Original plan retained. Part (a) chooses any two of three printed items, each keeping its own 10 marks.'),
}
ALT = dict(page=7, title='Universal Design for homes (alternative Question 10)', concept='universal-design',
           stem='“People regardless of age, size, ability or disability are positively contributing to the social, economic and cultural life of our communities. However, finding suitable and appropriate homes that can accommodate our changing needs over time can be difficult - whether for families with young children, a person with a temporary or permanent injury, someone with a disability, or an older person living independently. Universal Design can meet everyone’s needs through flexible homes designed to adapt to lifecycle and lifestyle patterns of people over time.” Adapted from: Universal Design Guidelines for Homes in Ireland Published by National Disability Authority',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the Passive House question.')
SCHEME_PAGES = {'1': [4, 5, 33], '2': [6, 7, 8, 34], '3': [9, 10, 11, 12, 35], '4': [12, 13, 14, 15, 36], '5': [15, 16, 37],
                '6': [17, 18, 19, 20, 38], '7': [21, 22, 39], '8': [23, 24, 40], '9': [24, 25, 26, 27, 41], '10': [27, 28, 29, 30, 42],
                '10-alt': [30, 31, 43]}

tasks, bindings, cards = [], [], {}


def add(q, key, ref, text, rows, nodes, topics, figure, review, boundary, selection, groups=None, total=None, alt=False):
    meta = ALT if alt else QUESTIONS[q]
    qkey = '10-alt' if alt else q
    cid = f'{PREFIX}q{qkey}-{key}'
    concept = LEGACY[cid]['conceptId'] if cid in LEGACY else f"{meta['concept']}-{key}"
    card = dict(id=cid, subjectId='construction-studies', year=2023, level='higher', section='B',
                topicId=nodes[0], conceptId=concept, questionRef=f'2023 HL Q{qkey}{ref}',
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


def parts(*pairs):
    return '\n\n'.join(f'({letter}) {text}' for letter, text in pairs)


# ---------------------------------------------------------------- Q1
B1 = 'Scheme p33 (printed 31): (a) external timber frame wall 5 × 4, roof structure 3 × 4, eaves detail 4 × 4 (each detail 4) = 48, scale 4 + drafting 4 = 56; (b) ventilation detail 4. Complete 60. The scale/drafting allowance assesses the section drawn in (a), so it stays with (a).'
S1 = 'One required section and one required ventilation detail. The scheme detail lists are marking menus, not printed choices.'
T1A = 'To a scale of 1:10, draw a vertical section through one half of the roof structure from eaves up to the ridge. Show one external wall and one rafter length. Include the typical construction details from 600 mm below the ceiling joist up to the ridge and include three courses of tiles at eaves.'
T1B = 'On your drawing, indicate the typical design detailing to ensure ventilation of the roof structure.'
A1 = add('1', 'a', '(a)', T1A,
         [row('wall', 'External timber frame wall', 20, 'Best five details, 4 each. Marking menu: external render; concrete block and tie; firestopping/cavity closer; air space/residual cavity; breather membrane; racking board; 250 × 50 mm stud; insulation; air barrier membrane; insulated service cavity; plasterboard/skim.'),
          row('roof', 'Roof structure', 12, 'Best three details, 4 each. Marking menu: prefabricated roof truss (rafter, ceiling joist, hanger, strut — any two) 200 × 50 mm at 400–600 mm centres; gang nail plates and truss fixing; attic insulation; insulated plasterboard ceiling (50 mm insulation + 12.5 mm plasterboard); airtightness tape at the wall/ceiling junction; air-barrier membrane at the ceiling.'),
          row('eaves', 'Eaves detail', 16, 'Best four details, 4 each. Marking menu: fascia/soffit/gutter (any two); tilting fillet; ventilation; wind tightness barrier; roof breather membrane; counter battens; tiling battens 40 × 40 mm at 400 mm centres; three courses of concrete tiles.'),
          row('presentation', 'Scale – 4 marks Drafting – 4 marks', 8, 'Scale 4 and drafting 4 for the section.')],
         ['cons-1-5', 'cons-3-8', 'cons-3-10', 'cons-3-9', 'cons-3-3'], ['question-1-drawing-questions', 'roofs', 'walls'], 'q1-section',
         'Scaled drawing (1.5) of a trussed roof (3.8) at the eaves (3.10) with its covering and insulation (3.9) on a timber-frame wall (3.3).', B1, S1)
B1b = add('1', 'b', '(b)', T1B,
          [row('ventilation', 'Design detailing to ensure ventilation of the roof', 4, 'Show and identify the ventilation route at the eaves, as in the scheme’s model detail: air entering through the soffit and passing over the insulation into the roof space.')],
          ['cons-3-9', 'cons-6-5'], ['roofs', 'wood-rot-ventilation'], 'q1-ventilation', 'Ventilation (6.5) of the roof space and insulation (3.9).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p34 (printed 32): (a) three items × (3 for point + 3 for discussion) = 18; (b) for each activity two guidelines × (4 for note + 4 for sketch) = 16, (b) 32; (c) two reasons × (3 for point + 2 for discussion) = 10. Complete 60.'
S2 = 'Parts (a) and (b) require every printed item, each separately marked, so each item is its own task and the part composes them; not choices. Guidelines and reasons are open responses.'
T2A = 'Discuss in detail the importance of each of the following in maintaining a safe working environment on a construction site: communication; supervision; training.'
ITEMS2 = [('communication', 'Communication', 'Point 3 and discussion 3. Such as: clear communication between co-workers so teams coordinate safely; regular site meetings so everyone knows of hazardous operations; clear signage at the entrance and throughout the site; a formal communication chain and a designated safety officer coordinating verbal and virtual communication.'),
          ('supervision', 'Supervision', 'Point 3 and discussion 3. Such as: experienced workers supervising inexperienced ones; an adequately trained site safety supervisor; supervision of hazardous operations; supervisors planning and allocating work, monitoring compliance and providing leadership; close supervision of young workers and high-risk activities.'),
          ('training', 'Training', 'Point 3 and discussion 3. Such as: a current Safe Pass certificate for every worker; training to carry out tasks and identify hazards; ongoing training against complacency; mentoring of new workers; training before operating machinery or new procedures.')]
a2 = [add('2', f'a-{slug}', f'(a) — {slug}', f'{T2A} — {heading}',
          [row('importance', f'{heading} (3 for point, 3 for discussion)', 6, note)],
          ['cons-1-8'], ['site-safety'], None, 'Safety precautions on site (1.8).', B2, S2) for slug, heading, note in ITEMS2]
A2 = compose('2', 'a', '(a)', a2, None, B2, S2, T2A, labels=[i[1] for i in ITEMS2])
T2B = 'Using notes and freehand sketches, outline two specific best practice guidelines that should be observed for each of the following on a construction site: site access; using a ladder.'
ITEMS2B = [('site-access', 'Site access', 'q2-site-access',
            'Note 4 and sketch 4. Such as: security fencing or hoarding (at least 2.4 m) to keep out unauthorised people and vehicles; clear signage at the entrance and on the approach; a site induction for all new personnel; good sight lines for vehicles leaving the site.',
            'A second, different guideline: note 4 and sketch 4. Such as: turnstiles, security gates or electronic access control (PIN, cards, biometrics) so only authorised personnel enter; a sign-in and reception area; Safe Pass and CSCS checks; a surface at the access point that keeps mud off the public road.'),
           ('using-a-ladder', 'Using a ladder', 'q2-ladder',
            'Note 4 and sketch 4. Such as: use a ladder only after a risk assessment shows low risk and short duration; a pre-use check each day; the 1-in-4 rule (about 74°); firm, level ground and the ladder secured against slipping.',
            'A second, different guideline: note 4 and sketch 4. Such as: extend at least 1 metre (three rungs) above the working level; three points of contact when climbing; no work within 6 m of an overhead power line unless it is dead; other equipment for tasks of 30 minutes or more.')]
b2 = [add('2', f'b-{slug}', f'(b) — {slug}', f'{T2B} — {heading}',
          [row('guideline-1', 'Guideline 1 (4 for note, 4 for sketch)', 8, g1), row('guideline-2', 'Guideline 2 (4 for note, 4 for sketch)', 8, g2)],
          ['cons-1-8'], ['site-safety'], figure, 'Safety precautions on site (1.8).', B2, S2) for slug, heading, figure, g1, g2 in ITEMS2B]
B2b = compose('2', 'b', '(b)', b2, 'q2-guidelines', B2, S2, T2B, labels=[i[1] for i in ITEMS2B])
T2C = 'Discuss two reasons why all construction sites must have a safety statement.'
C2 = add('2', 'c', '(c)', T2C,
         [row('reason-1', 'Reason 1 (3 for point, 2 for discussion)', 5, 'Point 3 and discussion 2. Such as: a legal requirement under the Safety, Health and Welfare at Work Act 2005; it safeguards the health and safety of workers and visitors; it identifies hazards and risks and plans their control.'),
          row('reason-2', 'Reason 2 (3 for point, 2 for discussion)', 5, 'A second, different reason: point 3 and discussion 2. Such as: it records risk assessments for Health and Safety Authority inspectors; fewer injuries, lost productivity, compensation and insurance costs; the employer’s ethical and moral obligation to prevent harm.')],
         ['cons-1-8'], ['site-safety'], None, 'Safety precautions on site (1.8).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-guidelines', B2, S2, parts(('a', T2A), ('b', T2B), ('c', T2C)))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p35 (printed 33): (a) three design considerations × (3 for point + 3 for discussion) = 18; (b) revised layout 14, the three considerations 2 each, justification 2 = 22; (c) two advantages and two disadvantages × (3 for point + 2 for discussion) = 20. Complete 60.'
S3 = 'Design considerations and layouts are open responses. Part (c) requires both two advantages and two disadvantages, separately marked: two required tasks composed into (c).'
T3A = 'Discuss in detail, three design considerations for the proposed new kitchen/dining and living area on the first floor.'
T3B = 'Using notes and freehand sketches, show a revised internal layout for the kitchen/dining and living area that incorporates each of the design considerations you outlined at 3(a) above. Justify your choices.'
T3C = 'Discuss two advantages and two disadvantages of locating a kitchen/dining and living area on the first floor of a dwelling house.'
A3 = add('3', 'a', '(a)', T3A,
         [row(f'consideration-{i}', f'Design consideration {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: the work triangle (hob, sink, fridge) and enough workspace; circulation space around the kitchen and the dining table and clear routes to exits.'),
             (2, 'A second, different consideration. Such as: access and egress — an alternative means of escape in a fire and free movement between floors; services — sockets, isolation switches, the sink near existing water and waste pipes, a service shaft.'),
             (3, 'A third, different consideration. Such as: the sensory experience — large south and sea-facing windows for light and views, triple glazing and sound insulation to the bedrooms below, MVHR to remove odours and moisture.')]],
         ['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'], 'q3-considerations',
         'Layout design within the built environment (1.2) for good illumination (7.4).', B3, S3)
B3b = add('3', 'b', '(b)', T3B,
          [row('layout', 'Revised internal layout for the kitchen/dining and living area on the first floor', 14, 'Notes and sketches of a coherent first-floor kitchen/dining and living layout that keeps two bedrooms and the stairs. Such as: a work triangle with adequate workspace; at least 1.2 m between opposite worktops; larger south windows and new sea-facing windows; lower cills; a sink on the outer wall at the existing waste outlet.'),
           row('consideration-1', 'Design consideration 1', 2, 'The first design consideration from (a) shown in the layout.'),
           row('consideration-2', 'Design consideration 2', 2, 'The second design consideration from (a) shown in the layout.'),
           row('consideration-3', 'Design consideration 3', 2, 'The third design consideration from (a) shown in the layout.'),
           row('justification', 'Justification', 2, 'The choices justified, such as more light and solar gain, sea views for wellbeing, fire escape routes or reduced noise to the bedrooms.')],
          ['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'], 'q3-layout',
          'Layout design within the built environment (1.2) for good illumination (7.4).', B3, S3)
c3 = [add('3', f'c-{kind}s', f'(c) — {kind}s', f'Discuss two {kind}s of locating a kitchen/dining and living area on the first floor of a dwelling house.',
          [row(f'{kind}-1', f'{kind.capitalize()} 1 (3 for point, 2 for discussion)', 5, n1), row(f'{kind}-2', f'{kind.capitalize()} 2 (3 for point, 2 for discussion)', 5, n2)],
          ['cons-1-2'], ['planning-sustainability-environment'], None, 'Layout design within the built environment (1.2).', B3, S3)
      for kind, n1, n2 in [('advantage', 'Point 3 and discussion 2. Such as: better, unobstructed views; more natural light in the rooms used by day.',
                            'A second, different advantage. Such as: bedrooms and stores that need little daylight go downstairs; a solution for steep or restricted sites; more privacy from neighbours.'),
                           ('disadvantage', 'Point 3 and discussion 2. Such as: kitchen leaks damage the rooms beneath; not future-proofed for reduced mobility.',
                            'A second, different disadvantage. Such as: moving appliances and furniture upstairs is harder; no access to the garden without costly balconies; extra cost of supports and sound insulation.')]]
C3 = compose('3', 'c', '(c)', c3, None, B3, S3, T3C, labels=['Advantages', 'Disadvantages'])
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-layout', B3, S3, parts(('a', T3A), ('b', T3B), ('c', T3C)))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p36 (printed 34): (a) three vernacular features × (notes 5 + sketches 5) = 30; (b) any two of three printed items × (4 for point + 3 for discussion) = 14; (c) two reasons × (4 for point + 4 for discussion) = 16. Complete 60.'
S4 = 'Choice is not a route: part (b) (any two of three printed items) is ONE card with an any-two group over the scheme headings. Features and reasons are open responses.'
T4A = 'Discuss in detail, using notes and freehand sketches, three features of vernacular Irish architecture evident in the cottage shown.'
T4B = 'Discuss the importance of any two of the following when carrying out a refurbishment of an old cottage built in the vernacular tradition: choice of materials; craft skills; respect for local character.'
T4C = 'Discuss two reasons to refurbish and maintain traditional Irish cottages.'
A4 = add('4', 'a', '(a)', T4A,
         [row(f'feature-{i}', f'Vernacular Feature {i}', 10, note) for i, note in [
             (1, 'Notes 5 and sketches 5. Such as: single storey with a steep, simply pitched roof; rectangular, narrow and one room deep because roof timber was scarce; a direct-entry plan shown by the chimneys’ position relative to the door.'),
             (2, 'A second, different feature: notes 5 and sketches 5. Such as: small door and window openings on the long elevation, keeping the walls strong; a central chimney for heat and cooking; a half-door.'),
             (3, 'A third, different feature: notes 5 and sketches 5. Such as: local stone walls, rendered and limewashed; small sash windows with four panes and stone cills; local natural slate with flush verges; a low void-to-mass ratio.')]],
         ['cons-1-1'], ['conservation-restoration'], 'q4-features', 'Historical development and appearance of buildings (1.1).', B4, S4)
ITEMS4 = [('Choice of material', 'reuse and repair existing materials; matching salvaged materials to keep the patina of age; local materials; breathable lime render and mortar instead of cement, which locks moisture in.'),
          ('Craft skills', 'experienced craftspeople with knowledge of regional traditions; repair only what cannot be kept; conservation specialists; local stonemasons and plasterers using lime.'),
          ('Respect for local character', 'vernacular design evolved from its surroundings and local materials; keep the simple materials, methods and detailing; a fabric-first approach; advice from conservation officers, architects and engineers.')]
A4b = add('4', 'b', '(b)', T4B,
          [dict(id='items', kind='anyN', verbatim='Refurbishing of an old cottage built in the vernacular tradition (any two)', marks=14,
                contextNote='Any two of the three, each 4 for point and 3 for discussion = 7. ' + ' '.join(f'{h}: {n}' for h, n in ITEMS4),
                group=dict(claimMax=2, perOption=7, options=[h for h, _ in ITEMS4]))],
          ['cons-1-1', 'cons-1-2'], ['conservation-restoration'], 'q4-refurbishment',
          'Conserving a vernacular building (1.1) in its setting (1.2).', B4, S4)
C4 = add('4', 'c', '(c)', T4C,
         [row('reason-1', 'Reason 1 (4 for point, 4 for discussion)', 8, 'Point 4 and discussion 4. Such as: reuse reduces the demand for new housing and is quicker than a new build; planning permission is usually obtained sooner; the cottage records the community and traditions of the locality.'),
          row('reason-2', 'Reason 2 (4 for point, 4 for discussion)', 8, 'A second, different reason. Such as: less embodied carbon — the greenest building is the one already built; rejuvenating the community; tourism, local spending and employment.')],
         ['cons-1-1', 'cons-1-2'], ['conservation-restoration'], None, 'Conserving historic buildings (1.1) in the built environment (1.2).', B4, S4)
compose('4', 'complete', ' — complete', [A4, A4b, C4], 'q4-scheme', B4, S4, parts(('a', T4A), ('b', T4B), ('c', T4C)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p37 (printed 35): (a) ten points × 3 = 30 (the two surface resistances, the six roof layers, total resistance, U-value); (b) five steps × 3 = 15; (c) notes/discussion 5 + sketch 10 = 15. Complete 60.'
S5 = 'No printed choice. Part (b) uses the U-value from (a).'
DATA5A = ('Waterproof covering thickness 2 mm; roof insulation thickness 150 mm; plywood decking thickness 20 mm; clear cavity between roof joists thickness 200 mm; '
          'ceiling insulation thickness 50 mm; plasterboard thickness 12.5 mm.\n'
          'Thermal data of the flat roof: resistance of external surface (R) 0.048 m² °C/W; resistivity of waterproof covering (r) 6.250 m °C/W; '
          'conductivity of roof insulation (k) 0.022 W/m °C; conductivity of plywood (k) 0.130 W/m °C; resistance of clear cavity (R) 0.170 m² °C/W; '
          'conductivity of ceiling insulation (k) 0.022 W/m °C; conductivity of plasterboard (k) 0.250 W/m °C; resistance of internal surface (R) 0.122 m² °C/W.')
T5A = 'Calculate the U-value of the roof, given the construction has the following sequence and data: ' + DATA5A
T5B = ('Using the U-value of the roof obtained at 5(a) above and the following data, calculate the cost of heat lost annually through this roof: dimensions of flat roof 8.5 metres × 4.5 metres; '
       'average internal temperature 18 °C; average external temperature 5 °C; heating period 8 hours daily for 36 weeks per annum; cost of oil €1.25 per litre; '
       'calorific value of oil 37350 kJ per litre; 1000 watts: 1 kJ per second.')
T5C = 'Using notes and a freehand sketch, show best practice design detailing that will prevent the formation of a thermal bridge at the abutment of the flat roof and external concrete block wall with a full-fill insulated cavity.'
A5 = add('5', 'a', '(a)', T5A,
         [row('resistances', 'Formulae: R=T/k R=T × r', 24, 'Eight resistances, 3 each, by R = T/k (or R = T × r): external surface 0.048 (given); waterproof covering 0.002 × 6.250 = 0.013; roof insulation 0.150/0.022 = 6.818; plywood 0.020/0.130 = 0.154; clear cavity 0.170 (given); ceiling insulation 0.050/0.022 = 2.273; plasterboard 0.0125/0.250 = 0.050; internal surface 0.122 (given). All in m²°C/W.', list(range(0, 25, 3))),
          row('total-resistance', 'Total resistance', 3, 'Total resistance Rt = 9.647 m²°C/W (the sum of all the resistances).', [0, 3]),
          row('u-value', 'Calculation of U-value (w/m2 °C or w/m2k)', 3, 'U = 1 ÷ Rt = 1 ÷ 9.647 = 0.104 W/m²°C, with units.', [0, 3])],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Thermal resistance, conductivity and transmittance (6.1).', B5, S5)
B5b = add('5', 'b', '(b)', T5B,
          [row('heat-loss', 'Heat loss formula and calculation', 3, 'Heat loss = U-value × area × temperature difference = 0.104 × 38.25 × (18 − 5) = 51.714 watts (joules per second).'),
           row('duration', 'Heating duration - calculation for one year', 3, 'Heating period = 60 × 60 × 7 × 8 × 36 = 7,257,600 seconds (2,016 hours).'),
           row('energy', 'k/Joules - calculation for one year', 3, 'Energy = 7,257,600 × 51.714 ÷ 1000 = 375,319 kJ per year.'),
           row('oil', 'Litres of oil - calculation for one year', 3, 'Oil = 375,319 ÷ 37,350 = 10.04 litres per year.'),
           row('cost', 'Annual cost – calculation of heat loss PA', 3, 'Annual cost = 10.04 × €1.25 = €12.53. The scheme’s alternative one-line method gives the same €12.53.')],
          ['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Heat loss calculation and running costs (6.3) from the U-value (6.1).', B5, S5)
C5 = add('5', 'c', '(c)', T5C,
         [row('notes', 'Notes / discussion', 5, 'Such as: thermal blocks and continuity of insulation at the junction of the flat roof and the external block wall, as in the scheme’s model detail.'),
          row('sketch', 'Sketch', 10, 'Freehand sketch of the flat-roof and cavity-wall junction showing the continuous insulation and thermal blocks.')],
         ['cons-6-2', 'cons-3-10'], ['heat-loss-insulation', 'roofs'], 'q5-thermal-bridge', 'A thermal bridge (6.2) at a flat-roof abutment (3.10).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p38 (printed 36): (a) three design features × (notes 5 + sketches 5) = 30; (b) each of three technologies notes 3 + sketches 3 = 18; (c) two advantages × (3 for point + 3 for discussion) = 12. Complete 60.'
S6 = 'All three printed technologies in (b) are required, each marked notes 3 + sketches 3, in one task. Features and advantages are open responses.'
T6A = 'With reference to the design shown, discuss using notes and freehand sketches, three features of the design that contribute to the house having a low environmental impact.'
T6B = 'Reducing operational energy demand is an important consideration in designing for low environmental impact. Using notes and freehand sketches, discuss in detail each of the following technologies and how each would further reduce the energy demand of the house: photovoltaic panels; air-to-water heat pump; evacuated tubes.'
T6C = 'Discuss in detail two advantages of reducing energy demand in the home.'
A6 = add('6', 'a', '(a)', T6A,
         [row(f'feature-{i}', f'Design Feature {i}', 10, note) for i, note in [
             (1, 'Notes 5 and sketches 5. Such as: the orientation of the building; local timber frame with lower embodied energy and stored carbon; locally sourced FSC timber cladding.'),
             (2, 'A second, different feature. Such as: large south-facing glazing in narrow, one-room-wide spaces for light and solar heat; small high-performance north windows; an L-shaped plan sheltering from wind.'),
             (3, 'A third, different feature. Such as: high insulation in floor, walls and roof; high-performance glazing (0.8 W/m²K); no chimney, so better airtightness; ridge roof lights.')]],
         ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-low-impact',
         'Low-impact design of the built environment (1.2), solar gain (6.4) and insulation (6.2).', B6, S6)
B6b = add('6', 'b', '(b)', T6B,
          [row('photovoltaic', 'Photovoltaic panels', 6, 'Notes 3 and sketches 3. Such as: silicon cells convert light into direct current, which an inverter changes to alternating current for the home; less mains electricity from fossil fuels; excess sold to the grid under microgeneration.'),
           row('heat-pump', 'Air-to-water heat pump', 6, 'Notes 3 and sketches 3. Such as: a fan draws heat from outside air into a coolant, a compressor raises its temperature and a heat exchanger heats water for radiators, underfloor heating or hot water; a coefficient of performance of 3–4.'),
           row('evacuated-tubes', 'Evacuated tubes', 6, 'Notes 3 and sketches 3. Such as: vacuum-insulated glass tubes whose heat pipes carry solar heat to a transfer fluid that heats the hot-water cylinder, pumped back to the tubes; efficient from many sun angles.')],
          ['cons-6-3', 'cons-5-8', 'cons-5-3', 'cons-5-2'], ['heat-loss-insulation', 'services-water-gas-electricity', 'hot-water-space-heating'], 'q6-technologies',
          'Reducing energy demand (6.3) through renewable electricity (5.8), heating (5.3) and hot water (5.2).', B6, S6)
C6 = add('6', 'c', '(c)', T6C,
         [row('advantage-1', 'Advantage 1 (3 for point, 3 for discussion)', 6, 'Point 3 and discussion 3. Such as: lower greenhouse gas emissions and less pollution from non-renewable energy.'),
          row('advantage-2', 'Advantage 2 (3 for point, 3 for discussion)', 6, 'A second, different advantage. Such as: lower utility bills; more stable electricity prices; less need for new generation and transmission infrastructure.')],
         ['cons-6-3', 'cons-1-2'], ['heat-loss-insulation', 'sustainability-the-environment'], None,
         'Running costs (6.3) and the sustainable built environment (1.2).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-low-impact', B6, S6, parts(('a', T6A), ('b', T6B), ('c', T6C)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p39 (printed 37): (a) head of the door 4 × 4, external door 4 × 4, threshold 4 × 4 (each detail 4) = 48, scale 4 + drafting 4 = 56; (b) moisture detail at the threshold 4. Complete 60.'
S7 = 'One required section and one required threshold detail. The scheme detail lists are marking menus, not printed choices.'
T7A = 'To a scale of 1:10, draw a vertical section through the centre of the door, external wall and ground floor. Show the typical construction details from a level 400 mm below the finished floor, through the door, up to a level 400 mm above the concrete lintels.'
T7B = 'On your drawing, show the typical design detailing that will prevent the ingress of moisture at the threshold.'
A7 = add('7', 'a', '(a)', T7A,
         [row('door-head', 'Head of the door', 16, 'Best four details, 4 each. Marking menu: external and internal render; cavity wall; wall tie; full-fill insulated cavity (250 mm); cavity closer; stepped damp-proof tray/course; reinforced concrete lintels (100 × 65 mm).'),
          row('external-door', 'External door', 16, 'Best four details, 4 each. Marking menu: airtightness tape at the door frame head; thermally broken door frame (160 × 70 mm); external door with sheeting; door insulation; proprietary insulated door threshold; 15 mm upstand or 15° slope; airtightness tape at the threshold.'),
          row('threshold', 'Threshold', 16, 'Best four details at floor level, 4 each. Marking menu: skirting board; 20 mm floor tiles; concrete floor; floor insulation; radon barrier; vertical insulation as a thermal break; drainage channel; a level entrance surface.'),
          row('presentation', 'Scale - 4 marks Drafting - 4 marks', 8, 'Scale 4 and drafting 4 for the section.')],
         ['cons-1-5', 'cons-3-7', 'cons-3-3', 'cons-3-4', 'cons-4-2'], ['question-1-drawing-questions', 'doors', 'walls', 'floors'], 'q7-section',
         'Scaled drawing (1.5) of an external door (3.7) in a cavity wall (3.3) with its lintels and DPC (3.4) at an insulated ground floor (4.2).', B7, S7)
B7b = add('7', 'b', '(b)', T7B,
          [row('threshold-moisture', 'Design detailing to prevent ingress of moisture', 4, 'Such as: a threshold drainage channel; a sloped threshold cill; a threshold upstand.')],
          ['cons-3-7', 'cons-3-4'], ['doors', 'walls'], 'q7-threshold', 'The door threshold (3.7) and damp proofing (3.4).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p40 (printed 38): (a) three functional requirements × (3 for point + 5 for discussion) = 24; (b) layout notes 6, sketch 10, description of how the system works 6, four typical dimensions 4 = 26; (c) two reasons × (2 for point + 3 for discussion) = 10. Complete 60.'
S8 = 'No printed choice. Requirements and reasons are open responses; the scheme gives a model layout.'
T8A = 'Discuss in detail, three functional requirements of a typical wastewater treatment system for a dwelling house.'
T8B = 'A wastewater treatment system is being installed for a dwelling house, as shown. Using notes and freehand sketches, show the typical design layout necessary for a wastewater treatment system and percolation area suitable for a house in a rural area. Describe how the system works and include four typical dimensions.'
T8C = 'Discuss two reasons why it is important to properly treat and dispose of wastewater from a dwelling house.'
A8 = add('8', 'a', '(a)', T8A,
         [row(f'requirement-{i}', f'Functional requirement {i} (3 for point, 5 for discussion)', 8, note) for i, note in [
             (1, 'Point 3 and discussion 5. Such as: remove waste efficiently and safely from the dwelling; treat it before it is discharged to the environment.'),
             (2, 'A second, different requirement. Such as: accessible pipework for maintenance, with access chambers at changes of direction; sound, leak-proof, corrosion-resistant pipes laid at 1:60.'),
             (3, 'A third, different requirement. Such as: work within the site boundary without affecting neighbours, water courses or habitats; the correct capacity for the number of occupants; carry off foul odours.')]],
         ['cons-5-5'], ['drainage'], None, 'Underground drainage and wastewater treatment (5.5).', B8, S8)
B8b = add('8', 'b', '(b)', T8B,
          [row('notes', 'Notes', 6, 'Notes on the layout: the treatment system, distribution box and at least four perforated percolation pipes in gravel trenches, with access points and vents.'),
           row('sketch', 'Sketch', 10, 'Freehand sketch of the treatment system and percolation area.'),
           row('description', 'Description of how the system works', 6, 'Foul water enters the tank; solids settle as sludge and are broken down by anaerobic bacteria; the liquid flows to a distribution box and into perforated percolation pipes; aerobic bacteria in the gravel break down remaining impurities before the water reaches the groundwater.'),
           row('dimensions', 'Four typical dimensions', 4, 'Four typical dimensions, 1 each. Such as: pipe to the distribution box 100–110 mm at 1 in 60; trenches at 1 in 200, 500 mm wide and 850 mm deep; at most 18 m of pipe per trench; trenches 2 m apart (2.5 m centres).')],
          ['cons-5-5'], ['drainage'], 'q8-system', 'Underground drainage and wastewater treatment (5.5).', B8, S8)
C8 = add('8', 'c', '(c)', T8C,
         [row('reason-1', 'Reason 1 (2 for point, 3 for discussion)', 5, 'Point 2 and discussion 3. Such as: to prevent contamination of wells and groundwater with harmful bacteria and viruses; to protect people and animals from harmful organisms.'),
          row('reason-2', 'Reason 2 (2 for point, 3 for discussion)', 5, 'A second, different reason. Such as: to limit foul odours; to protect lakes, rivers and coastal waters from phosphorus, nitrogen and oxygen-depleting solids that damage biodiversity.')],
         ['cons-5-5'], ['drainage'], None, 'Underground drainage and wastewater treatment (5.5).', B8, S8)
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-system', B8, S8, parts(('a', T8A), ('b', T8B), ('c', T8C)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p41 (printed 39): (a) two functional requirements × (notes 4 + sketches 4) = 16; (b) formula, correct entry, floor area, Li = Lo × WF × E, solving for w (two lines) and the window area, 7 × 4 = 28; (c) two advantages and two disadvantages × (2 for point + 2 for discussion) = 16. Complete 60.'
S9 = 'No printed choice. Part (c) requires both two advantages and two disadvantages, separately marked: two required tasks composed into (c).'
T9A = 'Discuss in detail, using notes and freehand sketches, two functional requirements of a modern glazing system for a dwelling house.'
T9B = 'The sketch shows a living room which measures 4.5 metres long by 4.2 metres wide. The living room has a vertical window and unobstructed views. An average illumination of 500 lux of daylight is required on the work plane. Calculate using the degree of efficiency method, or any other suitable method, the appropriate area of glazing required to provide the stated illumination. Assuming the illumination of a standard overcast sky to be 5000 lux.'
T9C = 'Discuss two advantages and two disadvantages of installing triple glazing in a modern window framing system.'
A9 = add('9', 'a', '(a)', T9A,
         [row(f'requirement-{i}', f'Functional requirement {i}', 8, note) for i, note in [
             (1, 'Notes 4 and sketches 4. Such as: admit plenty of daylight and views of the surroundings; allow solar gain and keep it in, reducing lighting and heating costs.'),
             (2, 'A second, different requirement: notes 4 and sketches 4. Such as: prevent overheating and glare (smart or electrochromic glass); provide an emergency escape (at least 0.33 m² clear opening, 450 mm wide and high, cill no more than 1100 mm); reduce outside noise with airtight fitting and acoustic glass.')]],
         ['cons-3-6', 'cons-7-4'], ['windows-light'], 'q9-requirements', 'Glazing (3.6) for good illumination (7.4).', B9, S9)
B9b = add('9', 'b', '(b)', T9B,
          [row('formula', 'Formula', 4, 'Li = Lo × WF × E × window area ÷ floor area, where Li is the lux required, Lo the standard overcast sky (5000 lux), WF the window factor (0.5 for a vertical window) and E the efficiency coefficient (0.4).'),
           row('entry', 'Correct entry into formula', 4, '500 = 5000 × 0.5 × 0.4 × window area ÷ (4.5 × 4.2).'),
           row('floor-area', 'Floor area', 4, 'Floor area = 4.5 × 4.2 = 18.9 m².'),
           row('lux', 'Using formula Li = Lo × WF × E', 4, '500 = 1,000 × window area ÷ 18.9.'),
           row('window-area', 'Solve for w (window area)', 12, 'Two solving lines and the answer, 4 each: 500 × 18.9 = 1,000 W, so 9450 = 1,000 W; W = 9450 ÷ 1000; window area = 9.45 m².')],
          ['cons-7-2', 'cons-7-4'], ['windows-light'], 'q9-calculation', 'The daylight factor (7.2) for good illumination (7.4).', B9, S9)
c9 = [add('9', f'c-{kind}s', f'(c) — {kind}s', f'Discuss two {kind}s of installing triple glazing in a modern window framing system.',
          [row(f'{kind}-1', f'{kind.capitalize()} 1 (2 for point, 2 for discussion)', 4, n1), row(f'{kind}-2', f'{kind.capitalize()} 2 (2 for point, 2 for discussion)', 4, n2)],
          ['cons-3-6'], ['windows-light'], None, 'Glass and glazing (3.6).', B9, S9)
      for kind, n1, n2 in [('advantage', 'Point 2 and discussion 2. Such as: lower energy costs, with U-values as low as 0.6 W/m²K; up to 40% less heat loss than the best double glazing.',
                            'A second, different advantage. Such as: better acoustic insulation (heaviness, isolation, completeness); less condensation on the inner pane.'),
                           ('disadvantage', 'Point 2 and discussion 2. Such as: higher cost, up to 30% more on glazing; overheating on large south elevations without shading.',
                            'A second, different disadvantage. Such as: heavier units needing structural support and stronger hinges; unsuitable for retrofitting into existing frames.')]]
C9 = compose('9', 'c', '(c)', c9, None, B9, S9, T9C, labels=['Advantages', 'Disadvantages'])
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-calculation', B9, S9, parts(('a', T9A), ('b', T9B), ('c', T9C)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p42 (printed 40): (a) any two of three printed items × (notes 5 + sketches 5) = 20; (b) line diagram 5, MVHR unit location 5, ducting layout 5, direction of airflow 5, description 6 = 26; (c) two considerations × (4 for point + 3 for discussion) = 14. Complete 60.'
S10 = 'Choice is not a route: part (a) (any two of three printed items) is ONE card with an any-two group over the scheme headings. The OR alternative is a separate Question 10 route.'
T10A = 'Using notes and freehand sketches, discuss the importance of any two of the following in Passive House design: foundation design; solar shading; thermally efficient building envelope.'
T10B = 'The drawing shows the draft design of the ground floor plan for a new dwelling house. The engineer must design a Mechanical Ventilation with Heat Recovery (MVHR) system for this house. Draw a line diagram of the given house plan. Show on your diagram the location of the MVHR unit and a typical design layout for the system ducting. Indicate clearly the direction of the airflow in the ducts. Describe how the MVHR system works. Note: It is not necessary to show the furniture.'
T10C = 'Discuss in detail, two design considerations that need to be taken into account when deciding on the location of a MVHR unit in a dwelling house.'
ITEMS10 = [('Foundation design', 'highly insulated to a U-value of 0.10–0.15 W/m²K; no thermal bridge at the wall-floor junction; aerated concrete blocks at critical junctions; insulation with high compressive strength; an insulated Passive raft-type foundation.'),
           ('Solar shading', 'prevents overheating by admitting low winter sun and blocking high summer sun; overhangs or deeper eaves; fixed or adjustable brise-soleil, external blinds, awnings and sliding screens; trees and climbing plants.'),
           ('Thermally efficient building envelope', 'an unbroken line of insulation and airtightness around the whole building, with every element at its optimum performance; a constant, predictable internal temperature; lower energy use, costs and carbon.')]
A10 = add('10', 'a', '(a)', T10A,
          [dict(id='items', kind='anyN', verbatim='Discuss two Passive House design features', marks=20,
                contextNote='Any two of the three, each notes 5 and sketches 5 = 10. ' + ' '.join(f'{h}: {n}' for h, n in ITEMS10),
                group=dict(claimMax=2, perOption=10, options=[h for h, _ in ITEMS10]))],
          ['cons-6-4', 'cons-2-4', 'cons-6-2'], ['passive-design', 'foundations', 'heat-loss-insulation'], 'q10-features',
          'The union of the three printed items: passive design and solar shading (6.4), the insulated foundation (2.4) and the insulated envelope (6.2).', B10, S10)
B10b = add('10', 'b', '(b)', T10B,
           [row('diagram', 'Line diagram of given house', 5, 'A line diagram of the given ground floor plan.'),
            row('unit', 'Location of MVHR unit', 5, 'The MVHR unit located, for example in a utility or plant room inside the insulated envelope.'),
            row('ducting', 'Layout of system ducting', 5, 'Supply ducts to the living spaces and bedrooms and extract ducts from the kitchen, bathroom and utility, with a vent to each room.'),
            row('airflow', 'Direction of airflow in ducts', 5, 'The direction of airflow shown clearly in the supply and extract ducts.'),
            row('description', 'Decription of how the system works', 6, 'Fans supply fresh filtered air and extract stale, moist air continuously; in the heat exchanger the outgoing air warms the incoming air without the two mixing; a particle filter removes dust and pollen.')],
           ['cons-6-5'], ['condensation-air-tightness', 'passive-design'], 'q10-mvhr', 'Mechanical ventilation with heat recovery (6.5).', B10, S10)
C10 = add('10', 'c', '(c)', T10C,
          [row('consideration-1', 'Design consideration 1 (4 for point, 3 for discussion)', 7, 'Point 4 and discussion 3. Such as: accessibility for routine maintenance and filter changes; noise — a solid wall or floor with anti-vibration mounts, away from bedrooms.'),
           row('consideration-2', 'Design consideration 2 (4 for point, 3 for discussion)', 7, 'A second, different consideration. Such as: aesthetics — a discreet plant or utility room or an enclosing press; optimum function — an internal corner so the intake and exhaust are on different faces, and inside the insulated envelope to cut duct heat loss.')],
          ['cons-6-5'], ['condensation-air-tightness', 'passive-design'], None, 'Mechanical ventilation (6.5).', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-scheme', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p43 (printed 41): (a) three discussion points × (4 for point + 6 for discussion) = 30; (b) three guidelines × (4 + 6) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the Passive House question. Its parts are open responses.'
TAA = 'Discuss the above statement in detail.'
TAB = 'Propose three best practice guidelines that would ensure all buildings are designed and constructed to be flexible to meet people’s needs over their life.'
AA = add('10', 'a', '(a)', TAA,
         [row(f'point-{i}', f'Discussion Point {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: Universal Design caters for people’s changing needs so they can stay in their homes and communities as they age or become disabled; buildings usable by people of diverse abilities without special assistance.'),
             (2, 'Point 4 and discussion 6. Such as: an ageing population, with those over 65 set to more than double by 2050; a 60% chance a new home will be occupied by someone with a disability; most people prefer to age in place.'),
             (3, 'Point 4 and discussion 6. Such as: Universal Design is good design — flexible, easily adapted, cost and energy effective, working as well for a newborn as for a grandparent. Three distinct, well-argued points are needed.')]],
         ['cons-1-2'], ['planning-sustainability-environment'], None, 'Accessible design of the built environment (1.2).', BALT, SALT, alt=True)
AB = add('10', 'b', '(b)', TAB,
         [row(f'guideline-{i}', f'Guideline {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: clear planning guidelines requiring accessible homes; legislation that new builds and retrofits are future-proofed to a Universal Design standard.'),
             (2, 'Point 4 and discussion 6. Such as: public awareness of adaptable housing; CPD for architects and planners on lifetime homes.'),
             (3, 'Point 4 and discussion 6. Such as: soft spots in internal walls and hard spots in ceilings for a future hoist; firm, level, slip-resistant garden paths 900–1200 mm wide without ramps or steps. Three distinct guidelines are needed.')]],
         ['cons-1-2'], ['planning-sustainability-environment'], None, 'Accessible design of the built environment (1.2).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, parts(('a', TAA), ('b', TAB)), alt=True)

# ---------------------------------------------------------------- ledgers
pattern = r'\b(?:choose|select|one\s+of|any\s+\w+|either|or|answer\s+\w+)\b'
observed = []
with fitz.open(R / P) as pdf:
    for i, p in enumerate(pdf):
        text = ' '.join(p.get_text().split())
        observed.extend((i + 1, m.start(), m.group(), text[max(0, m.start() - 80):m.end() + 80]) for m in re.finditer(pattern, text, re.I))
ledger_rows = [
    (1, 'Answer any', 'Whole-exam selection: any five of the ten questions; all question banks retained, no full-exam Cartesian cards.'),
    (3, 'any two', 'Q4(b) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
    (6, 'or', 'Q9(b) method permission (“the degree of efficiency method, or any other suitable method”): any method marked alike, not an answer selection.'),
    (6, 'any other', 'Q9(b) method permission (“or any other suitable method”): any method marked alike, not an answer selection.'),
    (7, 'any two', 'Q10(a) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
    (7, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.'),
    (7, 'or', 'Quotation narrative (“ability or disability”), not an answer directive.'),
    (7, 'or', 'Quotation narrative (“temporary or permanent injury”), not an answer directive.'),
    (7, 'or', 'Quotation narrative (“or an older person living independently”), not an answer directive.'),
]
assert [(o[0], o[2]) for o in observed] == [(r[0], r[1]) for r in ledger_rows], [(o[0], o[2]) for o in observed]
selection_ledger = dict(pattern=pattern, unclassified=0, sourceHashes=HASHES,
                        rows=[dict(page=o[0], start=o[1], match=o[2], context=o[3], classification=r[2]) for o, r in zip(observed, ledger_rows)],
                        finiteQuestionChoices={'4b': dict(choose=2, options=[h for h, _ in ITEMS4], cardId=A4b['id'], groupRowId='items'),
                                               '10a': dict(choose=2, options=[h for h, _ in ITEMS10], cardId=A10['id'], groupRowId='items')})
whole = {}
for t in tasks:
    c = t['card']
    if '-complete' in c['id']:
        whole.setdefault('10-alt' if t['alternative'] else t['questionNumber'], []).append(dict(id=c['id'], parts=[g['label'] for g in c['taskGroups']], marks=c['totalMarks']))

REASONS = {
    'q1-a': 'Rows rebuilt to the printed table with the scale and drafting allowance (8): 48 → 56.',
    'q1-b': 'Reshaped to the printed criterion row; tariff unchanged (4).',
    'q2-a-communication': 'Reshaped to the printed 3 point + 3 discussion row; tariff unchanged (6).',
    'q2-a-supervision': 'Reshaped to the printed 3 point + 3 discussion row; tariff unchanged (6).',
    'q2-a-training': 'Reshaped to the printed 3 point + 3 discussion row; tariff unchanged (6).',
    'q2-b-site-access': 'Split into the two printed guidelines (4 for note + 4 for sketch); tariff unchanged (16).',
    'q2-b-using-a-ladder': 'Split into the two printed guidelines (4 for note + 4 for sketch); tariff unchanged (16).',
    'q2-c': 'Split into the two printed reasons (3 for point + 2 for discussion); tariff unchanged (10).',
    'q3-a': 'Replaces an any-N pool of consideration headings with the three printed design considerations (3 + 3 each); tariff unchanged (18).',
    'q3-b': 'Rebuilt to the printed rows — layout 14, the three considerations 2 each, justification 2: 6 → 22.',
    'q3-c-advantages': 'Split into the two printed advantages (3 for point + 2 for discussion); tariff unchanged (10).',
    'q3-c-disadvantages': 'Split into the two printed disadvantages (3 for point + 2 for discussion); tariff unchanged (10).',
    'q4-a': 'Split into three vernacular features, each notes 5 + sketches 5; tariff unchanged (30).',
    'q4-b': 'Now one card printing all three items with an any-two group over the scheme headings (4 + 3 each); tariff unchanged (14).',
    'q4-c': 'Split into the two printed reasons (4 for point + 4 for discussion); tariff unchanged (16).',
    'q5-b': 'Reshaped to the five printed calculation steps (3 each) with the scheme’s worked answer; tariff unchanged (15).',
    'q6-a': 'Split into three design features, each notes 5 + sketches 5; tariff unchanged (30).',
    'q6-b': 'All three printed technologies required, each notes 3 + sketches 3, replacing an any-N pool of photovoltaic bullets; tariff unchanged (18).',
    'q6-c': 'Split into the two printed advantages (3 for point + 3 for discussion); tariff unchanged (12).',
    'q7-a': 'Rows rebuilt to the printed table with the scale and drafting allowance (8): 48 → 56.',
    'q7-b': 'Reshaped to the printed design-detail row; tariff unchanged (4).',
    'q8-a': 'Split into the three printed functional requirements (3 for point + 5 for discussion); tariff unchanged (24).',
    'q8-c': 'Split into the two printed reasons (2 for point + 3 for discussion); tariff unchanged (10).',
    'q9-a': 'Split into two functional requirements, each notes 4 + sketches 4; tariff unchanged (16).',
    'q9-b': 'Reshaped to the printed calculation rows with the scheme’s worked answer (9.45 m²); tariff unchanged (28).',
    'q9-c-advantages': 'Split into the two printed advantages (2 for point + 2 for discussion); tariff unchanged (8).',
    'q9-c-disadvantages': 'Split into the two printed disadvantages (2 for point + 2 for discussion); tariff unchanged (8).',
    'q10-a': 'Now one any-two group over the three printed items (notes 5 + sketches 5 each), replacing three separate five-mark pools; tariff unchanged (20).',
    'q10-c': 'Split into the two printed considerations (4 for point + 3 for discussion); tariff unchanged (14).',
}
assert set(REASONS) == {k.removeprefix(PREFIX) for k in LEGACY}
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
assert len(corrections) == 29

out = dict(schemaVersion=1, subjectId='construction-studies', year=2023, level='higher', lang='ev', sitting='main', paperKey='single',
           fileid='LC029ALP000EV.pdf', component='theory', status='Q1–Q10 and alternative Q10 source-reviewed draft; integration pending.',
           sourceHashes=HASHES, tasks=tasks, bindings=bindings, questionFigures=question_figures,
           addedIds=[t['card']['id'] for t in tasks if not t['correction']], corrections=corrections,
           selectionLedger=selection_ledger, questionRouteLedgers={q: dict(wholeRoutes=w) for q, w in whole.items()}, taxonomyGaps=[],
           questionsReviewed=[str(n) for n in range(1, 11)], unreviewedQuestions=[], alternativeQuestions=['10'])
(HERE / 'higher-2023-draft.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(tasks=len(tasks), added=len(out['addedIds']), corrected=len(corrections), figures=len(question_figures),
                      perQuestion={q: sum(1 for t in tasks if t['questionNumber'] == q and not t['alternative']) for q in QUESTIONS},
                      alternative=sum(1 for t in tasks if t['alternative']), wholeRoutes={q: len(w) for q, w in whole.items()})))
