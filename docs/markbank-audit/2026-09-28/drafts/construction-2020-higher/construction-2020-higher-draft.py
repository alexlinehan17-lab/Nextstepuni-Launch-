"""Draft the 2020 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 32-42). There is no closed choice on this paper. The 28 pre-audit 2020 Higher cards keep
their IDs and concept IDs and are corrected in place. Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Cut roof and externally insulated wall section', concept='cut-roof-section',
              stem='The sketch shows a dwelling house with a traditional slated cut roof. The roof has a pitch of 30⁰ and flush eaves as shown. The internal span of the house is 6.0 metres and the roof is highly insulated. The external wall of the house is a 215 mm single leaf wall of solid concrete block construction with 200 mm external insulation and acrylic render external finish. Insulated plasterboard is fixed to the underside of the ceiling joists. A 50 mm service cavity is also provided at the internal surface of the wall.',
              note='Original sketch and specification retained. Construction, dimension and scale/drafting marks belong to part (a); the ventilation detail in (b) is marked separately.'),
    '2': dict(page=2, title='Scaffolding and the Health and Safety Officer', concept='scaffolding-safety', stem='',
              note='Original question retained. All three printed activities in (a) are required, each with two guidelines.'),
    '3': dict(page=3, title='Adapting a bungalow for limited mobility and open-plan living', concept='bungalow-adaptation',
              stem='The drawing shows the floor plan and front elevation of a semi-detached bungalow. The internal wall A-A is load-bearing. The rear wall of the house is south facing. The owners intend to modify the internal layout to: make it fit for use by a person with limited mobility; create a bright open-plan kitchen/living space.',
              note='Original plan and elevation retained. Considerations and layouts are open responses; the scheme gives a model layout. Part (c) requires both two advantages and two disadvantages, separately marked.'),
    '4': dict(page=3, title='A new house on a vacant urban site', concept='urban-infill-house',
              stem='The sketch shows a vacant site located between two existing dwellings in an urban area. The owners are at the design stage for a new house to be built on this site. It is proposed that the characteristics of existing dwellings should have an influence on the external house design.',
              note='Original sketch retained. All three printed characteristics in (a) are required, each separately marked.'),
    '5': dict(page=4, title='Ground floor U-value, heat-loss cost and thermal bridge', concept='ground-floor-u-value',
              stem='A house built to nZEB standards has a highly insulated solid concrete ground floor with a hardwood finish, as shown.',
              note='All printed data are retained in the original question. Part (b) uses the U-value from (a); the scheme’s worked answers are U = 0.10 W/m²°C and an annual cost of €18.62.'),
    '6': dict(page=5, title='A retrofitted and extended vernacular cottage', concept='retrofit-vernacular-cottage',
              stem='The elevation and ground floor plan of an Irish vernacular cottage, which has been retrofitted and extended, are shown. The existing cottage has been upgraded to meet EnerPHit Passive House standard. The new extension on the right has two bedrooms and a bathroom upstairs. The external walls of the extension are of timber frame construction with an external corrugated metal cladding finish. The house is designed to have low environmental impact.',
              note='Original elevation and plan retained. Part (a) requires both two advantages and two disadvantages, separately marked.'),
    '7': dict(page=5, title='Stove, hearth and chimney section', concept='stove-hearth-section',
              stem='Space heating is provided in a family living area by a wood-burning stove inset into a chimney breast, as shown. The chimney has been constructed to accommodate the stove and is located on a 200 mm internal solid concrete block wall. A 150 mm diameter cast iron flue connects the stove to the chimney flue. The living area has an insulated solid concrete ground floor with a 20 mm hardwood finish. The dimensions of the stove are: height 600 mm, width 550 mm, depth 400 mm.',
              note='Original sketch and specification retained. Construction, dimension and scale/drafting marks belong to part (a); the air-supply detail in (b) is marked separately.'),
    '8': dict(page=6, title='First-floor bathroom and above-ground drainage', concept='bathroom-drainage',
              stem='The main bathroom located on the first floor of a dwelling house is shown.',
              note='Original sketch retained. All four printed fittings in (b) are required content of one layout, not a choice.'),
    '9': dict(page=6, title='Sound insulation for an upstairs entertainment room', concept='sound-insulation-upgrade',
              stem='The owners have decided to convert an upstairs room into a family entertainment room. They are concerned that the sound from this room will be heard in the adjoining rooms upstairs and in the kitchen beneath.',
              note='Original question retained. All three printed principles in (a) are required, each separately marked; (b) requires both the partition and the floor.'),
    '10': dict(page=7, title='Designing an MVHR system', concept='mvhr-design',
               stem='The drawing shows the draft design of the ground floor plan of a new dwelling house. The homeowners propose to install a Mechanical Ventilation with Heat Recovery (MVHR) system into their new home.',
               note='Original plan retained. Considerations and advantages are open responses; the scheme gives a model layout.'),
}
ALT = dict(page=7, title='Retrofitting buildings for energy efficiency (alternative Question 10)', concept='retrofit-energy-efficiency',
           stem='“Worldwide, buildings are responsible for over 40% of the total primary energy use and related greenhouse emissions. Through standards and energy efficiency programs, several countries have succeeded in improving the energy performance of new and existing buildings. Designing and retrofitting electrical power systems to be energy efficient have been primary components in the effort to reduce energy consumption by the built environment.” Adapted from: Optimal Design and Retrofit of Energy Efficient Buildings, Communities, and Urban Centers. by Moncef Krarti. Published by: Butterworth-Heinemann. ISBN: 978-0-12-849869-9',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the MVHR question.')
SCHEME_PAGES = {'1': [4, 5, 32], '2': [6, 7, 8, 33], '3': [9, 10, 11, 34], '4': [12, 13, 14, 35], '5': [15, 16, 36], '6': [17, 18, 19, 20, 37],
                '7': [21, 38], '8': [22, 23, 39], '9': [24, 25, 26, 40], '10': [27, 28, 41], '10-alt': [29, 30, 42]}
D = cp.Draft(HERE, 2020, 'higher', ('22c84780da2ac7b0b034506068b6b35804d9b522dfffc51a340b0c80b5c006c5',
                                    '74eaba480cdb9437c28084ac9707fc46bda4ba0fa321d275ce98fe9f8523ac8d'), 28, QUESTIONS, SCHEME_PAGES, alt=ALT)
row, add, compose, parts = D.row, D.add, D.compose, D.parts
BAND8 = [0, 4, 6, 8]
D.figures({
    'q1-original': D.paper(2, [45, 53, 580, 455]), 'q2-original': D.paper(2, [45, 455, 580, 695]),
    'q3-original': D.paper(3, [45, 53, 580, 422]), 'q4-original': D.paper(3, [45, 422, 580, 760]),
    'q5-original': D.paper(4, [45, 53, 580, 712]), 'q6-original': D.paper(5, [45, 53, 580, 431]),
    'q7-original': D.paper(5, [45, 431, 580, 745]), 'q8-original': D.paper(6, [45, 53, 580, 395]),
    'q9-original': D.paper(6, [45, 395, 580, 760]), 'q10-original': D.paper(7, [45, 53, 580, 417]),
    'q10-alt-original': D.paper(7, [45, 478, 580, 722]),
    'q1-section': D.composite((4, [51, 51, 550, 745]), (5, [51, 383, 550, 775])),
    'q1-ventilation': D.scheme(5, [51, 51, 550, 383]),
    'q2-scaffolding': D.composite((6, [51, 51, 550, 790]), (7, [51, 51, 550, 775]), (8, [51, 51, 550, 585])),
    'q3-layout': D.composite((9, [51, 455, 550, 762]), (10, [51, 51, 550, 690])),
    'q4-materials': D.scheme(12, [51, 51, 550, 455]), 'q4-shape': D.scheme(12, [51, 455, 550, 775]),
    'q4-streetscape': D.scheme(13, [51, 51, 550, 465]),
    'q4-characteristics': D.composite((12, [51, 51, 550, 775]), (13, [51, 51, 550, 465])),
    'q4-design': D.composite((13, [51, 470, 550, 765]), (14, [51, 51, 550, 605])),
    'q5-calculation': D.composite((15, [51, 51, 550, 735]), (16, [51, 51, 550, 240])),
    'q5-thermal-bridge': D.scheme(16, [51, 240, 550, 565]),
    'q6-low-impact': D.scheme(18, [51, 51, 550, 725]),
    'q6-modifications': D.composite((19, [51, 51, 550, 750]), (20, [51, 51, 550, 530])),
    'q7-section': D.scheme(21, [51, 51, 550, 765]),
    'q8-location': D.scheme(22, [51, 51, 550, 735]), 'q8-pipework': D.scheme(23, [51, 51, 550, 615]),
    'q9-completeness': D.scheme(24, [51, 51, 550, 350]), 'q9-flexibility': D.scheme(24, [51, 350, 550, 532]),
    'q9-isolation': D.scheme(24, [51, 532, 550, 750]), 'q9-principles': D.scheme(24, [51, 51, 550, 750]),
    'q9-upgrades': D.composite((25, [51, 51, 550, 790]), (26, [51, 51, 550, 262])),
    'q10-mvhr': D.scheme(28, [51, 51, 550, 640]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p32 (printed 30): (a) best eleven details × 4 across the external wall, roof structure and eaves = 44, four typical dimensions 4, scale 4 + drafting 4 banded 8/6/4 = 56; (b) ventilation detailing 2 × 2 = 4. Complete 60.'
S1 = 'One required section and one required ventilation detail. The detail lists are marking menus, not printed choices.'
T1A = 'To a scale of 1:10, draw a vertical section through one half of the roof structure from just below eaves up to ridge. Show one external wall and one rafter length. Include the typical construction details from 600 mm below the ceiling joists up to the ridge and include three courses of slate at eaves. Include four typical dimensions of the roof structure.'
T1B = 'On your drawing, show the typical design detailing to ensure ventilation of the roof structure.'
A1 = add('1', 'a', '(a)', T1A,
         [row('details', '11 × 4 marks', 44, 'Best eleven details, 4 each, across three menus. External wall: acrylic render; 200 mm external insulation; 215 mm block on flat; internal plaster/air barrier; insulated service cavity; plasterboard/skim. Roof structure: wallplate 100 × 75; rafter 200 × 50; ceiling joist; purlin 225 × 75; strut; hanger; collar tie; ridgeboard; insulation. Eaves: fascia and gutter; ventilation; breather membrane; slating batten 50 × 30; three courses of slates.'),
          row('dimensions', 'Four typical dimensions (1 × 4 marks)', 4, 'Four typical dimensions of the roof structure, 1 each.'),
          row('presentation', 'Scale - 4 marks Drafting - 4 marks', 8, 'Scale 4 and drafting 4, assessed together: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-3-8', 'cons-3-10', 'cons-3-9', 'cons-3-3'], ['question-1-drawing-questions', 'roofs', 'walls'], 'q1-section',
         'Scaled drawing (1.5) of a cut roof (3.8) at the eaves (3.10) with its covering and insulation (3.9) on an externally insulated wall (3.3).', B1, S1)
B1b = add('1', 'b', '(b)', T1B,
          [row('ventilation', 'Design detailing (2 × 2 marks)', 4, 'Two ventilation details, 2 each, as in the scheme’s model: a fascia ventilator and a proprietary eaves ventilator, with the airflow over the insulation.')],
          ['cons-3-9', 'cons-6-5'], ['roofs', 'wood-rot-ventilation'], 'q1-ventilation', 'Ventilation (6.5) of the roof space and insulation (3.9).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p33 (printed 31): (a) three activities × two guidelines × (3 for note + 4 for sketch) = 42; (b) three responsibilities × (3 + 3) = 18. Complete 60.'
S2 = 'All three printed activities in (a) are required, each with two guidelines; not a choice.'
SAFE = (['cons-1-8'], ['site-safety'])
T2A = 'Discuss in detail, using notes and freehand sketches, two specific best practice guidelines to be observed for each of the following when using scaffolding on a construction site: erecting scaffolding; accessing scaffolding; use of working platforms.'
T2B = 'The on-site Health and Safety Officer performs a key role in maintaining a safe working environment on a construction site. Discuss in detail three responsibilities of a Health and Safety Officer on a construction site.'
A2 = add('2', 'a', '(a)', T2A,
         [row('erecting', 'Erecting scaffolding', 14, 'Two guidelines, each 3 for note and 4 for sketch. Such as: erected only by certified scaffolders with the public excluded; a 3-board platform and guard-rail as it goes up; harnesses clipped to secure anchors; prepared, level ground with 35 × 220 mm sole boards under base plates.'),
          row('accessing', 'Accessing scaffolding', 14, 'Two guidelines, each 3 for note and 4 for sketch. Such as: ladder access towers with self-closing gates; ladders lashed at the top at 4 vertical to 1 horizontal, extending 1 m above the landing; landings no more than 9 m apart; access openings at least 450 × 600 mm.'),
          row('platforms', 'Use of working platforms', 14, 'Two guidelines, each 3 for note and 4 for sketch. Such as: toe-boards at least 150 mm high; guard-rails at least 950 mm with gaps no more than 470 mm; netting and exclusion zones against falling objects; signage.')],
         *SAFE, 'q2-scaffolding', 'Safety precautions on site (1.8).', B2, S2)
B2b = add('2', 'b', '(b)', T2B,
          [row(f'responsibility-{i}', f'Responsibility {i} - (3 for point, 3 for discussion)', 6, note) for i, note in [
              (1, 'Point 3 and discussion 3. Such as: carrying out safety inspections and risk assessments.'),
              (2, 'A second, different responsibility. Such as: reviewing site procedures and the safety statement.'),
              (3, 'A third, different responsibility. Such as: induction training for all new workers; investigating and reporting accidents.')]],
          *SAFE, None, 'Safety precautions on site (1.8).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b], 'q2-scaffolding', B2, S2, parts(('a', T2A), ('b', T2B)))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p34 (printed 32): (a) three considerations × (3 + 3) = 18; (b) revised layout 15, notes for the three considerations 3 each, open-plan kitchen/living 3, justification 3 = 30; (c) two advantages and two disadvantages × 3 = 12. Complete 60.'
S3 = 'Considerations and layouts are open responses. Part (c) requires both two advantages and two disadvantages, separately marked: two required tasks composed into (c).'
ACCESS = (['cons-1-2'], ['planning-sustainability-environment'])
T3A = 'Discuss in detail, three design considerations necessary when modifying the internal layout of the house shown to meet the needs of a person with limited mobility.'
T3B = 'Using notes and freehand sketches, show a revised internal layout that incorporates each of the design considerations you outlined at 3(a) above and include the open-plan kitchen/living space. Justify your choices.'
T3C = 'Discuss two advantages and two disadvantages of open-plan living in a domestic house.'
A3 = add('3', 'a', '(a)', T3A,
         [row(f'consideration-{i}', f'Design consideration {i} - (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: doors — a 300 mm clear space at the leading edge and 800 mm clear internal openings; corridors too narrow.'),
             (2, 'A second, different consideration. Such as: living room and kitchen without an Ø1500 mm turning circle or room between table and units.'),
             (3, 'A third, different consideration. Such as: a bathroom too small, with a bath unsuitable for limited mobility; a bedroom without turning space or en suite.')]],
         *ACCESS, None, 'Accessible layout design of the built environment (1.2).', B3, S3)
B3b = add('3', 'b', '(b)', T3B,
          [row('layout', 'Revised internal layout (meet the needs of a person with limited mobility + open-plan kitchen/living space)', 15, 'A revised layout with the open-plan kitchen/living space, as in the scheme’s model plan.'),
           row('considerations', 'Note for design Consideration 1 Note for design Consideration 2 Note for design Consideration 3', 9, 'Notes for the three considerations, 3 each. Such as: a 1500 mm hallway and 1050–1200 mm corridors; Ø1500–1800 mm turning circles; a 2400 × 2100 mm bathroom with a level-access shower and outward-opening door; 800 mm clear around the bed.'),
           row('open-plan', 'Note for Open-plan kitchen/living space', 3, 'The open-plan kitchen/living space noted, such as bright and to the south.'),
           row('justification', 'Note for justification', 3, 'The choices justified.')],
          *ACCESS, 'q3-layout', 'Accessible layout design of the built environment (1.2).', B3, S3)
c3 = [add('3', f'c-{kind}s', f'(c) — {kind}s', f'Discuss two {kind}s of open-plan living in a domestic house.',
          [row(f'{kind}-1', f'{kind.capitalize()} 1', 3, n1), row(f'{kind}-2', f'{kind.capitalize()} 2', 3, n2)],
          *ACCESS, None, 'Layout design of the built environment (1.2).', B3, S3)
      for kind, n1, n2 in [('advantage', 'Such as: flexibility for lifetime use; daylight and sunlight throughout.', 'A second, different advantage. Such as: more interaction between occupants; ease of movement; better air flow; added value.'),
                           ('disadvantage', 'Such as: a larger volume to heat; less privacy.', 'A second, different disadvantage. Such as: more noise; odours spreading through the space.')]]
C3 = compose('3', 'c', '(c)', c3, None, B3, S3, T3C, labels=['Advantages', 'Disadvantages'])
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-layout', B3, S3, parts(('a', T3A), ('b', T3B), ('c', T3C)))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p35 (printed 33): (a) three characteristics × (notes 4 + sketches 4) = 24; (b) notes 6, sketches 14, justification 4 = 24; (c) two advantages × (3 + 3) = 12. Complete 60.'
S4 = 'All three printed characteristics in (a) are required, each separately marked, so each is its own task and the part composes them; not a choice.'
URBAN = (['cons-1-2', 'cons-1-1'], ['planning-sustainability-environment', 'conservation-restoration'])
T4A = 'Using notes and freehand sketches, discuss the importance of considering each of the following characteristics when designing a house for this site: materials and finishes; shape and form; streetscape.'
ITEMS4 = [('materials-and-finishes', 'Materials and finishes', 'q4-materials', 'Such as: materials already used on neighbouring buildings (brick, render); natural or local materials with less embodied energy; planning guidelines; the street’s palette of doors, windows, walls and roofs.'),
          ('shape-and-form', 'Shape and form', 'q4-shape', 'Such as: the heights, roof profiles and proportions of the existing houses; not overshadowing neighbouring gardens.'),
          ('streetscape', 'Streetscape', 'q4-streetscape', 'Such as: respecting the building line, boundaries, fenestration and landscaping of the street; fitting in while allowing individuality.')]
a4 = [add('4', f'a-{slug}', f'(a) — {slug}', f'{T4A} — {heading}', [row('characteristic', heading, 8, 'Notes 4 and sketches 4. ' + note)],
          *URBAN, figure, 'Designing in the built environment (1.2) with respect for the existing character (1.1).', B4, S4) for slug, heading, figure, note in ITEMS4]
A4 = compose('4', 'a', '(a)', a4, 'q4-characteristics', B4, S4, T4A, labels=[x[1] for x in ITEMS4])
T4B = 'Using notes and freehand sketches, show a proposed external design for a house to be located on this site, which incorporates each of the characteristics discussed at 4(a) above. Justify your proposed design solution.'
T4C = 'Discuss in detail two advantages of developing vacant sites in urban areas.'
B4b = add('4', 'b', '(b)', T4B,
          [row('notes', 'Notes', 6, 'Such as: finishes relating to the neighbours or low-carbon materials such as timber cladding or a green roof; height in line with the eaves, ridge and cills; the façade in line with or set back from the street, with similar fenestration.'),
           row('sketches', 'Sketches', 14, 'Freehand sketches of the proposed external design between the existing houses.'),
           row('justification', 'Justification', 4, 'The design solution justified.')],
          *URBAN, 'q4-design', 'Designing in the built environment (1.2) with respect for the existing character (1.1).', B4, S4)
C4 = add('4', 'c', '(c)', T4C,
         [row(f'advantage-{i}', f'Advantage {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: helping meet housing demand using existing services and infrastructure.'),
             (2, 'A second, different advantage. Such as: revitalising the street and town centre; less urban sprawl into the countryside.')]],
         ['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'], None, 'The built environment (1.2) and site selection (1.3).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-design', B4, S4, parts(('a', T4A), ('b', T4B), ('c', T4C)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p36 (printed 34): (a) eleven points × 3 = 33 (the surface resistance, eight layers, total resistance, U-value); (b) five steps × 3 = 15; (c) design detail notes 4 + sketch 8 = 12. Complete 60.'
S5 = 'No printed choice. Part (b) uses the U-value from (a).'
DATA5 = ('Hardwood flooring thickness 20 mm; sand/cement fine screed thickness 65 mm; floor insulation thickness 200mm; concrete floor slab thickness 150 mm; radon barrier thickness 0.25 mm; '
         'sand blinding thickness 40 mm; hardcore thickness 200 mm; subsoil thickness 300 mm.\n'
         'Thermal data of the ground floor: resistance of internal top surface of floor (R) 0.104 m2 ⁰C/W; conductivity of hardwood flooring (k) 6.666 W/m ⁰C; resistivity of fine screed (r) 1.410 m ⁰C/W; '
         'conductivity of floor insulation (k) 0.022 W/m ⁰C; conductivity of concrete floor slab (k) 1.280 W/m ⁰C; conductivity of radon barrier (k) 0.250 W/m ⁰C; '
         'conductivity of sand blinding (k) 0.160 W/m ⁰C; conductivity of hardcore (k) 1.350 W/m ⁰C; conductivity of subsoil (k) 1.600 W/m ⁰C.')
T5A = 'Calculate the U-value of the floor, given the construction has the following sequence and data: ' + DATA5
T5B = ('Using the U-value of the floor obtained at 5(a) above and the following data, calculate the cost of heat lost annually through this floor: dimensions of floor slab 6.5 metres × 9.0 metres; '
       'average internal temperature 20 ⁰C; average temperature of subsoil 6 ⁰C; heating period 9 hours daily for 39 weeks per annum; cost of oil 96 cent per litre; '
       'calorific value of oil 37350 kJ per litre; 1000 Watts: 1 kJ per second.')
T5C = 'Using notes and a freehand sketch, show best practice design detailing that will prevent the formation of a thermal bridge at the junction of the concrete floor and an external concrete block wall with a full-fill insulated cavity.'
A5 = add('5', 'a', '(a)', T5A,
         [row('resistances', 'Formulae: R=T/k R=T × r', 27, 'Nine resistances, 3 each, by R = T/k (or R = T × r for the screed): internal surface 0.104 (given); hardwood 0.02/6.666 = 0.003; screed 0.065 × 1.410 = 0.092; insulation 0.2/0.022 = 9.091; slab 0.15/1.28 = 0.117; radon barrier 0.00025/0.25 = 0.001; sand blinding 0.04/0.16 = 0.25; hardcore 0.2/1.35 = 0.148; subsoil 0.3/1.6 = 0.188. All in m²°C/W.', list(range(0, 28, 3))),
          row('total-resistance', 'Total resistance (R)', 3, 'Total resistance Rt = 9.993 m²°C/W.', [0, 3]),
          row('u-value', 'Calculation of U- value', 3, 'U = 1 ÷ Rt = 1 ÷ 9.993 = 0.10 W/m²°C, with units.', [0, 3])],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Thermal resistance, conductivity and transmittance (6.1).', B5, S5)
B5b = add('5', 'b', '(b)', T5B,
          [row('heat-loss', 'Heat loss formula and calculations', 3, 'Heat loss = U-value × area × temperature difference = 0.10 × 58.5 × (20 − 6) = 81.9 watts (joules per second).'),
           row('duration', 'Heating duration for one year', 3, 'Heating period = 60 × 60 × 9 × 7 × 39 = 8,845,200 seconds (2,457 hours).'),
           row('energy', 'k/Joules calculation for one year', 3, 'Energy = 8,845,200 × 81.9 ÷ 1000 ≈ 724,422 kJ per year.'),
           row('oil', 'Litres of oil for one year', 3, 'Oil = 724,421.88 ÷ 37,350 = 19.39 litres per year.'),
           row('cost', 'Annual cost of heat loss', 3, 'Annual cost = 19.39 × €0.96 = €18.62. The scheme’s alternative one-line method gives the same €18.62.')],
          ['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Heat loss calculation and running costs (6.3) from the U-value (6.1).', B5, S5)
C5 = add('5', 'c', '(c)', T5C,
         [row('notes', 'Notes', 4, 'Notes on the design detail, as in the scheme’s model: the floor and cavity insulation made continuous at the junction, with an insulated block or perimeter insulation.'),
          row('sketch', 'Sketch', 8, 'Freehand sketch of the floor and cavity-wall junction.')],
         ['cons-6-2', 'cons-4-2'], ['heat-loss-insulation', 'floors'], 'q5-thermal-bridge', 'A thermal bridge (6.2) at the ground-floor junction (4.2).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p37 (printed 35): (a) two advantages and two disadvantages × 3 = 12; (b) three features × (notes 5 + sketches 5) = 30; (c) two modifications × (notes 3 + sketches 3) and two justifications × 3 = 18. Complete 60.'
S6 = 'Part (a) requires both two advantages and two disadvantages, separately marked: two required tasks composed into (a). Features and modifications are open responses.'
T6A = 'Discuss two advantages and two disadvantages of retrofitting the vernacular cottage shown.'
T6B = 'With reference to the design shown, discuss using notes and freehand sketches, three features of the design that contribute to the house having a low environmental impact.'
T6C = 'Discuss in detail, using notes and freehand sketches, two modifications to the house shown that would further reduce the environmental impact of the house. Justify your design choices.'
RETRO = (['cons-1-1', 'cons-1-2'], ['conservation-restoration'])
a6 = [add('6', f'a-{kind}s', f'(a) — {kind}s', f'Discuss two {kind}s of retrofitting the vernacular cottage shown.',
          [row(f'{kind}-1', f'{kind.capitalize()} 1', 3, n1), row(f'{kind}-2', f'{kind.capitalize()} 2', 3, n2)],
          *RETRO, None, 'Retrofitting a vernacular building (1.1) in the built environment (1.2).', B6, S6)
      for kind, n1, n2 in [('advantage', 'Such as: retaining our vernacular heritage; avoiding the embodied energy and carbon of a new house.', 'A second, different advantage. Such as: no added visual pollution; character features; good thermal mass; no planning permission for a retrofit alone.'),
                           ('disadvantage', 'Such as: the extent of work only found once the building is opened up; costs higher than expected.', 'A second, different disadvantage. Such as: small rooms unsuited to modern life; reaching current energy standards is harder.')]]
A6 = compose('6', 'a', '(a)', a6, None, B6, S6, T6A, labels=['Advantages', 'Disadvantages'])
B6b = add('6', 'b', '(b)', T6B,
          [row(f'feature-{i}', f'Design Feature {i}', 10, note) for i, note in [
              (1, 'Notes 5 and sketches 5. Such as: larger south windows for solar heat and light; small north windows.'),
              (2, 'A second, different feature. Such as: the existing cottage retained, avoiding new embodied carbon; low-embodied-energy timber frame for the extension.'),
              (3, 'A third, different feature. Such as: a simple one-room-deep form; high insulation; the attic used as living space; a stove in the fireplace using the stack’s thermal mass.')]],
          ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-low-impact',
          'Low-impact design of the built environment (1.2), solar gain (6.4) and insulation (6.2).', B6, S6)
C6 = add('6', 'c', '(c)', T6C,
         [row('modification-1', 'Modification 1', 6, 'Notes 3 and sketches 3. Such as: a draught lobby at the entrance; trees or built solar shading to the south.'),
          row('modification-2', 'Modification 2', 6, 'A second, different modification: notes 3 and sketches 3. Such as: evacuated tubes or PV panels; a wind turbine; rainwater harvesting; a centrally placed chimney.'),
          row('justification-1', 'Justification 1', 3, 'The first modification justified.'),
          row('justification-2', 'Justification 2', 3, 'The second modification justified.')],
         ['cons-1-2', 'cons-6-4'], ['sustainability-the-environment'], 'q6-modifications', 'Reducing environmental impact (1.2, 6.4).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-low-impact', B6, S6, parts(('a', T6A), ('b', T6B), ('c', T6C)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p38 (printed 36): (a) best nine of nineteen details × 5 = 45, three typical dimensions 3, scale and drafting 8 banded 8/6/4 = 56; (b) independent air supply detail 4. Complete 60.'
S7 = 'One required section and one required air-supply detail. The detail list is a marking menu, not a printed choice.'
T7A = 'To a scale of 1:5, draw a vertical section through the ground floor, hearth and chimney. Show the typical construction details from 350 mm below the finished floor to a level 300 mm above the top of the cast iron flue from the stove and include the connection to the flue liner in the chimney. Include three typical dimensions on your drawing.'
T7B = 'On your drawing, show the typical detailing to provide an independent air supply to the stove.'
A7 = add('7', 'a', '(a)', T7A,
         [row('details', '9 x 5 marks', 45, 'Best nine details, 5 each. Ground floor: 200 mm internal wall; concrete floor/subfloor; floor insulation; screed; radon barrier/DPM; insulated block; airtightness; 20 mm hardwood floor; plaster. Hearth, stove and chimney: hearth; stove; 150 mm cast iron flue; lintel/flue gatherer; chimney blockwork; metal flue gatherer; flue liners; lime-sand fill/vermiculite; internal plaster.'),
          row('dimensions', 'Three typical dimensions (3 × 1 mark)', 3, 'Three typical dimensions, 1 each.'),
          row('presentation', 'Scale and drafting marks (Excellent, Good, Fair)', 8, 'Scale and drafting, assessed together: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-5-7', 'cons-4-2'], ['question-1-drawing-questions', 'fireplaces-fire-prevention', 'floors'], 'q7-section',
         'Scaled drawing (1.5) of a stove, hearth and flue (5.7) on an insulated ground floor (4.2).', B7, S7)
B7b = add('7', 'b', '(b)', T7B,
          [row('air-supply', 'Independent air supply design detail', 4, 'Show and identify an independent air supply ducted to the stove, as in the scheme’s model section.')],
          ['cons-5-7', 'cons-6-5'], ['fireplaces-fire-prevention', 'condensation-air-tightness'], 'q7-section', 'Combustion air for a stove (5.7) in an airtight house (6.5).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p39 (printed 37): (a) two considerations × (notes 5 + sketches 5) = 20; (b) notes 12, sketch 12, any four dimensions 4 = 28; (c) two considerations × (3 + 3) = 12. Complete 60.'
S8 = 'All four printed fittings in (b) are required content of one layout, not a choice.'
DRAIN = (['cons-5-6'], ['drainage'])
T8A = 'Discuss in detail, using notes and freehand sketches, two considerations that should be taken into account when locating a bathroom on the first floor of a house.'
T8B = 'Using notes and a freehand sketch, show the above-ground pipework necessary for the safe removal of waste from the following fittings: shower; wash basin; water closet (W.C.); kitchen sink on ground floor. Include on your sketch typical sizes of the soil and vent pipe (svp) and of the waste pipe from each fitting.'
T8C = 'Outline two considerations to minimise blockages occurring in a drainage system.'
A8 = add('8', 'a', '(a)', T8A,
         [row(f'consideration-{i}', f'Consideration {i}', 10, note) for i, note in [
             (1, 'Notes 5 and sketches 5. Such as: position — the W.C. on an external wall for short pipe runs, a window and ventilation; the soil pipe kept off the front.'),
             (2, 'A second, different consideration. Such as: accessibility (850 mm door, 2100 × 2400 mm room, turning circle, grab rails); privacy with frosted glazing to the north.')]],
         ['cons-5-6', 'cons-1-2'], ['drainage', 'planning-sustainability-environment'], 'q8-location', 'Sanitary fitments (5.6) in the layout (1.2).', B8, S8)
B8b = add('8', 'b', '(b)', T8B,
          [row('notes', 'Notes', 12, 'Such as: a Ø110 mm soil vent pipe vented at the top with a 200 mm bend radius at its base; branches from the shower (Ø40 mm), basin (Ø32 mm), W.C. (Ø100 mm) and kitchen sink (Ø40 mm), each within its maximum length and slope, with deep-seal traps.'),
           row('sketch', 'Sketch', 12, 'Freehand sketch of the above-ground pipework from all four fittings to the stack.'),
           row('dimensions', 'Typical dimensions - Any four', 4, 'Any four typical sizes, 1 each, such as the 110 mm stack and the 40, 32 and 100 mm branches.')],
          *DRAIN, 'q8-pipework', 'Sanitary fitments and the single stack system (5.6).', B8, S8)
C8 = add('8', 'c', '(c)', T8C,
         [row(f'consideration-{i}', f'Consideration {i} - (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: smooth internal surfaces of pipes and fittings.'),
             (2, 'A second, different consideration. Such as: pipes correctly sized and laid to the right falls; access for rodding.')]],
         *DRAIN, None, 'Sanitary fitments and drainage (5.6).', B8, S8)
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-pipework', B8, S8, parts(('a', T8A), ('b', T8B), ('c', T8C)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p40 (printed 38): (a) three principles × (notes 4 + sketches 4) = 24; (b) partition note 4 + sketch 6, floor note 4 + sketch 6, materials 4, dimension 4 = 28; (c) two benefits × (2 + 2) = 8. Complete 60.'
S9 = 'All three printed principles in (a) are required, each separately marked, so each is its own task and the part composes them; (b) requires both the partition and the floor.'
SOUND = (['cons-8-3'], ['sound'])
T9A = 'Discuss in detail, using notes and freehand sketches, how each of the following contribute to reducing the transmission of sound in a dwelling house: completeness; flexibility; isolation.'
ITEMS9 = [('completeness', 'Completeness', 'q9-completeness', 'Such as: no small gaps in the structure — filled block joints, plastered walls, a continuous airtight membrane, sealed windows, doors and pipework.'),
          ('flexibility', 'Flexibility', 'q9-flexibility', 'Such as: absorbent quilt or acoustic matting in partitions and floors absorbing sound.'),
          ('isolation', 'Isolation', 'q9-isolation', 'Such as: separating the elements so sound has no direct path, such as staggered or separate studs and floating floors on resilient strips.')]
a9 = [add('9', f'a-{slug}', f'(a) — {slug}', f'{T9A} — {heading}', [row('principle', heading, 8, 'Notes 4 and sketches 4. ' + note)],
          *SOUND, figure, 'Airborne and impact sound insulation (8.3).', B9, S9) for slug, heading, figure, note in ITEMS9]
A9 = compose('9', 'a', '(a)', a9, 'q9-principles', B9, S9, T9A, labels=[x[1] for x in ITEMS9])
T9B = 'The partitions are of standard timber stud construction and the first floor is a softwood floor on timber joists, with a plasterboard ceiling beneath. The partitions and the floor are to be upgraded to reduce the transmission of sound from the entertainment room. Using notes and freehand sketches show a revised design detailing that will reduce the transmission of sound through the stud partition and the existing first floor. Specify the materials to be used and give their typical dimensions.'
T9C = 'Discuss two benefits that the sound insulation upgrades will have on the health and wellbeing of the occupants.'
B9b = add('9', 'b', '(b)', T9B,
          [row('partition', 'Stud Partition detail', 10, 'Note 4 and sketch 6. Such as: a staggered double-stud partition with absorbent quilt woven between the studs, two layers of plasterboard with staggered joints, sealed fittings and edges; or two separate stud walls.'),
           row('floor', 'Floor detail', 10, 'Note 4 and sketch 6. Such as: acoustic isolation strips on the joists with a floating floor on battens; acoustic matting; quilt between the joists; two layers of plasterboard below.'),
           row('materials', 'Materials to be used', 4, 'The materials specified, such as acoustic quilt, matting and plasterboard.'),
           row('dimension', 'Typical dimension', 4, 'Typical dimensions of the materials.')],
          ['cons-8-3', 'cons-4-3', 'cons-4-5'], ['sound', 'floors', 'doors'], 'q9-upgrades',
          'Sound insulation (8.3) of a timber upper floor (4.3) and stud partition (4.5).', B9, S9)
C9 = add('9', 'c', '(c)', T9C,
         [row(f'benefit-{i}', f'Benefit {i} - (2 for point, 2 for discussion)', 4, note) for i, note in [
             (1, 'Point 2 and discussion 2. Such as: less noise, stress and anger in the household; better sleep.'),
             (2, 'A second, different benefit. Such as: family members doing noisy activities without disturbing others; less risk of hearing loss.')]],
         *SOUND, None, 'Sound insulation and wellbeing (8.3).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-upgrades', B9, S9, parts(('a', T9A), ('b', T9B), ('c', T9C)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p41 (printed 39): (a) three considerations × (notes 4 + sketches 4) = 24; (b) line diagram, unit location, ducting layout and airflow 4 each, description 8 = 24; (c) two advantages × (3 + 3) = 12. Complete 60.'
S10 = 'No printed choice. The OR alternative is a separate Question 10 route.'
MVHR = (['cons-6-5'], ['condensation-air-tightness', 'passive-design'])
T10A = 'Discuss in detail, using notes and freehand sketches, three considerations that should be taken into account when designing a MVHR system for a domestic house.'
T10B = 'Draw a line diagram of the given house plan. Show on your diagram the location of the MVHR unit and a typical layout for the system ducting. Indicate clearly the direction of the airflow in the ducts. Describe how the MVHR system works. Note: It is not necessary to show the furniture.'
T10C = 'Discuss two advantages of installing a MVHR system into a domestic house.'
A10 = add('10', 'a', '(a)', T10A,
          [row(f'consideration-{i}', f'Design consideration {i}', 8, note) for i, note in [
              (1, 'Notes 4 and sketches 4. Such as: the unit on an internal corner inside the insulated envelope, so intake and exhaust are on different faces.'),
              (2, 'A second, different consideration. Such as: direct, individually designed ducting with few 90° bends, insulated where needed; diffusers central in rooms.'),
              (3, 'A third, different consideration. Such as: fit for purpose — an airtight house; access for maintenance and filters.')]],
          *MVHR, None, 'Mechanical ventilation (6.5).', B10, S10)
B10b = add('10', 'b', '(b)', T10B,
           [row('diagram', 'Line diagram of the given house', 4, 'A line diagram of the given ground floor plan.'),
            row('unit', 'Location of MVHR unit', 4, 'The MVHR unit located.'),
            row('ducting', 'Layout for the system ducting', 4, 'Supply ducts to living rooms and bedrooms, extract ducts from kitchen, bathroom and utility.'),
            row('airflow', 'Direction of airflow in ducts', 4, 'The direction of airflow shown in the ducts.'),
            row('description', 'Description of how the system works', 8, 'Fans continuously supply fresh air and extract warm, moist, stale air at equal rates; in the heat exchanger the outgoing air warms the incoming air without mixing; a particle filter removes dust and pollen.')],
           *MVHR, 'q10-mvhr', 'Mechanical ventilation with heat recovery (6.5).', B10, S10)
C10 = add('10', 'c', '(c)', T10C,
          [row(f'advantage-{i}', f'Advantage {i} - (3 for point, 3 for discussion)', 6, note) for i, note in [
              (1, 'Point 3 and discussion 3. Such as: constant fresh, filtered air with heat recovered from the stale air.'),
              (2, 'A second, different advantage. Such as: less condensation and mould; lower heating demand.')]],
          *MVHR, None, 'Mechanical ventilation (6.5).', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-mvhr', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p42 (printed 40): (a) three discussion points × (4 + 6) = 30; (b) three guidelines × (4 + 6) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the MVHR question. Its parts are open responses.'
TAA = 'Discuss the above statement in detail.'
TAB = 'Propose three best practice guidelines that would ensure all buildings are retrofitted in the most sustainable way possible to minimise their primary energy use and improve their energy performance.'
ENERGY = (['cons-6-3', 'cons-1-2'], ['heat-loss-insulation', 'sustainability-the-environment'])
AA = add('10', 'a', '(a)', TAA,
         [row(f'point-{i}', f'Discussion Point {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: Ireland reducing the primary energy use of buildings through new standards and retrofit programmes.'),
             (2, 'Point 4 and discussion 6. Such as: Parts F and L of the 2019 Building Regulations implementing the EU Energy Performance of Buildings Directive.'),
             (3, 'Point 4 and discussion 6. Such as: energy-efficient design and retrofit of electrical and heating systems. Three distinct, well-argued points are needed.')]],
         *ENERGY, None, 'Energy use (6.3) in a sustainable built environment (1.2).', BALT, SALT, alt=True)
AB = add('10', 'b', '(b)', TAB,
         [row(f'guideline-{i}', f'Guideline {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: grant-aided deep retrofit of the older housing stock to current standards, cutting heating energy and CO₂ by 75–90%.'),
             (2, 'Point 4 and discussion 6. Such as: major renovation (over 25% of the envelope) reaching the cost-optimal level under Part L; SEAI oversight of upgrades.'),
             (3, 'Point 4 and discussion 6. Such as: a whole-of-systems team approach linking form, fabric and services. Three distinct guidelines are needed.')]],
         *ENERGY, None, 'Energy use (6.3) in a sustainable built environment (1.2).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, parts(('a', TAA), ('b', TAB)), alt=True)

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and any four of the other nine (300 marks); all question banks retained, no full-exam Cartesian cards.'),
          (7, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.')]
REASONS = {
    'q1-b': 'Reshaped to the printed design-detailing row (2 × 2); tariff unchanged (4).',
    'q2-a': 'Reshaped to one row per printed activity, each two guidelines at 3 for note + 4 for sketch; tariff unchanged (42).',
    'q2-b': 'Split into the three printed responsibilities (3 + 3 each); tariff unchanged (18).',
    'q3-a': 'Split into the three printed considerations (3 + 3 each); tariff unchanged (18).',
    'q3-c-advantages': 'Split into the two printed advantages (3 each); tariff unchanged (6).',
    'q3-c-disadvantages': 'Split into the two printed disadvantages (3 each); tariff unchanged (6).',
    'q4-a-materials-and-finishes': 'Reshaped to the printed characteristic row (notes 4 + sketches 4); tariff unchanged (8).',
    'q4-a-shape-and-form': 'Reshaped to the printed characteristic row (notes 4 + sketches 4); tariff unchanged (8).',
    'q4-a-streetscape': 'Reshaped to the printed characteristic row (notes 4 + sketches 4); tariff unchanged (8).',
    'q4-b': 'Rebuilt to the printed rows — notes 6, sketches 14, justification 4: 4 → 24.',
    'q4-c': 'Split into the two printed advantages (3 + 3 each); tariff unchanged (12).',
    'q5-a': 'Rebuilt to the printed eleven points (3 each), including the surface resistance: 30 → 33.',
    'q5-b': 'Reshaped to the five printed calculation steps (3 each) with the scheme’s worked answer (€18.62); tariff unchanged (15).',
    'q6-a-advantages': 'Split into the two printed advantages (3 each); tariff unchanged (6).',
    'q6-a-disadvantages': 'Split into the two printed disadvantages (3 each); tariff unchanged (6).',
    'q6-b': 'Split into three design features, each notes 5 + sketches 5; tariff unchanged (30).',
    'q6-c': 'Rebuilt to the printed rows — two modifications (notes 3 + sketches 3) and two justifications (3 each); tariff unchanged (18).',
    'q7-a': 'Adds the scale and drafting allowance (8, banded 8/6/4) to the nine details and three dimensions: 48 → 56.',
    'q7-b': 'Reshaped to the printed air-supply detail row; tariff unchanged (4).',
    'q8-a': 'Split into two considerations, each notes 5 + sketches 5; tariff unchanged (20).',
    'q8-c': 'Split into the two printed considerations (3 + 3 each); tariff unchanged (12).',
    'q9-a-completeness': 'Reshaped to the printed principle row (notes 4 + sketches 4); tariff unchanged (8).',
    'q9-a-flexibility': 'Reshaped to the printed principle row (notes 4 + sketches 4); tariff unchanged (8).',
    'q9-a-isolation': 'Reshaped to the printed principle row (notes 4 + sketches 4); tariff unchanged (8).',
    'q9-b': 'Rebuilt to the printed rows — partition and floor details (note 4 + sketch 6 each), materials 4, dimension 4: 16 → 28.',
    'q9-c': 'Split into the two printed benefits (2 + 2 each); tariff unchanged (8).',
    'q10-a': 'Split into three considerations, each notes 4 + sketches 4; tariff unchanged (24).',
    'q10-c': 'Split into the two printed advantages (3 + 3 each); tariff unchanged (12).',
}
D.finish(LEDGER, {}, REASONS)
