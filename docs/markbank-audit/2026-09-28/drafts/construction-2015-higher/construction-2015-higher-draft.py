"""Redraft the 2015 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

The earlier 2015 Higher review (102 branch-only tasks, never on main) carried authored paraphrase stems
and expanded every printed choice into per-item and per-combination route cards. This redraft:

- lifts every stem and question text from the SEC paper (a narrowed task only deletes printed words;
  a task named by reference to a printed list carries the scheme's own heading after ' — ');
- publishes each printed choose-N-of-M as ONE card printing all M items with one anyN group over the
  scheme headings (choice is not a route): Q4(a), Q4(b), Q6(b), Q9(a) and Q10(a); Q3(b) "select one
  of the above options" is one task, because the scheme marks either option with the same rows;
- keeps the reviewed marking rows of every unchanged part, restructuring only Q3 (to the printed
  8 x 3 and 5 x 6 rows), Q5(a) (to its ten printed 3-mark criteria) and the Q6(a) row headings.

Cards kept by ID are corrected in place, each correction recording the SHA-256 of the card it
replaces; every other earlier ID is withdrawn (recorded by the consolidation step). Figures are the
earlier review's pixel-exact crops, reused unchanged.
"""
import copy
import hashlib
import json
import sys
import re
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
R = HERE.parents[4]
P = 'paper-trail-corpus/exampapers/2015/LC029ALP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2015/LC029ALP000EV.pdf'
HASHES = {P: '08976c01caaf916102e5f9f0aa18a512a5bf6aa2cad2ce5320208a63970fdc13',
          S: '9558f06c3c50cb7c858d0b4fb299b437277c0efcd182e0811c6aff0bb7dab3ef'}
ATTRIBUTION = 'SEC Leaving Certificate Construction Studies 2015 Higher Level — © State Examinations Commission.'
FP = 'construction-studies-2015-HL-'
PREFIX = 'cons-2015-hl-'
CROSS = 'construction-studies-higher-'

for f, h in HASHES.items():
    assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f

OLD_REVIEW = json.loads((HERE / 'prior-2015-higher-reviewed.json').read_text())
OLD = {t['card']['id']: t for t in OLD_REVIEW['tasks']}
OLD_BINDINGS = {b['cardId']: b for b in OLD_REVIEW['bindings']}
OLD_FIGURES = {f['key']: f for f in OLD_REVIEW['questionFigures']}
PRIOR = {c['id']: c for c in json.loads((HERE / 'prior-2015-higher-cards.json').read_text())}
assert len(OLD) == len(PRIOR) == 102 and all(PRIOR[i] == t['card'] for i, t in OLD.items())


def card_hash(c):
    return hashlib.sha256(json.dumps(c, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def page_hash(f, page):
    with fitz.open(R / f) as pdf:
        return hashlib.sha256(' '.join(pdf[page - 1].get_text().split()).encode()).hexdigest()


def old_rows(key):
    return copy.deepcopy(OLD[PREFIX + key]['card']['rows'])


def row(rid, verbatim, marks, note, steps=None):
    steps = steps or list(range(marks + 1))
    assert steps[0] == 0 and steps[-1] == marks
    return dict(id=rid, kind='criterion', verbatim=verbatim, marks=marks, contextNote=note, permittedMarks=steps)


def any_n(rid, verbatim, n, each, note, options):
    return dict(id=rid, kind='anyN', verbatim=verbatim, marks=n * each, contextNote=note,
                group=dict(claimMax=n, perOption=each, options=options))


# Figures: the earlier review's crops, reused byte-for-byte (single rects or 2x panel composites).
FIGURE_KEYS = ['q1-original', 'q1-scheme', 'q1-access-scheme', 'q2-original', 'q3-original', 'q3-scheme',
               'q4-original', 'q4-roof-windows', 'q5-original', 'q5-window-head', 'q6-original', 'q6-compact', 'q6-scheme',
               'q7-original', 'q7-roof-section', 'q8-original', 'q8-system', 'q8-collector', 'q8-locations', 'q8-scheme',
               'q9-original', 'q9-scheme', 'q10-original', 'q10-alternative', 'q10-scheme']
question_figures = [copy.deepcopy(OLD_FIGURES[FP + k]) for k in FIGURE_KEYS]
# A printed choice is one card, so its solution figure must carry every item's scheme drawings: Q4(a) had none
# attached, and the complete Q4 shows the whole scheme for the question.
sys.path.insert(0, str(R / 'scripts/markbank/authoring'))
import construction_figures  # noqa: E402
NEW_FIGURES = {'q4-discussion': construction_figures.composite([(S, 11, [51, 49, 563, 761]), (S, 12, [51, 50, 559, 278])]),
               'q4-scheme': construction_figures.composite([(S, 11, [51, 49, 563, 761]), (S, 12, [51, 50, 559, 770]),
                                                           (S, 13, [51, 50, 570, 778]), (S, 14, [51, 50, 574, 791])])}
NEW_FIGURE_ALTS = {FP + 'q4-discussion': 'SEC marking-scheme notes and sketches for all three Question 4(a) items: respect for local character, reuse of materials and breathable structure.',
                   FP + 'q4-scheme': 'SEC marking-scheme notes and sketches for the whole of Question 4: the three eco-refurbishment principles and the upgrading of the roof, sliding sash windows and suspended timber floor.'}
question_figures += [construction_figures.entry(FP + k, spec, HERE / f'{FP}{k}.png') for k, spec in NEW_FIGURES.items()]

QUESTIONS = {
    '1': dict(page=2, title='Accessible high-performance entrance', concept='accessible-entrance',
              stem='The main entrance to a dwelling house is designed to facilitate ease of access for everyone. The door shown is a high performance insulated wooden door with vertical sheeting on both sides. The door frame is 150 mm × 70 mm in cross-section and is fixed in the external wall. The wall has a 100 mm concrete block outer leaf, a 200 mm timber-frame inner leaf and a 60 mm insulated service cavity. The ground floor is an insulated solid concrete floor with a 20 mm quarry tile finish.',
              note='Original door illustration and specification retained. Construction, draughting and scale marks belong to part (a); the access detail in (b) is marked separately.'),
    '2': dict(page=2, title='External-wall performance and design', concept='external-wall-performance', stem='',
              note='Original question retained. Requirements and wall types are open choices; the scheme lists typical examples. Part (c) evaluates two of the candidate’s own wall types from (b).'),
    '3': dict(page=2, title='Attached extension or detached garden room', concept='extension-garden-room',
              stem='The drawing shows the ground floor plan of a two-storey semi-detached house and a portion of the rear garden. The external walls of the house are 400 mm concrete block walls with a full-fill insulated cavity. The rear wall M-M is south facing. The owners need an additional space for use as a study and occasionally as a family space. The space is to have internal dimensions of 5.0 metres × 3.0 metres as shown. The following options are being considered: (i) building a single-storey extension onto the rear of the house at A. or (ii) building a detached, free-standing space in the garden at B.',
              note='Original plan with positions A and B retained. Part (a) requires both options; in part (b) the candidate selects one option and the same design marks apply to either. Scheme sketches are examples, not required designs.'),
    '4': dict(page=3, title='Eco-refurbishment of a vernacular cottage', concept='vernacular-refurbishment', stem='',
              note='Original row-of-cottages sketch retained. Parts (a) and (b) each choose any two of three printed items, and each item keeps its own marks.'),
    '5': dict(page=3, title='Wall U-value, annual heat loss and window-head detail', concept='wall-heat-loss', stem='',
              note='All printed data are retained in the original question. Part (b) uses the U-value from (a); the scheme’s worked answers are U = 0.1183 W/m²°C and annual costs of €44.60 (new house) and €79.14 (existing house).'),
    '6': dict(page=4, title='Low environmental impact house', concept='low-impact-design',
              stem='The elevation and ground floor plan of a house are shown. The house has three bedrooms and a bathroom upstairs. The external walls are of timber frame construction with a rendered concrete block outer leaf. The house is designed to maximise solar energy, as shown, and to have low environmental impact.',
              note='Original elevation and plan retained. Part (b) chooses any two of three printed items, each keeping its own 10 marks. Features in (a) are open; the scheme lists typical examples.'),
    '7': dict(page=4, title='Insulated cut-roof section and ventilation', concept='attic-roof-section',
              stem='The roof of a new house, as shown, is a traditional cut roof and has a pitch of 45 degrees. The house has an internal width of 6.0 metres and the roof is highly insulated. Insulated plasterboard is also fixed to the underside of the rafters and is finished with a plaster skim coat. The external wall supporting the floor joists is a 400 mm concrete block wall with a full-fill insulated cavity. The 225 mm × 40 mm floor joists are supported centrally on a 100 mm internal load-bearing concrete block wall. The attic floor is finished with 25 mm tongue-and-groove floor boards.',
              note='Original roof sketch and dimensions retained. Construction, dimension and scale/draughting marks belong to part (a); the two ventilation details in (b) are marked separately.'),
    '8': dict(page=4, title='Stove, solar hot water and independently controlled heating zones', concept='zoned-heating-and-hot-water',
              stem='A wood-burning stove combined with a solar collector is to provide central heating and hot water for a three bedroom, two-storey dwelling house.',
              note='Original stove and collector sketch retained. Part (c) requires both the chimney and the hot press, each marked separately. The scheme diagrams are exam models, not installation specifications.'),
    '9': dict(page=5, title='Four circled thermal-bridge junctions', concept='thermal-bridge-junctions',
              stem='It is proposed to design the external envelope of a dwelling house to be thermal bridge free. The drawing shows an outline section through a two-storey house having a 450 mm external concrete block wall with a 250 mm full-fill insulated cavity. The roof is a traditional cut roof, the first floor has tongue-and-groove flooring on timber joists and the ground floor is an insulated solid concrete floor.',
              note='Original section with four circled locations retained. Part (a) chooses any three, each location keeping its own 16 marks; locations are named with the marking scheme’s headings.'),
    '10': dict(page=5, title='Passive House design', concept='passive-house-and-daylight', stem='',
               note='Original Passive House sketch retained. Part (a) chooses any two of three printed items, each keeping its own 16 marks. The 2015 scheme’s energy figures are historical, not current regulations.'),
}
ALT = dict(page=5, title='Natural light and glazing', concept='passive-house-and-daylight-alt',
           stem='Light is what architecture is all about. It is as fundamental for the soul as air, fire, earth and water. Light has been one of the key elements of architecture since the Modern movement began (and glass technology improved) at the turn of the 20th century. Yet, light has traditionally been lacking in Irish homes. Many old cottages only have windows on the south side and none on the north. Now glass has improved and windows can be made with incredibly low U-values (meaning it doesn’t let the cold through), so you can now have large glazed areas without heat loss. We need light and instinctively search for it. People move to the part of the room where there is natural light and children instinctively play in pools of light. Adapted from LOVE YOUR HOME Secrets to a Successful Space by Dermot Bannon (2014) Published by Gill & Macmillan. ISBN: 978 07171 6448 6',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the Passive House question.')
SCHEME_PAGES = {'1': [4, 5, 6, 32], '2': [6, 7, 8, 33], '3': [9, 10, 34], '4': [11, 12, 13, 14, 35], '5': [15, 16, 17, 36],
                '6': [18, 19, 20, 37], '7': [21, 38], '8': [22, 23, 39], '9': [24, 25, 40], '10': [25, 26, 27, 28, 41],
                '10-alt': [29, 30, 42]}

tasks, bindings, cards = [], [], {}


def checks(paper_page, scheme_pages):
    return ([dict(file=P, page=p, textSha256=page_hash(P, p)) for p in (1, paper_page)]
            + [dict(file=S, page=p, textSha256=page_hash(S, p)) for p in [2, *scheme_pages]])


def add(q, key, ref, text, rows, nodes, topics, figure, review, boundary, selection, groups=None, total=None, alt=False):
    meta = ALT if alt else QUESTIONS[q]
    qkey = '10-alt' if alt else q
    cid = f'{PREFIX}q{qkey}-{key}'
    concept = PRIOR[cid]['conceptId'] if cid in PRIOR else f"{meta['concept']}-{key}"
    card = dict(id=cid, subjectId='construction-studies', year=2015, level='higher', section='B',
                topicId=nodes[0], conceptId=concept, questionRef=f'2015 HL Q{qkey}{ref}',
                stem=meta['stem'], questionText=text, tariffModel={'kind': 'fixed'},
                totalMarks=total if total is not None else sum(r['marks'] for r in rows), rows=rows,
                questionFigureKey=FP + ('q10-alternative' if alt else f'q{q}-original'), questionFigureIncludesPrompt=True)
    if figure:
        card['figureKey'] = FP + figure
    attribution = ATTRIBUTION + (' Passage adapted from Dermot Bannon (2014), Gill & Macmillan, as credited on the original paper.' if alt else '')
    card['sourceMaterial'] = dict(kind='source-illustration',
                                  label=f"ORIGINAL QUESTION 10{' — ALTERNATIVE' if alt else ''}" if q == '10' else f'ORIGINAL QUESTION {q}',
                                  title=meta['title'], pages=[1, meta['page']], attribution=attribution, presentationNote=meta['note'])
    if groups:
        card['taskGroups'] = groups
    tasks.append(dict(questionNumber=q, alternative=alt, correction=cid in PRIOR, card=card,
                      sourceChecks=checks(meta['page'], SCHEME_PAGES[qkey]), boundaryReview=boundary, selectionReview=selection,
                      requiredQuestionFigures=[card['questionFigureKey']], requiredSolutionFigures=[FP + figure] if figure else []))
    bindings.append(dict(cardId=cid, markBankTopicId=nodes[0], canonicalTopicIds=nodes, canonicalTopicReview=review,
                         questionNumber=q, atlasTopicIds=[CROSS + t for t in topics]))
    cards[cid] = card
    return card


def keep(q, key, ref, text, rows, figure, boundary, selection, alt=False):
    """A reviewed part kept under its ID: its earlier topic binding is retained unchanged."""
    b = OLD_BINDINGS[f"{PREFIX}q{'10-alt' if alt else q}-{key}"]
    return add(q, key, ref, text, rows, b['canonicalTopicIds'], [t.removeprefix(CROSS) for t in b['atlasTopicIds']], figure,
               b['canonicalTopicReview'], boundary, selection, alt=alt)


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
B1 = 'Scheme p32 (Ceist 1): (a) any 11 points × 4 (drawing 3, annotation 1) = 44, draughting 4 (excellent 4, good 3, fair 2) + scale 4 = 52; (b) ease of access, sloped threshold and upstand, 8. Complete 60.'
S1 = 'One required section and one required access detail. The scheme detail list is a marking menu, not a printed choice.'
T1A = 'To a scale of 1:10, draw a vertical section through the centre of the door. Show the typical construction details from 500 mm below finished floor, through the floor, the threshold, the external wall, the door and doorframe to a level 300 mm above the top of the door frame.'
T1B = 'On your drawing, show clearly the design detailing that ensures ease of access for all persons.'
A1 = keep('1', 'a', '(a)', T1A, old_rows('q1-a'), 'q1-scheme', B1, S1)
B1b = keep('1', 'b', '(b)', T1B, old_rows('q1-b'), 'q1-access-scheme', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-scheme', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p33 (Ceist 2): (a) three requirements × (notes 4 + sketches 4) = 24; (b) three wall types × (notes 3 + sketches 3) + materials 3 × 1 + typical dimensions 3 × 1 = 24; (c) evaluation of two walls 3 + 3, recommendation 3, justification 3 = 12. Complete 60.'
S2 = '"Any two of the wall types at 2(b)" refers to the candidate’s own three wall types: an open choice with no printed list, so (c) stays one response. Requirements and wall types are open responses.'
T2A = 'Using notes and freehand sketches, discuss three functional requirements of an external wall for a new dwelling house.'
T2B = 'Using notes and freehand sketches, show the design detailing of three different, distinct external wall types suitable for a new dwelling house. For each wall type, specify the materials to be used and include typical dimensions.'
T2C = 'Evaluate the design of any two of the wall types at 2(b) above. Recommend a preferred external wall type for a new house and justify your recommendation.'
A2 = keep('2', 'a', '(a)', T2A, old_rows('q2-a'), None, B2, S2)
B2b = keep('2', 'b', '(b)', T2B, old_rows('q2-b'), None, B2, S2)
C2 = keep('2', 'c', '(c)', T2C, old_rows('q2-c'), None, B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], None, B2, S2, parts(('a', T2A), ('b', T2B), ('c', T2C)))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p34 (Ceist 3): (a) two advantages and two disadvantages of each option, 8 × 3 = 24 (Option A 12, Option B 12); (b) external design notes 6 + sketches 6, internal layout notes 6 + sketches 6, link to rear garden 6 = 30; (c) two advantages × 3 = 6. Complete 60.'
S3 = 'Part (a) requires both printed options, each separately marked, so each is its own 12-mark task and (a) composes them. In part (b) choosing option (i) or (ii) is part of the answer and the scheme marks either with the same five rows: one task, not two routes.'
T3A = 'Discuss in detail two advantages and two disadvantages of each option listed at (i) and (ii) above.'
T3B = 'Select one of the above options and, using notes and freehand sketches, show a proposed external design and internal layout for an attractive study/family space. Show in your design how the proposed space is to link with the surrounding rear garden.'
T3C = 'Discuss two advantages of designing a space that links with the rear garden.'
NODES3, TOPICS3 = ['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment']
REVIEW3 = OLD_BINDINGS[PREFIX + 'q3-a']['canonicalTopicReview']
A3A = add('3', 'a-A', '(a) — Option A', f'{T3A} — Option A', [
    row('advantage-1', 'Advantage 1', 3, 'An advantage of the single-storey extension at A, discussed for this house (3). Such as: saves on construction and insulation costs; conserves space in the rear garden; more efficient energy use, as it minimises the area of external walling; more freedom in using and dividing the total living space.'),
    row('advantage-2', 'Advantage 2', 3, 'A second, different advantage of the extension at A (3). Such as: easy, economical connection to existing services (space heating, plumbing, ventilation, electrical distribution); a compact plan that supports regular social interaction across the generations of the family.'),
    row('disadvantage-1', 'Disadvantage 1', 3, 'A disadvantage of the extension at A (3). Such as: disturbs the well-proportioned original layout; creates a large undifferentiated space that needs careful design; can reduce the natural lighting and ventilation of the kitchen/dining room; more energy for lighting and heating a large space.'),
    row('disadvantage-2', 'Disadvantage 2', 3, 'A second, different disadvantage of the extension at A (3). Such as: fewer discrete rooms for a quieter environment; may spoil the view from the existing kitchen and dining area; continuity of insulation and weatherproofing at the roof and wall abutment; spanning the larger opening in the existing external wall may need strengthening and RSJs; misses the chance to connect the garden with the living spaces.')],
    NODES3, TOPICS3, None, REVIEW3, B3, S3)
A3B = add('3', 'a-B', '(a) — Option B', f'{T3A} — Option B', [
    row('advantage-1', 'Advantage 1', 3, 'An advantage of the detached, free-standing space at B, discussed for this house (3). Such as: keeps the existing relationship between the kitchen/dining area and the outside; minimises disruption during construction; maintains natural lighting to the existing rooms; greater privacy in a distinct room in the garden.'),
    row('advantage-2', 'Advantage 2', 3, 'A second, different advantage of the space at B (3). Such as: space for a young or older family member; more freedom of design and more natural lighting in the new building; a closer link between room and garden; isolation for activities that need quiet or are noisy; does not overshadow the existing kitchen and dining room.'),
    row('disadvantage-1', 'Disadvantage 1', 3, 'A disadvantage of the space at B (3). Such as: a larger external envelope with higher insulation costs; the inconvenience of crossing the garden to reach it; possibly higher heating costs from an extra external door and reduced airtightness.'),
    row('disadvantage-2', 'Disadvantage 2', 3, 'A second, different disadvantage of the space at B (3). Such as: garden space lost to paths; unusable spaces near the external doors; fragmentation of family living space; the cost of access for all and of connecting services (heating, plumbing and waste, electrical). The scheme prints this list under the heading 3(b)(ii); it belongs to part (a), option B.')],
    NODES3, TOPICS3, None, REVIEW3, B3, S3)
A3 = compose('3', 'a', '(a)', [A3A, A3B], None, B3, S3, T3A, labels=['Option A', 'Option B'])
B3b = add('3', 'b', '(b)', T3B, [
    row('external-notes', 'External design - Notes', 6, 'Notes on the proposed external design for the chosen option (an extension on the south-facing rear wall M-M at A, or a free-standing space at B), keeping the 5.0 m × 3.0 m internal space. Such as: a flat-roofed structure with a low elevation lets more light into the enclosed garden and keeps the sense of space; windows on the south elevation for good natural lighting; a space at B can be linked to the house by a covered walkway. Any thoughtful modern or traditional design with creativity and flair is acceptable.'),
    row('external-sketches', 'Sketches', 6, 'Freehand sketch of the proposed external design (elevation) for the chosen option.'),
    row('layout-notes', 'Internal layout - Notes', 6, 'Notes on the internal layout of the study/family space. Such as: the space divided to give some privacy and a sense of seclusion; a small office area for individual work at a desk; a larger area for communal living; a convertible couch for occasional overnight visitors.'),
    row('layout-sketches', 'Sketches', 6, 'Freehand sketch (plan) of the proposed internal layout of the 5.0 m × 3.0 m space.'),
    row('garden-link', 'How proposed space is to link with rear garden', 6, 'Such as: double, folding or sliding doors for easy access outside; floor-to-ceiling windows to capture views of the garden; a paved patio with wide-opening doors for seating and access, extending the space into the garden.')],
    ['cons-1-3', 'cons-1-2'], TOPICS3, 'q3-scheme', OLD_BINDINGS[PREFIX + 'q3-b-A']['canonicalTopicReview'], B3, S3)
C3 = add('3', 'c', '(c)', T3C, [
    row('advantage-1', 'Advantage 1', 3, 'An advantage of linking the space with the rear garden (3). Such as: an increased sense of wellbeing from closer contact with nature; awareness of the changing seasons; engaging the senses; the health benefits of natural light.'),
    row('advantage-2', 'Advantage 2', 3, 'A second, different advantage (3). Such as: educational benefits for children; more use made of the valuable space outside; a greater sense of spaciousness for little extra investment. Naming a door type describes a design feature, not an advantage.')],
    ['cons-1-2'], TOPICS3, None, OLD_BINDINGS[PREFIX + 'q3-c']['canonicalTopicReview'], B3, S3)
compose('3', 'complete', ' — complete', [A3A, A3B, B3b, C3], 'q3-scheme', B3, S3, parts(('a', T3A), ('b', T3B), ('c', T3C)),
        labels=['a — Option A', 'a — Option B', 'b', 'c'])

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p35 (Ceist 4): (a) any two of three printed items × 10 = 20; (b) two of three areas for upgrading, each notes 10 + sketches 10 = 40. Complete 60.'
S4 = 'Choice is not a route: part (a) (any two of three printed items) and part (b) (any two of the three surveyed areas) are each ONE card printing every item, with one any-two group over the scheme headings; the complete question composes the two.'
T4A = 'Discuss the importance of any two of the following in the eco-refurbishment of an old house built in the vernacular tradition: respect for local character; breathable structure; reuse of materials.'
T4B = 'A row of single-storey cottages is shown in the sketch. One of the cottages is in need of significant refurbishment. A survey of the cottage reveals: un-insulated traditional cut roof with natural slates; softwood windows, single-glazed with sliding sash; un-insulated suspended timber floor. Select any two of the areas at 4(b) above and, using notes and freehand sketches, describe the steps involved in upgrading each area selected in a manner that respects the appearance and character of the original cottages.'
ITEMS4A = ['Respect for local character', 'Breathable structure', 'Reuse of materials']
A4 = add('4', 'a', '(a)', T4A, [any_n('items', 'Discussion - eco-refurbishment - any two', 2, 10,
    'Any two of the three, 10 each, as a developed discussion; the scheme does not split the 10 into points. '
    'Respect for local character: vernacular houses evolved from their location, built simply and modestly from local materials and labour, so refurbishment keeps materials, methods and detailing simple, retains the historic character and the unity of the row of cottages, upgrades the fabric first, and takes advice from a conservation officer, architect, engineer or designer. '
    'Breathable structure: moisture moves gradually from the inside through the walls and roof and is not trapped, preventing surface and interstitial condensation; natural, hygroscopic insulation and finishes (lime, hemp, cork, wood fibreboard, sheep’s wool, lime renders and plasters) let it move; vapour barriers and vapour-resistant materials are not usually appropriate in older buildings, and layers should become more permeable from inside to outside. '
    'Reuse of materials: examine the whole house to see what can be reused; replace only the decayed portions of roof members (splice rafter ends, wall plate in the same timber); replace decayed fascia and soffit to the identical profile; lift, number and store floorboards and skirtings for reuse, replacing damaged boards with similar salvaged ones to keep the patina of age.',
    ITEMS4A)],
    ['cons-1-1', 'cons-1-2', 'cons-6-6', 'cons-6-2'], ['conservation-restoration', 'condensation-air-tightness', 'heat-loss-insulation'], 'q4-discussion',
    'The union of the three printed items: conservation of vernacular buildings (1.1) and their setting (1.2), with breathable fabric and condensation control (6.6) and insulation (6.2).', B4, S4)
ITEMS4B = ['Roof', 'Sliding sash windows', 'Suspended timber floor']
B4b = add('4', 'b', '(b)', T4B, [any_n('areas', 'Two areas for upgrading - roof, windows, floor', 2, 20,
    'Any two of the three surveyed areas, each notes 10 and sketches 10 = 20, describing the upgrading steps in a way that respects the appearance and character of the original cottages. '
    'Roof: retain as much historic fabric as possible; remove, number and store the slates and reuse them (slates from the rear placed on the front for uniformity); inspect the members and replace only decayed portions; replace impermeable sarking felt with a vapour-diffuse membrane; insulate with hygroscopic materials (sheep’s wool between the rafters, wood fibreboard above and below) with counter battens for ventilation, or, as the scheme’s other option, insulation with a ventilation path and a continuous taped vapour barrier on the warm side behind an insulated service cavity. '
    'Sliding sash windows: maintain and repair before replacing; survey, number and remove the sashes; repair damaged wood with a similar species, sand, seal and repaint; remove cracked putty and re-glaze with linseed oil putty; check the pulleys and cords; then keep the existing glass, or fit draught-proof seals and double-glazed units where the rebates are deep enough, or fit secondary glazing inside. '
    'Suspended timber floor: determine the floor’s historical significance; record and number the floorboards and skirting, remove and store them; check the sub-floor ventilation; replace decayed joists or boards; fit insulation between the joists on netting or battens, friction tight with no gaps; fit a breather membrane and replace the floorboards as labelled.',
    ITEMS4B)],
    ['cons-1-1', 'cons-3-8', 'cons-3-9', 'cons-3-5', 'cons-3-6', 'cons-4-2', 'cons-4-3', 'cons-6-2'],
    ['conservation-restoration', 'roofs', 'windows-light', 'floors', 'heat-loss-insulation'], 'q4-roof-windows',
    'The union of the three surveyed areas, all conservation work (1.1): the cut roof and its covering (3.8, 3.9), sash windows (3.5, 3.6), the suspended timber floor (4.2, 4.3) and their insulation (6.2).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b], 'q4-scheme', B4, S4, parts(('a', T4A), ('b', T4B)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p36 (Ceist 5): (a) 10 points × 3 = 30 (1 mark for the U-value formula); (b) five 2-mark steps for each house = 20; (c) notes/annotations 5 + sketches 5 = 10. Complete 60.'
S5 = 'No printed choice. Both houses are required in (b), each separately marked, so each is its own 10-mark task and (b) composes them.'
DATA5A = ('Specification of external wall: external render thickness 16 mm; concrete block outer leaf thickness 100 mm; cavity width 250 mm; '
          'concrete block inner leaf thickness 100 mm; internal plaster thickness 12 mm.\n'
          'Thermal data of external wall: resistance of external surface (R) 0.048 m² °C/W; conductivity of external render (k) 0.720 W/m °C; '
          'conductivity of concrete blocks (k) 1.440 W/m °C; conductivity of polystyrene bead (k) 0.031 W/m °C; '
          'conductivity of internal plaster (k) 0.220 W/m °C; resistance of internal surface (R) 0.122 m² °C/W.')
DATA5B = ('Data for both houses: area of external wall of each house 150 m²; average internal temperature 20 °C; average external temperature 6 °C; '
          'heating period 8 hours per day, every day for 35 weeks per annum; cost of oil 95 cent per litre; calorific value of oil 37350 kJ per litre; '
          '1000 watts: 1kJ per second.')
T5A = ('Using the following data, calculate the U-value of the external wall of a new dwelling house. The wall is of concrete block construction, '
       'with a 250 mm cavity. The cavity is a full-fill insulated cavity, with polystyrene bead insulation as shown.\n' + DATA5A)
T5B = ('Using the U-value obtained at 5(a) and the data given below, calculate the cost of heat lost annually through the external walls of each of the following: '
       'the new house - as specified at 5(a) above and an existing house that complies with current Building Regulations, having a U-value of 0.21 W/m² °C for the walls.\n' + DATA5B)
T5BN = 'Using the U-value obtained at 5(a) and the data given below, calculate the cost of heat lost annually through the external walls of the new house - as specified at 5(a) above.\n' + DATA5B
T5BE = 'Using the data given below, calculate the cost of heat lost annually through the external walls of an existing house that complies with current Building Regulations, having a U-value of 0.21 W/m² °C for the walls.\n' + DATA5B
T5C = 'Using notes and freehand sketches, show best practice design detailing to prevent the ingress of water at the window head in the wall of the new house specified at 5(a) above.'
old5 = {r['id']: r for r in old_rows('q5-a')}
# The ten printed 3-mark points as four rows (a route task holds at most five): the seven resistances share
# the scheme's own "Formulae" heading, 3 each.
A5 = keep('5', 'a', '(a)', T5A, [
    row('method', 'Tabulation / methodology', 3, old5['method']['contextNote'], [0, 3]),
    row('resistances', 'Formulae: R=T/k R=T × r', 21,
        'Seven resistances, 3 each: the five material layers by R = thickness/conductivity, with thicknesses converted from mm to m, '
        'and the two given surface resistances. External surface Rse = 0.048 (given; do not divide it by a thickness); external render '
        '0.016/0.720 = 0.02222222; outer concrete-block leaf 0.100/1.440 = 0.06944444; polystyrene bead 0.250/0.031 = 8.06451613 (the cavity '
        'is fully filled, so no separate air-cavity resistance); inner concrete-block leaf 0.100/1.440 = 0.06944444 (both leaves count); '
        'internal plaster 0.012/0.220 = 0.05454545; internal surface Rsi = 0.122 (given). All in m²·°C/W.', list(range(0, 22, 3))),
    row('total-resistance', 'Total resistance', 3, old5['total-resistance']['contextNote'], [0, 3]),
    row('u-value', 'U-value (1 mark for formula)', 3, old5['u-value']['contextNote'], [0, 1, 3])], None, B5, S5)
B5n = keep('5', 'b-new', '(b) — new house', T5BN, old_rows('q5-b-new'), None, B5, S5)
B5e = keep('5', 'b-existing', '(b) — existing house', T5BE, old_rows('q5-b-existing'), None, B5, S5)
B5b = compose('5', 'b', '(b)', [B5n, B5e], None, B5, S5, T5B, labels=['New house', 'Existing house'])
C5 = keep('5', 'c', '(c)', T5C, old_rows('q5-c'), 'q5-window-head', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5n, B5e, C5], 'q5-window-head', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)),
        labels=['a', 'b — new house', 'b — existing house', 'c'])

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p37 (Ceist 6): (a) three design features × (notes 5 + sketches 5) = 30; (b) any two of three printed items × (notes 5 + sketches 5) = 20; (c) discussion of NZEB (4 for point, 6 for discussion) = 10. Complete 60.'
S6 = 'Choice is not a route: part (b) (any two of three printed items) is ONE card with an any-two group over the scheme headings. Features in (a) and the discussion in (c) are open responses.'
T6A = 'Using notes and freehand sketches, discuss three features of the design that ensure that the house has low environmental impact.'
T6B = 'Using notes and freehand sketches, discuss the importance of any two of the following in designing a house to have low environmental impact: compact form; flexible design; low maintenance.'
T6C = 'Discuss in detail the importance of designing nearly zero energy buildings (NZEB) for the 21st century.'
rows6a = old_rows('q6-a')
for i, r in enumerate(rows6a, 1):
    r['verbatim'] = f'Design feature {i}'
A6 = keep('6', 'a', '(a)', T6A, rows6a, 'q6-compact', B6, S6)
B6b = add('6', 'b', '(b)', T6B, [any_n('features', 'Any two design features', 2, 10,
    'Any two of the three, each notes 5 and sketches 5 = 10. '
    'Compact form: a reduced external surface area minimises heat loss and the materials needed to enclose the living space; less concrete and so lower carbon emissions; a smaller heated air volume; a house one room wide is easier to heat by passive solar gain; less land used and less visual impact. '
    'Flexible design: the dwelling can respond over time to changes in lifestyle and needs without major structural change, extending its useful life; a bathroom designed for lifetime use; a home office or occasional bedroom easily made; a wall to the hallway removable to form a larger open-plan area; easier retrofitting of new technologies. '
    'Low maintenance: reduces the energy and materials used over the dwelling’s lifetime and delays its replacement; keeps the energy-saving features at peak efficiency for longer; robust construction; keeps the attractive, unobtrusive appearance for longer.',
    ['Compact form', 'Flexible design', 'Low maintenance'])],
    ['cons-1-2'], ['planning-sustainability-environment'], 'q6-scheme',
    'All three printed items concern designing a house for low environmental impact (1.2).', B6, S6)
C6 = keep('6', 'c', '(c)', T6C, old_rows('q6-c'), None, B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-scheme', B6, S6, parts(('a', T6A), ('b', T6B), ('c', T6C)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p38 (Ceist 7): (a) any 10 points × 4 (drawing 3, annotation 1) = 40, 4 typical dimensions 4, draughting 4 + scale 4 = 52; (b) two ventilation details, eaves 4 + roof/ridge 4 = 8. Complete 60.'
S7 = 'One required half-roof section. Part (b) requires both ventilation details, eaves and roof/ridge, each separately marked: two required tasks composed into (b), not a choice. The best-ten detail list is a marking menu.'
T7A = 'To a scale of 1:10, draw a vertical section through one half of the roof structure from eaves up to ridge, showing one external wall and one rafter length. Show the typical construction details from 500 mm below the floor joists up to the ridge and include three courses of slate at eaves. Include four typical dimensions of the roof structure.'
T7B = 'Include on you drawing, best practice design detailing to ensure ventilation of the roof structure.'
A7 = keep('7', 'a', '(a)', T7A, old_rows('q7-a'), 'q7-roof-section', B7, S7)
B7e = keep('7', 'b-eaves', '(b) — eaves', f'{T7B} — Eaves', old_rows('q7-b-eaves'), 'q7-roof-section', B7, S7)
B7r = keep('7', 'b-ridge', '(b) — roof/ridge', f'{T7B} — Roof/ridge', old_rows('q7-b-ridge'), 'q7-roof-section', B7, S7)
B7b = compose('7', 'b', '(b)', [B7e, B7r], 'q7-roof-section', B7, S7, T7B, labels=['Eaves', 'Roof/ridge'])
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-roof-section', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p39 (Ceist 8): (a) nine items × 4 (sketch 3, annotation 1) = 36 + sizes of pipework (any 2) 2 × 2 = 40; (b) notes 4 + sketches 4 = 8; (c) chimney (notes 3 + sketches 3) + hot press (notes 3 + sketches 3) = 12. Complete 60.'
S8 = 'One required system layout. Part (c) requires both the chimney and the hot press, each separately marked: two required tasks composed into (c), not a choice. The best-nine item list is a marking menu; pipe sizes and considerations are open.'
T8A = 'Using notes and a single-line diagram, show a typical design layout for both the heating system and the hot water system. Show two independently controlled heating zones, one on each floor, and include three radiators on each floor. Indicate the location of the control valves and give the typical sizes of the pipework.'
T8B = 'Using notes and freehand sketches show a preferred location for a solar collector that will ensure its maximum efficiency.'
T8C = 'Using notes and freehand sketches, discuss two considerations that should be taken into account at the design stage of the house when selecting a location for both the chimney and the hot press. Justify your design choices.'
T8CC = 'Using notes and freehand sketches, discuss two considerations that should be taken into account at the design stage of the house when selecting a location for the chimney. Justify your design choices.'
T8CH = 'Using notes and freehand sketches, discuss two considerations that should be taken into account at the design stage of the house when selecting a location for the hot press. Justify your design choices.'
A8 = keep('8', 'a', '(a)', T8A, old_rows('q8-a'), 'q8-system', B8, S8)
B8b = keep('8', 'b', '(b)', T8B, old_rows('q8-b'), 'q8-collector', B8, S8)
C8c = keep('8', 'c-chimney', '(c) — chimney', T8CC, old_rows('q8-c-chimney'), 'q8-locations', B8, S8)
C8h = keep('8', 'c-hotpress', '(c) — hot press', T8CH, old_rows('q8-c-hotpress'), 'q8-locations', B8, S8)
C8 = compose('8', 'c', '(c)', [C8c, C8h], 'q8-locations', B8, S8, T8C, labels=['Chimney', 'Hot press'])
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-scheme', B8, S8, parts(('a', T8A), ('b', T8B), ('c', T8C)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p40 (Ceist 9): (a) three locations × (notes 8 + sketches 8) = 48; (b) two discussion points × (2 for point + 4 for discussion) = 12. Complete 60.'
S9 = 'Choice is not a route: part (a) (any three of the FOUR circled locations) is ONE card with one any-three group over the four locations, named by the scheme headings; the window head in the scheme is not circled and is not an option. The complete question composes (a) and (b).'
T9A = 'Select any three locations from those circled on the drawing and, using notes and freehand sketches, show best practice design detailing that will prevent the formation of a thermal bridge at each location selected.'
T9B = 'Discuss the importance of designing a building envelope that is thermal bridge free.'
LOCATIONS9 = ['Junction of roof and wall at eaves', 'Junction of upper floors and external walls', 'Window cill', 'Ground floors abutting external walls']
A9 = add('9', 'a', '(a)', T9A, [any_n('locations', 'Thermal bridging details - Three locations', 3, 16,
    'Any three of the four circled locations, each notes 8 and sketches 8 = 16, showing the insulation kept continuous so that no thermal bridge forms. '
    'Junction of roof and wall at eaves: 60 mm rigid insulation board; 400 mm fibreglass insulation; a 60 mm cavity closer; an autoclaved aerated concrete (AAC) block; 250 mm full-fill cavity insulation. '
    'Junction of upper floors and external walls: joists hung on the inside leaf, on metal hangers or resin-anchored bolts, with no penetration of the leaf and cavity; the wall plastered for airtightness. '
    'Window cill: insulation at the back of the cill so it does not bridge the cavity; a high-density proprietary cavity closer; 250 mm full-fill cavity insulation; airtightness tape to the triple-glazed window frame. '
    'Ground floors abutting external walls: cavity insulation carried down at least 225 mm below the top of the finished floor; an 80 mm perimeter insulation strip between the slab and the inner leaf; 150–300 mm insulation under the slab; 100 mm AAC blocks below ground level.',
    LOCATIONS9)],
    ['cons-6-2', 'cons-3-9', 'cons-3-3', 'cons-4-3', 'cons-3-6', 'cons-4-2'], ['heat-loss-insulation', 'roofs', 'walls', 'floors', 'windows-light'], 'q9-scheme',
    'Every location is a thermal-bridge insulation detail (6.2) at a junction of the external wall (3.3) with the roof eaves (3.9), the upper floor (4.3), the window cill (3.6) or the ground floor (4.2).', B9, S9)
B9b = keep('9', 'b', '(b)', T9B, old_rows('q9-b'), 'q9-scheme', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b], 'q9-scheme', B9, S9, parts(('a', T9A), ('b', T9B)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p41 (Ceist 10): (a) any two of three printed items × (notes 8 + sketches 8) = 32; (b) notes 7 + sketches 7 = 14; (c) notes 7 + sketches 7 = 14. Complete 60.'
S10 = 'Choice is not a route: part (a) (any two of three printed items) is ONE card with an any-two group over the scheme headings. The OR alternative is a separate Question 10 route.'
T10A = 'Using notes and freehand sketches, discuss in detail the importance of any two of the following in the design of a Passive House: airtight building envelope; space heating demand; indoor air quality.'
T10B = 'Using notes and freehand sketches, discuss the importance of thermal mass in the design of a Passive House.'
T10C = 'Using notes and freehand sketches, discuss the function of carefully designed solar shading for the Passive House shown.'
A10 = add('10', 'a', '(a)', T10A, [any_n('items', 'Design of a Passive House - any 2', 2, 16,
    'Any two of the three, each notes 8 and sketches 8 = 16. '
    'Airtight building envelope: build tight and ventilate right; an unbroken air barrier on the warm side of the insulation, taped at every junction (wall/floor, wall/window, wall/door, ceiling/wall, chimney/ceiling), prevents unregulated air leakage and heat loss and lets the fresh-air intake be controlled; a service cavity keeps services from puncturing it; grommets seal pipes and cables; a blower door test checks it. '
    'Space heating demand: the energy needed to keep 20 °C indoors all year, not including hot water; a Passive House limits it to 15 kWh/m² per year or less, with a heating load of no more than 10 W/m²; the 2015 scheme also cites a primary energy demand of no more than 120 kWh/m² per year. '
    'Indoor air quality: greater airtightness needs a designed ventilation system that supplies clean, warm, filtered fresh air; mechanical ventilation with heat recovery extracts moist air from the kitchen, utility and bathrooms and passes it through a heat exchanger without mixing it with the incoming air; filters changed every three to six months; relative humidity of 30% to 60%; 0.3 to 0.6 air changes per hour.',
    ['Airtight building envelope', 'Space heating demand', 'Indoor air quality'])],
    ['cons-6-5', 'cons-6-6', 'cons-5-3', 'cons-6-2'], ['passive-design', 'condensation-air-tightness', 'hot-water-space-heating', 'wood-rot-ventilation'], 'q10-scheme',
    'The union of the three printed items: airtightness and ventilation (6.5, 6.6), space heating (5.3) and heat loss (6.2) in Passive House design.', B10, S10)
B10b = keep('10', 'b', '(b)', T10B, old_rows('q10-b'), 'q10-scheme', B10, S10)
C10 = keep('10', 'c', '(c)', T10C, old_rows('q10-c'), 'q10-scheme', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-scheme', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p42 (Ceist 10 alternative): discussion of the statement, three points × (3 for point + 5 for discussion) = 24; advances in glazing technology 6; three guidelines × (4 for point + 6 for discussion) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the Passive House question. Its discussion points and guidelines are open responses.'
TA1 = 'Discuss the above statement in detail.'
TA2 = 'Outline how advances in glazing technology have led to the increased use of glass in house design.'
TA3 = 'Recommend three best practice guidelines that would encourage better use of natural light in the design of contemporary dwelling houses.'
AD = keep('10', 'discussion', ' — discussion', TA1, old_rows('q10-alt-discussion'), None, BALT, SALT, alt=True)
AG = keep('10', 'glazing', ' — glazing advances', TA2, old_rows('q10-alt-glazing'), None, BALT, SALT, alt=True)
AU = keep('10', 'guidelines', ' — guidelines', TA3, old_rows('q10-alt-guidelines'), None, BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AD, AG, AU], None, BALT, SALT,
        'Discuss the above statement in detail and outline how advances in glazing technology have led to the increased use of glass in house design.\n\n' + TA3,
        labels=['Discussion', 'Glazing advances', 'Guidelines'], alt=True)

# ---------------------------------------------------------------- ledgers
ledger_rows = [
    (1, 'Answer Question', 'Whole-paper selection: Question 1 and four other questions; all question banks retained, no full-exam Cartesian cards.'),
    (2, 'any two', 'Q2(c) any two of the candidate’s own wall types from 2(b): an open choice with no printed list; one task.'),
    (2, 'or', 'Q3 options (i) or (ii): part (a) requires both; part (b) selects one, marked with the same rows either way.'),
    (2, 'Select', 'Q3(b) select one of the two options: one task, the scheme marking either option with the same five rows.'),
    (2, 'one of', 'Q3(b) same directive: one task.'),
    (3, 'any two', 'Q4(a) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
    (3, 'One of', 'Narrative identifies one cottage, not an answer selection.'),
    (3, 'Select', 'Q4(b) closed choose-two of the three surveyed areas: one card with an any-two group (choice is not a route).'),
    (3, 'any two', 'Q4(b) same directive.'),
    (4, 'any two', 'Q6(b) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
    (5, 'Select', 'Q9(a) closed choose-three of the four circled locations: one card with an any-three group (choice is not a route).'),
    (5, 'any three', 'Q9(a) same directive.'),
    (5, 'any two', 'Q10(a) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
    (5, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.'),
    (5, 'one of', 'Quotation narrative, not an answer directive.'),
]
pattern = OLD_REVIEW['selectionLedger']['pattern']
observed = []
with fitz.open(R / P) as pdf:
    for i, p in enumerate(pdf):
        text = ' '.join(p.get_text().split())
        observed.extend((i + 1, m.start(), m.group(), text[max(0, m.start() - 80):m.end() + 80]) for m in re.finditer(pattern, text, re.I))
assert [(o[0], o[2]) for o in observed] == [(r[0], r[1]) for r in ledger_rows], observed
selection_ledger = dict(pattern=pattern, unclassified=0, sourceHashes=HASHES,
                        rows=[dict(page=o[0], start=o[1], match=o[2], context=o[3], classification=r[2]) for o, r in zip(observed, ledger_rows)],
                        finiteQuestionChoices={
                            '4a': dict(choose=2, options=ITEMS4A, cardId=A4['id'], groupRowId='items'),
                            '4b': dict(choose=2, options=ITEMS4B, cardId=B4b['id'], groupRowId='areas'),
                            '6b': dict(choose=2, options=['Compact form', 'Flexible design', 'Low maintenance'], cardId=B6b['id'], groupRowId='features'),
                            '9a': dict(choose=3, options=LOCATIONS9, cardId=A9['id'], groupRowId='locations'),
                            '10a': dict(choose=2, options=['Airtight building envelope', 'Space heating demand', 'Indoor air quality'], cardId=A10['id'], groupRowId='items')},
                        optionSelectionsMarkedAlike={'3b': dict(options=['(i) extension at A', '(ii) detached space at B'], cardId=B3b['id'])})
whole = {}
for t in tasks:
    c = t['card']
    if '-complete' in c['id']:
        whole.setdefault('10-alt' if t['alternative'] else t['questionNumber'], []).append(dict(id=c['id'], parts=[g['label'] for g in c['taskGroups']], marks=c['totalMarks']))

LIFTED = 'Stem and question text lifted verbatim from the paper, replacing the earlier authored paraphrase'
REASONS = {
    'q3-a-A': f'{LIFTED}; now the four printed 3-mark rows for option A (two advantages, two disadvantages) in place of two narrower per-pair tasks, which are withdrawn. Tariff unchanged (12).',
    'q3-a-B': f'{LIFTED}; now the four printed 3-mark rows for option B in place of two narrower per-pair tasks, which are withdrawn. Tariff unchanged (12).',
    'q3-a': f'{LIFTED}; composes the two option tasks with their printed rows. Tariff unchanged (24).',
    'q3-c': f'{LIFTED}; split into the two printed 3-mark advantage rows. Tariff unchanged (6).',
    'q5-a': f'{LIFTED}, with the printed data; the seven resistances (both surfaces and five layers, 3 each) now sit under the scheme’s “Formulae” heading instead of single-layer headings that named only one of them. Tariff unchanged (30).',
    'q6-a': f'{LIFTED}; rows renamed to the printed headings Design feature 1-3. Tariff unchanged (30).',
}
corrections = []
for t in tasks:
    c = t['card']
    if c['id'] in PRIOR:
        old = PRIOR[c['id']]
        key = c['id'].removeprefix(PREFIX)
        reason = REASONS.get(key) or (f"{LIFTED}; composes its reviewed constituent tasks. Tariff unchanged ({c['totalMarks']})."
                                     if 'taskGroups' in c else f"{LIFTED}; rows and tariff unchanged ({c['totalMarks']}).")
        assert old['totalMarks'] == c['totalMarks'] and old['conceptId'] == c['conceptId'], c['id']
        corrections.append(dict(cardId=c['id'], priorSha256=card_hash(old), correctedSha256=card_hash(c),
                                priorTotalMarks=old['totalMarks'], correctedTotalMarks=c['totalMarks'],
                                priorTopicId=old['topicId'], correctedTopicId=c['topicId'], reason=reason))
assert len(corrections) == 37 and len(tasks) == 48

out = dict(schemaVersion=1, subjectId='construction-studies', year=2015, level='higher', lang='ev', sitting='main', paperKey='single',
           fileid='LC029ALP000EV.pdf', component='theory',
           status='2015 Higher main English THEORY: 48 source-reviewed tasks with lifted wording; every printed choice is one card (choice is not a route).',
           sourceHashes=HASHES, tasks=tasks, bindings=bindings, questionFigures=question_figures, newFigureAlts=NEW_FIGURE_ALTS,
           addedIds=[t['card']['id'] for t in tasks if not t['correction']], corrections=corrections,
           selectionLedger=selection_ledger, questionRouteLedgers={q: dict(wholeRoutes=w) for q, w in whole.items()}, taxonomyGaps=[],
           questionsReviewed=[str(n) for n in range(1, 11)], unreviewedQuestions=[], alternativeQuestions=['10'], paperComplete=True,
           reviewedAt='2026-10-12T00:00:00+00:00',
           fullPaperReconciliation=dict(questions=10, alternativeQuestions=1,
                                        examRubric='Question 1 and four other questions, 60 marks each, 300 total; no full-exam Cartesian cards.',
                                        method='Same-operator source review of paper pages 1-5 and scheme pages 2-42; validator construction_2015_higher.py.'),
           priorCards='docs/markbank-audit/2026-09-28/drafts/construction-2015-higher/prior-2015-higher-cards.json',
           priorAuthoredCardHashes='docs/markbank-audit/2026-09-28/drafts/construction-2015-higher/prior-authored-card-hashes.json')
(HERE / 'higher-2015-draft.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(tasks=len(tasks), added=len(out['addedIds']), corrected=len(corrections), figures=len(question_figures),
                      withdrawn=len(set(PRIOR) - set(cards)),
                      perQuestion={q: sum(1 for t in tasks if t['questionNumber'] == q and not t['alternative']) for q in QUESTIONS},
                      alternative=sum(1 for t in tasks if t['alternative']), wholeRoutes={q: len(w) for q, w in whole.items()})))
