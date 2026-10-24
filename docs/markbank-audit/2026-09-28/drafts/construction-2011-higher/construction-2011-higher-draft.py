"""Draft the 2011 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 30-40; the English scheme carries Irish running headers). This paper was never carded: every task is
added. Q9(a) "select any three locations" from the four circled and Q10(a) "any two of the following" are ONE
card each with an anyN group (choice is not a route). Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Accessible entrance door and threshold section', concept='accessible-door-threshold-section',
              stem='The main external doorway of a dwelling house is designed to facilitate access for everyone, including a person with reduced mobility, as shown in the sketch. The door is a framed wooden door with 12 mm thick vertical sheeting on both sides. The doorframe is 150 mm × 70 mm and is fixed in a 350 mm external concrete block wall with an insulated cavity. The house has an insulated solid concrete ground floor with a 20 mm quarry tile finish.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the two threshold drainage details in (b) are marked separately.'),
    '2': dict(page=2, title='Roof requirements and pitched roof structures', concept='pitched-roof-structures', stem='',
              note='Both roof types in (b) are required, each separately marked; the requirements and the recommendation are open responses.'),
    '3': dict(page=2, title='Renovating a house for solar gain', concept='solar-renovation',
              stem='The plan and elevation of a house built thirty years ago are shown in the accompanying drawing. The house is of traditional construction with a slated cut roof and a 300 mm external cavity wall of concrete block construction. The internal walls are of 100 mm solid block construction and the internal wall A-A is a load bearing wall. The front elevation is south facing. It has been decided to renovate the house to improve its thermal performance by: redesigning the external envelope to allow the increased penetration of sunlight into the interior of the house and redesigning the layout of the interior to optimise solar gain.',
              note='Original plan and elevation retained. Both printed aims are required; the designs are open responses.'),
    '4': dict(page=3, title='Sound insulation: principles, a party wall and a stud partition', concept='sound-insulation-party-wall', stem='',
              note='Original sketch retained. All three printed principles in (a) are required, each separately marked.'),
    '5': dict(page=3, title='Hollow block wall U-value and external insulation thickness', concept='hollow-block-wall-u-value',
              stem='The external wall of a house built in the 1970s is constructed using a single leaf 215 mm hollow concrete block. The wall is rendered externally and plasterboard is fixed to the internal surface using dabs of plaster adhesive, as shown in the accompanying sketch.',
              note='All printed data are retained in the original question. Part (b) uses the resistance from (a); the scheme’s worked answers are U = 1.563599 W/m²K and 113 mm of expanded polystyrene.'),
    '6': dict(page=4, title='A low environmental impact house', concept='low-impact-cedar-house',
              stem='The elevation and ground floor plan of a house are shown. The house has two additional bedrooms and a bathroom upstairs. The external leaf is of concrete block and cedar cladding construction, as shown. The house is designed to have low environmental impact.',
              note='Original elevation and plan retained. Features are open responses; all three printed considerations in (b) are required.'),
    '7': dict(page=4, title='Chimney stack through a slated roof', concept='chimney-stack-roof-section',
              stem='A concrete block chimney stack with a sand/cement render passes through a cut roof which is slated and is pitched at 45°, as shown in the sketch.',
              note='Original sketch retained. The chimney, flashing and roof menus are marking menus, not printed choices.'),
    '8': dict(page=4, title='Zoned stove heating with a solar collector', concept='zoned-stove-solar-heating', stem='',
              note='Original sketches retained. The listed components are marking menus, not printed choices.'),
    '9': dict(page=5, title='Thermal bridges at the circled junctions', concept='thermal-bridge-junctions',
              stem='Careful design detailing is necessary in order to design a building envelope which is free of thermal/cold bridges. The drawing shows an outline section through a single storey house having a 350 mm external concrete block wall with an insulated cavity. The ground floor is an insulated solid concrete floor.',
              note='Original section with four circled junctions retained: the eaves, the window head, the window cill and the floor. Part (a) is a closed choice of any three: one card holding all four, named by the scheme’s own words for each detail.'),
    '10': dict(page=5, title='Passive House design and MHRV', concept='passive-house-mhrv', stem='',
               note='Original sketch retained. Part (a) is a closed choice of any two of the three printed items: one card holding all three.'),
}
ALT = dict(page=5, title='Sustainable urban neighbourhoods (alternative Question 10)', concept='urban-neighbourhoods',
           stem='“A good neighbourhood is one where people can easily satisfy daily needs whilst feeling safe to do so. The most successful neighbourhoods are well connected – to employment centres, or places where people spend their leisure time. They are places where people can live at any stage of their lives – regardless of physical ability or social status. Successful neighbourhoods also tend to have a wide variety of things to do within them and have a strong connection to the area in which they sit – be it historical, cultural or visual.” Urban Design Manual – A Best Practice Guide (2009). Department of the Environment, Heritage and Local Government..',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately.')
SCHEME_PAGES = {'1': [4, 5, 30], '2': [6, 7, 31], '3': [8, 9, 10, 11, 32], '4': [11, 12, 13, 33], '5': [14, 15, 34], '6': [16, 17, 18, 19, 35],
                '7': [20, 36], '8': [21, 22, 37], '9': [22, 23, 38], '10': [24, 25, 26, 39], '10-alt': [26, 27, 28, 40]}
D = cp.Draft(HERE, 2011, 'higher', ('d02fe420b8c4aabdf284fc4551d08af11e98fc0b3447a29f8b98ecf78e7f2be8',
                                    'd71697473ec9446fc95f06bb2c855e31c25047b741324af6f7a2c8b6f5ea8bef'), 0, QUESTIONS, SCHEME_PAGES, alt=ALT)
row, add, compose, parts, anyn = D.row, D.add, D.compose, D.parts, D.anyn
D.figures({
    'q1-original': D.paper(2, [30, 50, 580, 276]), 'q2-original': D.paper(2, [30, 276, 580, 429]),
    'q3-original': D.paper(2, [30, 429, 580, 790]), 'q4-original': D.paper(3, [30, 50, 580, 321]),
    'q5-original': D.paper(3, [30, 321, 580, 790]), 'q6-original': D.paper(4, [30, 50, 580, 305]),
    'q7-original': D.paper(4, [30, 305, 580, 527]), 'q8-original': D.paper(4, [30, 527, 580, 790]),
    'q9-original': D.paper(5, [30, 50, 580, 262]), 'q10-original': D.paper(5, [30, 262, 580, 526]),
    'q10-alt-original': D.paper(5, [30, 550, 580, 790]),
    'q1-section': D.composite((4, [40, 60, 585, 575]), (5, [40, 60, 585, 762])),
    'q2-requirements': D.scheme(6, [40, 60, 585, 345]),
    'q2-roofs': D.composite((6, [40, 345, 585, 780]), (7, [40, 60, 585, 425])), 'q2-recommendation': D.scheme(7, [40, 425, 585, 780]),
    'q3-design': D.composite((8, [40, 60, 585, 780]), (9, [40, 60, 585, 780]), (10, [40, 60, 585, 578])),
    'q3-reasons': D.composite((10, [40, 578, 585, 780]), (11, [40, 60, 585, 220])),
    'q4-principles': D.composite((11, [40, 220, 585, 780]), (12, [40, 60, 585, 214])),
    'q4-party-wall': D.scheme(12, [40, 214, 585, 680]), 'q4-partition': D.scheme(13, [40, 60, 585, 780]),
    'q5-calculation': D.scheme(14, [40, 60, 585, 607]),
    'q5-walls': D.composite((14, [40, 607, 585, 780]), (15, [40, 60, 585, 780])),
    'q6-features': D.composite((16, [40, 60, 585, 780]), (17, [40, 60, 585, 204])),
    'q6-importance': D.composite((17, [40, 204, 585, 780]), (18, [40, 60, 585, 780]), (19, [40, 60, 585, 232])),
    'q7-section': D.scheme(20, [40, 60, 585, 780]),
    'q8-system': D.scheme(21, [40, 60, 585, 780]), 'q8-siting': D.scheme(22, [40, 60, 585, 435]),
    'q9-scheme': D.composite((22, [40, 435, 585, 780]), (23, [40, 60, 585, 659])),
    'q10-principles': D.composite((24, [40, 60, 585, 780]), (25, [40, 60, 585, 282]), (25, [40, 282, 405, 366]), (25, [405, 280, 585, 392])),
    'q10-mhrv': D.composite((25, [40, 366, 405, 389.5]), (25, [40, 389.5, 585, 633])),
    'q10-advantages': D.composite((25, [40, 633, 585, 780]), (26, [40, 60, 585, 345])),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p30 (printed 2): (a) best eleven points × 4 (drawing 3, annotation 1) = 44 and scale and drafting 8 = 52; (b) two design details × 4 = 8. Complete 60.'
S1 = 'One required section and two required threshold details. The detail list is a marking menu, not a printed choice.'
T1A = 'To a scale of 1:10, draw a vertical section through the centre of the door. The section should show the typical construction details from 500 mm below finished floor level, through the threshold, the door, the doorframe and the external wall to a level 300 mm above the concrete lintels over the doorframe.'
T1B = 'Show on the drawing the design detailing that ensures that rainwater is removed from the threshold area.'
A1 = add('1', 'a', '(a)', T1A,
         [row('details', 'Any 11 points x 4 marks', 44, 'Best eleven points, 4 each (drawing 3, annotation 1). Menu: blockwork; at least 150 mm hardcore with sand blinding; radon barrier or DPM; at least 150 mm floor insulation; subfloor; tile; sloped concrete cill; DPC behind and under the cill; drainage channel; level surface; a 15 mm proprietary threshold; door and seal; frame head; airtightness; lintels; stepped DPC; cavity insulation; internal and external render.', list(range(0, 45, 4))),
          row('presentation', 'Scale & Drafting', 8, 'Scale and drafting of the section.')],
         ['cons-1-5', 'cons-3-7', 'cons-4-2', 'cons-3-4'], ['question-1-drawing-questions', 'doors', 'floors', 'walls'], 'q1-section',
         'Scaled drawing (1.5) of an entrance door and threshold (3.7) on a solid ground floor (4.2) under lintels and a stepped DPC (3.4).', B1, S1)
B1b = add('1', 'b', '(b)', T1B,
          [row('drainage', 'Two Design details', 8, 'Two details, 4 each, shown on the drawing as in the scheme’s model sections: such as a drainage channel at the threshold; a sloped concrete cill; a level, accessible surface.')],
          ['cons-3-7', 'cons-1-2'], ['doors', 'planning-sustainability-environment'], 'q1-section', 'An accessible door threshold (3.7, 1.2).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p31 (printed 3): (a) three requirements × (notes 4 + sketches 4) = 24; (b) two roof types, each name 3, stability detail 6 and three dimensions 3 = 24; (c) recommendation 4 and two reasons × 4 = 12. Complete 60.'
S2 = 'Both roof types in (b) are required, each separately marked; not a choice.'
ROOF = (['cons-3-8'], ['roofs'])
T2A = 'Discuss in detail, using notes and freehand sketches, three functional requirements of a roof suitable for a dwelling house.'
T2B = 'Using notes and freehand sketches, show two different types of pitched roof structure suitable for a dwelling house having an internal span of 6.0 metres and one internal load-bearing wall. For each roof type, indicate the design detailing that ensures the structural stability of the roof and include the typical dimensions of three structural members.'
T2C = 'Recommend a preferred roof structure for a dwelling house and give two reasons in support of your recommendation.'
A2 = add('2', 'a', '(a)', T2A,
         [row(f'requirement-{i}', f'Functional requirement {i}', 8, note) for i, note in [
             (1, 'Notes 4 and sketches 4. Such as: weather resistance against rain, snow, wind and sun; structural stability under dead and live loads and lateral movement.'),
             (2, 'A second, different requirement: notes 4 and sketches 4. Such as: durability, with boron-treated timbers; thermal insulation; ventilation against condensation and fungal attack.'),
             (3, 'A third, different requirement: notes 4 and sketches 4. Such as: fire resistance to allow escape; sound insulation; accommodating services such as the water tank and storage.')]],
         ['cons-3-8', 'cons-3-9'], ['roofs'], 'q2-requirements', 'Roof forms (3.8) and coverings (3.9).', B2, S2)
B2b = add('2', 'b', '(b)', T2B,
          [row('roof-1', 'Name of roof type 1', 12, 'Name 3, stability detail in sketch and note 6, three typical dimensions 3. Such as, a traditional cut purlin roof: the purlin supporting the rafters, struts carrying the purlin to the load-bearing wall; rafters 200 × 50, ceiling joists 225 × 50, purlin 175 × 75 mm.'),
           row('roof-2', 'Roof type 2', 12, 'A second, different type: name 3, stability detail 6, three dimensions 3. Such as, a prefabricated W truss: triangulation, with webs in compression and tension making a rigid structure; rafters 170 × 45, ceiling tie 220 × 45, webs 120 × 45 mm, gang nail plates.')],
          *ROOF, 'q2-roofs', 'Roof forms, trusses and trussed rafters (3.8).', B2, S2)
C2 = add('2', 'c', '(c)', T2C,
         [row('recommendation', 'Recommendation', 4, 'A preferred roof structure, cut or trussed.'),
          row('reason-1', 'Reason 1', 4, 'A reason matching the choice. Such as, cut roof: the attic can later be converted to living space; no mechanical lifting or specialist manufacture.'),
          row('reason-2', 'Reason 2', 4, 'A second, different reason. Such as, trussed roof: fast to erect with little time on site; economical, stress-graded timber; guaranteed structural integrity; no internal load-bearing wall needed.')],
         *ROOF, 'q2-recommendation', 'The choice of roof structure (3.8).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-roofs', B2, S2, parts(('a', T2A), ('b', T2B), ('c', T2C)))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p32 (printed 4): (a) external envelope note 10 + sketch 10 and layout note 10 + sketch 10 = 40; (b) reasons for the envelope 10 and for the layout 10 = 20. Complete 60.'
S3 = 'Both printed aims are required; the designs are open responses.'
SUN = (['cons-6-4', 'cons-3-6', 'cons-6-2'], ['passive-design', 'windows-light', 'heat-loss-insulation'])
T3A = 'For each of the above, show using notes and freehand sketches, a revised design detailing that will improve the thermal performance of the dwelling house.'
T3B = 'For each of the above, discuss in detail the reasons for your proposed design choices when redesigning the house shown.'
A3 = add('3', 'a', '(a)', T3A,
         [row('envelope', 'Design detailing :- External envelope', 20, 'Note 10 and sketch 10. Such as: more high-performance low-e glazing on the south and west in thermally broken frames, sealed airtight; walls insulated to 0.21 W/m²K by external insulation, cavity fill or dry lining; more attic insulation; an insulated floor with upstands at the walls; rooflights or a sky tunnel.'),
          row('layout', 'Design detailing :- Layout', 20, 'Note 10 and sketch 10. Such as: rarely used rooms, the bathroom and a bedroom moved to the north; the dining room moved to the south; open plan on the south side, with lintels in wall A-A; a tiled kitchen floor for thermal mass.')],
         *SUN, 'q3-design', 'Solar gain (6.4) through glazing (3.6) in an insulated envelope (6.2).', B3, S3)
B3b = add('3', 'b', '(b)', T3B,
          [row('envelope-reasons', 'Reason - external envelope', 10, 'Such as: south and west glazing admits more sunlight and heat; tall windows give deeper penetration; low-e, argon-filled glazing and thermally broken frames keep the heat; walls upgraded to the regulations and every leakage route sealed.'),
           row('layout-reasons', 'Reason - layout', 10, 'Such as: living rooms on the sunny south side gain morning and day-long sun; open plan lets heated air move freely; rooflights with a raised ceiling let sunlight in deeper; thermal mass stores the heat.')],
          *SUN, 'q3-reasons', 'Solar gain (6.4) through glazing (3.6) in an insulated envelope (6.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-design', B3, S3, parts(('a', T3A), ('b', T3B)))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p33 (printed 5): (a) three printed principles × (notes 4 + sketches 4) = 24; (b) two reasons × 4 and the revised party wall note 4 + sketch 4 = 16; (c) the revised partition note, sketch, principles, materials and dimensions × 4 = 20. Complete 60.'
S4 = 'All three printed principles in (a) are required, each separately marked; not a choice.'
SOUND = (['cons-8-3'], ['sound'])
T4A = 'Discuss in detail, using notes and freehand sketches, the importance of each of the following in reducing the transmittance of sound in a dwelling house: mass; completeness; isolation.'
T4B = 'The party wall between the two semi-detached houses shown in the sketch is of concrete block construction. The occupants of one house can hear everyday sounds from the adjoining house. Discuss two possible reasons why sound is transmitted between the houses, and using notes and freehand sketches, show the revised design detailing that would improve the sound insulation properties of the party wall between both houses.'
T4C = 'To reduce the transmittance of sound through a timber stud partition between two adjoining bedrooms on the first floor in one of the houses, it has been decided to redesign the partition. Show, using notes and freehand sketches, a revised design for the stud partition and outline the sound insulation principles associated with the each design detail. Specify the materials used and give their typical dimensions.'
A4 = add('4', 'a', '(a)', T4A,
         [row('mass', 'Mass', 8, 'Notes 4 and sketches 4. Such as: by the mass law, sound insulation rises with mass per unit area — about 5 dB for each doubling in practice; sand pugging between joists; solid, heavy party walls.'),
          row('completeness', 'Completeness', 8, 'Notes 4 and sketches 4. Such as: small gaps around pipes, doorframes, windows and floor junctions let sound through; mortar joints filled and walls plastered; one unsealed door outweighs its area.'),
          row('isolation', 'Isolation', 8, 'Notes 4 and sketches 4. Such as: discontinuous construction — staggered studs, floating floors, double windows at least 150 mm apart — breaks the paths for flanking transmission.')],
         *SOUND, 'q4-principles', 'Airborne and impact sound insulation (8.3).', B4, S4)
B4b = add('4', 'b', '(b)', T4B,
          [row('reason-1', 'Reason 1', 4, 'Such as: poor workmanship leaving gaps; mortar joints not completely filled.'),
           row('reason-2', 'Reason 2', 4, 'A second, different reason. Such as: too little mass in the party wall; its junctions with the side walls or roof not sealed.'),
           row('note', 'Design detail note', 4, 'Such as: a sound insulating panel or extra layers of plasterboard with staggered joints; the party wall carried up and sealed in the attic with mineral wool; gaps sealed; joists not bearing on the party wall.'),
           row('sketch', 'Design detail sketch', 4, 'A sketch of the revised party wall, as in the scheme’s model details.')],
          ['cons-8-3', 'cons-3-3'], ['sound', 'walls'], 'q4-party-wall', 'Sound insulation (8.3) of a party wall (3.3).', B4, S4)
C4 = add('4', 'c', '(c)', T4C,
         [row('note', 'Revised design - note', 4, 'Such as: a double stud partition with separate sole and head plates for each side.'),
          row('sketch', 'Revised design – sketch', 4, 'A sketch of the double, isolated partition, as in the scheme’s model.'),
          row('principles', 'Sound insulation principle 1&2', 4, 'Such as: mass — more layers of plasterboard; isolation — the two leaves unconnected, with mineral wool; completeness — gaps sealed and the door fitted with an acoustic gasket.'),
          row('materials', 'Materials used', 4, 'Such as: timber studs, plasterboard and mineral wool insulation.'),
          row('dimensions', 'Typical dimensions', 4, 'Such as: studs 75 × 50 mm at 400 mm centres; 2 × 12.7 mm plasterboard; 60 mm mineral wool on each side.')],
         ['cons-8-3', 'cons-4-5'], ['sound', 'doors'], 'q4-partition', 'Sound insulation (8.3) of a stud partition (4.5).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-party-wall', B4, S4, parts(('a', T4A), ('b', T4B), ('c', T4C)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p34 (printed 6): (a) nine points × 3 = 27 (tabulation, six resistances, total resistance, U-value); (b) five steps × 3 = 15; (c) two disadvantages with discussion × 6 and the recommended wall, notes and sketches 3 × 2 = 18. Complete 60.'
S5 = 'No printed choice. Part (b) uses the resistance from (a); the recommended wall in (c) is an open response.'
DATA5 = ('External render thickness 15 mm; Concrete hollow block thickness 215 mm; Air space between plasterboard and block width 10 mm; Internal plasterboard thickness 12 mm. '
         'Thermal data of external wall of house: Resistance of external surface (R) 0.048 m2 °C/W; Resistivity of external render (r) 2.170 m °C/W; Resistance of hollow block (R) 0.210 m2 °C/W; '
         'Resistance of airspace (R) 0.170 m2 °C/W; Conductivity of plasterboard (k) 0.160 W/m °C; Resistance of internal surface (R) 0.104 m2 °C/W.')
T5A = 'Calculate the U-value of the external hollow block wall, given the following data: ' + DATA5
T5B = 'It is proposed to upgrade the thermal properties of the wall by fixing expanded polystyrene to the external surface. Given the thermal conductivity (k) of expanded polystyrene as 0.037 W/m °C, calculate the thickness of expanded polystyrene required to achieve a U-value of 0.27 W/m2 °C to meet the requirements of the current Building Regulations.'
T5C = 'In the past, many dwelling houses were built using hollow concrete blocks, as outlined at 5 (a) above. Discuss two disadvantages of this type of construction, and using notes and freehand sketches, recommend a preferred external wall type suitable for a contemporary house.'
A5 = add('5', 'a', '(a)', T5A,
         [row('tabulation', 'Correct tabulation', 3, 'The calculation set out in a table of material, conductivity or resistivity, thickness and resistance.'),
          row('resistances', '9 points × 3 marks for each point', 18, 'Six resistances, 3 each: external surface 0.048 (given); render 0.015 × 2.170 = 0.03255; hollow block 0.210 (given); air space 0.170 (given); plasterboard 0.012/0.160 = 0.075; internal surface 0.104 (given). All in m²°C/W.', list(range(0, 19, 3))),
          row('total-resistance', 'Total Resistance', 3, 'Total resistance, the sum of R = 0.63955 m²°C/W.', [0, 3]),
          row('u-value', 'U Value (1 mark for the formula)', 3, 'U = 1/Rt = 1 ÷ 0.63955 = 1.563599 W/m²K (1 mark for the formula).')],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Thermal resistance, conductivity and transmittance (6.1).', B5, S5)
B5b = add('5', 'b', '(b)', T5B,
          [row('target', 'Resistance for U-value of 0.27 (2 marks for formula R=1/U)', 3, 'R = 1/U = 1 ÷ 0.27 = 3.703 m²K/W (2 marks for the formula).'),
           row('existing', 'Existing Resistance from part (a)', 3, 'The existing resistance, 0.63955 m²K/W.'),
           row('difference', 'Difference in Resistances', 3, 'Difference = 3.703 − 0.63955 = 3.06345 m²K/W.'),
           row('formula', 'Application of Formula R = T/k (1 mark for formula)', 3, 'R = T/k solved for T: T = R × k = 3.06345 × 0.037 (1 mark for the formula).'),
           row('thickness', 'Required thickness of insulation', 3, 'T = 0.1133476 metres: 113 mm of expanded polystyrene.')],
          ['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation'], 'q5-calculation', 'Thermal transmittance (6.1) and insulating materials (6.2).', B5, S5)
C5 = add('5', 'c', '(c)', T5C,
         [row('disadvantage-1', 'Disadvantage 1 and discussion', 6, 'Such as: each hollow block and its ribs form thermal bridges; no insulation in the block or the wall, so heat is lost.'),
          row('disadvantage-2', 'Disadvantage 2 and discussion', 6, 'A second, different disadvantage. Such as: impractical to fill with insulation retrospectively; a risk of damp penetrating the hollow block.'),
          row('recommendation', 'Recommendation and notes/sketches ( 3 × 2 marks)', 6, 'Such as: a 350 mm cavity wall with 100 mm rigid insulation and ties; hollow block filled with insulation and 300 mm external insulation with acrylic render; 225 mm block on flat with 300 mm external insulation; or timber frame with a block outer leaf.')],
         ['cons-3-3', 'cons-6-2'], ['walls', 'heat-loss-insulation'], 'q5-walls', 'External walls (3.3) and their insulation (6.2).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p35 (printed 7): (a) three design features × (note 8 + sketch 6) = 42; (b) three printed considerations × 6 = 18. Complete 60.'
S6 = 'The features are open responses; all three printed considerations in (b) are required.'
GREEN = (['cons-1-2', 'cons-6-4'], ['sustainability-the-environment'])
T6A = 'With reference to the design shown, discuss in detail, using notes and freehand sketches, three features of the design that ensure the house has low environmental impact.'
T6B = 'Discuss in detail the importance of each of the following when designing environmentally sustainable housing: form of the house; materials and labour; design for lifetime use.'
A6 = add('6', 'a', '(a)', T6A,
         [row(f'feature-{i}', f'Design feature {i}', 14, note) for i, note in [
             (1, 'Note 8 and sketch 6. Such as: modest scale on a small footprint, with mixed block and timber walls and bedrooms in the attic, lowering embodied energy.'),
             (2, 'A second, different feature: note 8 and sketch 6. Such as: rainwater harvesting in above-ground tanks for gardens and flushing; solar panels on the south roof for 40–60% of hot water.'),
             (3, 'A third, different feature: note 8 and sketch 6. Such as: roof lights giving three times the light of vertical glazing; a wood or pellet stove, draught lobby or zoned heating.')]],
         ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-features',
         'Sustainable design of the built environment (1.2), solar gain (6.4) and insulation (6.2).', B6, S6)
B6b = add('6', 'b', '(b)', T6B,
          [row('form', 'Form of house', 6, 'Such as: a narrow plan with south-facing living rooms one room wide; economical use of space with small rooms; a pitched roof giving attic rooms and solar panels at 45°.'),
           row('materials', 'Materials and labour', 6, 'Such as: local, renewable, naturally durable timber cladding such as larch; less concrete and low-carbon GGBS concrete; local stone and timber; local labour building skills and communities.'),
           row('lifetime', 'Design for lifetime use', 6, 'Such as: universal design — a ramp, 800 mm doors, no ground floor steps, a ground floor bedroom and accessible bathroom, switches at 900–1200 mm.')],
          *GREEN, 'q6-importance', 'Sustainable design of the built environment (1.2) with solar gain (6.4).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b], 'q6-features', B6, S6, parts(('a', T6A), ('b', T6B)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p36 (printed 8): (a) eleven points × 4 (drawing 3, annotation 1) — best four of the chimney stack, three of the flashings and four of the roof structure — = 44 and scale and drafting 8 = 52; (b) two downdraught details × 4 = 8. Complete 60.'
S7 = 'One required section and two required details. The detail lists are marking menus, not printed choices.'
T7A = 'To a scale of 1:5, draw a vertical section through the chimney stack and roof, showing the typical details of the chimney stack, flue, chimney capping and portion of the roof structure. Show clearly the design details necessary to prevent the penetration of water between the chimney stack and the adjoining roof surface.'
T7B = 'On your drawing, show two design details that will help prevent the occurrence of a downdraught in a chimney as shown. Include dimensions as appropriate.'
A7 = add('7', 'a', '(a)', T7A,
         [row('chimney', 'Chimney stack (any 4)', 16, 'Best four, 4 each: blockwork; render; flue liners; fill; chimney capping.', list(range(0, 17, 4))),
          row('flashing', 'Flashing (any 3)', 12, 'Best three, 4 each: cover flashing; under flashing; lead flashing to the rear gutter; lead apron or tray.', list(range(0, 13, 4))),
          row('roof', 'Roof structure (any 4)', 16, 'Best four, 4 each: fillet piece or gutter; rafter; felt or breathable membrane; battens; slates; trimmer.', list(range(0, 17, 4))),
          row('presentation', 'Scale & Drafting', 8, 'Scale and drafting of the section.')],
         ['cons-1-5', 'cons-5-7', 'cons-3-9', 'cons-3-10'], ['question-1-drawing-questions', 'fireplaces-fire-prevention', 'roofs'], 'q7-section',
         'Scaled drawing (1.5) of a chimney stack (5.7) through a slated roof (3.9) with its flashings at the abutment (3.10).', B7, S7)
B7b = add('7', 'b', '(b)', T7B,
          [row('detail-1', 'Design detail 1', 4, 'Show and identify a detail that helps prevent downdraught, with dimensions, as in the scheme’s model section.'),
           row('detail-2', 'Design detail 2', 4, 'A second, different detail, shown and identified as in the scheme’s model section.')],
          ['cons-5-7'], ['fireplaces-fire-prevention'], 'q7-section', 'Chimneys and flues (5.7).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p37 (printed 9): (a) best seven items × 4 (sketch 3, annotation 1) and two pipe sizes 4 — the scheme’s "8 × 4" — = 32; (b) best four solar items × 4 = 16; (c) location note 3 + sketch 3 and two factors × 3 = 12. Complete 60.'
S8 = 'The heating and solar components are marking menus, not printed choices.'
HEAT = (['cons-5-3', 'cons-5-2'], ['hot-water-space-heating'])
T8A = 'A wood burning stove, as shown in the sketch, is used to heat two independently controlled heating zones, one on each floor, in a two storey dwelling house. Using notes and a single-line diagram, show a typical design layout for the pipework necessary to independently heat each zone. Show three radiators on each floor, indicate the control valves and give the typical sizes of the pipework.'
T8B = 'It is proposed to connect a solar collector, as shown in the sketch below, to the system at 8(a) above to heat domestic water. Show a design layout for the pipework necessary to connect the solar collector to the existing system and outline the modifications required to the existing system to accommodate the solar collector.'
T8C = 'Using notes and freehand sketches, show a preferred location for the solar collector and discuss in detail two factors that influenced your choice of location.'
A8 = add('8', 'a', '(a)', T8A,
         [row('items', '8 × 4marks (Sketch 3 Annotation 1)', 28, 'Best seven items, 4 each (sketch 3, annotation 1); the scheme’s eighth 4 marks are the pipe sizes. Menu: wood burning stove; radiators; zone control mechanism; header or expansion tank; feed to it; cold feed from it; expansion pipe or vessel; flow and return pipes to the radiators; radiator valves; zone thermostats; pump and valves.', list(range(0, 29, 4))),
          row('sizes', 'Sizes of pipework (2 sizes)', 4, 'Two typical pipe sizes, 2 each, such as 22 mm flow and return, 15 mm upstands and 28 mm expansion.')],
         *HEAT, 'q8-system', 'Zoned heating systems (5.3) with a stove and cylinder (5.2).', B8, S8)
B8b = add('8', 'b', '(b)', T8B,
          [row('solar', 'Any 4 × 4marks (Sketch 3 Annotation 1)', 16, 'Best four, 4 each. Menu: solar panel; flow and return; pump; twin-coil cylinder; pipe sizes; temperature sensors; control panel; expansion vessel; thermal reducing vessel; safety valve; mixing valve. Modifications such as a 300 litre twin-coil cylinder, a blending valve and an electronic control system.', list(range(0, 17, 4)))],
          ['cons-5-2', 'cons-6-4'], ['hot-water-space-heating', 'sustainability-the-environment'], 'q8-system', 'Hot water from solar gain (5.2, 6.4).', B8, S8)
C8 = add('8', 'c', '(c)', T8C,
         [row('location', 'Location (note 3 marks, sketch 3 marks)', 6, 'Note 3 and sketch 3. Such as: on the roof, integrated or on-roof, or on a wall or ground mount with adjustable tilt.'),
          row('factor-1', 'Factor 1', 3, 'Such as: orientation — facing south, within 15° east or west of south.'),
          row('factor-2', 'Factor 2', 3, 'A second, different factor. Such as: an inclination of about 45° in Ireland; no shading from trees, chimneys or buildings; the weight on the roof.')],
         ['cons-6-4'], ['sustainability-the-environment'], 'q8-siting', 'Solar heat gain and siting a collector (6.4).', B8, S8)
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-system', B8, S8, parts(('a', T8A), ('b', T8B), ('c', T8C)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p38 (printed 10): (a) any three of the four circled locations × (notes 6 + sketches 10) = 48; (b) two advantages × 6 = 12. Complete 60.'
S9 = 'Choice is not a route: part (a) (any three of the FOUR circled locations) is ONE card with one any-three group over the four junctions, each named by the scheme’s own words for its detail; its figure carries the whole of the scheme’s answer.'
T9A = 'Select any three locations from those circled on the sketch, and show clearly, using notes and annotated freehand sketches, the typical design detailing which will prevent the formation of thermal bridges at each location selected.'
T9B = 'Discuss in detail two advantages of designing a building envelope which is free of thermal bridges.'
LOCATIONS9 = [('Wall plate and eaves', 'the eaves (Fig 9.3): a cavity closer or high-density fireproof insulation; the gap between the wall plate and the eaves vent completely filled with insulation; 450 mm of insulation between and over the ceiling joists.'),
              ('Insulated steel lintel', 'the window head (Figs 9.2 and 9.5): a high-density block of insulation closing the cavity; an insulated steel lintel with internal insulation; gaps sealed with tape or flexible sealant.'),
              ('Sill', 'the window cill (Fig 9.1): a proprietary cavity closer or block of insulation behind the sill separating the leaves; thermally broken, low-e, argon-filled glazing.'),
              ('Floor insulation', 'the floor and wall junction (Fig 9.4): perimeter insulation of R at least 0.75 m²K/W; wall insulation taken at least 225 mm below the top of the floor; all junctions sealed airtight.')]
A9 = add('9', 'a', '(a)', T9A,
         [anyn('locations', '3 locations', 3, 16, LOCATIONS9, 'Any three of the four circled locations, each notes 6 and sketches 10 = 16, showing the insulation kept continuous so that no thermal bridge forms.')],
         ['cons-6-2', 'cons-3-10', 'cons-3-6', 'cons-4-2'], ['heat-loss-insulation', 'roofs', 'windows-light', 'floors'], 'q9-scheme',
         'Every location is a thermal-bridge detail (6.2): at the eaves (3.10), the window head and cill (3.6) and the ground floor (4.2).', B9, S9)
B9b = add('9', 'b', '(b)', T9B,
          [row('advantage-1', 'Advantage 1', 6, 'Such as: less heat lost through the fabric at critical junctions; better thermal comfort.'),
           row('advantage-2', 'Advantage 2', 6, 'A second, different advantage. Such as: lower heating bills, fossil fuel use and CO₂; no condensation, damp or mould at cold spots — a healthier building.')],
          ['cons-6-2', 'cons-6-3'], ['heat-loss-insulation'], 'q9-scheme', 'Thermal bridges (6.2) and running costs (6.3).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b], 'q9-scheme', B9, S9, parts(('a', T9A), ('b', T9B)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p39 (printed 11): (a) any two of three printed items × (note 6 + sketch 6) = 24; (b) description, notes 10 + sketches 10 = 20; (c) two advantages and two disadvantages × 4 = 16. Complete 60.'
S10 = 'Choice is not a route: part (a) (any two of three printed items) is ONE card with an any-two group over the scheme headings; its figure and the complete-question figure carry all three items. The OR alternative is a separate Question 10 route.'
T10A = 'Using notes and freehand sketches, discuss in detail the importance of any two of the following in the design of a Passive House: foundations suitable for a Passive House; airtight building envelope; windows and glazing.'
T10B = 'A Mechanical Heat Recovery with Ventilation (MHRV) system for a Passive House is shown in the accompanying sketch. Using notes and freehand sketches, describe how such a system operates.'
T10C = 'Discuss in detail two advantages and two disadvantages of using a Mechanical Heat Recovery with Ventilation system in a domestic dwelling.'
ITEMS10 = [('Foundations suitable for passive house', 'a well insulated passive slab wrapped in 100–400 mm EPS, with a reinforced ring beam and slab and no internal foundations; on compacted, blinded hardcore; cold bridges and heat loss to the ground eliminated.'),
           ('Airtight building envelope', 'a continuous airtight layer — the rule of the red line — with overlapped, sealed membranes and grommets at services, a service cavity, and leakage below 0.6 air changes per hour; it must be ventilated.'),
           ('Windows and Glazing', 'triple glazing with U below 0.8 W/m²K, low-conductivity spacers, low-e coatings and g ≥ 50; insulated, thermally broken frames; more south and less north glazing, with shading against summer overheating.')]
A10 = add('10', 'a', '(a)', T10A,
          [anyn('items', 'Notes and Sketches (4 × 6marks)', 2, 12, ITEMS10, 'Any two of the three printed items, each note 6 and sketch 6 = 12.')],
          ['cons-2-4', 'cons-6-5', 'cons-3-6', 'cons-6-2'], ['passive-design', 'foundations', 'condensation-air-tightness', 'windows-light'], 'q10-principles',
          'The union of the three printed items: the insulated foundation (2.4, 6.2), airtightness (6.5) and windows and glazing (3.6).', B10, S10)
B10b = add('10', 'b', '(b)', T10B,
           [row('description', 'Description notes and sketches (2 × 10 marks)', 20, 'Notes 10 and sketches 10. Such as: continuous fresh air; stale air extracted from kitchens and bathrooms passes a heat exchanger warming the incoming fresh air without mixing; the unit downstairs in the utility room so filters are changed every six months.')],
           ['cons-6-5'], ['passive-design', 'condensation-air-tightness'], 'q10-mhrv', 'Ventilation with heat recovery (6.5).', B10, S10)
C10 = add('10', 'c', '(c)', T10C,
          [row('advantage-1', 'Advantage 1', 4, 'Such as: a continuous, controlled supply of fresh air to all rooms; up to 93% of the heat recovered.'),
           row('advantage-2', 'Advantage 2', 4, 'A second, different advantage. Such as: lower humidity, mould and allergens; less fossil fuel to heat air; only two breaches of the fabric.'),
           row('disadvantage-1', 'Disadvantage 1', 4, 'Such as: complete dependence on a mechanical, electrical system; filters to replace regularly.'),
           row('disadvantage-2', 'Disadvantage 2', 4, 'A second, different disadvantage. Such as: high installation cost and specialist skill; windows kept closed; noisy fans if ducts are undersized; no open fire.')],
          ['cons-6-5'], ['passive-design', 'condensation-air-tightness'], 'q10-advantages', 'Ventilation with heat recovery (6.5).', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-principles', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p40 (printed 12): discussion of the statement, three points × (4 + 6) = 30; three guidelines × (4 + 6) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately, so each is its own task and the complete card composes them.'
TAA = 'Discuss the above statement in detail.'
TAB = 'Propose three guidelines for best practice that would help create sustainable urban neighbourhoods.'
TALL = 'Discuss the above statement in detail and propose three guidelines for best practice that would help create sustainable urban neighbourhoods.'
NEIGH = (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'])
AA = add('10', 'discussion', ' — discussion', TAA,
         [row(f'point-{i}', f'Discussion – point {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: a good neighbourhood is mixed, compact and people-centred, with good public transport and less dependence on the car; safe streets and public spaces with passive surveillance.'),
             (2, 'Point 4 and discussion 6. Such as: well connected and walkable, with safe green routes for walking and cycling to school and work.'),
             (3, 'Point 4 and discussion 6. Such as: integrated communities for every stage of life, built to universal design; a strong local identity and heritage; a wide mix of shops, work places and leisure. Three distinct, well-argued points are needed.')]],
         *NEIGH, None, 'Planning sustainable neighbourhoods (1.2, 1.3).', BALT, SALT, alt=True)
AB = add('10', 'guidelines', ' — guidelines', TAB,
         [row('guideline-1', 'Guideline 1 (4 for point, 6 for discussion)', 10, 'Point 4 and discussion 6. Such as: renewable energy, on-site generation and energy-saving fittings; grants and education for sustainable, low embodied energy design.'),
          row('guideline-2', 'Guideline 2 (4 for point, 6 for discussion)', 10, 'Point 4 and discussion 6. Such as: car pooling and sharing; neighbourhoods where people can spend their whole lives, supported by a culture of mutual care.'),
          row('guideline-3', 'Guideline 2 (4 for point, 6 for discussion)', 10, 'The third guideline: point 4 and discussion 6 (the scheme prints this row as a second "Guideline 2"). Such as: exemplars of good practice from the Urban Design Manual; urban living promoted as desirable and communal. Three distinct guidelines are needed.')],
         *NEIGH, None, 'Planning sustainable neighbourhoods (1.2, 1.3).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, TALL, labels=['Discussion of the statement', 'Three guidelines'], alt=True)

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and four other questions (300 marks); all question banks retained, no full-exam Cartesian cards.'),
          (3, 'one of', 'Q4(c) "in one of the houses": the house with the partition, not a candidate choice.'),
          (5, 'Select', 'Q9(a) closed choose-three of the four circled locations: one card with an any-three group (choice is not a route).'),
          (5, 'any three', 'Q9(a) the same any-three group.'),
          (5, 'any two', 'Q10(a) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
          (5, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.'),
          (5, 'or', 'Alternative Question 10 quotation ("employment centres, or places"): not a candidate choice.'),
          (5, 'any stage', 'Alternative Question 10 quotation ("at any stage of their lives"): not a candidate choice.'),
          (5, 'or', 'Alternative Question 10 quotation ("physical ability or social status"): not a candidate choice.'),
          (5, 'or', 'Alternative Question 10 quotation ("historical, cultural or visual"): not a candidate choice.')]
FINITE = {'9a': dict(choose=3, options=[h for h, _ in LOCATIONS9], cardId=A9['id'], groupRowId='locations'),
          '10a': dict(choose=2, options=[h for h, _ in ITEMS10], cardId=A10['id'], groupRowId='items')}
D.finish(LEDGER, FINITE, {})
