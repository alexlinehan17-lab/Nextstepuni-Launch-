"""Draft the 2021 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 31-41). Q4(b) "select your preferred site A or B" is one task, the scheme marking either site
with the same rows. The 33 pre-audit 2021 Higher cards keep their IDs and concept IDs and are
corrected in place. Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Accessible door threshold, wall and floor section', concept='accessible-threshold-section',
              stem='The sketch shows an external wooden door which is designed to facilitate ease of access for everyone to the dwelling house. The door is highly insulated with vertical sheeting on both sides. The wall of the house is a 400 mm wall of concrete block construction with a full-fill insulated cavity. The ground floor is a highly insulated solid concrete floor with a 20 mm tongue and groove floating hardwood finish.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the thermal-bridge detail in (b) is marked separately.'),
    '2': dict(page=2, title='Duty of care and site risks', concept='site-duty-of-care', stem='',
              note='Original question retained. Every printed item in (a) and (b) is required, each separately marked; (c) gives two procedures for each risk.'),
    '3': dict(page=3, title='A garden home office for health and wellbeing', concept='home-office',
              stem='The drawing shows the ground floor plan of a two-storey semi-detached house and its rear garden. The rear wall A-A is south facing. The owners require a home office space, which will enhance health and wellbeing while working from home. It is proposed to build a single-storey office space, not greater than 18.0 m2 in area, at the rear of the house.',
              note='Original plan retained. Considerations and layouts are open responses; the scheme gives model layouts. Part (c) requires both two advantages and two disadvantages, separately marked.'),
    '4': dict(page=3, title='Choosing a rural site', concept='rural-site-selection', stem='',
              note='Original site location map retained. All three printed factors in (a) are required, each separately marked. In (b) the candidate selects site A or B and the same three considerations are marked either way; (c) sketches the selected site.'),
    '5': dict(page=4, title='Timber-frame wall U-value, Passive House upgrade and moisture control', concept='timber-frame-u-value',
              stem='The sketch shows a proposed external wall design detail for a new house of timber frame construction.',
              note='All printed data are retained in the original question. Part (b) uses the U-value from (a); the scheme’s worked answers are U = 0.184 W/m²°C and about 42 mm of sheep wool.'),
    '6': dict(page=5, title='Low environmental impact urban terraced house', concept='low-impact-terrace',
              stem='The elevation and ground floor plan of a terraced house constructed in an urban location are shown. The external walls are of timber frame construction with a rendered concrete block and cedar cladding finish. Central heating is provided using a renewable heat source. The house is designed to have low environmental impact.',
              note='Original elevation and plan retained. Features, added features and advantages are open responses; the scheme lists typical examples.'),
    '7': dict(page=5, title='Chimney stack and roof section', concept='chimney-roof-section',
              stem='A chimney stack projects through a pitched roof at ridge level as shown. The chimney is of solid concrete block construction with a sand/cement render finish. The traditional cut roof has a pitch of 45° with a slate finish.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the two moisture details in (b) are marked separately.'),
    '8': dict(page=6, title='Wood-burning stove: zoned heating and hot water', concept='stove-zoned-heating',
              stem='The sketch shows a wood-burning stove used to provide hot water and central heating for a two-storey dwelling house.',
              note='Original sketch retained. The scheme’s system diagram is an exam model; the efficiency features in (b) are open choices.'),
    '9': dict(page=6, title='Sockets, ring main and micro-generation', concept='ring-main-circuit', stem='',
              note='Original question retained. The distribution board and three sockets in (b) are required content, not a choice.'),
    '10': dict(page=7, title='Solar overheating in a vernacular-inspired rural house', concept='solar-overheating',
               stem='The sketch shows the proposed design for a dwelling house in a rural setting. The design is inspired by vernacular Irish architecture.',
               note='Original sketch retained. Reasons, effects, methods and features are open, well-reasoned responses.'),
}
ALT = dict(page=7, title='Reusing historic buildings (alternative Question 10)', concept='reusing-historic-buildings',
           stem='“There is considerable potential to convert and reuse former schools, churches, mills and farm buildings in the county which will preserve these historic buildings which presently lie empty. This is an approach which underpins sustainable development in that it retains our built heritage while bringing empty structures into use. The reuse of these buildings can help to reduce the demand for new housing while also preserving the vernacular design of the area.” Adapted from: County Roscommon Rural Design Guidelines by Roscommon County Council Published by: Roscommon County Council',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the overheating question.')
SCHEME_PAGES = {'1': [4, 5, 31], '2': [6, 7, 8, 32], '3': [9, 10, 11, 33], '4': [12, 13, 14, 34], '5': [15, 16, 35], '6': [17, 18, 19, 36],
                '7': [20, 37], '8': [21, 22, 38], '9': [23, 24, 39], '10': [25, 26, 27, 40], '10-alt': [28, 29, 41]}
D = cp.Draft(HERE, 2021, 'higher', ('4c6644e20702d03fbfedaffe0e97f0e48edc2868ca8c937300cb204de4ce273e',
                                    '6753b7de9d8ecb13faaf35f0c954d5b69bb31c1671aae77db7300594419840ca'), 33, QUESTIONS, SCHEME_PAGES, alt=ALT)
row, add, compose, parts = D.row, D.add, D.compose, D.parts
BAND8 = [0, 4, 6, 8]
D.figures({
    'q1-original': D.paper(2, [45, 53, 580, 455]), 'q2-original': D.paper(2, [45, 455, 580, 720]),
    'q3-original': D.paper(3, [45, 53, 580, 419]), 'q4-original': D.paper(3, [45, 419, 580, 762]),
    'q5-original': D.paper(4, [45, 53, 580, 615]), 'q6-original': D.paper(5, [45, 53, 580, 469]),
    'q7-original': D.paper(5, [45, 469, 580, 746]), 'q8-original': D.paper(6, [45, 53, 580, 455]),
    'q9-original': D.paper(6, [45, 455, 580, 714]), 'q10-original': D.paper(7, [45, 53, 580, 390]),
    'q10-alt-original': D.paper(7, [45, 465, 580, 683]),
    'q1-section': D.composite((4, [51, 51, 550, 600]), (5, [51, 51, 550, 386])),
    'q1-thermal-bridge': D.scheme(5, [51, 415, 550, 760]),
    'q2-procedures': D.composite((7, [51, 460, 550, 790]), (8, [51, 51, 550, 790])),
    'q3-layout': D.composite((10, [51, 51, 550, 740]), (11, [51, 51, 550, 320])),
    'q4-services': D.scheme(12, [51, 51, 550, 331]), 'q4-trees': D.composite((12, [51, 312, 372, 331]), (12, [51, 331, 550, 510])),
    'q4-topography': D.scheme(12, [51, 510, 550, 770]), 'q4-factors': D.scheme(12, [51, 51, 550, 770]),
    'q4-sites': D.scheme(13, [51, 51, 550, 585]), 'q4-site-plans': D.scheme(14, [51, 51, 550, 760]),
    'q5-calculation': D.scheme(15, [51, 51, 550, 670]), 'q5-layers': D.scheme(16, [51, 51, 550, 465]),
    'q6-low-impact': D.scheme(17, [51, 51, 550, 598]),
    'q6-features': D.composite((17, [51, 598, 550, 782]), (18, [51, 51, 550, 778]), (19, [51, 51, 550, 190])),
    'q7-section': D.scheme(20, [51, 51, 550, 785]),
    'q8-system': D.scheme(21, [51, 51, 550, 591]),
    'q8-features': D.composite((21, [51, 591, 550, 790]), (22, [51, 51, 550, 400])),
    'q8-heat-pump': D.scheme(22, [51, 415, 550, 787]),
    'q9-ring-main': D.scheme(24, [51, 51, 550, 575]),
    'q10-shading': D.scheme(26, [51, 51, 550, 782]), 'q10-setting': D.scheme(27, [51, 51, 550, 640]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p31 (printed 29): (a) foundation, wall and level entrance 4 × 4, solid ground floor 4 × 4, threshold and door 4 × 4 (3 for drawing, 1 for annotation) = 48, scale 4 + drafting 4 banded 8/6/4 = 56; (b) thermal-bridge detail 4. Complete 60.'
S1 = 'One required section and one required thermal-bridge detail. The scheme detail lists are marking menus, not printed choices.'
T1A = 'To a scale of 1:5, draw a vertical section through the centre of the door, the external wall and the ground floor. Show the typical construction details from the bottom of the strip foundation to a level 400 mm above finished floor level. Show a width of 1.0 metre on each side of the door.'
T1B = 'On your drawing, show the typical design detailing that will prevent the formation of a thermal bridge at the threshold.'
A1 = add('1', 'a', '(a)', T1A,
         [row('foundation', 'Foundation, external wall and level entrance', 16, 'Best four details, 4 each (3 for drawing, 1 for annotation). Marking menu: R.C. strip foundation (typically 1350 × 400 mm); blockwork deadwork; vertical insulation as a thermal break; entrance substructure; level concrete entrance surface.'),
          row('floor', 'Solid ground floor', 16, 'Best four details, 4 each. Marking menu: compacted hardcore; sand blinding; radon barrier/DPM; 200 mm floor insulation; 150 mm concrete floor/subfloor; 20 mm hardwood flooring.'),
          row('threshold', 'Door threshold and door', 16, 'Best four details, 4 each. Marking menu: drainage channel; concrete threshold with wrap-around DPC or a proprietary insulated threshold; 15 mm upstand or 15°; airtight tape at the threshold; external door with vertical sheeting; door insulation.'),
          row('presentation', 'Scale - 4 marks Drafting - 4 marks', 8, 'Scale 4 and drafting 4, assessed together: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-3-7', 'cons-4-2', 'cons-2-4'], ['question-1-drawing-questions', 'doors', 'floors', 'foundations'], 'q1-section',
         'Scaled drawing (1.5) of an accessible door threshold (3.7) on an insulated solid ground floor (4.2) and strip foundation (2.4).', B1, S1)
B1b = add('1', 'b', '(b)', T1B,
          [row('thermal-bridge', 'Design detailing to prevent a thermal bridge', 4, 'Show and identify the detail, as in the scheme’s model: vertical insulation at the threshold keeping the floor and wall insulation continuous.')],
          ['cons-6-2', 'cons-3-7'], ['heat-loss-insulation', 'doors'], 'q1-thermal-bridge', 'A thermal bridge (6.2) at the door threshold (3.7).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p32 (printed 30): (a) three items × (3 for point + 3 for discussion) = 18; (b) one risk for each of three items × (3 + 3) = 18; (c) two procedures for each risk × (2 for note + 2 for sketch) = 24. Complete 60.'
S2 = 'Parts (a) and (b) require every printed item, each separately marked, so each item is its own task and the part composes them; not choices.'
SAFE = (['cons-1-8'], ['site-safety'])
T2A = 'Under each of the following, discuss in detail the duty of care that all workers have in maintaining high safety standards on a construction site: safety training; personal protective equipment (PPE); vigilance.'
ITEMS2A = [('safety-training', 'Safety Training', 'Point 3 and discussion 3. Such as: a Safe Pass course and refresher every 3–4 years; attending and engaging in all safety training; specialist training before using equipment, machinery or vehicles.'),
           ('personal-protective-equipment-ppe', 'Personal Protective Equipment', 'Point 3 and discussion 3. Such as: PPE required by law (helmet, boots, high-visibility clothing, gloves, glasses, ear protection, harness); no work without the correct PPE; defects reported at once; visitors given PPE.'),
           ('vigilance', 'Vigilance', 'Point 3 and discussion 3. Such as: knowing and regularly reviewing the safety statement; reporting hazards and concerns about health and safety.')]
a2 = [add('2', f'a-{slug}', f'(a) — {slug}', f'{T2A} — {heading}', [row('duty', f'{heading} (3 for point, 3 for discussion)', 6, note)], *SAFE, None,
          'Safety precautions on site (1.8).', B2, S2) for slug, heading, note in ITEMS2A]
A2 = compose('2', 'a', '(a)', a2, None, B2, S2, T2A, labels=[x[1] for x in ITEMS2A])
T2B = 'Discuss in detail one possible risk associated with each of the following: repairing a chimney stack; overhead electrical cables; on-site health & hygiene.'
ITEMS2B = [('repairing-a-chimney-stack', 'Repairing a chimney stack', 'Repairing a chimney (3 for point, 3 for discussion)', 'Point 3 and discussion 3. Such as: falls from the roof, ladder or scaffolding; scaffold collapse; an unstable stack falling; tools or materials falling on people below.'),
           ('overhead-electrical-cables', 'Overhead electrical cables', 'Overhead electrical cables (3 for point, 3 for discussion)', 'Point 3 and discussion 3. Such as: electricity arcing to anyone close by; contact lethal even at 230 V; current through damp wood or plastic; high plant such as excavators and cranes at particular risk.'),
           ('on-site-health-hygiene', 'On-site health & hygiene', 'On-site health & hygiene (3 for point, 3 for discussion)', 'Point 3 and discussion 3. Such as: cross-contamination of bacteria and viruses between workers; disease from animals, vermin or contaminated water; eating in an unhealthy environment.')]
b2 = [add('2', f'b-{slug}', f'(b) — {slug}', f'{T2B} — {heading}', [row('risk', verbatim, 6, note)], *SAFE, None,
          'Safety precautions on site (1.8).', B2, S2) for slug, heading, verbatim, note in ITEMS2B]
B2b = compose('2', 'b', '(b)', b2, None, B2, S2, T2B, labels=[x[1] for x in ITEMS2B])
T2C = 'Using notes and freehand sketches, outline two specific safety procedures that should be observed to eliminate each risk identified at 2(b) above.'
C2 = add('2', 'c', '(c)', T2C,
         [row('chimney', 'Repairing a chimney stack', 8, 'Two procedures, each 2 for note and 2 for sketch. Such as: scaffolding around the stack, erected by certified people, with hand rails, mid rails and toe boards and tied to the house.'),
          row('cables', 'Overhead electrical cable', 8, 'Two procedures, each 2 for note and 2 for sketch. Such as: bunting 6–10 m either side of the cable at 3–4.2 m high; crossing points for machinery; ground-level guard rails; warning signs every 20 m; supervised plant movement; ESB emergency contact.'),
          row('hygiene', 'On-site health & hygiene', 8, 'Two procedures, each 2 for note and 2 for sketch. Such as: drinking water and washing facilities; ventilated, regularly cleaned welfare facilities; masks and distancing; disinfecting shared tools and surfaces; hand hygiene and signage.')],
         *SAFE, 'q2-procedures', 'Safety precautions on site (1.8).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-procedures', B2, S2, parts(('a', T2A), ('b', T2B), ('c', T2C)))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p33 (printed 31): (a) three considerations × (3 + 3) = 18; (b) layout 15, three considerations 4 each, justification 3 = 30; (c) two advantages and two disadvantages × 3 = 12. Complete 60.'
S3 = 'Considerations and layouts are open responses. Part (c) requires both two advantages and two disadvantages, separately marked: two required tasks composed into (c).'
T3A = 'Discuss in detail, three design considerations that should be taken into account in the design of this home office space to enhance health and wellbeing.'
T3B = 'Using notes and freehand sketches, show a proposed design layout for the office space that incorporates each of the design considerations you outlined at 3(a) above. Justify your design choices.'
T3C = 'Discuss two advantages and two disadvantages of working from a home office.'
OFFICE = (['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'])
A3 = add('3', 'a', '(a)', T3A,
         [row(f'consideration-{i}', f'Design consideration {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: visual comfort — daylight through the day, a connection with nature, good artificial light, little glare.'),
             (2, 'A second, different consideration. Such as: thermal comfort — a steady temperature, fresh air, passive heating and user controls.'),
             (3, 'A third, different consideration. Such as: ergonomic comfort and storage; flexibility; acoustic comfort; services such as sockets and internet points.')]],
         *OFFICE, None, 'Layout design of the built environment (1.2) for good illumination (7.4).', B3, S3)
B3b = add('3', 'b', '(b)', T3B,
          [row('layout', 'Design layout for home office space', 15, 'A freehand layout of the office (no more than 18 m²) at the rear of the house, as in the scheme’s model sketches.'),
           row('consideration-1', 'Design Consideration 1', 4, 'The first consideration shown in the layout, such as glazing to the sun path and garden, ceiling and desk lights, solar shading.'),
           row('consideration-2', 'Design Consideration 2', 4, 'The second consideration shown, such as triple glazing, south glazing for passive gains, thermostats, insulation and cross ventilation.'),
           row('consideration-3', 'Design Consideration 3', 4, 'The third consideration shown, such as MVHR, space for furniture and storage, or sound insulation and good doors and windows.'),
           row('justification', 'Justification', 3, 'The design choices justified.')],
          *OFFICE, 'q3-layout', 'Layout design of the built environment (1.2) for good illumination (7.4).', B3, S3)
c3 = [add('3', f'c-{kind}s', f'(c) — {kind}s', f'Discuss two {kind}s of working from a home office.',
          [row(f'{kind}-1', f'{kind.capitalize()} 1', 3, n1), row(f'{kind}-2', f'{kind.capitalize()} 2', 3, n2)],
          ['cons-1-2'], ['planning-sustainability-environment'], None, 'The built environment (1.2).', B3, S3)
      for kind, n1, n2 in [('advantage', 'Such as: no commute and more free time; no transport costs.', 'A second, different advantage. Such as: more productivity and flexibility; a better work-life balance; fewer distractions.'),
                           ('disadvantage', 'Such as: no social contact with colleagues; loneliness and isolation.', 'A second, different disadvantage. Such as: distractions at home; being overlooked; always being available.')]]
C3 = compose('3', 'c', '(c)', c3, None, B3, S3, T3C, labels=['Advantages', 'Disadvantages'])
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-layout', B3, S3, parts(('a', T3A), ('b', T3B), ('c', T3C)))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p34 (printed 32): (a) three factors × (notes 4 + sketches 4) = 24; (b) three considerations × 4 = 12; (c) sketch 4, house location, orientation, road entrance and driveway 4 each, justification 4 = 24. Complete 60.'
S4 = 'All three printed factors in (a) are required, each separately marked. "Select your preferred site A or B" in (b) is one task: the scheme marks the three considerations alike for either site.'
SITE = (['cons-1-3'], ['planning-sustainability-environment'])
T4A = 'Using notes and freehand sketches, discuss in detail each of the following factors when selecting a site for a new house in a rural setting: availability of services; existing trees and hedgerows; site topography.'
ITEMS4 = [('availability-of-services', 'Availability of services', 'q4-services', 'Such as: rural sites usually have power and telecommunications but may lack mains water, gas or sewerage; the cost of bringing services to the boundary can be substantial.'),
          ('existing-trees-and-hedgerows', 'Existing trees and hedgerows', 'q4-trees', 'Such as: a natural sound buffer and privacy; wellbeing and wildlife kept; natural integration into the countryside; removing large trees may affect settlement.'),
          ('site-topography', 'Site topography', 'q4-topography', 'Such as: use natural shelter from contours and trees; do not break the skyline; avoid cutting and filling; check for flooding.')]
a4 = [add('4', f'a-{slug}', f'(a) — {slug}', f'{T4A} — {heading}',
          [row('factor', heading, 8, 'Notes 4 and sketches 4. ' + note)],
          *SITE, figure, 'Choosing a site (1.3).', B4, S4) for slug, heading, figure, note in ITEMS4]
A4 = compose('4', 'a', '(a)', a4, 'q4-factors', B4, S4, T4A, labels=[x[1] for x in ITEMS4])
T4B = 'Shown is an extract from a site location map. A and B are possible sites for a new house in a rural setting. Select your preferred site A or B and discuss three considerations you took into account when selecting your site.'
B4b = add('4', 'b', '(b)', T4B,
          [row(f'consideration-{i}', f'Consideration {i}', 4, note) for i, note in [
              (1, 'Such as, site A: away from the main road with less noise and more privacy, no houses overlooking it.'),
              (2, 'A second, different consideration. Such as, site A: the lane joins the main road on a straight for clear sight lines; site B: services close by from the neighbouring house.'),
              (3, 'A third, different consideration. Such as, site A: natural hedgerows and views of the lake and forest; site B: favoured by planning beside an existing dwelling, close to schools and facilities, room for wastewater treatment.')]],
          *SITE, 'q4-sites', 'Choosing a site (1.3).', B4, S4)
T4C = 'Draw a well-proportioned sketch of your selected site and the immediate boundaries. On your sketch, show a preferred: location and orientation of a house on the site; layout of the road entrance and the driveway to the house. For each of the above, justify your design choice.'
C4 = add('4', 'c', '(c)', T4C,
         [row('sketch', 'Sketch of selected site', 4, 'A well-proportioned sketch of the selected site and its boundaries.'),
          row('items', 'Sketch site showing: house location, orientation, road entrance & driveway', 16, 'House location, orientation, road entrance and driveway, 4 each. Such as: the largest perimeter facing south, set back from the road; a short driveway; the entrance set back 5 m with walls splayed at 45° for clear vision.'),
          row('justification', 'Justification', 4, 'The design choices justified, such as solar gain, privacy, safe sight lines and less hard surface.')],
         ['cons-1-3', 'cons-6-4'], ['planning-sustainability-environment'], 'q4-site-plans', 'Site layout (1.3) for solar gain (6.4).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-site-plans', B4, S4, parts(('a', T4A), ('b', T4B), ('c', T4C)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p35 (printed 33): (a) eight resistances, total resistance and U-value, 10 × 3 = 30; (b) five steps × 3 = 15; (c) notes/discussion 8 + sketch 7 = 15. Complete 60.'
S5 = 'No printed choice. Part (b) uses the U-value from (a).'
DATA5 = ('External brick thickness 100 mm; clear cavity width 50 mm; orientated strand board (OSB) thickness 9 mm; timber stud thickness 175 mm; cellulose insulation between studs thickness 175 mm; '
         'orientated strand board (OSB) thickness 9 mm; plasterboard thickness 12.5 mm.\n'
         'Thermal data of the external wall: resistance of external surface (R) 0.048 m2 ⁰C/W; resistivity of external brick (r) 1.300 m ⁰C/W; resistance of clear cavity (R) 0.440 m2 ⁰C/W; '
         'conductivity of OSB (k) 0.130 W/m ⁰C; conductivity of cellulose insulation (k) 0.039 W/m ⁰C; conductivity of OSB (k) 0.130 W/m ⁰C; conductivity of plasterboard (k) 0.250 W/m ⁰C; '
         'resistance of internal surface (R) 0.130 m2 ⁰C/W. Note: The timber studs need not be considered in your calculations.')
T5A = 'Calculate the U-value of the wall, given the construction has the following sequence and data: ' + DATA5
T5B = 'It is proposed to redesign the above timber frame wall and upgrade its thermal properties to meet the Passive House standard by adding sheep wool insulation to the design of the internal leaf. Given the thermal conductivity (k) of sheep wool insulation as 0.034 W/m ⁰C, calculate the thickness of additional insulation required to achieve a U-value of 0.15 W/m2 ⁰C.'
T5C = 'Using notes and freehand sketches, discuss why a moisture control layer and a vapour control layer need to be incorporated into timber frame construction.'
A5 = add('5', 'a', '(a)', T5A,
         [row('resistances', 'Formulae: R=T/k R=T × r', 24, 'Eight resistances, 3 each, by R = T/k (or R = T × r for the brick): external surface 0.048 (given); brick 0.1 × 1.300 = 0.130; cavity 0.440 (given); OSB 0.009/0.130 = 0.069; cellulose 0.175/0.039 = 4.487; OSB 0.069; plasterboard 0.0125/0.25 = 0.050; internal surface 0.130 (given). All in m²°C/W.', list(range(0, 25, 3))),
          row('total-resistance', 'Total resistance', 3, 'Total resistance Rt = 5.424 m²°C/W.', [0, 3]),
          row('u-value', 'Calculation of U-value (w/m2 °c or w/m2k)', 3, 'U = 1 ÷ Rt = 1 ÷ 5.424 = 0.184 W/m²°C, with units.', [0, 3])],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Thermal resistance, conductivity and transmittance (6.1).', B5, S5)
B5b = add('5', 'b', '(b)', T5B,
          [row('required-resistance', 'Resistance for U- value for 0.15 W/m2 °c (using R=1/U)', 3, 'Required resistance = 1 ÷ 0.15 = 6.666 m²°C/W.'),
           row('existing-resistance', 'Resistance from calculated U-value from part (a)', 3, 'Resistance of the wall from (a) = 1 ÷ 0.184 = 5.424 m²°C/W.'),
           row('difference', 'Difference in resistances (required resistance)', 3, 'Difference = 6.666 − 5.424 = 1.243 m²°C/W.'),
           row('formula', 'Application of formula R = T/k', 3, '1.243 = T ÷ 0.034, so T = 0.04226 metres.'),
           row('thickness', 'Required thickness of insulation in mm.', 3, 'Additional sheep wool = 42 mm (42 or 43 mm accepted). Alternative calculation methods are acceptable.')],
          ['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation'], 'q5-calculation',
          'Thermal resistance and transmittance (6.1) of added insulation (6.2).', B5, S5)
C5 = add('5', 'c', '(c)', T5C,
         [row('notes', 'Notes / discussion', 8, 'Such as: a breather membrane on the outer side of the frame lets vapour escape while repelling water, its joints taped; a vapour control layer on the inner side limits warm, moist air reaching cold surfaces in the wall, preventing condensation, moisture damage and rot; it must be continuous and sealed at all laps.'),
          row('sketch', 'Sketch', 7, 'Freehand sketch of the timber-frame wall showing the breather membrane and the vapour control layer.')],
         ['cons-6-6', 'cons-3-3'], ['condensation-air-tightness', 'walls'], 'q5-layers', 'Vapour control and condensation (6.6) in a timber-frame wall (3.3).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p36 (printed 34): (a) three features × (notes 5 + sketches 5) = 30; (b) two added features × (notes 5 + sketches 5) = 20; (c) two advantages × (2 + 3) = 10. Complete 60.'
S6 = 'Features, added features and advantages are open responses with no printed list; the scheme lists typical examples.'
T6A = 'With reference to the design shown, discuss using notes and freehand sketches, three features of the design that contribute to the house having a low environmental impact.'
T6B = 'Operational energy use is an important consideration in designing for low environmental impact. Using notes and freehand sketches, discuss two features that could be added to the house that would further reduce its energy use.'
T6C = 'Discuss in detail two advantages of designing a house that will have a low operational energy use when the house is built.'
A6 = add('6', 'a', '(a)', T6A,
         [row(f'feature-{i}', f'Design Feature {i}', 10, note) for i, note in [
             (1, 'Notes 5 and sketches 5. Such as: local timber frame with lower embodied energy and carbon; FSC cedar cladding.'),
             (2, 'A second, different feature. Such as: a one-room-deep plan lit and warmed from both sides; high insulation.'),
             (3, 'A third, different feature. Such as: no chimney, so better airtightness; a renewable heat source; a simple compact form.')]],
         ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-low-impact',
         'Low-impact design of the built environment (1.2), solar gain (6.4) and insulation (6.2).', B6, S6)
B6b = add('6', 'b', '(b)', T6B,
          [row(f'feature-{i}', f'Feature {i}', 10, note) for i, note in [
              (1, 'Notes 5 and sketches 5. Such as: photovoltaic panels on a south-facing roof; evacuated tubes for hot water; mechanical ventilation with heat recovery.'),
              (2, 'A second, different feature. Such as: an air-to-water heat pump; triple-glazed, thermally broken windows; an insulated service cavity.')]],
          ['cons-6-3', 'cons-5-8', 'cons-5-3'], ['heat-loss-insulation', 'services-water-gas-electricity', 'hot-water-space-heating'], 'q6-features',
          'Reducing operational energy (6.3) through renewable electricity (5.8) and efficient heating (5.3).', B6, S6)
C6 = add('6', 'c', '(c)', T6C,
         [row(f'advantage-{i}', f'Advantage {i} (2 for point, 3 for discussion)', 5, note) for i, note in [
             (1, 'Point 2 and discussion 3. Such as: less energy used, benefiting the environment and ecosystems.'),
             (2, 'A second, different advantage. Such as: lower running costs; less exposure to pollution; fewer finite resources consumed.')]],
         ['cons-6-3', 'cons-1-2'], ['heat-loss-insulation', 'sustainability-the-environment'], None,
         'Running costs (6.3) and the sustainable built environment (1.2).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-low-impact', B6, S6, parts(('a', T6A), ('b', T6B), ('c', T6C)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p37 (printed 35): (a) chimney stack best four × 5, roofing best four × 5 (4 for drawing, 1 for annotation), three courses of slates 6, scale 4 + drafting 4 banded 8/6/4 = 54; (b) two design details × 3 = 6. Complete 60.'
S7 = 'One required section and two required moisture details. The detail lists are marking menus, not printed choices.'
T7A = 'To a scale of 1:5, draw a vertical section through the centre of the chimney stack and roof structure. The section should show the typical construction details through the chimney stack, flue liner, chimney capping and portion of the roof structure. On your drawing include three courses of slate at each side of the chimney stack.'
T7B = 'On your drawing, show two typical design details to prevent the penetration of moisture at the junction of the roof and chimney stack.'
A7 = add('7', 'a', '(a)', T7A,
         [row('chimney', 'Chimney stack', 20, 'Best four details, 5 each (4 for drawing, 1 for annotation). Marking menu: chimney blockwork; external render; flue liners; lime-sand fill or vermiculite; concrete chimney capping; DPC beneath the capping; lead flashing; DPC at roof level.'),
          row('roofing', 'Roofing', 20, 'Best four details, 5 each. Marking menu: rafters 200 × 50 mm at 400 mm centres; chimney trimmer 200 × 50 mm; windtight OSB layer; breather membrane; counter battens; slating battens; apron lead flashing.'),
          row('slates', 'Three courses of slates on each side', 6, 'Three courses of slates shown on each side of the stack.'),
          row('presentation', 'Scale - 4 marks Drafting - 4 marks', 8, 'Scale 4 and drafting 4, assessed together: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-5-7', 'cons-3-9', 'cons-3-8'], ['question-1-drawing-questions', 'fireplaces-fire-prevention', 'roofs'], 'q7-section',
         'Scaled drawing (1.5) of a chimney stack and flue (5.7) through a slated (3.9) cut roof (3.8).', B7, S7)
B7b = add('7', 'b', '(b)', T7B,
          [row('detail-1', 'Design detail 1', 3, 'Such as: a DPC at roof level through the stack.'),
           row('detail-2', 'Design detail 2', 3, 'A second, different detail. Such as: lead flashings (cover and apron) at the junction.')],
          ['cons-3-4', 'cons-5-7'], ['walls', 'fireplaces-fire-prevention'], 'q7-section', 'Damp proof courses (3.4) at a chimney stack (5.7).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p38 (printed 36): (a) best seven of fifteen components × 4 (3 for drawing, 1 for annotation) = 28 and typical pipe sizes (any two) 4 = 32; (b) two features × (notes/discussion 5 + sketches 5) = 20; (c) two advantages × (2 + 2) = 8. Complete 60.'
S8 = 'The two zones and three radiators per floor are required content of one layout, not a choice. The efficiency features are open choices.'
T8A = 'Using notes and a single-line diagram, show a typical design layout for both the heating system and hot water system. Show two independently controlled heating zones, one on each floor. Include three radiators on each floor and give the typical sizes of the pipework.'
T8B = 'Using notes and freehand sketches, describe two features that increase the efficiency of the heating system. Discuss the importance of each feature identified.'
T8C = 'Discuss two advantages of installing an Air-to-Water heat pump system in the house as an alternative to the stove.'
A8 = add('8', 'a', '(a)', T8A,
         [row('layout', 'Typical design layout to provide hot water and central heating', 28, 'Best seven components, 4 each (3 for drawing, 1 for annotation): wood-burning stove; radiators on both floors; zone control panel; zone thermostats; cylinder and coil; header/expansion tank; rising main; feed to the expansion tank; cold feed; expansion pipe or vessel; flow and return to the radiators; control valves; pump.'),
          row('sizes', 'Typical sizes of pipework - any two', 4, 'Any two, 2 each. Such as: Ø15 mm rising main; Ø22 mm primary flow and return; Ø15 mm pipes to radiators; Ø22 mm cold feed; Ø28 mm hot water feed or overflow.')],
         ['cons-5-3', 'cons-5-2'], ['hot-water-space-heating'], 'q8-system', 'Heating systems (5.3) and hot water (5.2).', B8, S8)
B8b = add('8', 'b', '(b)', T8B,
          [row(f'feature-{i}', f'Feature {i}', 10, note) for i, note in [
              (1, 'Notes/discussion 5 and sketches 5. Such as: thermostatic radiator valves controlling each radiator; room thermostats switching the heating at a chosen temperature.'),
              (2, 'A second, different feature. Such as: more efficient double-panel or aluminium radiators; time switches and programmers running heating and hot water independently.')]],
          ['cons-5-3'], ['hot-water-space-heating'], 'q8-features', 'Temperature control and heat conservation (5.3).', B8, S8)
C8 = add('8', 'c', '(c)', T8C,
         [row(f'advantage-{i}', f'Advantage {i} (2 for point, 2 for discussion)', 4, note) for i, note in [
             (1, 'Point 2 and discussion 2. Such as: heat taken from the outside air, even at −15 °C, with no fuel burned on site.'),
             (2, 'A second, different advantage. Such as: very efficient heating and hot water; a low carbon footprint; easily installed or retrofitted.')]],
         ['cons-5-3', 'cons-1-2'], ['hot-water-space-heating', 'sustainability-the-environment'], 'q8-heat-pump',
         'Heating systems (5.3) in a sustainable built environment (1.2).', B8, S8)
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-system', B8, S8, parts(('a', T8A), ('b', T8B), ('c', T8C)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p39 (printed 37): (a) three considerations × (3 + 3) = 18; (b) distribution board, three sockets, live, neutral and earth cabling, cable size and colour, each 5 (4 for drawing, 1 for annotation) = 30; (c) two benefits × (3 + 3) = 12. Complete 60.'
S9 = 'The distribution board and three sockets are required content of one layout, not a choice.'
T9A = 'Discuss in detail, three considerations when designing the layout for sockets in the electrical system of a domestic house.'
T9B = 'Using notes and freehand sketches, show the design of a typical wiring layout for a ring main circuit to include: distribution board; three electrical sockets. Indicate the typical sizes and colour coding of the electrical cables.'
T9C = 'The current Building Regulations require all new houses to have a renewable energy ratio (RER) of 20%. Discuss two benefits for the homeowner of generating their own electricity by using micro-generation to help meet this energy requirement.'
A9 = add('9', 'a', '(a)', T9A,
         [row(f'consideration-{i}', f'Consideration {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: the position and number of sockets for each room’s function now and in future; heights of 900–1200 mm; visible, easy to reach and operate one-handed.'),
             (2, 'A second, different consideration. Such as: safety — sockets to current standards, correctly sized cable, MCB and RCD protection, correct earthing.'),
             (3, 'A third, different consideration. Such as: an accessible distribution board with cable routes to the sockets; conduit installed in the building fabric.')]],
         ['cons-5-8'], ['services-water-gas-electricity'], None, 'Domestic electrical installation (5.8).', B9, S9)
B9b = add('9', 'b', '(b)', T9B,
          [row('board', 'Distribution board', 5, 'The distribution board shown (4 for drawing, 1 for annotation).'),
           row('sockets', 'Three sockets', 5, 'Three sockets on the ring (4 for drawing, 1 for annotation).'),
           row('cabling', 'Live cabling Neutral cabling Earth cabling', 15, 'Live, neutral and earth cabling, 5 each, forming the ring from the board through the sockets and back.'),
           row('size-colour', 'Cable size (2) and colour (3)', 5, 'Size 2 and colour 3: 2.5 mm² cable; live brown (red), neutral blue, earth green and yellow.')],
          ['cons-5-8'], ['services-water-gas-electricity'], 'q9-ring-main', 'Domestic electrical circuits (5.8).', B9, S9)
C9 = add('9', 'c', '(c)', T9C,
         [row(f'benefit-{i}', f'Benefit {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: lower electricity bills; a smaller household carbon footprint.'),
             (2, 'A second, different benefit. Such as: excess electricity sold to the national grid; less reliance on grid electricity and fossil fuels.')]],
         ['cons-5-8', 'cons-1-2'], ['services-water-gas-electricity', 'sustainability-the-environment'], None,
         'Domestic electricity (5.8) from renewable sources (1.2).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-ring-main', B9, S9, parts(('a', T9A), ('b', T9B), ('c', T9C)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p40 (printed 38): (a) two reasons and two effects × (3 + 3) = 24; (b) two methods × (notes 6 + sketches 6) = 24; (c) two features × (notes 3 + sketches 3) = 12. Complete 60.'
S10 = 'No printed choice. The OR alternative is a separate Question 10 route.'
T10A = 'Discuss two reasons why solar overheating may occur in the house shown and discuss two effects solar overheating may have on occupants.'
T10B = 'Using notes and freehand sketches, suggest two ways to reduce the possibility of solar overheating while being sympathetic to the design of this house.'
T10C = 'Using notes and freehand sketches, discuss two features of the given house design that contribute to the house responding to its rural setting.'
A10 = add('10', 'a', '(a)', T10A,
          [row('reason-1', 'Reason 1 for overheating (3 for point, 3 for discussion)', 6, 'Point 3 and discussion 3. Such as: large south-facing glazing gathering high solar gain; no shading such as overhangs or brise-soleil.'),
           row('reason-2', 'Reason 2 for overheating (3 for point, 3 for discussion)', 6, 'A second, different reason. Such as: too little ventilation in an airtight house; little thermal mass; high insulation and triple glazing retaining heat; heat from occupants and appliances.'),
           row('effect-1', 'Effect 1 on occupants (3 for point, 3 for discussion)', 6, 'Point 3 and discussion 3. Such as: discomfort in an overly warm room; dehydration causing headaches and lethargy.'),
           row('effect-2', 'Effect 2 on occupants (3 for point, 3 for discussion)', 6, 'A second, different effect. Such as: exhaustion; irritability; poor sleep.')],
          ['cons-6-4', 'cons-6-5'], ['passive-design'], None, 'Solar heat gain (6.4) and human comfort (6.5).', B10, S10)
B10b = add('10', 'b', '(b)', T10B,
           [row(f'method-{i}', f'Method {i}', 12, note) for i, note in [
               (1, 'Notes 6 and sketches 6. Such as: an extended roof overhang or a surround around the largest opening; a louvred brise-soleil in matching materials; shutters inspired by vernacular features.'),
               (2, 'A second, different method: notes 6 and sketches 6. Such as: thermal mass such as polished concrete floors; deciduous trees or a pergola with vines; dynamic electrochromic glass.')]],
           ['cons-6-4'], ['passive-design'], 'q10-shading', 'Controlling solar heat gain (6.4).', B10, S10)
C10 = add('10', 'c', '(c)', T10C,
          [row(f'feature-{i}', f'Feature {i}', 6, note) for i, note in [
              (1, 'Notes 3 and sketches 3. Such as: a dome-shaped roof like a hay barn; corrugated metal cladding recalling agricultural buildings.'),
              (2, 'A second, different feature. Such as: a narrow, one-room-deep longhouse plan; a white rendered base like lime render; the house nestled into the landscape.')]],
          ['cons-1-1', 'cons-1-2'], ['conservation-restoration'], 'q10-setting', 'Vernacular character (1.1) in its rural setting (1.2).', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-shading', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p41 (printed 39): (a) three discussion points × (4 + 6) = 30; (b) three guidelines × (4 + 6) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the overheating question. Its parts are open responses.'
TAA = 'Discuss the above statement in detail.'
TAB = 'Propose three best practice guidelines that would promote the reuse or repurposing of some existing buildings in Ireland.'
REUSE = (['cons-1-1', 'cons-1-2'], ['conservation-restoration'])
AA = add('10', 'a', '(a)', TAA,
         [row(f'point-{i}', f'Discussion Point {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: reuse reduces the demand for new housing while preserving the vernacular design of the area.'),
             (2, 'Point 4 and discussion 6. Such as: historic buildings give villages and towns their distinctive character and sense of place.'),
             (3, 'Point 4 and discussion 6. Such as: remodelling to meet today’s needs rather than letting buildings fall into disuse; land shortages, planning delays and housing demand. Three distinct, well-argued points are needed.')]],
         *REUSE, None, 'Conserving historic buildings (1.1) in the built environment (1.2).', BALT, SALT, alt=True)
AB = add('10', 'b', '(b)', TAB,
         [row(f'guideline-{i}', f'Guideline {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: government and local authority support, with faster planning for reuse projects and exemplars promoted.'),
             (2, 'Point 4 and discussion 6. Such as: substantial grants for refurbishing heritage buildings; traditional skills and local materials kept alive.'),
             (3, 'Point 4 and discussion 6. Such as: clear local planning guidelines for sustainable repurposing; minimal intervention, with new additions distinguishable from the original. Three distinct guidelines are needed.')]],
         *REUSE, None, 'Conserving historic buildings (1.1) in the built environment (1.2).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, parts(('a', TAA), ('b', TAB)), alt=True)

LEDGER = [
    (1, 'Answer any', 'Whole-exam selection: any four of the ten questions (240 marks); all question banks retained, no full-exam Cartesian cards.'),
    (3, 'Select', 'Q4(b) select site A or B: one task, the scheme marking the three considerations alike for either site.'),
    (3, 'or', 'Q4(b) "site A or B": the same site selection, marked alike, not a separate route.'),
    (7, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.'),
    (7, 'or', 'Alternative Question 10 part (b) wording ("reuse or repurposing"), not an answer selection.'),
]
REASONS = {
    'q1-a': 'Rows rebuilt to the printed table, with the scale and drafting allowance (8, banded 8/6/4) it prints: 48 → 56.',
    'q1-b': 'Reshaped to the printed criterion row; tariff unchanged (4).',
    'q2-a-safety-training': 'Reshaped to the printed 3 point + 3 discussion row; tariff unchanged (6).',
    'q2-a-personal-protective-equipment-ppe': 'Reshaped to the printed 3 point + 3 discussion row; tariff unchanged (6).',
    'q2-a-vigilance': 'Reshaped to the printed 3 point + 3 discussion row; tariff unchanged (6).',
    'q2-b-repairing-a-chimney-stack': 'Reshaped to the printed 3 point + 3 discussion row; tariff unchanged (6).',
    'q2-b-overhead-electrical-cables': 'Reshaped to the printed 3 point + 3 discussion row; tariff unchanged (6).',
    'q2-b-on-site-health-hygiene': 'Reshaped to the printed 3 point + 3 discussion row; tariff unchanged (6).',
    'q2-c': 'Reshaped to one row per risk, each two procedures at 2 for note + 2 for sketch; tariff unchanged (24).',
    'q3-a': 'Split into the three printed considerations (3 + 3 each); tariff unchanged (18).',
    'q3-b': 'Rebuilt to the printed rows — layout 15, three considerations 4 each, justification 3: 12 → 30.',
    'q3-c-advantages': 'Split into the two printed advantages (3 each); tariff unchanged (6).',
    'q3-c-disadvantages': 'Split into the two printed disadvantages (3 each); tariff unchanged (6).',
    'q4-a-availability-of-services': 'Reshaped to the printed factor row (notes 4 + sketches 4); tariff unchanged (8).',
    'q4-a-existing-trees-and-hedgerows': 'Reshaped to the printed factor row (notes 4 + sketches 4); tariff unchanged (8).',
    'q4-a-site-topography': 'Reshaped to the printed factor row (notes 4 + sketches 4); tariff unchanged (8).',
    'q4-b': 'Replaces a pool of scheme bullets from both sites with the three printed considerations, marked alike for either site; tariff unchanged (12).',
    'q4-c': 'Rebuilt to the printed rows — site sketch 4, house location, orientation, road entrance and driveway 4 each, justification 4; tariff unchanged (24).',
    'q5-b': 'Reshaped to the five printed calculation steps (3 each) with the scheme’s worked answer (42 mm); tariff unchanged (15).',
    'q6-a': 'Split into three design features, each notes 5 + sketches 5; tariff unchanged (30).',
    'q6-b': 'Split into two added features, each notes 5 + sketches 5; tariff unchanged (20).',
    'q6-c': 'Split into the two printed advantages (2 for point + 3 for discussion); tariff unchanged (10).',
    'q7-a': 'Adds the printed three courses of slates (6) and scale and drafting allowance (8, banded 8/6/4) to the chimney and roofing details: 40 → 54.',
    'q7-b': 'Split into the two printed design details (3 each); tariff unchanged (6).',
    'q8-a': 'Adds the printed typical pipe sizes (any two, 4) to the best-seven components: 28 → 32.',
    'q8-b': 'Split into two features, each notes/discussion 5 + sketches 5; tariff unchanged (20).',
    'q8-c': 'Split into the two printed advantages (2 + 2 each); tariff unchanged (8).',
    'q9-a': 'Split into the three printed considerations (3 + 3 each); tariff unchanged (18).',
    'q9-b': 'Rebuilt to the printed rows — distribution board, three sockets, live/neutral/earth cabling and cable size and colour, 5 each; tariff unchanged (30).',
    'q9-c': 'Split into the two printed benefits (3 + 3 each); tariff unchanged (12).',
    'q10-a': 'Split into the two printed reasons and two effects (3 + 3 each); tariff unchanged (24).',
    'q10-b': 'Split into two methods, each notes 6 + sketches 6; tariff unchanged (24).',
    'q10-c': 'Split into two features, each notes 3 + sketches 3; tariff unchanged (12).',
}
D.finish(LEDGER, {}, REASONS, marked_alike={'4b': dict(options=['site A', 'site B'], cardId=B4b['id'])})
