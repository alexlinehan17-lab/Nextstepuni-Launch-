"""Draft the 2013 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 15-23). The paper was never carded, so every task is added. Question 5 is one unlettered drawing
question, so it is one whole-question card. Q8 "any five of nine" is ONE card (choice is not a route).
The text layer prints Q6(a)'s three bullets after Q9; they are read back into Q6 (module TAILS).
Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Timber flat roof eaves section', concept='flat-roof-eaves-section',
              stem='The eaves of a timber flat roof for a bathroom is constructed as shown in the sketch. The roof is covered with layers of bituminous felt on plywood decking on 200 mm × 50 mm roof joists. The roof is insulated and there is a plasterboard ceiling beneath. The external wall supporting the flat roof is a 350 mm concrete block wall with an insulated cavity.',
              note='Original sketch and specification retained. The scheme prints the draughting, accuracy and scale band after the part (b) row, so it is marked with the rainwater detail.'),
    '2': dict(page=2, title='Cavity fill and internal insulation of external walls', concept='cavity-internal-insulation',
              stem='The sketch shows a dwelling house which was built over ten years ago. The external walls of the house are 300 mm concrete block walls with an un-insulated cavity. It is proposed to improve the insulation properties of the external walls by: insulating the cavity and adding a system of insulation to the inside of the walls.',
              note='Original sketch retained. Both printed systems of insulation in (a) are required, each separately marked.'),
    '3': dict(page=2, title='Hot and cold water to a basin and bath, and an easy-use tap', concept='basin-bath-water-supply', stem='',
              note='Original sketch retained. The listed components are required content, not a choice; the best-seven list is a marking menu.'),
    '4': dict(page=2, title='Setting out and a strip foundation', concept='setting-out-strip-foundation', stem='',
              note='Original sketch retained. All four printed headings in (a) are required, each separately marked.'),
    '5': dict(page=3, title='Stud partition on a timber floor section', concept='stud-partition-floor-section',
              stem='A non load-bearing stud partition separates two upstairs bedrooms in a dwelling house. The floor and partition are supported on a 215 mm solid block wall, as shown in the sketch. The floor is a floating tongued and grooved oak floor on plywood, on 200 mm × 50 mm joists with a plasterboard ceiling beneath.',
              note='Original sketch and specification retained. Question 5 has no lettered parts: one drawing, marked as a whole.'),
    '6': dict(page=3, title='Personal protective equipment on site', concept='site-ppe', stem='',
              note='Original sketch retained. All three printed items in (a) and (b) are required, each separately marked.'),
    '7': dict(page=3, title='Insulated solid ground floor junction and bathroom floor covering', concept='ground-floor-junction',
              stem='A dwelling house has an insulated solid concrete ground floor which abuts a 350 mm concrete block external wall with an insulated cavity, as shown in the sketch. The floor has a sand/cement fine screed finish.',
              note='Original sketch retained. The floor covering is an open response; the scheme lists typical examples.'),
    '8': dict(page=3, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=3, title='Glazed solid oak double doors', concept='glazed-oak-doors',
              stem='Two solid oak doors with glazed panels are fitted in the dividing wall between a sitting room and a kitchen, as shown in the sketch.',
              note='Original sketch retained. The joint is an open choice; the scheme gives a haunched or rebated mortise and tenon.'),
}
SCHEME_PAGES = {'1': [4, 5, 15], '2': [5, 6, 16], '3': [6, 17], '4': [7, 8, 18], '5': [8, 19], '6': [9, 10, 20], '7': [10, 11, 21], '8': [11, 12, 13, 22], '9': [14, 23]}
D = cp.Draft(HERE, 2013, 'ordinary', ('c339448bf1d0e305695e8e4c6671facec2416b13b03c5617cfd632e28f77c34b',
                                      'bbb47b80dd5a3770ac1af97855fbee9264beca1dac16d7c3749ba43acf83541b'), 0, QUESTIONS, SCHEME_PAGES)
row, add, compose = D.row, D.add, D.compose
BAND8 = [0, 4, 6, 8]
BAND6 = [0, 2, 4, 6]


def parts(*cards):
    return D.parts(*[(letter, c['questionText']) for letter, c in zip('abc', cards)])


def quality(verbatim, what='the sketches', rid='presentation'):
    return row(rid, verbatim, 8, f'Quality of {what}: excellent 8, good 6, fair 4.', BAND8)


D.figures({
    'q1-original': D.paper(2, [30, 39, 580, 228]), 'q2-original': D.paper(2, [30, 228, 580, 430]),
    'q3-original': D.paper(2, [30, 430, 580, 621]), 'q4-original': D.paper(2, [30, 621, 580, 790]),
    'q5-original': D.paper(3, [30, 39, 580, 208]), 'q6-original': D.paper(3, [30, 208, 580, 378]),
    'q7-original': D.paper(3, [30, 378, 580, 551]), 'q8-original': D.paper(3, [30, 551, 580, 650]),
    'q9-original': D.paper(3, [30, 650, 580, 797]),
    'q1-section': D.scheme(4, [25, 45, 580, 778]), 'q1-rainwater': D.scheme(5, [25, 45, 580, 206]),
    'q2-systems': D.scheme(5, [25, 206, 580, 778]),
    'q2-advantages': D.scheme(6, [25, 45, 580, 195]),
    'q3-system': D.scheme(6, [25, 195, 580, 578]), 'q3-tap': D.scheme(6, [25, 578, 580, 778]),
    'q4-setting-out': D.scheme(7, [25, 45, 580, 779]), 'q4-strip': D.scheme(8, [25, 45, 580, 340]),
    'q5-scheme': D.scheme(8, [25, 340, 580, 778]),
    'q6-signs': D.scheme(9, [25, 45, 580, 216]), 'q6-tasks': D.scheme(9, [25, 216, 580, 560]),
    'q6-other': D.composite((9, [25, 560, 580, 778]), (10, [25, 45, 580, 293])),
    'q7-floor': D.scheme(10, [25, 293, 580, 576]), 'q7-cold-bridge': D.scheme(10, [25, 576, 580, 778]),
    'q7-covering': D.scheme(11, [25, 45, 580, 500]),
    'q8-terms': D.composite((11, [25, 500, 580, 778]), (12, [25, 45, 580, 778]), (13, [25, 45, 580, 778])),
    'q9-joint': D.scheme(14, [25, 45, 580, 312]), 'q9-glass': D.scheme(14, [25, 312, 580, 613]),
    'q9-advantages': D.scheme(14, [25, 613, 580, 778]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p15 (printed 12): (a) best 7 of 15 listed details × 5 = 35, four typical dimensions 4 = 39; (b) eaves gutter and downpipe 3, and draughting, accuracy and scale 8 (8/6/4) printed after it = 11. Complete 50.'
S1 = 'One required section and one required rainwater detail. The best-seven detail list is a marking menu, not a printed choice.'
A1 = add('1', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the eaves of the flat roof and through the external wall. The section should show the typical construction details from 400 mm below the wallplate, through the wall, fascia, soffit and roof joists and include the roof surface. Show 1.5 metres length of roof joist and include four typical dimensions.',
         [row('details', 'Any 7 of the above details ( 5 marks each)', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: three layers of bituminous felt; plywood decking 25 mm; 50 × 50 mm counter battens on a firring piece; roof/ceiling joists 200 × 50 mm; at least 150 mm insulation; 12.5 mm insulated foil-backed plasterboard and skim; an airtightness seal taped to the masonry; a 100 × 75 mm wallplate with straps; a cavity barrier or non-combustible tile or slate; 15 mm internal plaster; 100 mm inner leaf; cavity insulation; 100 mm outer leaf; 19 mm render; fascia and soffit.', list(range(0, 36, 5))),
          row('dimensions', 'Four typical dimensions', 4, 'Four appropriate typical dimensions on the section, 1 each.')],
         ['cons-1-5', 'cons-3-10', 'cons-3-3'], ['question-one-drawing-questions', 'roofs', 'foundations-floors-walls'], 'q1-section',
         'Scaled drawing (1.5) of a flat roof at the eaves (3.10) on a cavity wall (3.3).', B1, S1)
B1b = add('1', 'b', '(b)', 'On your drawing, show how rainwater is removed from the flat roof.',
          [row('rainwater', 'Eave gutter and downpipe', 3, 'Show the eaves gutter and downpipe, as in the scheme: the felt turned down over a 50 × 25 mm drip batten into the gutter fixed to the fascia, the firring giving the fall, and a downpipe to ground level.'),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the whole section: excellent 8, good 6, fair 4. The scheme prints this band after the part (b) row.', BAND8)],
          ['cons-3-10', 'cons-5-4'], ['roofs', 'drainage'], 'q1-rainwater', 'Flat roof eaves (3.10) draining to an eaves gutter (5.4).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p16 (printed 13): (a) for each printed system, two descriptions × 4 and insulation type and internal finish 4 = 12, and quality of sketch and details 8 (8/6/4) = 40; (b) two advantages × 5 = 10. Complete 50.'
S2 = 'Both printed systems of insulation in (a) are required, each separately marked; not a choice.'
A2 = add('2', 'a', '(a)', 'Using notes and neat freehand sketches, show how to apply each system of insulation to the wall. For each system of insulation, specify the insulation material used and include details of the internal surface finish of the wall.',
         [row('cavity-notes', 'Insulating the cavity – Notes', 12, 'Two valid descriptions 4 each, and the insulation type and internal finish 4. Such as: 22 mm holes drilled through the outer leaf at 800 mm horizontally and 1350 mm vertically, with extra holes under cills and over heads; polystyrene beads pumped in with a light glue by a specialist; the holes filled and painted to match.'),
          row('cavity-sketch', 'Quality of sketch and details (excellent, good, fair)', 8, 'Quality of the cavity-fill sketch and details: excellent 8, good 6, fair 4.', BAND8),
          row('internal-notes', 'Adding a system of insulating to the inside of the walls – Notes', 12, 'Two valid descriptions 4 each, and the insulation type and internal finish 4. Such as: 50 × 50 mm battens at 400 mm centres with insulation between, a vapour barrier and 12 mm plasterboard and skim; or insulated dry-lining board glued and mechanically fixed, joints taped and filled, and emulsion paint. Insulation such as fibreglass, polystyrene, polyurethane, cork, hemp or sheep’s wool.'),
          row('internal-sketch', 'Quality of sketch and details (excellent, good, fair)', 8, 'Quality of the internal-insulation sketch and details: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q2-systems',
         'Insulating materials (6.2) added to a cavity wall (3.3).', B2, S2)
B2b = add('2', 'b', '(b)', 'List two advantages of improving the insulation properties of the external walls of the house.',
          [row('advantage-1', 'Advantage one', 5, 'Such as: less heat loss; a warmer house and a better indoor environment.'),
           row('advantage-2', 'Advantage two', 5, 'A second, different advantage. Such as: lower energy bills, better for the environment; a better U-value and Building Energy Rating.')],
          ['cons-6-3', 'cons-6-2'], ['heat-loss-insulation'], 'q2-advantages', 'Heat loss and running costs (6.3) with insulation (6.2).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b], 'q2-systems', B2, S2, parts(A2, B2b))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p17 (printed 14): (a) best 7 of 12 listed details × 5 = 35 and quality of sketch 8 (8/6/4) = 43; (b) tap design primary communication 4 and other communication 3 = 7. Complete 50.'
S3 = 'The printed component list is required content, not a choice; the best-seven list is a marking menu.'
A3 = add('3', 'a', '(a)', 'Using a single-line labelled diagram, show the pipework necessary to supply hot and cold water to a wash hand basin and a bath, as shown in the sketch. Include the following in your diagram: water storage tank and overflow; rising main; hot water cylinder and pipework; insulation to the water storage tank and to all pipework; location of all necessary valves.',
         [row('details', 'Any 7 of the above details (5 marks each)', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: rising main; ballvalve; cold water storage tank; overflow; cold feed from the storage tank to the indirect cylinder; indirect hot water cylinder; expansion pipe from the cylinder; hot water supply to the appliances; cold water supply from the storage tank to the appliances; valves; insulation to the tank, cylinder and pipework; labelling.', list(range(0, 36, 5))),
          quality('Quality of sketch (excellent, good, fair)', 'the sketch')],
         ['cons-5-2'], ['hot-water-space-heating', 'services-water-gas-electrical'], 'q3-system', 'Hot and cold water systems, cisterns and cylinders (5.2).', B3, S3)
B3b = add('3', 'b', '(b)', 'Show, using notes and neat freehand sketches, a design for a tap which will be easy to use by a person with limited hand mobility.',
          [row('primary', 'Primary communication of relevant information', 4, 'Such as: a spatula lever tap needing a quarter turn from off to full flow; a tall swivel-neck mixer for filling large containers.'),
           row('other', 'Other communication of relevant information', 3, 'Such as: taps placed within easy reach, perhaps to the side; water pressure adjusted so it does not spray or splash.')],
          ['cons-5-6', 'cons-1-2'], ['drainage', 'planning-sustainability-environment'], 'q3-tap', 'Sanitary fitments (5.6) designed for all users (1.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-system', B3, S3, parts(A3, B3b))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p18 (printed 15): (a) four printed headings × (primary communication 5 + other communication 4) = 36; (b) position of reinforcement 3, typical dimensions 3 and quality of sketch 8 (8/6/4) = 14. Complete 50.'
S4 = 'All four printed headings in (a) are required, each separately marked; not a choice.'
FOUND = 'No Ordinary outgoing reference heading covers setting out and excavation (2.1); the card keeps the Foundations, Floors & Walls association.'
A4 = add('4', 'a', '(a)', 'One corner of a trench for a strip foundation is shown in the sketch. Describe, using notes and neat freehand sketches, the setting-out of a typical strip foundation under the following headings: levelling the profiles; locating the position of the trench; squaring the corner of the trench; locating the finished level of the concrete in the foundation.',
         [row('profiles', 'Levelling the profiles', 9, 'Primary communication 5 and other communication 4. Such as: profiles of two uprights and a cross rail, levelled from a secured datum point with a laser, optical or water level, the top usually at finished floor level.'),
          row('trench', 'Locating the position of the trench', 9, 'Primary communication 5 and other communication 4. Such as: lines stretched across the profile rails at the four corners locate the outside of the wall; the wall and trench widths marked on the profiles.'),
          row('square', 'Squaring the corner of the trench', 9, 'Primary communication 5 and other communication 4. Such as: lines at right angles to the building line set with a 3, 4, 5 triangle; the rectangle checked by measuring the diagonals.'),
          row('level', 'Locating the finished level of the concrete in the foundation', 9, 'Primary communication 5 and other communication 4. Such as: pegs driven in the trench with their tops level with the top of the foundation, set by laser or with boning rods and a traveller.')],
         ['cons-2-1', 'cons-2-4'], ['foundations-floors-walls'], 'q4-setting-out', 'Setting out and excavation (2.1) for a strip foundation (2.4).', B4, S4)
B4b = add('4', 'b', '(b)', 'Draw a sketch of a typical strip foundation for a 350 mm concrete block external wall and show the position of the reinforcing in the foundation. Include three typical dimensions in your sketch.',
          [row('reinforcement', 'Position of reinforcement', 3, 'The reinforcing steel shown in the lower part of the foundation, as in the scheme’s model sketch.'),
           row('dimensions', 'Typical dimensions', 3, 'Three typical dimensions, 1 each.'),
           quality('Quality of sketch (excellent, good, fair)', 'the sketch')],
          ['cons-2-4', 'cons-2-5'], ['foundations-floors-walls'], 'q4-strip', 'A strip foundation (2.4) with its reinforcement (2.5).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b], 'q4-setting-out', B4, S4, parts(A4, B4b))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p19 (printed 16): best 6 of 12 listed details × 6 = 36, three typical dimensions 6 and draughting, accuracy and scale 8 (8/6/4). Total 50.'
S5 = 'One required section; the best-six detail list is a marking menu, not a printed choice.'
add('5', 'section', '', 'To a scale of 1:5, draw a vertical section through the stud partition and the floor. Show the typical construction details from a level 300 mm below the plasterboard ceiling, through the wall, floor and partition to a point 400 mm above the finished floor level. Include three typical dimensions on your drawing. Note: Show a floor width of 500 mm at each side of the partition.',
    [row('details', 'Any 6 of the above details ( 6 marks each)', 36, 'Credit the best SIX acceptable details at 6 marks each, capped at 36. Marked details: stud partition 100 × 50 mm; insulation between the studs; 12.5 mm plasterboard; 120 × 20 mm skirting; floating tongued and grooved oak floor; bubble underlay or matting; 18–25 mm plywood; 200 × 50 mm joists; at least 150 mm insulation between the joists; plasterboard, plaster and vapour barrier; 15 mm plaster; 215 mm solid block wall.', list(range(0, 37, 6))),
     row('dimensions', 'Three typical dimensions', 6, 'Three typical dimensions, 2 each.'),
     row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the section: excellent 8, good 6, fair 4.', BAND8)],
    ['cons-1-5', 'cons-4-5', 'cons-4-3'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls'], 'q5-scheme',
    'Scaled drawing (1.5) of a stud partition (4.5) on a timber upper floor (4.3).', B5, S5)

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p20 (printed 17): (a) three signs, quality of sketch 6 (6/4/2) each = 18; (b) a task for each item × 6 = 18; (c) one other item 6 and two reasons × 4 = 14. Complete 50.'
S6 = 'All three printed items are required in (a) and (b), each separately marked; the other item in (c) is an open response.'
SITE = (['cons-1-8'], ['site-safety'])
A6 = add('6', 'a', '(a)', 'For each of the following, draw the particular safety sign to indicate that the following personal protective equipment (ppe) must be worn on a construction site: eye protection; ear protection; safety gloves.',
         [row(rid, f'{item} Quality of sketch (excellent, good, fair)', 6, f'The mandatory blue sign for {item.lower()}, as in the scheme: quality of the sketch, excellent 6, good 4, fair 2.', BAND6)
          for rid, item in [('eye-sign', 'Eye protection'), ('ear-sign', 'Ear protection'), ('gloves-sign', 'Safety gloves')]],
         *SITE, 'q6-signs', 'Safety signs on site (1.8).', B6, S6)
B6b = add('6', 'b', '(b)', 'For each item of personal protective equipment listed at 6(a) above, outline one specific task on a building site where workers must wear the personal protective equipment.',
          [row('eye', 'Eye protection', 6, 'Such as: drilling or cutting concrete or steel; chipping paint; using a hammer, angle grinder or nail gun; welding.'),
           row('ear', 'Ear protection', 6, 'Such as: using machinery, drills or pneumatic tools; cutting equipment; continuous noise of 85–90 decibels or more.'),
           row('gloves', 'Safety gloves', 6, 'Such as: handling sharp edges such as glass; hot bitumen on flat roofs; vibrating machinery; corrosive or toxic substances.')],
          *SITE, 'q6-tasks', 'Personal protective equipment on site (1.8).', B6, S6)
C6 = add('6', 'c', '(c)', 'List one other item of personal protective equipment that must be worn at all times on a construction site and discuss the reasons why the wearing of this item is compulsory.',
         [row('item', 'Item of personal protection equipment', 6, 'Such as: a high visibility jacket; a safety helmet; steel cap boots.'),
          row('reason-1', 'Valid reason one', 4, 'A reason matching the item. Such as: a high visibility jacket keeps workers visible, especially near machinery; a helmet protects the head from falling objects.'),
          row('reason-2', 'Valid reason two', 4, 'A second, different reason. Such as: extra safety for workers; steel caps protect the toes from falling items.')],
         *SITE, 'q6-other', 'Personal protective equipment on site (1.8).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-signs', B6, S6, parts(A6, B6b, C6))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p21 (printed 18): (a) two details × 4, three dimensions 6, labelling 8 and quality of sketch 8 (8/6/4) = 30; (b) cold bridge detail 5; (c) floor covering 5 and two reasons × 5 = 15. Complete 50.'
S7 = 'The floor covering in (c) is an open response; the scheme lists typical examples.'
A7 = add('7', 'a', '(a)', 'Show, using notes and neat freehand sketches, the typical design detailing at the junction of the floor and wall. Label the floor components and include three typical dimensions.',
         [row('detail-1', 'Valid detail one', 4, 'Such as: a 25–50 mm screed on a 100–150 mm slab, taped to the wall for airtightness.'),
          row('detail-2', 'Valid detail two', 4, 'A second, different detail. Such as: 200 mm floor insulation on a DPM/radon barrier, on sand blinding and at least 150 mm hardcore.'),
          row('dimensions', 'Three typical dimensions', 6, 'Three typical dimensions, 2 each.'),
          row('labelling', 'Labelling the floor components and other details', 8, 'The floor components labelled, as in the scheme’s model sketch.'),
          quality('Quality of sketch (excellent, good, fair)', 'the sketch')],
         ['cons-4-2', 'cons-3-3'], ['foundations-floors-walls'], 'q7-floor', 'A solid ground floor (4.2) at a cavity wall (3.3).', B7, S7)
B7b = add('7', 'b', '(b)', 'Show clearly on your sketch the typical design detailing which will prevent the formation of a cold bridge at the junction of the floor and the wall.',
          [row('cold-bridge', 'Shown on sketch', 5, 'Such as: vertical perimeter insulation between the slab and the inner leaf, overlapping the wall insulation by 150–225 mm; lightweight insulating blocks in the inner leaf from the floor insulation to floor level.')],
          ['cons-6-2', 'cons-4-2'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q7-cold-bridge', 'A thermal bridge (6.2) at the ground floor junction (4.2).', B7, S7)
C7 = add('7', 'c', '(c)', 'Recommend a suitable floor covering for a bathroom on the ground floor of the house and give two reasons for your choice of floor covering.',
         [row('covering', 'Type of floor covering', 5, 'Such as: ceramic tiles; vinyl; cork tiles; heavy-duty linoleum; marmoleum; natural stone.'),
          row('reason-1', 'Reason one', 5, 'A reason matching the covering. Such as: ceramic tiles are durable, with textured, less slippery finishes; vinyl resists water, stains and scuffs.'),
          row('reason-2', 'Reason two', 5, 'A second, different reason. Such as: easy to clean and low maintenance; warm underfoot and resistant to mould (cork); affordable, in a wide range of colours.')],
         ['cons-4-2'], ['foundations-floors-walls'], 'q7-covering', 'Ground floor finishes (4.2).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-floor', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p22 (printed 19): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination. No pre-audit card existed for this question.'
TERMS = [
    ('solar panel', 'Solar panel', ['cons-6-4'], ['planning-sustainability-environment'],
     'collects solar radiation and converts it to heat; generally on a south-facing sloping roof, or on secure fixings at ground level; flat plate or evacuated tube; used with other heating; helps reduce CO₂.', 'Solar heat gain (6.4).'),
    ('dovetail halving joint', 'Dovetail halving joint', ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'],
     'like a tee halving with a dovetail slope added, half the thickness taken from each piece; strong, resists pulling and has a large gluing area; slope 1:8 for hardwoods, 1:6 for softwoods.',
     'Joints (10.1) and the choice of joint (10.4). The Ordinary reference taxonomy has no joinery heading; the term keeps the Wood, Rot & Ventilation association used for joinery, and 10.1/10.4 are declared outside that heading’s crosswalk.'),
    ('sash cramp', 'Sash cramp', ['cons-10-6'], ['wood-rot-ventilation'],
     'a steel bar with a threaded mechanism at one end and a movable shoe, used to put pressure on wooden members while glue sets, as in furniture making; in various lengths.',
     'Holding work while gluing (10.6). The Ordinary reference taxonomy has no workshop heading; the term keeps the Wood, Rot & Ventilation association used for joinery, and 10.6 is declared outside that heading’s crosswalk.'),
    ('flue liner', 'Flue liner', ['cons-5-7'], ['fire-places-fire-prevention'],
     'a conduit carrying smoke from the fire or stove, built in as the chimney is constructed or fitted to an existing chimney for a new stove; usually ceramic clay, or flexible stainless steel.', 'Flues to domestic fireplaces (5.7).'),
    ('purlin', 'Purlin', ['cons-3-8'], ['roofs'],
     'the member stretching under the rafters to support a traditional cut roof, typically 150 × 75 mm, carried on struts to an internal load-bearing wall or on an RSJ; it helps attic development.', 'Roof forms (3.8).'),
    ('water-table', 'Water table', ['cons-2-1'], ['foundations-floors-walls'],
     'the natural level of underground water: rain percolates through the topsoil and subsoil; it rises and falls with rainfall, with springs appearing as it rises; below it water is held in aquifers reached by deep wells.',
     'Water in excavations (2.1). No Ordinary outgoing reference heading covers site water; the term keeps the Foundations, Floors & Walls association, and 2.1 is declared outside that heading’s crosswalk.'),
    ('wind turbine', 'Wind turbine', ['cons-5-8'], ['services-water-gas-electrical'],
     'converts the energy of the wind into mechanical energy to generate electricity, small scale or commercial; a clean source of energy; blades, generator and support tower.', 'Domestic electricity supply (5.8).'),
    ('low-e coating', 'Low-e coating', ['cons-3-6', 'cons-6-2'], ['windows-doors', 'heat-loss-insulation'],
     'a very thin transparent metal or metal-oxide coating on the inner pane of double glazing that reflects heat back into the house while admitting solar gain; dearer, but reduces heat loss.', 'Glazing (3.6) that reduces heat loss (6.2).'),
    ('vapour barrier', 'Vapour barrier', ['cons-6-6'], ['air-tightness-condensation'],
     'a continuous membrane on the warm side of the insulation, slowing water vapour into it; used in timber frame walls, flat roofs and attic conversions; often part of insulated plasterboard.', 'Vapour barriers (6.6).'),
]
Q8 = add('8', 'terms', '', 'Explain with the aid of notes and neat freehand sketches, any five of the following: ' + '; '.join(t[0] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Terms', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{t[1]}: {t[4]}' for t in TERMS),
               group=dict(claimMax=5, perOption=10, options=[t[1] for t in TERMS]))],
         list(dict.fromkeys(n for t in TERMS for n in t[2])), list(dict.fromkeys(a for t in TERMS for a in t[3])), 'q8-terms',
         'The union of the nine printed terms: ' + ' '.join(t[5] for t in TERMS), B8, S8)

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p23 (printed 20): (a) two joint details × 6 and quality of sketch 8 (8/6/4) = 20; (b) two glazing details × 6 and quality of sketches 8 (8/6/4) = 20; (c) two advantages × 5 = 10. Complete 50.'
S9 = 'The joint in (a) is an open choice; the scheme gives a haunched or rebated mortise and tenon.'
A9 = add('9', 'a', '(a)', 'Show, using notes and neat freehand sketches, a suitable joint for joining the top rail to the vertical stile of the door.',
         [row('detail-1', 'Valid detail - one', 6, 'Such as: a haunched, rebated mortise and tenon — the traditional joint for good joinery; a mortise with a haunch in the upper stile.'),
          row('detail-2', 'Valid detail - two', 6, 'A second, different detail. Such as: a tenon with a haunch on the top rail; rebates on the rail and stile to take the glass; strong, with a high glue area, resisting twisting.'),
          quality('Quality of sketch (excellent good fair)', 'the sketch')],
         ['cons-3-7', 'cons-10-1'], ['windows-doors', 'wood-rot-ventilation'], 'q9-joint', 'Door details (3.7) and their joints (10.1).', B9, S9)
B9b = add('9', 'b', '(b)', 'Show, using notes and neat freehand sketches, how to fit one glass panel safely in the door.',
          [row('detail-1', 'Valid detail one', 6, 'Such as: the panel size checked against the frame; help engaged; the door steadied with a wedge; the rebate cleaned.'),
           row('detail-2', 'Valid detail two', 6, 'A second, different detail. Such as: clear silicone in the rebate and a spacer at the bottom; the panel lifted in wearing safety gloves; the stops fitted to hold it; surplus silicone trimmed and the glass cleaned.'),
           quality('Quality of sketches (excellent good fair)')],
          ['cons-3-6', 'cons-3-7'], ['windows-doors'], 'q9-glass', 'Glazing (3.6) a door (3.7).', B9, S9)
C9 = add('9', 'c', '(c)', 'Discuss two advantages of fitting glazed double doors between the sitting room and the kitchen in a dwelling house.',
         [row('advantage-1', 'Advantage one', 5, 'Such as: opened for extra space and people; the glass lets light through to both rooms.'),
          row('advantage-2', 'Advantage two', 5, 'A second, different advantage. Such as: closed to cut heating costs or keep cooking separate; a confined area for children; better use of the total area.')],
         ['cons-3-7', 'cons-1-2'], ['windows-doors', 'planning-sustainability-environment'], 'q9-advantages', 'Doors (3.7) in the layout of the home (1.2).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-joint', B9, S9, parts(A9, B9b, C9))

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and three other questions (200 marks); all question banks retained, no full-exam Cartesian cards.'),
          (3, 'any five', 'Q8 closed choose-five of nine printed terms: one card with an any-five group over all nine terms (choice is not a route).')]
FINITE = {'8': dict(choose=5, options=[t[1] for t in TERMS], cardId=Q8['id'], groupRowId='terms', wholeQuestionMarks=50, termMarks=10)}
JOIN = 'No Ordinary outgoing reference heading covers joinery (10.1, 10.4, 10.6); the card keeps the Wood, Rot & Ventilation association.'
GAPS = [dict(cardId=A4['id'], canonicalTopicIds=['cons-2-1'], atlasTopicId=D.CROSS + 'foundations-floors-walls', reason=FOUND),
        dict(cardId=B4b['id'], canonicalTopicIds=['cons-2-5'], atlasTopicId=D.CROSS + 'foundations-floors-walls',
             reason='No Ordinary outgoing reference heading covers reinforcement (2.5); the card keeps the Foundations, Floors & Walls association.'),
        dict(cardId=Q8['id'], canonicalTopicIds=['cons-10-1', 'cons-10-4', 'cons-10-6'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers joinery or workshop clamping (10.1, 10.4, 10.6: dovetail halving joint, sash cramp).'),
        dict(cardId=Q8['id'], canonicalTopicIds=['cons-2-1'], atlasTopicId=D.CROSS + 'foundations-floors-walls',
             reason='No Ordinary outgoing reference heading covers water in the ground (2.1, water table); the term keeps the Foundations, Floors & Walls association.'),
        dict(cardId=A9['id'], canonicalTopicIds=['cons-10-1'], atlasTopicId=D.CROSS + 'wood-rot-ventilation', reason=JOIN)]
D.finish(LEDGER, FINITE, {}, taxonomy_gaps=GAPS, whole_choices={'q8-terms', 'q5-section'})
