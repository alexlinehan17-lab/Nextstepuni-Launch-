"""Draft the 2012 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 24-34; the English scheme carries Irish running headers). This paper was never carded: every task is
added. Q9(b) "select any three locations" from the four circled and Q10(a) "any two of the following" are ONE
card each with an anyN group (choice is not a route). Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Triple-glazed bay window with a lean-to roof', concept='bay-window-roof-section',
              stem='A triple-glazed bay window projects 1.5 metres from the external wall of a dwelling house, as shown in the accompanying sketch. The external wall is a 350 mm concrete block wall with an insulated cavity. The lean-to roof is an insulated slated roof and has a pitch of 30°. Insulated plasterboard is fixed to the underside of the rafters to form a sloped ceiling.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the abutment detail in (b) is marked separately.'),
    '2': dict(page=2, title='Designing for lifetime use and a wheelchair-accessible bathroom', concept='lifetime-use-bathroom', stem='',
              note='Original plan retained. Both printed areas in (a) and all five printed bathroom items in (b) and (c) are required.'),
    '3': dict(page=2, title='Converting a storeroom: sunlight and thermal upgrade', concept='storeroom-conversion',
              stem='The drawing shows the elevation and plan of a semi-detached house with an adjoining storeroom. All external walls are of single leaf 215 mm hollow block construction and all roofs are slated. All internal walls are of solid block construction and the internal wall A-A is load-bearing. The storeroom wall B-B is south facing. It has been decided to convert the storeroom in order to enlarge the living space. In the conversion, you need to give consideration to: redesigning the ground floor layout to allow increased penetration of sunlight to the interior and upgrading the thermal properties of the external walls.',
              note='Original elevation and plan retained. Both printed considerations are required; the designs are open responses.'),
    '4': dict(page=3, title='Septic tank and percolation area', concept='septic-tank-percolation',
              stem='The typical layout of an on-site wastewater treatment system suitable for a single house is shown in the accompanying drawing.',
              note='Original drawing retained. The percolation details are a marking menu, not a printed choice.'),
    '5': dict(page=3, title='Uninsulated ground floor U-value, heat-loss cost and a Passive floor', concept='uninsulated-floor-u-value',
              stem='A house built in the 1970s has an un-insulated solid concrete ground floor with a sand/cement fine screed finish.',
              note='All printed data are retained in the original question. Part (b) uses the U-value from (a); the scheme’s worked answers are U = 0.704 W/m²K and an annual cost of €183.13.'),
    '6': dict(page=4, title='Doing more with less for longer', concept='more-with-less-house',
              stem='The elevation and ground floor plan of a house are shown. The house has a study / office as shown and also has three bedrooms and a bathroom upstairs. The external wall is of timber frame construction with a concrete block outer leaf. The house is designed to have low environmental impact, reflecting the sustainable ideal of doing more with less for longer.',
              note='Original elevation and plan retained. Features are open responses; all three printed considerations in (b) are required.'),
    '7': dict(page=4, title='Panelled entrance door in a timber frame wall', concept='entrance-door-timber-frame-section',
              stem='The main entrance door to a two storey dwelling house is a four-panel solid wooden door. The external wall in which the door is fitted is of timber frame construction with a rendered concrete block outer leaf. This wall supports the first floor joists, as shown in the accompanying outline drawing.',
              note='Original outline drawing retained. Construction, dimension and scale/drafting marks belong to part (a); the vapour control layer in (b) is marked separately.'),
    '8': dict(page=4, title='Ring main sockets, safety and saving electricity', concept='ring-main-circuit', stem='',
              note='All printed requirements are marked; the safety features and strategies are open responses.'),
    '9': dict(page=5, title='Designing for airtightness', concept='airtightness-design',
              stem='Designing for airtightness presents one of the most challenging aspects of contemporary house design.',
              note='Original section with four circled locations retained. Part (b) is a closed choice of any three of the four: one card holding all four, named by the scheme’s headings.'),
    '10': dict(page=5, title='Passive House principles, MHRV and Passive House construction', concept='passive-house-construction', stem='',
               note='Original plan retained. Part (a) is a closed choice of any two of the three printed items: one card holding all three.'),
}
ALT = dict(page=5, title='A sustainable ethos and the building’s life cycle (alternative Question 10)', concept='building-life-cycle',
           stem='“A sustainable ethos in building will require the consideration of environmental implications associated with design, construction and operation of buildings and neighbourhoods; and greater emphasis on the improvement of existing buildings. Most buildings are used for several decades, and many survive for centuries. As the community’s principal physical asset, getting good value requires that the building’s full life cycle be considered, avoiding short-sighted attempts to merely minimise initial cost.” THE GREEN VITRUVIUS – PRINCIPLES AND PRACTICE OF SUSTAINABLE ARCHITECTURAL DESIGN (2011) by Vivienne Brophy and J Owen Lewis (UCD). - Earthscan Ltd, 14a St Cross Street, London ECIN 8XA, UK',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately.')
SCHEME_PAGES = {'1': [4, 24], '2': [5, 6, 25], '3': [6, 7, 26], '4': [8, 27], '5': [9, 28], '6': [10, 11, 12, 29],
                '7': [13, 30], '8': [14, 15, 31], '9': [15, 16, 32], '10': [17, 18, 19, 20, 33], '10-alt': [20, 21, 34]}
D = cp.Draft(HERE, 2012, 'higher', ('2a13b942b63a681f24f3a0a146afdd78e3020e620a3c63dac93a1c822d5bef20',
                                    '1d92d18557cfb807abeb7d938cf5baac82f061135cb8a6f755e2c1d607c93995'), 0, QUESTIONS, SCHEME_PAGES, alt=ALT)
row, add, compose, parts, anyn = D.row, D.add, D.compose, D.parts, D.anyn
D.figures({
    'q1-original': D.paper(2, [30, 50, 580, 256]), 'q2-original': D.paper(2, [30, 256, 580, 517]),
    'q3-original': D.paper(2, [30, 517, 580, 775]), 'q4-original': D.paper(3, [30, 50, 580, 327]),
    'q5-original': D.paper(3, [30, 327, 580, 790]), 'q6-original': D.paper(4, [30, 50, 580, 403]),
    'q7-original': D.paper(4, [30, 403, 580, 623]), 'q8-original': D.paper(4, [30, 623, 580, 790]),
    'q9-original': D.paper(5, [30, 50, 580, 331]), 'q10-original': D.paper(5, [30, 331, 580, 620]),
    'q10-alt-original': D.paper(5, [30, 640, 580, 790]),
    'q1-section': D.scheme(4, [40, 57, 585, 784]),
    'q2-requirements': D.scheme(5, [40, 60, 585, 515]),
    'q2-layout': D.composite((5, [40, 476, 300, 515]), (5, [40, 515, 585, 783])),
    'q2-locations': D.scheme(6, [40, 60, 585, 450]),
    'q3-design': D.composite((6, [40, 450, 585, 784]), (7, [40, 60, 585, 558])), 'q3-reasons': D.scheme(7, [40, 558, 585, 784]),
    'q4-scheme': D.scheme(8, [40, 60, 585, 784]),
    'q5-calculation': D.scheme(9, [40, 60, 585, 612]), 'q5-floor': D.scheme(9, [40, 612, 585, 784]),
    'q6-features': D.composite((10, [40, 60, 585, 784]), (11, [40, 60, 585, 275])),
    'q6-importance': D.composite((11, [40, 275, 585, 784]), (12, [40, 60, 585, 560])),
    'q7-section': D.scheme(13, [40, 60, 585, 784]),
    'q8-wiring': D.composite((14, [40, 60, 205, 178]), (14, [205, 60, 585, 337])),
    'q8-safety': D.composite((14, [40, 176, 205, 337]), (14, [40, 337, 585, 536]), (14, [460, 220, 560, 334])),
    'q8-economy': D.composite((14, [40, 536, 585, 784]), (15, [40, 60, 585, 160])),
    'q9-airtightness': D.scheme(15, [40, 160, 585, 784]),
    'q9-locations': D.scheme(16, [40, 60, 585, 645]), 'q9-service': D.scheme(16, [40, 645, 585, 784]),
    'q10-principles': D.composite((17, [40, 60, 585, 784]), (18, [40, 60, 585, 273.5]), (20, [40, 60, 585, 240])),
    'q10-mhrv': D.composite((18, [40, 273.5, 585, 784]), (19, [40, 60, 585, 462])),
    'q10-passive': D.scheme(19, [40, 462, 585, 784]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p24 (printed 21): (a) best twelve points × 4 (drawing 3, annotation 1) = 48 and scale and drafting 8 = 56; (b) abutment design detail 4. Complete 60.'
S1 = 'One required section and one required abutment detail. The detail list is a marking menu, not a printed choice.'
T1A = 'To a scale of 1:5, draw a vertical section through the window, roof and front wall of the house. The section should show the typical construction details from 400 mm below the concrete lintels of the bay window, through the fixed frame of the window, wallplate and rafter to a level 400 mm above the abutment of the lean-to roof and the front wall of the house.'
T1B = 'Indicate on your drawing the design detailing that ensures moisture does not penetrate at the abutment of the roof and the wall of the house.'
A1 = add('1', 'a', '(a)', T1A,
         [row('details', 'Any 12 points × 4 marks', 48, 'Best twelve points, 4 each (drawing 3, annotation 1). Menu: slates; battens; felt or breather membrane; rafter; roof insulation; vapour control layer; ventilation to the roof; wallplate or hanger to the main wall; insulated plasterboard; fascia, soffit and gutter; lead flashing; cavity wall and ties; cavity closer; internal and external plaster; wall insulation; stepped DPC in the cavity; lintels; wallplate; window frame; triple-glazed unit.', list(range(0, 49, 4))),
          row('presentation', 'Scale and Drafting', 8, 'Scale and drafting of the section.')],
         ['cons-1-5', 'cons-3-6', 'cons-3-9', 'cons-3-10'], ['question-1-drawing-questions', 'windows-light', 'roofs'], 'q1-section',
         'Scaled drawing (1.5) of a bay window (3.6) under a slated lean-to roof (3.9) at its abutment (3.10).', B1, S1)
B1b = add('1', 'b', '(b)', T1B,
          [row('abutment', 'Design detail', 4, 'Show the abutment detail, as in the scheme’s model section: a lead flashing and a stepped DPC in the cavity over the lean-to roof.')],
          ['cons-3-10', 'cons-3-4'], ['roofs', 'walls'], 'q1-section', 'Roof abutments (3.10) with flashings and a stepped DPC (3.4).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p25 (printed 22): (a) two requirements × (note 6 + sketch 5) = 22; (b) five printed items × 4 = 20 and three typical dimensions 3 = 23; (c) five printed items × 3 = 15. Complete 60.'
S2 = 'Both printed areas in (a) and all five printed bathroom items in (b) and (c) are required, each separately marked; not a choice.'
LIFE = (['cons-1-2'], ['planning-sustainability-environment'])
T2A = 'Discuss in detail, using notes and freehand sketches, two functional requirements of a dwelling house designed for lifetime use. Refer in particular to the: main entrance and internal corridor layout.'
T2B = ('The layout of a bedroom and an adjoining bathroom, which is 2.3 m × 2.9 m, is shown in the accompanying drawing. The hot press is also shown. Using notes and freehand sketches, show a preferred layout for the bathroom space to ensure that it is suitable for a person in a wheelchair. '
       'Indicate in your design sketches the location of the following: window, shower area, toilet, wash hand basin and grab rails. Include three typical dimensions.')
T2C = 'Discuss your preferred location for the bathroom items listed at 2(b) above.'
A2 = add('2', 'a', '(a)', T2A,
         [row('requirement-1', 'Functional requirement 1', 11, 'Note 6 and sketch 5. Such as, the main entrance: level access no steeper than 1:50; a 1200 × 1200 mm clear area at the door; an 800 mm clear opening; a flush threshold, at most 15 mm; good lighting and a porch.'),
          row('requirement-2', 'Functional requirement 2', 11, 'A second requirement: note 6 and sketch 5. Such as, the internal corridors: kept to a minimum; at least 1200 mm wide for wheelchair users; a 1500 mm turning circle; switches and handles at 900–1200 mm; motion-sensor lighting.')],
         *LIFE, 'q2-requirements', 'Lifetime, universal design of the built environment (1.2).', B2, S2)
B2b = add('2', 'b', '(b)', T2B,
          [row('items', 'Preferred layout for bathroom space (5 × 4 marks)', 20, 'Window, shower area, toilet, wash hand basin and grab rails each located, 4 each, around a clear 1500 mm turning circle, as in the scheme’s model layouts; alternative layouts are accepted.'),
           row('dimensions', '3 typical dimensions', 3, 'Three typical dimensions, 1 each.')],
          *LIFE, 'q2-layout', 'Universal design of a bathroom (1.2).', B2, S2)
C2 = add('2', 'c', '(c)', T2C,
         [row('window', 'Window', 3, 'Such as: a low cill near the toilet for ventilation, with lever handles low on the sash.'),
          row('shower', 'Shower area', 3, 'Such as: a flush tray or wet area at least 1000 × 1000 mm; a flip seat; vertical and horizontal 35 mm grab rails; a non-slip floor.'),
          row('toilet', 'Toilet', 3, 'Such as: a fold-up rail on the open side and a fixed rail on the wall at 700 mm; a lever flush; an alarm cord.'),
          row('basin', 'Wash hand basin', 3, 'Such as: wall-mounted at 800 mm with knee space beneath; close to the toilet; lever or sensor taps; a 1500 mm turning circle.'),
          row('rails', 'Grab rails', 3, 'Such as: folding grab rails installed close to all appliances.')],
         *LIFE, 'q2-locations', 'Universal design of a bathroom (1.2).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-layout', B2, S2, parts(('a', T2A), ('b', T2B), ('c', T2C)))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p26 (printed 23): (a) layout and glazing, note and sketch 2 × 10 = 20, and the thermal upgrade, note and sketch 2 × 10 = 20 = 40; (b) reasons for the floor layout 10 and for the wall upgrade 10 = 20. Complete 60.'
S3 = 'Both printed considerations are required; the designs are open responses.'
T3A = 'Show, using notes and freehand sketches, a revised design detailing for the dwelling house.'
T3B = 'For each of the above, discuss in detail the reasons for your proposed design choices.'
A3 = add('3', 'a', '(a)', T3A,
         [row('layout', 'Design detailing : Layout / glazing', 20, 'Notes and sketches, 2 × 10. Such as: high-performance low-e double or triple glazing on the south elevation; roof lights; glazed doors to the storeroom and between it and the dining room; the kitchen wall removed on an RSJ or lintels; bi-fold glazed doors; a draught lobby.'),
          row('thermal', 'Design detailing : Upgrade thermal properties', 20, 'Notes and sketches, 2 × 10. Such as: external insulation on the hollow block, 80–300 mm, fixed with adhesive and bolts, with fibreglass mesh and two coats of acrylic render; windows moved to the outer edge; thermal bridges detailed out; XPS carried below ground to the foundation.')],
         ['cons-1-2', 'cons-3-6', 'cons-6-2'], ['planning-sustainability-environment', 'windows-light', 'heat-loss-insulation'], 'q3-design',
         'Redesigning the house (1.2) with glazing (3.6) and external insulation (6.2).', B3, S3)
B3b = add('3', 'b', '(b)', T3B,
          [row('layout-reasons', 'Discussion - reasons for revised floor layout', 10, 'Such as: warm, sunlit, spacious living; the health benefits of natural light; tall windows for winter sun, with shades or brise-soleil against summer overheating.'),
           row('wall-reasons', 'Discussion - reasons for external wall upgrade', 10, 'Such as: external insulation preferred to dry lining, using the thermal mass of the block walls; less condensation with thermal bridges removed; lower costs, fossil fuel use and CO₂.')],
          ['cons-6-4', 'cons-6-2'], ['passive-design', 'heat-loss-insulation'], 'q3-reasons', 'Solar gain (6.4) and insulation (6.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-design', B3, S3, parts(('a', T3A), ('b', T3B)))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p27 (printed 24): (a) two operating principles × (discussion 7 + sketch 7) = 28; (b) any four percolation details × (note 2 + sketch 2) = 16 and any two dimensions 4 = 20; (c) three reasons × 4 = 12. Complete 60.'
S4 = 'The percolation details in (b) are a marking menu, not a printed choice.'
SEPTIC = (['cons-5-5'], ['drainage'])
T4A = 'Describe in detail, using notes and freehand sketches, the operating principles of a conventional septic tank system.'
T4B = 'Show, using notes and freehand sketches, the typical design detailing for the percolation area to ensure the safe treatment of waste from the septic tank. Include dimensions as appropriate.'
T4C = 'Discuss in detail three reasons why a proposed site for a dwelling house may be unsuitable for a conventional septic tank wastewater treatment system.'
A4 = add('4', 'a', '(a)', T4A,
         [row('principle-1', 'Operating principle 1', 14, 'Discussion 7 and sketch 7. Such as: a prefabricated primary settlement tank, at least 7.0 m from the house, sized for at least four persons; solids settle and scum floats in the first chamber, where anaerobic bacteria break the solids down.'),
          row('principle-2', 'Operating principle 2', 14, 'A second principle: discussion 7 and sketch 7. Such as: the liquid passes through openings in the dividing wall to the second chamber for further settlement, then drains to the percolation area, where aerobic bacteria in the gravel break down the remaining impurities; a watertight, ventilated cover.')],
         *SEPTIC, 'q4-scheme', 'Septic tanks (5.5).', B4, S4)
B4b = add('4', 'b', '(b)', T4B,
          [row('details', 'Design detailing of percolation area - any 4', 16, 'Best four details, note 2 and sketch 2 each. Menu: soil; geotextile layer; distribution box; perforated pipes; washed clean gravel (8–32 mm); vents. Such as: a distribution box feeding at least four 100–110 mm perforated pipes with 8 mm holes at 4, 6 and 8 o’clock, runs of at most 18.0 m at 2.0 m spacing, in gravel under a geotextile layer and topsoil.', list(range(0, 17, 2))),
           row('dimensions', 'Dimensions - any two', 4, 'Any two dimensions, 2 each, such as the 18.0 m pipe run and the 2.0 m spacing.')],
          *SEPTIC, 'q4-scheme', 'Percolation areas for septic tanks (5.5).', B4, S4)
C4 = add('4', 'c', '(c)', T4C,
         [row(f'reason-{i}', f'Reason {i}', 4, note) for i, note in [
             (1, 'Such as: a site too small for the tank and percolation area; unsuitable or shallow subsoil percolating too quickly or too slowly.'),
             (2, 'A second, different reason. Such as: too close to a stream, river, lake, well, wetland, boundary, house or another percolation area; a site too steep.'),
             (3, 'A third, different reason. Such as: no access to empty the tank; a water table less than 2.0 m below the original ground surface.')]],
         ['cons-5-5', 'cons-1-3'], ['drainage', 'planning-sustainability-environment'], 'q4-scheme', 'Septic tanks (5.5) and the choice of site (1.3).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-scheme', B4, S4, parts(('a', T4A), ('b', T4B), ('c', T4C)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p28 (printed 25): (a) ten points × 3 = 30 (tabulation, seven layers, total resistance, U-value); (b) five steps × 3 = 15; (c) Passive floor notes 5 + sketches 10 = 15. Complete 60.'
S5 = 'No printed choice. Part (b) uses the U-value from (a).'
DATA5 = ('Sand/cement fine screed thickness 60 mm; Concrete floor slab thickness 100 mm; Damp proof membrane (DPM) thickness 0.25 mm; Sand blinding thickness 50 mm; Hardcore thickness 225 mm; Subsoil thickness 300 mm. '
         'Thermal data of concrete ground floor: Resistance of internal surface (R) 0.104 m2 °C/W; Resistivity of fine screed (r) 0.710 m °C/W; Conductivity of concrete floor slab (k) 0.160 W/m °C; Conductivity of DPM (k) 0.250 W/m °C; '
         'Conductivity of sand blinding (k) 0.160 W/m °C; Conductivity of hardcore (k) 1.330 W/m °C; Conductivity of subsoil (k) 1.800 W/m °C.')
T5A = 'Calculate the U-value of the concrete ground floor given the following data: ' + DATA5
T5B = ('Using the U-value of the concrete ground floor obtained at 5(a) above and the following data, calculate the cost of heat lost annually through the un-insulated concrete floor slab: '
       'Dimensions of floor 9.0 metres × 7.0 metres; Average internal temperature 20° C; Average external temperature of subsoil 5° C; Heating period 12 hours per day for 40 weeks per annum; '
       'Cost of oil 85 cent per litre; Calorific value of oil 37350 kJ per litre; 1000 Watts 1 kJ per second.')
T5C = 'An insulated concrete ground floor is designed to prevent the penetration of radon gas through the floor and to meet the Passive House standard. Using notes and freehand sketches, show the typical design detailing for such a floor.'
A5 = add('5', 'a', '(a)', T5A,
         [row('tabulation', 'Correct tabulation', 3, 'The calculation set out in a table of material, conductivity or resistivity, thickness and resistance.'),
          row('resistances', '10 points × 3 marks for each point', 21, 'Seven resistances, 3 each, by R = T/k (R = T × r for the screed): screed 0.060 × 0.710 = 0.0426; slab 0.100/0.160 = 0.625; DPM 0.00025/0.250 = 0.001; sand blinding 0.050/0.160 = 0.3125; hardcore 0.225/1.330 = 0.1692; subsoil 0.300/1.800 = 0.1667; internal surface 0.104 (given). All in m²°C/W.', list(range(0, 22, 3))),
          row('total-resistance', 'Total Resistance', 3, 'Total resistance, the sum of R = 1.421 m²°C/W.', [0, 3]),
          row('u-value', 'U-value (1 mark for the formula)', 3, 'U = 1/Rt = 1 ÷ 1.421 = 0.704 W/m²K (1 mark for the formula).')],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Thermal resistance, conductivity and transmittance (6.1).', B5, S5)
B5b = add('5', 'b', '(b)', T5B,
          [row('heat-loss', 'Heat loss formula and calculation', 3, 'Heat loss = U-value × area × temperature difference = 0.704 × 63 × 15 = 665.28 watts (joules per second).'),
           row('duration', 'Heating duration for one year', 3, 'Heating period = 12 × 7 × 40 = 3,360 hours = 12,096,000 seconds.'),
           row('energy', 'k/joules calculation for one year', 3, 'Energy = 12,096,000 × 665.28 ÷ 1000 = 8,047,226 kJ per year.'),
           row('oil', 'litres of oil for one year', 3, 'Oil = 8,047,226 ÷ 37,350 = 215.45 litres per year.'),
           row('cost', 'Annual cost of heat lost', 3, 'Annual cost = 215.45 × €0.85 = €183.13.')],
          ['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Heat loss calculation and running costs (6.3) from the U-value (6.1).', B5, S5)
C5 = add('5', 'c', '(c)', T5C,
         [row('notes', 'Passive insulated ground floor with radon barrier Notes', 5, 'Such as: 25 mm screed on a 75 mm slab; 250–400 mm expanded polystyrene for U ≤ 0.15 W/m²K; a radon barrier; sand blinding and hardcore; a low-conductivity thermal block in the inner leaf; 300 mm cavity insulation.'),
          row('sketches', 'Sketches', 10, 'A sketch of the floor and its junction with the wall, as in the scheme’s model detail.')],
         ['cons-4-2', 'cons-6-2', 'cons-3-4'], ['floors', 'heat-loss-insulation', 'walls'], 'q5-floor', 'An insulated ground floor (4.2, 6.2) with a radon barrier (3.4).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p29 (printed 26): (a) three features × (note 5 + sketch 5) = 30; (b) three printed considerations × (5 for point + 5 for discussion) = 30. Complete 60.'
S6 = 'The features are open responses; all three printed considerations in (b) are required.'
GREEN = (['cons-1-2', 'cons-6-4'], ['sustainability-the-environment'])
T6A = 'With reference to the design shown, discuss in detail, using notes and freehand sketches, three features of the design that reflect the sustainable ideal of doing more with less for longer.'
T6B = 'Discuss in detail the importance of each of the following when designing an environmentally sustainable dwelling house: orientation of house; flexibility of design; sourcing of materials.'
A6 = add('6', 'a', '(a)', T6A,
         [row(f'feature-{i}', f'Feature {i}', 10, note) for i, note in [
             (1, 'Note 5 and sketch 5. Such as: the roof space used for three bedrooms and a bathroom on one compact foundation; roof lights giving three times the daylight of dormers.'),
             (2, 'A second, different feature: note 5 and sketch 5. Such as: south-facing high-performance glazing and small north windows; a porch or draught lobby; a wood-burning stove on an internal chimney.'),
             (3, 'A third, different feature: note 5 and sketch 5. Such as: rainwater harvesting in above-ground tanks; solar panels on the south roof at about 45°.')]],
         ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-features',
         'Sustainable design of the built environment (1.2), solar gain (6.4) and insulation (6.2).', B6, S6)
B6b = add('6', 'b', '(b)', T6B,
          [row('orientation', 'Orientation of house (5 for point, 5 for discussion)', 10, 'Point 5 and discussion 5. Such as: the longer elevation on an east–west axis with large high-performance south windows for passive solar gain, cutting costs and fossil fuel use.'),
           row('flexibility', 'Flexibility of design (5 for point, 5 for discussion)', 10, 'Point 5 and discussion 5. Such as: universal design for all ages and abilities; a ground floor study convertible to a bedroom near an accessible bathroom; open plan; 800 mm doors; no ground floor steps.'),
           row('materials', 'Sourcing materials (5 for point, 5 for discussion)', 10, 'Point 5 and discussion 5. Such as: local, renewable, naturally durable timber; low-carbon GGBS concrete; local stone, sand and block with less transport, embodied energy and CO₂.')],
          *GREEN, 'q6-importance', 'Sustainable design of the built environment (1.2) with solar gain (6.4).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b], 'q6-features', B6, S6, parts(('a', T6A), ('b', T6B)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p30 (printed 27): (a) best nine points × 5 (sketch 4, annotation 1) = 45, any four typical dimensions × 1 = 4 and scale and drafting 8 = 57; (b) position of the vapour barrier 3. Complete 60.'
S7 = 'One required section and one required vapour control detail. The detail list is a marking menu, not a printed choice.'
T7A = 'To a scale of 1:5, draw a vertical section through a portion of the external wall, doorframe, door and first floor joists. The section should show the typical construction details from 400 mm below the top of the door to a level 500 mm above the first floor joists. Include typical dimensions.'
T7B = 'Show clearly on your drawing the position of the vapour control layer to ensure an airtight structure.'
A7 = add('7', 'a', '(a)', T7A,
         [row('details', 'Timber frame - 9 points × 5 marks', 45, 'Best nine points, 5 each (sketch 4, annotation 1). Menu: doorframe; door; render; block outer leaf and lintel; breather membrane; sheathing; timber stud; insulation; airtight membrane, tape and sealant; plaster slab; solid timber lintel; stepped DPC; cavity barrier or fire check; finished floor; acoustic layer; plywood sheeting; first floor joists.', list(range(0, 46, 5))),
          row('dimensions', 'Any 4 typical dimensions (4 × 1 mark)', 4, 'Any four typical dimensions, 1 each.'),
          row('presentation', 'Scale & Drafting', 8, 'Scale and drafting of the section.')],
         ['cons-1-5', 'cons-3-7', 'cons-3-3', 'cons-4-3'], ['question-1-drawing-questions', 'doors', 'walls', 'floors'], 'q7-section',
         'Scaled drawing (1.5) of an entrance door (3.7) in a timber frame wall (3.3) carrying the first floor (4.3).', B7, S7)
B7b = add('7', 'b', '(b)', T7B,
          [row('vapour', 'Position of vapour barrier', 3, 'Show the vapour control layer on the warm side of the insulation, continuous and taped and sealed at the door and floor junctions, as in the scheme’s model section.')],
          ['cons-6-6', 'cons-6-5'], ['condensation-air-tightness'], 'q7-section', 'Vapour barriers (6.6) and airtightness (6.5).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p31 (printed 28): (a) six items × 4 — wiring diagram with consumer unit, socket connections, cable size and the live, neutral and earth colours = 24; (b) two safety features × (notes 6 + sketches 6) = 24; (c) two strategies with elaboration × 6 = 12. Complete 60.'
S8 = 'All printed requirements in (a) are marked; the safety features and strategies are open responses.'
ELEC = (['cons-5-8'], ['services-water-gas-electricity'])
T8A = 'Show, using notes and freehand sketches, the correct wiring layout for two electrical sockets in a ring mains circuit for a domestic electrical installation. Indicate on your sketch the sizes and the colour coding of all electrical cables used in the circuit.'
T8B = 'Show, using notes and freehand sketches, two safety features that should be incorporated into the design of the above circuit to ensure that the circuit is safe for all users.'
T8C = 'Discuss in detail two strategies that would ensure the economical use of electricity in the home.'
A8 = add('8', 'a', '(a)', T8A,
         [row('wiring', 'Correct wiring diagram to include consumer unit', 4, 'A ring from the consumer unit through both sockets and back, as in the scheme’s model diagram.'),
          row('sockets', 'Sockets – correct connections', 4, 'Live, neutral and earth correctly connected at each socket.'),
          row('cables', 'Size of cables', 4, '2.5 mm² twin core and earth cable.'),
          row('colours', 'Live colour - colour coding Neutral colour - colour coding Earth - colour coding', 12, 'Live brown, neutral blue and earth green and yellow, 4 each.', [0, 4, 8, 12])],
         *ELEC, 'q8-wiring', 'Domestic electrical circuits (5.8).', B8, S8)
B8b = add('8', 'b', '(b)', T8B,
          [row('feature-1', 'Safety feature 1', 12, 'Notes 6 and sketches 6. Such as: the circuit earthed, so a short circuit sends current to ground and trips the fuse or MCB; a fuse or MCB cutting the supply on a fault.'),
           row('feature-2', 'Safety feature 2', 12, 'A second, different feature: notes 6 and sketches 6. Such as: an RCD disconnecting within 25–40 milliseconds when it detects a 5–30 mA leakage; a socket RCD; cables isolated in conduits.')],
          *ELEC, 'q8-safety', 'Protection of domestic electrical circuits (5.8).', B8, S8)
C8 = add('8', 'c', '(c)', T8C,
         [row('strategy-1', 'Strategy plus elaboration 1', 6, 'Such as, lighting: smart meters; CFL bulbs using 80% less electricity; task lighting; occupancy sensors; daylight with light-coloured reflective walls.'),
          row('strategy-2', 'Strategy plus elaboration 2', 6, 'A second, different strategy. Such as, heating: timer switches on immersion heaters; zoned, thermostatic controls; lagging the cylinder and pipes; or low-energy appliances switched off rather than on standby.')],
         ['cons-5-8', 'cons-5-3'], ['services-water-gas-electricity'], 'q8-economy', 'Domestic electricity use (5.8) and heating controls (5.3).', B8, S8)
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-wiring', B8, S8, parts(('a', T8A), ('b', T8B), ('c', T8C)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p32 (printed 29): (a) two discussion points × (5 for point + 5 for discussion) = 20; (b) any three of the four circled locations × (note 5 + sketch 5) = 30; (c) two advantages × (2 for point + 3 for discussion) = 10. Complete 60.'
S9 = 'Choice is not a route: part (b) (any three of the FOUR circled locations) is ONE card with one any-three group over the four locations, named by the scheme’s headings; its figure carries all four.'
AIR = (['cons-6-5', 'cons-6-6'], ['condensation-air-tightness'])
T9A = 'Discuss in detail the importance of careful design detailing in improving the airtightness performance of a dwelling house.'
T9B = 'The drawing shows an outline section through a portion of a single storey house of timber frame construction. The outer leaf is of rendered concrete block and the ground floor is an insulated solid concrete floor. Select any three locations from those circled on the sketch and show, using notes and freehand sketches, the typical design detailing which will prevent air leakage at each of the locations selected.'
T9C = 'Discuss the advantages of including a service cavity in an external wall of timber frame construction, as shown in the accompanying sketch.'
LOCATIONS9 = [('Ground Floor', 'an airtightness membrane and butyl tape carried under the timber frame and bonded to the slab; mastic sealant under the skirting; mortar joints pointed and sealed; a service cavity so the barrier is not ruptured.'),
              ('Window Cill', 'the air barrier bonded to the DPC; joints at the window, window board and cill taped and sealed with mastic; a draught seal between the opening sash and the frame.'),
              ('Light Fittings', 'grommets around cables piercing the barrier; the barrier resealed with tape and mastic; no recessed lights, or enclosed casings; a service cavity where possible.'),
              ('Trapdoor', 'a gasket or draught seal along the batten; tape returned along the joist; a bolt compressing the seal; insulation on the back; a proprietary trapdoor with sealed rebates.')]
A9 = add('9', 'a', '(a)', T9A,
         [row(f'point-{i}', f'Discussion – point {i} (5 for point, 5 for discussion)', 10, note) for i, note in [
             (1, 'Point 5 and discussion 5. Such as: seal tight and ventilate right — a continuous airtight seal around the envelope removes draughts and heat loss; air leakage also lets dampness into the fabric.'),
             (2, 'A second, different point. Such as: a vapour check barrier cuts interstitial condensation and mould; a small tear can reduce its performance by a factor of up to 1600; laps of 100–150 mm taped, grommets for services, skilled installation and a blower door test.')]],
         *AIR, 'q9-airtightness', 'Airtightness (6.5) and vapour control (6.6).', B9, S9)
B9b = add('9', 'b', '(b)', T9B,
          [anyn('locations', 'Three locations', 3, 10, LOCATIONS9, 'Any three of the four circled locations, each note 5 and sketch 5 = 10.')],
          ['cons-6-5', 'cons-4-2', 'cons-3-6', 'cons-5-8'], ['condensation-air-tightness', 'floors', 'windows-light', 'services-water-gas-electricity'], 'q9-locations',
          'The union of the four circled locations: airtightness (6.5) at the ground floor (4.2), the window cill (3.6), light fittings (5.8) and the attic trapdoor.', B9, S9)
C9 = add('9', 'c', '(c)', T9C,
         [row('advantage-1', 'Discuss advantage 1 - (2 for point, 3 for discussion)', 5, 'Point 2 and discussion 3. Such as: the air continuity barrier is not pierced by services; easier work for plumbers and electricians.'),
          row('advantage-2', 'Discuss advantage 2 - (2 for point, 3 for discussion)', 5, 'A second, different advantage. Such as: room for more insulation, improving the wall’s thermal performance; better acoustic insulation; more taping and sealing for airtightness.')],
         ['cons-3-3', 'cons-6-5'], ['walls', 'condensation-air-tightness'], 'q9-service', 'Timber frame external walls (3.3) and airtightness (6.5).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-locations', B9, S9, parts(('a', T9A), ('b', T9B), ('c', T9C)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p33 (printed 30): (a) any two of three printed items × (note 5 + sketch 5) = 20; (b) ducting layout 10, direction of airflow 5 and how the system works 5 = 20; (c) two advantages and two disadvantages × 5 = 20. Complete 60.'
S10 = 'Choice is not a route: part (a) (any two of three printed items) is ONE card with an any-two group over the scheme headings; its figure and the complete-question figure carry all three items. The OR alternative is a separate Question 10 route.'
T10A = 'Using notes and freehand sketches as appropriate, discuss in detail the importance of any two of the following in the design of a Passive House: building form; indoor environment; energy performance.'
T10B = ('It is proposed to install a Mechanical Heat Recovery with Ventilation (MHRV) system for a Passive House, as shown in the drawing. The location of the MHRV unit - M - in the utility room is shown. '
        'Draw a single line diagram of the given plan and show a typical design layout for the ducting to such a unit. Indicate clearly the direction of airflow in all the ducts and describe how a Mechanical Heat Recovery with Ventilation (MHRV) system works. '
        'Note: While a plan of the room layout is required, it is not necessary to show the furniture.')
T10C = 'Discuss in detail two advantages and two disadvantages of Passive House construction.'
ITEMS10 = [('Building form', 'a compact form with a minimum of extensions, as heat is lost through the external surfaces; a surface-to-volume ratio of 0.7 or less.'),
           ('Indoor environment', 'relative humidity of 35–55% against respiratory illness, mould and dust mites; internal surfaces not below 12.6°C, preventing condensation.'),
           ('Energy performance', 'space heating demand at most 15 kWh/m²a; heating load at most 10 W/m²; primary energy demand at most 120 kWh/m²a, typically 60–70, with a conversion factor of 2.58 for electricity.')]
A10 = add('10', 'a', '(a)', T10A,
          [anyn('items', 'Discussion of 2 design details', 2, 10, ITEMS10, 'Any two of the three printed items, each note 5 and sketch 5 = 10.')],
          ['cons-6-2', 'cons-6-5', 'cons-6-3'], ['passive-design', 'heat-loss-insulation'], 'q10-principles',
          'The union of the three printed items: compact form and heat loss (6.2), the indoor environment (6.5) and energy demand (6.3).', B10, S10)
B10b = add('10', 'b', '(b)', T10B,
           [row('ducting', 'Design layout for ducting', 10, 'A single-line plan with supply ducts to the living spaces and bedrooms and extract ducts from the kitchen, bathroom and utility, as in the scheme’s model plan.'),
            row('airflow', 'Direction of airflow', 5, 'The direction of airflow shown in every duct.'),
            row('explanation', 'Explanation of how the system works', 5, 'Moist warm extract air and filtered outdoor air pass through a heat exchanger of thin plates without mixing; the warmed supply air goes to the living spaces; a post heater in cold weather, a summer bypass and a sound attenuator.')],
           ['cons-6-5'], ['passive-design', 'condensation-air-tightness'], 'q10-mhrv', 'Ventilation with heat recovery (6.5).', B10, S10)
C10 = add('10', 'c', '(c)', T10C,
          [row('advantage-1', 'Advantage 1', 5, 'Such as: about 75% less energy than a house built to the building regulations; a constant comfortable 20°C all year.'),
           row('advantage-2', 'Advantage 2', 5, 'A second, different advantage. Such as: far cheaper to run; a much smaller carbon footprint and less CO₂.'),
           row('disadvantage-1', 'Disadvantage 1', 5, 'Such as: a very high standard of workmanship needed from every member of the team.'),
           row('disadvantage-2', 'Disadvantage 2', 5, 'A second, different disadvantage. Such as: tradespersons and designers need training; precise detailing may take longer; reliance on a mechanical system.')],
          ['cons-6-3', 'cons-6-2'], ['passive-design', 'heat-loss-insulation'], 'q10-passive', 'Running costs (6.3) of a highly insulated house (6.2).', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-principles', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p34 (printed 31): discussion of the statement, three points × (4 + 6) = 30; three guidelines × (4 + 6) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately, so each is its own task and the complete card composes them.'
TAA = 'Discuss the above statement in detail.'
TAB = 'Propose three guidelines that would promote the development of environmentally sustainable housing in Ireland.'
TALL = 'Discuss the above statement in detail and propose three guidelines that would promote the development of environmentally sustainable housing in Ireland.'
HOUSING = (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'])
AA = add('10', 'discussion', ' — discussion', TAA,
         [row(f'point-{i}', f'Discussion – point {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: a sustainable ethos puts the environment at the heart of every design decision — doing more with less for longer, thinking globally and acting locally, with best practice the only acceptable standard.'),
             (2, 'Point 4 and discussion 6. Such as: a whole-systems team approach at the design stage, with low embodied energy, renewable materials and life-cycle costing, and each building considered within its neighbourhood.'),
             (3, 'Point 4 and discussion 6. Such as: buildings as the community’s principal asset — durable, beautiful and flexible; low initial cost brings higher lifetime costs. Three distinct, well-argued points are needed.')]],
         *HOUSING, None, 'Sustainable housing in the built environment (1.2, 1.3).', BALT, SALT, alt=True)
AB = add('10', 'guidelines', ' — guidelines', TAB,
         [row('guideline-1', 'Guideline 1 (4 for point, 6 for discussion)', 10, 'Point 4 and discussion 6. Such as: universal design and flexible, lifetime housing as the norm; sustainability a condition of planning.'),
          row('guideline-2', 'Guideline 2 (4 for point, 6 for discussion)', 10, 'Point 4 and discussion 6. Such as: urban renewal on sustainable principles; higher densities with cycle and walking routes; consultation with local communities.'),
          row('guideline-3', 'Guideline 2 (4 for point, 6 for discussion)', 10, 'The third guideline: point 4 and discussion 6 (the scheme prints this row as a second "Guideline 2"). Such as: renewable energy on site and A-rated appliances; grants and incentives for sustainable design; eco-villages such as Cloughjordan as models. Three distinct guidelines are needed.')],
         *HOUSING, None, 'Sustainable housing in the built environment (1.2, 1.3).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, TALL, labels=['Discussion of the statement', 'Three guidelines'], alt=True)

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and four other questions (300 marks); all question banks retained, no full-exam Cartesian cards.'),
          (5, 'one of', 'Q9 stem "one of the most challenging aspects": not a candidate choice.'),
          (5, 'Select', 'Q9(b) closed choose-three of the four circled locations: one card with an any-three group (choice is not a route).'),
          (5, 'any three', 'Q9(b) the same any-three group.'),
          (5, 'any two', 'Q10(a) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
          (5, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.')]
FINITE = {'9b': dict(choose=3, options=[h for h, _ in LOCATIONS9], cardId=B9b['id'], groupRowId='locations'),
          '10a': dict(choose=2, options=[h for h, _ in ITEMS10], cardId=A10['id'], groupRowId='items')}
D.finish(LEDGER, FINITE, {})
