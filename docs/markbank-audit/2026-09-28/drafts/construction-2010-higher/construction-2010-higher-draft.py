"""Draft the 2010 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 24-34; the English scheme carries Irish running headers). This paper was never carded: every task is
added. Q10(a) "any two of the following" is ONE card with an any-two group (choice is not a route).
Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Trussed roof, wall and window section', concept='truss-wall-window-section',
              stem='The sketch shows portion of an external wall, roof and a window of a dwelling house. The external wall is a 350 mm concrete block wall with an insulated cavity. The roof has prefabricated trussed rafters, it is slated and has a pitch of 30 degrees. The house has an internal span of 6.0 metres. The window is an outward opening triple-glazed wooden casement window and is 600 mm in height. The fixed frame of the window is 150 mm × 80 mm.',
              note='Original sketch and specification retained. Construction, dimension and scale/drafting marks belong to part (a); the cavity closure in (b) is marked separately.'),
    '2': dict(page=2, title='An entrance and open-plan living for a wheelchair user', concept='wheelchair-open-plan',
              stem='The accompanying diagram shows an open-plan living, dining and kitchen space suitable for a person in a wheelchair. The floor is an insulated solid concrete ground floor.',
              note='Original diagram retained. The two areas in (b) are chosen from the diagram; the scheme marks any two alike.'),
    '3': dict(page=2, title='Internal and external insulation of a cavity wall', concept='internal-external-insulation',
              stem='The external wall of a dwelling house built in the 1970s is a 300 mm concrete block wall with 40 mm expanded polystyrene insulation in the cavity. It has been decided to upgrade the thermal properties of the external wall by using either: an internal insulation system or an external insulation system.',
              note='Both printed systems are required ("for each of the insulation systems"); not a choice.'),
    '4': dict(page=3, title='Below ground drainage, a manhole and testing', concept='drainage-manhole', stem='',
              note='Original sketch retained. The requirements and the test are open responses; the scheme lists typical examples.'),
    '5': dict(page=3, title='Solid wall U-value, phenolic foam thickness and thermal mass', concept='solid-wall-u-value', stem='',
              note='All printed data are retained in the original question. Part (b) uses the resistance from (a); the scheme’s worked answers are U = 1.805 W/m²K and 78.75 mm of phenolic foam.'),
    '6': dict(page=3, title='A timber frame house with low environmental impact', concept='timber-frame-low-impact',
              stem='The drawing shows the design of a timber frame house with an external wooden cladding and a flat roof. The house is designed to have low environmental impact.',
              note='Original drawing retained. Features are open responses; all three printed qualities in (b) are required.'),
    '7': dict(page=4, title='Open riser stairs section', concept='open-riser-stairs-section',
              stem='The top portion of an open riser timber stairs is shown in the accompanying sketch. The first floor landing has a suspended timber floor with 25 mm hardwood flooring on timber joists and a plasterboard ceiling beneath. The newel post is 100 mm × 100 mm.',
              note='Original sketch retained. Construction, handrail and scale/drafting marks belong to part (a); the two safety features in (b) are marked separately.'),
    '8': dict(page=4, title='Window size by daylight, and a high-performance window', concept='window-daylight-performance', stem='',
              note='The method in (a) is open ("or by any other suitable method"); the scheme works the degree of efficiency method to a window area of 2.85 m².'),
    '9': dict(page=4, title='An attic living space and its airtightness', concept='attic-living-airtightness', stem='',
              note='Original sketch retained. The requirements and leakage routes are open responses; the scheme lists typical examples.'),
    '10': dict(page=5, title='Passive House design, MHRV and overheating', concept='passive-house-overheating', stem='',
               note='Original sketch retained. Part (a) is a closed choice of any two of the three printed items: one card holding all three.'),
}
ALT = dict(page=5, title='Sustainable urbanism (alternative Question 10)', concept='sustainable-urbanism',
           stem='“In the increasingly urbanised world of the 21st century, a major challenge is to find solutions to the problems facing our towns and cities – the control of sprawl, sustainable growth, integrated transport systems and better-quality urban environments and public realms. Cities and towns that are diverse, varied in use, walkable, human scaled and identifiable by the high quality of their public realm can contribute to the process of creating sustainable urbanism. The challenge for all citizens is to make our towns and cities viable in the long term, environmentally and socially, as well as economically. There will be no sustainable world and no sustainable country without sustainable cities and towns”. Sustainable Urbanism: creating communities for the knowledge economy: by Anthony Reddy in The New Housing 2, Royal Institute of Architects of Ireland 2009.',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately.')
SCHEME_PAGES = {'1': [4, 24], '2': [5, 6, 25], '3': [6, 7, 8, 26], '4': [9, 10, 27], '5': [10, 11, 12, 28], '6': [12, 13, 29],
                '7': [14, 15, 30], '8': [15, 16, 31], '9': [17, 18, 32], '10': [18, 19, 33], '10-alt': [20, 21, 34]}
D = cp.Draft(HERE, 2010, 'higher', ('c4651a6996cf20f3efda5b3c754337f4c57bd4d9155a49d79a3cb6176fd51ccb',
                                    '43dbe433ff008b0ebea913028b365e78e93bf3eaaff3eee5858bc089190070e0'), 0, QUESTIONS, SCHEME_PAGES, alt=ALT)
row, add, compose, parts, anyn = D.row, D.add, D.compose, D.parts, D.anyn
D.figures({
    'q1-original': D.paper(2, [30, 50, 580, 304]), 'q2-original': D.paper(2, [30, 304, 580, 537]),
    'q3-original': D.paper(2, [30, 537, 580, 790]), 'q4-original': D.paper(3, [30, 50, 580, 251]),
    'q5-original': D.paper(3, [30, 251, 580, 534]), 'q6-original': D.paper(3, [30, 534, 580, 790]),
    'q7-original': D.paper(4, [30, 50, 580, 266]), 'q8-original': D.paper(4, [30, 266, 580, 479]),
    'q9-original': D.paper(4, [30, 479, 580, 790]), 'q10-original': D.paper(5, [30, 50, 580, 311]),
    'q10-alt-original': D.paper(5, [30, 330, 580, 790]),
    'q1-section': D.scheme(4, [40, 60, 585, 784]),
    'q2-entrance': D.scheme(5, [40, 60, 585, 324]),
    'q2-areas': D.composite((5, [40, 324, 585, 784]), (6, [40, 60, 585, 130])),
    'q3-systems': D.composite((6, [40, 130, 585, 786]), (7, [40, 60, 585, 784]), (8, [40, 60, 585, 209.5])),
    'q3-advantages': D.scheme(8, [40, 209.5, 585, 784]),
    'q4-requirements': D.scheme(9, [40, 60, 585, 438]), 'q4-manhole': D.scheme(9, [40, 438, 585, 725]),
    'q4-test': D.composite((9, [40, 725, 585, 786]), (10, [40, 60, 585, 310])),
    'q5-calculation': D.composite((10, [40, 310, 585, 784]), (11, [40, 60, 585, 320])),
    'q5-mass': D.composite((11, [40, 320, 585, 784]), (12, [40, 60, 585, 452])),
    'q6-features': D.composite((12, [40, 452, 585, 784]), (13, [40, 60, 585, 228])), 'q6-materials': D.scheme(13, [40, 228, 585, 784]),
    'q7-scheme': D.composite((14, [40, 60, 585, 784]), (15, [40, 60, 585, 290])),
    'q8-calculation': D.scheme(15, [40, 300, 585, 784]), 'q8-window': D.scheme(16, [40, 60, 585, 554]),
    'q8-environment': D.scheme(16, [40, 554, 585, 784]),
    'q9-requirements': D.scheme(17, [40, 60, 585, 524]), 'q9-leakage': D.composite((17, [40, 524, 585, 784]), (18, [40, 60, 585, 158])),
    'q9-advantages': D.scheme(18, [40, 158, 585, 431]),
    'q10-principles': D.composite((18, [40, 431, 585, 784]), (19, [40, 60, 585, 187])),
    'q10-mhrv': D.scheme(19, [40, 187, 585, 784]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p24 (printed 2): (a) best twelve details × 4 (drawing 3, annotation 1) = 48, four roof dimensions 4 and scale and drafting 4 = 56; (b) cavity closure at wallplate level 4. Complete 60.'
S1 = 'One required section and one required cavity closure. The detail list is a marking menu, not a printed choice.'
T1A = 'To a scale of 1:10, draw a vertical section through the external wall, window and roof structure. The section should show the typical construction details from 300 mm below the concrete cill, through the fixed frame of the window and include the roof to the level of the ridge. Include four typical dimensions of the roof structure.'
T1B = 'Indicate clearly on the drawing how the cavity is closed at wallplate level. Note: Show the details for one external wall, one half of the roof from eaves to ridge level and include three courses of slate at eaves.'
A1 = add('1', 'a', '(a)', T1A,
         [row('details', 'Any 12 details ×4 marks', 48, 'Best twelve details, 4 each (drawing 3, annotation 1). Wall: inner and outer leaf; internal and external plaster; 150 mm cavity with 100 mm insulation; cavity closer; concrete lintels; stepped DPC. Window: concrete cill with DPC behind; wooden frame cill; window board; triple-glazed unit; frame head; insulation behind the cill. Roof: fascia, soffit and gutter; eaves vent; felt and battens; slates; ceiling joist; attic insulation; strut.', list(range(0, 49, 4))),
          row('dimensions', 'Four typical dimensions of roof structure', 4, 'Four typical dimensions of the roof structure, 1 each, such as wallplate 100 × 75, ceiling 150 × 50, rafter 150 × 50, strut 100 × 50 and batten 50 × 30 mm.'),
          row('presentation', 'Scale & Drafting', 4, 'Scale and drafting of the section.')],
         ['cons-1-5', 'cons-3-8', 'cons-3-9', 'cons-3-6', 'cons-3-3'], ['question-1-drawing-questions', 'roofs', 'windows-light', 'walls'], 'q1-section',
         'Scaled drawing (1.5) of a trussed roof (3.8) with its covering (3.9) over a window (3.6) in a cavity wall (3.3).', B1, S1)
B1b = add('1', 'b', '(b)', T1B,
          [row('closure', '4 marks for indicating how cavity is closed at wallplate level', 4, 'Show how the cavity is closed at wallplate level, such as with a proprietary cavity closer or a block of insulation, as in the scheme’s model sections.')],
          ['cons-3-3', 'cons-3-10'], ['walls', 'roofs'], 'q1-section', 'Closing the cavity (3.3) at the eaves (3.10).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p25 (printed 3): (a) any two design details × (note 8 + sketch 8) = 32; (b) two areas × (note 7 + sketch 7) = 28. Complete 60.'
S2 = 'The two areas in (b) are chosen from the given diagram; the scheme marks any two areas alike, so the task has two area rows (choice is not a route).'
ACCESS = (['cons-1-2', 'cons-3-7'], ['planning-sustainability-environment', 'doors'])
T2A = 'Using notes and freehand sketches show the design detailing at the entrance door to ensure that rainwater is removed from the threshold area and that the entrance is suitable for a person in a wheelchair.'
T2B = 'From the given diagram, select any two areas that need specific consideration to ensure suitability for a person in a wheelchair. For each area selected, using notes and freehand sketches, show the specific design detailing that ensures ease of use for a person in a wheelchair. Indicate on your design sketches typical dimensions as appropriate.'
A2 = add('2', 'a', '(a)', T2A,
         [row('detail-1', 'Design detail 1 - note 8 marks, sketch 8 marks', 16, 'Note 8 and sketch 8. Such as: a level entrance with a 1500 mm turning circle; a ramp no steeper than 1:20; a drainage channel beside the threshold to remove rainwater quickly.'),
          row('detail-2', 'Design detail 2 - note 8 marks, sketch 8 marks', 16, 'A second, different detail: note 8 and sketch 8. Such as: a reinforced concrete threshold with a DPC tray behind it; a proprietary threshold no more than 15 mm high; insulation, radon barrier and floor build-up.')],
         *ACCESS, 'q2-entrance', 'Accessible design (1.2) of an entrance door (3.7).', B2, S2)
B2b = add('2', 'b', '(b)', T2B,
          [row('area-1', 'Area 1', 14, 'Note 7 and sketch 7, with dimensions. Such as, the dining area: a circular, pedestal table at 700–800 mm; space round it; switches and sockets at 900–1200 mm; low cills and lever handles.'),
           row('area-2', 'Area 2', 14, 'A second, different area: note 7 and sketch 7. Such as, the kitchen: sink, cooker and fridge in a close triangle; a low sink with open knee space and lever taps; worktop beside the cooker and appliances; eye-level oven; doors at least 800 mm clear.')],
          *ACCESS, 'q2-areas', 'Universal design of the home (1.2) with wide doors (3.7).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b], 'q2-entrance', B2, S2, parts(('a', T2A), ('b', T2B)))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p26 (printed 4): (a) for each printed system, fixing, insulation and thickness, and finish × (note 4 + sketch 4) = 24, 48; (b) two advantages of each system × 2 = 8 and recommendation 4 = 12. Complete 60.'
S3 = 'Both printed systems are required; "either ... or" names the two systems being considered. The recommendation is an open choice.'
INSUL = (['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'walls'])
T3A = 'For each of the insulation systems outlined above, show using notes and freehand sketches, one method of applying the insulation material. For each insulation system, include the following in your sketches: method of fixing; insulation material and its thickness; surface finish.'
T3B = 'Discuss in detail two advantages of each system of insulation and recommend a preferred system of insulation for the house outlined above.'
A3 = add('3', 'a', '(a)', T3A,
         [row('internal', 'Internal Insulation System (note 4 marks, sketch 4 marks)', 24, 'Fixing, insulation and its thickness, and finish, each note 4 and sketch 4. Such as: insulated dry-lining board on adhesive dabs or mechanical fixings, or battens at 400 mm with insulation between; rigid phenolic foam at least 80 mm with 12.5 mm plasterboard and an integral vapour barrier; a skim finish.'),
          row('external', 'External Insulation System (note 4 marks, sketch 4 marks)', 24, 'Fixing, insulation and its thickness, and finish, each note 4 and sketch 4. Such as: rigid phenolic foam 80–300 mm or EPS bonded with base coat adhesive and anchor bolts; fibreglass mesh; two coats of acrylic render; angle beads and sealed cill and head details.')],
         *INSUL, 'q3-systems', 'Insulating materials (6.2) on an external wall (3.3).', B3, S3)
B3b = add('3', 'b', '(b)', T3B,
          [row('internal-advantages', 'Two advantages of each system (2×2 marks each)', 4, 'Two advantages of internal insulation, 2 each. Such as: the elevations unchanged, no planning needed; the character of older buildings kept; rooms warm up faster; easy to install.'),
           row('external-advantages', 'Two advantages of each system (2×2 marks each)', 4, 'Two advantages of external insulation, 2 each. Such as: no loss of floor space or disruption inside; an upgraded appearance and BER; the wall’s thermal mass stores heat for the rooms.'),
           row('recommendation', 'Recommendation', 4, 'A preferred system for the house, internal or external, with a reason.')],
          *INSUL, 'q3-advantages', 'Insulating materials (6.2) on an external wall (3.3).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-systems', B3, S3, parts(('a', T3A), ('b', T3B)))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p27 (printed 5): (a) three requirements × (note 4 + sketch 4) = 24; (b) manhole note 8, sketch 8 and dimensions 8 = 24; (c) one test, note and sketch 2 × 6 = 12. Complete 60.'
S4 = 'The requirements and the test are open responses with no printed list.'
DRAIN = (['cons-5-5'], ['drainage'])
T4A = 'Discuss, using notes and freehand sketches, three functional requirements of a below ground drainage system to ensure the safe removal of sewage from a domestic dwelling.'
T4B = 'The accompanying sketch shows the location of a manhole at the intersection of a branch drain and a main drain in a below ground drainage system for a domestic dwelling. Using notes and freehand sketches, show the typical construction details through the manhole from the foundation to the manhole cover. Indicate on the sketch the typical dimensions.'
T4C = 'Using notes and freehand sketches, describe in detail one test that may be carried out to ensure that the below ground drainage system is watertight.'
A4 = add('4', 'a', '(a)', T4A,
         [row(f'requirement-{i}', f'Functional requirement {i}', 8, note) for i, note in [
             (1, 'Note 4 and sketch 4. Such as: watertight, with correctly sealed joints; self-cleansing at the correct gradient.'),
             (2, 'A second, different requirement. Such as: access for clearing blockages, with straight runs and oblique connections; flexible joints against settlement, traffic and tree roots.'),
             (3, 'A third, different requirement. Such as: ventilation so foul air and methane do not enter the dwelling; traps and seals of the correct depth; resistance to corrosive soil.')]],
         *DRAIN, 'q4-requirements', 'Underground drainage (5.5).', B4, S4)
B4b = add('4', 'b', '(b)', T4B,
          [row('note', 'Note 8marks', 8, 'Such as: a 150 mm mass concrete base; branches laid obliquely into a half-round channel at or above its horizontal diameter; benching rounded and up to the top of the outgoing pipe; rendered concrete or block walls; a cast iron, pressed steel or precast cover; step irons over 1 m deep.'),
           row('sketch', 'Sketch 8 marks', 8, 'A sketch through the manhole from the base to the cover, as in the scheme’s model section.'),
           row('dimensions', 'Typical dimensions', 8, 'Typical dimensions, such as an internal size of 1200 × 750 to 1200 × 840 mm and a 150 mm base.')],
          *DRAIN, 'q4-manhole', 'Manholes in underground drainage (5.5).', B4, S4)
C4 = add('4', 'c', '(c)', T4C,
         [row('test', 'Note and sketch (2×6 marks)', 12, 'Note 6 and sketch 6. Such as, the water test before backfilling: the end plugged, a 1.5 m head of water above the invert, filled and left 2 hours, then leakage over 30 minutes no more than 0.05 litres per metre; or an air test.')],
         *DRAIN, 'q4-test', 'Testing underground drainage (5.5).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-manhole', B4, S4, parts(('a', T4A), ('b', T4B), ('c', T4C)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p28 (printed 6): (a) ten points × 3 = 30 (tabulation, five resistances, total, U formula and value, units); (b) seven steps × 3 = 21; (c) thermal mass note 5 + sketch 4 = 9. Complete 60.'
S5 = 'No printed choice. Part (b) uses the resistance from (a).'
DATA5 = ('External render thickness 16 mm; Solid concrete wall thickness 225 mm; Internal plaster thickness 13 mm. Thermal data of external wall of house: Resistivity of the solid concrete wall (r) 1.190 m °C/W; '
         'Resistivity of external render (r) 2.170 m °C/W; Resistivity of internal plaster (r) 6.250 m °C/W; Resistance of external surface (R) 0.048 m2 °C/W; Resistance of internal surface (R) 0.122 m2 °C/W.')
T5A = 'Calculate the U-value of an uninsulated external solid concrete wall of a dwelling house built in the 1950s given the following data: ' + DATA5
T5B = 'Phenolic foam insulation is to be fitted to the external surface of the solid concrete wall. Given the conductivity (k) of phenolic foam as 0.025 W/m °C, calculate the thickness of phenolic foam required to achieve a U-value of 0.27 W/m2 °C.'
T5C = 'Discuss in detail, using notes and freehand sketches, the importance of thermal mass in improving the thermal performance of a dwelling house.'
A5 = add('5', 'a', '(a)', T5A,
         [row('tabulation', 'Correct Tabulation', 3, 'The calculation set out in a table of material, resistivity, thickness and resistance.'),
          row('resistances', '10 points×3 marks for each point', 15, 'Five resistances, 3 each, by R = T × r: render 0.016 × 2.17 = 0.03472; wall 0.225 × 1.190 = 0.26775; plaster 0.013 × 6.250 = 0.08125; external surface 0.048 and internal surface 0.122 (given). All in m²°C/W.', list(range(0, 16, 3))),
          row('total-resistance', 'Total Resistance', 3, 'Total resistance, the sum of R = 0.55372 m²°C/W.', [0, 3]),
          row('u-value', 'U-value Formula U=1/R t', 6, 'The formula U = 1/Rt 3 and the U-value 3: U = 1 ÷ 0.55372 = 1.805.'),
          row('units', 'Correct units W/m2 °C or W/m2 K', 3, 'The correct units, W/m²°C or W/m²K.')],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Thermal resistance, conductivity and transmittance (6.1).', B5, S5)
B5b = add('5', 'b', '(b)', T5B,
          [row('formula', 'Application of formula : R=1/U', 3, 'R = 1/U.'),
           row('existing', 'Current Resistance from part (a)', 3, 'The existing resistance, 0.55372 m²K/W.'),
           row('required', 'Resistance required for a U- Value of 0.27', 3, 'R = 1 ÷ 0.27 = 3.703 m²K/W.'),
           row('difference', 'Difference in Resistances', 3, 'Difference = 3.703 − 0.55372 = 3.15 m²K/W.'),
           row('thickness', 'Required thickness of insulation', 9, 'The formula R = T/k 3, its application 3 and the thickness 3: T = 3.15 × 0.025 = 0.07875 metres, 78.75 mm (79 mm) of phenolic foam.')],
          ['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation'], 'q5-calculation', 'Thermal transmittance (6.1) and insulating materials (6.2).', B5, S5)
C5 = add('5', 'c', '(c)', T5C,
         [row('mass', 'Note and sketch', 9, 'Note 5 and sketch 4. Such as: dense materials such as concrete, block and tiles store solar gain by day and release it slowly; passive solar collection through tall south glazing at about 6:1 mass to glass; thermal mass in direct sun 30% more efficient; insulated and airtight so the stored heat is kept.')],
         ['cons-6-4', 'cons-6-2'], ['passive-design', 'heat-loss-insulation'], 'q5-mass', 'Solar heat gain (6.4) stored in the building fabric (6.2).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p29 (printed 7): (a) three design features × (note 8 + sketch 8) = 48; (b) three printed qualities × 4 = 12. Complete 60.'
S6 = 'The features are open responses; all three printed qualities in (b) are required.'
GREEN = (['cons-1-2', 'cons-6-4'], ['sustainability-the-environment'])
T6A = 'Discuss in detail, using notes and freehand sketches, three design features that contribute to reducing the environmental impact of the house shown.'
T6B = 'Discuss in detail the importance of each of the following when choosing materials for an environmentally sustainable house: renewable; durable; locally sourced.'
A6 = add('6', 'a', '(a)', T6A,
         [row(f'feature-{i}', f'Design feature {i}', 16, note) for i, note in [
             (1, 'Note 8 and sketch 8. Such as: external wooden cladding, locally sourced and renewable with low embodied energy, using less concrete.'),
             (2, 'A second, different feature: note 8 and sketch 8. Such as: passive solar gain through a large south-facing glazed area, small north windows and a tiled floor for thermal mass.'),
             (3, 'A third, different feature: note 8 and sketch 8. Such as: a compact form one room wide with a low surface-to-volume ratio and a flat roof using fewer materials.')]],
         ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-features',
         'Sustainable design of the built environment (1.2), solar gain (6.4) and insulation (6.2).', B6, S6)
B6b = add('6', 'b', '(b)', T6B,
          [row('renewable', 'Renewable', 4, 'Such as: materials that regrow, with low embodied energy and less fossil fuel in processing; carbon-neutral materials such as hemp; low-carbon GGBS concrete.'),
           row('durable', 'Durable', 4, 'Such as: naturally durable cedar, Douglas fir or oak, or boron-treated timber; long-lasting stone and glass; less maintenance; water resistance against mould and rot.'),
           row('local', 'Locally sourced', 4, 'Such as: fewer transport miles and fossil fuels; buildings integrated with their surroundings; local enterprise, skills and employment.')],
          *GREEN, 'q6-materials', 'Sustainable materials in the built environment (1.2).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b], 'q6-features', B6, S6, parts(('a', T6A), ('b', T6B)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p30 (printed 8): (a) best six details × 5 (drawing 3, annotation 1) = 30, scale and drafting 4, and the two handrail heights and baluster spacing × 2 = 40; (b) two safety features × (note 5 + sketch 5) = 20. Complete 60.'
S7 = 'One required section and two required safety features. The detail list is a marking menu, not a printed choice.'
STAIRS = (['cons-4-4'], ['stairs'])
T7A = 'To a scale of 1:5 draw a vertical section through the top three steps of the stairs and landing. Show the newel post, balusters and handrail of the stairs. Indicate on the drawing the: handrail height to stairs; handrail height to landing; spacing between balusters.'
T7B = 'Using notes and freehand sketches, show two safety features in the design of an open riser stairs to ensure that the stairs is safe for all users.'
A7 = add('7', 'a', '(a)', T7A,
         [row('details', 'Any 6 details × 5 marks each', 30, 'Best six details, 5 each (drawing 3, annotation 1). Menu: closed string; string capping; partial riser; tread; newel post; handrail; balusters; trimmer; flooring; landing handrail; the string and the handrail jointed to the newel post.', list(range(0, 31, 5))),
          row('presentation', 'Scale and Drafting', 4, 'Scale and drafting of the section.'),
          row('stairs-handrail', 'Handrail height to stairs', 2, 'The handrail height to the stairs, 840–900 mm from the pitch line.'),
          row('landing-handrail', 'Handrail height to landing', 2, 'The handrail height to the landing, at least 900 mm.'),
          row('balusters', 'Spacing between balusters', 2, 'Spacing so a 100 mm sphere cannot pass between the balusters.')],
         ['cons-1-5', 'cons-4-4', 'cons-4-3'], ['question-1-drawing-questions', 'stairs', 'floors'], 'q7-scheme',
         'Scaled drawing (1.5) of an open riser stairs (4.4) at its landing floor (4.3).', B7, S7)
B7b = add('7', 'b', '(b)', T7B,
          [row('feature-1', 'Two design features that ensure the stairs is safe', 10, 'Note 5 and sketch 5. Such as: a going of at least 220 mm and rise of at most 220 mm, 2R + G between 550 and 700 mm, a pitch of at most 42°; openings that do not pass a 100 mm sphere.'),
           row('feature-2', 'Two design features that ensure the stairs is safe', 10, 'A second, different feature: note 5 and sketch 5. Such as: handrails at 840–900 mm, on both sides over 1000 mm wide; guarding not easily climbed; 2 m headroom; a landing at the top of every flight.')],
          *STAIRS, 'q7-scheme', 'Stairs: rise, going, handrail and headroom (4.4).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-scheme', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p31 (printed 9): (a) seven steps × 2 = 14; (b) two frame designs and two glazing designs × (note 4 + sketch 4) = 32; (c) two environmental considerations × 7 = 14. Complete 60.'
S8 = 'The method in (a) is open ("or by any other suitable method"); the scheme works the degree of efficiency method.'
T8A = 'Determine by degree of efficiency method, or by any other suitable method, the approximate size of a vertical window for a living room 5.0 metres long by 3.8 metres wide requiring an average illumination of 150 lux on the working plane. Assume an unobstructed view and the illumination of a standard overcast sky to be 5000 lux.'
T8B = 'Discuss in detail, using notes and freehand sketches, two design considerations for a contemporary window frame and glazing system that will ensure the high thermal performance of both: the window frame and the glazing system.'
T8C = 'Outline two environmental considerations that should be taken into account when recommending a preferred material for the window frame.'
A8 = add('8', 'a', '(a)', T8A,
         [row('formula', 'Correct entry into formula', 4, 'The formula Li = Lo × WF × E × window area ÷ floor area 2, and the correct entry 2: 150 = 5,000 × 0.5 × 0.4 × W ÷ (5.0 × 3.8).'),
          row('floor-area', 'Floor area', 2, 'Floor area = 5.0 × 3.8 = 19.0 m².'),
          row('product', 'Lo×WF×E', 2, 'Lo × WF × E = 5,000 × 0.5 × 0.4 = 1,000.'),
          row('solve', 'Solve for w (window area) line 1', 4, 'Two lines solving for W, 2 each: 150 × 19 = 1,000 W; 2850 = 1000 W.'),
          row('window-area', 'Window area', 2, 'Window area = 2,850 ÷ 1,000 = 2.85 m².')],
         ['cons-7-2', 'cons-3-5'], ['windows-light'], 'q8-calculation', 'Units of illumination and the daylight factor (7.2) sizing a window (3.5).', B8, S8)
B8b = add('8', 'b', '(b)', T8B,
          [row('frame-1', 'Frame design 1', 8, 'Note 4 and sketch 4. Such as: a thermally broken wooden frame, the outside separated from the inside by a low-conductivity material.'),
           row('frame-2', 'Frame design 2', 8, 'A second, different frame design. Such as: composite materials with good insulation; good seals between sash and frame; a dwell vent system preheating incoming air between two frames.'),
           row('glazing-1', 'Glazing system 1', 8, 'Note 4 and sketch 4. Such as: double, triple or quadruple glazing with a low-e coating reflecting heat back into the house.'),
           row('glazing-2', 'Glazing system 2', 8, 'A second, different glazing design. Such as: argon, krypton or xenon gas fills; insulated spacers between the panes; an airtight assembly.')],
          ['cons-3-6', 'cons-6-2'], ['windows-light', 'heat-loss-insulation'], 'q8-window', 'Window frames and glazing (3.6) that cut heat loss (6.2).', B8, S8)
C8 = add('8', 'c', '(c)', T8C,
         [row('consideration-1', 'Environmental consideration 1', 7, 'Such as: a renewable frame material such as wood, with far less embodied energy than aluminium; local and easily replaced.'),
          row('consideration-2', 'Environmental consideration 2', 7, 'A second, different consideration. Such as: good insulation reducing fossil fuel for heating; durability, perhaps aluminium-clad timber; recyclable or biodegradable at end of life.')],
         ['cons-3-5', 'cons-1-2'], ['windows-light', 'sustainability-the-environment'], 'q8-environment', 'Window materials (3.5) chosen sustainably (1.2).', B8, S8)
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-window', B8, S8, parts(('a', T8A), ('b', T8B), ('c', T8C)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p32 (printed 10): (a) three requirements × (note 4 + sketch 4) = 24; (b) two leakage routes × 5 and their design details × (note 2 + sketch 2), and materials 2 = 20; (c) two advantages × 8 = 16. Complete 60.'
S9 = 'The requirements and leakage routes are open responses with no printed list.'
AIR = (['cons-6-5', 'cons-6-6'], ['condensation-air-tightness'])
T9A = 'Discuss in detail, using notes and freehand sketches, three functional requirements of an attic space suitable for use as a living area.'
T9B = 'The sketch shows the outline of an attic space in a new house. Identify two possible air leakage routes in the attic space. Using notes and freehand sketches, show clearly the correct design detailing that will improve the airtightness level at each air leakage route identified. Specify the materials used to achieve satisfactory airtightness levels.'
T9C = 'Discuss two advantages of improved airtightness in the attic space.'
A9 = add('9', 'a', '(a)', T9A,
         [row(f'requirement-{i}', f'Functional requirement {i}', 8, note) for i, note in [
             (1, 'Note 4 and sketch 4. Such as: adequate floor area, height, light and ventilation; adequate access.'),
             (2, 'A second, different requirement. Such as: fire resistance — fire-grade plasterboard, fire stops, encased steel and a safe means of escape; sound insulation with a floating, isolated floor.'),
             (3, 'A third, different requirement. Such as: structural integrity with correctly sized joists; a vapour barrier and roof ventilation against condensation; insulation to 0.2 W/m²K without thermal bridges.')]],
         ['cons-3-8', 'cons-1-9', 'cons-6-2'], ['roofs', 'fireplaces-fire-prevention', 'heat-loss-insulation'], 'q9-requirements',
         'An attic conversion (3.8) meeting fire (1.9) and thermal (6.2) requirements.', B9, S9)
B9b = add('9', 'b', '(b)', T9B,
          [row('leakage-1', 'Air leakage 1', 5, 'Such as: the junction of the wall and floor, or the sloping ceiling and the vertical wall.'),
           row('detail-1', 'Design detail 1', 4, 'Note 2 and sketch 2. Such as: the skirting sealed to the floor with flexible sealant or tape; a continuous air barrier taped at the junctions; plasterboard joints sealed; a void for services.'),
           row('leakage-2', 'Air leakage 2', 5, 'A second, different route. Such as: the roof light; services such as lights, plugs, switches and pipes piercing the barrier.'),
           row('detail-2', 'Design detail 2', 4, 'Note 2 and sketch 2. Such as: tape and flexible sealant round the roof light, taped to the roof membrane; grommets and proprietary socket boxes at services.'),
           row('materials', 'Specification of materials', 2, 'The materials specified, such as airtight tape, flexible sealant, membranes and grommets.')],
          *AIR, 'q9-leakage', 'Airtightness (6.5) and vapour control (6.6).', B9, S9)
C9 = add('9', 'c', '(c)', T9C,
         [row('advantage-1', 'Advantage 1', 8, 'Such as: build tight and ventilate right — less heat lost to draughts, which can be up to half of all heat loss; no cold draughts.'),
          row('advantage-2', 'Advantage 2', 8, 'A second, different advantage. Such as: moist indoor air kept out of the structure, preventing interstitial condensation and decay; lower carbon emissions.')],
         *AIR, 'q9-advantages', 'Airtightness (6.5) and condensation (6.6).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-leakage', B9, S9, parts(('a', T9A), ('b', T9B), ('c', T9C)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p33 (printed 11): (a) any two of three printed items × (note 4 + sketch 4) = 16; (b) two operating principles × (note and sketch 4 + 4) = 16 and two advantages × 4 = 8; (c) two overheating details × (note 5 + sketch 5) = 20. Complete 60.'
S10 = 'Choice is not a route: part (a) (any two of three printed items) is ONE card with an any-two group over the scheme headings; its figure and the complete-question figure carry all three items. The OR alternative is a separate Question 10 route.'
T10A = 'Using notes and freehand sketches, discuss in detail the importance of any two of the following in the design of a Passive House: shape and form of the house; continuity of insulation; reduced thermal/cold bridging.'
T10B = 'The layout of a Mechanical Heat Recovery with Ventilation system (MHRV) for a Passive House is shown in the accompanying sketch. Explain, using notes and freehand sketches, the operating principles of such a system and discuss two advantages of this system for a Passive House.'
T10C = 'Show, using notes and freehand sketches, two design details that would help prevent the possible overheating of a Passive House in summer.'
ITEMS10 = [('Shape and Form', 'a compact form with a low surface-to-volume ratio; maximum glazing to the south and minimum to the north; open-plan living, a sunspace and draught lobbies; a 45° roof for solar panels.'),
           ('Continuity of Insulation', 'rigid wall insulation carried down to the foundation; at least 300 mm under the whole slab, with edge insulation; insulation continuous at the eaves; triple-glazed, thermally broken windows.'),
           ('Reduced cold bridge', 'continuous insulation at the window reveals, head and cill, at the top of the wall at wallplate level, and at the ground floor and wall junction.')]
A10 = add('10', 'a', '(a)', T10A,
          [anyn('items', 'Design of a passive house', 2, 8, ITEMS10, 'Any two of the three printed items, each note 4 and sketch 4 = 8.')],
          ['cons-6-2', 'cons-6-4'], ['passive-design', 'heat-loss-insulation'], 'q10-principles',
          'The union of the three printed items: form and solar gain (6.4), continuous insulation and freedom from cold bridges (6.2).', B10, S10)
B10b = add('10', 'b', '(b)', T10B,
           [row('principle-1', 'Operating principle 1', 8, 'Note and sketch. Such as: warm air extracted from the kitchen, bathroom and utility passes to the heat exchange unit, where its heat is taken out.'),
            row('principle-2', 'Operating principle 2', 8, 'A second principle. Such as: the recovered heat warms the colder incoming fresh air, which is distributed through a separate, independent duct system.'),
            row('advantage-1', 'Advantage 1', 4, 'Such as: up to 93% of the heat recovered, cutting heating costs; no conventional heating system needed.'),
            row('advantage-2', 'Advantage 2', 4, 'A second, different advantage. Such as: filters against pollen and allergens; less mould; odours removed; a constant flow of fresh air to bedrooms.')],
           ['cons-6-5'], ['passive-design', 'condensation-air-tightness'], 'q10-mhrv', 'Ventilation with heat recovery (6.5).', B10, S10)
C10 = add('10', 'c', '(c)', T10C,
          [row('detail-1', 'Design detail 1', 10, 'Note 5 and sketch 5. Such as: brise soleil over the large glazed area; an extended but not excessive soffit overhang.'),
           row('detail-2', 'Design detail 2', 10, 'A second, different detail: note 5 and sketch 5. Such as: heavily lined blinds or curtains or timber shutters; openings opposite each other for through ventilation; opening sashes.')],
          ['cons-6-4', 'cons-6-5'], ['passive-design'], 'q10-mhrv', 'Solar heat gain (6.4) and ventilation (6.5).', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-principles', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p34 (printed 12): discussion of the statement, three points × 10 = 30; three guidelines × 10 = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately, so each is its own task and the complete card composes them.'
TAA = 'Discuss the above statement in detail.'
TAB = 'Propose three guidelines that would help create environmentally sustainable urban development in Ireland.'
TALL = 'Discuss the above statement in detail and propose three guidelines that would help create environmentally sustainable urban development in Ireland.'
URBAN = (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'])
AA = add('10', 'discussion', ' — discussion', TAA,
         [row(f'point-{i}', f'Point {i} - discussion', 10, note) for i, note in [
             (1, 'Such as: controlling sprawl by building close to amenities, renewing town centres as places to live at carefully planned higher densities.'),
             (2, 'Such as: integrated transport with good bus, rail and light rail; better public realms — safe, overlooked, well-managed public spaces and play areas.'),
             (3, 'Such as: diverse, walkable, human-scaled towns with distinctive character, inclusive universal design and adaptable, efficient buildings. Three distinct, well-argued points are needed.')]],
         *URBAN, None, 'Sustainable urban development (1.2, 1.3).', BALT, SALT, alt=True)
AB = add('10', 'guidelines', ' — guidelines', TAB,
         [row(f'guideline-{i}', f'Guideline {i}', 10, note) for i, note in [
             (1, 'Such as: energy analysis and low embodied energy design for every development; urban living made an attractive option.'),
             (2, 'Such as: modest, flexible buildings for every stage of life; building close to amenities and in clusters so people walk and cycle.'),
             (3, 'Such as: renewable energy and A-rated fittings; clear sustainable planning guidelines; grants and education for sustainable design. Three distinct guidelines are needed.')]],
         *URBAN, None, 'Sustainable urban development (1.2, 1.3).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, TALL, labels=['Discussion of the statement', 'Three guidelines'], alt=True)

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and four other questions (300 marks); all question banks retained, no full-exam Cartesian cards.'),
          (2, 'select', 'Q2(b) select any two areas from the given diagram: the scheme marks any two areas alike, one card with two area rows (choice is not a route).'),
          (2, 'any two', 'Q2(b) the same two areas.'),
          (2, 'either', 'Q3 "either: an internal insulation system or an external insulation system": both systems are required ("for each of the insulation systems").'),
          (2, 'or', 'Q3 the same two systems, both required.'),
          (4, 'or', 'Q8(a) "degree of efficiency method, or by any other suitable method": an open choice of method within one task.'),
          (4, 'any other', 'Q8(a) the same open choice of method.'),
          (5, 'any two', 'Q10(a) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
          (5, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.')]
FINITE = {'10a': dict(choose=2, options=[h for h, _ in ITEMS10], cardId=A10['id'], groupRowId='items')}
D.finish(LEDGER, FINITE, {})
