"""Draft the 2016 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 28-38; the English scheme carries Irish running headers). Q8(b) "select any two areas" and
Q10(a) "any two of the following" are ONE card each with an any-two group over the three printed items
(choice is not a route). The 22 pre-audit 2016 Higher cards keep their IDs and concept IDs and are
corrected in place; the two printed Q2(b) items keep their per-item cards and (b) composes them.
Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Flat-roofed porch, window and abutment section', concept='flat-roof-porch-section',
              stem='A front porch with a flat roof projects 1.5 metres from the external wall of a house, as shown. The roof of the porch is insulated, and is covered with layers of bituminous felt, on plywood decking, on 200 mm × 40 mm roof joists. Insulated plasterboard is fixed to the underneath of the roof joists. The external wall of the porch and of the house is a 400 mm wall of concrete block construction with a full-fill insulated cavity. The window of the porch is triple-glazed, with a thermally broken wooden frame.',
              note='Original sketch and specification retained. Construction, dimension and scale/drafting marks belong to part (a); the abutment detail in (b) is marked separately.'),
    '2': dict(page=2, title='Safety culture and safe use of ladders', concept='safety-culture-ladders', stem='',
              note='Original sketch retained. Both printed items in (a) and in (b) are required, each separately marked.'),
    '3': dict(page=2, title='Redesigning a 1970s bungalow for natural light', concept='bungalow-natural-light',
              stem='The drawing shows the plan and elevation of a two-bedroom bungalow built in the 1970s. The front elevation is south facing. The bungalow has a slated cut roof and a 300 mm external wall of concrete block construction with a full-fill insulated cavity. All internal walls are of 100 mm concrete block construction and the wall A-A is load-bearing. In the existing design, many of the rooms have low levels of natural light.',
              note='Original plan and elevation retained. Both printed considerations in (a) are required, each separately marked.'),
    '4': dict(page=3, title='A one-off house on a rural site', concept='rural-one-off-house',
              stem='This site location map shows field boundaries, roadways and some domestic buildings. It is proposed to build a new house on the site marked A.',
              note='Original site location map retained. Part (c) requires both two advantages and two disadvantages, each separately marked.'),
    '5': dict(page=3, title='Timber frame wall U-value, heat-loss cost and insulation thickness', concept='timber-frame-wall-u-value',
              stem='The external wall of a house of timber frame construction has the following specification: External render thickness 19 mm; Concrete block outer leaf thickness 100 mm; Oriented Strand Board (OSB) sheeting thickness 18 mm; Timber stud inner leaf thickness 120 mm; Mineral wool insulation between studs thickness 120 mm; Plasterboard thickness 12.5 mm. Thermal data of outer leaf and cavity: Resistance of the external surface (R) 0.048 m2 °C/W; Resistivity of the external plaster (r) 2.170 m °C/W; Conductivity of concrete block (k) 1.320 W/m °C; Resistance of the cavity (R) 0.170 m2 °C/W. Thermal data of inner leaf: Conductivity of OSB sheeting (k) 0.130 W/m °C; Conductivity of mineral wool (k) 0.040 W/m °C; Conductivity of plasterboard (k) 0.160 W/m °C; Resistance of the internal surface (R) 0.104 m2 °C/W. Note: The timber studs of the inner leaf need not be considered in your calculations.',
              note='All printed data are retained in the original question. Parts (b) and (c) use the U-value from (a); the scheme’s worked answers are U = 0.27356 W/m²°C, an annual cost of €96.96 and 111.4 mm of expanded polystyrene.'),
    '6': dict(page=4, title='A low environmental impact house and on-site renewables', concept='low-impact-renewables',
              stem='The drawing shows a single storey house. The external walls are of insulated timber frame construction and are finished externally with rendered cement board and cedar cladding, as shown. All internal partitions are of timber frame construction. The house is designed to have low environmental impact.',
              note='Original elevation and plan retained. Features and the renewable energy means are open responses; the scheme lists typical examples.'),
    '7': dict(page=4, title='Chimney stack through a slated roof', concept='chimney-stack-section',
              stem='A chimney stack projects through the pitched roof of a house as shown. The chimney stack is of solid concrete block construction with an external sand / cement render. The roof is a slated cut roof and is pitched at 45°.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the downdraught details in (b) are marked separately.'),
    '8': dict(page=4, title='Eco-refurbishing a stone storeroom as a home office', concept='storeroom-home-office',
              stem='The sketch shows a semi-detached house with a storeroom in the rear garden. The owners wish to undertake an eco-refurbishment of the storeroom to make it suitable for use as a home office.',
              note='Original sketch retained. Part (b) is a closed choice of any two of the three printed areas: one card holding all three.'),
    '9': dict(page=5, title='Domestic circuits and a lighting circuit', concept='domestic-lighting-circuits', stem='',
              note='Original sketch retained. Both printed circuits in (a) are required; (b) requires the circuit, its cable sizes and colours, and two safety features.'),
    '10': dict(page=5, title='Passive House heat storage, overheating and planning', concept='passive-house-overheating', stem='',
               note='Original sketch retained. Part (a) is a closed choice of any two of the three printed items: one card holding all three.'),
}
ALT = dict(page=5, title='Reusing existing buildings (alternative Question 10)', concept='reuse-existing-buildings',
           stem='One of the greatest challenges and opportunities for sustainable development is the reuse of our existing buildings for multiple uses. This gives vitality, density, security, utility and beauty to our countryside, villages, towns and cities. Repairing and Reusing an 18th Century House – Report by Robin Mandal Architects. Issue 283 - The Journal of the Royal Institute of the Architects of Ireland, 2015.',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately.')
SCHEME_PAGES = {'1': [4, 5, 6, 28], '2': [6, 7, 8, 29], '3': [9, 10, 30], '4': [10, 11, 31], '5': [12, 13, 32], '6': [13, 14, 15, 33],
                '7': [16, 34], '8': [17, 18, 19, 20, 35], '9': [20, 21, 36], '10': [22, 23, 24, 37], '10-alt': [25, 26, 38]}
D = cp.Draft(HERE, 2016, 'higher', ('a5bd5ecc2755e771f98bb2e6b13e3a95af33521592d128d05e676be556be5de9',
                                    'c6e563e2a60a0c2c660cc215179795443b2c8ae93a15f5ad410bfd2f7e448f81'), 22, QUESTIONS, SCHEME_PAGES, alt=ALT)
row, add, compose, parts, anyn = D.row, D.add, D.compose, D.parts, D.anyn
PRES = [0, 2, 3, 4, 5, 6, 7, 8]  # scale 4/3/2 + drafting 4/3/2, each printed separately
D.figures({
    'q1-original': D.paper(2, [30, 39, 580, 290]), 'q2-original': D.paper(2, [30, 290, 580, 490]),
    'q3-original': D.paper(2, [30, 490, 580, 790]), 'q4-original': D.paper(3, [30, 39, 580, 270]),
    'q5-original': D.paper(3, [30, 272, 580, 760]), 'q6-original': D.paper(4, [30, 39, 580, 315]),
    'q7-original': D.paper(4, [30, 315, 580, 540]), 'q8-original': D.paper(4, [30, 543, 580, 785]),
    'q9-original': D.paper(5, [30, 39, 580, 250]), 'q10-original': D.paper(5, [30, 252, 580, 490]),
    'q10-alt-original': D.paper(5, [30, 555, 580, 670]),
    'q1-section': D.composite((4, [45, 50, 575, 790]), (5, [45, 60, 575, 790]), (6, [45, 50, 575, 625])),
    'q2-culture': D.composite((6, [45, 625, 575, 790]), (7, [45, 50, 575, 750])),
    'q2-level-of-risk': D.scheme(8, [45, 50, 575, 348]), 'q2-duration-of-task': D.scheme(8, [45, 348, 575, 589]),
    'q2-ladder': D.scheme(8, [45, 50, 575, 589]), 'q2-guidelines': D.scheme(8, [45, 589, 575, 795]),
    'q3-redesign': D.scheme(9, [45, 50, 575, 418]), 'q3-reasons': D.composite((9, [45, 418, 575, 790]), (10, [45, 50, 575, 245])),
    'q4-reasons': D.scheme(10, [45, 260, 575, 458]), 'q4-layout': D.scheme(10, [45, 458, 575, 790]), 'q4-one-off': D.scheme(11, [45, 50, 575, 425]),
    'q5-calculation': D.composite((12, [45, 50, 575, 770]), (13, [45, 50, 575, 205])), 'q5-thickness': D.scheme(13, [45, 208, 575, 470]),
    'q6-features': D.composite((13, [45, 485, 575, 790]), (14, [45, 50, 575, 334])),
    'q6-renewable': D.composite((14, [45, 334, 575, 790]), (15, [45, 50, 575, 355])), 'q6-advantages': D.scheme(15, [45, 355, 575, 765]),
    'q7-section': D.scheme(16, [45, 50, 575, 785]),
    'q8-advantages': D.scheme(17, [45, 50, 575, 640]),
    'q8-upgrades': D.composite((17, [45, 640, 575, 790]), (18, [45, 50, 575, 790]), (19, [45, 50, 575, 790]), (20, [45, 50, 575, 292])),
    'q9-circuits': D.scheme(20, [45, 455, 575, 765]), 'q9-lighting': D.scheme(21, [45, 50, 575, 445]), 'q9-economy': D.scheme(21, [45, 445, 575, 775]),
    'q10-principles': D.scheme(22, [45, 50, 575, 785]),
    'q10-overheating': D.composite((23, [45, 50, 575, 790]), (24, [45, 50, 575, 165])), 'q10-planning': D.scheme(24, [45, 168, 575, 500]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p28 (printed 26): (a) best eleven details × 4 (drawing 3, annotation 1) = 44, four typical dimensions 4, scale 4/3/2 + drafting 4/3/2 = 8: 56; (b) design detail to prevent the ingress of water 4. Complete 60.'
S1 = 'One required section and one required abutment detail. The detail list is a marking menu, not a printed choice.'
T1A = 'To a scale of 1:5, draw a vertical section through the porch, showing the external wall, the flat roof and the window of the porch. Show the typical construction details from a level 300 mm below the fixed frame of the porch window, through the walls, the window head, lintels and flat roof to a level 400 mm above the abutment of the flat roof and the front wall of the house. Include four typical dimensions.'
T1B = 'Show on your drawing the design detailing to prevent the ingress of water at the junction of the flat roof and the main wall of the house.'
A1 = add('1', 'a', '(a)', T1A,
         [row('details', 'Timber flat roof, external walls and window (11 × 4 marks)', 44, 'Best eleven details, 4 each (drawing 3, annotation 1). Menu: lead flashing; bituminous felt; eaves batten/drip; plywood decking; counter battens/ventilation; tilting fillet; breather membrane; joists and roof insulation; wallplate; vapour control layer; hangers to the main wall; insulated plasterboard; fascia, soffit and gutter; cavity wall and ties; cavity closer; wall insulation; renders; stepped DPC; lintels; thermally broken window frame (2 without the break); triple-glazed unit; airtightness tapes.', list(range(0, 45, 4))),
          row('dimensions', 'Four typical dimensions', 4, 'Four typical dimensions, 1 each.'),
          row('presentation', 'Scale 4 marks Drafting 4 marks', 8, 'Scale 4 and drafting 4, each excellent 4, good 3, fair 2.', PRES)],
         ['cons-1-5', 'cons-3-10', 'cons-3-3', 'cons-3-6'], ['question-1-drawing-questions', 'roofs', 'walls', 'windows-light'], 'q1-section',
         'Scaled drawing (1.5) of a flat roof and its abutment (3.10) on a cavity wall (3.3) over a window head (3.6).', B1, S1)
B1b = add('1', 'b', '(b)', T1B,
          [row('abutment', 'Design detail to prevent the ingress of water', 4, 'Show and identify the abutment detailing, such as a stepped DPC with lead flashing and counter flashing over an upstand, as in the scheme’s model sections.')],
          ['cons-3-10', 'cons-3-4'], ['roofs', 'walls'], 'q1-section', 'A flat roof abutment (3.10) with stepped DPC and flashings (3.4).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p29 (printed 27): (a) safety training and collective responsibility × (2 + 4) = 12; (b) level of risk and duration of task × (2 + 4) = 12; (c) three guidelines × (notes 6 + sketches 6) = 36. Complete 60.'
S2 = 'Both printed items in (a) and in (b) are required, each separately marked; in (b) each keeps its pre-audit card and the part composes them. The guidelines in (c) are open responses.'
SAFE = (['cons-1-8'], ['site-safety'])
T2A = 'Discuss in detail the importance of each of the following in developing a positive safety culture among workers on a construction site: safety training; collective responsibility.'
T2B = 'Discuss in detail the importance of each of the following when deciding if the use of a ladder is appropriate, or not, for a proposed task: level of risk; duration of task.'
T2C = 'Discuss in detail, using notes and freehand sketches, three specific best practice guidelines that should be observed when placing a ladder to access a scaffold platform on a construction site.'
A2 = add('2', 'a', '(a)', T2A,
         [row('training', 'Safety training', 6, 'Point 2 and discussion 4. Such as: initial training before new work or procedures, since the first days on site are the most dangerous; ongoing training against complacency; Safe Pass.'),
          row('responsibility', 'Collective responsibility', 6, 'Point 2 and discussion 4. Such as: everyone looks out for the safety of others; safety becomes the group norm and a shared experience; reporting hazards; management commitment.')],
         *SAFE, 'q2-culture', 'Safety precautions on site (1.8).', B2, S2)
ITEMS2B = [('level-of-risk', 'Level of risk', 'q2-level-of-risk', 'Point 2 and discussion 4. Such as: a ladder is always hazardous and a risk remains; if the risk stays too high use a lift or mechanical hoist; risks include poor fixing, the wrong angle, over-reaching and fatigue; higher work means more severe consequences.'),
           ('duration-of-task', 'Duration of task', 'q2-duration-of-task', 'Point 2 and discussion 4. Such as: the risk rises when a ladder is used for long periods; use a ladder only where the risk is low, the work short and light and three points of contact can be kept; otherwise a hoist or scaffold.')]
b2 = [add('2', f'b-{slug}', f'(b) — {slug}', f'{T2B} — {heading}', [row('item', heading, 6, note)],
          *SAFE, figure, 'Safety precautions on site, here with ladders (1.8).', B2, S2) for slug, heading, figure, note in ITEMS2B]
B2b = compose('2', 'b', '(b)', b2, 'q2-ladder', B2, S2, T2B, labels=[x[1] for x in ITEMS2B])
C2 = add('2', 'c', '(c)', T2C,
         [row(f'guideline-{i}', f'Guideline {i}', 12, note) for i, note in [
             (1, 'Notes 6 and sketches 6. Such as: the ladder securely held or tied at both ends; level grounding for the foot on uneven ground.'),
             (2, 'A second, different guideline. Such as: the ladder extends at least 1.0 m above the platform; the foot out a quarter of the height, a slope of about 74°.'),
             (3, 'A third, different guideline. Such as: positioned so users are protected by safety rails, toe boards and gates; multiple ladder runs above one storey; structurally sound and rated for the loads.')]],
         *SAFE, 'q2-guidelines', 'Safety precautions on site, here with ladders and scaffolds (1.8).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-guidelines', B2, S2, parts(('a', T2A), ('b', T2B), ('c', T2C)))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p30 (printed 28): (a) external envelope and internal layout, each note 10 + sketch 10 = 40; (b) two redesign discussions × 10 = 20. Complete 60.'
S3 = 'Both printed considerations in (a) are required, each separately marked; the reasons in (b) are open responses.'
LIGHT = (['cons-7-4', 'cons-1-2'], ['windows-light', 'planning-sustainability-environment'])
T3A = 'Show, using notes and freehand sketches, a revised design of the bungalow which will ensure a bright, light-filled interior. In your revised design, you should consider: modifying the external envelope to improve the penetration of natural light and revising the internal layout to optimise natural light.'
T3B = 'Discuss in detail the reasons for your proposed design choices in the redesign of the bungalow. Note: It is not necessary to show the furniture in your design sketches.'
A3 = add('3', 'a', '(a)', T3A,
         [row('envelope', 'Design feature external envelope', 20, 'Notes 10 and sketches 10. Such as: more glazing to the south, east and west and little to the north; low-e double or triple glazing; floor-to-ceiling glazing; roof lights or a sky tunnel for north rooms.'),
          row('layout', 'Design feature internal layout', 20, 'Notes 10 and sketches 10. Such as: kitchen and dining moved to the south; little-used rooms and the bathroom to the north; open plan to let light through, keeping the load-bearing wall A-A.')],
         *LIGHT, 'q3-redesign', 'Good daylighting (7.4) by layout design (1.2).', B3, S3)
B3b = add('3', 'b', '(b)', T3B,
          [row(f'redesign-{i}', f'Redesign {i} - Discussion', 10, note) for i, note in [
              (1, 'Such as, the internal layout: living areas to the south; furniture kept from windows; light colours and mirrors reflecting light; a glass door or roof light bringing light to the hallway.'),
              (2, 'Such as, the external envelope: a south principal elevation; fewer, smaller north windows to cut heat loss; tall south windows and an east window for morning sun; roof lights sized to the roof.')]],
          *LIGHT, 'q3-reasons', 'Good daylighting (7.4) by layout design (1.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-redesign', B3, S3, parts(('a', T3A), ('b', T3B)))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p31 (printed 29): (a) three reasons × 6 = 18; (b) sketches, location and orientation, entrance gateway and access road, and two justifications × 6 = 30; (c) two advantages and two disadvantages × 3 = 12. Complete 60.'
S4 = 'Reasons and the layout are open responses. Part (c) requires both two advantages and two disadvantages, each separately marked.'
SITE = (['cons-1-3'], ['planning-sustainability-environment'])
T4A = 'Discuss in detail three reasons why site A may be considered suitable for a new house.'
T4B = 'Using a well proportioned freehand sketch, redraw the given site and the immediate surrounding boundaries. On your sketch show a proposed: location and orientation for a house on site A; entrance gateway and access road to the house. For each of the above, justify your design choices.'
T4C = 'Discuss in detail two advantages and two disadvantages of building one-off houses in the Irish rural landscape.'
A4 = add('4', 'a', '(a)', T4A,
         [row(f'reason-{i}', f'Reason {i}', 6, note) for i, note in [
             (1, 'Such as: large enough, with suitable proportions, for a house and its waste-water treatment and percolation area.'),
             (2, 'A second, different reason. Such as: public access from the adjoining roads; a possible southerly aspect for sustainable design.'),
             (3, 'A third, different reason. Such as: close to existing houses, so water, electricity and broadband are available and cost effective; straight roads with sightlines for safe access.')]],
         *SITE, 'q4-reasons', 'Choosing a site (1.3).', B4, S4)
B4b = add('4', 'b', '(b)', T4B,
          [row('sketches', 'Sketches', 6, 'A well-proportioned sketch of the site and its boundaries.'),
           row('location', 'Location and orientation of house on site', 6, 'Such as: the front facing south for solar gain; close to the road and services with a short driveway; not overlooked or obtrusive; room for waste-water treatment.'),
           row('entrance', 'Entrance gateway and access road', 6, 'Such as: clear sightlines; entry from a quiet side road, away from the junction and the bend; perpendicular access; space to stop off the road while the gates open.'),
           row('justification-1', 'Justification 1', 6, 'The location and orientation justified.'),
           row('justification-2', 'Justification 2', 6, 'The entrance and access road justified.')],
          ['cons-1-3', 'cons-6-4'], ['planning-sustainability-environment'], 'q4-layout', 'Siting (1.3) and orientation for solar gain (6.4).', B4, S4)
C4 = add('4', 'c', '(c)', T4C,
         [row('advantage-1', 'Advantage 1', 3, 'Such as: local people live among family and neighbours; a quality of life in healthy, quiet surroundings.'),
          row('advantage-2', 'Advantage 2', 3, 'A second, different advantage. Such as: supports the rural economy and services; a community of people who tend the countryside.'),
          row('disadvantage-1', 'Disadvantage 1', 3, 'Such as: unsustainable, with higher building, maintenance and transport costs; services may be hard to get.'),
          row('disadvantage-2', 'Disadvantage 2', 3, 'A second, different disadvantage. Such as: no reliable public transport; long school journeys; loss of visual amenity; isolation in old age.')],
         ['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'], 'q4-one-off', 'The built environment (1.2) and choosing a site (1.3).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-layout', B4, S4, parts(('a', T4A), ('b', T4B), ('c', T4C)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p32 (printed 30): (a) ten points × 3 = 30 (five layers, the cavity, two surface resistances, total resistance, U-value); (b) five steps × 3 = 15; (c) five steps × 3 = 15. Complete 60.'
S5 = 'No printed choice. Parts (b) and (c) use the U-value from (a).'
T5A = 'Calculate the U-value of the above external wall.'
T5B = ('Calculate the cost of heat lost annually through this wall, using the following data: Area of external wall 150 m2; Average internal temperature 18 °C; Average external temperature 6 °C; '
       'U-value of wall as calculated above; Heating period 8 hours per day, every day for 38 weeks per annum; Cost of oil 96 cent per litre; Calorific value of oil 37350 kJ per litre; 1000 Watts 1 kJ per second.')
T5C = ('It is proposed to upgrade the thermal properties of the above wall to meet the Passive House standard by fixing expanded polystyrene to the external surface. '
       'Given the thermal conductivity (k) of expanded polystyrene as 0.037 W/m °C, calculate the thickness of expanded polystyrene required to achieve a U-value of 0.15 W/m2 °C.')
A5 = add('5', 'a', '(a)', T5A,
         [row('resistances', 'External plaster External block OSB Racking Board Mineral Wool Insulation Plasterboard Cavity External surface resistance Internal surface resistance', 24,
              'Eight resistances, 3 each, by R = T/k (or R = T × r for the render): render 0.019 × 2.170 = 0.04123; block 0.100/1.320 = 0.07575; OSB 0.018/0.130 = 0.13846; mineral wool 0.120/0.040 = 3.00000; plasterboard 0.0125/0.160 = 0.078125; cavity 0.170, external surface 0.048 and internal surface 0.104 (given). All in m²°C/W.', list(range(0, 25, 3))),
          row('total-resistance', 'Total resistance', 3, 'Total resistance Rt = 3.655565 m²°C/W.', [0, 3]),
          row('u-value', 'U-value of external wall (1 mark for formula)', 3, 'U = 1 ÷ Rt = 1 ÷ 3.655565 = 0.273555 W/m²°C (1 mark for the formula).', [0, 1, 2, 3])],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Thermal resistance, conductivity and transmittance (6.1).', B5, S5)
B5b = add('5', 'b', '(b)', T5B,
          [row('heat-loss', 'Heat loss formula and calculation', 3, 'Heat loss = U-value × area × temperature difference = 0.273555 × 150 × 12 = 492.39994 watts (joules per second).'),
           row('duration', 'Heating duration for one year', 3, 'Heating period = 60 × 60 × 8 × 7 × 38 = 7,660,800 seconds (2,128 hours).'),
           row('energy', 'k/Joules calculation for one year', 3, 'Energy = 7,660,800 × 492.39994 ÷ 1000 = 3772168.08 kJ per year.'),
           row('oil', 'Litres of oil for one year', 3, 'Oil = 3772168.08 ÷ 37,350 = 100.99 litres per year.'),
           row('cost', 'Annual cost of heat loss', 3, 'Annual cost = 100.99 × €0.96 = €96.96. The scheme’s alternative one-line method gives €96.94.')],
          ['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Heat loss calculation and running costs (6.3) from the U-value (6.1).', B5, S5)
C5 = add('5', 'c', '(c)', T5C,
         [row('required-resistance', 'Resistance for U-value of 0.15 W/m2 °C', 3, 'Required resistance = 1 ÷ 0.15 = 6.6666 m²K/W.'),
          row('existing-resistance', 'Existing resistance from part (a)', 3, 'Existing resistance = 1 ÷ 0.27356 = 3.6555 m²K/W.'),
          row('difference', 'Difference in resistances (required resistance)', 3, 'Difference = 6.6666 − 3.6555 = 3.0111 m²K/W.'),
          row('formula', 'Application of formula R = T/k', 3, 'R = T/k, so 3.0111 = T/0.037.'),
          row('thickness', 'Required thickness of insulation', 3, 'T = 3.0111 × 0.037 = 0.1114107 m: 111.4 mm of expanded polystyrene (111 or 112 mm accepted).')],
         ['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation'], 'q5-thickness', 'Thermal transmittance (6.1) and insulating materials (6.2).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p33 (printed 31): (a) three features × (notes 5 + sketches 5) = 30; (b) one means of on-site renewable energy, notes 10 + sketches 10 = 20; (c) two advantages × 5 = 10. Complete 60.'
S6 = 'Features and the renewable energy means are open responses with no printed list.'
T6A = 'Discuss in detail, using notes and freehand sketches, three features of the design that contribute to the house having low environmental impact.'
T6B = 'To meet the Nearly Zero Energy Building (NZEB) requirements, the production of on-site renewable energy is recommended. Using notes and freehand sketches show one means of generating on-site renewable energy for the dwelling house.'
T6C = 'Discuss in detail two advantages of generating renewable energy on-site.'
A6 = add('6', 'a', '(a)', T6A,
         [row(f'feature-{i}', f'Design feature {i}', 10, note) for i, note in [
             (1, 'Notes 5 and sketches 5. Such as: carbon-neutral cedar cladding needing no preservatives; renewable timber frame storing CO₂.'),
             (2, 'A second, different feature. Such as: trees planted for shade, biodiversity and carbon sequestration, softening the architecture.'),
             (3, 'A third, different feature. Such as: large south and double-height glazing for solar gain and small north windows; the stove against a high-thermal-mass inner wall; a compact, open-plan form with a storm porch.')]],
         ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-features',
         'Low-impact design of the built environment (1.2), solar gain (6.4) and insulation (6.2).', B6, S6)
B6b = add('6', 'b', '(b)', T6B,
          [row('notes', 'Notes', 10, 'Such as: a micro wind turbine of 1.5–2.0 m sited at least 10 m above obstructions within 100 m, with an inverter and batteries or a grid connection; photovoltaic panels; evacuated tubes for up to 60% of hot water; air, water or ground heat exchangers.'),
           row('sketches', 'Sketches', 10, 'Freehand sketches of the system on the house.')],
          ['cons-5-8', 'cons-6-4'], ['services-water-gas-electricity', 'sustainability-the-environment'], 'q6-renewable', 'On-site electricity (5.8) and solar energy (6.4).', B6, S6)
C6 = add('6', 'c', '(c)', T6C,
         [row('advantage-1', 'On-site generation - advantage 1', 5, 'Such as: a sustainable alternative to mains electricity from fossil fuels; freely available natural resources.'),
          row('advantage-2', 'On-site generation - advantage 2', 5, 'A second, different advantage. Such as: no carbon taxes or transmission losses; the household less dependent on the mains, with battery storage making off-grid possible.')],
         ['cons-1-2', 'cons-5-8'], ['sustainability-the-environment', 'services-water-gas-electricity'], 'q6-advantages', 'Sustainable (1.2) on-site electricity (5.8).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-features', B6, S6, parts(('a', T6A), ('b', T6B), ('c', T6C)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p34 (printed 32): (a) best eleven details × 4 = 44 and scale 4/3/2 + drafting 4/3/2 = 8: 52; (b) two design details × 2 and typical dimensions 2 × 2 = 8. Complete 60.'
S7 = 'One required section and two required downdraught details. The detail list is a marking menu, not a printed choice.'
T7A = 'To a scale of 1:5, draw a vertical section through the chimney stack and roof structure. Show the typical construction details of the chimney stack, flue, chimney capping and portion of the adjoining roof structure. Include the design details to prevent the penetration of rainwater between the chimney stack and the adjoining roof surface.'
T7B = 'On your drawing, show two considerations to be taken into account in the design of the chimney stack shown which will help prevent a downdraught. Include typical dimensions as appropriate.'
A7 = add('7', 'a', '(a)', T7A,
         [row('details', 'Vertical section through chimney stack and roof structure (11 × 4 marks)', 44, 'Best eleven details, 4 each. Menu: blockwork; render; flue liners; fill; chimney capping; two cover flashings; under flashing (apron); flashing to the rear gutter; apron or tray; rafter; fillet piece; breather membrane; battens and counter battens; trimmer; slates.', list(range(0, 45, 4))),
          row('presentation', 'Scale Drafting (Excellent, good, fair)', 8, 'Scale 4 and drafting 4, each excellent 4, good 3, fair 2.', PRES)],
         ['cons-1-5', 'cons-5-7', 'cons-3-9', 'cons-3-10'], ['question-1-drawing-questions', 'fireplaces-fire-prevention', 'roofs'], 'q7-section',
         'Scaled drawing (1.5) of a chimney stack and flue (5.7) through a slated roof (3.9) with its flashings (3.10).', B7, S7)
B7b = add('7', 'b', '(b)', T7B,
          [row('detail-1', 'Design detail 1', 2, 'Such as: the stack at least 600 mm above the ridge, or 1000 mm above the roof surface where it meets it.'),
           row('detail-2', 'Design detail 2', 2, 'A second, different detail. Such as: a cowl on the flue; the stack clear of nearby obstructions.'),
           row('dimensions', 'Typical dimensions (2 × 2 marks)', 4, 'Two typical dimensions, 2 each, such as the 600 mm and 1000 mm heights.')],
          ['cons-5-7'], ['fireplaces-fire-prevention'], 'q7-section', 'Flues to domestic fireplaces (5.7).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p35 (printed 33): (a) two advantages and two disadvantages × 5 = 20; (b) any two of three printed areas × (notes 8 + sketches 8) = 32 and two justifications × 4 = 8: 40. Complete 60.'
S8 = 'Choice is not a route: part (b) (select any two of the three printed areas) is ONE card with an any-two group over the scheme headings, plus the two printed justification rows; its figure carries all three areas’ scheme drawings.'
T8A = 'Discuss two advantages and two disadvantages of refurbishing the storeroom for use as a home office.'
T8B = 'A survey of the storeroom reveals: walls: random rubble, unrendered, 450 mm thick; roof: uninsulated, traditional cut roof with natural slate; floor: stone flags on earth. Select any two areas from the above and, using notes and freehand sketches, show the design detailing necessary to upgrade the storeroom to make it suitable for use as a home office. The refurbishment should be eco-friendly and should respect the character and appearance of the original storeroom. Justify your design choices.'
A8 = add('8', 'a', '(a)', T8A,
         [row('advantage-1', 'Advantage 1', 5, 'Such as: refurbishment usually costs less than new build; a stone building kept, maintaining the local heritage.'),
          row('advantage-2', 'Advantage 2', 5, 'A second, different advantage. Such as: no daily commute, saving time and energy; fewer new materials; an exemplar of reuse.'),
          row('disadvantage-1', 'Disadvantage 1', 5, 'Such as: a derelict building may not be worth refurbishing; slow, costly work to keep its character.'),
          row('disadvantage-2', 'Disadvantage 2', 5, 'A second, different disadvantage. Such as: hard to bring up to modern standards; rising damp; no external insulation without losing the stone finish; work and home hard to separate.')],
         ['cons-1-1', 'cons-1-2'], ['conservation-restoration'], 'q8-advantages', 'Reusing an older building (1.1) in the built environment (1.2).', B8, S8)
AREAS = [('Upgrading walls', 'a breathable structure letting moisture move out; hygroscopic, natural insulation such as hemp-lime, wood fibre or sheep’s wool; layers more permeable towards the outside; raking out and repointing in lime by hand; three coats of lime plaster.'),
         ('Upgrading roof', 'all members vented; slates removed, numbered and stored; decayed rafters cut back or replaced in treated timber of the same section; a vapour-diffuse membrane and counter battens; matching salvaged slates; cast-iron rainwater goods.'),
         ('Upgrading floor', 'flags photographed, numbered and lifted; earth replaced with compacted hardcore, blinding and a radon barrier; a hemp-lime or insulated slab; the flags relaid on lime or proprietary screed and sealed.')]
A8b = add('8', 'b', '(b)', T8B,
          [anyn('areas', 'Design detailing to upgrade storeroom - 2 areas', 2, 16, AREAS, 'Any two of the three printed areas, each notes 8 and sketches 8 = 16.'),
           row('justification-1', 'Justification for design choices - area 1', 4, 'The choices for the first area justified, such as breathability and respect for the original character.'),
           row('justification-2', 'Justification for design choices - area 2', 4, 'The choices for the second area justified.')],
          ['cons-1-1', 'cons-3-3', 'cons-3-9', 'cons-4-2', 'cons-6-2'], ['conservation-restoration', 'walls', 'roofs', 'floors', 'heat-loss-insulation'], 'q8-upgrades',
          'The union of the three printed areas, upgraded with respect for the original character (1.1): the rubble walls (3.3), the slated roof (3.9) and the flagged floor (4.2), with breathable insulation (6.2).', B8, S8)
compose('8', 'complete', ' — complete', [A8, A8b], 'q8-upgrades', B8, S8, parts(('a', T8A), ('b', T8B)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p36 (printed 34): (a) ring and radial circuit locations × 4 = 8; (b) annotated sketch 12, cable sizes 3 × 2, colour coding 3 × 2 and two safety features × 6 = 36; (c) two economy features × 8 = 16. Complete 60.'
S9 = 'Both printed circuits in (a) are required; (b) requires every printed element of the circuit; the features in (c) are open responses.'
ELEC = (['cons-5-8'], ['services-water-gas-electricity'])
T9A = 'State where the following electrical circuits are typically used in a domestic dwelling: ring circuit; radial circuit.'
T9B = 'Two electrical light points, as shown, are controlled by a single switch. Using an annotated freehand sketch, show the design of a typical electrical circuit for the lights. Show the circuit from the consumer electrical distribution board to the light points and switch. Indicate the typical sizes and colour coding of the electric cables. In your sketch, show two safety features in the design of the lighting circuit to ensure that it is safe for all users.'
T9C = 'Show two features that could be incorporated into the design of a lighting system to ensure the economical use of electricity in the house.'
A9 = add('9', 'a', '(a)', T9A,
         [row('ring', 'Ring circuit – typical location in house', 4, 'Such as: socket outlets in adjacent rooms, not the kitchen; 2.5 mm² cable on a 32 A MCB, serving up to 100 m².'),
          row('radial', 'Radial circuit - typical location in house', 4, 'Such as: the kitchen, which needs at least two; at most ten sockets and two rooms; a 20 A MCB with 2.5 mm² cable.')],
         *ELEC, 'q9-circuits', 'Domestic electrical installation and circuits (5.8).', B9, S9)
B9b = add('9', 'b', '(b)', T9B,
          [row('sketch', 'Annotated sketch for switch and two lights', 12, 'An annotated sketch of the loop-in circuit from the distribution board (main switch, RCDs, MCBs) to the switch and two ceiling roses, as in the scheme’s model diagram.'),
           row('sizes', 'Typical sizes of cables (3 × 2 marks)', 6, 'Three sizes, 2 each, such as 1.5 mm² PVC/PVC cable for the circuit and 0.5 mm² heat-resistant flex to the lamp holders.'),
           row('colours', 'Colour coding of cables (3 × 2 marks)', 6, 'Three colours, 2 each: brown for live and switch conductors, blue for neutral, green/yellow sleeving for earth.'),
           row('safety-1', 'Safety feature 1 in design of circuit', 6, 'Such as: an earth to both lighting points and the switch; correctly sized cables.'),
           row('safety-2', 'Safety feature 2 in design of circuit', 6, 'A second, different feature. Such as: protection by fuse/MCB and RCD; the switch breaking the live conductor; all circuits earthed.')],
          *ELEC, 'q9-lighting', 'Domestic electrical installation, circuits and protection (5.8).', B9, S9)
C9 = add('9', 'c', '(c)', T9C,
         [row('feature-1', 'Design feature 1 in circuit', 8, 'Such as: separate lighting circuits and task lighting used only as needed; motion or heat sensors switching lights off in empty rooms.'),
          row('feature-2', 'Design feature 2 in circuit', 8, 'A second, different feature. Such as: low-energy LED lamps of 80–120 lumens per watt; smart metering and app control; natural light maximised with reflective surfaces.')],
         ['cons-5-8', 'cons-7-4'], ['services-water-gas-electricity', 'windows-light'], 'q9-economy', 'Electrical installation (5.8) and good illumination (7.4).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-lighting', B9, S9, parts(('a', T9A), ('b', T9B), ('c', T9C)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p37 (printed 35): (a) any two of three printed items × (notes 6 + sketches 6) = 24; (b) two reasons for overheating × 6 and two design details × 6 = 24; (c) two advantages and two disadvantages × 3 = 12. Complete 60.'
S10 = 'Choice is not a route: part (a) (any two of three printed items) is ONE card with an any-two group over the scheme headings; its figure and the complete-question figure carry all three items’ drawings. The OR alternative is a separate Question 10 route.'
T10A = 'Minimising heat loss and storing heat gain are important considerations in Passive House design. Using notes and freehand sketches, show best practice design detailing to minimise heat loss and maximise heat storage in a Passive House for any two of the following: foundations; ground floor; walls.'
T10B = 'The Passive House shown overheats in summer. Discuss two reasons why overheating occurs and, using notes and freehand sketches, show two design details for the house that would reduce the possibility of overheating.'
T10C = 'Discuss two advantages and two disadvantages of making the Passive House standard a planning requirement for all new housing in Ireland.'
ITEMS10 = [('Foundations', 'a passive foundation of U-value 0.10–0.15 W/m²K with no thermal bridges; high compressive strength insulation; a traditional strip with autoclaved aerated concrete blockwork.'),
           ('Ground Floor', 'thermal mass from a thicker screed and tile finish to absorb and retain heat; high insulation; no thermal bridges; airtightness.'),
           ('Walls', 'a passive wall of U-value 0.10–0.15 W/m²K; high insulation, no thermal bridges, airtightness; a block inner leaf with plaster for thermal mass, or heat stores such as a Trombe wall in timber frame.')]
A10 = add('10', 'a', '(a)', T10A,
          [anyn('items', 'Best practice design detailing - any 2', 2, 12, ITEMS10, 'Any two of the three printed items, each notes 6 and sketches 6 = 12.')],
          ['cons-6-2', 'cons-2-4', 'cons-4-2', 'cons-3-3'], ['passive-design', 'foundations', 'floors', 'walls'], 'q10-principles',
          'The union of the three printed items, insulated without thermal bridges (6.2): foundations (2.4), the ground floor (4.2) and walls (3.3).', B10, S10)
B10b = add('10', 'b', '(b)', T10B,
           [row('reason-1', 'Reason 1 for overheating', 6, 'Such as: inadequate or no shading of windows — no overhang, balcony or brise-soleil; large south glazing giving too much solar gain.'),
            row('reason-2', 'Reason 2 for overheating', 6, 'A second, different reason. Such as: insufficient ventilation; too little thermal mass; heat from lighting, appliances, hot water and cooking.'),
            row('detail-1', 'Design detail 1 (note and sketch)', 6, 'Note and sketch. Such as: an extended roof overhang sized from the summer and winter sun angles.'),
            row('detail-2', 'Design detail 2 (note and sketch)', 6, 'A second, different detail. Such as: brise-soleil or external blinds; dynamic glass; thermal mass; MHRV summer bypass and through ventilation.')],
           ['cons-6-4', 'cons-6-5'], ['passive-design'], 'q10-overheating', 'Solar heat gain (6.4) and ventilation (6.5).', B10, S10)
C10 = add('10', 'c', '(c)', T10C,
          [row('advantage-1', 'Advantage 1', 3, 'Such as: about 75% less energy than a house built to the building regulations.'),
           row('advantage-2', 'Advantage 2', 3, 'A second, different advantage. Such as: constant comfort at 20 °C; cheaper to run; lower CO₂ emissions.'),
           row('disadvantage-1', 'Disadvantage 1', 3, 'Such as: a very high standard of workmanship and training for every trade.'),
           row('disadvantage-2', 'Disadvantage 2', 3, 'A second, different disadvantage. Such as: expensive materials and capital cost; longer contracts; a private standard that charges for certification.')],
          ['cons-1-3', 'cons-6-3'], ['planning-sustainability-environment', 'heat-loss-insulation'], 'q10-planning', 'Planning control (1.3) and running costs (6.3).', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-principles', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p38 (printed 36): discussion of the statement, three points × (4 + 6) = 30; three best practice guidelines × (4 + 6) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately, so each is its own task and the complete card composes them.'
TAA = 'Discuss the above statement in detail.'
TAB = 'Recommend three best practice guidelines that would promote the refurbishment and reuse of existing buildings in Ireland.'
TALL = 'Discuss the above statement in detail and recommend three best practice guidelines that would promote the refurbishment and reuse of existing buildings in Ireland.'
REUSE = (['cons-1-1', 'cons-1-2'], ['conservation-restoration'])
AA = add('10', 'discussion', ' — discussion', TAA,
         [row(f'point-{i}', f'Discussion – point {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: present-day uses differ from those buildings were designed for, so remodelling is needed for reuse.'),
             (2, 'Point 4 and discussion 6. Such as: guidelines should respect the original structure and allow sensitive changes; if reuse is not achievable buildings decay and heritage is lost.'),
             (3, 'Point 4 and discussion 6. Such as: modest existing buildings suit a sustainability age; reuse brings new vitality, businesses and mixed uses to derelict areas. Three distinct, well-argued points are needed.')]],
         *REUSE, None, 'Conserving and reusing buildings (1.1) in the built environment (1.2).', BALT, SALT, alt=True)
AB = add('10', 'guidelines', ' — guidelines', TAB,
         [row(f'guideline-{i}', f'Recommendation {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: refurbishment true to the original layout, materials and processes; exemplars promoted.'),
             (2, 'Point 4 and discussion 6. Such as: conservation grants and supports; best practice guidelines widely disseminated; conservation architects on the design team.'),
             (3, 'Point 4 and discussion 6. Such as: the new use and essential works specified; defects and future works identified; public resources for thoughtful refurbishment. Three distinct guidelines are needed.')]],
         *REUSE, None, 'Conserving and reusing buildings (1.1) in the built environment (1.2).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, TALL, labels=['Discussion of the statement', 'Three best practice guidelines'], alt=True)

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and any four of the other nine (300 marks); all question banks retained, no full-exam Cartesian cards.'),
          (2, 'or', 'Q2(b) wording ("appropriate, or not"): not a candidate choice.'),
          (4, 'Select', 'Q8(b) closed choose-two of three printed areas: one card with an any-two group (choice is not a route).'),
          (4, 'any two', 'Q8(b) closed choose-two of three printed areas: the same any-two group.'),
          (5, 'any two', 'Q10(a) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
          (5, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.'),
          (5, 'One of', 'Alternative Question 10 quotation ("One of the greatest challenges"): not a candidate choice.')]
FINITE = {'8b': dict(choose=2, options=[h for h, _ in AREAS], cardId=A8b['id'], groupRowId='areas'),
          '10a': dict(choose=2, options=[h for h, _ in ITEMS10], cardId=A10['id'], groupRowId='items')}
REASONS = {
    'q2-a': 'Split into the two printed items, safety training and collective responsibility (2 + 4 each); tariff unchanged (12).',
    'q2-b-level-of-risk': 'Reshaped to the printed item row (2 for point, 4 for discussion), named by its scheme heading; tariff unchanged (6).',
    'q2-b-duration-of-task': 'Reshaped to the printed item row (2 for point, 4 for discussion), named by its scheme heading; tariff unchanged (6).',
    'q2-c': 'Split into three guidelines, each notes 6 + sketches 6; tariff unchanged (36).',
    'q3-a': 'Rebuilt to the printed rows — external envelope and internal layout, each note 10 + sketch 10: 20 → 40.',
    'q3-b': 'Split into the two printed redesign discussions (10 each); tariff unchanged (20).',
    'q4-a': 'Split into the three printed reasons (6 each); tariff unchanged (18).',
    'q4-b': 'Split into the five printed rows (6 each); tariff unchanged (30).',
    'q4-c': 'Split into the two printed advantages and two disadvantages (3 each); tariff unchanged (12).',
    'q5-b': 'Reshaped to the five printed calculation steps (3 each) with the scheme’s worked answer (€96.96); tariff unchanged (15).',
    'q5-c': 'Reshaped to the five printed calculation steps (3 each) with the scheme’s worked answer (111.4 mm); tariff unchanged (15).',
    'q6-a': 'Split into three design features, each notes 5 + sketches 5; tariff unchanged (30).',
    'q6-b': 'Reshaped to the printed notes 10 + sketches 10 for one means; tariff unchanged (20).',
    'q6-c': 'Split into the two printed advantages (5 each); tariff unchanged (10).',
    'q7-a': 'Adds the scale and drafting allowance (4/3/2 each) printed with the eleven details: 44 → 52.',
    'q7-b': 'Rebuilt to the printed rows — two design details (2 each) and typical dimensions (2 × 2): 4 → 8.',
    'q8-a': 'Split into the two printed advantages and two disadvantages (5 each); tariff unchanged (20).',
    'q9-a': 'Split into the two printed circuits (4 each); tariff unchanged (8).',
    'q9-c': 'Split into the two printed design features (8 each); tariff unchanged (16).',
    'q10-a': 'Now one card with an any-two group over all three printed items (notes 6 + sketches 6 each); choice is not a route: 18 → 24.',
    'q10-b': 'Rebuilt to the printed rows — two reasons and two design details (6 each): 42 → 24 (42 overran the question’s 60).',
    'q10-c': 'Split into the two printed advantages and two disadvantages (3 each); tariff unchanged (12).',
}
D.finish(LEDGER, FINITE, REASONS)
