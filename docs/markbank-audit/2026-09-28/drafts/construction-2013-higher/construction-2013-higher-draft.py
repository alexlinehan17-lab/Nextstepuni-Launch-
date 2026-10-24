"""Draft the 2013 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 26-36). This paper was never carded: every task is added. Q9(a) "select any three locations"
from the four circled on the drawing and Q10(a) "any two of the following" are ONE card each with an
anyN group (choice is not a route). Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Closed-string stairs and landing section', concept='closed-string-stairs-section',
              stem='A closed-string wooden stairs leads to a landing with balustrade, as shown in the sketch. The landing has a hardwood tongued and grooved floor, on 200 mm × 50 mm joists with a plasterboard ceiling beneath. The newel post is 100 mm × 100 mm and the rise of a step should not exceed 175 mm.',
              note='Original sketch and specification retained. Construction, dimension, handrail height and scale/drafting marks belong to part (a); the two safety features in (b) are marked separately.'),
    '2': dict(page=2, title='Safety culture, ladders, windows and power tools on site', concept='site-safety-culture', stem='',
              note='All three printed items in (a) and both printed activities in (b) are required, each separately marked.'),
    '3': dict(page=2, title='A sunlit rear extension and revised ground floor', concept='rear-extension-sunlight',
              stem='The drawing shows the elevation, ground floor plan and portion of the rear garden of a two-storey semi-detached house. The rear wall B-B of the house is south facing. The external walls are 350 mm concrete block walls with an insulated cavity. All internal walls are of 100 mm solid block construction and the internal wall A-A is load-bearing. It is proposed to build a single-storey extension to the rear of the house to: allow increased sunlight into the interior of the house and improve the view to the rear garden.',
              note='Original elevation and plan retained. The design and layout are open responses; the scheme gives model designs.'),
    '4': dict(page=3, title='Wood-burning stove and solar collector heating', concept='stove-solar-heating',
              stem='It is proposed to use a wood-burning stove combined with a solar collector to provide central heating and hot water for a two-storey house.',
              note='Original sketch retained. The listed components are a marking menu, not a printed choice.'),
    '5': dict(page=3, title='Triple-glazed window U-values and window head detail', concept='window-u-values', stem='A section through a triple-glazed, high performance wooden window is shown at A. The frame is a thermally broken, insulated frame as shown. Two of the panes of glass have a low-emissivity (low-e) coating and the spaces between the panes are filled with argon gas. A section through a traditional single-glazed solid wooden window is shown at B.',
              note='All printed data are retained in the original question. Part (b) uses the U-values from (a); the scheme’s worked answers are U = 0.178 for the frame and U = 0.260495 for the glazing unit.'),
    '6': dict(page=4, title='A low-impact house for first-time buyers', concept='first-time-buyer-house',
              stem='The elevation and ground floor plan of a house are shown. The house has three bedrooms and a bathroom in the attic space. The external wall is of timber frame construction with a rendered concrete block outer leaf. The house is designed to have low environmental impact and be suitable for first-time buyers.',
              note='Original elevation and plan retained. Features are open responses; the scheme lists typical examples. All three printed considerations in (b) are required.'),
    '7': dict(page=4, title='Hearth and chimney for a wood-burning stove', concept='stove-hearth-chimney-section',
              stem='A chimney is designed to accommodate a modern wood-burning stove, as shown in the accompanying sketch. The chimney is located on an internal 215 mm solid concrete block wall between the living room and the kitchen. The flue from the stove to the main flue liner is 150 mm in diameter. The floor is an insulated solid concrete ground floor with a 20 mm floating hardwood finish. The dimensions of the stove are: height 700 mm, width 550 mm, depth 450 mm.',
              note='Original sketch and specification retained. Construction, dimension and scale/drafting marks belong to part (a); the flue liner joint in (b) is marked separately.'),
    '8': dict(page=4, title='Foundations: requirements, strip or raft, and concrete strength', concept='strip-raft-foundations', stem='',
              note='Original sketch retained. Both printed foundations in (b) are detailed, then one is recommended; not a choice.'),
    '9': dict(page=5, title='Preventing damp at the circled junctions', concept='damp-junctions',
              stem='A two-storey house, as shown in the drawing, is of timber frame construction with a rendered concrete block outer leaf. The chimney is also of rendered concrete block construction and both roofs are slated. Careful design detailing is required to prevent the penetration of dampness at the critical junctions circled in the drawing.',
              note='Original drawing with four circled junctions retained. Part (a) is a closed choice of any three of the four: one card holding all four, named by the scheme’s Location headings.'),
    '10': dict(page=5, title='Passive House principles and MHRV', concept='passive-house-mhrv', stem='',
               note='Original drawing retained. Part (a) is a closed choice of any two of the three printed items: one card holding all three.'),
}
ALT = dict(page=5, title='Sustainable housing beyond the energy rating (alternative Question 10)', concept='sustainable-housing-location',
           stem='“It is worth questioning whether a large house built to passive standards but remote from schools, shops or workplace, may in the long term be less sustainable than a modestly-sized home built within walking or cycling distance from daily destinations. The cost of energy required to power but also to transport goods and people from place to place will increasingly form part of the debate on sustainability. Passive living is not just a factor of the energy rating of the fabric of the house, but of an holistic approach to how we as a society think about dwelling, about the reuse of existing space in the first instance and about the appropriateness of scale”. From House to Home: a long conversation - Orla Murphy, School of Architecture, UCD HOUSE - AN EXHIBITION OF 21ST CENTURY HOMES IN THE WEST OF IRELAND (2012) AVAYA: 25-29 Mervue Business Park, Mervue, Galway',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately.')
SCHEME_PAGES = {'1': [4, 26], '2': [5, 6, 27], '3': [6, 7, 8, 28], '4': [8, 9, 29], '5': [10, 11, 30], '6': [12, 13, 14, 15, 31],
                '7': [15, 32], '8': [16, 17, 33], '9': [17, 18, 34], '10': [19, 20, 21, 22, 35], '10-alt': [23, 24, 36]}
D = cp.Draft(HERE, 2013, 'higher', ('ae15d2922194ca980c0f2cd89d011a1f8f54b26f2c9ef75a75538d84808b5693',
                                    '1c269d4c127339d06f4efe11b0d4cfcd0126230fde3aab345f89839aaf1abba3'), 0, QUESTIONS, SCHEME_PAGES, alt=ALT)
row, add, compose, parts, anyn = D.row, D.add, D.compose, D.parts, D.anyn
D.figures({
    'q1-original': D.paper(2, [30, 50, 580, 280]), 'q2-original': D.paper(2, [30, 280, 580, 510]),
    'q3-original': D.paper(2, [30, 510, 580, 796]), 'q4-original': D.paper(3, [30, 50, 580, 236]),
    'q5-original': D.paper(3, [30, 236, 580, 790]), 'q6-original': D.paper(4, [30, 50, 580, 328]),
    'q7-original': D.paper(4, [30, 328, 580, 577]), 'q8-original': D.paper(4, [30, 577, 580, 790]),
    'q9-original': D.paper(5, [30, 50, 580, 294]), 'q10-original': D.paper(5, [30, 294, 580, 580]),
    'q10-alt-original': D.paper(5, [30, 605, 580, 790]),
    'q1-section': D.scheme(4, [45, 50, 575, 800]),
    'q2-culture': D.composite((5, [45, 50, 575, 536]), (5, [45, 536, 440, 585])),
    'q2-risks': D.composite((5, [45, 585, 440, 790]), (5, [440, 540, 575, 760]), (6, [45, 50, 575, 258])),
    'q2-tools': D.scheme(6, [45, 258, 575, 480]),
    'q3-design': D.composite((6, [45, 483, 575, 800]), (7, [45, 50, 575, 310]), (7, [45, 310, 430, 462]), (7, [430, 312, 575, 488])),
    'q3-reasons': D.composite((7, [45, 462, 430, 800]), (7, [430, 525, 575, 720]), (8, [45, 50, 575, 150])),
    'q4-system': D.scheme(8, [45, 148, 575, 800]),
    'q4-siting': D.scheme(9, [45, 50, 575, 452]), 'q4-advantages': D.scheme(9, [45, 452, 575, 790]),
    'q5-calculation': D.scheme(10, [45, 50, 575, 790]),
    'q5-comparison': D.scheme(11, [45, 60, 575, 556]), 'q5-head': D.scheme(11, [45, 556, 575, 800]),
    'q6-features': D.composite((12, [45, 50, 575, 800]), (13, [45, 60, 575, 800]), (14, [45, 50, 575, 262])),
    'q6-buyers': D.composite((14, [45, 262, 575, 800]), (15, [45, 60, 575, 300])),
    'q7-section': D.scheme(15, [25, 300, 575, 800]),
    'q8-requirements': D.composite((16, [45, 60, 575, 255]), (16, [45, 255, 390, 278])),
    'q8-foundations': D.composite((16, [45, 276, 390, 371]), (16, [390, 252, 575, 371]), (16, [45, 371, 575, 800])), 'q8-concrete': D.scheme(17, [45, 50, 575, 305]),
    'q9-locations': D.composite((17, [45, 305, 575, 800]), (18, [45, 60, 370, 172]), (18, [370, 80, 575, 263])),
    'q9-materials': D.composite((18, [45, 170, 370, 263]), (18, [45, 263, 575, 420])),
    'q9-moisture': D.scheme(18, [45, 420, 575, 800]),
    'q10-principles': D.composite((19, [45, 60, 575, 800]), (20, [45, 50, 575, 800])),
    'q10-mhrv': D.composite((21, [45, 50, 575, 800]), (22, [45, 50, 575, 175])),
    'q10-location': D.scheme(22, [45, 175, 575, 480]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p26 (printed 24): (a) best ten points × 4 (drawing 3, annotation 1) = 40, dimensions of three structural members 3 × 2 = 6, typical handrail heights 2 × 2 = 4, scale and drafting 6 = 56; (b) two design features × 2 = 4. Complete 60.'
S1 = 'One required section and two required safety features. The detail list is a marking menu, not a printed choice.'
T1A = 'To a scale of 1:5, draw a vertical section through the centre of the stairs and through the landing. The section should show the typical construction details through the top three steps of the stairs and the landing, showing the newel post, balusters and handrails to the stairs and landing. Include the typical dimensions of three structural members of the stairs. Show the typical handrail height to stairs and landing. Note: On your drawing, show a 500 mm length of landing.'
T1B = 'Indicate on your drawing two design features that ensure that the stairs is safe for all users.'
A1 = add('1', 'a', '(a)', T1A,
         [row('details', 'Any 10 points × 4 marks', 40, 'Best ten points, 4 each (drawing 3, annotation 1). Menu: closed string 250 × 50; string capping; pitch line; riser and rise 175 mm; tread and going 225 mm plus nosing; glue blocks and wedges; newel post 100 × 100; string and handrail jointed to the newel with tenons; balusters 40 × 40 to stairs and landing; 500 mm of landing; handrails 60 × 60 to 120 × 70; trimmer 200 × 75; landing joists 200 × 50 on hangers or notched; hardwood flooring 100 × 20; plasterboard ceiling.', list(range(0, 41, 4))),
          row('dimensions', 'Dimensions of 3 structural members (3 × 2 marks)', 6, 'Typical dimensions of three structural members, 2 each, such as the string 250 × 50, the newel post 100 × 100 and the trimmer 200 × 75.'),
          row('handrails', 'Typical handrail heights (2 × 2 marks)', 4, 'The minimum handrail heights to the stairs and to the landing, 2 each, shown on the drawing.'),
          row('presentation', 'Scale and Drafting', 6, 'Scale and drafting of the section.')],
         ['cons-1-5', 'cons-4-4', 'cons-4-3'], ['question-1-drawing-questions', 'stairs', 'floors'], 'q1-section',
         'Scaled drawing (1.5) of a closed-string stairs (4.4) and its landing floor (4.3).', B1, S1)
B1b = add('1', 'b', '(b)', T1B,
          [row('feature-1', 'Design detail 1', 2, 'Show and identify a safety feature, such as a pitch line of less than 42°.'),
           row('feature-2', 'Design detail 2', 2, 'A second, different feature, such as balusters spaced so that a 100 mm sphere cannot pass between them, or the minimum handrail heights to the stairs and landing.')],
          ['cons-4-4'], ['stairs'], 'q1-section', 'Stairs: rise, going, handrail and balustrade (4.4).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p27 (printed 25): (a) three printed items × 9 = 27; (b) two risks for each printed activity × 3 = 12 and two safety procedures for each, note and sketch × 3 = 12 = 24; (c) three guidelines × 3 = 9. Complete 60.'
S2 = 'All three printed items in (a) and both printed activities in (b) are required, each separately marked; not a choice.'
SAFE = (['cons-1-8'], ['site-safety'])
T2A = 'Discuss in detail the importance of each of the following in the development of a safety culture amongst workers on a construction site: training; vigilance; teamwork.'
T2B = 'Identify two possible risks to personal safety associated with each of the following: using a ladder on a construction site; fitting a window in the second storey of a dwelling house. Using notes and freehand sketches as appropriate, outline two specific safety procedures that should be observed to eliminate each risk identified at 2(b) above.'
T2C = 'Recommend three best practice guidelines that should be observed when using electrical tools on a construction site.'
A2 = add('2', 'a', '(a)', T2A,
         [row('training', 'Training', 9, 'Such as: awareness of risks on site; accidents minimised through planning and constant risk assessment; the legally required Safe Pass course, renewed every four years; specialist equipment training; mandatory PPE.'),
          row('vigilance', 'Vigilance', 9, 'Such as: management committed to monitoring safety; a regularly reviewed safety statement; a safety officer assessing risks; reporting of hazards, accidents and near misses; enforcement by the Health and Safety Authority.'),
          row('teamwork', 'Teamwork', 9, 'Such as: inexperienced workers paired with trained ones; trust and good communication between management and employees; a shared responsibility and a climate of openness; work suited to each worker’s skills.')],
         *SAFE, 'q2-culture', 'Safety precautions and culture on site (1.8).', B2, S2)
B2b = add('2', 'b', '(b)', T2B,
          [row('ladder-risks', 'Using a ladder on site Risk 1 Risk 2', 6, 'Two risks, 3 each. Such as: a damaged ladder; a ladder slipping or falling; working near power lines.'),
           row('window-risks', 'Fitting a window Risk 1 Risk 2', 6, 'Two risks, 3 each. Such as: a fall from height; back injury lifting a heavy window.'),
           row('ladder-procedures', 'Using a ladder Safety procedure 1 Note & sketch Safety procedure 2 Note & sketch', 6, 'Two procedures, note and sketch, 3 each. Such as: inspect the ladder; secure it at both ends on a firm, level base; three points of contact; extend it at least 1.0 m above the platform at about 74°, the foot a quarter of the height out; wooden ladders near power lines.'),
           row('window-procedures', 'Fitting a window Safety procedure 1 Note & sketch Safety procedure 2 Note & sketch', 6, 'Two procedures, note and sketch, 3 each. Such as: work from a safe platform such as scaffolding; at most 25 kg lifted per person with the correct lifting procedure; enough people lifting in unison; a cherry picker, teleporter or suction pads.')],
          *SAFE, 'q2-risks', 'Safety precautions on site (1.8).', B2, S2)
C2 = add('2', 'c', '(c)', T2C,
         [row(f'guideline-{i}', f'Guideline {i}', 3, note) for i, note in [
             (1, 'Such as: all power tools on a 110 volt supply, regularly serviced and properly earthed.'),
             (2, 'A second, different guideline. Such as: cables correctly sized, undamaged, waterproof and not a trip hazard; equipment kept covered and dry.'),
             (3, 'A third, different guideline. Such as: insulated footwear, gloves, earmuffs and safety glasses; damaged equipment removed from service for repair.')]],
         ['cons-9-4', 'cons-1-8'], ['site-safety'], 'q2-tools', 'Safety with electrical tools (9.4) on site (1.8).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-risks', B2, S2, parts(('a', T2A), ('b', T2B), ('c', T2C)))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p28 (printed 26): (a) proposed extension note 10 + sketch 10 and revised layout note 10 + sketch 10 = 40; (b) two reasons for each printed aim × 5 = 20. Complete 60.'
S3 = 'The design and layout are open responses with no printed list; both printed aims are required in (b).'
LIGHT = (['cons-1-2', 'cons-6-4', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'])
T3A = 'Show, using notes and freehand sketches, a proposed design for the extension to the rear of the dwelling house and a revised layout for the ground floor to include the extension.'
T3B = 'For each of the above, discuss in detail the reasons for your proposed design choices.'
A3 = add('3', 'a', '(a)', T3A,
         [row('extension', 'Proposed design for the extension Note Sketch', 20, 'Note 10 and sketch 10. Such as: an optimised south-facing footprint; high-performance low-e glazing; rooflights; part of wall B-B removed to let light in; the thermal mass of block walls and floor.'),
          row('layout', 'Revised Layout Note Sketch', 20, 'Note 10 and sketch 10. Such as: an open-plan layout with more floor area and kitchen space; floor-to-ceiling glazing to the garden; more natural light to the existing rooms; access to the garden.')],
         *LIGHT, 'q3-design', 'Designing the built environment (1.2) for solar gain (6.4) and daylight (7.4).', B3, S3)
B3b = add('3', 'b', '(b)', T3B,
          [row('sunlight', 'Increased sunlight into the interior of the house', 10, 'Two reasons, 5 each. Such as: energy gains from sunlight and heat collected; the health benefits of natural light; a high window head for deep daylight; a careful balance of glazing against winter heat loss and summer overheating; south is the optimal orientation.'),
           row('view', 'Improve the view to the rear garden', 10, 'Two reasons, 5 each. Such as: bringing the outdoors in, a pleasant space to relax; the garden becomes part of the living space; children seen at play; views of wildlife; health and well-being.')],
          *LIGHT, 'q3-reasons', 'Designing the built environment (1.2) for solar gain (6.4) and daylight (7.4).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-design', B3, S3, parts(('a', T3A), ('b', T3B)))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p29 (printed 27): (a) best nine items × 4 (sketch 3, annotation 1) = 36 and any two pipe sizes × 2 = 4 = 40; (b) two design considerations × (note 3 + sketch 3) = 12; (c) two advantages and two disadvantages × 2 = 8. Complete 60.'
S4 = 'The heating components are a marking menu, not a printed choice.'
T4A = 'Using notes and a single-line diagram, show a typical design layout for the heating system and the domestic hot water system. Show two independently controlled heating zones, one on each floor, and include three radiators on each floor. Indicate the location of the control valves and give the typical sizes of the pipework.'
T4B = 'Using notes and freehand sketches, discuss two design considerations that should be taken into account when siting a solar collector, as shown, to ensure maximum efficiency.'
T4C = 'Discuss in detail two advantages and two disadvantages of the heating system outlined at 4 above.'
A4 = add('4', 'a', '(a)', T4A,
         [row('items', '9 × 4 marks (Sketch 3 Annotation 1)', 36, 'Best nine items, 4 each (sketch 3, annotation 1). Menu: wood burning stove; radiators; zone control mechanism; zone thermostats; header or expansion tank; feed to the expansion tank; cold feed from it; expansion pipe or vessel; flow and return pipes to the radiators; radiator valves; pump and valves; solar panel with its flow and return and solar pump; twin-coil cylinder; control panel; expansion vessel; thermal reducing vessel.', list(range(0, 37, 4))),
          row('sizes', 'Sizes of pipework (any 2)', 4, 'Any two typical pipe sizes, 2 each, such as 22 mm flow and return, 28 mm expansion and 15 mm upstands to the radiators.')],
         ['cons-5-3', 'cons-5-2'], ['hot-water-space-heating'], 'q4-system', 'Zoned heating systems and controls (5.3) with a twin-coil cylinder (5.2).', B4, S4)
B4b = add('4', 'b', '(b)', T4B,
          [row('consideration-1', 'Design consideration 1 Note 3 marks & sketch 3 marks', 6, 'Note 3 and sketch 3. Such as: orientation facing south, within 15° east or west of south; the angle of inclination, about 45° in Ireland.'),
           row('consideration-2', 'Design consideration 2 Note 3 marks & sketch 3 marks', 6, 'A second, different consideration: note 3 and sketch 3. Such as: a location free of shading and close to the cylinder; sizing of about 1.0–1.5 m² of panel per person, avoiding oversizing.')],
          ['cons-6-4', 'cons-5-2'], ['sustainability-the-environment', 'hot-water-space-heating'], 'q4-siting', 'Solar heat gain (6.4) for hot water (5.2).', B4, S4)
C4 = add('4', 'c', '(c)', T4C,
         [row('advantage-1', 'Advantage 1', 2, 'Such as: solar power is renewable and silent, with less CO₂; up to 60% of hot water demand.'),
          row('advantage-2', 'Advantage 2', 2, 'A second, different advantage. Such as: wood is a renewable, carbon-neutral fuel; stoves are over 70% efficient; easy installation and grants available.'),
          row('disadvantage-1', 'Disadvantage 1', 2, 'Such as: weather dependent, with less sunlight further north; a significant initial cost.'),
          row('disadvantage-2', 'Disadvantage 2', 2, 'A second, different disadvantage. Such as: disposal of the glycol solar fluid; stoves lit and cleaned by hand; dry storage needed for wood pellets.')],
         ['cons-5-3', 'cons-6-4'], ['hot-water-space-heating', 'sustainability-the-environment'], 'q4-advantages', 'Heating systems (5.3) and solar gain (6.4).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-system', B4, S4, parts(('a', T4A), ('b', T4B), ('c', T4C)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p30 (printed 28): (a) thermally broken frame 15 (tabulation 2, wood 3, insulation 3, surfaces 2, total 2, U-value 3) and glazing unit 15 (glass 3, argon 3, surfaces 2, low-e 2, total 2, U-value 3) = 30; (b) two headings × 7 = 14; (c) window head notes 8 + sketch 8 = 16. Complete 60.'
S5 = 'No printed choice. Part (b) uses the U-values from (a).'
DATA5 = ('Glass thickness 4 mm; Space between panes of glass, each space 20 mm; Wood in thermally broken frame, each piece 30 mm; Rigid urethane insulation in frame, thickness 60 mm. '
         'Data for thermally broken wooden frame: Conductivity of wood (k) 0.150 W/m °C; Conductivity of rigid urethane insulation (k) 0.021 W/m °C; Resistance of external surface of frame (R) 0.950 m2 °C/W; Resistance of internal surface of frame (R) 1.400 m2 °C/W. '
         'Data for triple-glazed unit: Conductivity of glass (k) 1.050 W/m °C; Conductivity of argon gas (k) 0.160 W/m °C; Resistance of external surface of glass (R) 0.075 m2 °C/W; Resistance of internal surface of glass (R) 0.110 m2 °C/W; Total resistance of the low-e panes of glass (R) 3.400 m2 °C/W.')
T5A = 'For window A, using the given data, calculate the U-value of each of the following: the thermally broken wooden frame and the triple glazed argon-filled glazing unit. ' + DATA5
T5B = ('The traditional single-glazed solid wooden window shown at B has the following U-values: U-value of the solid wooden frame 0.317 W/ m2 °C; U-value of the single glazing 5.300 W/ m2 °C. '
       'Using the U-values of the high performance window frame and glazing unit obtained at 5(a) and the U-values of the traditional single-glazed wooden window given at 5(b) above, discuss the performance of both windows under the following headings: thermal properties; environmental considerations.')
T5C = 'Using notes and freehand sketches, show the design detailing of a window which is fixed in a 350 mm concrete block wall with an insulated cavity, to ensure minimum heat loss. Note: Show design details at the window head only.'
A5 = add('5', 'a', '(a)', T5A,
         [row('frame', 'Thermally broken wooden frame (15 marks)', 15, 'Correct tabulation 2, wood 3, insulation 3, external and internal surfaces 2, total resistance 2, U-value 3 (1 for the formula). By R = T/k: wood 0.06/0.150 = 0.400; urethane 0.06/0.021 = 2.857; surfaces 0.950 + 1.400; total 5.607 m²°C/W; U = 1/Rt = 1/5.607 = 0.178 W/m²K.'),
          row('glazing', 'Triple glazed, low-e, soft coat unit (15 marks)', 15, 'Glass 3, argon gas 3, external and internal surfaces 2, low-e glazing 2, total resistance 2, U-value 3 (1 for the formula). By R = T/k: one pane of glass 0.004/1.050 = 0.0038095; argon 0.040/0.160 = 0.25; surfaces 0.075 + 0.110; low-e glass 3.400; total 3.8388 m²°C/W; U = 1/3.8388 = 0.260495 W/m²K.')],
         ['cons-6-1', 'cons-3-6'], ['heat-u-value-calculations', 'windows-light'], 'q5-calculation', 'Thermal transmittance (6.1) of a window frame and glazing (3.6).', B5, S5)
B5b = add('5', 'b', '(b)', T5B,
          [row('thermal', 'Thermal properties', 7, 'Such as: the thermally broken frame (0.178) is almost twice as efficient as the traditional frame (0.317), the insulation in line with the glazing; the triple-glazed unit (0.261) up to twenty times more efficient than single glazing (5.300), which loses about 25% of the heat; lower heat loss costs and more comfort.'),
           row('environmental', 'Environmental considerations', 7, 'Such as: less demand for finite fossil fuels and less CO₂; locally sourced, naturally durable timber such as larch, cedar or Douglas fir from FSC-certified sources, with low embodied energy and no chemical preservatives or aluminium.')],
          ['cons-6-3', 'cons-3-6', 'cons-1-2'], ['heat-u-value-calculations', 'windows-light', 'sustainability-the-environment'], 'q5-comparison',
          'Heat loss and running costs (6.3) of windows (3.6) and their environmental impact (1.2).', B5, S5)
C5 = add('5', 'c', '(c)', T5C,
         [row('notes', 'Notes / Annotations', 8, 'Such as: a cavity tray; the cavity at the head sealed with 50 mm high-density insulation or a proprietary cavity closer; no thermal bridge; airtight tape; reinforced concrete lintels; the thermally broken frame positioned in line with the insulation.'),
          row('sketch', 'Sketch', 8, 'A sketch of the window head in the insulated cavity wall, as in the scheme’s model details.')],
         ['cons-3-6', 'cons-3-4', 'cons-6-2'], ['windows-light', 'walls', 'heat-loss-insulation'], 'q5-head', 'Window head detail (3.6) with lintel and cavity tray (3.4), free of thermal bridges (6.2).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p31 (printed 29): (a) three features × (note 5 + sketch 5) = 30; (b) three printed considerations × (4 for point + 6 for discussion) = 30. Complete 60.'
S6 = 'The features are open responses; all three printed considerations in (b) are required.'
T6A = 'With reference to the design shown, discuss in detail, using notes and freehand sketches, three features of the design that contribute to the house having a low environmental impact.'
T6B = 'Discuss in detail the importance of each of the following when designing a house suitable for first-time buyers: modest in scale; easy to modify; proximity to services.'
A6 = add('6', 'a', '(a)', T6A,
         [row(f'feature-{i}', f'Feature {i} Note Sketch', 10, note) for i, note in [
             (1, 'Note 5 and sketch 5. Such as: a steep pitched roof giving three bedrooms and a bathroom on a compact footprint; roof lights giving three times the daylight of dormers.'),
             (2, 'A second, different feature: note 5 and sketch 5. Such as: south-facing high-performance glazing and small north windows; a wood-burning stove on an internal chimney stack; rainwater harvesting.'),
             (3, 'A third, different feature: note 5 and sketch 5. Such as: solar panels on the south roof; the long elevation on an east–west axis; a flexible universal design; local timber frame and low-carbon GGBS concrete.')]],
         ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-features',
         'Low-impact design of the built environment (1.2), solar gain (6.4) and insulation (6.2).', B6, S6)
B6b = add('6', 'b', '(b)', T6B,
          [row('scale', 'Modest in scale (4 for point, 6 for discussion)', 10, 'Point 4 and discussion 6. Such as: a small footprint and site keep building, purchase and mortgage costs down; one room deep for solar gain; no corridors to heat; bedrooms in the attic; zoned heating.'),
           row('modify', 'Easy to modify (4 for point, 6 for discussion)', 10, 'Point 4 and discussion 6. Such as: the downstairs room used as a study, playroom or bedroom at no extra cost; a door opening into the bathroom; upstairs work done while the ground floor room is used.'),
           row('services', 'Proximity to services (4 for point, 6 for discussion)', 10, 'Point 4 and discussion 6. Such as: schools, shops and a doctor within walking or cycling distance; public transport to work, with no second car; a stronger sense of community; services nearby are more sustainable.')],
          ['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'], 'q6-buyers', 'Designing for first-time buyers in the built environment (1.2) and the choice of site (1.3).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b], 'q6-features', B6, S6, parts(('a', T6A), ('b', T6B)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p32 (printed 30): (a) best nine points × 5 (detail 4, annotation 1) = 45, three typical dimensions × 2 = 6, scale and drafting 6 = 57; (b) flue liner joint design detail 3. Complete 60.'
S7 = 'One required section and one required liner detail. The detail list is a marking menu, not a printed choice.'
T7A = 'To a scale of 1:5, draw a vertical section through the ground floor, hearth and chimney. The section should show the typical construction details from 400 mm below the finished floor to a level 300 mm above the top of the flue from the stove, and include the connection to the main flue liner in the chimney. Include three typical dimensions on your drawing.'
T7B = 'Indicate clearly on the drawing how the flue liners in the chimney are joined to ensure the safe removal of smoke and flue gases. Note: Show an outline of the stove only; it is not necessary to show a detailed drawing of the stove.'
A7 = add('7', 'a', '(a)', T7A,
         [row('details', '9 points × 5 marks', 45, 'Best nine points, 5 each (detail 4, annotation 1). Menu: hardcore; sand blinding; radon barrier; subfloor and screed or floor slab; insulation; hearth; 20 mm floating hardwood floor; internal block wall; lintel or flue gatherer; plaster; flue liners; lime-sand or vermiculite fill; cast iron flue from the stove; airtight seal to the wall; stove; independent air supply; cleaning access.', list(range(0, 46, 5))),
          row('dimensions', '3 typical dimensions (3 × 2 marks)', 6, 'Three typical dimensions, 2 each.'),
          row('presentation', 'Scale & Drafting', 6, 'Scale and drafting of the section.')],
         ['cons-1-5', 'cons-5-7', 'cons-4-2'], ['question-1-drawing-questions', 'fireplaces-fire-prevention', 'floors'], 'q7-section',
         'Scaled drawing (1.5) of a stove hearth and flue (5.7) on a solid ground floor (4.2).', B7, S7)
B7b = add('7', 'b', '(b)', T7B,
          [row('liners', 'Design detail', 3, 'Show the joint of the flue liners, as in the scheme’s model section: liners socketed and jointed for the safe removal of smoke and gases; a specialised adaptor joining the stove flue to the clay liner, or a continuous stainless steel liner, in vermiculite fill.')],
          ['cons-5-7'], ['fireplaces-fire-prevention'], 'q7-section', 'Flues to domestic appliances (5.7).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p33 (printed 31): (a) two requirements × (note 5 + sketch 5) = 20; (b) strip and raft foundations, each notes 5 + sketches 5 = 20, recommendation 3 and two reasons × 4 = 31; (c) three guidelines × 3 = 9. Complete 60.'
S8 = 'Both printed foundations in (b) are detailed ("either ... or" names the two being considered), then one is recommended; not a choice.'
CONCRETE = 'No Higher outgoing reference heading covers concrete materials and mixing (2.6, 2.7); the card keeps the Foundations association.'
T8A = 'Discuss in detail, using notes and freehand sketches, two functional requirements of a foundation suitable for a dwelling house.'
T8B = 'A trial hole, as shown in the sketch, indicates a moderately firm clay subsoil for the foundations of a dwelling house. The external wall of the house is a 350 mm solid concrete block wall with an insulated cavity. Consideration is being given at the design stage to using either: a traditional strip foundation or a raft foundation. Show, using notes and annotated freehand sketches, the typical design detailing for each type of foundation. Recommend a preferred foundation for the house and give two reasons for your recommendation.'
T8C = 'Discuss in detail three best practice guidelines that should be observed to ensure the maximum strength of concrete in a foundation.'
A8 = add('8', 'a', '(a)', T8A,
         [row(f'requirement-{i}', f'Functional requirement of foundation {i}', 10, note) for i, note in [
             (1, 'Note 5 and sketch 5. Such as: to transmit the dead and live loads safely to the ground, with a factor of safety; to provide a level surface for building.'),
             (2, 'A second, different requirement: note 5 and sketch 5. Such as: to anchor the structure; to prevent differential settlement; to resist seasonal ground movement, below the frost line; to resist sulphates in the soil.')]],
         ['cons-2-2'], ['foundations'], 'q8-requirements', 'Functions of a foundation (2.2).', B8, S8)
B8b = add('8', 'b', '(b)', T8B,
          [row('strip', 'Traditional strip foundation Notes Sketches', 10, 'Notes 5 and sketches 5. Such as: a reinforced strip at least 600 mm down against frost heave; hardcore, sand blinding, radon barrier and insulation; cavity fill.'),
           row('raft', 'Raft foundation Notes Sketches', 10, 'Notes 5 and sketches 5. Such as: a mesh-reinforced concrete raft on hardcore; radon barrier and insulation; DPC at least 150 mm above ground level.'),
           row('recommendation', 'Recommendation for foundation', 3, 'The preferred foundation, strip or raft.'),
           row('reason-1', 'Reason 1', 4, 'A reason matching the choice. Such as, strip: suited to moderately firm clay; easily constructed, filled and levelled.'),
           row('reason-2', 'Reason 2', 4, 'A second, different reason. Such as, strip: economical in materials and labour; raft: suited to poor soils, spreads the load evenly and reduces settlement, and allows load-bearing walls anywhere.')],
          ['cons-2-4', 'cons-2-3', 'cons-2-5'], ['foundations'], 'q8-foundations', 'Strip and raft foundations (2.4) on clay subsoil (2.3), reinforced (2.5).', B8, S8)
C8 = add('8', 'c', '(c)', T8C,
         [row(f'guideline-{i}', f'Guideline {i}', 3, note) for i, note in [
             (1, 'Such as: a level trench bottom free of loose soil; clean, correctly sized aggregates; batching by weight.'),
             (2, 'A second, different guideline. Such as: the correct water/cement ratio, about 0.6; reinforcement placed as designed with 75 mm cover; sulphate-resisting cement where needed.'),
             (3, 'A third, different guideline. Such as: compaction without excessive vibration; concrete not dropped from a height; cured for up to 28 days and protected from extreme heat or cold.')]],
         ['cons-2-7', 'cons-2-5'], ['foundations'], 'q8-concrete', 'Mixing, placing and curing site concrete (2.7) with reinforcement (2.5).', B8, S8)
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-foundations', B8, S8, parts(('a', T8A), ('b', T8B), ('c', T8C)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p34 (printed 32): (a) any three of the four circled locations × (note 6 + sketch 6) = 36; (b) two damp-proofing materials × (specification 3 + advantages 3) = 12; (c) two discussion points × 6 = 12. Complete 60.'
S9 = 'Choice is not a route: part (a) (any three of the FOUR circled locations) is ONE card with one any-three group over the four locations, named by the scheme’s Location headings; its figure carries all four. Part (b) (any two junctions) is marked per material: one card with two material rows.'
T9A = 'Select any three locations from those circled on the drawing and show, using notes and freehand sketches, the typical design detailing which will prevent the penetration of dampness at each location.'
T9B = 'Select any two junctions and specify a damp-proofing material suitable for each junction. Discuss the advantages of each material for the specified junction.'
T9C = 'Discuss in detail the importance of ensuring that moisture does not penetrate to the inner leaf of a wall of timber frame construction.'
LOCATIONS9 = [('Location 1', 'the chimney on the main roof: a lead back gutter welted under the slates; the roofing membrane carried under the battens and taped to the chimney; a cover flashing at the back of the chimney overhanging the lead gutter.'),
              ('Location 2', 'the window head: a stepped DPC so moisture cannot reach the inside leaf; an anti-capillary groove at the sash opening; a weather strip at the top of the window; mastic sealant around the window.'),
              ('Location 3', 'the window cill: the cill wrapped in DPC; a second layer of DPC around the cavity barrier; an anti-capillary groove in the cill; mastic sealant; airtight tape between the frame and the internal wall.'),
              ('Location 4', 'the lean-to roof against the wall: a stepped DPC; a cover flashing at the roof–wall junction; the roof membrane carried onto the wall and taped to the masonry.')]
A9 = add('9', 'a', '(a)', T9A,
         [anyn('locations', 'Three locations', 3, 12, LOCATIONS9, 'Any three of the four circled locations, each note 6 and sketch 6 = 12.')],
         ['cons-3-4', 'cons-3-10', 'cons-3-6'], ['walls', 'roofs', 'windows-light'], 'q9-locations',
         'The union of the four circled junctions: DPCs and flashings (3.4) at the roof abutments and chimney (3.10) and at the window head and cill (3.6).', B9, S9)
B9b = add('9', 'b', '(b)', T9B,
          [row('material-1', 'Damp proof material 1 (specification 3 marks) (advantages 3 marks)', 6, 'Specification 3 and advantages 3. Such as: lead — widely used around chimneys; flexible, corrosion-resistant, accommodates moderate movement, readily available and easily worked.'),
           row('material-2', 'Damp proof material 2 (specification 3 marks) (advantages 3 marks)', 6, 'A material for the second junction: specification 3 and advantages 3. Such as: a flexible plastic DPC — readily available, inexpensive and highly resistant to corrosive materials in mortar.')],
          ['cons-3-4'], ['walls'], 'q9-materials', 'Damp-proof courses and flashings (3.4).', B9, S9)
C9 = add('9', 'c', '(c)', T9C,
         [row('discussion-1', 'Discussion 1', 6, 'Such as: a longer life, avoiding decay of the timber frame — fungal decay follows prolonged contact with damp masonry; damp insulation loses its effectiveness.'),
          row('discussion-2', 'Discussion 2', 6, 'A second, different point. Such as: no mould on the internal walls; openings detailed and sealed; the breather membrane fixed correctly so moisture is kept out while vapour escapes; timber kept away from masonry.')],
         ['cons-3-3', 'cons-6-6'], ['walls', 'condensation-air-tightness'], 'q9-moisture', 'Timber frame external walls (3.3) and moisture control (6.6).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-locations', B9, S9, parts(('a', T9A), ('b', T9B), ('c', T9C)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p35 (printed 33): (a) any two of three printed items × (note 6 + sketch 6) = 24; (b) room layout, MHRV location, ducting with airflow and how the system works × 6 = 24; (c) two design considerations × 6 = 12. Complete 60.'
S10 = 'Choice is not a route: part (a) (any two of three printed items) is ONE card with an any-two group over the scheme headings; its figure and the complete-question figure carry all three items. The OR alternative is a separate Question 10 route.'
PASSIVE = (['cons-6-5'], ['passive-design', 'condensation-air-tightness'])
T10A = 'Using notes and freehand sketches as appropriate, discuss in detail the importance of any two of the following in the design of a Passive House: building orientation; thermal mass; primary energy demand.'
T10B = ('It is proposed to install a Mechanical Heat Recovery with Ventilation (MHRV) system in a Passive House, as shown in the drawing. Draw a single line diagram of the given room layout and indicate a preferred location for the MHRV unit. '
        'Show a typical design layout for the ducting to the MHRV unit and indicate clearly the direction of airflow in all the ducts. Describe how a Mechanical Heat Recovery with Ventilation (MHRV) system works. '
        'Note: Show a plan of the room layout only, it is not necessary to show the furniture.')
T10C = 'Discuss in detail two design considerations that should be taken into account when deciding a preferred location for the MHRV unit in a Passive House.'
ITEMS10 = [('Building orientation', 'the glazed façade due south or within 30° of south to maximise solar gain, especially in winter; otherwise more insulation and careful fenestration are needed.'),
           ('Thermal mass', 'the ability of a material, usually the concrete floor, to absorb and store heat: it stores solar gain, stabilising the temperature against summer overheating and heating the home in winter; high heat capacity and density with moderate conductivity.'),
           ('Primary energy demand', 'the total energy for space and water heating, ventilation and all electricity, at most 120 kWh/m²a for certification (typically 60–70); electricity has a conversion factor of about 2.4.')]
A10 = add('10', 'a', '(a)', T10A,
          [anyn('items', 'Discussion of 2 design details', 2, 12, ITEMS10, 'Any two of the three printed items, each note 6 and sketch 6 = 12.')],
          ['cons-6-4', 'cons-6-2', 'cons-6-3'], ['passive-design', 'heat-loss-insulation'], 'q10-principles',
          'The union of the three printed items: orientation for solar gain (6.4), thermal mass and the building fabric (6.2) and energy demand (6.3).', B10, S10)
B10b = add('10', 'b', '(b)', T10B,
           [row('layout', 'Room layout', 6, 'A single-line plan of the given rooms.'),
            row('location', 'MHRV location', 6, 'A preferred location for the unit, such as the utility room.'),
            row('ducting', 'Ducting layout including direction of airflow', 6, 'Extract ducts from the kitchen, bathroom and utility and supply ducts to the living spaces and bedrooms, with the airflow shown in every duct, as in the scheme’s model plans.'),
            row('explanation', 'Explanation of how the system works', 6, 'Moist warm extract air and filtered outdoor air pass through a heat exchanger of thin plates without mixing; the outdoor air is warmed and supplied to the living spaces; a post heater in cold weather and a summer bypass; a sound attenuator.')],
           *PASSIVE, 'q10-mhrv', 'Ventilation with heat recovery (6.5).', B10, S10)
C10 = add('10', 'c', '(c)', T10C,
          [row('consideration-1', 'Design consideration 1', 6, 'Such as: energy conservation — the unit inside the thermal envelope, with short ducts and the extract rooms grouped.'),
           row('consideration-2', 'Design consideration 2', 6, 'A second, different consideration. Such as: maintenance — accessible for the annual filter change; noise — at most 25 dB; aesthetics — in a utility room or kitchen cabinet.')],
          ['cons-6-5'], ['passive-design'], 'q10-location', 'Ventilation with heat recovery (6.5).', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-principles', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p36 (printed 34): discussion of the statement, three points × (4 + 6) = 30; three guidelines × (4 + 6) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately, so each is its own task and the complete card composes them.'
TAA = 'Discuss the above statement in detail.'
TAB = 'Propose three guidelines that would promote the development of environmentally sustainable housing in Ireland.'
TALL = 'Discuss the above statement in detail and propose three guidelines that would promote the development of environmentally sustainable housing in Ireland.'
HOUSING = (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'])
AA = add('10', 'discussion', ' — discussion', TAA,
         [row(f'point-{i}', f'Discussion – point {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: a remote house needs large amounts of energy and materials for services and roads, while a modest home near schools, shops and work is reached by walking, cycling or public transport.'),
             (2, 'Point 4 and discussion 6. Such as: oil and gas are finite and over a third of energy goes on transport; sustainability must look beyond the BER of the fabric to a holistic approach to living.'),
             (3, 'Point 4 and discussion 6. Such as: Ireland builds the largest houses in the EU while town centres decay; reuse existing buildings, build modest, compact, flexible deep-green homes. Three distinct, well-argued points are needed.')]],
         *HOUSING, None, 'Sustainable housing in the built environment (1.2, 1.3).', BALT, SALT, alt=True)
AB = add('10', 'guidelines', ' — guidelines', TAB,
         [row(f'guideline-{i}', f'Guideline {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: universal design and flexible, lifetime housing as the norm; sustainability a condition of planning.'),
             (2, 'Point 4 and discussion 6. Such as: urban renewal with grant aid to refurbish decaying buildings; higher urban densities with cycle and walking routes.'),
             (3, 'Point 4 and discussion 6. Such as: deep-green planning guidelines for all developments; housing clusters and eco-villages as exemplars; incentives for low embodied energy design. Three distinct guidelines are needed.')]],
         *HOUSING, None, 'Sustainable housing in the built environment (1.2, 1.3).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, TALL, labels=['Discussion of the statement', 'Three guidelines'], alt=True)

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and four other questions (300 marks); all question banks retained, no full-exam Cartesian cards.'),
          (4, 'either', 'Q8(b) "either: a traditional strip foundation or a raft foundation": both are detailed ("for each type of foundation"), then one is recommended; not a candidate choice.'),
          (4, 'or', 'Q8(b) the same two foundations, both required.'),
          (5, 'Select', 'Q9(a) closed choose-three of the four circled locations: one card with an any-three group (choice is not a route).'),
          (5, 'any three', 'Q9(a) the same any-three group.'),
          (5, 'Select', 'Q9(b) any two of the circled junctions: the scheme marks the two damp-proofing materials, one card with two material rows (choice is not a route).'),
          (5, 'any two', 'Q9(b) the same two junctions.'),
          (5, 'any two', 'Q10(a) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
          (5, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.'),
          (5, 'or', 'Alternative Question 10 quotation ("schools, shops or workplace"): not a candidate choice.'),
          (5, 'or', 'Alternative Question 10 quotation ("walking or cycling distance"): not a candidate choice.')]
FINITE = {'9a': dict(choose=3, options=[h for h, _ in LOCATIONS9], cardId=A9['id'], groupRowId='locations'),
          '10a': dict(choose=2, options=[h for h, _ in ITEMS10], cardId=A10['id'], groupRowId='items')}
GAPS = [dict(cardId=C8['id'], canonicalTopicIds=['cons-2-7'], atlasTopicId=D.CROSS + 'foundations', reason=CONCRETE)]
D.finish(LEDGER, FINITE, {}, taxonomy_gaps=GAPS)
