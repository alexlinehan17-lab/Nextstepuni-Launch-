"""Draft the 2016 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 17-25). Q8 "any five of nine" is ONE card (choice is not a route): it keeps the pre-audit
lever-valve ID and the other seven pre-audit per-term IDs alias to it (cob wall was never carded).
The other 19 pre-audit 2016 Ordinary cards keep their IDs and concept IDs and are corrected in place.
Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Strip foundation, cavity wall and insulated ground floor section', concept='foundation-floor-section',
              stem='A dwelling house has a 400 mm external concrete block wall with a 200 mm full-fill insulated cavity. The ground floor is an insulated concrete floor with a 20 mm floating tongue-and-groove hardwood finish, as shown.',
              note='Original sketch and specification retained. The scheme prints the draughting, accuracy and scale band after the part (b) row, so it is marked with the thermal-bridge detail.'),
    '2': dict(page=2, title='Insulating an attic, its tank and pipework', concept='attic-tank-insulation',
              stem='The owners of a house have decided to insulate their house over a number of years, starting with the attic space. The rafters and ceiling joists are 200 mm × 40 mm. The water storage tank is in the attic, as shown.',
              note='Original sketch retained. All three printed items in (a) are required, each separately marked.'),
    '3': dict(page=2, title='Stove and solar collector hot water', concept='stove-solar-hot-water',
              stem='The sketch shows a wood burning stove which is combined with a solar collector to provide hot water for a dwelling house. Also shown are a dual-coil hot water cylinder and the expansion tank in the attic.',
              note='Original sketch retained. The listed components are required content, not a choice; the best-eight list is a marking menu.'),
    '4': dict(page=2, title='Planning permission for a sunspace', concept='sunspace-planning',
              stem='The owners intend to apply for planning permission to build a sunspace on to the gable end of their house, as shown in the sketch.',
              note='Original sketch retained. Both printed planning documents in (b) are required, each separately marked.'),
    '5': dict(page=3, title='Cut string stairs section', concept='cut-string-stairs-section',
              stem='The sketch shows a portion of a cut string wooden stairs. The stairs leads to a small landing as shown. The newel post is 100 mm × 100 mm and the balusters are 50 mm × 50 mm. The rise of each step is 175 mm.',
              note='Original sketch and specification retained. The scheme prints the draughting, accuracy and scale band after the part (b) row, so it is marked with the baluster detail.'),
    '6': dict(page=3, title='Safety in the Construction Studies room', concept='workshop-safety', stem='',
              note='Original sketch retained. All three printed situations in (a) are required, each with two precautions and separately marked.'),
    '7': dict(page=3, title='Timber stud partition with a door', concept='stud-partition-door',
              stem='A non load-bearing timber stud partition with a plasterboard finish separates two bedrooms on the ground floor of a house. A solid wooden door is fitted in the stud partition, as shown.',
              note='Original sketch retained. The sound reduction and plasterboard finish are open choices of method.'),
    '8': dict(page=3, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=3, title='Eco-friendly garden room', concept='eco-garden-room',
              stem='The sketch shows an eco-friendly garden room with an external wooden cladding.',
              note='Original sketch retained. The wood, the finish and the features are open responses; the scheme lists typical examples.'),
}
SCHEME_PAGES = {'1': [4, 17], '2': [5, 18], '3': [6, 19], '4': [7, 8, 20], '5': [8, 21], '6': [9, 10, 22], '7': [11, 12, 23], '8': [12, 13, 14, 15, 24], '9': [15, 16, 25]}
D = cp.Draft(HERE, 2016, 'ordinary', ('1dae550c6c6e5a3dbb497bb66e319afd086086453929cfe829ba581c79f6b312',
                                      '167fd55b676b7b104721282db92dff78cedb79654ada944e5ea16a41dfc6f135'), 27, QUESTIONS, SCHEME_PAGES)
row, add, compose = D.row, D.add, D.compose
BAND8 = [0, 4, 6, 8]


def parts(*cards):
    return D.parts(*[(letter, c['questionText']) for letter, c in zip('abc', cards)])


def quality(what='the sketches', verbatim='Quality of sketches (excellent, good, fair)', rid='presentation'):
    return row(rid, verbatim, 8, f'Quality of {what}: excellent 8, good 6, fair 4.', BAND8)


D.figures({
    'q1-original': D.paper(2, [30, 39, 580, 207]), 'q2-original': D.paper(2, [30, 210, 580, 370]),
    'q3-original': D.paper(2, [30, 375, 580, 610]), 'q4-original': D.paper(2, [30, 615, 580, 790]),
    'q5-original': D.paper(3, [30, 39, 580, 170]), 'q6-original': D.paper(3, [30, 172, 580, 328]),
    'q7-original': D.paper(3, [30, 330, 580, 528]), 'q8-original': D.paper(3, [30, 532, 580, 620]),
    'q9-original': D.paper(3, [30, 625, 580, 790]),
    'q1-scheme': D.scheme(4, [25, 50, 580, 685]),
    'q2-attic': D.scheme(5, [25, 50, 580, 484]), 'q2-reasons': D.scheme(5, [25, 484, 580, 750]),
    'q3-system': D.scheme(6, [25, 50, 580, 478]), 'q3-solar': D.scheme(6, [25, 478, 580, 607]), 'q3-advantages': D.scheme(6, [25, 607, 580, 770]),
    'q4-reasons': D.scheme(7, [25, 50, 580, 320]), 'q4-documents': D.scheme(7, [25, 320, 580, 652]), 'q4-public': D.scheme(8, [25, 50, 580, 257]),
    'q5-scheme': D.scheme(8, [25, 260, 580, 710]),
    'q6-precautions': D.scheme(9, [25, 50, 580, 677]), 'q6-lathe': D.scheme(10, [25, 50, 580, 560]),
    'q7-partition': D.scheme(11, [25, 50, 580, 387]), 'q7-sound': D.composite((11, [25, 387, 580, 710]), (12, [25, 30, 580, 288])),
    'q7-finish': D.scheme(12, [25, 288, 580, 497]),
    'q8-terms': D.composite((12, [25, 497, 580, 710]), (13, [25, 50, 580, 776]), (14, [25, 50, 580, 710]), (15, [25, 50, 580, 509])),
    'q9-wood': D.composite((15, [25, 509, 580, 776]), (16, [25, 50, 580, 212])), 'q9-finish': D.scheme(16, [25, 212, 580, 547]),
    'q9-eco': D.scheme(16, [25, 547, 580, 745]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p17 (printed 14): (a) best 9 of 14 listed details × 4 = 36, four typical dimensions 4 = 40; (b) thermal-bridge detail 2, and draughting, accuracy and scale 8 (8/6/4) printed after it = 10. Complete 50.'
S1 = 'One required section and one required thermal-bridge detail. The best-nine detail list is a marking menu, not a printed choice.'
A1 = add('1', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the strip foundation, the external wall and the ground floor. Show the typical construction details from the bottom of the foundation to a level 400 mm above finished floor. Show the position of the radon barrier and include four typical dimensions on your drawing. Show 1.0 metre width of floor.',
         [row('details', 'Any 9 of the above details ( 4 marks each)', 36, 'Credit the best NINE acceptable details at 4 marks each, capped at 36. Marked details: 100 mm concrete path/ground level; DPC; 100 mm block outer leaf and 19 mm render; full-fill cavity insulation; wall tie; 100 mm block inner leaf and 13 mm plaster; skirting board; 20 mm floating timber floor; 150 mm concrete floor taped and sealed to the wall; 300 mm floor insulation; DPM/radon barrier; hardcore and sand blinding; concrete fill/foundation blocks; reinforced concrete foundation.', list(range(0, 37, 4))),
          row('dimensions', 'Four typical dimensions', 4, 'Four appropriate typical dimensions on the section, 1 each.')],
         ['cons-1-5', 'cons-2-4', 'cons-3-3', 'cons-4-2'], ['question-one-drawing-questions', 'foundations-floors-walls'], 'q1-scheme',
         'Scaled drawing (1.5) of a strip foundation (2.4), cavity wall (3.3) and solid ground floor (4.2).', B1, S1)
B1b = add('1', 'b', '(b)', 'On your drawing, show the typical design detailing to prevent the formation of a thermal bridge at the junction of the external wall and the floor.',
          [row('thermal-bridge', 'Perimeter insulation/thermal blocks/cavity insulation overlaps with floor insulation/flexible seal between floor and wall', 2, 'Show and identify the detail, as in the scheme’s model sections: perimeter insulation, thermal blocks, the cavity insulation overlapping the floor insulation, or a flexible seal between floor and wall.', [0, 2]),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the whole section: excellent 8, good 6, fair 4. The scheme prints this band after the part (b) row.', BAND8)],
          ['cons-6-2', 'cons-4-2'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q1-scheme', 'A thermal bridge (6.2) at the ground floor junction (4.2).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-scheme', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p18 (printed 15): (a) attic — joist, rafter, two layers of insulation × 4 = 12; tank — tank, supports, top and sides × 4 = 12; pipes — expansion and other pipes × 4 = 8; quality of sketches 8 (8/6/4) = 40; (b) two reasons × 5 = 10. Complete 50.'
S2 = 'All three printed items in (a) are required, each separately marked; not a choice.'
A2 = add('2', 'a', '(a)', 'Draw a large freehand sketch of the attic space. On your sketch, show the typical design detailing necessary to insulate, to a high standard, each of the following: attic space; water storage tank and pipework.',
         [row('attic', 'Attic insulation', 12, 'Ceiling joist 4, rafter 4 and insulation in two layers 4, as in the scheme’s model sketch.'),
          row('tank', 'Water storage tank insulation', 12, 'The tank 4, its supports kept free of insulation 4, and insulation on top and sides 4.'),
          row('pipes', 'Pipe insulation – Notes', 8, 'Insulation on the expansion pipe 4 and other exposed pipes 4.'),
          quality()],
         ['cons-3-9', 'cons-6-2', 'cons-5-2'], ['roofs', 'heat-loss-insulation', 'hot-water-space-heating'], 'q2-attic',
         'Insulating the roof space (3.9, 6.2) and its cistern and pipework (5.2).', B2, S2)
B2b = add('2', 'b', '(b)', 'Discuss two reasons why the attic space is chosen as the first area to be insulated.',
          [row('reason-1', 'Reason one', 5, 'Such as: the greatest heat loss, up to 30%, is through the roof; the most effective way to save energy.'),
           row('reason-2', 'Reason two', 5, 'A second, different reason. Such as: relatively easy for the home owner; lower bills, a better BER and a warmer house; the tank and pipes there must be insulated anyway.')],
          ['cons-6-3', 'cons-6-2'], ['heat-loss-insulation'], 'q2-reasons', 'Heat loss and running costs (6.3) with insulation (6.2).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b], 'q2-attic', B2, S2, parts(A2, B2b))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p19 (printed 16): (a) best 8 of 11 listed items × 4 = 32 and quality of sketch 8 (8/6/4) = 40; (b) solar pipework details 4; (c) two advantages × 3 = 6. Complete 50.'
S3 = 'The printed component list is required content, not a choice; the best-eight list is a marking menu.'
HEAT = (['cons-5-2', 'cons-5-3'], ['hot-water-space-heating'])
A3 = add('3', 'a', '(a)', 'Draw a large freehand sketch of the given diagram and also include the main cold water storage tank in the attic. Show the pipework required to connect the stove to the cylinder. Include the following on your sketch: rising main and the main cold water storage tank; hot water cylinder and expansion pipe; stove and pipework from stove to cylinder; all necessary valves.',
         [row('items', 'Any 8 of the above details (4 marks each)', 32, 'Credit the best EIGHT acceptable items at 4 marks each, capped at 32. Secondary circulation: 15 mm rising main; insulated storage tank; 22 mm cold feed to the cylinder; indirect cylinder; 22 mm expansion pipe. Primary circulation: wood burning stove; 28 mm primary flow and return; 22 mm cold supply and expansion pipe from the expansion tank; insulated expansion tank; overflows; valves.', list(range(0, 33, 4))),
          quality('the sketch', 'Quality of sketch (excellent, good, fair)')],
         *HEAT, 'q3-system', 'Hot water systems and cylinders (5.2) heated by a stove (5.3).', B3, S3)
B3b = add('3', 'b', '(b)', 'On the same sketch, show also the pipework necessary to connect the solar collector on the roof to the cylinder.',
          [row('solar', 'Valid details', 4, 'Such as: a solar controller; 22 mm flow from the panel to the cylinder and 22 mm return; a pump and isolator on the return; an expansion vessel and pressure release valve.')],
          ['cons-5-2', 'cons-6-4'], ['hot-water-space-heating', 'planning-sustainability-environment'], 'q3-solar', 'Hot water systems (5.2) heated by solar gain (6.4).', B3, S3)
C3 = add('3', 'c', '(c)', 'Discuss two advantages of including a solar collector to provide domestic hot water for a house.',
         [row('advantage-1', 'Advantage one', 3, 'Such as: lower energy bills for hot water; low running costs once installed.'),
          row('advantage-2', 'Advantage two', 3, 'A second, different advantage. Such as: less CO₂ from fossil fuels; an independent source of energy; helps slow climate change.')],
         ['cons-6-4', 'cons-6-3'], ['planning-sustainability-environment', 'heat-loss-insulation'], 'q3-advantages', 'Solar heat gain (6.4) and running costs (6.3).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-system', B3, S3, parts(A3, B3b, C3))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p20 (printed 17): (a) two reasons × 6 = 12; (b) site layout map three details × 5 = 15 and newspaper notice three details × 5 = 15 = 30; (c) one reason 8. Complete 50.'
S4 = 'Both printed planning documents in (b) are required, each separately marked; not a choice.'
PLAN = (['cons-1-3'], ['planning-sustainability-environment'])
A4 = add('4', 'a', '(a)', 'Discuss two reasons why it is necessary to apply for planning permission to build the sunspace shown.',
         [row('reason-1', 'Reason one', 6, 'Such as: a legal requirement when changing the front elevation of a house; it informs the public.'),
          row('reason-2', 'Reason two', 6, 'A second, different reason. Such as: it controls height, shape, design and location; prevents an unsafe sunspace; ensures it blends with its surroundings.')],
         *PLAN, 'q4-reasons', 'Planning permission (1.3).', B4, S4)
B4b = add('4', 'b', '(b)', 'State the information that must be contained in each of the following planning documents: site layout map; planning notice in newspaper.',
          [row('site-layout-map', 'Site layout map - Notes', 15, 'Three valid details, 5 each. Such as: what the site will look like when finished; the location of buildings and the new development; the septic tank and percolation area; the site notice position; north; a scale of 1:500.'),
           row('newspaper-notice', 'Planning notice in newspaper - Notes', 15, 'Three valid details, 5 each. Such as: the planning authority; the applicant’s name; the location or address; the type of permission; the nature and extent of the development; whether it is a protected structure; where and when the application can be viewed.')],
          *PLAN, 'q4-documents', 'Planning permission documents (1.3).', B4, S4)
C4 = add('4', 'c', '(c)', 'Discuss one reason why the planning authority allows the public to view all planning documents after a planning application is submitted.',
         [row('reason', 'Reason', 8, 'Such as: residents must be aware of developments in their environment; anyone can view the plans and object or make a submission; a legal requirement; the process is clear and transparent.')],
         *PLAN, 'q4-public', 'Planning permission (1.3).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-documents', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p21 (printed 18): (a) best 8 of 10 listed details × 5 = 40; (b) dowel or mortice and tenon joint 2, and draughting, accuracy and scale 8 (8/6/4) printed after it = 10. Complete 50.'
S5 = 'One required section and one required baluster detail. The best-eight detail list is a marking menu, not a printed choice.'
STAIRS = 'No Ordinary outgoing reference heading covers stairs (4.4); the card keeps the Foundations, Floors & Walls association.'
A5 = add('5', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the bottom three steps of the stairs. Show the cut string, newel post, handrail and balusters.',
         [row('details', 'Any 8 of the above details (5 marks each)', 40, 'Credit the best EIGHT acceptable details at 5 marks each, capped at 40. Marked details: newel post 100 × 100 mm; handrail; balusters 50 × 50 mm; treads 250 mm; nosing at least 16 mm; risers 175 mm; cut string; glue blocks; the tread–riser joint; the bottom three steps.', list(range(0, 41, 5)))],
         ['cons-1-5', 'cons-4-4'], ['question-one-drawing-questions', 'foundations-floors-walls'], 'q5-scheme', 'Scaled drawing (1.5) of a timber stairs (4.4).', B5, S5)
B5b = add('5', 'b', '(b)', 'On your drawing, show how one baluster is fitted securely to the thread.',
          [row('baluster', 'Dowel joint, mortice and tenon joint or equivalent', 2, 'Show and identify the joint, such as the baluster turned and fitted into the tread, a mortice and tenon, or a dowel, as in the scheme’s model detail.', [0, 2]),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the whole section: excellent 8, good 6, fair 4. The scheme prints this band after the part (b) row.', BAND8)],
          ['cons-4-4', 'cons-10-1'], ['foundations-floors-walls', 'wood-rot-ventilation'], 'q5-scheme', 'Stairs (4.4) and their joints (10.1).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-scheme', B5, S5, parts(A5, B5b))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p22 (printed 19): (a) three printed situations × two precautions × 4 = 24; (b) three precautions each with a reason × 6 and quality of sketches 8 (8/6/4) = 26. Complete 50.'
S6 = 'All three printed situations in (a) are required, each with two precautions and separately marked; not a choice.'
WORKSHOP = (['cons-9-4'], ['site-safety'])
A6 = add('6', 'a', '(a)', 'Outline two specific safety precautions to be observed in the Construction Studies room in each of the following situations: using a scalpel to cut modelling card; carrying a chisel; using a contact adhesive.',
         [row('scalpel', 'Using a scalpel to cut modelling card', 8, 'Two precautions, 4 each. Such as: a clean flat surface and cutting mat; a firmly held straight edge; always cut away from your hands; score lightly then repeat; cover scalpels and replace blunt blades.'),
          row('chisel', 'Carrying a chisel', 8, 'Two precautions, 4 each. Such as: carry it down by your side with the edge towards the floor; never in a pocket; walk, never run.'),
          row('adhesive', 'Using contact adhesives', 8, 'Two precautions, 4 each. Such as: latex gloves and goggles; a well-ventilated area; avoid inhaling the fumes; keep away from heat; follow the instructions for use and storage.')],
         *WORKSHOP, 'q6-precautions', 'Safety with tools in the workshop (9.4).', B6, S6)
B6b = add('6', 'b', '(b)', 'Using notes and freehand sketches, describe three specific safety precautions to be observed when turning a wooden bowl on a lathe, as shown. Give one reason for each safety precaution outlined.',
          [row('precaution-1', 'Precaution one and valid reason', 6, 'Precaution and reason. Such as: the work properly secured to the faceplate, or it may come loose.'),
           row('precaution-2', 'Precaution two and valid reason', 6, 'A second, different precaution and reason. Such as: rotate the piece by hand first so it clears the tool rest; set the correct speed, slow for big work.'),
           row('precaution-3', 'Precaution three and valid reason', 6, 'A third, different precaution and reason. Such as: a visor against flying chips; long hair and loose cuffs tied up; know how to stop the lathe; sound wood free of defects.'),
           quality()],
          *WORKSHOP, 'q6-lathe', 'Safety with machines in the workshop (9.4).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b], 'q6-lathe', B6, S6, parts(A6, B6b))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p23 (printed 20): (a) sketch — two valid details (2 × 3) = 12, quality 8 (8/6/4) — and notes — two valid details (2 × 2) = 8 = 28; (b) sound detail 4 and quality of sketch 8 (8/6/4) = 12; (c) two valid details × 5 = 10. Complete 50.'
S7 = '"one method" in (b) and (c) is an open choice; the scheme gives typical methods.'
A7 = add('7', 'a', '(a)', 'Using notes and freehand sketches show the typical construction details of the stud partition. Show clearly the studwork necessary to accommodate the doorframe. Indicate on your sketch the names and typical sizes of all components.',
         [row('sketch', 'Non-load bearing timber stud partition with a plaster board finish - Sketch', 12, 'Two valid details on the sketch, 2 × 3 each, as in the scheme’s model sketches of the studwork around the door opening.'),
          quality('the sketch', 'Quality of sketch (excellent, good, fair)'),
          row('notes', 'Non-load bearing timber stud partition with a plaster board finish - Notes', 8, 'Two valid details, 2 × 2 each. Such as: sole and head plates, studs and noggins 100 × 45 mm; door head and jambs to the opening 100 × 70 mm.')],
         ['cons-4-5'], ['windows-doors'], 'q7-partition', 'Stud partitions and internal doors (4.5).', B7, S7)
B7b = add('7', 'b', '(b)', 'On a separate annotated sketch, show one method that would help reduce the transmittance of sound through the stud partition.',
          [row('detail', 'Valid detail', 4, 'Such as: mineral wool or glass fibre quilt between the studs; two layers of plasterboard with staggered joints; acoustic board on battens; staggered studs; resilient channels and sealed gaps.'),
           quality('the sketch', 'Quality of sketch (excellent, good, fair)')],
          ['cons-8-3', 'cons-4-5'], ['sound', 'windows-doors'], 'q7-sound', 'Airborne sound insulation (8.3) of a stud partition (4.5).', B7, S7)
C7 = add('7', 'c', '(c)', 'Describe briefly one method of providing a surface finish to the plasterboard prior to painting.',
         [row('detail-1', 'Valid detail one', 5, 'Such as: boards screwed with all edges supported; scrim to internal corners; or joints and angles taped and filled.'),
          row('detail-2', 'Valid detail two', 5, 'A second, different step. Such as: a skim coat with a steel float for a smooth finish; or joint filler smoothed with a sponge; allowed to dry before painting.')],
         ['cons-4-1'], ['foundations-floors-walls'], 'q7-finish', 'Wall finishes (4.1).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-partition', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p24 (printed 21): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination. It keeps the pre-audit lever-valve ID; the other seven pre-audit per-term IDs alias to it (cob wall was never carded).'
TERMS = [
    ('lever-valve', 'lever valve', 'Lever valve', ['cons-5-2'], ['services-water-gas-electrical'],
     'controls the flow of water with a single lever operating a hollow ball; the lever shows the valve open when parallel to the pipe and closed when perpendicular; a good seal; various diameters.', 'Water systems and their valves (5.2).'),
    ('mortice-and-tenon-joint', 'mortice and tenon joint', 'Mortice and tenon joint', ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'],
     'used in doors, windows and furniture: a mortice cut in one piece and a tenon, about a third of the thickness, formed on the end of the other to fit it.',
     'Joints (10.1) and the choice of joint (10.4). The Ordinary reference taxonomy has no joinery heading; the term keeps the Wood, Rot & Ventilation association, and 10.1/10.4 are declared outside that heading’s crosswalk.'),
    ('cob-wall', 'cob wall', 'Cob wall', ['cons-3-3'], ['foundations-floors-walls'],
     'clay, straw or hemp mixed with water (sometimes lime or sand), built in layers on a coursed stone base, each layer dried before the next; tapered and finished with lime render.', 'External walls (3.3).'),
    ('thermal-bridge', 'thermal bridge', 'Thermal bridge', ['cons-6-2'], ['heat-loss-insulation'],
     'a bridge in the insulation, at floors, cills, lintels, jambs or roofs, conducting heat out; higher heat loss, condensation and mould; prevented by continuous insulation.', 'Thermal bridges (6.2).'),
    ('dual-flush-toilet', 'dual flush toilet', 'Dual flush toilet', ['cons-5-2'], ['services-water-gas-electrical'],
     'a cistern with two buttons: about 6–9 litres for solid and 3–4 litres for liquid waste, cutting water use and the water sent to treatment.', 'Cold water systems and cisterns (5.2).'),
    ('smart-meter', 'smart meter', 'Smart meter', ['cons-5-8'], ['services-water-gas-electrical'],
     'records and shows the electricity used in the home and its cost, giving the householder control; may be topped up; can also record water or gas.', 'Domestic electrical installation (5.8).'),
    ('solar-gain', 'solar gain', 'Solar gain', ['cons-6-4'], ['planning-sustainability-environment'],
     'free heat from solar radiation entering through glazing, stored in masonry as a heat sink; maximised by orientation, insulation and airtightness; the main principle of passive design.', 'Solar heat gain (6.4).'),
    ('low-e-glazing', 'low-e glazing', 'Low-e glazing', ['cons-3-6'], ['windows-doors'],
     'a thin transparent metal or metal-oxide coating on the panes that reflects heat back into the house while admitting solar gain; dearer but reduces heat loss.', 'Glass and glazing (3.6).'),
    ('access-ramp', 'access ramp', 'Access ramp', ['cons-1-2'], ['planning-sustainability-environment'],
     'a sloping path for easy access for wheelchairs, buggies and people with restricted mobility: gradient about 1:20, at least 1500 mm clear width, sections no longer than 9.0 m, non-slip and well lit.', 'Inclusive design of the built environment (1.2).'),
]
Q8 = add('8', 'None-lever-valve', '', 'Explain, with the aid of notes and freehand sketches, any five of the following: ' + '; '.join(t[1] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Terms', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{t[2]}: {t[5]}' for t in TERMS),
               group=dict(claimMax=5, perOption=10, options=[t[2] for t in TERMS]))],
         list(dict.fromkeys(n for t in TERMS for n in t[3])), list(dict.fromkeys(a for t in TERMS for a in t[4])), 'q8-terms',
         'The union of the nine printed terms: ' + ' '.join(t[6] for t in TERMS), B8, S8)

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p25 (printed 22): (a) wood 5 and two reasons × 5 = 15; (b) finish 4, three steps × 5 = 15 and quality of sketches 8 (8/6/4) = 27; (c) two features × 4 = 8. Complete 50.'
S9 = 'The wood, the finish and the features are open responses with no printed list.'
A9 = add('9', 'a', '(a)', 'Specify a suitable wood for the external cladding, and give two reasons for your choice of wood.',
         [row('wood', 'Choice of wood', 5, 'Such as: Western red cedar; larch; Douglas fir.'),
          row('reason-1', 'Valid reason one', 5, 'A reason matching the wood. Such as, cedar: durable and suitable for all weathers; larch: naturally durable outdoors and resistant to rot.'),
          row('reason-2', 'Valid reason two', 5, 'A second, different reason. Such as: a pleasant appearance; easy to cut and finish; lightweight; grown in Ireland.')],
         ['cons-3-2', 'cons-10-7'], ['foundations-floors-walls', 'wood-rot-ventilation'], 'q9-wood', 'External cladding (3.2) in a durable timber (10.7).', B9, S9)
B9b = add('9', 'b', '(b)', 'Recommend a suitable applied finish to preserve the external cladding. Using notes and freehand sketches, describe the steps involved in preparing the wood and in applying the recommended surface finish.',
          [row('finish', 'Suitable applied finish', 4, 'Such as: an oil-based varnish or stain; a water-based finish; deck or teak oil.'),
           row('steps', 'Steps involved in preparing the wood and in applying the recommended surface finish - Notes', 15, 'Three valid steps, 5 each. Such as: the surface sanded and cleaned, with white spirit or a damp cloth; the finish applied with a brush or cloth in two or three coats; dried and sanded between coats.'),
           quality()],
          ['cons-10-7'], ['wood-rot-ventilation'], 'q9-finish', 'Surface preparation and finishing of timber (10.7).', B9, S9)
C9 = add('9', 'c', '(c)', 'Discuss two features of the design that ensure the garden room is eco-friendly.',
         [row('feature-1', 'Design feature one', 4, 'Such as: renewable wood grown in Ireland for the walls and patio; a water butt collecting rainwater.'),
          row('feature-2', 'Design feature two', 4, 'A second, different feature. Such as: large glazing for solar gain with a roof overhang against overheating; a permeable surface around the room.')],
         ['cons-1-2', 'cons-6-4'], ['planning-sustainability-environment'], 'q9-eco', 'Sustainable design (1.2) with solar gain (6.4).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-finish', B9, S9, parts(A9, B9b, C9))

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and three other questions (200 marks); all question banks retained, no full-exam Cartesian cards.'),
          (3, 'any five', 'Q8 closed choose-five of nine printed terms: one card with an any-five group over all nine terms (choice is not a route).')]
FINITE = {'8': dict(choose=5, options=[t[0] for t in TERMS], cardId=Q8['id'], groupRowId='terms', wholeQuestionMarks=50, termMarks=10)}
REASONS = {
    'q1-a': 'Adds the four typical dimensions (4) printed within part (a): 36 → 40.',
    'q1-b': 'Adds the draughting, accuracy and scale band (8/6/4) the scheme prints after the part (b) row to the thermal-bridge detail: 2 → 10.',
    'q2-a': 'Rebuilt to the printed rows — attic 12, tank 12, pipes 8 and quality of sketches (8/6/4): 32 → 40.',
    'q2-b': 'Split into the two printed reasons (5 each); tariff unchanged (10).',
    'q3-a': 'Rebuilt to the best-eight items (4 each) and the printed quality-of-sketch band (8/6/4): 32 → 40.',
    'q3-b': 'Reshaped to the printed solar pipework row; tariff unchanged (4).',
    'q3-c': 'Split into the two printed advantages (3 each); tariff unchanged (6).',
    'q4-a': 'Split into the two printed reasons (6 each); tariff unchanged (12).',
    'q4-b': 'Reshaped to the two printed documents (three details × 5 each); tariff unchanged (30).',
    'q4-c': 'Reshaped to the printed reason row; tariff unchanged (8).',
    'q5-a': 'Reshaped to the best-eight details (5 each); tariff unchanged (40).',
    'q5-b': 'Adds the draughting, accuracy and scale band (8/6/4) the scheme prints after the part (b) row to the baluster joint: 2 → 10.',
    'q6-a': 'Reshaped to the three printed situations (two precautions × 4 each); tariff unchanged (24).',
    'q6-b': 'Adds the printed quality-of-sketches band (8/6/4) to the three precautions with reasons: 18 → 26.',
    'q7-a': 'Rebuilt to the printed rows — sketch details (2 × 3 each), quality (8/6/4) and notes (2 × 2 each): 6 → 28.',
    'q7-b': 'Adds the printed quality-of-sketch band (8/6/4) to the sound detail: 4 → 12.',
    'q7-c': 'Split into the two printed details (5 each); tariff unchanged (10).',
    'q9-a': 'Split into the printed wood (5) and two reasons (5 each); tariff unchanged (15).',
    'q9-c': 'Split into the two printed design features (4 each); tariff unchanged (8).',
    'q8-None-lever-valve': 'Now the whole of Question 8: one card printing all nine terms with an any-five group (10 each, 50), kept under this ID; the other seven pre-audit per-term IDs alias to it (choice is not a route): 10 → 50.',
}
CONSOLIDATED = {f'q8-None-{t[0]}': 'q8-None-lever-valve' for t in TERMS[1:] if t[0] != 'cob-wall'}
GAPS = [dict(cardId=A5['id'], canonicalTopicIds=['cons-4-4'], atlasTopicId=D.CROSS + 'foundations-floors-walls', reason=STAIRS),
        dict(cardId=B5b['id'], canonicalTopicIds=['cons-4-4', 'cons-10-1'], atlasTopicId=D.CROSS + 'foundations-floors-walls',
             reason='No Ordinary outgoing reference heading covers stairs (4.4) or joinery (10.1); the card keeps the Foundations, Floors & Walls and Wood, Rot & Ventilation associations.'),
        dict(cardId=C7['id'], canonicalTopicIds=['cons-4-1'], atlasTopicId=D.CROSS + 'foundations-floors-walls',
             reason='No Ordinary outgoing reference heading covers internal wall finishes (4.1); the card keeps the Foundations, Floors & Walls association.'),
        dict(cardId=Q8['id'], canonicalTopicIds=['cons-10-1', 'cons-10-4'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers joinery (10.1, 10.4, mortice and tenon joint).')]
D.finish(LEDGER, FINITE, REASONS, consolidated=CONSOLIDATED, taxonomy_gaps=GAPS, whole_choices={'q8-None-lever-valve'})
