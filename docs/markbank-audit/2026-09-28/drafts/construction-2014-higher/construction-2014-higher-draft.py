"""Draft the 2014 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 32-42; the English scheme carries Irish running headers). This paper was never carded: every
task is added. Q4(b) "select any two of the above areas", Q9(a) and Q10(a) "any two of the following"
are ONE card each with an any-two group over the three printed items (choice is not a route).
Question 5 is printed "5" without a full stop; the census is repaired from the page
(construction_census_repairs.py) so its three parts are not read as Q4. Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Trussed rafter roof on a timber frame wall', concept='trussed-roof-timber-frame-section',
              stem='The sketch shows portion of the roof and external wall of a single-storey dwelling house. The house has an internal span of 6.0 metres. The external wall is of timber frame construction, with a rendered concrete block outer leaf, a 200 mm timber frame inner leaf and a 60 mm insulated service cavity. The roof, which is slated, has prefabricated trussed rafters and is pitched at 30 degrees.',
              note='Original sketch and specification retained. Construction, dimension and scale/drafting marks belong to part (a); the airtightness detail in (b) is marked separately.'),
    '2': dict(page=2, title='An accessible main entrance', concept='accessible-entrance',
              stem='The sketch shows the main entrance to a dwelling house. It has been decided to upgrade this entrance to ensure that everybody can enter the house without special assistance. The following is to be provided at the main entrance: threshold and access ramp; weather protection; suitable lighting.',
              note='Original sketch retained. All three printed provisions in (a) are required, each separately marked.'),
    '3': dict(page=2, title='Converting a storeroom to a study', concept='storeroom-study',
              stem='The drawing shows the elevation, the ground floor plan and portion of the rear garden of a two-storey semi-detached house with an adjoining flat roofed storeroom. The storeroom wall A-A is south facing. The external walls are 350 mm concrete block walls with a full-fill insulated cavity. Planning permission is being sought to convert the storeroom to an attractive space suitable for use as a study.',
              note='Original elevation and plan retained. The requirements, layout and external design are open responses; the scheme gives model designs.'),
    '4': dict(page=3, title='Step-by-step refurbishment of a vernacular house', concept='vernacular-refurbishment',
              stem='A house in the vernacular tradition, as shown in the sketch, was built over 100 years ago without insulation and is now in need of significant refurbishment. The occupants have decided to refurbish the house on a step-by-step basis over a number of years.',
              note='Original sketch retained. Part (b) is a closed choice of any two of the three printed areas: one card holding all three, with the printed character and reuse rows.'),
    '5': dict(page=3, title='Insulated ground floor U-value, heat-loss cost and cold bridge', concept='insulated-ground-floor-u-value', stem='',
              note='All printed data are retained in the original question. Part (b) uses the U-value from (a); the scheme’s worked answers are U = 0.1298 W/m²K and an annual cost of €49.59.'),
    '6': dict(page=4, title='A low environmental impact house', concept='low-impact-house',
              stem='The elevation and the ground floor plan of a house are shown. The house has three bedrooms and a bathroom upstairs. The external walls are of timber frame construction with a rendered concrete block outer leaf. The house is designed to have low environmental impact.',
              note='Original elevation and plan retained. Features are open responses; the scheme lists typical examples.'),
    '7': dict(page=4, title='Triple-glazed casement window section', concept='casement-window-section',
              stem='The sketch shows a wooden casement window fitted in the external wall of a dwelling house. The window, which is 800 mm in height, is a triple glazed, high performance window with a thermally broken insulated frame. The external wall is a 400 mm concrete block wall with a 200 mm full-fill insulated cavity. The wall has an external render and an internal hardwall plaster skim finish.',
              note='Original sketch and specification retained. Construction, dimension and scale/drafting marks belong to part (a); the head and cill details in (b) are each marked.'),
    '8': dict(page=4, title='An en suite bathroom in a bedroom', concept='ensuite-bathroom',
              stem='It is proposed to redesign the existing bedroom shown in the drawing to accommodate a small en-suite bathroom. The bedroom is located on the first floor of the dwelling house.',
              note='Original plan retained. All five printed items in (a) and all three fittings in (b) are required.'),
    '9': dict(page=5, title='Acoustic principles and a sound-insulated bedroom', concept='bedroom-sound-insulation', stem='',
              note='Original sketch retained. Part (a) is a closed choice of any two of the three printed principles: one card holding all three.'),
    '10': dict(page=5, title='Passive House design, orientation and overheating', concept='passive-house-orientation', stem='',
               note='Original sketch retained. Part (a) is a closed choice of any two of the three printed items: one card holding all three.'),
}
ALT = dict(page=5, title='Resilient and sustainable neighbourhoods (alternative Question 10)', concept='sustainable-neighbourhoods',
           stem='“Our common ground starts with the planet. As a species we have never been more vulnerable than we are today. The world is under stress and we are the cause of it. We are now at a tipping point and, as with all periods of great change, there is great opportunity. The world needs the way architects think, we should not keep ourselves aloof from the urgent situation we are in. The most resilient and sustainable form of human habitation is the town or the neighbourhood. We must build to create neighbourhoods. We must plan and design to avoid isolation and disconnection. We must design for what matters, which is ultimately happiness.” Adapted from: PRESIDENT’S INTRODUCTION - Michelle Fagan, President RIAI IRISH ARCHITECTURE, Vol. 3, 2012 / 2013. RIAI, 8 Merrion Square, Dublin 2. ISBN: 978-0-9567493-2-1',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately.')
SCHEME_PAGES = {'1': [4, 5, 32], '2': [5, 6, 33], '3': [6, 7, 8, 34], '4': [8, 9, 10, 11, 12, 13, 35], '5': [14, 36], '6': [15, 16, 17, 18, 37],
                '7': [19, 38], '8': [20, 21, 39], '9': [22, 23, 40], '10': [24, 25, 26, 27, 41], '10-alt': [28, 29, 42]}
D = cp.Draft(HERE, 2014, 'higher', ('fa69de01573c5b7504ed8b2cc76ae930be5d815c85febcb1a7c2e7d03d68e2d1',
                                    '9673985bd87e5867668828d4f03244185b7cb75d0dbe70fa4f55ad819214608c'), 0, QUESTIONS, SCHEME_PAGES, alt=ALT)
row, add, compose, parts, anyn = D.row, D.add, D.compose, D.parts, D.anyn
D.figures({
    'q1-original': D.paper(2, [30, 45, 580, 275]), 'q2-original': D.paper(2, [30, 277, 580, 505]),
    'q3-original': D.paper(2, [30, 505, 580, 790]), 'q4-original': D.paper(3, [30, 45, 580, 318]),
    'q5-original': D.paper(3, [30, 318, 580, 790]), 'q6-original': D.paper(4, [30, 45, 580, 310]),
    'q7-original': D.paper(4, [30, 310, 580, 545]), 'q8-original': D.paper(4, [30, 545, 580, 790]),
    'q9-original': D.paper(5, [30, 45, 580, 360]), 'q10-original': D.paper(5, [30, 360, 580, 575]),
    'q10-alt-original': D.paper(5, [30, 595, 580, 790]),
    'q1-section': D.composite((4, [45, 50, 575, 800]), (5, [45, 50, 575, 462])),
    'q2-entrance': D.composite((5, [45, 462, 575, 795]), (6, [45, 50, 575, 222]), (6, [320, 222, 575, 298])),
    'q2-reasons': D.composite((6, [45, 222, 320, 307]), (6, [45, 307, 575, 405])),
    'q3-requirements': D.scheme(6, [45, 405, 575, 800]), 'q3-layout': D.scheme(7, [45, 50, 575, 805]), 'q3-external': D.scheme(8, [45, 50, 575, 478]),
    'q4-step': D.scheme(8, [45, 478, 575, 800]),
    'q4-upgrades': D.composite((9, [45, 50, 575, 800]), (10, [45, 50, 575, 800]), (11, [45, 50, 575, 800]), (12, [45, 50, 575, 800]), (13, [45, 50, 575, 790])),
    'q5-calculation': D.scheme(14, [45, 60, 575, 576]), 'q5-cold-bridge': D.scheme(14, [45, 576, 575, 800]),
    'q6-features': D.composite((15, [45, 50, 575, 800]), (16, [45, 50, 575, 535])),
    'q6-other': D.composite((16, [45, 535, 575, 800]), (17, [45, 50, 575, 560]), (18, [45, 50, 575, 612])),
    'q6-importance': D.scheme(18, [45, 612, 575, 790]),
    'q7-section': D.scheme(19, [45, 50, 575, 790]),
    'q8-layout': D.scheme(20, [45, 50, 575, 790]),
    'q8-pipework': D.composite((21, [45, 50, 575, 330]), (21, [345, 330, 575, 450])),
    'q8-water': D.composite((21, [45, 330, 345, 470]), (21, [45, 470, 575, 795])),
    'q9-principles': D.composite((22, [45, 50, 575, 563]), (22, [45, 563, 360, 598])),
    'q9-upgrades': D.composite((22, [360, 563, 575, 598]), (22, [45, 598, 575, 790]), (23, [45, 50, 575, 334])),
    'q9-insulating': D.scheme(23, [45, 334, 575, 790]),
    'q10-principles': D.composite((24, [45, 50, 575, 800]), (25, [45, 50, 575, 790])),
    'q10-orientation': D.scheme(26, [45, 50, 575, 286]),
    'q10-overheating': D.composite((26, [45, 286, 575, 810]), (27, [45, 50, 575, 800])),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p32 (printed 29): (a) best ten points × 4 (drawing 3, annotation 1) = 40, scale and drafting 8, three dimensions 3, three courses of slate 3, ventilation path 3 = 57; (b) airtightness detail 3. Complete 60.'
S1 = 'One required section and one required airtightness detail. The detail lists are marking menus, not printed choices.'
T1A = 'To a scale of 1:10, draw a vertical section through one external wall and one rafter length. Show the typical construction details from 400 mm below the ceiling joists, through the external wall and eaves, up to ridge level. Include the ventilation path to the roof and show three courses of slate at eaves. Include three typical dimensions of the roof structure.'
T1B = 'Indicate clearly the design detailing to ensure airtightness at the junction of the ceiling and the external wall.'
A1 = add('1', 'a', '(a)', T1A,
         [row('details', 'Any 10 points × 4 marks', 40, 'Best ten points, 4 each (drawing 3, annotation 1). Wall: double headplate 200 × 50; studs 200 × 50 at 400 mm centres; 60 mm insulated service cavity; sealed vapour barrier; plasterboard and skim; airtight tape at the wall–ceiling junction; 200 mm insulation; 12–20 mm OSB or plywood racking; taped breather membrane; 50–100 mm vapour diffusion cavity; stainless ties; cavity closer; block outer leaf; render. Roof: 50 × 40 battens; breather membrane; trusses at 400–600 mm centres; struts with nail plates; 300–600 mm ceiling insulation; plasterboard with vapour barrier; fascia, soffit and gutter.', list(range(0, 41, 4))),
          row('presentation', 'Scale and Drafting', 8, 'Scale and drafting of the section.'),
          row('dimensions', 'Three typical dimensions of roof structure', 3, 'Three typical dimensions of the roof structure, 1 each.'),
          row('slates', 'Three courses of slate at eaves', 3, 'Three courses of slate shown at the eaves.'),
          row('ventilation', 'Ventilation path at eaves', 3, 'The ventilation path at the eaves, such as a continuous soffit vent and counter battens.')],
         ['cons-1-5', 'cons-3-8', 'cons-3-9', 'cons-3-10', 'cons-3-3'], ['question-1-drawing-questions', 'roofs', 'walls'], 'q1-section',
         'Scaled drawing (1.5) of a trussed rafter roof (3.8) with its covering (3.9) at the eaves (3.10) on a timber frame wall (3.3).', B1, S1)
B1b = add('1', 'b', '(b)', T1B,
          [row('airtightness', 'Design detail to ensure airtightness', 3, 'Show the airtightness detail at the ceiling–wall junction, such as the vapour barriers of wall and ceiling taped together, or scrim and tape at the junction.')],
          ['cons-6-5', 'cons-3-10'], ['condensation-air-tightness', 'roofs'], 'q1-section', 'Airtightness (6.5) at the eaves junction (3.10).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p33 (printed 30): (a) three printed provisions × (note and justification 7 + sketch 7) = 42 and any three dimensions 6 = 48; (b) two reasons × (3 + 3) = 12. Complete 60.'
S2 = 'All three printed provisions in (a) are required, each separately marked; not a choice.'
ACCESS = (['cons-1-2', 'cons-3-7'], ['planning-sustainability-environment', 'doors'])
T2A = 'For each of the above, using notes and freehand sketches, show appropriate design detailing to ensure that the house is accessible to all. Justify your design choices and include dimensions as appropriate.'
T2B = 'Discuss in detail two reasons why provision for lifetime use should be considered at the design stage of a dwelling.'
A2 = add('2', 'a', '(a)', T2A,
         [row('threshold', 'Threshold and access ramp', 14, 'Note and justification 7, sketch 7. Such as: a level threshold no higher than 15 mm; an 1800 × 1800 mm level area at the door; a 1:20 ramp at least 1200 mm wide with raised kerbs and a slip-resistant surface; a door with 800–1000 mm clear opening and lever handles.'),
          row('weather', 'Weather protection', 14, 'Note and justification 7, sketch 7. Such as: a canopy over the door extending at least 1800 mm, securely braced against high winds.'),
          row('lighting', 'Suitable lighting', 14, 'Note and justification 7, sketch 7. Such as: low and high level lighting; lights inset to the ramp and landing; low-voltage, sensor-activated lighting.'),
          row('dimensions', 'Dimensions (any three)', 6, 'Any three appropriate dimensions, 2 each.')],
         *ACCESS, 'q2-entrance', 'Accessible design (1.2) of an entrance door (3.7).', B2, S2)
B2b = add('2', 'b', '(b)', T2B,
          [row(f'reason-{i}', f'Reason {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
              (1, 'Point 3 and discussion 3. Such as: decisions made before construction need little modification afterwards; later modifications mean demolition and costly retrofit.'),
              (2, 'A second, different reason. Such as: a flexible layout with movable partitions and services planned from the outset; lintels fitted where openings may be needed later.')]],
          ['cons-1-2'], ['planning-sustainability-environment'], 'q2-reasons', 'Lifetime design of the built environment (1.2).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b], 'q2-entrance', B2, S2, parts(('a', T2A), ('b', T2B)))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p34 (printed 31): (a) three requirements × (3 + 3) = 18; (b) three requirements in the layout × (note 5 + sketch 5) = 30; (c) external design notes and sketches 12. Complete 60.'
S3 = 'The requirements, layout and external design are open responses with no printed list.'
STUDY = (['cons-1-2'], ['planning-sustainability-environment'])
T3A = 'Discuss in detail three functional requirements of a space suitable for use as a study.'
T3B = 'Using notes and freehand sketches, show a proposed design layout for the study incorporating each functional requirement you have specified.'
T3C = 'Using notes and freehand sketches, show a revised external design for the study that will enhance its visual appearance.'
A3 = add('3', 'a', '(a)', T3A,
         [row(f'requirement-{i}', f'Functional requirement {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: thermal comfort — easily heated, ventilated, no extremes; acoustic comfort — a quiet space for solitude.'),
             (2, 'A second, different requirement. Such as: visual comfort — daylight, task lighting and views to the garden; ergonomic comfort — adjustable desk and chair.'),
             (3, 'A third, different requirement. Such as: olfactory comfort — fresh air and plants; a multi-functional, agile space that can become a bedroom.')]],
         *STUDY, 'q3-requirements', 'Layout design of the built environment (1.2).', B3, S3)
B3b = add('3', 'b', '(b)', T3B,
          [row(f'requirement-{i}', f'Functional requirement {i}', 10, note) for i, note in [
              (1, 'Note 5 and sketch 5, showing the first requirement in the layout. Such as: a light-drenched space with large south glazing, roof lights and brise-soleil.'),
              (2, 'Note 5 and sketch 5, the second requirement. Such as: a sound-insulated wall and well-sealed glazed door to the kitchen.'),
              (3, 'Note 5 and sketch 5, the third requirement. Such as: sliding or bi-fold doors to a patio bringing the garden in; a movable desk and fold-away bed.')]],
          ['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'], 'q3-layout', 'Layout design (1.2) with good daylighting (7.4).', B3, S3)
C3 = add('3', 'c', '(c)', T3C,
         [row('design', 'Notes and sketches', 12, 'Notes 6 and sketches 6. Such as: blending with or contrasting with the house; a flat or sloping roof with roof lights; full-height glazing; an integral part of the house, not a garage.')],
         *STUDY, 'q3-external', 'External design in the built environment (1.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-layout', B3, S3, parts(('a', T3A), ('b', T3B), ('c', T3C)))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p35 (printed 32): (a) two advantages and two disadvantages × (3 + 3) = 24; (b) any two of three printed areas × (note 6 + sketch 6) = 24, character of the original house 6, reuse of materials 6 = 36. Complete 60.'
S4 = 'Choice is not a route: part (b) (select any two of the three printed areas) is ONE card with an any-two group over the scheme headings, plus the printed character and reuse rows; its figure carries all three areas’ scheme drawings.'
T4A = 'Discuss two advantages and two disadvantages of adopting a step-by-step approach to the refurbishment of the house.'
T4B = 'A survey of the house reveals: external random rubble stone walls, 450 mm in thickness, with an internal and external lime render; traditional cut roof with natural slates; suspended timber ground floor. Select any two of the above areas and, using notes and freehand sketches, describe the steps involved in upgrading each area selected. Show how the refurbishment should be carried out in a manner that respects the character of the original house and ensures the reuse of materials.'
A4 = add('4', 'a', '(a)', T4A,
         [row('advantage-1', 'Advantage 1 (point 3 marks, discussion 3 marks)', 6, 'Such as: phased upgrading as finance allows, without a large loan; time for research between stages.'),
          row('advantage-2', 'Advantage 2 (point 3 marks, discussion 3 marks)', 6, 'A second, different advantage. Such as: energy bills fall as the upgrade progresses; the occupants live in the house throughout.'),
          row('disadvantage-1', 'Disadvantage 1 (point 3 marks, discussion 3 marks)', 6, 'Such as: disruption over a long period; hard to keep momentum while living in the house.'),
          row('disadvantage-2', 'Disadvantage 2 (point 3 marks, discussion 3 marks)', 6, 'A second, different disadvantage. Such as: high bills until complete; best practice harder to apply in phases; rooms unusable for periods.')],
         ['cons-1-1', 'cons-1-2'], ['conservation-restoration'], 'q4-step', 'Refurbishing a vernacular building (1.1) in the built environment (1.2).', B4, S4)
AREAS = [('External random rubble wall', 'keep the wall breathable with no vapour barriers; hempcrete, wood fibre boards or lime plasters inside or out; a French drain against rising damp; layers progressively more permeable towards the outside.'),
         ('Traditional cut roof', 'minimal intervention: slates numbered, stored and reused; impermeable felt replaced with a vapour-diffuse membrane; only decayed parts of rafters spliced or replaced in the same timber; hygroscopic insulation such as sheep’s wool and wood fibre board; counter battens for ventilation.'),
         ('Suspended timber ground floor', 'floorboards numbered and lifted; sub-floor ventilation checked; decayed joists or boards replaced; insulation between the joists on netting or battens with a breather membrane; boards and skirting relaid as labelled.')]
A4b = add('4', 'b', '(b)', T4B,
          [anyn('areas', 'Survey of house any 2 areas', 2, 12, AREAS, 'Any two of the three printed areas, each note 6 and sketch 6 = 12.'),
           row('character', 'Character of the original house', 6, 'The refurbishment respects the character of the original house, such as matching materials, profiles and the original roof plane.'),
           row('reuse', 'Reuse of materials', 6, 'Materials reused, such as numbered slates and floorboards relaid and decayed timber replaced only where needed.')],
          ['cons-1-1', 'cons-3-3', 'cons-3-9', 'cons-4-3', 'cons-6-2'], ['conservation-restoration', 'walls', 'roofs', 'floors', 'heat-loss-insulation'], 'q4-upgrades',
          'The union of the three printed areas, upgraded with respect for the original character (1.1): the rubble walls (3.3), the slated roof (3.9) and the suspended timber floor (4.3), with breathable insulation (6.2).', B4, S4)
compose('4', 'complete', ' — complete', [A4, A4b], 'q4-upgrades', B4, S4, parts(('a', T4A), ('b', T4B)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p36 (printed 33): (a) nine points × 3 = 27 (tabulation, the top surface and five layers, total resistance, U-value); (b) five steps × 3 = 15; (c) cold-bridge note 9 + sketch 9 = 18. Complete 60.'
S5 = 'No printed choice. Part (b) uses the U-value from (a).'
DATA5 = ('Concrete floor slab thickness 125 mm; Extruded polystyrene insulation thickness 200 mm; Damp proof membrane (DPM) thickness 0.30 mm; Sand blinding thickness 30 mm; Hardcore thickness 225 mm.\n'
         'Thermal data of floor: Resistance of top surface of floor (R) 0.104 m2 °C/W; Conductivity of concrete (k) 0.160 W/m °C; Conductivity of polystyrene insulation (k) 0.031 W/m °C; '
         'Conductivity of damp proof membrane (DPM) (k) 0.450 W/m °C; Conductivity of sand blinding (k) 0.160 W/m °C; Conductivity of hardcore (k) 1.260 W/m °C.')
T5A = 'Using the following data, calculate the U-value of the insulated concrete ground floor: ' + DATA5
T5B = ('Using the U-value of the concrete ground floor obtained at 5(a) above and the following data, calculate the cost of heat lost annually through the concrete ground floor: '
       'Dimensions of floor 13.0 metres × 7.0 metres; Average internal temperature 21°C; Average external temperature 7°C; Heating period 12 hours per day for 39 weeks per annum; '
       'Cost of oil 95 cent per litre; Calorific value of oil 37350 kJ per litre; 1000 Watts 1 kJ per second.')
T5C = ('A solid concrete ground floor abuts a 350 mm concrete block external wall with an insulated cavity. Using notes and freehand sketches, show best practice design detailing which will prevent '
       'the formation of a cold bridge at the junction of the floor and the wall. Show the typical design detailing from the bottom of the hardcore to the top of the skirting board.')
A5 = add('5', 'a', '(a)', T5A,
         [row('tabulation', 'Correct tabulation', 3, 'The calculation set out in a table of material, conductivity, thickness and resistance.'),
          row('resistances', 'Insulated concrete ground floor (9 points × 3 marks)', 18, 'Six resistances, 3 each, by R = T/k: top surface 0.1040 (given); slab 0.125/0.160 = 0.7813; insulation 0.200/0.031 = 6.4516; DPM 0.00030/0.450 = 0.0006; sand blinding 0.030/0.160 = 0.1875; hardcore 0.225/1.260 = 0.1786. All in m²°C/W.', list(range(0, 19, 3))),
          row('total-resistance', 'Total resistance', 3, 'Total resistance, the sum of R = 7.70 m²°C/W.', [0, 3]),
          row('u-value', 'U-Value (1 mark for formula)', 3, 'U = 1/Rt = 1 ÷ 7.7 = 0.1298 W/m²K (1 mark for the formula).')],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Thermal resistance, conductivity and transmittance (6.1).', B5, S5)
B5b = add('5', 'b', '(b)', T5B,
          [row('heat-loss', 'Heat loss formula and calculation', 3, 'Heat loss = U-value × area × temperature difference = 0.1298 × 91 × 14 = 165.36 watts (joules per second).'),
           row('duration', 'Heating duration for one year', 3, 'Heating period = 12 × 7 × 39 = 3,276 hours = 11,793,600 seconds.'),
           row('energy', 'K/joules calculation for one year', 3, 'Energy = 11,793,600 × 165.36 ÷ 1000 ≈ 1,950,190 kJ per year.'),
           row('oil', 'Litres of oil for one year', 3, 'Oil = 1,950,190 ÷ 37,350 = 52.2 litres per year.'),
           row('cost', 'Annual cost of heat loss', 3, 'Annual cost = 52.2 × €0.95 = €49.59.')],
          ['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Heat loss calculation and running costs (6.3) from the U-value (6.1).', B5, S5)
C5 = add('5', 'c', '(c)', T5C,
         [row('note', 'Note – (to include thermal blocks and vertical insulation)', 9, 'Notes on the detail, including thermal blocks and vertical perimeter insulation linking the floor and cavity insulation.'),
          row('sketch', 'Sketch – (to include thermal blocks and vertical insulation)', 9, 'A sketch from the bottom of the hardcore to the top of the skirting, showing the thermal blocks and vertical insulation, as in the scheme’s model detail.')],
         ['cons-6-2', 'cons-4-2'], ['heat-loss-insulation', 'floors'], 'q5-cold-bridge', 'A thermal bridge (6.2) at the ground floor junction (4.2).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p37 (printed 34): (a) three features × (note 5 + sketch 5) = 30; (b) two other features × (note 5 + sketch 5) = 20; (c) discussion (4 + 6) = 10. Complete 60.'
S6 = 'Features are open responses with no printed list; the scheme lists typical examples.'
T6A = 'With reference to the design shown, discuss in detail, using notes and freehand sketches, three features of the design that contribute to the house having low environmental impact.'
T6B = 'Describe, using notes and freehand sketches, two other design features that could be introduced to further reduce the environmental impact of the house. Justify your choice of design features.'
T6C = 'Discuss the importance of designing low environmental impact housing.'
A6 = add('6', 'a', '(a)', T6A,
         [row(f'feature-{i}', f'Design feature {i}', 10, note) for i, note in [
             (1, 'Note 5 and sketch 5. Such as: a steep roof giving habitable attic space on a compact footprint; roof lights for daylight.'),
             (2, 'A second, different feature. Such as: large south glazing and small north windows; a wood-burning stove on an internal chimney stack.'),
             (3, 'A third, different feature. Such as: the long elevation on an east–west axis; an open, level ground floor; local timber frame with low embodied energy; a modest, one-room-deep plan.')]],
         ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-features',
         'Low-impact design of the built environment (1.2), solar gain (6.4) and insulation (6.2).', B6, S6)
B6b = add('6', 'b', '(b)', T6B,
          [row(f'feature-{i}', f'Design feature {i}', 10, note) for i, note in [
              (1, 'Note 5 and sketch 5, justified. Such as: solar collector panels on the south roof for 40–60% of hot water; photovoltaic panels.'),
              (2, 'A second, different feature, justified. Such as: a winter garden; a porch or draught lobby; internal doors zoning the heating; a wind turbine; rainwater harvesting.')]],
          ['cons-1-2', 'cons-6-4', 'cons-5-8'], ['sustainability-the-environment', 'services-water-gas-electricity'], 'q6-other',
          'Sustainable additions (1.2): solar gain (6.4) and on-site electricity (5.8).', B6, S6)
C6 = add('6', 'c', '(c)', T6C,
         [row('discussion', 'Discussion (4 for point, 6 for discussion)', 10, 'Point 4 and discussion 6. Such as: economical use of finite resources; buildings of human scale leaving resources for future generations; a reduced carbon footprint; less damage to landscapes and habitats.')],
         ['cons-1-2'], ['sustainability-the-environment'], 'q6-importance', 'Sustainable design of the built environment (1.2).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-features', B6, S6, parts(('a', T6A), ('b', T6B), ('c', T6C)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p38 (printed 35): (a) best eight of thirteen details × 5 = 40, three dimensions 3, scale 3 and draughting 6/4/2 = 9: 52; (b) head and cill details × 4 = 8. Complete 60.'
S7 = 'One required section and both printed water details. The detail list is a marking menu, not a printed choice.'
T7A = 'To a scale of 1:5, draw a vertical section through the wall and the centre of the window. The section should show the typical construction details from 300 mm below the window cill, through the fixed frame of the window, to a level 450 mm above the window head. Include three typical dimensions on your drawing.'
T7B = 'Indicate clearly on your drawing the typical design detailing to prevent the ingress of water at both the window head and cill.'
A7 = add('7', 'a', '(a)', T7A,
         [row('details', 'Section through wall and window (8 × 5 marks)', 40, 'Best eight details, 5 each. Menu: external and internal leaf; external and internal plaster; 200 mm full-fill cavity insulation; lintels; stepped DPC; cavity closer; airtightness tape; thermally broken frame (2 at most without the break); triple glazing; window cill; window board; wrap-around DPC; insulation behind the cill.', list(range(0, 41, 5))),
          row('dimensions', '3 typical dimensions', 3, 'Three typical dimensions, 1 each.'),
          row('presentation', 'Scale and drafting', 9, 'Scale 3 and draughting excellent 6, good 4, fair 2.')],
         ['cons-1-5', 'cons-3-6', 'cons-3-3', 'cons-3-4'], ['question-1-drawing-questions', 'windows-light', 'walls'], 'q7-section',
         'Scaled drawing (1.5) of window head and cill details (3.6) in a cavity wall (3.3) with lintels and DPC (3.4).', B7, S7)
B7b = add('7', 'b', '(b)', T7B,
          [row('head', 'Detail at head', 4, 'Show and identify the head detail, such as the stepped DPC and cavity closer over the window.'),
           row('cill', 'Detail at cill', 4, 'Show and identify the cill detail, such as the wrap-around DPC and the cill’s drip and slope.')],
          ['cons-3-6', 'cons-3-4'], ['windows-light', 'walls'], 'q7-section', 'Window head and cill details (3.6) with DPCs (3.4).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p39 (printed 36): (a) sketch 4, preferred location 4 and five items each location 3 + justification 1 = 28; (b) four pipework items × (notes 2 + sketches 2) = 16 and pipe sizes 4 × 1 = 20; (c) two considerations × 6 = 12. Complete 60.'
S8 = 'All five printed items in (a) and all printed fittings in (b) are required; not a choice.'
DRAIN = (['cons-5-6'], ['drainage'])
T8A = 'Draw a freehand sketch of the bedroom shown and indicate a preferred location for the bathroom in the bedroom. Show the location of the following: door, window, shower, wash hand basin and W.C. Justify your design choices.'
T8B = 'Using notes and freehand sketches, show the above-ground pipework necessary for the safe removal of waste from the shower, wash hand basin and W.C. Include on your sketch typical sizes of the soil and vent pipe (svp) and of the waste pipe from each fitting.'
T8C = 'Outline two design considerations to ensure the economical use of water in the bathroom.'
A8 = add('8', 'a', '(a)', T8A,
         [row('sketch', 'Sketch Preferred location', 8, 'The sketch of the bedroom 4 and the preferred location of the en suite 4, as in the scheme’s model plans.'),
          row('items', 'Location (3 marks) Justification (1 mark) Door Window Shower Wash hand basin W.C.', 20, 'Each of the five items located 3 and justified 1. Such as: an outward-opening door avoiding a view of the WC; the window opposite the door for ventilation; the shower on an external wall with an extractor; a corner basin; the WC on an external wall near the stack.')],
         ['cons-5-6', 'cons-1-2'], ['drainage', 'planning-sustainability-environment'], 'q8-layout', 'Sanitary fitments (5.6) in the layout (1.2).', B8, S8)
B8b = add('8', 'b', '(b)', T8B,
          [row('shower', 'Shower', 4, 'Notes 2 and sketch 2. Such as: a 40 mm branch to the 100 mm stack, at most 4.0 m long at 18–90 mm/m, with a deep-seal trap.'),
           row('basin', 'Wash hand basin', 4, 'Notes 2 and sketch 2. Such as: a 32 mm branch, at most 1.7 m long at 18–90 mm/m, with a deep-seal trap.'),
           row('wc', 'WC', 4, 'Notes 2 and sketch 2. Such as: a 100 mm branch, at most 6.0 m for a single WC at 9 mm/m, with a 50 mm seal.'),
           row('svp', 'Soil and Vent pipe', 4, 'Notes 2 and sketch 2. Such as: a 100 mm soil and vent pipe with a 200 mm offset at the WC connection.'),
           row('sizes', 'Typical pipe sizes (4 × 1 marks)', 4, 'Four typical pipe sizes, 1 each.')],
          *DRAIN, 'q8-pipework', 'Sanitary fitments and the single stack system (5.6).', B8, S8)
C8 = add('8', 'c', '(c)', T8C,
         [row('consideration-1', 'Design consideration 1', 6, 'Such as: dual-flush cisterns cutting a 10–14 litre flush to 4–6 litres; rain or grey water to flush toilets; a displacement device in the cistern.'),
          row('consideration-2', 'Design consideration 2', 6, 'A second, different consideration. Such as: aerators, flow restrictors or sensor taps on the basin; an air-jet or pulsating shower head and a flow reducer.')],
         ['cons-5-6', 'cons-5-2'], ['drainage', 'services-water-gas-electricity'], 'q8-water', 'Sanitary fitments (5.6) and water supply (5.2).', B8, S8)
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-pipework', B8, S8, parts(('a', T8A), ('b', T8B), ('c', T8C)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p40 (printed 37): (a) any two of three printed principles × (notes 6 + sketch 6) = 24; (b) floor and partition, each note 4 + sketch 4, materials 4, dimensions 4 = 24; (c) two principles × 6 = 12. Complete 60.'
S9 = 'Choice is not a route: part (a) (any two of three printed principles) is ONE card with an any-two group over the scheme headings; its figure carries all three principles’ drawings.'
SOUND = (['cons-8-3'], ['sound'])
T9A = 'Using notes and freehand sketches explain any two of the following: sound absorption; sound reflection; reverberation time.'
T9B = 'A bedroom is located on the first floor of a house, directly above the kitchen, as shown in the sketch. Music from the bedroom can be heard in the adjoining rooms and in the kitchen beneath. The bedroom has a standard stud partition and a softwood floor on wooden joists, with a plasterboard ceiling beneath. It has been decided to upgrade the existing partition and floor to reduce the transmittance of sound from the bedroom. Using notes and freehand sketches, show a revised design detailing that will reduce the transmittance of sound through the floor and the existing stud partition. Specify the materials to be used and give their typical dimensions.'
T9C = 'Explain the sound insulation principles associated with the design details you have shown.'
ITEMS9 = [('Sound absorption', 'the sound absorbed by surfaces and materials in a room: hard shiny surfaces absorb little and reflect, causing echo; soft carpets, curtains and furnishings absorb sound.'),
          ('Sound reflection', 'the angle of reflection equals the angle of incidence, as with light; used to distribute sound evenly in a room, important in theatres.'),
          ('Reverberation time', 'the time for a sound to decline by 60 dB; it varies with the room’s size and furnishings; reflective surfaces give a longer time than soft ones.')]
A9 = add('9', 'a', '(a)', T9A,
         [anyn('items', 'Acoustic design principles - Explain any 2', 2, 12, ITEMS9, 'Any two of the three printed principles, each notes 6 and sketch 6 = 12.')],
         ['cons-8-1', 'cons-8-2'], ['sound'], 'q9-principles', 'The union of the three printed principles: the nature of sound (8.1), absorption, reflection and reverberation time (8.2).', B9, S9)
B9b = add('9', 'b', '(b)', T9B,
          [row('floor', 'Floor detail', 8, 'Note 4 and sketch 4. Such as: a floating floor on battens not nailed through; acoustic isolation strips; quilt or sand between the joists; acoustic matting; a double-slabbed ceiling with staggered joints.'),
           row('partition', 'Stud partition', 8, 'Note 4 and sketch 4. Such as: staggered studs forming a double partition with quilt woven between; two layers of plasterboard with staggered joints.'),
           row('materials', 'Materials to be used', 4, 'The materials specified, such as absorbent quilt, acoustic matting, isolation strips and plasterboard.'),
           row('dimensions', 'Typical dimensions', 4, 'Typical dimensions of the materials, such as 2 × 12.5 mm plasterboard.')],
          ['cons-8-3', 'cons-4-3', 'cons-4-5'], ['sound', 'floors', 'doors'], 'q9-upgrades',
          'Sound insulation (8.3) of a timber upper floor (4.3) and stud partition (4.5).', B9, S9)
C9 = add('9', 'c', '(c)', T9C,
         [row('principle-1', 'Sound insulating principle 1', 6, 'Such as: isolation — separating surfaces so voids break the sound path; mass — denser materials insulate better.'),
          row('principle-2', 'Sound insulating principle 2', 6, 'A second, different principle. Such as: flexibility — quilt and resilient layers absorb sound; completeness — no small gaps.')],
         *SOUND, 'q9-insulating', 'Airborne and impact sound insulation (8.3).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-upgrades', B9, S9, parts(('a', T9A), ('b', T9B), ('c', T9C)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p41 (printed 38): (a) any two of three printed items × (note 5 + sketch 5) = 20; (b) orientation notes 7 + sketches 7 and sun path 6 = 20; (c) two reasons × 4 and two design details × (notes 3 + sketches 3) = 20. Complete 60.'
S10 = 'Choice is not a route: part (a) (any two of three printed items) is ONE card with an any-two group over the scheme headings; its figure and the complete-question figure carry all three items’ drawings. The OR alternative is a separate Question 10 route.'
PASSIVE = (['cons-6-4', 'cons-6-5'], ['passive-design'])
T10A = 'Using notes and freehand sketches, discuss in detail the importance of any two of the following in the design of a Passive House: building form; indoor air quality; foundation design.'
T10B = 'Using notes and freehand sketches, discuss the importance of orientation in the siting of a Passive House. Show the sun path in your sketch.'
T10C = 'A Passive House, as shown in the sketch, may overheat in summer. Discuss two reasons why overheating occurs and, using notes and freehand sketches, show two design details that would reduce the possibility of overheating.'
ITEMS10 = [('Building form', 'a simple, compact form with a surface-to-volume ratio of 0.7 or less: less material, easier to heat and make airtight; complex forms add wall area, cold bridges and wind chill.'),
           ('Indoor air quality', 'build tight and ventilate right: MHRV supplying filtered fresh air and extracting moist air from wet rooms; at most 0.6 air changes per hour; humidity 30–60%; CO₂ below 1000 ppm.'),
           ('Foundation Design', 'an insulated foundation to cut heat loss to the soil: high-density extruded polystyrene on blinded, compacted hardcore; a mesh-reinforced slab; a radon barrier.')]
A10 = add('10', 'a', '(a)', T10A,
          [anyn('items', 'Design of a passive house - any 2', 2, 10, ITEMS10, 'Any two of the three printed items, each note 5 and sketch 5 = 10.')],
          ['cons-6-2', 'cons-6-5', 'cons-2-4'], ['passive-design', 'foundations'], 'q10-principles',
          'The union of the three printed items: building form and heat loss (6.2), indoor air quality (6.5) and the insulated foundation (2.4).', B10, S10)
B10b = add('10', 'b', '(b)', T10B,
           [row('notes', 'Notes', 7, 'Such as: the glazed façade facing south, within 30° of the east–west axis; one room deep with no rooms on the sunless north; spacing to avoid overshadowing.'),
            row('sketches', 'Sketches', 7, 'Sketches of the orientation, as in the scheme’s model.'),
            row('sun-path', 'Sun path', 6, 'The sun path shown on the sketch.')],
           ['cons-6-4'], ['passive-design'], 'q10-orientation', 'Solar heat gain and orientation (6.4).', B10, S10)
C10 = add('10', 'c', '(c)', T10C,
          [row('reason-1', 'Reason 1 for overheating', 4, 'Such as: no overhang, balcony or brise-soleil shading the windows; too much south glazing.'),
           row('reason-2', 'Reason 2 for overheating', 4, 'A second, different reason. Such as: insufficient ventilation; little thermal mass; heat from lighting, appliances and cooking.'),
           row('detail-1', 'Design Detail 1', 6, 'Notes 3 and sketches 3. Such as: thermal mass in concrete floors and block walls absorbing solar gain; an extended roof overhang sized from the summer and winter sun angles.'),
           row('detail-2', 'Design Detail 2', 6, 'A second, different detail: notes 3 and sketches 3. Such as: adjustable brise-soleil; dynamic glass; external blinds and shutters.')],
          *PASSIVE, 'q10-overheating', 'Solar heat gain (6.4) and ventilation (6.5).', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-principles', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p42 (printed 39): discussion of the statement, three points × (4 + 6) = 30; three guidelines × (4 + 6) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately, so each is its own task and the complete card composes them.'
TAA = 'Discuss the above statement in detail.'
TAB = 'Propose three planning guidelines that would promote the development of resilient and sustainable neighbourhoods in Ireland.'
TALL = 'Discuss the above statement in detail and propose three planning guidelines that would promote the development of resilient and sustainable neighbourhoods in Ireland.'
NEIGH = (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'])
AA = add('10', 'discussion', ' — discussion', TAA,
         [row(f'point-{i}', f'Discussion – point {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: the planet is under stress — climate change, flooding, diminishing fossil fuels and rising CO₂ at a tipping point.'),
             (2, 'Point 4 and discussion 6. Such as: architects leading a new paradigm of deep-green, nearly zero energy, beautiful homes rather than staying aloof.'),
             (3, 'Point 4 and discussion 6. Such as: towns and neighbourhoods as the most resilient habitation — living near work and leisure, avoiding isolated, energy-hungry one-off houses. Three distinct, well-argued points are needed.')]],
         *NEIGH, None, 'Planning a sustainable built environment (1.2, 1.3).', BALT, SALT, alt=True)
AB = add('10', 'guidelines', ' — guidelines', TAB,
         [row(f'guideline-{i}', f'Guideline {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: universal design and flexible, lifetime housing of mixed sizes as the norm.'),
             (2, 'Point 4 and discussion 6. Such as: higher urban densities with cycle lanes, walking routes and green, car-free spaces; urban renewal on sustainable principles.'),
             (3, 'Point 4 and discussion 6. Such as: deep-green planning guidelines and incentives for sustainable design; high-quality public spaces; eco-villages as exemplars. Three distinct guidelines are needed.')]],
         *NEIGH, None, 'Planning a sustainable built environment (1.2, 1.3).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, TALL, labels=['Discussion of the statement', 'Three planning guidelines'], alt=True)

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and any four of the other nine (300 marks); all question banks retained, no full-exam Cartesian cards.'),
          (3, 'Select', 'Q4(b) closed choose-two of three printed areas: one card with an any-two group (choice is not a route).'),
          (3, 'any two', 'Q4(b) closed choose-two of three printed areas: the same any-two group.'),
          (5, 'any two', 'Q9(a) closed choose-two of three printed principles: one card with an any-two group (choice is not a route).'),
          (5, 'any two', 'Q10(a) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
          (5, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.'),
          (5, 'or', 'Alternative Question 10 quotation ("the town or the neighbourhood"): not a candidate choice.')]
FINITE = {'4b': dict(choose=2, options=[h for h, _ in AREAS], cardId=A4b['id'], groupRowId='areas'),
          '9a': dict(choose=2, options=[h for h, _ in ITEMS9], cardId=A9['id'], groupRowId='items'),
          '10a': dict(choose=2, options=[h for h, _ in ITEMS10], cardId=A10['id'], groupRowId='items')}
D.finish(LEDGER, FINITE, {})
