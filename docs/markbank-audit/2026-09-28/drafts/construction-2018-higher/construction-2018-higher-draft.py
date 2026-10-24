"""Draft the 2018 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 28-38; the English-version scheme carries Irish running headers). Q10(a) "any two of the
following" is ONE card with an any-two group over the three printed items (choice is not a route);
Q4(b) "site A or site B" is one task marked alike for either site. The 27 pre-audit 2018 Higher cards
keep their IDs and concept IDs and are corrected in place. Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Timber-clad porch with a lean-to slated roof', concept='porch-lean-to-section',
              stem='A front porch projects 1.2 metres from the external wall of a dwelling house, as shown. The insulated wall of the porch is of timber frame construction with a rainscreen of vertical cedar cladding. The studwork is 250 mm × 50 mm. The external wall of the house is a 400 mm rendered concrete block wall with a full-fill insulated cavity. The lean-to roof of the porch is an insulated slated roof and has a pitch of 30°. Insulated plasterboard is also fixed to the underside of the sloping rafters.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the abutment detail in (b) is marked separately.'),
    '2': dict(page=2, title='Site risks, guidelines and safety culture', concept='site-risks-safety-culture', stem='',
              note='Original sketch retained. All three printed tasks in (a) and (b) are required, each separately marked.'),
    '3': dict(page=3, title='Extending a terraced cottage for health and wellbeing', concept='cottage-wellbeing-extension',
              stem='The drawing shows the ground floor plan and the front elevation of a terraced cottage. Also shown is a portion of the rear garden. The walls of the cottage are of random rubble construction and are rendered. The rear wall A-A is south facing. To provide additional living space, and to enhance the health and wellbeing of the occupants, it has been decided to build a single-storey extension, not greater than 18.0 m2 in area, to the rear of the cottage.',
              note='Original plan and elevation retained. Considerations and the layout are open responses; the scheme gives model layouts.'),
    '4': dict(page=3, title='Choosing a rural site and siting the house', concept='rural-site-selection', stem='',
              note='Original site location map retained. Both printed characteristics in (a) are required; in (b) either site may be chosen and is marked alike.'),
    '5': dict(page=4, title='Ground floor U-value, heat-loss cost and insulation thickness', concept='ground-floor-u-value',
              stem='A house built in the 1970s has an uninsulated solid concrete ground floor, as shown, with a sand/cement fine screed finish.',
              note='All printed data are retained in the original question. Parts (b) and (c) use the U-value from (a); the scheme’s worked answers are U = 1.2434 W/m²°C, an annual cost of €352.50 and 216.9 mm of expanded polystyrene.'),
    '6': dict(page=5, title='A self-build eco-friendly timber house', concept='self-build-eco-house',
              stem='A young couple have obtained planning permission to build an eco-friendly house, with internal dimensions of 10.0 m × 4.0 m, as shown. There are two bedrooms and a bathroom upstairs. The couple have an interest in house construction and wish to self-build their house with the help of neighbours, family and friends. They have also engaged professional design supervision and an electrician. The house is of timber frame construction throughout, with an external rainscreen of native larch.',
              note='Original elevation and plan retained. Part (a) requires both two advantages and two disadvantages, each separately marked.'),
    '7': dict(page=5, title='Entrance door, cavity wall and first floor section', concept='door-wall-floor-section',
              stem='The main entrance door to a two-storey dwelling house is a high performance insulated wooden door, with vertical sheeting on both sides. The doorframe is thermally broken and is fitted in a 450 mm external concrete block wall with a full-fill insulated cavity. This external wall supports the first floor joists, as shown in the accompanying outline drawing. The first floor is a 25 mm floating wooden floor, on a 20 mm plywood deck, on 200 mm × 40 mm wooden joists, with a plasterboard ceiling beneath.',
              note='Original outline drawing retained. Construction and scale/drafting marks belong to part (a); the airtightness detail in (b) is marked separately.'),
    '8': dict(page=6, title='Stove and solar collector heating and hot water', concept='stove-solar-heating-system',
              stem='A wood-burning stove as shown, combined with a solar collector, is used to provide central heating and hot water for a compact three bedroom, two-storey house.',
              note='Original sketch retained. The listed components are a marking menu; both safety features and both chimney considerations are required.'),
    '9': dict(page=6, title='Attic bedroom in a cut roof', concept='attic-bedroom-roof', stem='',
              note='Original sketch retained. The requirements are open responses; (b) requires the roof, the stud side walls and insulation, and labelled dimensions.'),
    '10': dict(page=7, title='Passive House principles, modifications and orientation', concept='passive-house-upgrade', stem='',
               note='Original elevation and plan retained. Part (a) is a closed choice of any two of the three printed items: one card holding all three.'),
}
ALT = dict(page=7, title='Building modestly and sourcing locally (alternative Question 10)', concept='green-sustainable-housing',
           stem='Green design is about being green, rather than simply appearing to be green. So greening your house is about more than just buying all sorts of expensive ‘eco-bling’ and adding it to your house. Ironically, that could be just another display of consumerism. Rather, greening your house is about making responsible environmental choices based on what you want to do, what you can do and what you can afford. This means that - before we get into the minutiae of sustainable building materials - we should address some fundamentals, chief among which is the need to build modestly and source locally. From: contemporary design secrets: the art of building a house in the countryside Jane Burnside (2013) Published by: BOOKLINK. ISBN 978-1-906886-42-4',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately.')
SCHEME_PAGES = {'1': [4, 5, 28], '2': [5, 6, 7, 8, 29], '3': [8, 9, 10, 30], '4': [10, 11, 12, 31], '5': [13, 14, 32], '6': [14, 15, 16, 33],
                '7': [17, 34], '8': [18, 19, 35], '9': [19, 20, 21, 36], '10': [21, 22, 23, 24, 37], '10-alt': [24, 25, 26, 38]}
D = cp.Draft(HERE, 2018, 'higher', ('c719ee9d731d6897511c1f159d266a6a1323190112f29d9c12083b8c63685725',
                                    'e511515f52851ffc803fd68b5f7e7b87709fc0523acf0149c684282bbd9f72a1'), 27, QUESTIONS, SCHEME_PAGES, alt=ALT)
row, add, compose, parts, anyn = D.row, D.add, D.compose, D.parts, D.anyn
PRES = [0, 2, 3, 4, 5, 6, 7, 8]  # scale 4/3/2 + drafting 4/3/2, each printed separately
D.figures({
    'q1-original': D.paper(2, [30, 53, 580, 395]), 'q2-original': D.paper(2, [30, 510, 580, 730]),
    'q3-original': D.paper(3, [30, 65, 580, 415]), 'q4-original': D.paper(3, [30, 460, 580, 790]),
    'q5-original': D.paper(4, [30, 39, 580, 700]), 'q6-original': D.paper(5, [30, 39, 580, 495]),
    'q7-original': D.paper(5, [30, 530, 580, 775]), 'q8-original': D.paper(6, [30, 39, 580, 285]),
    'q9-original': D.paper(6, [30, 390, 580, 650]), 'q10-original': D.paper(7, [30, 39, 580, 420]),
    'q10-alt-original': D.paper(7, [30, 515, 580, 720]),
    'q1-section': D.composite((4, [45, 56, 575, 790]), (5, [45, 56, 575, 555])),
    'q2-guidelines': D.composite((6, [45, 265, 575, 805]), (7, [45, 56, 575, 795])),
    'q3-considerations': D.scheme(8, [45, 450, 575, 780]), 'q3-layout': D.scheme(9, [45, 56, 575, 795]), 'q3-meets': D.scheme(10, [45, 56, 575, 410]),
    'q4-characteristics': D.composite((10, [45, 420, 575, 795]), (11, [45, 56, 575, 280])),
    'q4-sites': D.composite((11, [45, 305, 575, 740]), (12, [45, 56, 575, 170])), 'q4-layout': D.scheme(12, [45, 180, 575, 625]),
    'q5-calculation': D.scheme(13, [45, 56, 575, 760]), 'q5-thickness': D.scheme(14, [45, 56, 575, 280]),
    'q6-self-build': D.scheme(14, [45, 300, 575, 640]), 'q6-features': D.composite((14, [45, 645, 575, 805]), (15, [45, 56, 575, 270])),
    'q6-modifications': D.composite((15, [45, 280, 575, 790]), (16, [45, 56, 575, 595])),
    'q7-section': D.scheme(17, [45, 56, 575, 795]),
    'q8-layout': D.scheme(18, [45, 56, 575, 400]), 'q8-safety': D.composite((18, [45, 405, 575, 800]), (19, [45, 56, 575, 180])),
    'q8-chimney': D.scheme(19, [45, 190, 575, 485]),
    'q9-requirements': D.composite((19, [45, 530, 575, 790]), (20, [45, 56, 575, 480])),
    'q9-structure': D.composite((20, [45, 495, 575, 795]), (21, [45, 56, 575, 140])), 'q9-air-leakage': D.scheme(21, [45, 148, 575, 255]),
    'q10-principles': D.composite((21, [45, 265, 575, 800]), (22, [45, 56, 575, 775])),
    'q10-modifications': D.scheme(23, [45, 56, 575, 603]), 'q10-orientation': D.composite((23, [45, 603, 575, 790]), (24, [45, 56, 575, 400])),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p28 (printed 26): (a) three sections — wall of main house, roof, wall of porch — each best four details × 4 = 48, scale 4/3/2 + drafting 4/3/2 = 8: 56; (b) stepped DPC / flashing and counter flashing 4. Complete 60.'
S1 = 'One required section and one required abutment detail. The detail lists are marking menus, not printed choices.'
T1A = 'To a scale of 1:5, draw a vertical section through the porch showing the external wall of the porch, the sloping roof, and the front wall of the house. Show the typical construction details of the porch from a point 300 mm below the wallplate, through the sloping rafters to a level 300 mm above and 200 mm below the abutment of the roof and the front wall of the house. Show three courses of slate at eaves. It is not necessary to show window or door details.'
T1B = 'On your drawing, show the typical design detailing to prevent the ingress of rainwater between the roof of the porch and the front wall of the house.'
A1 = add('1', 'a', '(a)', T1A,
         [row('house-wall', 'Wall of main house', 16, 'Best four details, 4 each. Such as: external and internal renders; 100 mm block leaves with wall ties; full-fill insulated cavity; lintels; thermal blocks below the roof abutment; a timber bearer or metal hanger on the main wall; any four dimensions.'),
          row('roof', 'Roof', 16, 'Best four details, 4 each. Such as: slate on 35 × 50 mm counter battens and battens; breathable membrane on 10 mm OSB; 250–300 mm rafters or I-joists packed with 300 mm insulation; insulated plasterboard with vapour control layer; tilting fillet and ventilation at eaves and roof head; fascia, soffit and gutter.'),
          row('porch-wall', 'Wall of porch – timber clad', 16, 'Best four details, 4 each. Such as: double joists at the head; cedar cladding on battens and counter battens; breather membrane on 10 mm OSB; 250 × 50 mm studs with 250 mm breathable insulation; OSB with taped vapour control layer inside; insulated 38 mm service cavity; 12.5 mm plasterboard; airtightness tapes.'),
          row('presentation', 'Scale 4 marks, Drafting 4 marks', 8, 'Scale 4 and drafting 4, each excellent 4, good 3, fair 2.', PRES)],
         ['cons-1-5', 'cons-3-10', 'cons-3-9', 'cons-3-3', 'cons-3-2'], ['question-1-drawing-questions', 'roofs', 'walls'], 'q1-section',
         'Scaled drawing (1.5) of a lean-to roof (3.9) at its abutment (3.10) with a cavity wall (3.3) and a timber-clad wall (3.2).', B1, S1)
B1b = add('1', 'b', '(b)', T1B,
          [row('abutment', 'stepped DPC/ flashing and counter flashing', 4, 'Show and identify a stepped DPC with lead flashing and counter flashing at the abutment, as in the scheme’s model section.')],
          ['cons-3-10', 'cons-3-4'], ['roofs', 'walls'], 'q1-section', 'A roof abutment (3.10) with stepped DPC (3.4).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p29 (printed 27): (a) one risk for each of three printed tasks × 4 = 12; (b) two guidelines for each task × (note 3 + sketch 3) = 36; (c) three strategies × 4 = 12. Complete 60.'
S2 = 'All three printed tasks in (a) and (b) are required, each separately marked; not a choice.'
SAFE = (['cons-1-8'], ['site-safety'])
T2A = 'Discuss in detail one possible safety risk associated with each of the following tasks on a construction site: excavating where there are underground electrical cables; working in a deep trench; working at height when slating a roof.'
T2B = 'For each risk discussed at 2(a) above, show, using notes and freehand sketches, two best practice guidelines that should be observed to reduce the possibility of injury to a worker undertaking each task.'
T2C = 'Discuss in detail three strategies that would promote a positive safety culture among workers on a construction site.'
A2 = add('2', 'a', '(a)', T2A,
         [row('cables', 'Excavating for underground electrical cables', 4, 'Such as: electric shock or electrocution from a live cable; burns, explosion or fire if a cable is pierced; loss of power to emergency services.'),
          row('trench', 'Working in a deep trench', 4, 'Such as: the sides collapsing and burying workers; neighbouring structures undermined; materials, plant or people falling in.'),
          row('roof', 'Working at height when slating a roof', 4, 'Such as: falling from the roof, scaffold or ladder; slipping on the slates; materials or tools falling on people below.')],
         *SAFE, None, 'Safety precautions on site (1.8).', B2, S2)
B2b = add('2', 'b', '(b)', T2B,
          [row('cables', 'Excavating for electrical cables', 12, 'Two guidelines, each note 3 + sketch 3. Such as: dial before you dig and use the supplier’s cable plans; locate cables with a detector and mark them; hand dig near cables with insulated tools; no excavator within 300 mm of a cable.'),
           row('trench', 'Working in a deep trench', 12, 'Two guidelines, each note 3 + sketch 3. Such as: a trench box or shuttering; battering back the sides; guard and toe boards and an exclusion zone; spoil and plant kept back from the edge.'),
           row('roof', 'Working at slating a roof', 12, 'Two guidelines, each note 3 + sketch 3. Such as: a safe working platform with guard rails and toe boards at the eaves; slating jacks and boards on the slope; a harness or safety netting; properly secured ladders.')],
          *SAFE, 'q2-guidelines', 'Safety precautions on site (1.8).', B2, S2)
C2 = add('2', 'c', '(c)', T2C,
         [row(f'strategy-{i}', f'Strategy {i}', 4, note) for i, note in [
             (1, 'Such as: a buddy system pairing new and experienced workers; Safe Pass and manual handling courses for all.'),
             (2, 'A second, different strategy. Such as: frequent site safety meetings; a safety statement and emergency plan all workers know.'),
             (3, 'A third, different strategy. Such as: a safety representative on larger sites; clear multilingual signage and interpreters; everyone alert to risks for one another.')]],
         *SAFE, None, 'Safety precautions on site (1.8).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-guidelines', B2, S2, parts(('a', T2A), ('b', T2B), ('c', T2C)))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p30 (printed 28): (a) three considerations × 6 = 18; (b) extension note 6 and sketch 6, modification note 6 and sketch 6 = 24; (c) three discussions × 6 = 18. Complete 60.'
S3 = 'Considerations and the layout are open responses with no printed list.'
WELL = (['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'])
T3A = 'Discuss three considerations that should be taken into account in the design of the extension to ensure that the health and wellbeing of the occupants is enhanced by building the extension.'
T3B = 'Using notes and freehand sketches, show a proposed design layout for the extension and the necessary modifications to the existing layout of the cottage.'
T3C = 'Discuss how your proposed design meets each consideration discussed at 3(a) above.'
A3 = add('3', 'a', '(a)', T3A,
         [row(f'consideration-{i}', f'Consideration {i}', 6, note) for i, note in [
             (1, 'Such as: biophilic design — a connection with nature, seeing plants, hearing birds; daylight central to the design.'),
             (2, 'A second, different consideration. Such as: more south glazing for solar gain and lower heating costs; natural light and shade.'),
             (3, 'A third, different consideration. Such as: local, natural materials; decking extending the inside outdoors; good thermal and airflow comfort; a sense of safety.')]],
         *WELL, 'q3-considerations', 'Health and wellbeing in the built environment (1.2) through good daylighting (7.4).', B3, S3)
B3b = add('3', 'b', '(b)', T3B,
          [row('extension-note', 'Note for extension', 6, 'Such as: glazed openings to the garden with sliding or bi-fold doors; glazing to floor level; open plan for daylight; roof lights; overhangs or brise-soleil against summer glare.'),
           row('extension-sketch', 'Sketch of extension', 6, 'A layout sketch of the extension at the rear, as in the scheme’s model plan.'),
           row('modification-note', 'Note for modification', 6, 'Such as: openings through to the existing rooms; bright colours and mirrors to spread light; glass panels in doors.'),
           row('modification-sketch', 'Sketch of modification', 6, 'A sketch of the modified existing layout.')],
          ['cons-1-2', 'cons-1-1'], ['planning-sustainability-environment', 'conservation-restoration'], 'q3-layout',
          'Extending an older dwelling (1.1) in the built environment (1.2).', B3, S3)
C3 = add('3', 'c', '(c)', T3C,
         [row(f'discussion-{i}', f'Discussion {i}', 6, note) for i, note in [
             (1, 'How the design meets the first consideration. Such as: large south windows maximise light and solar gain and connect with nature.'),
             (2, 'How the design meets the second consideration. Such as: sliding doors bring the garden in; open plan lets sunlight through.'),
             (3, 'How the design meets the third consideration. Such as: high thermal performance and shading; external materials connected to the local ecology; water and planting to stimulate the senses.')]],
         *WELL, 'q3-meets', 'Health and wellbeing in the built environment (1.2) through good daylighting (7.4).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-layout', B3, S3, parts(('a', T3A), ('b', T3B), ('c', T3C)))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p31 (printed 29): (a) two printed characteristics × (notes 6 + sketches 6) = 24; (b) site A or site B, three considerations × 5 = 15; (c) sketch, location, orientation, entrance and driveway × 3 = 15 and justification 6 = 21. Complete 60.'
S4 = 'Both printed characteristics in (a) are required. "Select your preferred site" (A or B) is one task, the scheme marking the three considerations alike for either site, not a separate route.'
SITE = (['cons-1-3'], ['planning-sustainability-environment'])
T4A = 'Using notes and freehand sketches, discuss the importance of each of the following when identifying a suitable site for a new house in a rural landscape: characteristics of existing dwellings; characteristics of the proposed site.'
T4B = 'An extract from a site location map is shown. A and B are possible sites for a new house. Select your preferred site and discuss three considerations you took into account when selecting your site.'
T4C = 'Draw a well-proportioned sketch of your selected site and the immediate boundaries. On your sketch, show a preferred: location and orientation of a house on the site; layout of the road entrance and the driveway to the house. For each of the above, justify your design choices.'
A4 = add('4', 'a', '(a)', T4A,
         [row('dwellings', 'Characteristics of existing dwellings (notes and sketches)', 12, 'Notes 6 and sketches 6. Such as: scale, volume, shape and materials informed by the local vernacular; simple regular forms; the direction and position of existing dwellings; not overshadowing or overlooking neighbours.'),
          row('site', 'Characteristics of proposed site (notes and sketches)', 12, 'Notes 6 and sketches 6. Such as: road layout and sightlines for a safe entrance; existing stone walls, trees and boundaries kept; topography and natural shelter; orientation for solar gain; soil, percolation, services and flooding.')],
         ['cons-1-3', 'cons-1-1'], ['planning-sustainability-environment', 'conservation-restoration'], 'q4-characteristics',
         'Choosing a site (1.3) with respect for the existing rural character (1.1).', B4, S4)
B4b = add('4', 'b', '(b)', T4B,
          [row(f'consideration-{i}', f'Consideration {i}', 5, note) for i, note in [
              (1, 'For either site. Such as, site A: away from the main road, less noise and pollution; site B: access from the main or minor road with little roadwork.'),
              (2, 'A second, different consideration. Such as, site A: not overlooked, more privacy; site B: close to services such as water, electricity and broadband.'),
              (3, 'A third, different consideration. Such as, site A: a smaller site needing less land; site B: long sightlines on a straight road; houses nearby in a cluster.')]],
          *SITE, 'q4-sites', 'Choosing a site (1.3).', B4, S4)
C4 = add('4', 'c', '(c)', T4C,
         [row('sketch', 'Sketch showing location, orientation, road entrance and driveway (5 × 3 marks)', 15, 'Sketch 3, location 3, orientation 3, entrance 3 and driveway 3. Such as: the largest elevation facing south; close to the road where the services are; a short driveway; a splayed entrance set back about 5 m with clear sightlines both ways.'),
          row('justification', 'Justification', 6, 'The location, orientation, entrance and driveway justified, such as for solar gain, privacy, lower cost and safe access.')],
         ['cons-1-3', 'cons-6-4'], ['planning-sustainability-environment'], 'q4-layout', 'Siting (1.3) and orientation for solar gain (6.4).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-layout', B4, S4, parts(('a', T4A), ('b', T4B), ('c', T4C)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p32 (printed 30): (a) ten points × 3 = 30 (tabulation, the internal surface and six layers, total resistance, U-value); (b) five steps × 3 = 15; (c) five steps × 3 = 15. Complete 60.'
S5 = 'No printed choice. Parts (b) and (c) use the U-value from (a).'
DATA5 = ('Sand/cement fine screed thickness 50 mm; Concrete floor slab thickness 100 mm; Radon barrier thickness 0.25 mm; Sand blinding thickness 40 mm; Hardcore thickness 200 mm; Subsoil thickness 300 mm.\n'
         'Thermal data of the concrete ground floor: Resistance of internal top surface of floor (R) 0.104 m2 °C/W; Resistivity of fine screed (r) 0.710 m °C/W; '
         'Conductivity of concrete floor slab (k) 1.280 W/m °C; Conductivity of radon barrier (k) 0.250 W/m °C; Conductivity of sand blinding (k) 0.160 W/m °C; '
         'Conductivity of hardcore (k) 1.350 W/m °C; Conductivity of subsoil (k) 1.600 W/m °C.')
T5A = 'Calculate the U-value of the uninsulated concrete ground floor, given the following data: ' + DATA5
T5B = ('Using the U-value of the concrete floor obtained at 5(a) above and the following data, calculate the cost of heat lost annually through the uninsulated concrete floor slab: '
       'dimensions of floor slab 6.0 metres × 12.0 metres; average internal temperature 21 °C; average temperature of subsoil 5 °C; heating period 10 hours daily for 38 weeks per annum; '
       'cost of oil 96 cent per litre; calorific value of oil 37350 kJ per litre; 1000 Watts 1 kJ per second.')
T5C = ('It is proposed to redesign the above floor and upgrade its thermal properties to meet the Passive House standard by including expanded polystyrene in the design of the floor. '
       'Given the thermal conductivity (k) of expanded polystyrene as 0.037 W/m °C, calculate the thickness of expanded polystyrene required to achieve a U-value of 0.15 W/m2 °C.')
A5 = add('5', 'a', '(a)', T5A,
         [row('tabulation', 'Tabulation', 3, 'The calculation set out in a table of material, conductivity, resistivity, thickness and resistance.'),
          row('resistances', 'Internal top surface resistance Fine screed Concrete floor slab Radon barrier Sand blinding Hardcore Subsoil', 21,
              'Seven resistances, 3 each, by R = T/k (or R = T × r for the screed): internal top surface 0.1040 (given); screed 0.05 × 0.71 = 0.0355; slab 0.1/1.28 = 0.0781; radon barrier 0.00025/0.25 = 0.0010; sand blinding 0.04/0.16 = 0.2500; hardcore 0.2/1.35 = 0.1481; subsoil 0.3/1.6 = 0.1875. All in m²°C/W.', list(range(0, 22, 3))),
          row('total-resistance', 'Total resistance', 3, 'Total resistance Rt = 0.8042 m²°C/W.', [0, 3]),
          row('u-value', 'Calculation of U-value of ground floor', 3, 'U = 1 ÷ Rt = 1 ÷ 0.8042 = 1.2434 W/m²°C, with units.', [0, 3])],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Thermal resistance, conductivity and transmittance (6.1).', B5, S5)
B5b = add('5', 'b', '(b)', T5B,
          [row('heat-loss', 'Heat loss formula and calculations', 3, 'Heat loss = U-value × area × temperature difference = 1.2434 × 72 × 16 = 1432.3968 watts (joules per second).'),
           row('duration', 'Heating duration for one year', 3, 'Heating period = 60 × 60 × 10 × 7 × 38 = 9,576,000 seconds (2,660 hours).'),
           row('energy', 'k/Joules calculation for one year', 3, 'Energy = 9,576,000 × 1432.3968 ÷ 1000 = 13,716,631.18 kJ per year.'),
           row('oil', 'Litres of oil for one year', 3, 'Oil = 13,716,631.18 ÷ 37,350 = 367.24 litres per year.'),
           row('cost', 'Annual cost of heat loss', 3, 'Annual cost = 367.24 × €0.96 = €352.5. The scheme’s alternative one-line method gives the same €352.5.')],
          ['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Heat loss calculation and running costs (6.3) from the U-value (6.1).', B5, S5)
C5 = add('5', 'c', '(c)', T5C,
         [row('required-resistance', 'Resistance for U- value for 0.15Wm2K using R=1/U', 3, 'Required resistance = 1 ÷ 0.15 = 6.6666 m²K/W.'),
          row('existing-resistance', 'Resistance from calculated U-value from part (a)', 3, 'Existing resistance = 1 ÷ 1.2434 = 0.8042 m²K/W.'),
          row('difference', 'Difference in resistances (required resistance)', 3, 'Difference = 6.6666 − 0.8042 = 5.8624 m²K/W.'),
          row('formula', 'Application of formula R = T/k', 3, 'R = T/k, so 5.8624 = T/0.037.'),
          row('thickness', 'Required thickness of insulation', 3, 'T = 5.8624 × 0.037 = 0.2169088 m: 216.9 mm of expanded polystyrene (216 or 217 mm accepted).')],
         ['cons-6-1', 'cons-6-2', 'cons-4-2'], ['heat-u-value-calculations', 'heat-loss-insulation', 'floors'], 'q5-thickness',
         'Thermal transmittance (6.1) and insulating (6.2) a solid ground floor (4.2).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p33 (printed 31): (a) two advantages and two disadvantages × 3 = 12; (b) three design features × (note 5 + sketch 5) = 30; (c) two modifications × (note 3 + sketch 3) and two justifications × 3 = 18. Complete 60.'
S6 = 'Part (a) requires both two advantages and two disadvantages, each separately marked. Features and modifications are open responses.'
GREEN = (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'])
T6A = 'Discuss two advantages and two disadvantages of self-build as a method of building a house.'
T6B = 'Discuss in detail, using notes and freehand sketches, three features of the design shown that make the house suitable as a self-build project.'
T6C = 'Suggest, using notes and freehand sketches, two modifications to the existing design that would further reduce the environmental impact of the house and help meet the nearly Zero Energy Building (nZEB) requirements. Justify your design choices.'
A6 = add('6', 'a', '(a)', T6A,
         [row('advantage-1', 'Advantage 1 of self-build', 3, 'Such as: reduced costs with help from family, friends and neighbours; a smaller mortgage.'),
          row('advantage-2', 'Advantage 2 of self-build', 3, 'A second, different advantage. Such as: control over build quality and finish; personal satisfaction; building over a longer period as budget allows.'),
          row('disadvantage-1', 'Disadvantage 1 of self-build', 3, 'Such as: a skills deficit through inexperience; demanding building contract management.'),
          row('disadvantage-2', 'Disadvantage 2 of self-build', 3, 'A second, different disadvantage. Such as: a longer construction period; no building guarantee or contracts with friends; responsibility for health and safety and regulations.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q6-self-build', 'Procuring a house in the built environment (1.2).', B6, S6)
B6b = add('6', 'b', '(b)', T6B,
          [row(f'feature-{i}', f'Design feature {i}', 10, note) for i, note in [
              (1, 'Note 5 and sketch 5. Such as: built mainly of locally sourced, renewable timber, easy to cut and shape with hand tools; a simple form, easy to set out.'),
              (2, 'A second, different feature. Such as: small and compact with a narrow span for standard joists; a light building simplifying the foundations.'),
              (3, 'A third, different feature. Such as: a straightforward roof; light frame and rainscreen needing no lifting equipment; early closing-in for dry indoor trades.')]],
          ['cons-1-2', 'cons-3-3'], ['sustainability-the-environment', 'walls'], 'q6-features', 'A simple timber frame house (3.3) built sustainably (1.2).', B6, S6)
C6 = add('6', 'c', '(c)', T6C,
         [row('modification-1', 'Modification 1', 6, 'Note 3 and sketch 3. Such as: a storm porch or inner hall at the front door; thicker insulation in the external walls.'),
          row('modification-2', 'Modification 2', 6, 'A second, different modification: note 3 and sketch 3. Such as: more south glazing or a sunroom; a glazed partition zoning the kitchen and dining areas; evacuated tubes, PV panels, rainwater harvesting or a wind generator.'),
          row('justification-1', 'Justification 1', 3, 'The first modification justified against nZEB: very low energy demand largely met from renewables.'),
          row('justification-2', 'Justification 2', 3, 'The second modification justified.')],
         *GREEN, 'q6-modifications', 'Reducing environmental impact (1.2) through solar gain (6.4) and insulation (6.2).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-features', B6, S6, parts(('a', T6A), ('b', T6B), ('c', T6C)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p34 (printed 32): (a) four details from each of three sections — external wall, door, floor — × 4 = 48, scale and drafting 4/3/2 each = 8: 56; (b) airtightness design detail 4. Complete 60.'
S7 = 'One required section and one required airtightness detail. The detail lists are marking menus, not printed choices.'
T7A = 'To a scale of 1:5, draw a vertical section through a portion of the external wall, doorframe, door, first floor joists, and floor. Show the typical construction details from a level 400 mm below the top of the door to a level 300 mm above the first floor joists.'
T7B = 'Show clearly on your drawing best-practice design detailing to ensure airtightness at the junction of the external wall and the first floor.'
A7 = add('7', 'a', '(a)', T7A,
         [row('wall', 'External wall', 16, 'Best four details, 4 each. Such as: 450 mm block wall; full-fill cavity insulation; internal and external plaster/render; cavity closer; lintels; basalt low-conductivity wall ties; stepped DPC.'),
          row('door', 'Door', 16, 'Best four details, 4 each. Such as: thermally broken frame; top rail; airtightness tape from frame to wall; insulation; vertical sheeting; double rebates with draught-proofing strips.'),
          row('floor', 'Floor', 16, 'Best four details, 4 each. Such as: joist bearer fixed to the wall; mechanical fixing of the joist to the wall; joist hanger; 200 × 40 mm joists; plywood decking; floating wooden floor; plasterboard ceiling.'),
          row('presentation', 'Scale and drafting marks (Excellent, Good, Fair)', 8, 'Scale and drafting, each excellent 4, good 3, fair 2.', PRES)],
         ['cons-1-5', 'cons-3-7', 'cons-3-3', 'cons-4-3'], ['question-1-drawing-questions', 'doors', 'walls', 'floors'], 'q7-section',
         'Scaled drawing (1.5) of an external door (3.7) in a cavity wall (3.3) carrying a timber upper floor (4.3).', B7, S7)
B7b = add('7', 'b', '(b)', T7B,
          [row('airtightness', 'Design detail', 4, 'Show and identify the airtightness detail at the wall/floor junction, such as airtightness tape at the junction of wall and ceiling and joists on hangers rather than built into the inner leaf.')],
          ['cons-6-5', 'cons-4-3'], ['condensation-air-tightness', 'floors'], 'q7-section', 'Airtightness (6.5) at the upper floor junction (4.3).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p35 (printed 33): (a) best eight of the listed items × 3 = 24 and pipe sizes (any 2) 4 = 28; (b) two features × (note 4 + sketch 4) and discussion 4 = 20; (c) two chimney considerations × (note 3 + sketch 3) = 12. Complete 60.'
S8 = 'The listed components are a marking menu. Both safety features and both chimney considerations are required.'
HEAT = (['cons-5-3', 'cons-5-2'], ['hot-water-space-heating'])
T8A = 'Using notes and a single-line diagram, show a typical design layout for both the central heating and the hot water systems. Show two independently controlled heating zones, one on each floor. Include three radiators on each floor and give the typical sizes of the pipework.'
T8B = 'Using notes and freehand sketches, describe two features that ensure that the system operates safely at all times. Discuss the importance of each safety feature outlined.'
T8C = 'Using notes and freehand sketches, show two design considerations that should be taken into account when selecting a preferred location of a chimney for the stove. Discuss the importance of each consideration outlined.'
A8 = add('8', 'a', '(a)', T8A,
         [row('items', 'Design layout of zoned plumbing system (8 × 3 marks)', 24, 'Best eight items, 3 each. Menu: stove and radiators; zone controls and zone thermostats; header/expansion tank; feed and cold feed; expansion pipe or vessel; flow and return pipes to radiators; radiator valves; pump and valves; solar panel; flow and return marked; solar pump; twin-coil cylinder; control panel; expansion vessel; thermal reducing vessel.', list(range(0, 25, 3))),
          row('sizes', 'Sizes of pipework (any 2)', 4, 'Any two typical pipe sizes, 2 each, such as 22 mm flow and return and 15 mm to radiators.')],
         *HEAT, 'q8-layout', 'Heating systems (5.3) with an indirect cylinder (5.2).', B8, S8)
B8b = add('8', 'b', '(b)', T8B,
          [row('feature-1', 'Feature 1', 8, 'Note 4 and sketch 4. Such as: thermostatic control of the burning rate and TRVs with a boiler interlock; a cylinder thermostat a third of the way up.'),
           row('feature-2', 'Feature 2', 8, 'A second, different feature: note 4 and sketch 4. Such as: a pressure relief or vent valve; an open expansion pipe or sealed expansion vessel; a carbon monoxide alarm.'),
           row('discussion', 'Discussion of safety features', 4, 'The importance of each feature discussed, such as preventing overheating, explosion from pressure build-up, or carbon monoxide poisoning.')],
          *HEAT, 'q8-safety', 'Heating systems and their controls (5.3, 5.2).', B8, S8)
C8 = add('8', 'c', '(c)', T8C,
         [row('consideration-1', 'Design consideration1 Note & Sketch', 6, 'Note 3 and sketch 3. Such as: on an internal wall so the chimney’s thermal mass keeps heat in the house.'),
          row('consideration-2', 'Design consideration 2 Note & Sketch', 6, 'A second, different consideration: note 3 and sketch 3. Such as: central and near the bathroom to avoid wasting water; an insulated, double-walled system chimney encased where it passes combustible material.')],
         ['cons-5-7'], ['fireplaces-fire-prevention'], 'q8-chimney', 'Flues to domestic fireplaces and stoves (5.7).', B8, S8)
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-layout', B8, S8, parts(('a', T8A), ('b', T8B), ('c', T8C)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p36 (printed 34): (a) three requirements × (notes 6 + sketches 6) = 36; (b) structural stability 6, stud side wall and insulation 6, labelled components and dimensions 3 × 2 = 18; (c) air-leakage detail 6. Complete 60.'
S9 = 'Requirements are open responses; (b) requires the roof, the stud side walls and insulation, and labelled dimensions, each separately marked.'
T9A = 'Discuss in detail using notes and freehand sketches, three functional requirements of an attic space suitable for use as a bedroom.'
T9B = 'A traditional cut roof, which is slated and has a pitch of 45°, is designed to provide a well-insulated bedroom in the attic space, as shown. Using notes and freehand sketches, show the typical design detailing for such a roof. Include the stud side walls and the insulation. Show clearly the design detailing necessary to ensure the structural stability of the roof. Label the main components and give their typical dimensions.'
T9C = 'On your sketch, show one design detail to prevent air leakage at the junction of the stud side wall and the sloped ceiling.'
A9 = add('9', 'a', '(a)', T9A,
         [row(f'requirement-{i}', f'Functional requirement {i}', 12, note) for i, note in [
             (1, 'Notes 6 and sketches 6. Such as: adequate floor area with a 2400 mm ceiling over at least half the floor; natural lighting and ventilation through roof lights or dormers.'),
             (2, 'A second, different requirement. Such as: fire safety — fire-rated plasterboard, smoke detection, fire doors and a means of escape; sound insulation with a floating floor.'),
             (3, 'A third, different requirement. Such as: safe permanent stair access; thermal insulation to a U-value of 0.16 for the roof, avoiding thermal bridging; electrical work to standard.')]],
         ['cons-3-9', 'cons-1-9'], ['roofs', 'fireplaces-fire-prevention'], 'q9-requirements', 'A habitable roof space (3.9) meeting the building regulations (1.9).', B9, S9)
B9b = add('9', 'b', '(b)', T9B,
          [row('stability', 'Structural stability - pitched roof Notes & sketches', 6, 'Such as: purlins strutted from mounted wallplates; collar ties at 2400 mm forming a triangle; doubled rafters at roof lights; struts, runners and joists of sufficient size for the span.'),
           row('stud-wall', 'Stud side wall and insulation Notes & sketches', 6, 'Such as: vertical studs 200 × 40 mm; insulation between and under the rafters with a vapour barrier; a service cavity at the ceiling.'),
           row('labels', 'Labelled components and dimensions (3 × 2 marks)', 6, 'Three labelled components with dimensions, 2 each, such as rafters 200 × 40 at 400–600 mm, collar ties 200 × 40, purlin 200 × 75 mm.')],
          ['cons-3-8', 'cons-3-9', 'cons-4-5'], ['roofs', 'doors'], 'q9-structure', 'Cut roof structure (3.8), insulation (3.9) and stud side walls (4.5).', B9, S9)
C9 = add('9', 'c', '(c)', T9C,
         [row('air-leakage', 'Air leakage design detail', 6, 'Such as: the continuous airtight membrane overlapped at the junction and sealed with proprietary adhesive tape, kept clear of the angle between stud wall and sloping ceiling.')],
         ['cons-6-5', 'cons-3-9'], ['condensation-air-tightness', 'roofs'], 'q9-air-leakage', 'Airtightness (6.5) of the roof space (3.9).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-structure', B9, S9, parts(('a', T9A), ('b', T9B), ('c', T9C)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p37 (printed 35): (a) any two of three printed items × (notes 4 + sketches 4) = 16; (b) three modifications × (notes and sketches 8) and justification 4 = 28; (c) sketch, orientation, sun path and thermal performance × 4 = 16. Complete 60.'
S10 = 'Choice is not a route: part (a) (any two of three printed items) is ONE card with an any-two group over the scheme headings; its figure and the complete-question figure carry all three items’ drawings. The OR alternative is a separate Question 10 route.'
PASSIVE = (['cons-6-2', 'cons-6-4', 'cons-6-5'], ['passive-design'])
T10A = 'Using notes and freehand sketches, discuss the importance of any two of the following in Passive House design: space heating energy demand; building form; thermal bridging.'
T10B = 'The drawing shows a preliminary design of a dwelling house, having two bedrooms and a bathroom upstairs. The clients wish to upgrade this design to meet the Passive House standard. Show, using notes and freehand sketches, three modifications you would make to this design to help meet the Passive House standard. Justify your design choices.'
T10C = 'Show, using notes and freehand sketches, a preferred orientation for your upgraded design. Include the sun path in your sketch and discuss how your preferred orientation ensures the optimum thermal performance of the house. Note: It is not necessary to show the furniture.'
ITEMS10 = [('Space heating energy demand', 'the energy to keep 20 °C all year, at most 15 kWh/m²/a in a Passive House, set by insulation and airtightness; solar gain from well-placed glazing with shading against overheating.'),
           ('Building form', 'a simple compact form with fewer junctions, less envelope and lower heat loss; a low surface-to-volume (A/V) ratio, ideally 0.7 or less; avoid complex hips and valleys.'),
           ('Thermal bridging', 'areas of higher conductivity let heat escape and cause cold spots, condensation and mould; continuity of insulation at openings, floor and eaves junctions, as in the scheme’s details.')]
A10 = add('10', 'a', '(a)', T10A,
          [anyn('items', 'Design of a passive house - any 2', 2, 8, ITEMS10, 'Any two of the three printed items, each notes 4 and sketches 4 = 8.')],
          ['cons-6-2', 'cons-6-3', 'cons-6-4'], ['passive-design', 'heat-loss-insulation'], 'q10-principles',
          'The union of the three printed items: space heating demand (6.3), building form and solar gain (6.4), and thermal bridging (6.2).', B10, S10)
B10b = add('10', 'b', '(b)', T10B,
           [row(f'modification-{i}', f'Modification {i} (notes and sketches)', 8, note) for i, note in [
               (1, 'Notes and sketches, 8. Such as: a draught lobby at the entrance; the long axis east-west with larger south windows and smaller north windows.'),
               (2, 'A second, different modification. Such as: more window area in the kitchen and dining room; roof lights; large eaves or brise-soleil over south windows.'),
               (3, 'A third, different modification. Such as: the stove and chimney moved to an inner wall, or replaced with MHRV; heat exchange technology; solar PV or evacuated tubes on the south roof.')]]
           + [row('justification', 'Justification', 4, 'The modifications justified against the Passive House standard.')],
           *PASSIVE, 'q10-modifications', 'Passive design: insulation (6.2), solar gain (6.4) and ventilation (6.5).', B10, S10)
C10 = add('10', 'c', '(c)', T10C,
          [row('sketch', 'Sketch', 4, 'A sketch of the upgraded design on its site.'),
           row('orientation', 'Orientation', 4, 'The long glazed façade facing south, or within 30° of south.'),
           row('sun-path', 'Sunpath', 4, 'The sun path shown, with its winter and summer heights.'),
           row('thermal-performance', 'Optimum thermal performance', 4, 'How the orientation gives solar gain and less heat loss: large glazing south or south-west, small glazing north, south roof for solar panels.')],
          ['cons-6-4'], ['passive-design', 'planning-sustainability-environment'], 'q10-orientation', 'Solar heat gain and orientation (6.4).', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-principles', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p38 (printed 36): discussion of the statement, three points × (4 + 6) = 30; three best practice guidelines × (4 + 6) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately, so each is its own task and the complete card composes them.'
TAA = 'Discuss the above statement in detail.'
TAB = 'Propose three best practice guidelines that would promote green, sustainable housing in Ireland.'
TALL = 'Discuss the above statement in detail and propose three best practice guidelines that would promote green, sustainable housing in Ireland.'
SUST = (['cons-1-2', 'cons-6-4'], ['sustainability-the-environment'])
AA = add('10', 'discussion', ' — discussion', TAA,
         [row(f'point-{i}', f'Discussion – point {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: building green means responsible choices from the start of the design, not a last resort; avoiding eco-bling gadgets.'),
             (2, 'Point 4 and discussion 6. Such as: modest, compact buildings with less material and a small ecological footprint; local materials cutting transport and embodied energy.'),
             (3, 'Point 4 and discussion 6. Such as: health and wellbeing at the centre with natural, non-toxic materials and biophilic design; life-cycle thinking about running costs. Three distinct, well-argued points are needed.')]],
         *SUST, None, 'Sustainable design of the built environment (1.2, 6.4).', BALT, SALT, alt=True)
AB = add('10', 'guidelines', ' — guidelines', TAB,
         [row(f'guideline-{i}', f'Guideline {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: planning authorities publishing green design guides and clear planning guidelines for sustainable homes.'),
             (2, 'Point 4 and discussion 6. Such as: grants and incentives for renewable energy, on-site generation and energy-saving fittings.'),
             (3, 'Point 4 and discussion 6. Such as: training professionals in green building with materials such as wood, cob, rammed earth and hemp-lime; promoting eco-villages and universal design. Three distinct guidelines are needed.')]],
         *SUST, None, 'Sustainable design of the built environment (1.2, 6.4).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, TALL, labels=['Discussion of the statement', 'Three best practice guidelines'], alt=True)

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and any four of the other nine (300 marks); all question banks retained, no full-exam Cartesian cards.'),
          (2, 'or', 'Q1(a) wording ("window or door details"): not a candidate choice.'),
          (2, 'answer fits', 'Q1 note ("ensure that the answer fits on the drawing sheet"): not a candidate choice.'),
          (3, 'Select', 'Q4(b) select site A or B: one task, the scheme marking the three considerations alike for either site.'),
          (7, 'any two', 'Q10(a) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
          (7, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.')]
FINITE = {'10a': dict(choose=2, options=[h for h, _ in ITEMS10], cardId=A10['id'], groupRowId='items')}
REASONS = {
    'q1-a': 'Rows rebuilt to the printed table — three sections of four details × 4 and the scale and drafting allowance (8): 40 → 56.',
    'q1-b': 'Reshaped to the printed row "stepped DPC/ flashing and counter flashing"; tariff unchanged (4).',
    'q2-a': 'Split into one row per printed task (4 each); tariff unchanged (12).',
    'q2-b': 'One row per printed task, each two guidelines at note 3 + sketch 3; tariff unchanged (36).',
    'q2-c': 'Split into the three printed strategies (4 each); tariff unchanged (12).',
    'q3-a': 'Split into the three printed considerations (6 each); tariff unchanged (18).',
    'q3-b': 'Split into the printed extension and modification notes and sketches (6 each); tariff unchanged (24).',
    'q3-c': 'Split into the three printed discussions (6 each); tariff unchanged (18).',
    'q4-a': 'Split into the two printed characteristics (notes 6 + sketches 6 each); tariff unchanged (24).',
    'q4-b': 'Split into the three printed considerations (5 each), marked alike for site A or site B; tariff unchanged (15).',
    'q4-c': 'Adds the printed justification (6) to the sketch, location, orientation, entrance and driveway (5 × 3): 15 → 21.',
    'q5-a': 'Rebuilt to the ten printed points (3 each), including the tabulation and the internal surface resistance: 27 → 30.',
    'q5-b': 'Reshaped to the five printed calculation steps (3 each) with the scheme’s worked answer (€352.5); tariff unchanged (15).',
    'q5-c': 'Reshaped to the five printed calculation steps (3 each) with the scheme’s worked answer (216.9 mm); tariff unchanged (15).',
    'q6-a': 'Split into the two printed advantages and two disadvantages (3 each); tariff unchanged (12).',
    'q6-b': 'Split into three design features, each note 5 + sketch 5; tariff unchanged (30).',
    'q6-c': 'Rebuilt to the printed rows — two modifications (note 3 + sketch 3) and two justifications (3 each); tariff unchanged (18).',
    'q7-a': 'Rows rebuilt to the printed table — external wall, door and floor, four details × 4 each, and the scale and drafting allowance (8): 16 → 56.',
    'q7-b': 'Reshaped to the printed design-detail row; tariff unchanged (4).',
    'q8-a': 'Adds the printed pipe sizes (any 2, 4) to the best-eight items: 24 → 28.',
    'q8-b': 'Rebuilt to the printed rows — two features (note 4 + sketch 4) and the discussion (4); tariff unchanged (20).',
    'q8-c': 'Split into the two printed considerations (note & sketch 6 each); tariff unchanged (12).',
    'q9-a': 'Split into three requirements, each notes 6 + sketches 6; tariff unchanged (36).',
    'q9-b': 'Rebuilt to the printed rows — structural stability 6, stud side wall and insulation 6, labelled components and dimensions 3 × 2: 24 → 18 (the printed table totals 18; 24 overran the question’s 60).',
    'q9-c': 'Reshaped to the printed air-leakage detail row; tariff unchanged (6).',
    'q10-a': 'Now one card with an any-two group over all three printed items (notes 4 + sketches 4 each); choice is not a route; tariff unchanged (16).',
    'q10-c': 'Split into the four printed rows (4 each); tariff unchanged (16).',
}
D.finish(LEDGER, FINITE, REASONS, marked_alike={'4b': dict(options=['site A', 'site B'], cardId=B4b['id'])})
