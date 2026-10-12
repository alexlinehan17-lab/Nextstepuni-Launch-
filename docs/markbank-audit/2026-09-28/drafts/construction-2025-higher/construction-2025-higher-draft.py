"""Draft the 2025 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Question wording is lifted from the SEC paper: a narrowed task only deletes printed words.
Where the paper identifies a choice only by a circle on its drawing (Q8), or a part refers back
to an earlier list (Q2(c)), the card names the item after ' — ' using the marking scheme's own
heading for it. Every row's verbatim is printed in the scheme's mark tables (pages 37-47),
checked against rendered pages. Unbanded components accept any whole mark up to the published
maximum; printed excellent/good/fair bands are kept as printed. Figures are exact 2x crops of
the original PDFs.

The 21 pre-audit 2025 Higher cards keep their IDs (and concept IDs) and are corrected in place
to the reviewed boundaries and tariffs; each correction records the SHA-256 of the card it
replaces. Every other prior card stays byte-identical.
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
P = 'paper-trail-corpus/exampapers/2025/LC029ALP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2025/LC029ALP000EV.pdf'
HASHES = {P: 'b0779f335d38e88afcae39af2e5aa9124a53e3472aa3a9f535c7d9989ebb8dec',
          S: 'c9ca8dee72bc663d239244d9cde736b284de65540f48bb7aa9763d0baed1189b'}
ATTRIBUTION = 'SEC Leaving Certificate Construction Studies 2025 Higher Level — © State Examinations Commission.'
FP = 'construction-studies-2025-HL-'
PREFIX = 'cons-2025-hl-'
CROSS = 'construction-studies-higher-'
BAND8 = [0, 4, 6, 8]
PAGE = [48, 46, 591, 803]

for f, h in HASHES.items():
    assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f

# The pre-audit cards are snapshotted before integration so the draft regenerates byte-identically afterwards.
LEGACY_FILE = HERE / 'prior-2025-higher-cards.json'
if not LEGACY_FILE.exists():
    AUTHORED = json.loads((R / 'scripts/markbank/authored/construction-studies.json').read_text())
    LEGACY_FILE.write_text(json.dumps([c for c in AUTHORED if c['id'].startswith(PREFIX)], ensure_ascii=False, indent=2) + '\n')
LEGACY = {c['id']: c for c in json.loads(LEGACY_FILE.read_text())}
assert len(LEGACY) == 21, sorted(LEGACY)


def card_hash(c):
    return hashlib.sha256(json.dumps(c, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


FIGURES = {
    'q1-original': (P, 2, [45, 50, 575, 380], False),
    'q1-section': (S, 4, PAGE, True),
    'q1-radon': (S, 5, [48, 580, 568, 760], True),
    'q2-original': (P, 2, [45, 440, 580, 750], False),
    'q2-trench': (S, 8, PAGE, True),
    'q2-attic': (S, 9, [48, 46, 582, 384], True),
    'q2-chimney': (S, 9, [48, 384, 582, 790], True),
    'q3-original': (P, 3, [45, 50, 580, 455], False),
    'q3-layout-1': (S, 10, PAGE, True),
    'q3-layout-2': (S, 11, PAGE, True),
    'q3-garage': (S, 13, PAGE, True),
    'q4-original': (P, 3, [45, 470, 580, 745], False),
    'q4-requirements': (S, 14, PAGE, True),
    'q4-walls': (S, 15, PAGE, True),
    'q5-original': (P, 4, [45, 50, 575, 750], False),
    'q5-calculation': (S, 20, PAGE, True),
    'q5-thickness': (S, 21, [48, 46, 568, 380], True),
    'q6-original': (P, 5, [45, 50, 580, 470], False),
    'q6-low-impact': (S, 22, PAGE, True),
    'q7-original': (P, 5, [45, 500, 580, 760], False),
    'q7-section': (S, 25, PAGE, True),
    'q7-flashing': (S, 26, [48, 45, 568, 622], True),
    'q8-original': (P, 6, [45, 50, 575, 395], False),
    'q8-door-head': (S, 27, [48, 326, 568, 497], True),
    'q8-first-floor': (S, 27, [48, 498, 568, 790], True),
    'q8-wallplate': (S, 28, [48, 46, 568, 255], True),
    'q8-mvhr-duct': (S, 28, [48, 296, 568, 588], True),
    'q9-original': (P, 6, [45, 455, 575, 740], False),
    'q9-wiring': (S, 29, PAGE, True),
    'q9-safety': (S, 30, [48, 46, 568, 446], True),
    'q10-original': (P, 7, [45, 50, 580, 410], False),
    'q10-building-form': (S, 31, [48, 132, 568, 382], True),
    'q10-foundation-design': (S, 31, [48, 382, 568, 790], True),
    'q10-space-heating-energy-demand': (S, 32, [48, 46, 568, 308], True),
    'q10-orientation': (S, 32, [48, 314, 568, 790], True),
    'q10-overheating': (S, 33, PAGE, True),
    'q10-alt-original': (P, 7, [45, 490, 580, 725], False),
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
    '1': dict(page=2, title='Strip foundation, ground floor, timber-frame wall and window section', concept='timber-frame-window-section',
              stem='A triple glazed window is fitted in the external wall of a dwelling house, as shown. The window has a thermally broken wooden frame. The fixed frame of the window is 120 mm × 80 mm. The wall is of timber frame construction with an external rendered concrete block outer leaf. The internal timber frame is 250 mm × 50 mm with a 50 mm service cavity provided at the internal surface. The bottom of the concrete cill is located 300 mm above finished floor level. The ground floor is a solid concrete floor with a 20 mm quarry tile finish.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the radon detail in (b) is marked separately. Any alternative detailing that meets current Building Regulations is acceptable.'),
    '2': dict(page=2, title='Health and safety on a construction site', concept='site-safety-culture', stem='',
              note='Original question retained. Part (a) chooses any two of three printed items; parts (b) and (c) require all three activities, each separately priced. The scheme lists typical points, not an exhaustive list.'),
    '3': dict(page=3, title='Revising a semi-detached house and garage layout', concept='garage-layout-revision',
              stem='The drawing shows the front elevation and ground floor plan of a semi-detached house with an adjoining garage. The wall A-A is south facing. The owners wish to revise the design of the ground floor layout and garage space to: include a downstairs bathroom; create an open-plan kitchen/dining and living area; optimise daylight into the ground floor.',
              note='Original elevation and plan retained. The scheme shows two acceptable layouts; any well-reasoned layout meeting all three requirements is acceptable.'),
    '4': dict(page=3, title='High-performance external walls', concept='high-performance-external-wall', stem='',
              note='Original sketch retained. Functional requirements and wall types are open choices; the scheme lists typical examples, not a printed list.'),
    '5': dict(page=4, title='Externally insulated hollow-block wall: U-value, heat-loss cost and Passive House upgrade', concept='hollow-block-external-insulation',
              stem='The external wall of a house built in the 1970s is of single leaf hollow-block construction with an external render. Insulated plasterboard is fixed to the internal surface of the wall. It is proposed to upgrade the thermal properties of the external wall by installing external insulation as shown.',
              note='All printed data are retained in the original question. Parts (b) and (c) use the U-value from part (a); the scheme’s worked answers are U = 0.221 W/m²°C, an annual cost of €76.34 and 137 mm of additional insulation.'),
    '6': dict(page=5, title='Low-impact single-storey house and a healthy indoor environment', concept='low-impact-healthy-house',
              stem='The elevation and ground floor plan of a single-storey house are shown. The external walls are of timber frame construction with a rendered concrete block and locally sourced larch cladding external finish. Space heating is provided using a renewable heat source. The house is designed to have a low environmental impact.',
              note='Original elevation and plan retained. Part (b) requires all three printed items, each separately priced. Features and benefits are open; the scheme lists typical examples.'),
    '7': dict(page=5, title='Chimney stack through a pitched roof', concept='chimney-stack-section',
              stem='A chimney stack projects through the pitched roof of a house as shown. The chimney stack is of solid concrete block construction with an external sand/cement render finish. The traditional cut roof has a pitch of 30° with a slate finish.',
              note='Original sketch retained. Construction, slate-course and scale/drafting marks belong to part (a); the rainwater detail in (b) is marked separately.'),
    '8': dict(page=6, title='Airtight building envelope', concept='airtight-envelope',
              stem='An airtight external building envelope is important in the design of a dwelling house.',
              note='Original drawing with four circled locations retained. Part (b) chooses any three: every combination is kept, and each location keeps its own 16 marks. Locations are named with the marking scheme’s headings.'),
    '9': dict(page=6, title='Domestic lighting circuit', concept='lighting-circuit', stem='',
              note='Original sketch retained. Cable sizes and colours in the scheme are the typical values.'),
    '10': dict(page=7, title='Passive House in a rural setting', concept='rural-passive-house',
               stem='The sketch shows the proposed design of a Passive House which is to be constructed in a rural setting.',
               note='Original sketch retained. Part (a) chooses any two of three printed items: every pair is kept, and each item keeps its own 10 marks.'),
}
ALT = dict(page=7, title='Reusing the historic built environment (alternative Question 10)', concept='historic-building-reuse',
           stem='“The historic built environment is critical in addressing climate change. Protecting, adapting and reusing historic building stock reduces environmental waste and the carbon dioxide emissions associated with demolition and reconstruction. Traditional building methods and materials have much to teach us about the skills needed to work with prevailing weather conditions and the use of available local materials.” Adapted from: Heritage Ireland 2030 Department of Housing, Local Government and Heritage Published on: gov.ie/housing',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the Passive House question.')
SCHEME_PAGES = {'1': [4, 5, 37], '2': [6, 7, 8, 9, 38], '3': [10, 11, 12, 13, 39], '4': [14, 15, 16, 17, 18, 19, 40],
                '5': [20, 21, 41], '6': [22, 23, 24, 42], '7': [25, 26, 43], '8': [27, 28, 44],
                '9': [29, 30, 45], '10': [31, 32, 33, 46], '10-alt': [34, 35, 47]}

tasks, bindings, cards = [], [], {}


def add(q, key, ref, text, rows, nodes, topics, figure, review, boundary, selection, groups=None, total=None, alt=False):
    meta = ALT if alt else QUESTIONS[q]
    qkey = '10-alt' if alt else q
    cid = f'{PREFIX}q{qkey}-{key}'
    concept = LEGACY[cid]['conceptId'] if cid in LEGACY else f"{meta['concept']}-{key}"
    card = dict(id=cid, subjectId='construction-studies', year=2025, level='higher', section='B',
                topicId=nodes[0], conceptId=concept, questionRef=f"2025 HL Q{qkey}{ref}",
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
B1 = 'Scheme p37 (printed 1): (a) foundation and solid ground floor 5 × 4, external wall 4 × 4, window detail 3 × 4 (3 for drawing, 1 for annotation) = 48, scale 4 + drafting 4 banded excellent 8/good 6/fair 4 = 56; (b) radon detail 4. Complete 60. The scale/drafting allowance assesses the section drawn in (a), so it stays with (a).'
S1 = 'One required section and one required radon detail. The scheme detail lists are marking menus, not printed choices.'
A1 = add('1', 'a', '(a)',
         'To a scale of 1:5, draw a vertical section through the external wall, ground floor, and window. Show the typical construction details from the bottom of the strip foundation to a level 200 mm above the bottom frame of the window. Show a 1.0 metre width of ground floor.',
         [row('foundation-floor', 'Foundation and solid concrete ground floor – typical detailing', 20, 'Best five foundation and ground-floor details, 4 each (3 for drawing, 1 for annotation). Marking menu: R.C. strip foundation; dead blockwork and cavity wall above foundation; cavity infill; thermal blocks on inner leaf; DPC; hardcore/sand blinding/radon barrier; subfloor; insulation; screed; airtightness barrier at floor and wall junction; 20 mm quarry tile finish/skirting board.'),
          row('external-wall', 'External wall – typical detailing', 16, 'Best four external-wall details, 4 each (3 for drawing, 1 for annotation). Marking menu: external render; concrete block outer leaf; air space/residual cavity; anchor strap; breather membrane; racking board; 250 × 50 mm stud detail and insulation; OSB sheeting; airtightness membrane; 50 mm insulated service cavity; plasterboard and skim.'),
          row('window', 'Window detail – typical detailing', 12, 'Best three window details, 4 each (3 for drawing, 1 for annotation). Marking menu: cavity closer; concrete window cill; DPC at cill (cill wrapped in DPC); thermally broken window frame; window board; triple glazing; airtight barrier at junction.'),
          row('presentation', 'Scale - 4 marks Drafting - 4 marks', 8, 'Scale 4 and drafting 4, assessed together: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-2-4', 'cons-4-2', 'cons-3-3', 'cons-3-6'],
         ['question-1-drawing-questions', 'foundations', 'floors', 'walls', 'windows-light'], 'q1-section',
         'Scaled drawing (1.5) from the strip foundation (2.4) through the solid ground floor (4.2) and timber-frame external wall (3.3) to the window cill (3.6).',
         B1, S1)
B1b = add('1', 'b', '(b)',
          'On your drawing, show the typical design detailing that will prevent the penetration of radon gas into the house.',
          [row('radon', 'Design detailing identified to prevent the penetration of radon gas', 4,
               'Show and identify the radon barrier: a gas-resistant membrane across the ground floor, carried continuously across the wall as in the scheme’s model detail. Any other relevant point is acceptable.')],
          ['cons-3-4', 'cons-4-2'], ['walls', 'floors'], 'q1-radon',
          'A radon barrier is a damp/gas-proof membrane (3.4) in the solid ground floor (4.2).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p38 (printed 2): (a) any two of three printed items × 6 = 12; (b) one risk for each of three printed activities × 4 = 12; (c) for each activity Guideline 1 and Guideline 2, each 3 for note + 3 for sketch = 12 per activity, 36. Complete 60.'
S2 = 'Part (a) selects any two of three printed items: C(3,2) = 3 pairs plus each single item. Parts (b) and (c) require all three activities, each separately priced, so they are split per activity, not offered as choices. Complete question: 3 routes.'
ITEMS2 = [
    ('safety-training', 'safety training', 'Safety training',
     'Such as: Safe Pass is mandatory and kept current through refresher courses; training builds awareness of site risks and the skills to identify them and follow best practice; specialist tickets for machinery and vehicles; monitoring and enforcing safe work practices; it may be a condition of the insurance provider.'),
    ('health-and-safety-officer', 'health and safety officer', 'Health and safety officer',
     'Such as: provides induction and ongoing training (working at heights, machinery use); develops emergency response plans; keeps first aid and emergency equipment available; ensures the correct PPE is worn; carries out safety inspections and risk assessments; reviews the safety statement; investigates, records and reports accidents.'),
    ('risk-assessment-audit', 'risk assessment audit', 'Risk assessment audit',
     'Such as: provides a safe working environment; evaluates compliance with safety regulations and policies; identifies hazards and puts control measures in place where a risk cannot be eliminated (for fire: alarms, evacuation signage, drills, extinguishers); recommends improvements; identifies training needs; reduces accidents and liability.'),
]
STEM2A = 'Discuss in detail the importance of {any}the following in maintaining a positive health and safety culture among workers on a construction site: {items}.'
a2 = {}
for slug, item, verbatim, content in ITEMS2:
    a2[slug] = add('2', f'a-{slug}', f'(a) — {item}', STEM2A.format(any='', items=item),
                   [row('importance', verbatim, 6, f'Discuss the importance of {item}. ' + content)],
                   ['cons-1-8'], ['site-safety'], None, 'Safety precautions on site (1.8).', B2, S2)
a2_pairs = {}
for (s1, i1, *_), (s2, i2, *_) in itertools.combinations(ITEMS2, 2):
    a2_pairs[(s1, s2)] = compose('2', f'a-{s1}-and-{s2}', f'(a) — {i1} and {i2}', [a2[s1], a2[s2]], None, B2, S2,
                                 STEM2A.format(any='any two of ', items=f'{i1}; {i2}'), labels=[i1, i2])
ACTIVITIES = [
    ('deep-trench', 'working in a deep trench', 'Working in a deep trench', 'q2-trench',
     'One risk outlined. Such as: workers seriously injured or buried if the trench sides collapse; machinery or vehicles falling in; materials stored too close to the edge causing a collapse; falling into an unguarded trench; materials falling in; nearby structures undermined.',
     'Note 3 and sketch 3. Such as: a trench box or shuttering to support the sides; battering back (sloping) the sides; a barrier with a toe board, or a temporary cover over a vacant trench.',
     'A second, different guideline: note 3 and sketch 3. Such as: no materials, machinery or vehicles near the edge; a clearly marked exclusion zone and signage; PPE (hard hat, eye protection, footwear); digging in suitable, not wet, conditions; an engineer’s survey of nearby structures.'),
    ('attic-insulation', 'installing insulation in an attic space', 'Installing insulation in an attic space', 'q2-attic',
     'One risk outlined. Such as: falling through the plasterboard ceiling; injury when cutting the insulation; skin or eye irritation without a coverall, gloves and goggles; electrocution from exposed wires; fire if insulation covers recessed lights; lung damage from inhaled machine-made mineral fibres (MMMFs).',
     'Note 3 and sketch 3. Such as: crawl boards to spread the load across the joists, or walking only on the joists and never on the plasterboard ceiling; a hooded coverall and gloves; an appropriate dust mask.',
     'A second, different guideline: note 3 and sketch 3. Such as: safety goggles; non-combustible protection covers over downlighters; cutting insulation in a well-ventilated area; kneepads.'),
    ('chimney-capping', 'repairing a chimney capping', 'Repairing a chimney capping', 'q2-chimney',
     'One risk outlined. Such as: falling or slipping from the roof or from a ladder; equipment or materials dropped on people below; scaffolding collapsing; falling from lifting machinery such as a cherry picker.',
     'Note 3 and sketch 3. Such as: a safety harness or other fall protection; scaffolding around the stack erected by certified personnel, tied to the house or chimney, with safety rails and toe boards.',
     'A second, different guideline: note 3 and sketch 3. Such as: toe boards and netting against falling objects; ladders secured and extending 1 metre past the scaffolding platform; a cherry picker operated by certified personnel on a level surface, with workers securely attached.'),
]
STEM2B = 'Outline one possible risk to personal safety associated with each of the following: {items}.'
STEM2C = 'For each risk discussed at 2(b) above, show, using notes and freehand sketches, two best practice guidelines that should be observed to reduce the possibility of injury to a worker undertaking each task.'
b2, c2 = {}, {}
for slug, item, verbatim, figure, risk, g1, g2 in ACTIVITIES:
    b2[slug] = add('2', f'b-{slug}', f'(b) — {item}', STEM2B.format(items=item),
                   [row('risk', verbatim, 4, risk)], ['cons-1-8'], ['site-safety'], None, 'Safety precautions on site (1.8).', B2, S2)
for slug, item, verbatim, figure, risk, g1, g2 in ACTIVITIES:
    c2[slug] = add('2', f'c-{slug}', f'(c) — {item}', STEM2C.removesuffix('.') + f' — {item}',
                   [row('guideline-1', 'Guideline 1 (3 for note, 3 for sketch)', 6, g1),
                    row('guideline-2', 'Guideline 2 (3 for note, 3 for sketch)', 6, g2)],
                   ['cons-1-8'], ['site-safety'], figure, 'Safety precautions on site (1.8).', B2, S2)
B2b = compose('2', 'b', '(b)', list(b2.values()), None, B2, S2,
              STEM2B.format(items='; '.join(a[1] for a in ACTIVITIES)), labels=[a[1] for a in ACTIVITIES])
C2 = compose('2', 'c', '(c)', list(c2.values()), 'q2-trench', B2, S2, STEM2C, labels=[a[1] for a in ACTIVITIES])
for (s1, s2), pair in a2_pairs.items():
    compose('2', f'complete-{s1}-and-{s2}', f" — complete: {pair['questionRef'].split(' — ')[1]}",
            [pair, B2b, *c2.values()], 'q2-trench', B2, S2, parts(pair, B2b, C2),
            labels=[f"(a) {pair['questionRef'].split(' — ')[1]}", '(b)'] + [f'(c) {a[1]}' for a in ACTIVITIES])

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p39 (printed 3): (a) revised layout 16 + downstairs bathroom 2 + open-plan 2 + daylight 2 = 22; (b) three reasons × 6 = 18; (c) notes 10 + sketch 10 = 20. Complete 60.'
S3 = 'The three design requirements are all required in one layout, not a choice. The scheme shows two model layouts; layouts, reasons and external designs are open responses.'
A3 = add('3', 'a', '(a)', 'Using notes and freehand sketches, show a revised internal layout for the ground floor that incorporates each of the above design requirements.',
         [row('layout', 'Revised internal layout for the ground floor and garage space', 16, 'Notes and freehand sketch of a coherent revised ground-floor plan that uses the garage space and respects the south-facing wall A-A. Such as (two model layouts): remove the wall between the garage and utility for one large space; replace the garage door with high-performance glazing; a corner window on the south-west; sliding or bi-fold doors to a patio; doorways into the corridor or at both ends of the new space (steel beams where a wall is load-bearing).'),
          row('bathroom', 'Include a downstairs bathroom', 2, 'A downstairs bathroom included, for example a large family bathroom where the kitchen or dining room was, on an external wall with easy access to the drainage.'),
          row('open-plan', 'Create an open-plan kitchen/dining and living area', 2, 'An open-plan kitchen/dining and living area, for example by combining the garage and utility into one large space.'),
          row('daylight', 'Optimising daylight into the ground floor', 2, 'Daylight optimised, for example high-performance glazing on the south and west, a corner window, roof lights in the garage roof, or glazed doors between rooms.')],
         ['cons-1-2', 'cons-7-4', 'cons-6-4'], ['planning-sustainability-environment', 'windows-light'], 'q3-layout-1',
         'Layout design within the built environment (1.2), good daylighting (7.4) and solar gain (6.4).', B3, S3)
B3b = add('3', 'b', '(b)', 'Outline three reasons for your proposed layout.',
          [row(f'reason-{i}', f'Reason {i}', 6, note) for i, note in [
              (1, 'One reason for the layout. Such as: combining the garage and utility gives a large south-facing space for open-plan kitchen/dining and living; high-performance glazing in place of the garage door improves solar gain and thermal performance.'),
              (2, 'A second reason. Such as: south-facing glazing makes the open-plan space bright and warm and lessens the need for artificial light and energy bills; glazed doors let evening light from the west into the sitting room.'),
              (3, 'A third reason. Such as: a large, wheelchair-accessible family bathroom suits lifetime use; roof lights flood the new space with light for wellbeing; matching brick keeps the character of the converted garage. Three distinct reasons are needed.')]],
          ['cons-1-2', 'cons-6-4', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'], None,
          'Reasons drawn from layout design (1.2), solar gain (6.4) and daylight (7.4).', B3, S3)
C3 = add('3', 'c', '(c)', 'Using notes and freehand sketches, show a revised external design for the garage that will enhance the overall visual appearance of the house.',
         [row('notes', 'Notes', 10, 'Such as: replace the garage door with high-performance glazing (full height or above worktop level); the same plaster finish as the house, or brick to strengthen the connection with it; glazing to the south and west and roof lights in the garage roof; solar shading against overheating; keep a bitumen flat roof, use zinc, or raise the pitch and slate it to match the house.'),
          row('sketch', 'Sketch', 10, 'Freehand sketch of the revised garage exterior.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q3-garage',
         'External design of an alteration within the built environment (1.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-layout-1', B3, S3, parts(A3, B3b, C3))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p40 (printed 4): (a) three functional requirements × (notes 3 + sketches 3) = 18; (b) two external wall constructions × (notes 5 + sketches 6 + position of insulation 2 + dimensions 2) = 30; (c) for each wall type advantage 3 + disadvantage 3 = 12. Complete 60.'
S4 = 'Requirements and wall types are open choices: the scheme lists typical examples, not a printed list. Part (c) refers to the two wall types drawn in (b).'
A4 = add('4', 'a', '(a)', 'Discuss in detail, using notes and freehand sketches, three functional requirements of an external wall suitable for a new dwelling house.',
         [row(f'requirement-{i}', f'Functional Requirement {i}', 6, note) for i, note in [
             (1, 'Notes 3 and sketches 3. Such as: structural stability — support the floors and roof, spread loads evenly to the foundations, provide robust openings and avoid cracking under load; or thermal comfort — room for insulation and a high thermal mass.'),
             (2, 'Notes 3 and sketches 3. Such as: weather resistance — no moisture ingress from wind-driven rain, low-maintenance finishes, no cold bridges, no condensation or interstitial dampness; or acoustic resistance to external noise.'),
             (3, 'Notes 3 and sketches 3. Such as: fire resistance for at least 30 minutes before structural integrity is compromised; sustainability — local, durable, recyclable materials; airtightness by sand cement plaster, membranes, tapes, paint or foam. Three distinct requirements are needed.')]],
         ['cons-3-2', 'cons-3-3'], ['walls'], 'q4-requirements', 'Functions of the external envelope (3.2) for an external wall (3.3).', B4, S4)
B4b = add('4', 'b', '(b)', 'The sketch shows the proposed design of a new house. The owners wish to specify a high-performance external wall design for their house. Using notes and freehand sketches, show the typical design detailing for two different external wall construction types that can achieve a high-performance for their house. For each design detail show the position of the insulation and include the typical dimensions of the wall.',
          [row('construction-1', 'External Wall Construction 1', 15, 'Notes 5, sketches 6, position of insulation 2 and dimensions 2 for the first wall type. Such as: block cavity — 100 mm outer leaf, 200 mm insulated cavity, 100 mm inner leaf, sand cement render and plaster for airtightness, DPC in the rising wall, thermal blocks in the inner-leaf rising wall; or insulated concrete forms — two 75 mm EPS panels joined by polypropylene webs around a 150 mm reinforced concrete core (300 mm), with acrylic render.'),
           row('construction-2', 'External Wall Construction 2', 15, 'The same four components (5 + 6 + 2 + 2) for a second, different wall type. Such as: 215 mm solid concrete block with up to 150 mm external insulation and acrylic render; timber frame with a brick outer leaf — 100 mm brick, 50 mm cavity, 140 mm insulated studs, 12 mm sheathing, breather membrane outside and airtightness membrane on the warm side; 215 mm solid block with a 25 mm batten, 50 mm insulation, vapour barrier and 12.5 mm plasterboard inside; or an insulated cavity wall with a 52 mm insulated slab on the inner leaf.')],
          ['cons-3-3', 'cons-6-2'], ['walls', 'heat-loss-insulation'], 'q4-walls', 'External wall construction (3.3) and the position of insulation (6.2).', B4, S4)
C4 = add('4', 'c', '(c)', 'Discuss one advantage and one disadvantage of each wall type you have shown at 4(b) above.',
         [row('construction-1', 'External Wall Construction 1', 6, 'Advantage 1 (3) and disadvantage 1 (3) of the first wall type shown at 4(b). Such as, for an insulated block cavity wall: better insulation, durability, fire resistance, sound insulation and moisture protection; against it, skilled labour is scarce and a bridged cavity lets damp and cold through.'),
          row('construction-2', 'External Wall Construction 2', 6, 'Advantage 1 (3) and disadvantage 1 (3) of the second wall type. Such as: ICF — superior energy efficiency and faster construction, but a high initial cost and specialised labour; solid block with external insulation — thermal mass and steady temperatures, but thermal bridging if poorly detailed; timber frame with brick — fast and sustainable, but poorer acoustic performance and rot if the detailing fails.')],
         ['cons-3-3'], ['walls'], None, 'Comparing external wall constructions (3.3).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-walls', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p41 (printed 5): (a) eleven entries × 3 — external and internal surface resistances, seven layers, total resistance and U-value — = 33; (b) five calculation steps × 3 = 15; (c) four calculation steps × 3 = 12. Complete 60. The seven layer entries form one 21-mark row so the task keeps the five-row limit.'
S5 = 'Required calculations; no printed choice. Parts (b) and (c) use the U-value from (a); the scheme marks each later step on the candidate’s own value.'
A5 = add('5', 'a', '(a)',
         'Calculate the U-value of the proposed wall, given the construction has the following sequence and data: External acrylic render thickness 8 mm External polystyrene insulation thickness 100 mm External render thickness 16 mm Hollow concrete block thickness 215 mm Insulation thickness 25 mm Plasterboard thickness 12.5 mm Internal skim coat thickness 3 mm. Thermal data of the external wall: Resistance of external surface (R) 0.048 m2 ºC/W; Conductivity of acrylic render (k) 0.670 W/m ºC; Conductivity of external insulation (k) 0.030 W/m ºC; Resistivity of external render (r) 2.170 m ºC/W; Resistance of hollow concrete block (R) 0.210 m2 ºC/W; Conductivity of insulation (k) 0.037 W/m ºC; Conductivity of plasterboard (k) 0.160 W/m ºC; Resistivity of skim coat (r) 5.550 m ºC/W; Resistance of internal surface (R) 0.122 m2 ºC/W.',
         [row('external-surface', 'External surface resistance', 3, 'External surface resistance 0.048 m²°C/W (given).'),
          row('internal-surface', 'Internal surface resistance', 3, 'Internal surface resistance 0.122 m²°C/W (given).'),
          row('layers', 'Formulae: R=T/k R=T × r', 21, 'Seven layer resistances, 3 each: acrylic render 0.008 ÷ 0.670 = 0.012; external insulation 0.100 ÷ 0.030 = 3.333; sand cement render 0.016 × 2.170 = 0.035; hollow concrete block 0.210 (given); insulation 0.025 ÷ 0.037 = 0.676; plasterboard 0.0125 ÷ 0.160 = 0.078; internal skim coat 0.003 × 5.550 = 0.017 m²°C/W.'),
          row('total-resistance', 'Total resistance', 3, 'Total resistance Rt = 4.531 m²°C/W (sum of all resistances).'),
          row('u-value', 'Calculation of U-value (w/m2 °C or w/m2k)', 3, 'U = 1 ÷ Rt = 1 ÷ 4.531 = 0.221 W/m²°C, with units.')],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Thermal resistance and U-value calculation (6.1).', B5, S5)
B5b = add('5', 'b', '(b)',
          'Using the U-value of the wall obtained at 5(a) above and the following data, calculate the cost of heat lost annually through this wall: area of external wall 144 m2; average internal temperature 19 ºC; average external temperature 6 ºC; heating period 7 hours daily for 33 weeks per annum; cost of wood pellets 55 cent per kg; calorific value of wood pellets 17350 kJ per kg; 1000 Watts 1 kJ per second.',
          [row('heat-loss', 'Heat loss formula and calculation', 3, 'Heat loss = U × area × temperature difference = 0.221 × 144 × (19 − 6) = 413.712 W (J/s).'),
           row('duration', 'Heating duration for one year', 3, 'Heating time = 60 × 60 × 7 × 7 × 33 = 5,821,200 seconds per year (1,344 hours).'),
           row('energy', 'k/Joules calculation for one year', 3, 'Energy = 5,821,200 × 413.712 ÷ 1000 = 2,408,300.29 kJ per year.'),
           row('pellets', 'Kgs of wood pellets for one year', 3, 'Wood pellets = 2,408,300.29 ÷ 17,350 = 138.810 kg per year.'),
           row('cost', 'Annual cost of heat loss', 3, 'Cost = 138.810 × €0.55 = €76.34 per year. The single-formula method (U × area × ΔT × seconds × cost ÷ (calorific value × 1000)) gives the same €76.34.')],
          ['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation',
          'Heat-loss and running-cost calculation (6.3) from the U-value (6.1).', B5, S5)
C5 = add('5', 'c', '(c)', 'It has been decided that the wall at 5(a) above should meet the Passive House standard, by further increasing the thickness of the external insulation. Calculate the thickness of additional external insulation required to achieve a U-value of 0.11 W/m2 ºC.',
         [row('required-resistance', 'Resistance for U-value for 0.11 W/m2 °C (using R=1/U)', 3, 'Required resistance = 1 ÷ 0.11 = 9.091 m²K/W (the scheme first finds R = 1 ÷ 0.221 = 4.525 for the wall at 5(a)).'),
          row('difference', 'Difference in resistances (required resistance)', 3, 'Additional resistance = 9.091 − 4.525 = 4.566 m²K/W.'),
          row('formula', 'Application of formula R = T/k', 3, 'R = T ÷ k for the external insulation: 4.566 = T ÷ 0.030.'),
          row('thickness', 'Required thickness of insulation', 3, 'T = 4.566 × 0.030 = 0.137 m, so 137 mm of additional insulation. Alternative calculation methods are acceptable.')],
         ['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation'], 'q5-thickness',
         'Thermal resistance calculation (6.1) to size additional insulation (6.2).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(A5, B5b, C5))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p42 (printed 6): (a) three design features × (notes 5 + sketches 5) = 30; (b) indoor air quality, natural light, materials and finishes, each 3 for point + 3 for discussion = 18; (c) two benefits (printed "Advantage 1/2") × (3 + 3) = 12. Complete 60.'
S6 = 'Part (b) requires all three printed items, each separately priced, so they are split per item, not offered as choices. Features and benefits are open responses.'
A6 = add('6', 'a', '(a)', 'With reference to the design shown, discuss using notes and freehand sketches, three features of the design that contribute to the house having a low environmental impact.',
         [row(f'feature-{i}', f'Design Feature {i}', 10, note) for i, note in [
             (1, 'Notes 5 and sketches 5. Such as: the largest glazed area facing south with high-performance glazing (U-value at least 0.8 W/m²K) so solar gain reduces the need for artificial heating.'),
             (2, 'Notes 5 and sketches 5. Such as: timber frame with a lower embodied energy than concrete and insulated studs that retain heat; locally sourced, low-maintenance larch cladding with low product miles.'),
             (3, 'Notes 5 and sketches 5. Such as: a renewable heat source instead of fossil fuels; a narrow plan and open-plan living that let daylight deep into the house; deciduous trees to the south against summer overheating; a patio as outdoor living space. Three distinct features are needed.')]],
         ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-low-impact',
         'Low environmental impact of the built environment (1.2) through solar gain (6.4) and an insulated envelope (6.2).', B6, S6)
ITEMS6 = [
    ('indoor-air-quality', 'indoor air quality', 'Indoor Air Quality (3 for point, 3 for discussion)',
     'Point 3 and discussion 3. Such as: an airtight house needs ventilation — an MVHR system supplies fresh air to dry rooms and recovers heat from moist air in wet rooms, with filters against allergens; humidity kept at 30–50% to prevent mould; sensors and regular maintenance; openable windows.',
     ['cons-6-5', 'cons-6-6'], ['condensation-air-tightness'], 'Ventilation and human comfort (6.5) and condensation and mould (6.6).'),
    ('natural-light', 'natural light', 'Natural Light (3 for point, 3 for discussion)',
     'Point 3 and discussion 3. Such as: daylight lifts mood and energy, regulates circadian rhythms and helps vitamin D synthesis; large glazing connects occupants with nature; sunlight gives warmth and cuts artificial heating and lighting bills.',
     ['cons-7-4'], ['windows-light'], 'Conditions for good (natural) illumination (7.4).'),
    ('materials-and-finishes', 'materials and finishes', 'Materials and Finishes (3 for point, 3 for discussion)',
     'Point 3 and discussion 3. Such as: low- or zero-VOC paints, adhesives, sealants and flooring; solid timber instead of formaldehyde-bonded boards; natural finishes (beeswax, linseed or tung oil); wool carpet without a synthetic, chemically bonded backing; VOC-free grout.',
     ['cons-6-5', 'cons-1-2'], ['condensation-air-tightness', 'sustainability-the-environment'],
     'Indoor air quality and comfort (6.5) through healthy, sustainable material choices (1.2).'),
]
STEM6B = 'Discuss in detail, how each of the following contribute to the creation of a healthy indoor environment: {items}.'
b6 = {}
for slug, item, verbatim, content, nodes, topics, review in ITEMS6:
    b6[slug] = add('6', f'b-{slug}', f'(b) — {item}', STEM6B.format(items=item), [row('contribution', verbatim, 6, content)],
                   nodes, topics, None, review, B6, S6)
B6b = compose('6', 'b', '(b)', list(b6.values()), None, B6, S6, STEM6B.format(items='; '.join(i[1] for i in ITEMS6)),
              labels=[i[1] for i in ITEMS6])
C6 = add('6', 'c', '(c)', 'Discuss in detail two benefits of using locally sourced materials in the construction of a dwelling house.',
         [row(f'advantage-{i}', f'Advantage {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: supports the local economy, jobs and supply chains; low product miles cut carbon emissions and delivery costs.'),
             (2, 'A second, different benefit: point 3 and discussion 3. Such as: fits the character of the area; suited to the local climate and conditions; shorter lead times and fewer supply delays; local craft knowledge and quality control; encourages reclaimed and renewable materials.')]],
         ['cons-1-2'], ['sustainability-the-environment'], None, 'Sustainable sourcing in the built environment (1.2).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-low-impact', B6, S6, parts(A6, B6b, C6))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p43 (printed 7): (a) best ten details × 4 (3 for drawing, 1 for annotation) + two courses of slate above and below the stack 6 = 46, then scale 4 + drafting 4 banded excellent 8/good 6/fair 4 = 54; (b) design detail 6. Complete 60. The printed (46 marks) heading excludes the scale/drafting row, which assesses the section drawn in (a), so it stays with (a).'
S7 = 'One required section and one required rainwater detail; the detail list is a marking menu, not a printed choice.'
A7 = add('7', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the centre of the chimney stack and roof structure. The section should be parallel to a common rafter, and show the typical construction details through the chimney stack, flue liner, chimney capping, and portion of the roof structure. Show two courses of slate above and below the chimney stack.',
         [row('construction', 'Vertical section through the centre of the chimney stack and roof structure', 40, 'Best ten details, 4 each (3 for drawing, 1 for annotation). Marking menu: external render; chimney blockwork; flue liners; lime sand fill/vermiculite; concrete chimney capping; DPC beneath chimney capping; lead cover flashing × 2; under flashing (apron); flashing to rear gutter; horizontal tray; rafter; windtight OSB layer; fillet piece; breather membrane/felt; battens/counter battens; chimney trimmer.'),
          row('slate-courses', 'Two courses of slate above and below the chimney stack', 6, 'Two courses of slate shown above and below the chimney stack.'),
          row('presentation', 'Scale - 4 marks Drafting - 4 marks', 8, 'Scale 4 and drafting 4, assessed together: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-5-7', 'cons-3-10', 'cons-3-9'], ['question-1-drawing-questions', 'fireplaces-fire-prevention', 'roofs'], 'q7-section',
         'Scaled drawing (1.5) of a chimney stack and flue (5.7) at its abutment with a slated pitched roof (3.10, 3.9).', B7, S7)
B7b = add('7', 'b', '(b)', 'On your drawing, show the typical design detailing to prevent the penetration of rainwater between the chimney stack and the adjoining roof.',
          [row('detail', 'Design detail', 6, 'Show and identify the weathering at the stack. Such as: at the back, a lead back gutter welted over a tilting fillet and under the breather membrane, with lead cover flashing overhanging it; at the front, a lead apron flashing dressed over the slates and covered by the lead DPC tray (150 mm above the lowest point where the stack exits the roof).')],
          ['cons-3-10', 'cons-5-7'], ['roofs', 'fireplaces-fire-prevention'], 'q7-flashing',
          'Weathering a roof abutment (3.10) at a chimney stack (5.7).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(A7, B7b))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p44 (printed 8): (a) two benefits × (3 for point + 3 for discussion) = 12; (b) three selected locations, each notes 8 + sketches 8 = 16; (b) 48. Complete 60.'
S8 = 'Part (b) selects any three of the FOUR circled locations: C(4,3) = 4 routes, plus each location as a separate 16-mark task. Locations are named by the scheme headings. Complete question: 4 routes.'
A8 = add('8', 'a', '(a)', 'Discuss in detail two benefits of preventing air leakage from a dwelling house.',
         [row(f'benefit-{i}', f'Benefit {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: lower energy bills because less heat escapes through gaps in the building fabric; lower carbon emissions from heating.'),
             (2, 'A second, different benefit: point 3 and discussion 3. Such as: mechanical ventilation works efficiently with better indoor air quality; no draughts; less moisture entering the fabric (preventing rot); less noise; the insulation performs better.')]],
         ['cons-6-5', 'cons-6-2'], ['condensation-air-tightness', 'heat-loss-insulation'], None,
         'Air leakage and ventilation (6.5) and heat loss through the fabric (6.2).', B8, S8)
LOCATIONS = [
    ('door-head', 'Head of external door', 'head of external door', ['cons-6-5', 'cons-6-6', 'cons-3-7'], ['condensation-air-tightness', 'doors'],
     'Such as: seal the thermally broken door frame to the reveal of the inner block wall with plasterable airtightness tape, then plaster over the tape; or airtightness paint on the reveal before plastering, or slabbing and skimming.',
     'Airtight (6.5) and vapour-control (6.6) sealing at an external door head (3.7).'),
    ('first-floor', 'First floor junction with external wall', 'first floor junction with external wall', ['cons-6-5', 'cons-6-6', 'cons-4-3'], ['condensation-air-tightness', 'floors'],
     'Such as: make the wall airtight where the joists bear — an airtightness membrane sealed with airtight silicone or plasterable tape, or sand cement render or airtightness paint; tape each joist where it breaks the airtightness barrier; seal the floor/wall and roof/wall junctions with tape or paint.',
     'Airtightness (6.5, 6.6) where the timber upper floor (4.3) meets the external wall.'),
    ('wallplate', 'Wallplate level', 'wallplate level', ['cons-6-5', 'cons-6-6', 'cons-3-10'], ['condensation-air-tightness', 'roofs'],
     'Such as: an airtightness membrane under the ceiling joists, wrapped onto the wallplate and down onto the first block below it, fixed to the wall with plasterable airtightness tape or a bead of airtight silicone, then scrim or mesh and sand cement plaster.',
     'Airtightness (6.5, 6.6) at the eaves/wallplate (3.10).'),
    ('mvhr-duct', 'MVHR duct protruding through the ceiling', 'MVHR duct protruding through the ceiling', ['cons-6-5', 'cons-6-6'], ['condensation-air-tightness'],
     'Such as: an airtightness membrane under the joists, sealed to the duct with a self-adhesive grommet fixed to the membrane, or by carefully taping the duct to the membrane with airtightness tape.',
     'Sealing a ventilation (6.5) duct through the airtight vapour-control layer (6.6).'),
]
STEM8B = 'The drawing shows an outline section of a two-storey house having a 450 mm external concrete block wall with a 250 mm full-fill insulated cavity. The house has a truss roof and a first floor of timber construction. The external door has a thermally broken frame. A Mechanical Ventilation with Heat Recovery system supplies ventilation through ceiling ducts. Using notes and freehand sketches, show best practice design detailing that will prevent air leakage at {any}the locations circled on the drawing — {items}'
a8 = {}
for slug, verbatim, label, nodes, topics, content, review in LOCATIONS:
    a8[slug] = add('8', f'b-{slug}', f'(b) — {label}', STEM8B.format(any='', items=label),
                   [row('notes', 'Notes', 8, f'Notes on best-practice detailing at the circled {label}. ' + content),
                    row('sketches', 'Sketches', 8, f'Sketches of the {label} detail showing the continuous airtight layer.')],
                   nodes, topics, f'q8-{slug}', review, B8, S8)
for combo in itertools.combinations(LOCATIONS, 3):
    names = [c[2] for c in combo]
    triple = compose('8', 'b-' + '-'.join(c[0] for c in combo), '(b) — ' + ', '.join(names), [a8[c[0]] for c in combo], f'q8-{combo[0][0]}', B8, S8,
                     STEM8B.format(any='any three of ', items='; '.join(names)), labels=names)
    # Each selected location stays its own task group: a three-location group would exceed the five-row limit.
    compose('8', 'complete-' + '-'.join(c[0] for c in combo), ' — complete: ' + ', '.join(names),
            [A8] + [a8[c[0]] for c in combo], f'q8-{combo[0][0]}', B8, S8, parts(A8, triple),
            labels=['(a)'] + [f'(b) {n}' for n in names])

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p45 (printed 9): (a) six items × 5 (4 for drawing, 1 for annotation) + cable size (1) and colour (3) 4 = 34; (b) two safety features × (notes 4 + sketches 4) = 16; (c) two approaches × (2 for point + 3 for discussion) = 10. Complete 60.'
S9 = 'One required wiring layout; safety features and approaches are open responses. No printed choice.'
A9 = add('9', 'a', '(a)', 'Using notes and freehand sketches, show the design of a typical wiring layout for two electrical light points which are controlled by a single switch. Show the lighting circuit from the distribution board to the switch and to the light points. Indicate the typical sizing and colour coding of the cables.',
         [row('distribution-board', 'Distribution board', 5, 'The distribution board drawn (4) and annotated (1), feeding the lighting circuit.'),
          row('single-switch', 'Single switch', 5, 'The single switch drawn (4) and annotated (1); a 1.5 mm² twin and earth LSF (low-smoke and fume) cable runs from the distribution board to the switch.'),
          row('light-points', 'Two electrical light points', 5, 'Both light points drawn (4) and annotated (1); the cable runs from the switch to the first light, where it is looped on to the second.'),
          row('cabling', 'Live cabling, neutral cabling, earth cabling', 15, 'Live, neutral and earth cabling, 5 each (4 for drawing, 1 for annotation), from the distribution board to the switch and both light points.'),
          row('cable-size-colour', 'Cable size (1) and colour (3)', 4, 'Cable size 1: 1.5 mm² twin and earth LSF cable. Colour coding 3: live brown, neutral blue, earth green and yellow.')],
         ['cons-5-8'], ['services-water-gas-electricity'], 'q9-wiring', 'Domestic lighting circuit and its cables (5.8).', B9, S9)
B9b = add('9', 'b', '(b)', 'Using notes and freehand sketches, describe two safety features that are typically incorporated into the design of lighting circuits.',
          [row('feature-1', 'Safety Feature 1', 8, 'Notes 4 and sketches 4. Such as: an earth to both light points and the switch; correctly sized 1.5 mm² cable for the load; low-smoke and fume (LSF) cable for safety in a fire.'),
           row('feature-2', 'Safety Feature 2', 8, 'A second, different feature: notes 4 and sketches 4. Such as: a 6 A RCBO protecting the circuit so it can be isolated; the switch breaking the phase (live) conductor so a bulb can be changed safely; a labelled distribution board for quick isolation.')],
          ['cons-5-8'], ['services-water-gas-electricity'], 'q9-safety', 'Circuit protection and electrical safety (5.8).', B9, S9)
C9 = add('9', 'c', '(c)', 'Discuss two approaches that homeowners could take to reduce the consumption of electricity in the home.',
         [row(f'approach-{i}', f'Approach {i} (2 for point, 3 for discussion)', 5, note) for i, note in [
             (1, 'Point 2 and discussion 3. Such as: low-wattage LED bulbs; sensor, motion or timer-switched lights; smart bulbs and smart metering.'),
             (2, 'A second, different approach: point 2 and discussion 3. Such as: A-rated (or better) appliances; avoiding standby (vampire) loads, with isolator switches on under-counter sockets; separate lighting circuits in open-plan rooms; light-coloured surfaces and natural light; a lower thermostat where electricity heats the home.')]],
         ['cons-5-8'], ['services-water-gas-electricity'], None, 'Domestic electricity use and its control (5.8).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-wiring', B9, S9, parts(A9, B9b, C9))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p46 (printed 10): (a) any two of three printed items, each notes 5 + sketches 5 = 10; (a) 20. (b) sketch 8, orientation 4, sun path 4, two benefits × (3 for point + 3 for discussion) = 28; (c) two methods × (notes 3 + sketches 3) = 12. Complete 60.'
S10 = 'Part (a) selects any two of three printed items: C(3,2) = 3 pairs plus each single item. The OR alternative is a separate Question 10 route. Complete question: 3 routes.'
ITEMS10 = [
    ('building-form', 'building form',
     'Such as: a compact, simple rectangular form with the smallest surface area (A/V ratio 0.7 or less) to cut heat loss, materials and cost; a narrow plan, one room deep, to maximise solar gain; clean lines in walls and roof that make airtightness easy.',
     ['cons-6-4', 'cons-6-2'], ['passive-design'], 'Passive solar design (6.4) and a compact, low-loss envelope (6.2).'),
    ('foundation-design', 'foundation design',
     'Such as: insulated ring-beam or passive raft foundations wrapped in insulation to eliminate thermal bridging; thermal blocks in the inner-leaf rising wall; 50–100 mm edge insulation at the floor/wall junction; thermally broken wall ties; a U-value of 0.10–0.15 W/m²K.',
     ['cons-6-2', 'cons-2-4'], ['passive-design', 'foundations'], 'Thermal bridging and insulation (6.2) in the choice of foundation (2.4).'),
    ('space-heating-energy-demand', 'space heating energy demand',
     'Such as: passive house space-heating demand of no more than 15 kWh/m² per year; quality workmanship in airtightness and insulation; eliminating thermal bridges; solar gain through well-designed fenestration; solar shading, thermal mass and controlled ventilation to keep about 20 °C all year.',
     ['cons-6-3', 'cons-6-2', 'cons-6-4'], ['passive-design', 'heat-loss-insulation'], 'Heating demand and heat loss (6.3) minimised by insulation (6.2) and solar gain (6.4).'),
]
STEM10A = 'Using notes and freehand sketches, discuss the importance of {any}the following in Passive House design: {items}.'
a10 = {}
for slug, item, content, nodes, topics, review in ITEMS10:
    a10[slug] = add('10', f'a-{slug}', f'(a) — {item}', STEM10A.format(any='', items=item),
                    [row('notes', 'Notes', 5, f'Notes on the importance of {item} in Passive House design. ' + content),
                     row('sketches', 'Sketches', 5, f'Sketches illustrating {item}.')],
                    nodes, topics, f'q10-{slug}', review, B10, S10)
B10b = add('10', 'b', '(b)', 'Using notes and freehand sketches, suggest a preferred orientation for the house shown. Show the sun path on your sketch. Discuss two benefits to the homeowner of your preferred orientation.',
           [row('sketch', 'Sketch', 8, 'Freehand sketch of the house showing the preferred orientation and the sun path.'),
            row('orientation', 'Orientation', 4, 'Such as: the long axis with the largest amount of glazing facing south to maximise solar gain, with minimal glazing on the north.'),
            row('sunpath', 'Sunpath', 4, 'The sun path shown on the sketch relative to north and the house.'),
            row('benefit-1', 'Benefit 1 (3 for point, 3 for discussion)', 6, 'Point 3 and discussion 3. Such as: lower energy bills, as solar gains reduce the need for artificial lighting and heating.'),
            row('benefit-2', 'Benefit 2 (3 for point, 3 for discussion)', 6, 'A second, different benefit: point 3 and discussion 3. Such as: lower carbon dioxide emissions from less artificial heating; a bright, airy home that enhances wellbeing.')],
           ['cons-6-4'], ['passive-design'], 'q10-orientation', 'Orientation for solar heat gain (6.4).', B10, S10)
C10 = add('10', 'c', '(c)', 'Solar overheating may occur during the summer months in the house shown. Using notes and freehand sketches, suggest two ways to reduce the possibility of solar overheating while respecting the character of this house design.',
          [row('method-1', 'Method 1 to reduce solar overheating', 6, 'Notes 3 and sketches 3. Such as: dynamic (electrochromic) glass that tints in response to light, heat or an electrical signal; or mature deciduous trees that block the summer sun and let winter sun through.'),
           row('method-2', 'Method 2 to reduce solar overheating', 6, 'A second, different method: notes 3 and sketches 3. Such as: a brise soleil on the south side; internal or external shutters closed against the midday summer sun; high thermal mass (polished concrete floor, exposed stone walls) to even out temperatures.')],
          ['cons-6-4'], ['passive-design'], 'q10-overheating', 'Controlling solar heat gain (6.4).', B10, S10)
for (s1, i1, *_), (s2, i2, *_) in itertools.combinations(ITEMS10, 2):
    pair = compose('10', f'a-{s1}-and-{s2}', f'(a) — {i1} and {i2}', [a10[s1], a10[s2]], f'q10-{s1}', B10, S10,
                   STEM10A.format(any='any two of ', items=f'{i1}; {i2}'), labels=[i1, i2])
    compose('10', f'complete-{s1}-and-{s2}', f' — complete: {i1} and {i2}', [pair, B10b, C10], f'q10-{s1}', B10, S10,
            parts(pair, B10b, C10), labels=[f'(a) {i1} and {i2}', '(b)', '(c)'])

BALT = 'Scheme p47 (printed 11): (a) three discussion points × (5 for point + 5 for discussion) = 30; (b) three guidelines × (5 + 5) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the Passive House question. Its parts are open responses.'
AA = add('10', 'a', '(a)', 'Discuss the above statement in detail.',
         [row(f'point-{i}', f'Discussion Point {i} (5 for point, 5 for discussion)', 10, note) for i, note in [
             (1, 'Point 5 and discussion 5. Such as: demolition creates significant waste and carbon dioxide emissions, while reuse conserves timber, stone and brick and avoids new raw-material extraction — the greenest building is the one already built.'),
             (2, 'Point 5 and discussion 5. Such as: historic buildings used local materials and local knowledge of the climate and prevailing weather, so reuse supports local economies, traditional crafts and skilled jobs.'),
             (3, 'Point 5 and discussion 5. Such as: reuse preserves local character, vernacular streetscapes and heritage, draws heritage tourism, limits urban sprawl onto green land and can provide homes for those in need. Three distinct, well-argued points are needed.')]],
         ['cons-1-1', 'cons-1-2'], ['conservation-restoration'], None,
         'Historic buildings (1.1) and the sustainable built environment (1.2).', BALT, SALT, alt=True)
AB = add('10', 'b', '(b)', 'Propose three best practice guidelines that would promote the reuse of historic buildings.',
         [row(f'guideline-{i}', f'Guideline {i} (5 for point, 5 for discussion)', 10, note) for i, note in [
             (1, 'Point 5 and discussion 5. Such as: financial supports and conservation grants for refurbishment; low-interest mortgages for historic buildings.'),
             (2, 'Point 5 and discussion 5. Such as: free training in conservation methods for tradespeople, designers and craftspeople; conservation architects on the design team, possibly subsidised.'),
             (3, 'Point 5 and discussion 5. Such as: faster planning decisions on adaptations; councils buying and adapting historic buildings for housing; penalties for derelict, unoccupied buildings; promoting successful examples; compatible materials such as breathable lime mortar. Three distinct guidelines are needed.')]],
         ['cons-1-1', 'cons-1-2'], ['conservation-restoration'], None,
         'Conserving and reusing historic buildings (1.1) within the built environment (1.2).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, parts(AA, AB), alt=True)

# ---------------------------------------------------------------- ledgers
ledger_rows = [
    (1, 'Answer any', 'Whole-exam selection: any five of the ten questions; all question banks retained, no full-exam Cartesian cards.'),
    (2, 'any two', 'Q2(a) closed choose-two of three printed items — 3 pairs and 3 single-item tasks.'),
    (6, 'any three', 'Q8(b) closed choose-three of the four circled locations — 4 triples and 4 single-location tasks.'),
    (7, 'any two', 'Q10(a) closed choose-two of three printed items — 3 pairs and 3 single-item tasks.'),
    (7, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.'),
]
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
                            '2a': dict(choose=2, options=[i[0] for i in ITEMS2], routes=[list(c) for c in itertools.combinations([i[0] for i in ITEMS2], 2)]),
                            '8b': dict(choose=3, options=[loc[0] for loc in LOCATIONS], routes=[list(c) for c in itertools.combinations([loc[0] for loc in LOCATIONS], 3)]),
                            '10a': dict(choose=2, options=[i[0] for i in ITEMS10], routes=[list(c) for c in itertools.combinations([i[0] for i in ITEMS10], 2)])})
whole = {}
for t in tasks:
    c = t['card']
    if '-complete' in c['id']:
        whole.setdefault('10-alt' if t['alternative'] else t['questionNumber'], []).append(dict(id=c['id'], parts=[g['label'] for g in c['taskGroups']], marks=c['totalMarks']))

REASONS = {
    'q1-a': 'Adds the scale and drafting allowance (8, banded 8/6/4) printed in the Question 1 table: 48 → 56. Rows keep the printed menus and best-N counts.',
    'q1-b': 'Reshaped to the reviewed criterion row; tariff unchanged (4).',
    'q2-a-safety-training': 'Reshaped to the reviewed criterion row; tariff unchanged (6).',
    'q2-a-health-and-safety-officer': 'Reshaped to the reviewed criterion row; tariff unchanged (6).',
    'q2-a-risk-assessment-audit': 'Reshaped to the reviewed criterion row; tariff unchanged (6).',
    'q2-c': 'Now the whole of part (c), built from its three separately marked activities (Guideline 1 and 2, 3 for note + 3 for sketch, each); tariff unchanged (36).',
    'q3-b': 'Split into the three printed reasons (6 each); total unchanged (18).',
    'q3-c': 'Split into the printed notes 10 and sketch 10; total unchanged (20).',
    'q4-a': 'Split into three functional requirements, each notes 3 + sketches 3; total unchanged (18).',
    'q5-c': 'Split into the four printed calculation steps (3 each) with the scheme’s worked answer; total unchanged (12).',
    'q6-b-indoor-air-quality': 'Reshaped to the printed 3 point + 3 discussion row; tariff unchanged (6).',
    'q6-b-natural-light': 'Reshaped to the printed 3 point + 3 discussion row; tariff unchanged (6); filed under illumination (7.4).',
    'q6-b-materials-and-finishes': 'Reshaped to the printed 3 point + 3 discussion row; tariff unchanged (6).',
    'q6-c': 'Split into the two printed benefits (3 point + 3 discussion); total unchanged (12); filed under the built environment (1.2), not heat-loss calculations.',
    'q7-b': 'Reshaped to the printed design-detail row; tariff unchanged (6).',
    'q8-a': 'Split into the two printed benefits (3 point + 3 discussion); total unchanged (12).',
    'q9-a': 'Adds the cable size (1) and colour (3) row printed in the table: 30 → 34; the six drawn items keep 5 each.',
    'q9-c': 'Split into the two printed approaches (2 point + 3 discussion); total unchanged (10).',
    'q10-a-building-form': 'Split into the printed notes 5 + sketches 5; total unchanged (10); filed under passive design.',
    'q10-a-foundation-design': 'Split into the printed notes 5 + sketches 5; total unchanged (10); filed under passive design and foundations.',
    'q10-b': 'Replaces an unprinted "best 2 of 4 × 14" tariff with the printed rows: sketch 8, orientation 4, sun path 4, two benefits 6 + 6 = 28.',
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

out = dict(schemaVersion=1, subjectId='construction-studies', year=2025, level='higher', lang='ev', sitting='main', paperKey='single',
           fileid='LC029ALP000EV.pdf', component='theory', status='Q1–Q10 and alternative Q10 source-reviewed draft; integration pending.',
           sourceHashes=HASHES, tasks=tasks, bindings=bindings, questionFigures=question_figures,
           addedIds=[t['card']['id'] for t in tasks if not t['correction']], corrections=corrections,
           selectionLedger=selection_ledger, questionRouteLedgers={q: dict(wholeRoutes=w) for q, w in whole.items()}, taxonomyGaps=[],
           questionsReviewed=[str(n) for n in range(1, 11)], unreviewedQuestions=[], alternativeQuestions=['10'])
(HERE / 'higher-2025-draft.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(tasks=len(tasks), added=len(out['addedIds']), corrected=len(corrections), figures=len(question_figures),
                      perQuestion={q: sum(1 for t in tasks if t['questionNumber'] == q and not t['alternative']) for q in QUESTIONS},
                      alternative=sum(1 for t in tasks if t['alternative']), wholeRoutes={q: len(w) for q, w in whole.items()})))
