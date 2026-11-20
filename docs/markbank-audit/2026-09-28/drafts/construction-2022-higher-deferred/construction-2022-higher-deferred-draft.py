"""Draft the 2022 Higher Level Construction Studies DEFERRED theory paper (LC029ALP000EV, deferred sitting), Q1-Q10 and the Q10 alternative.

Wording is lifted from the SEC deferred paper; every row's verbatim is printed in the deferred scheme's
mark tables (pages 29-39). The printed choices Q6(b), Q9(b) and Q10(a) (any two of three) are one card
each with an any-two group; the figures of Q9(b) and Q10(a) carry every item's scheme drawings (Q6(b)'s
items are answered in text only). Q2's printed items and activities are each their own task, composed
into their part; a Q2(c) activity, named only by reference to 2(b), carries the scheme's heading after
' — '. No pre-audit cards exist for this sitting. Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Suspended timber floor, external wall and window section', concept='suspended-floor-window-section',
              stem='A fixed frame triple-glazed wooden window is fitted in the external wall of a dwelling house, as shown. The external wall is a 450 mm concrete block wall with a full-fill insulated cavity. The wall is plastered on both sides. The bottom of the concrete cill is located 400 mm above finished floor level. The ground floor is an insulated suspended timber floor with 25 mm tongue-and-groove hardwood flooring. The wooden joists are 200 mm × 40 mm.',
              note='Original sketch and specification retained. Construction, dimension and scale/drafting marks belong to part (a); the ventilation detail in (b) is marked separately.'),
    '2': dict(page=2, title='Workers’ safety on a construction site', concept='workers-site-safety', stem='',
              note='Original question retained. All three printed items in (a) and all three printed activities in (b) and (c) are required, each separately marked. The scheme lists typical points, not an exhaustive list.'),
    '3': dict(page=3, title='A garden study connected to the house', concept='garden-study-space',
              stem='The drawing shows the ground floor plan of a two-storey, semi-detached house and a portion of the rear garden. Also shown is the location of a proposed single-storey space to be built in the rear garden of the house. The internal dimensions of the proposed space are 4.5 m × 3.0 m. The space is to be used as a study and also occasionally as a family space. The front wall A-A of the house is south facing. The occupants require that the new space: maximises the use of daylight; is structurally connected to the existing house; links with the surrounding rear garden.',
              note='Original plan retained. All three printed requirements are required in both the external design and the internal layout; the scheme’s elevations and plan are examples, not required designs.'),
    '4': dict(page=3, title='Stove: two-zone heating and hot water', concept='stove-two-zone-heating',
              stem='A stove, as shown, is to provide space heating and hot water for a two-storey dwelling house. The heating of each floor is to be independently controlled.',
              note='Original sketch retained. The scheme’s single-line diagram is one acceptable layout; its component list is a marking menu, not a printed choice.'),
    '5': dict(page=4, title='Tiled solid ground floor: U-value, Passive House insulation and heat-loss cost', concept='tiled-ground-floor-u-value',
              stem='A new house is to have a solid concrete ground floor with a ceramic tile finish, as shown.',
              note='All printed data are retained in the original question. Part (b) uses the U-value from (a) and part (c) the upgraded floor from (b); the scheme’s worked answers are U = 0.318 W/m²°C, 114 mm of additional insulation and an annual cost of €25.63.'),
    '6': dict(page=5, title='Low environmental impact house with stone and timber cladding', concept='low-impact-stone-timber-house',
              stem='The elevation and ground floor plan of a house are shown. The house has two bedrooms and a bathroom upstairs. The external walls are of concrete block construction with a stone and timber cladding finish. The house is designed to have low environmental impact.',
              note='Original elevation and plan retained. Part (b) chooses any two of three printed items, each keeping its own 10 marks.'),
    '7': dict(page=5, title='External door, wall and eaves section', concept='door-eaves-section',
              stem='A wooden door is fitted in the external wall of a dwelling house, as shown. The door has 15 mm vertical sheeting on both sides and is highly insulated. The doorframe is thermally broken and is 150 mm × 70 mm in cross-section. The external wall is a 450 mm concrete block wall with a full-fill insulated cavity. The wall is plastered on both sides. The tiled roof is constructed using prefabricated trussed rafters and has a pitch of 30⁰.',
              note='Original sketch and specification retained. Construction, tile-course and scale/drafting marks belong to part (a); the thermal-bridge detail in (b) is marked separately.'),
    '8': dict(page=6, title='External walls for a nearly Zero Energy Building', concept='nzeb-external-walls', stem='',
              note='Original sketch retained. The three walls in (b) are an open choice with no printed list; the scheme models five constructions.'),
    '9': dict(page=6, title='Preventing moisture penetration at the circled locations', concept='moisture-penetration-circled',
              stem='Careful design detailing is required to prevent the penetration of dampness into a dwelling house. The drawing below shows an outline section through a 450 mm external concrete block wall with a full-fill insulated cavity and a slated truss roof. A rendered concrete block chimney projects through the roof and the window frame is thermally broken.',
              note='Original section drawing retained. Part (b) chooses any two of the three circled locations, each keeping its own 14 marks.'),
    '10': dict(page=7, title='Passive House design, orientation and overheating', concept='passive-house-orientation-overheating', stem='',
               note='Original sketch retained. Part (a) chooses any two of three printed items, each keeping its own 10 marks.'),
}
ALT = dict(page=7, title='Embodied energy (alternative Question 10)', concept='embodied-energy-guidelines',
           stem='“The energy used in heating, lighting and in supplying power to a dwelling needs to be reduced, but the energy required to build it also must be addressed. This is the so-called embodied energy, the energy required to dig raw materials out of the ground and transport them to a factory where they are turned into metals or plastics. This embodied energy can account for up to 50% of the total energy consumed during the life of a low-energy-use home. It can be reduced substantially by using natural materials.” Adapted from: The Green Self-Build Book – how to design and build your own eco-home – by Jon Broome. Published by: Green Books Ltd. ISBN: 978 1 903998 73 1',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the Passive House question.')
SCHEME_PAGES = {'1': [4, 5, 29], '2': [6, 7, 8, 30], '3': [9, 10, 31], '4': [11, 32], '5': [12, 13, 33], '6': [14, 15, 34],
                '7': [16, 17, 35], '8': [18, 19, 20, 36], '9': [21, 22, 37], '10': [23, 24, 25, 26, 38], '10-alt': [26, 27, 39]}
HASHES = ('11b605087a6ee3d40ab3668af3003b8b97c740fe50ae3d188cdf984becb99356', 'e2d8850b5be78760d43044a95dee137e3b8250fd8fecd411c67355bbc5aa1ec3')
D = cp.Draft(HERE, 2022, 'higher', HASHES, 0, QUESTIONS, SCHEME_PAGES, alt=ALT, sitting='deferred')
row, add, compose, parts, anyn = D.row, D.add, D.compose, D.parts, D.anyn
Q10_PAGES = ((23, [51, 51, 545, 778]), (24, [51, 51, 545, 784]))
D.figures({
    'q1-original': D.paper(2, [45, 50, 580, 372]), 'q2-original': D.paper(2, [45, 440, 580, 730]),
    'q3-original': D.paper(3, [45, 50, 580, 386]), 'q4-original': D.paper(3, [45, 440, 580, 750]),
    'q5-original': D.paper(4, [45, 50, 580, 722]), 'q6-original': D.paper(5, [45, 50, 580, 405]),
    'q7-original': D.paper(5, [45, 470, 580, 760]), 'q8-original': D.paper(6, [45, 50, 580, 322]),
    'q9-original': D.paper(6, [45, 412, 580, 736]), 'q10-original': D.paper(7, [45, 50, 580, 388]),
    'q10-alt-original': D.paper(7, [45, 500, 580, 710]),
    'q1-section': D.composite((4, [51, 51, 545, 792]), (5, [51, 51, 545, 518])),
    'q1-ventilation': D.scheme(5, [51, 520, 545, 792]),
    'q2-procedures': D.scheme(8, [51, 51, 545, 768]),
    'q3-design': D.composite((9, [51, 51, 562, 768]), (10, [51, 51, 545, 290])),
    'q4-system': D.scheme(11, [51, 51, 553, 392]),
    'q5-u-value': D.scheme(12, [51, 51, 545, 380]), 'q5-thickness': D.scheme(12, [51, 404, 545, 645]),
    'q5-cost': D.scheme(13, [51, 51, 545, 606]),
    'q5-scheme': D.composite((12, [51, 51, 545, 645]), (13, [51, 51, 545, 606])),
    'q6-low-impact': D.scheme(14, [51, 51, 545, 566]),
    'q7-section': D.composite((16, [26, 51, 545, 732]), (17, [51, 51, 545, 284])),
    'q7-thermal-bridge': D.scheme(17, [51, 333, 545, 642]),
    'q8-requirements': D.scheme(18, [51, 51, 545, 780]),
    'q8-walls': D.composite((19, [51, 51, 545, 708]), (20, [51, 51, 545, 232])),
    'q9-locations': D.scheme(21, [51, 268, 560, 766]), 'q9-materials': D.scheme(22, [51, 51, 545, 656]),
    'q10-items': D.composite(*Q10_PAGES),
    'q10-orientation': D.scheme(25, [51, 51, 545, 400]),
    'q10-overheating': D.composite((25, [51, 422, 545, 672]), (26, [51, 51, 545, 426])),
    'q10-scheme': D.composite(*Q10_PAGES, (25, [51, 51, 545, 672]), (26, [51, 51, 545, 426])),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p29: (a) foundation and external wall 3 × 4, floor structure 5 × 4, window detail 3 × 4 (each 3 for drawing, 1 for annotation) = 44, three typical dimensions 3, scale 4 + drafting 4 banded excellent 8/good 6/fair 4 = 55; (b) ventilation design detail 5. Complete 60. The dimensions and the scale/drafting allowance assess the section drawn in (a), so they stay with (a).'
S1 = 'One required section and one required ventilation detail. The scheme detail lists are marking menus, not printed choices.'
T1A = 'To a scale of 1:5, draw a vertical section through the ground floor and window. Show the typical construction details from the bottom of the strip foundation, through the suspended timber floor and the external wall to a level 200 mm above the bottom frame of the window. Include three typical dimensions on your drawing.'
T1B = 'On your drawing, show clearly the ventilation to the suspended timber floor.'
A1 = add('1', 'a', '(a)', T1A,
         [row('foundation-wall', 'Foundation and external wall', 12, 'Best three details, 4 each (3 for drawing, 1 for annotation). Marking menu: R.C. foundation; blockwork below and above floor level; full-fill wall insulation and thermal blocks; external render and internal plaster; DPC. Typical sizes in the scheme’s model: R.C. strip foundation 1350 × 450 mm; 100 mm block leaves; 250 mm full-fill cavity with basalt-coated low-conductivity ties; 19 mm external render; 15 mm internal plaster.'),
          row('floor', 'Floor structure', 20, 'Best five details, 4 each (3 for drawing, 1 for annotation). Marking menu: compacted hardcore and sand blinding; radon barrier; R.C. concrete subfloor; dwarf walls; wallplate and DPC; ventilation pipe/cover/sealed; floor joists at 400 mm centres; airtight membrane and floor insulation; airtight membrane and tape to the floor perimeter; T + G flooring; skirting. Typical sizes: 150 mm subfloor; 100 mm dwarf walls; 100 × 75 mm wallplate; 200 × 40 mm joists; 200 mm floor insulation; 25 mm T + G flooring; Ø100 mm ventilation pipe.'),
          row('window', 'Window detail', 12, 'Best three details, 4 each (3 for drawing, 1 for annotation). Marking menu: concrete window cill; DPC wrapped around the cill; thermally broken window frame; window board; triple glazing; airtight tapes at the cill; vertical DPC.'),
          row('dimensions', 'Three typical dimensions', 3, 'Three typical dimensions shown on the drawing, 1 each.'),
          row('presentation', 'Scale 4 marks: Drafting 4 marks:', 8, 'Scale 4 and drafting 4, assessed together: excellent 8, good 6, fair 4.', [0, 4, 6, 8])],
         ['cons-1-5', 'cons-2-4', 'cons-4-3', 'cons-3-3', 'cons-3-6'], ['question-1-drawing-questions', 'foundations', 'floors', 'walls', 'windows-light'], 'q1-section',
         'Scaled drawing (1.5) from a strip foundation (2.4) through a suspended timber floor (4.3) and cavity wall (3.3) to the window cill (3.6).', B1, S1)
B1b = add('1', 'b', '(b)', T1B,
          [row('ventilation', 'Design detail to provide ventilation to suspended timber floor', 5, 'Show and identify the detail, as in the scheme’s model: a Ø100 mm vent pipe with a gasket through the external wall below the floor, laid to fall towards the outside.')],
          ['cons-4-3', 'cons-6-5'], ['floors', 'wood-rot-ventilation'], 'q1-ventilation', 'Ventilation (6.5) of a suspended timber floor (4.3).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p30: (a) three printed items × 5 (2 for point, 3 for discussion) = 15; (b) one risk for each of three printed activities × 3 = 9; (c) for each activity Safety procedure 1 and Safety procedure 2, each 3 for note + 3 for sketch = 12 per activity, 36. Complete 60.'
S2 = 'Parts (a), (b) and (c) require every printed item and activity, each separately priced, so each is its own task and the part composes them; not choices. Risks and procedures are open responses.'
T2A = 'Discuss in detail the importance of each of the following in relation to workers’ safety on a construction site: {items}.'
T2B = 'Identify one possible risk to personal safety on a construction site associated with each of the following: {items}.'
T2C = 'Using notes and freehand sketches, outline two safety procedures that should be observed to reduce each of the risks identified at 2(b) above.'
MISPRINT2C = (' A misprint in the scheme: its mark table heads part (c) “Three safety procedures”, but the paper asks for two procedures for '
              'each risk and the table itself prices two for each of the three activities (6 × 6 marks).')
ITEMS2A = [('safety-signage', 'safety signage', 'Safety signage: (2 for point: 3 for discussion)',
            'Point 2 and discussion 3. Such as: signage displayed prominently throughout the site; self-explanatory graphics; multilingual wording for workers with different native languages; warnings of falling objects, slippery surfaces, deep excavations, low objects and electrocution; colour-coded categories (green safe, red circle with a diagonal line prohibited, blue mandatory, yellow and black warning).'),
           ('personal-protective-equipment', 'personal protective equipment (PPE)', 'Personal Protective Equipment (PPE):(2 for point: 3 for discussion)',
            'Point 2 and discussion 3. Such as: PPE is required by law on site; hard hat, boots, high-visibility clothing, gloves, safety glasses, ear protection and harness; specific PPE for specialist and dangerous tasks; ear protection against noise above 80 dB that still lets workers hear speech; dust masks with filters; harnesses with quick-release D rings; making workers visible to machine operators and drivers; PPE for every visitor.'),
           ('awareness', 'awareness', 'Awareness: (2 for point: 3 for discussion)',
            'Point 2 and discussion 3. Such as: every worker must pass the national safety course (Safe Pass) before starting; full awareness of the possible hazards before work begins; an unaware worker puts everyone at risk; understanding of the hazards and general alertness is perhaps the best way to prevent accidents; enforcement of safe work practices; new workers paired with an experienced worker.')]
a2 = [add('2', f'a-{slug}', f'(a) — {item}', T2A.format(items=item), [row('importance', verbatim, 5, note)],
          ['cons-1-8'], ['site-safety'], None, 'Safety precautions on site (1.8).', B2, S2) for slug, item, verbatim, note in ITEMS2A]
A2 = compose('2', 'a', '(a)', a2, None, B2, S2, T2A.format(items='; '.join(i[1] for i in ITEMS2A)), labels=[i[2].split(':')[0] for i in ITEMS2A])
ACTIVITIES = [
    ('use-of-vehicles', 'use of vehicles', 'Use of vehicles',
     'One risk identified. Such as: a reversing vehicle knocking down a worker; a vehicle capsizing on uneven ground; the driver thrown from the vehicle or trapped underneath; electrocution from overhead cables; scaffolding knocked over, throwing off workers; driving into a poorly signposted excavation or collapsing its sides; burying someone while tipping a load.',
     'Note 3 and sketch 3. Such as: drivers who have completed the required safety training; vehicles operated only by trained, competent and authorised people.',
     'A second, different procedure: note 3 and sketch 3. Such as: signage throughout the site warning workers of machinery; seat belts worn in operation; sensors and horns that sound automatically when the vehicle is put in reverse.'),
    ('use-of-a-ladder', 'use of a ladder', 'Use of a ladder',
     'One risk identified. Such as: falling when three points of contact are not kept while climbing; the ladder sliding on metal; electrocution when a metal ladder touches overhead cables; the ladder falling when not secured; the ladder set at the wrong angle (it should be about 74°); the ladder not extending 1 metre above the platform.',
     'Note 3 and sketch 3. Such as: ladders used only by employees who have completed a ladder safety course; the ladder held or tied at both ends; a slope of 74°.',
     'A second, different procedure: note 3 and sketch 3. Such as: the ladder extending at least 1.0 metre above the platform; multiple ladder runs where the platform is more than one storey high; a structurally sound ladder designed for the loads; no overreaching.'),
    ('demolition-work', 'demolition work', 'Demolition work',
     'One risk identified. Such as: workers falling from structures being demolished; falling objects or materials injuring workers or a third party; walls collapsing unexpectedly; crushed limbs from falling masonry; inhaling dust from hazardous materials; machine operators trapped by collapsing walls or chimneys.',
     'Note 3 and sketch 3. Such as: signage around the area where demolition is taking place; warning or barrier tape marking a safe boundary around the site.',
     'A second, different procedure: note 3 and sketch 3. Such as: all services isolated or disconnected before demolition begins; hazardous materials disposed of appropriately.'),
]
b2, c2 = [], []
for slug, item, heading, risk, p1, p2 in ACTIVITIES:
    b2.append(add('2', f'b-{slug}', f'(b) — {item}', T2B.format(items=item), [row('risk', heading, 3, risk)],
                  ['cons-1-8'], ['site-safety'], None, 'Safety precautions on site (1.8).', B2, S2))
for slug, item, heading, risk, p1, p2 in ACTIVITIES:
    c2.append(add('2', f'c-{slug}', f'(c) — {item}', f'{T2C} — {heading}',
                  [row('procedure-1', 'Safety procedure 1 (3 for note, 3 for sketch)', 6, p1 + MISPRINT2C),
                   row('procedure-2', 'Safety procedure 2 (3 for note, 3 for sketch)', 6, p2)],
                  ['cons-1-8'], ['site-safety'], 'q2-procedures', 'Safety precautions on site (1.8).', B2, S2))
B2b = compose('2', 'b', '(b)', b2, None, B2, S2, T2B.format(items='; '.join(a[1] for a in ACTIVITIES)), labels=[a[2] for a in ACTIVITIES])
C2 = compose('2', 'c', '(c)', c2, 'q2-procedures', B2, S2, T2C, labels=[a[2] for a in ACTIVITIES])
compose('2', 'complete', ' — complete', [A2, B2b, *c2], 'q2-procedures', B2, S2,
        parts(('a', T2A.format(items='; '.join(i[1] for i in ITEMS2A))), ('b', T2B.format(items='; '.join(a[1] for a in ACTIVITIES))), ('c', T2C)),
        labels=['(a)', '(b)'] + [f'(c) {a[1]}' for a in ACTIVITIES])

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p31: (a) external design notes 6 + sketches 12, internal design notes 6 + sketches 12 = 36, each design considering the use of daylight, the structural connection and the link to the garden; (b) three requirements × 8 = 24. Complete 60.'
S3 = 'The three printed requirements are all required, in one external design and one internal layout in (a) and in the reasons in (b); not a choice. Designs and reasons are open responses.'
T3A = 'Using notes and freehand sketches, show a proposed external design and an internal layout for the space that will meet each of the occupants’ requirements outlined above.'
T3B = 'For each of the requirements above, discuss in detail the reasons for your proposed design choices.'
A3 = add('3', 'a', '(a)', T3A,
         [row('external', 'External design', 18, 'Notes 6 and sketches 12. The design considers the use of daylight, the structural connection and the link to the garden. Such as: large areas of high-performance glazing on the south and east elevations, with a sliding glass door and floor-to-ceiling glazing; small windows on the north and west for views of the garden; a flat zinc roof sloping from south to north over the 3.0 m span; cedar or larch cladding, or smooth render to match the house; a canopy and a timber deck or footpath linking the house to the study.'),
          row('internal', 'Internal design', 18, 'Notes 6 and sketches 12. Such as, as in the scheme’s model plan: the study desk in the south-west corner for daylight; a circular table for ease of movement; a single couch beside the desk for a companion; furniture against the external walls to leave open space; glazing that brings the garden into the room.')],
         ['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'], 'q3-design',
         'Design of a garden room within the built environment (1.2) for good daylighting (7.4).', B3, S3)
B3b = add('3', 'b', '(b)', T3B,
          [row('daylight', 'Maximise the use of daylight', 8, 'Reasons for the choices that maximise daylight. Such as: a large south-facing glazed façade for maximum solar gain; glazing on the east, south and west for morning, afternoon and evening sun; the health benefits of natural light; less need for artificial lighting; solar shading to admit winter gains and prevent summer overheating; low cills; rooflights or sun tunnels.'),
           row('connection', 'Structural connection to existing house', 8, 'Reasons for the structural connection. Such as: a roof or canopy from the house to the study gives shelter from rain; a footpath or decking gives easy access when the ground is wet; locally sourced materials reduce embodied energy; cedar or larch cladding is attractive, durable and low-maintenance; smooth render matches the house.'),
           row('garden', 'Link to surrounding garden', 8, 'Reasons for the link to the garden. Such as: windows and doors opening onto the garden; fresh air and the smells of the garden; a visual connection to nature through the glazing (biophilic design); planting chosen for biodiversity and colour; the large sliding glass door.')],
          ['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'], None,
          'Design of a garden room within the built environment (1.2) for good daylighting (7.4).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-design', B3, S3, parts(('a', T3A), ('b', T3B)))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p32: (a) any eight components × 4 (3 sketch, 1 annotation) = 32 + typical sizes of pipework (any two) 4 = 36; (b) two advantages × (3 for point + 3 for discussion) = 12; (c) two considerations × (3 + 3) = 12. Complete 60.'
S4 = 'No printed choice. The component list in (a) is a marking menu (best eight); the radiators and control valves the paper asks for are items on it.'
T4A = 'Using notes and a single-line diagram, show a typical design layout for the pipework necessary to independently heat two zones, one on each floor, and to provide hot water. Show three radiators on each floor, indicate the location of the control valves and give the typical sizes of the pipework.'
T4B = 'Many homeowners are choosing to replace open fires with stoves. Discuss two advantages of replacing an open fire with a stove.'
T4C = 'Discuss two considerations that should be taken into account when selecting a stove to provide space heating and hot water for a house.'
A4 = add('4', 'a', '(a)', T4A,
         [row('layout', 'Typical layout for the pipework necessary to provide space heating and hot water for a two-storey house', 32, 'Best eight components, 4 each (3 for sketch, 1 for annotation). Marking menu: woodburning stove; radiators on the ground floor and first floor; zone control panel; zone thermostats; cylinder and coil; header/expansion tank/storage; feed to the expansion tank; cold feed from the expansion tank and overflow; expansion pipe or vessel; flow pipe to the radiators; return pipe from the radiators; control valves (radiator, isolating or drain-off valves, any two); pump.'),
          row('sizes', 'Typical sizes of pipework – any two', 4, 'Any two, 2 each. Such as: Ø15 mm cold water rising main; Ø15 mm on upstands; Ø22 mm primary flow and return to the radiators; Ø22 mm cold water feed to the cylinder; Ø28 mm hot water feed; Ø28 mm overflow pipe.')],
         ['cons-5-3', 'cons-5-2'], ['hot-water-space-heating'], 'q4-system', 'Zoned space heating (5.3) and hot water (5.2) from a stove.', B4, S4)
B4b = add('4', 'b', '(b)', T4B,
          [row('advantage-1', 'Advantage 1 (3 for point, 3 for discussion)', 6, 'Point 3 and discussion 3. Such as: an open fire is less efficient, as heat escapes up the open flue; an open flue lets cold air in and warm air out, while a stove is a sealed unit whose airtight door stops the cold air and limits heat loss; a modern stove takes its air through a vent pipe in the floor or external wall.'),
           row('advantage-2', 'Advantage 2 (3 for point, 3 for discussion)', 6, 'A second, different advantage. Such as: a cast-iron stove stores heat and releases it to the room; cheaper space and water heating; insulated modern stoves reduce the risk of burns to children; far less CO2 and SO2 released than from an open fireplace.')],
          ['cons-5-7', 'cons-5-3'], ['fireplaces-fire-prevention', 'hot-water-space-heating'], None, 'Fireplaces and stoves (5.7) for heating (5.3).', B4, S4)
C4 = add('4', 'c', '(c)', T4C,
         [row('consideration-1', 'Consideration 1 (3 for point, 3 for discussion)', 6, 'Point 3 and discussion 3. Such as: the output of the stove, whether it will meet the heating and hot water needs of the house; whether it will fit in the required location; its position, ideally within the house structure for efficiency.'),
          row('consideration-2', 'Consideration 2 (3 for point, 3 for discussion)', 6, 'A second, different consideration. Such as: fitting to an existing chimney or installing a new steel flue; compliance with the building regulations; an independent air supply to the stove; additional pipework.')],
         ['cons-5-3', 'cons-5-7'], ['hot-water-space-heating', 'fireplaces-fire-prevention'], None, 'Choosing a stove (5.7) for heating and hot water (5.3).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-system', B4, S4, parts(('a', T4A), ('b', T4B), ('c', T4C)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p33: (a) eight resistances, total resistance and U-value, 10 × 3 = 30; (b) five steps × 3 = 15; (c) five steps × 3 = 15. Complete 60.'
S5 = 'No printed choice. Part (b) uses the U-value from (a); part (c) uses the upgraded floor from (b).'
DATA5 = ('Ceramic tile thickness 12 mm; concrete floor slab thickness 150 mm; floor insulation thickness 50 mm; radon barrier thickness 0.25 mm; sand blinding thickness 50 mm; hardcore thickness 175 mm; subsoil thickness 300 mm.\n'
         'Thermal data of the ground floor: resistance of internal top surface of floor (R) 0.104 m2 ⁰C/W; resistivity of ceramic tiles (r) 0.770 m ⁰C/W; '
         'conductivity of concrete floor slab (k) 1.180 W/m ⁰C; conductivity of floor insulation (k) 0.022 W/m ⁰C; conductivity of radon barrier (k) 0.250 W/m ⁰C; '
         'conductivity of sand blinding (k) 0.160 W/m ⁰C; conductivity of hardcore (k) 1.350 W/m ⁰C; conductivity of subsoil (k) 1.600 W/m ⁰C.')
T5A = 'Calculate the U-value of the floor, given the construction has the following sequence and data: ' + DATA5
T5B = 'It is proposed to redesign the above floor and upgrade its thermal properties to meet the Passive House standard by including additional insulation in the design of the floor. Calculate the thickness of additional insulation required to achieve a U-value of 0.12 W/m2 ⁰C.'
T5C = ('Calculate the cost of heat loss annually through the upgraded floor at 5(b) above, using the following data: dimensions of the floor slab 10.5 metres × 7.0 metres; '
       'average internal temperature 21 ⁰C; average temperature of subsoil 6 ⁰C; heating period 8 hours daily for 37 weeks per annum; cost of oil 97 cent per litre; '
       'calorific value of oil 37350 kJ per litre; 1000 Watts 1 kJ per second.')
A5 = add('5', 'a', '(a)', T5A,
         [row('resistances', 'Internal surface resistance Ceramic tile Concrete floor slab Floor insulation Radon barrier Sand blinding Hardcore Subsoil', 24,
              'Eight resistances, 3 each, by R = T/k (or R = T × r for the tiles): internal surface 0.104 (given); ceramic tiles 0.012 × 0.770 = 0.009; concrete floor slab 0.150/1.180 = 0.127; floor insulation 0.050/0.022 = 2.273; radon barrier 0.00025/0.250 = 0.001; sand blinding 0.050/0.160 = 0.313; hardcore 0.175/1.350 = 0.130; subsoil 0.300/1.600 = 0.188. All in m²°C/W.',
              list(range(0, 25, 3))),
          row('total-resistance', 'Total resistance', 3, 'Total resistance Rt = 3.145 m²°C/W (the sum of all the resistances).', [0, 3]),
          row('u-value', 'Calculation of U-value (W/m2 °C or W/m2K)', 3, 'U = 1 ÷ Rt = 1 ÷ 3.145 = 0.318 W/m²°C, with units.', [0, 3])],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-u-value', 'Thermal resistance, conductivity and transmittance (6.1).', B5, S5)
B5b = add('5', 'b', '(b)', T5B,
          [row('required-resistance', 'Resistance for U- value for 0.12 W/m2 °C (using R=1/U)', 3, 'Required resistance = 1 ÷ 0.12 = 8.333 m²K/W.'),
           row('existing-resistance', 'Resistance from calculated U-value from part (a)', 3, 'Resistance of the floor from (a): R = 1 ÷ 0.318, printed in the scheme as 3.144 m²K/W.'),
           row('difference', 'Difference in resistances (required resistance)', 3, 'Difference = 8.333 − 3.144 = 5.190 m²K/W, as the scheme prints it. A misprint in the scheme: 8.333 − 3.144 is 5.189, and 1 ÷ 0.318 rounds to 3.145 (the total resistance in (a)), not 3.144; neither slip changes the answer, 0.114 m.'),
           row('formula', 'Application of formula R = T/k', 3, '5.190 = T ÷ 0.022, so T = 5.190 × 0.022 = 0.114 metres.'),
           row('thickness', 'Required thickness of insulation (mm)', 3, 'Additional floor insulation = 114/115 mm. Alternative calculation methods are acceptable.')],
          ['cons-6-1', 'cons-6-2', 'cons-4-2'], ['heat-u-value-calculations', 'heat-loss-insulation', 'floors'], 'q5-thickness',
          'Thermal resistance (6.1) of added insulation (6.2) in a solid ground floor (4.2).', B5, S5)
C5 = add('5', 'c', '(c)', T5C,
         [row('heat-loss', 'Heat loss formula and calculations', 3, 'Heat loss = U-value × area × temperature difference = 0.12 × 73.5 × (21 − 6) = 132.3 watts (joules per second), using the upgraded U-value of 0.12 W/m²°C and a floor area of 10.5 × 7.0 = 73.5 m².'),
          row('duration', 'Heating duration for one year & calculation', 3, 'Heating period = 60 × 60 × 8 × 7 × 37 = 7,459,200 seconds (2,072 hours).'),
          row('energy', 'K/Joules calculation for one year & calculation', 3, 'Energy = 7,459,200 × 132.3 ÷ 1000 = 986,852 kJ per year.'),
          row('oil', 'Litres of oil for one year: & calculation', 3, 'Oil = 986,852 ÷ 37,350 = 26.422 litres per year.'),
          row('cost', 'Annual cost of heat loss: & calculation', 3, 'Annual cost = 26.4222 × €0.97 = €25.63. The scheme’s alternative one-line method gives the same €25.63. A misprint in the scheme: its answer line reads “Cost of heat loss annually through wall”; the question is about the upgraded floor.')],
         ['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations'], 'q5-cost', 'Heat loss calculation and running costs (6.3) from the U-value (6.1).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-scheme', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p34: (a) three features × (notes 5 + sketches 5) = 30; (b) any two of three printed items × (notes 5 + sketches 5) = 20; (c) two advantages × (2 for point + 3 for discussion) = 10. Complete 60.'
S6 = 'Choice is not a route: part (b) (any two of three printed items) is ONE card with an any-two group over the scheme headings. The scheme answers the three items in text only, so the card carries no drawing.'
T6A = 'With reference to the design shown, discuss using notes and freehand sketches, three features of the design that contribute to the house having a low environmental impact.'
T6B = 'Using notes and freehand sketches, discuss the importance of any two of the following when designing a house to have low environmental impact: flexibility of design; use of recycled materials; thermal efficiency.'
T6C = 'Discuss two advantages of using locally sourced materials when building the house shown.'
A6 = add('6', 'a', '(a)', T6A,
         [row(f'feature-{i}', f'Design Feature {i}', 10, note) for i, note in [
             (1, 'Notes 5 and sketches 5. Such as: large south-facing glazed windows and doors for solar gain, cutting heating costs and dependence on fossil fuels; a single small window on the north elevation to limit heat loss.'),
             (2, 'A second, different feature: notes 5 and sketches 5. Such as: a wood-burning stove, carbon neutral, more efficient and free of the draughts of an open fire; high thermal mass in a super-insulated external wall; timber cladding, low in embodied energy and carbon neutral.'),
             (3, 'A third, different feature: notes 5 and sketches 5. Such as: attic space used for living without extra building products; a small footprint using fewer resources and less embodied energy; single-room depth for solar gain; an open-plan kitchen, dining and living area that lets the sun’s heat pass through.')]],
         ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-low-impact',
         'Low-impact design of the built environment (1.2), solar gain (6.4) and insulation (6.2).', B6, S6)
ITEMS6 = [('Flexibility of design', 'homes adapt as occupants age without major renovation or structural change; cradle-to-grave design; the study can become a bedroom simply by removing the office furniture, near the ground-floor bathroom.'),
          ('Use of recycled materials', 'materials chosen for their potential to be recycled or upcycled later; products made from recycled materials; crushed concrete reused as hardcore; locally sourced rubble stone for boundary walls.'),
          ('Thermal efficiency', 'much lower heating and running costs over the long term, quickly repaying a higher capital cost; less harm to the planet; less demand for finite fossil fuels and fewer CO2 and SO2 emissions.')]
A6b = add('6', 'b', '(b)', T6B,
          [anyn('items', 'Discuss the importance of any two in the design a low E.I. house', 2, 10, ITEMS6, 'Any two of the three, each notes 5 and sketches 5 = 10.')],
          ['cons-1-2', 'cons-6-2'], ['sustainability-the-environment'], None,
          'The union of the three printed items: flexible design and recycled materials in the built environment (1.2) and thermal efficiency (6.2).', B6, S6)
C6 = add('6', 'c', '(c)', T6C,
         [row(f'advantage-{i}', f'Advantage {i} (2 for point, 3 for discussion)', 5, note) for i, note in [
             (1, 'Point 2 and discussion 3. Such as: lower embodied energy in the house; lower transport costs.'),
             (2, 'A second, different advantage. Such as: locally sourced timber is low in embodied energy and carbon neutral; buying locally sustains the local economy; stone from the local quarry links the house with other dwellings in the area.')]],
         ['cons-1-2'], ['sustainability-the-environment'], None, 'Sustainable materials in the built environment (1.2).', B6, S6)
compose('6', 'complete', ' — complete', [A6, A6b, C6], 'q6-low-impact', B6, S6, parts(('a', T6A), ('b', T6B), ('c', T6C)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p35: (a) external wall 3 × 5, doorframe and door 3 × 5, roof eaves 3 × 5 (each 4 for drawing, 1 for annotation) = 45, three courses of tiles 3, scale and drafting banded excellent 8/good 6/fair 4 = 56; (b) design details 4. Complete 60.'
S7 = 'One required section and one required thermal-bridge detail. The detail lists are marking menus, not printed choices.'
T7A = 'To a scale of 1:5, draw a vertical section through the external wall, doorframe, door and eaves of the roof. Show the typical construction details from a level 200 mm below the head of the door, through the eaves and include three courses of tiles at eaves.'
T7B = 'On your drawing, show the typical design detailing to prevent the formation of a thermal bridge at the head of the door.'
A7 = add('7', 'a', '(a)', T7A,
         [row('external-wall', 'External Wall', 15, 'Best three details, 5 each (4 for drawing, 1 for annotation). Marking menu: internal and external plaster/render; 450 mm concrete block wall and basalt-coated wall ties; full-fill insulated cavity; stepped DPC; cavity closer; lintels; wall plate; airtightness tape at the junction of wall and ceiling. Typical sizes in the scheme’s model: 18 mm render; 100 mm block leaves; 250 mm cavity; 15 mm plaster; 100 × 75 mm wallplate.'),
          row('door', 'External Door & Frame', 15, 'Best three details, 5 each (4 for drawing, 1 for annotation). Marking menu: thermally broken door frame; top rail of the door; airtightness tape from doorframe to wall; insulation; 15 mm vertical sheeting on both sides; double rebates with draught-proofing strips.'),
          row('eaves', 'Roof eaves', 15, 'Best three details, 5 each (4 for drawing, 1 for annotation). Marking menu: fascia, soffit and gutter (any two); ventilation at the soffit and a ventilation path to the roof; tilting fillet; breather membrane and 40 × 40 mm battens; prefabricated roof trusses; ceiling insulation; gypsum plasterboard ceiling with a vapour/airtightness barrier.'),
          row('tiles', '3 courses of tiles at the eaves', 3, 'Three courses of tiles drawn at the eaves.'),
          row('presentation', 'Scale and drafting marks (Excellent, Good, Fair)', 8, 'Scale and drafting, assessed together: excellent 8, good 6, fair 4.', [0, 4, 6, 8])],
         ['cons-1-5', 'cons-3-7', 'cons-3-3', 'cons-3-4', 'cons-3-10', 'cons-3-8'], ['question-1-drawing-questions', 'doors', 'walls', 'roofs'], 'q7-section',
         'Scaled drawing (1.5) of an external door (3.7) in a cavity wall (3.3) with its lintels and DPC (3.4), up to the eaves (3.10) of a trussed roof (3.8).', B7, S7)
B7b = add('7', 'b', '(b)', T7B,
          [row('thermal-bridge', 'Design detailing to prevent formation of a thermal bridge @ head of door', 4, 'Show and identify the detail, as in the scheme’s model: a thermally broken door frame and high-density insulation used as a cavity closer at the head of the door.')],
          ['cons-6-2', 'cons-3-7', 'cons-3-4'], ['heat-loss-insulation', 'doors', 'walls'], 'q7-thermal-bridge',
          'A thermal bridge (6.2) at the head of a door (3.7) and its lintel (3.4).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p36: (a) three requirements × (notes 4 + sketches 4) = 24; (b) three walls × (notes 4 + sketches 4 + dimensions 2) = 30; (c) recommendation 2 + justification 4 = 6. Complete 60.'
S8 = '"Three different external wall constructions" is an open choice with no printed list; each part stays one response. The scheme models five constructions.'
T8A = 'Discuss, using notes and freehand sketches, three functional requirements of an external wall suitable for a new dwelling house.'
T8B = 'The owners of the house design shown, intend to construct the dwelling to meet the nearly Zero Energy Building (nZEB) standard. Using notes and freehand sketches, show the design detailing for three different external wall constructions suitable to meet the nZEB standard. Name the typical components of each wall and include the typical dimensions.'
T8C = 'Recommend your preferred external wall construction from 8(b) above and justify your recommendation.'
A8 = add('8', 'a', '(a)', T8A,
         [row(f'requirement-{i}', f'Functional Requirement {i}', 8, note) for i, note in [
             (1, 'Notes 4 and sketches 4. Such as: weather resistance, sheltering the occupants from rain, snow, wind and sun with little maintenance; structural stability, carrying the loads of the roof and upper floors, spreading them evenly over the foundation and anchoring the roof.'),
             (2, 'A second, different requirement: notes 4 and sketches 4. Such as: airtightness, an airtightness barrier (sand-cement plaster taped at junctions, or a membrane in a service cavity) preventing uncontrolled air flow; sustainability, durable, long-lasting materials of low embodied energy.'),
             (3, 'A third, different requirement: notes 4 and sketches 4. Such as: thermal comfort, with maximum insulation, minimal thermal bridges and high thermal mass; sound resistance against external noise; fire resistance, resisting the spread of fire and keeping its load-bearing capacity for at least 30 minutes.')]],
         ['cons-3-2', 'cons-3-3'], ['walls'], 'q8-requirements', 'Functions of the external envelope (3.2) and external walls (3.3).', B8, S8)
B8b = add('8', 'b', '(b)', T8B,
          [row(f'wall-{i}', f'External Wall Construction {i}', 10, note) for i, note in [
              (1, 'Notes 4, sketches 4 and dimensions 2 for one wall. Such as, concrete block cavity: durable external render; robust concrete blocks; a full-fill insulated cavity that also keeps moisture from the inner leaf; sand-cement plaster on the inner leaf for airtightness.'),
              (2, 'Notes 4, sketches 4 and dimensions 2 for a second, different wall. Such as, timber frame with a concrete block external leaf: a ventilated cavity, not filled, against wind-driven rain; a breather membrane on the racking board on the cavity side; an airtightness membrane on the warm side of the studs. Or a single-leaf timber frame wall: full-fill insulation between the studs; a cedar or larch rainscreen on counter battens, or external insulation with acrylic render; an airtightness membrane or a service cavity.'),
              (3, 'Notes 4, sketches 4 and dimensions 2 for a third, different wall. Such as, a single-leaf concrete block wall (blocks on the flat) with expanded polystyrene external insulation fixed by adhesive and mechanical fixings and finished in acrylic plaster, made airtight with sand-cement plaster or a service cavity; or insulated concrete forms (ICF): EPS panels joined by polypropylene webs and filled with steel-reinforced concrete, acrylic plaster outside and insulated plasterboard inside.')]],
          ['cons-3-3', 'cons-6-2'], ['walls', 'heat-loss-insulation'], 'q8-walls', 'External wall constructions (3.3) insulated to the nZEB standard (6.2).', B8, S8)
C8 = add('8', 'c', '(c)', T8C,
         [row('recommendation', 'Recommendation', 2, 'The preferred wall from 8(b) named.'),
          row('justification', 'Justification', 4, 'Such as, a concrete block cavity wall: robust, long-lasting materials, a durable weatherproof outer leaf, airtight with sand-cement plaster or a service cavity membrane, and familiar to builders. Timber frame: low embodied energy, built in a factory or on site, a carbon store. Blocks with external insulation: high thermal mass. ICF: quick to build, a low U-value, very airtight, acoustic comfort.')],
         ['cons-3-3', 'cons-1-2'], ['walls', 'sustainability-the-environment'], None, 'Choosing an external wall (3.3) for a sustainable building (1.2).', B8, S8)
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-walls', B8, S8, parts(('a', T8A), ('b', T8B), ('c', T8C)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p37: (a) two reasons × (4 for point + 4 for discussion) = 16; (b) any two of the three circled locations × (note 4 + sketch 10) = 28; (c) two materials × (note 4 + sketch 4) = 16. Complete 60.'
S9 = 'Choice is not a route: part (b) (any two of the three circled locations) is ONE card with an any-two group over the scheme headings; its figure carries all three locations’ drawings.'
T9A = 'Discuss two reasons why it is important to ensure that moisture does not penetrate into a house.'
T9B = 'Using notes and freehand sketches, show best practice design detailing that will prevent the penetration of moisture at any two locations circled on the drawing.'
T9C = 'Describe, using notes and freehand sketches, two different materials that are used to prevent the penetration of moisture into the house at the locations circled.'
A9 = add('9', 'a', '(a)', T9A,
         [row(f'reason-{i}', f'Reason {i} (4 for point, 4 for discussion)', 8, note) for i, note in [
             (1, 'Point 4 and discussion 4. Such as: health, mould growth on internal walls harming the occupants; structural stability, timber roof members rotting over time; thermal comfort, damp insulation between the joists working less well.'),
             (2, 'A second, different reason. Such as: appearance, with mould, discoloured walls, bubbling paint and rusting metal; the cost of replacing wooden doors, windows or flooring that swell and warp; higher energy bills, as damp air takes more energy to heat or cool.')]],
         ['cons-3-4', 'cons-3-3'], ['walls'], None, 'Keeping dampness out of the external walls (3.3) with damp proofing (3.4).', B9, S9)
ITEMS9 = [('Back of chimney', 'a lead back gutter welted over a tilting fillet and under the breather membrane; the breather membrane or roofing felt carried under the back gutter and lapped up the chimney; a lead cover flashing overhanging the gutter.'),
          ('Front of chimney', 'the breather membrane carried under the battens and taped to the chimney; a lead front apron flashing dressed on top of the slates and covered by the lead above; the lead carried 150 mm above the lowest point where the stack leaves the roof.'),
          ('Head of Window', 'a stepped DPC so moisture does not reach the inner wall; the window frame sealed with mastic so wind-driven rain cannot reach the internal leaf.')]
A9b = add('9', 'b', '(b)', T9B,
          [anyn('locations', 'Preventing moisture penetration at two locations', 2, 14, ITEMS9, 'Any two of the three circled locations, each note 4 and sketch 10 = 14.')],
          ['cons-3-4', 'cons-5-7', 'cons-3-10', 'cons-3-6'], ['walls', 'fireplaces-fire-prevention', 'roofs', 'windows-light'], 'q9-locations',
          'The union of the three circled locations: flashings and gutters where a chimney (5.7) meets the roof (3.10), and the DPC (3.4) at a window head (3.6).', B9, S9)
C9 = add('9', 'c', '(c)', T9C,
         [row(f'material-{i}', f'Material {i}', 8, note) for i, note in [
             (1, 'Note 4 and sketch 4. Such as: lead, malleable, durable and resistant to corrosion, used for flashings, valleys and gutters; a damp proof course (DPC), impervious, flexible, lightweight and embossed to bond with the mortar.'),
             (2, 'A second, different material: note 4 and sketch 4. Such as: a breather membrane or roofing felt, water-resistant but vapour-permeable, fixed under battens outside the insulation; slate (natural or fibre cement), nailed to battens through two holes and shedding water to the gutter.')]],
         ['cons-3-4', 'cons-3-9'], ['walls', 'roofs'], 'q9-materials', 'Damp proof courses and flashings (3.4) and roof coverings and membranes (3.9).', B9, S9)
compose('9', 'complete', ' — complete', [A9, A9b, C9], 'q9-locations', B9, S9, parts(('a', T9A), ('b', T9B), ('c', T9C)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p38: (a) any two of three printed items × (notes 5 + sketches 5) = 20; (b) preferred orientation notes 5 + sketch 5, sun path 5, justification 5 = 20; (c) two reasons × 5 and one modification notes 5 + sketches 5 = 20. Complete 60.'
S10 = 'Choice is not a route: part (a) (any two of three printed items) is ONE card with an any-two group over the scheme headings; its figure and the complete-question figure carry all three items’ drawings. The OR alternative is a separate Question 10 route.'
T10A = 'Using notes and freehand sketches, discuss the importance of any two of the following in Passive House design: building form; continuity of insulation; windows and glazing.'
T10B = 'The preliminary design sketch for a Passive House is shown. Using notes and freehand sketches, show the preferred orientation to ensure the optimum thermal performance of the house and also show the sun path on your sketch. Justify your choice of orientation.'
T10C = 'The passive house as shown in the design above may overheat during summer. Discuss two reasons why overheating may occur. Show, using notes and freehand sketches, one modification you would make to this design to reduce the possibility of overheating.'
ITEMS10 = [('Building form', 'a simple, compact form, not oversized for its site; the smallest surface area for the volume (an A/V ratio of 0.7 or less) to cut heat loss, materials and labour; single-room depth for solar gain; T, L or U plans use more material than a rectangle.'),
           ('Continuity of insulation', 'unbroken insulation so heat cannot escape through the envelope: 200-300 mm under the whole floor slab; 50-100 mm edge insulation; cavity insulation carried below the slab; thermal blocks on the inner leaf; passive raft foundations wrapped in insulation; the eaves junction; thermally broken window and door frames.'),
           ('Windows and glazing', 'thermally broken high-performance frames with double or triple rebated, sealed sashes; window U-values of 0.8 to 0.47 W/m²K (double glazing 2.8 to 2.0); argon or krypton gas between the panes; low-e soft coats; warm edge spacers; dynamic or thermochromic glass.')]
A10 = add('10', 'a', '(a)', T10A,
          [anyn('items', 'Any two in Passive House design', 2, 10, ITEMS10, 'Any two of the three, each notes 5 and sketches 5 = 10.')],
          ['cons-6-4', 'cons-6-2', 'cons-3-6'], ['passive-design', 'heat-loss-insulation', 'windows-light'], 'q10-items',
          'The union of the three printed items: compact passive form (6.4), continuous insulation (6.2) and high-performance windows and glazing (3.6).', B10, S10)
B10b = add('10', 'b', '(b)', T10B,
           [row('orientation', 'Preferred orientation', 10, 'Notes 5 and sketch 5. Such as: the large glazed façade facing south for greater solar gain and lower heating demand; the long axis of the house running east-west, or turned no more than 30° east or west of south.'),
            row('sun-path', 'Sun path', 5, 'The sun path shown on the sketch, with the summer sun higher in the sky than the winter sun.'),
            row('justification', 'Justification', 5, 'Such as: maximum solar gain through the south glazing improves the thermal performance of the house and lowers its thermal energy demand.')],
           ['cons-6-4'], ['passive-design'], 'q10-orientation', 'Solar heat gain and orientation (6.4).', B10, S10)
C10 = add('10', 'c', '(c)', T10C,
          [row('reason-1', 'Reason 1', 5, 'Such as: large areas of high-performance glazing on the south elevation trapping too much solar gain in long summer sunshine; the summer sun shining from a higher angle than in winter.'),
           row('reason-2', 'Reason 2', 5, 'A second, different reason. Such as: inadequate natural or mechanical ventilation; too little thermal mass to store the solar gain; heat from cooking, lighting and appliances; no roof overhang or brise-soleil; no deciduous trees for summer shade.'),
           row('modification', 'Modification to reduce overheating', 10, 'Notes 5 and sketches 5. Such as: a brise-soleil along the south face; extended eaves as an overhang; external roller blinds; an MHRV system with a summer bypass; dynamic glass; thermal mass such as concrete internal walls.')],
          ['cons-6-4', 'cons-6-5'], ['passive-design'], 'q10-overheating', 'Solar gain (6.4) and ventilation (6.5) against overheating.', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-scheme', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p39: (a) three discussion points × (4 for point + 6 for discussion) = 30; (b) three guidelines × (4 + 6) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the Passive House question. Its parts are open responses.'
TAA = 'Discuss the above statement in detail.'
TAB = 'Propose three best practice guidelines that would ensure all buildings are built in the most sustainable way possible to minimise their embodied energy.'
AA = add('10', 'a', '(a)', TAA,
         [row(f'point-{i}', f'Discussion: Point {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: locally sourced materials cut transport and so embodied energy; imported granite and imported timber carry high embodied energy, while timber grown in Ireland is low in embodied energy and carbon neutral.'),
             (2, 'Point 4 and discussion 6. Such as: cement manufacture produces 900 kg of CO2 and SO2 for every 1000 kg of cement, so using less concrete, or cement made with GGBFS (40% less embodied energy), cuts embodied energy; durable native timbers such as cedar, larch and Douglas fir need little processing.'),
             (3, 'Point 4 and discussion 6. Such as: smaller floor areas and narrow single-room plans spanned by standard timber, with no structural steel; low-embodied-energy insulation such as recycled fibreglass, cellulose or local hemp; hempcrete; stone driveways in place of concrete. Three distinct, well-argued points are needed.')]],
         ['cons-1-2'], ['sustainability-the-environment'], None, 'Embodied energy in a sustainable built environment (1.2).', BALT, SALT, alt=True)
AB = add('10', 'b', '(b)', TAB,
         [row(f'guideline-{i}', f'Guideline {i}: (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: government agencies funding research and publishing the embodied energy of every building material; grants or tax relief for builders using natural, low-embodied-energy materials.'),
             (2, 'Point 4 and discussion 6. Such as: planning regulations restricting concrete boundary walls and requiring native trees and hedgerows; landowners encouraged to grow hemp so builders can choose hempcrete over concrete.'),
             (3, 'Point 4 and discussion 6. Such as: training building professionals to design and build with wood, cob, rammed earth and hemp-lime; homes adaptable for lifetime use under Universal Design; designers reducing concrete and steel. Three distinct guidelines are needed.')]],
         ['cons-1-2'], ['sustainability-the-environment'], None, 'Embodied energy in a sustainable built environment (1.2).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, parts(('a', TAA), ('b', TAB)), alt=True)

LEDGER = [
    (1, 'Answer any', 'Whole-exam selection: any four of the ten questions (240 marks); all question banks retained, no full-exam Cartesian cards.'),
    (5, 'any two', 'Q6(b) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
    (6, 'any two', 'Q9(b) closed choose-two of the three circled locations: one card with an any-two group (choice is not a route).'),
    (7, 'any two', 'Q10(a) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
    (7, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.'),
    (7, 'or', 'Inside the quotation of the alternative Question 10 ("turned into metals or plastics"): wording of the quoted passage, not a selection.'),
]
FINITE = {'6b': dict(choose=2, options=[h for h, _ in ITEMS6], cardId=A6b['id'], groupRowId='items'),
          '9b': dict(choose=2, options=[h for h, _ in ITEMS9], cardId=A9b['id'], groupRowId='locations'),
          '10a': dict(choose=2, options=[h for h, _ in ITEMS10], cardId=A10['id'], groupRowId='items')}
D.finish(LEDGER, FINITE, {})
