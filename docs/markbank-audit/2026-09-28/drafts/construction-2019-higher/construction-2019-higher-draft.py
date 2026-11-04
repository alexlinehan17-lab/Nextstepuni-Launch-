"""Draft the 2019 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 32-42). Q4(b) "select any two of the above areas" is ONE card with an any-two group over the
three printed areas (choice is not a route). The 21 pre-audit 2019 Higher cards keep their IDs and
concept IDs and are corrected in place; their four build-time overrides are retired.
Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Triple-glazed window in a timber frame wall', concept='timber-frame-window-section',
              stem='A triple glazed window with a wooden frame is fitted in the external wall of a dwelling house as shown. The fixed frame of the window is 100 mm × 80 mm. The wall is of timber frame construction with an external concrete block leaf. The internal timber frame is 250 mm × 50 mm and the outer leaf is of 100 mm concrete block construction with an external render finish. A 50 mm service cavity is also provided at the internal surface. Above the window head, an inset wooden panel is sheeted with vertical larch cladding of 130 mm × 20 mm to form an external rainscreen, as shown. The window is 600 mm in height and has a thermally broken insulated frame.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the cill detail in (b) is marked separately.'),
    '2': dict(page=2, title='Roof requirements, profiles and materials', concept='roof-profiles-materials', stem='',
              note='Original sketch retained. Requirements, profiles and materials are open responses; the scheme shows four example profiles.'),
    '3': dict(page=3, title='Second-storey bedroom and en suite extension', concept='bedroom-ensuite-extension',
              stem='The drawing shows the elevation of a detached house and the plan of its first floor. The front wall A-A is south facing. The owners intend to apply for planning permission to build an additional bedroom and en suite bathroom. It is proposed to remove the roof of the single storey extension on the left and build the bedroom and bathroom over it.',
              note='Original elevation and plan retained. Considerations, layouts and the external design are open responses; the scheme gives model layouts and designs.'),
    '4': dict(page=3, title='Refurbishing a terraced townhouse', concept='townhouse-refurbishment',
              stem='The sketch shows a row of terraced townhouses built over 100 years ago. A young couple have purchased one of the houses and have decided to refurbish it as their family home.',
              note='Original sketch retained. Part (b) is a closed choice of any two of the three printed areas: one card holding all three.'),
    '5': dict(page=4, title='Cavity wall U-value, heat-loss cost and external insulation', concept='cavity-wall-u-value',
              stem='The external wall of a house built in the 1990s is of 100 mm concrete block construction with a 100 mm partially filled cavity, as shown.',
              note='All printed data are retained in the original question. Part (b) uses the U-value from (a); the scheme’s worked answers are U = 0.516 W/m²°C, an annual cost of €199.60 and 147 mm of expanded polystyrene.'),
    '6': dict(page=5, title='Low environmental impact house and renewable energy', concept='low-impact-renewables',
              stem='The elevation and ground floor plan of a house are shown. The house has two bedrooms and a bathroom upstairs. The external walls are of timber frame construction with a rendered concrete block and timber cladding finish. The house is designed to have low environmental impact.',
              note='Original elevation and plan retained. All three printed technologies in (b) are required, each separately marked.'),
    '7': dict(page=5, title='Closed riser stairs with a bullnose step', concept='bullnose-stairs-section',
              stem='The main hall of a two-storey dwelling has a closed riser wooden stairs. The bottom of the stairs has a bullnose step as shown. The newel post is 120 mm × 120 mm and the rise of a step should not exceed 175 mm.',
              note='Original sketch and specification retained. Construction, dimension and scale/drafting marks belong to part (a); the safety features in (b) are marked separately.'),
    '8': dict(page=6, title='Rural wastewater treatment', concept='rural-wastewater-treatment', stem='',
              note='Original site layout map retained. Considerations and the alternative method are open responses; the scheme gives a model layout and three alternative systems.'),
    '9': dict(page=6, title='Thermal bridging at a door, wallplate and threshold', concept='thermal-bridge-door-section',
              stem='Thermal envelope continuity is essential to ensure a dwelling house is thermal bridge free. The drawing shows an outline section through the external door of a single-storey house having a 450 mm external concrete block wall with a 250 mm full-fill insulated cavity. The house has a traditional cut roof with an insulated solid concrete ground floor. The external door and frame are thermally broken.',
              note='Original section retained. Every circled location in (a) is required, each separately marked under the scheme’s heading for it.'),
    '10': dict(page=7, title='EnerPHit deep retrofit of a 1970s bungalow', concept='enerphit-retrofit',
               stem='The plan and elevation of a bungalow built in the 1970s are shown. The wall B-B is south facing. The owners intend to carry out a deep retrofit upgrade of their house to meet the EnerPHit Passive House standard.',
               note='Original plan and elevation retained. Part (b) develops each consideration given in (a).'),
}
ALT = dict(page=7, title='Building sustainably to minimise a carbon footprint (alternative Question 10)', concept='sustainable-carbon-footprint',
           stem='“Global warming is now a generally recognised phenomenon and sustainability is recognised as being a necessity, not an option. One of the main culprits blamed for global warming is carbon dioxide (CO2), so it is worth taking a look at what can be done about it. CO2 is produced by each of us every day, and our personal carbon footprint is a measure of how many tonnes of CO2 are emitted directly or indirectly, as a result of the consumption of goods and services. When building your own home you should take every opportunity to build in the most sustainable way so as to minimise your own carbon footprint.” Adapted from: Building Your Own Sustainable and Energy Efficient House. by Henry Skates Published by: The Crowood Press Ltd. ISBN: 978-1-84797-258-3',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the EnerPHit question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately.')
SCHEME_PAGES = {'1': [4, 5, 32], '2': [5, 6, 33], '3': [7, 8, 9, 10, 34], '4': [11, 12, 13, 14, 15, 35], '5': [16, 17, 36], '6': [17, 18, 19, 20, 37],
                '7': [21, 38], '8': [22, 23, 39], '9': [24, 25, 40], '10': [25, 26, 27, 41], '10-alt': [28, 29, 42]}
D = cp.Draft(HERE, 2019, 'higher', ('45bad0b8a8a9d02b29f856805aa37e3385709cbfe458661f79a3104fbe769ea0',
                                    '8b5abe8e2e0ba5d4d19c280bbdce76fde932a941cd07205edd9bb0a8c71c3edc'), 21, QUESTIONS, SCHEME_PAGES, alt=ALT)
row, add, compose, parts, anyn = D.row, D.add, D.compose, D.parts, D.anyn
BAND8 = [0, 4, 6, 8]
D.figures({
    'q1-original': D.paper(2, [45, 53, 580, 430]), 'q2-original': D.paper(2, [45, 430, 580, 750]),
    'q3-original': D.paper(3, [45, 53, 580, 440]), 'q4-original': D.paper(3, [45, 440, 580, 760]),
    'q5-original': D.paper(4, [45, 53, 580, 760]), 'q6-original': D.paper(5, [45, 53, 580, 470]),
    'q7-original': D.paper(5, [45, 475, 580, 730]), 'q8-original': D.paper(6, [45, 53, 580, 415]),
    'q9-original': D.paper(6, [45, 415, 580, 760]), 'q10-original': D.paper(7, [45, 53, 580, 425]),
    'q10-alt-original': D.paper(7, [45, 495, 580, 715]),
    'q1-section': D.composite((4, [45, 50, 575, 790]), (5, [45, 50, 575, 310])),
    'q1-cill': D.scheme(5, [45, 50, 575, 310]),
    'q2-profiles': D.scheme(6, [45, 50, 575, 530]),
    'q3-layout': D.composite((8, [45, 235, 575, 770]), (9, [45, 50, 575, 330])),
    'q3-external': D.composite((9, [45, 360, 575, 745]), (10, [45, 50, 575, 790])),
    'q4-upgrades': D.composite((11, [45, 250, 575, 770]), (12, [45, 50, 575, 790]), (13, [45, 50, 575, 790]), (14, [45, 50, 575, 790]), (15, [45, 50, 575, 475])),
    'q5-calculation': D.scheme(16, [45, 50, 575, 780]), 'q5-thickness': D.scheme(17, [45, 50, 575, 285]),
    'q6-features': D.scheme(17, [45, 290, 575, 790]),
    'q6-renewables': D.composite((18, [45, 50, 575, 740]), (19, [45, 50, 575, 670]), (20, [45, 50, 575, 395])),
    'q7-section': D.scheme(21, [45, 50, 575, 770]),
    'q8-layout': D.scheme(22, [45, 345, 575, 775]), 'q8-alternative': D.scheme(23, [45, 75, 575, 790]),
    'q9-details': D.scheme(24, [45, 50, 575, 790]),
    'q10-retrofit': D.composite((26, [45, 50, 575, 780]), (27, [45, 50, 575, 510])),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p32 (printed 29): (a) best twelve details × 4 across the timber frame wall, the triple glazing and the sheeting/panel/lintel = 48, scale 4 + drafting 4 banded 8/6/4 = 56; (b) wrap-around DPC 4. Complete 60.'
S1 = 'One required section and one required cill detail. The detail lists are marking menus, not printed choices.'
T1A = 'To a scale of 1:5, draw a vertical section through the fixed frame of the window and the external wall of the house. Show the typical construction detail from a level 400 mm below the window cill, through the window frame, up to a level 500 mm above the window head.'
T1B = 'On your drawing, show the typical design detailing to prevent the ingress of rainwater at the window cill.'
A1 = add('1', 'a', '(a)', T1A,
         [row('details', 'Any 12 × 4marks', 48, 'Best twelve details, 4 each, across three menus. External timber frame wall: external render; concrete block; air space/residual cavity; cavity closer; breather membrane; racking board; 250 stud/insulation; sheeting; air barrier membrane; insulated service cavity; plasterboard/skim. Triple glazing: concrete window cill; wrap-around DPC; thermally broken frame cill; window board; triple glazing; thermally broken frame head; airtight tapes at head and cill. Sheeting/panel/lintel: larch cladding; soffit; battens; counter battens; DPC; batten for DPC; timber lintels.'),
          row('presentation', 'Scale 4 marks: Drafting 4 marks:', 8, 'Scale 4 and drafting 4, assessed together: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-3-6', 'cons-3-3', 'cons-3-2'], ['question-1-drawing-questions', 'windows-light', 'walls'], 'q1-section',
         'Scaled drawing (1.5) of window details at head and cill (3.6) in a timber frame external wall (3.3) behind a rainscreen (3.2).', B1, S1)
B1b = add('1', 'b', '(b)', T1B,
          [row('cill', 'wrap around DPC', 4, 'Show and identify a DPC wrapped around the cill under the window frame, as in the scheme’s model detail.')],
          ['cons-3-6', 'cons-3-4'], ['windows-light', 'walls'], 'q1-cill', 'The window cill (3.6) and its damp proof course (3.4).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p33 (printed 30): (a) three requirements × (notes 3 + sketches 3) = 18; (b) three roof profiles × (notes 2 + sketches 6) = 24, recommendation 3, justification 3 = 30; (c) three materials × (identify 2 + advantage 1 + disadvantage 1) = 12. Complete 60.'
S2 = '"Select a different roofing material for each" is an open choice of material for every profile, not a closed choice; all parts are open responses.'
ROOF = (['cons-3-8', 'cons-3-9'], ['roofs'])
T2A = 'Discuss in detail, using notes and freehand sketches, three functional requirements of a roof suitable for a domestic dwelling house.'
T2B = 'The owners of a house located in a rural setting wish to build an extension to create an additional living space. The sketch shows the existing house and the proposed outline of the new extension at design stage. Using notes and freehand sketches, show the design for three different, distinct roof profiles suitable for the proposed extension. Recommend a preferred roof profile for the proposed extension and justify your recommendation.'
T2C = 'Select a different roofing material for each of the three roof types you have shown at 2(b). Give one advantage and one disadvantage for each material selected.'
A2 = add('2', 'a', '(a)', T2A,
         [row(f'requirement-{i}', f'Design Feature {i}', 6, note) for i, note in [
             (1, 'Notes 3 and sketches 3. Such as: weather resistance against rain, snow, wind and sun; structural stability under dead and live loads and lateral movement.'),
             (2, 'A second, different requirement. Such as: thermal insulation for comfort in winter and against summer heat gain; durability with little maintenance and treated members.'),
             (3, 'A third, different requirement. Such as: ventilation against condensation and fungal attack; an unbroken airtightness layer.')]],
         *ROOF, None, 'Roof structure (3.8) and covering (3.9).', B2, S2)
B2b = add('2', 'b', '(b)', T2B,
          [row(f'profile-{i}', f'Roof profile {i}', 8, note) for i, note in [
              (1, 'Notes 2 and sketches 6. Such as, from the scheme’s sketches: a pitched gable roof matching the house.'),
              (2, 'A second, distinct profile: notes 2 and sketches 6. Such as: a pitched roof with roof lights; a flat green roof.'),
              (3, 'A third, distinct profile: notes 2 and sketches 6. Such as: a curved (barrel) roof.')]]
          + [row('recommendation', 'Recommendation for a roof profile', 3, 'One preferred profile recommended.'),
             row('justification', 'Justification for recommendation', 3, 'The recommendation justified for the rural extension.')],
          ['cons-3-8', 'cons-1-2'], ['roofs', 'planning-sustainability-environment'], 'q2-profiles', 'Roof forms (3.8) for an extension in the built environment (1.2).', B2, S2)
C2 = add('2', 'c', '(c)', T2C,
         [row(f'material-{i}', f'Material {i} - identify (2 marks), adv (1 mark), disadv (1 mark)', 4, note) for i, note in [
             (1, 'Identify 2, advantage 1, disadvantage 1, for the first profile. Such as: natural slates; fibre cement slates; concrete or clay tiles.'),
             (2, 'A different material for the second profile. Such as: zinc sheeting; wood shingle; thatch; corrugated steel.'),
             (3, 'A different material for the third profile. Such as: roofing felt; asphalt; single-ply membrane (EPDM rubber).')]],
         ['cons-3-9'], ['roofs'], None, 'Roof coverings (3.9).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-profiles', B2, S2, parts(('a', T2A), ('b', T2B), ('c', T2C)))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p34 (printed 31): (a) three considerations × (3 + 3) = 18; (b) internal layout 14, three design considerations 3 each, justification 3 = 26; (c) notes 4 + sketches 12 = 16. Complete 60.'
S3 = 'Considerations, the layout and the external design are open responses with no printed list.'
EXT = (['cons-1-2', 'cons-5-6'], ['planning-sustainability-environment', 'drainage'])
T3A = 'Discuss in detail, three design considerations for the proposed bedroom and en suite bathroom.'
T3B = 'Using notes and freehand sketches, show a proposed internal layout for the bedroom and en suite bathroom that incorporates each of the design considerations you outlined at 3(a) above. Justify your choices.'
T3C = 'Using notes and freehand sketches, show an external design for your extension that will enhance the overall visual appearance of the house.'
A3 = add('3', 'a', '(a)', T3A,
         [row(f'consideration-{i}', f'Design consideration {i} - (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: furniture layout for the bed, lockers and wardrobe, with the en suite fittings close to existing drainage; access and escape, with a second means of egress such as an escape window.'),
             (2, 'A second, different consideration. Such as: storage in wardrobes or a walk-in wardrobe; future flexibility in sockets, lights and multi-functional space; ergonomics around doors and drawers.'),
             (3, 'A third, different consideration. Such as: the human senses — natural light from the south (visual), triple glazing against noise (auditory), insulation and thermostats (tactile), ventilation of bedroom and en suite (olfactory).')]],
         *EXT, None, 'Layout design (1.2) with sanitary fitments (5.6).', B3, S3)
B3b = add('3', 'b', '(b)', T3B,
          [row('layout', 'Internal layout design (Bedroom + en-suite)', 14, 'A layout of the bedroom and en suite, as in the scheme’s model plans: furniture placed with circulation space; en suite fittings near the existing waste pipes or on an external wall; a stud partition to the en suite and walk-in wardrobe.'),
           row('consideration-1', 'Design Consideration 1', 3, 'The first consideration from (a) shown in the layout.'),
           row('consideration-2', 'Design Consideration 2', 3, 'The second consideration from (a) shown in the layout.'),
           row('consideration-3', 'Design Consideration 3', 3, 'The third consideration from (a) shown in the layout.'),
           row('justification', 'Justification', 3, 'The choices justified, such as large south windows for light and heat, an escape window and a ventilated en suite.')],
          *EXT, 'q3-layout', 'Layout design (1.2) with sanitary fitments (5.6).', B3, S3)
C3 = add('3', 'c', '(c)', T3C,
         [row('notes', 'Notes', 4, 'Such as: brick and slates in keeping with the house; the same pitch so eaves and ridge lines align; matching window proportions; or a deliberate contrast — a flat roof with larch cladding, or a zinc-clad dormer in a hipped roof.'),
          row('sketches', 'Sketches', 12, 'Freehand sketches of the external design of the extension on the house.')],
         ['cons-1-2', 'cons-1-1'], ['planning-sustainability-environment', 'conservation-restoration'], 'q3-external',
         'Extending a house in keeping with its character (1.1, 1.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-layout', B3, S3, parts(('a', T3A), ('b', T3B), ('c', T3C)))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p35 (printed 32): (a) three benefits × (4 + 4) = 24; (b) any two of the three printed areas × (notes 10 + sketches 8) = 36. Complete 60.'
S4 = 'Choice is not a route: part (b) (select any two of the three printed areas) is ONE card with an any-two group over the scheme’s three areas; its figure and the complete-question figure carry all three areas’ drawings.'
T4A = 'Discuss three benefits to the local community of refurbishing one of the townhouses as a family home.'
T4B = 'The owners commissioned a survey of the house which revealed the following: traditional cut roof with natural slates; softwood sliding sash windows with single-glazing; solid external walls of brick construction, uninsulated and with internal lime render. Select any two of the above areas and, using notes and freehand sketches, describe in detail the steps involved in upgrading each area selected in a manner that respects the appearance and character of the original townhouses.'
A4 = add('4', 'a', '(a)', T4A,
         [row(f'benefit-{i}', f'Benefit {i} (4 for point, 4 for discussion)', 8, note) for i, note in [
             (1, 'Point 4 and discussion 4. Such as: sustaining the local social community — schools, parks and playgrounds; supporting local shops and cafés.'),
             (2, 'A second, different benefit. Such as: improving the physical fabric of the neighbourhood; easing the urban housing shortage.'),
             (3, 'A third, different benefit. Such as: pride that encourages neighbours to upgrade; keeping the residential architectural heritage; regeneration of the area.')]],
         ['cons-1-1', 'cons-1-2'], ['conservation-restoration'], None, 'Conserving older buildings (1.1) in the built environment (1.2).', B4, S4)
AREAS = [('Traditional cut roof with natural slates', 'remove the slates carefully, clean only their undersides of lime parging, weigh and grade them and refit the heaviest at the eaves; replace decayed rafter ends, wallplate and fascia in the same species and profiles; a vapour-diffuse breathable membrane with counter battens; cast-iron rainwater goods; hygroscopic insulation such as sheep’s wool with woodfibre board, and a thoroughly ventilated roof.'),
         ('Softwood sliding sash windows with single - glazing', 'repair rather than replace, by a specialist conservation joiner; remove the sashes and glass carefully and record their positions; replace rotten timber in the same species with traditional joints and animal glue; free the pulleys, renew the cords and reuse the counter-balance weights; non-toxic paint; discreet secondary glazing.'),
         ('Solid external walls of brick construction, uninsulated and with internal lime render', 'never cement mortar; have the lime mortar analysed and matched (NHL strength, sand); rake out by hand to twice the joint width and repoint in stages, protected with hessian; internally, hempcrete or an insulating lime plaster system with a three-coat lime render.')]
A4b = add('4', 'b', '(b)', T4B,
          [anyn('areas', 'Two areas for upgrading', 2, 18, AREAS, 'Any two of the three printed areas, each notes 10 and sketches 8 = 18.')],
          ['cons-1-1', 'cons-3-9', 'cons-3-5', 'cons-3-3', 'cons-6-2'], ['conservation-restoration', 'roofs', 'windows-light', 'walls', 'heat-loss-insulation'], 'q4-upgrades',
          'The union of the three printed areas, upgraded with respect for the original character (1.1): the slated roof (3.9), the sash windows (3.5) and the solid brick walls (3.3) with breathable insulation (6.2).', B4, S4)
compose('4', 'complete', ' — complete', [A4, A4b], 'q4-upgrades', B4, S4, parts(('a', T4A), ('b', T4B)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p36 (printed 33): (a) ten points × 3 = 30 (two surface resistances, six layers, total resistance, U-value); (b) five steps × 3 = 15; (c) five steps × 3 = 15. Complete 60.'
S5 = 'No printed choice. Parts (b) and (c) use the U-value from (a).'
CALC = (['cons-6-1'], ['heat-u-value-calculations'])
DATA5 = ('External render thickness 16 mm; Concrete block outer leaf thickness 100 mm; Clear cavity width 50 mm; Polystyrene insulation thickness 50 mm; Concrete block inner leaf thickness 100 mm; Internal plaster thickness 12 mm.\n'
         'Thermal data of the external wall: Resistance of external surface (R) 0.048 m2 °C/W; Resistivity of external render (r) 2.170 m °C/W; Conductivity of concrete external blockwork (k) 1.440 W/m °C; '
         'Resistance of clear cavity (R) 0.170 m2 °C/W; Conductivity of insulation (k) 0.037 W/m °C; Conductivity of concrete internal blockwork (k) 1.440 W/m °C; '
         'Resistivity of internal plaster (r) 6.250 m °C/W; Resistance of internal surface (R) 0.122 m2 °C/W.')
T5A = 'Calculate the U-value of the wall, given the construction has the following sequence and data: ' + DATA5
T5B = ('Using the U-value of the wall obtained at 5(a) above and the following data, calculate the cost of heat lost annually through this wall: area of external wall 135 m2; '
       'average internal temperature 19 °C; average external temperature 5 °C; heating period 9 hours daily for 36 weeks per annum; cost of oil 94 cent per litre; '
       'calorific value of oil 37350 kJ per litre; 1000 Watts 1 kJ per second.')
T5C = ('It is proposed to upgrade the thermal properties of the above wall, to meet the Passive House standard, by fixing expanded polystyrene to the external surface, as shown. '
       'Given the thermal conductivity (k) of expanded polystyrene as 0.031 W/m°C, calculate the thickness of expanded polystyrene required to achieve a U-value of 0.15 W/m2 °C.')
A5 = add('5', 'a', '(a)', T5A,
         [row('resistances', 'Formulae: R=T/k R=T × r', 24, 'Eight resistances, 3 each, by R = T/k (or R = T × r for render and plaster): external surface 0.048 (given); render 0.016 × 2.170 = 0.035; external blockwork 0.1/1.44 = 0.069; clear cavity 0.170 (given); insulation 0.05/0.037 = 1.351; internal blockwork 0.1/1.44 = 0.069; plaster 0.012 × 6.25 = 0.075; internal surface 0.122 (given). All in m²°C/W.', list(range(0, 25, 3))),
          row('total-resistance', 'Total resistance', 3, 'Total resistance Rt = 1.939 m²°C/W.', [0, 3]),
          row('u-value', 'Calculation of U- value', 3, 'U = 1 ÷ Rt = 1 ÷ 1.939 = 0.516 W/m²°C, with units.', [0, 3])],
         *CALC, 'q5-calculation', 'Thermal resistance, conductivity and transmittance (6.1).', B5, S5)
B5b = add('5', 'b', '(b)', T5B,
          [row('heat-loss', 'Heat loss formula and calculations', 3, 'Heat loss = U-value × area × temperature difference = 0.516 × 135 × (19 − 5) = 975.24 watts (joules per second).'),
           row('duration', 'Heating duration for one year', 3, 'Heating period = 60 × 60 × 9 × 7 × 36 = 8,164,800 seconds (2,268 hours).'),
           row('energy', 'k/Joules calculation for one year', 3, 'Energy = 8,164,800 × 975.24 ÷ 1000 = 7,962,639.552 kJ per year.'),
           row('oil', 'Litres of oil for one year', 3, 'Oil = 7,962,639.552 ÷ 37,350 = 212.34 litres per year.'),
           row('cost', 'Annual cost of heat loss', 3, 'Annual cost = 212.34 × €0.94 = €199.60. The scheme’s alternative one-line method gives the same €199.60.')],
          ['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Heat loss calculation and running costs (6.3) from the U-value (6.1).', B5, S5)
C5 = add('5', 'c', '(c)', T5C,
         [row('required-resistance', 'Resistance for U- value for 0.15Wm2K (using R=1/U)', 3, 'Required resistance = 1 ÷ 0.15 = 6.666 m²K/W.'),
          row('existing-resistance', 'Resistance from calculated U-value from part (a)', 3, 'Existing resistance = 1 ÷ 0.516 = 1.939 m²K/W (the scheme prints the divisor as 0.156).'),
          row('difference', 'Difference in resistances (required resistance)', 3, 'Difference = 6.666 − 1.939 = 4.727 m²K/W.'),
          row('formula', 'Application of formula R = T/k', 3, 'R = T/k, so 4.727 = T/0.031.'),
          row('thickness', 'Required thickness of insulation', 3, 'T = 4.727 × 0.031 = 0.146537 m: 147 mm of expanded polystyrene (146 or 147 mm accepted).')],
         ['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation'], 'q5-thickness', 'Thermal transmittance (6.1) and insulating materials (6.2).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p37 (printed 34): (a) three features × (notes 5 + sketches 5) = 30; (b) three printed technologies × (notes/discussion 3 + sketch 3) = 18; (c) two advantages × (3 + 3) = 12. Complete 60.'
S6 = 'All three printed technologies in (b) are required, each separately marked; not a choice.'
T6A = 'With reference to the design shown, discuss using notes and freehand sketches, three features of the design that contribute to the house having a low environmental impact.'
T6B = 'Using notes and freehand sketches, discuss in detail each of the following renewable energy technologies and identify how each contributes to making a home more eco-friendly: evacuated tubes; wind turbines; photovoltaic panels.'
T6C = 'Discuss in detail two advantages of using local craft skills when building the house shown.'
A6 = add('6', 'a', '(a)', T6A,
         [row(f'feature-{i}', f'Design Feature {i}', 10, note) for i, note in [
             (1, 'Notes 5 and sketches 5. Such as: large south-facing glazing for sunlight and heat; trees to the south for summer shading.'),
             (2, 'A second, different feature. Such as: a wood-burning stove in a central high-thermal-mass chimney; high insulation; small north windows.'),
             (3, 'A third, different feature. Such as: photovoltaic cells on the roof; a low-embodied-energy timber frame; the attic used as living space, reducing the footprint.')]],
         ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-features',
         'Low-impact design of the built environment (1.2), solar gain (6.4) and insulation (6.2).', B6, S6)
B6b = add('6', 'b', '(b)', T6B,
          [row('evacuated-tubes', 'Evacuated Tubes', 6, 'Notes/discussion 3 and sketch 3. Such as: tubes in a vacuum, each with a copper heat pipe whose fluid vaporises and gives up its heat at the manifold to the water from the storage tank; heating hot water with less fossil fuel.'),
           row('wind-turbines', 'Wind Turbines', 6, 'Notes/discussion 3 and sketch 3. Such as: wind turns the blades, rotor and generator; an inverter converts DC to AC for the home, batteries or the grid; a control box protects it in strong winds; less demand on fossil-fuelled grid electricity.'),
           row('photovoltaic-panels', 'Photovoltaic Panels', 6, 'Notes/discussion 3 and sketch 3. Such as: light frees electrons in the PV cells, giving direct current; an inverter supplies AC to the home; excess stored in batteries or sent to the grid; clean electricity without CO₂.')],
          ['cons-5-3', 'cons-5-8', 'cons-6-4'], ['services-water-gas-electricity', 'sustainability-the-environment'], 'q6-renewables',
          'Renewable heating (5.3) and electricity (5.8) from solar and wind energy (6.4).', B6, S6)
C6 = add('6', 'c', '(c)', T6C,
         [row(f'advantage-{i}', f'Advantage {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: traditional knowledge and skills preserved for future generations; a sense of place and pride.'),
             (2, 'A second, different advantage. Such as: local employment, keeping families in the locality; local materials sourced, reducing embodied energy.')]],
         ['cons-1-1', 'cons-1-2'], ['conservation-restoration', 'sustainability-the-environment'], None, 'Traditional craft skills (1.1) in a sustainable built environment (1.2).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-features', B6, S6, parts(('a', T6A), ('b', T6B), ('c', T6C)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p38 (printed 35): (a) best eight of thirteen details × 5 = 40, three dimensions of the stairs 6, scale and drafting 8 banded 8/6/4 = 54; (b) three safety design details × 2 = 6. Complete 60.'
S7 = 'One required section and three required safety features. The detail list is a marking menu, not a printed choice.'
STAIRS = (['cons-4-4'], ['stairs'])
T7A = 'To a scale of 1:5, draw a vertical section through the centre of the stairs. The section should show the typical construction detail through the bottom three steps of the stairs, showing the newel post, string, balusters and handrail. Include the typical dimensions of three structural members of the stairs.'
T7B = 'Indicate on your drawing three design features that ensure the stairs is safe for users.'
A7 = add('7', 'a', '(a)', T7A,
         [row('details', '8 x 5 marks', 40, 'Best eight details, 5 each. Menu: bullnose step; newel post; string; string capping; riser; tread; wedges; glue blocks; handrail; balusters; nosing line/pitch line; handrail-to-newel joint; string-to-newel joint.'),
          row('dimensions', 'Three dimensions of the stairs', 6, 'Typical dimensions of three structural members, 2 each, such as string 250 × 50 mm, newel 120 × 120 mm, tread 250 × 25 mm, riser 175 × 20 mm, balusters and handrail 40 × 40 mm.'),
          row('presentation', 'Scale and drafting marks (Excellent, Good, Fair)', 8, 'Scale and drafting, assessed together: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-4-4', 'cons-10-1'], ['question-1-drawing-questions', 'stairs'], 'q7-section',
         'Scaled drawing (1.5) of a timber stairs (4.4) and its joints (10.1).', B7, S7)
B7b = add('7', 'b', '(b)', T7B,
          [row('safety', 'Design details (3 x 2 marks)', 6, 'Any three, 2 each, indicated on the drawing. Such as: maximum pitch 42°; minimum going 220 mm; maximum rise 200 mm; a Ø100 mm sphere must not pass between balusters; minimum handrail height 840 mm; at most 16 risers in a flight; minimum width 800 mm.')],
          *STAIRS, 'q7-section', 'Stairs: rise, going, handrail, height and headroom (4.4).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p39 (printed 36): (a) three considerations × (3 + 3) = 18; (b) layout notes 10, sketch 10, any three dimensions 6 = 26; (c) alternative system notes 8 + sketch 8 = 16. Complete 60.'
S8 = 'Considerations and the alternative method are open responses; the scheme gives three alternative systems as examples.'
DRAIN = (['cons-5-5'], ['drainage'])
T8A = 'Discuss three considerations to ensure the proper treatment and disposal of sewage when selecting a site for a house in a rural location.'
T8B = 'The drawing shows a site layout map. The outline of a new house and driveway is shown on site A. Using notes and freehand sketches, show the design layout necessary for a typical wastewater treatment system and percolation area on this site. Include typical dimensions for the system.'
T8C = 'Using notes and freehand sketches, discuss an alternative method, other than a typical percolation area to ensure the safe treatment of wastewater from a dwelling house.'
A8 = add('8', 'a', '(a)', T8A,
         [row(f'consideration-{i}', f'Consideration {i} - (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: the soil type and how well it percolates; the topography of the site.'),
             (2, 'A second, different consideration. Such as: a high water table risking contamination; distances to neighbouring buildings, roads, rivers, lakes and water sources.'),
             (3, 'A third, different consideration. Such as: the number of residents and a tank of at least 2725 litres; pipework at 1:60 with a vented soil pipe; odours.')]],
         ['cons-5-5', 'cons-1-3'], ['drainage', 'planning-sustainability-environment'], None, 'Septic tanks and percolation (5.5) in choosing a site (1.3).', B8, S8)
B8b = add('8', 'b', '(b)', T8B,
          [row('notes', 'Notes', 10, 'Notes on the layout of dwelling, tank and percolation area, as in the scheme’s model map.'),
           row('sketch', 'Sketch', 10, 'Freehand sketch of the treatment system and percolation area on site A.'),
           row('dimensions', 'Dimensions - Any three', 6, 'Any three, 2 each. Such as: pipes 100–110 mm; septic tank at least 7 m from the house; percolation area at least 10 m from the house; percolation pipe at most 18 m long; trenches at least 2 m apart; at least 3 m to the boundary and 4 m to a road.')],
          *DRAIN, 'q8-layout', 'Septic tanks and laying drains (5.5).', B8, S8)
C8 = add('8', 'c', '(c)', T8C,
         [row('notes', 'Notes', 8, 'Notes on one alternative system. Such as: a raised percolation area with imported topsoil mounded over the ground; a constructed wetland (reed bed); a peat filter system dosed from the septic tank.'),
          row('sketch', 'Sketch', 8, 'Freehand sketch of the alternative system.')],
         *DRAIN, 'q8-alternative', 'Wastewater treatment (5.5).', B8, S8)
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-layout', B8, S8, parts(('a', T8A), ('b', T8B), ('c', T8C)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p40 (printed 37): (a) the three circled locations × (notes 8 + sketches 8) = 48; (b) two impacts × (3 + 3) = 12. Complete 60.'
S9 = 'Every circled location in (a) is required, each separately marked under the scheme’s heading for it; not a choice.'
T9A = 'Using notes and freehand sketches, show best practice design detailing that will prevent the formation of a thermal bridge at each location circled on the drawing.'
T9B = 'Discuss two negative impacts of thermal bridging as a result of poor design detailing.'
A9 = add('9', 'a', '(a)', T9A,
         [row('wallplate', 'Wallplate position detail', 16, 'Notes 8 and sketches 8, as in the scheme’s model detail: the ceiling insulation carried over the wallplate to meet the cavity insulation, with ventilation kept at the eaves.'),
          row('door-head', 'Head of door detail', 16, 'Notes 8 and sketches 8, as in the scheme’s model detail: the cavity insulation carried down over the lintels to the thermally broken frame, with a cavity closer at the head.'),
          row('threshold', 'Threshold of door detail', 16, 'Notes 8 and sketches 8, as in the scheme’s model detail: the floor and cavity insulation linked under the threshold with insulating blocks, the frame in line with the insulation and a drainage channel outside.')],
         ['cons-6-2', 'cons-3-10', 'cons-3-7', 'cons-4-2'], ['heat-loss-insulation', 'roofs', 'doors', 'floors'], 'q9-details',
         'Thermal bridges (6.2) at the eaves wallplate (3.10), the door head and threshold (3.7) and the ground floor junction (4.2).', B9, S9)
B9b = add('9', 'b', '(b)', T9B,
          [row(f'impact-{i}', f'Impact {i} - (3 for point, 3 for discussion)', 6, note) for i, note in [
              (1, 'Point 3 and discussion 3. Such as: warm air meeting the cold surface condenses, and mould grows on the damp surfaces, harming health.'),
              (2, 'A second, different impact. Such as: staining and decay of finishes and materials; more heat lost and a higher energy demand.')]],
          ['cons-6-2', 'cons-6-6'], ['heat-loss-insulation', 'condensation-air-tightness'], None, 'Thermal bridges (6.2) and surface condensation (6.6).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b], 'q9-details', B9, S9, parts(('a', T9A), ('b', T9B)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p41 (printed 38): (a) three considerations × (notes 4 + sketches 4) = 24; (b) three retrofit upgrades × (notes 4 + sketches 4) = 24; (c) two advantages × (3 + 3) = 12. Complete 60.'
S10 = 'No printed choice: part (b) develops each consideration given in (a). The OR alternative is a separate Question 10 route.'
ENERPHIT = (['cons-6-2', 'cons-6-5', 'cons-6-4'], ['passive-design'])
T10A = 'Using notes and freehand sketches, outline three design considerations necessary to achieve the EnerPHit Passive House design standard.'
T10B = 'Discuss in detail, using notes and freehand sketches, how you would retrofit the given house to include each consideration you specified at 10(a) above.'
T10C = 'Discuss two advantages of retrofitting an existing house to meet the EnerPHit standard.'
A10 = add('10', 'a', '(a)', T10A,
          [row(f'consideration-{i}', f'Design consideration {i}', 8, note) for i, note in [
              (1, 'Notes 4 and sketches 4. Such as: the thermal efficiency of the envelope — insulation, windows, doors, porch.'),
              (2, 'A second, different consideration. Such as: ventilation with heat recovery; airtightness (EnerPHit: 1.0 air changes per hour).'),
              (3, 'A third, different consideration. Such as: maximising solar gains; optimum thermal comfort (heating demand 25 kWh/m²/yr); renewable energy systems.')]],
          *ENERPHIT, None, 'Passive design: insulation (6.2), ventilation (6.5) and solar gain (6.4).', B10, S10)
B10b = add('10', 'b', '(b)', T10B,
           [row(f'upgrade-{i}', f'Retrofit upgrade {i}', 8, note) for i, note in [
               (1, 'Notes 4 and sketches 4, for the first consideration. Such as: more insulation in walls, roof (ceiling U ≤ 0.120) and floor; Passive House triple-glazed windows (Uw ≤ 0.85) and doors (Ud ≤ 0.80).'),
               (2, 'Notes 4 and sketches 4, for the second consideration. Such as: a heat recovery ventilation system (efficiency ≥ 75%); sealing penetrations and frames, a stove in place of the open fire, a storm porch.'),
               (3, 'Notes 4 and sketches 4, for the third consideration. Such as: new south windows and the dining/kitchen wall removed for solar gain; upgraded heating controls; PV, a wind turbine or evacuated tubes.')]],
           *ENERPHIT, 'q10-retrofit', 'Passive design: insulation (6.2), ventilation (6.5) and solar gain (6.4).', B10, S10)
C10 = add('10', 'c', '(c)', T10C,
          [row(f'advantage-{i}', f'Impact {i} – (3 for name, 3 for discussion)', 6, note) for i, note in [
              (1, 'Name 3 and discussion 3. Such as: reduced heating costs; better energy efficiency.'),
              (2, 'A second, different advantage. Such as: reduced carbon emissions; improved wellbeing; existing buildings reused in the community.')]],
          ['cons-6-3', 'cons-1-2'], ['heat-loss-insulation', 'sustainability-the-environment'], None, 'Running costs (6.3) and sustainability (1.2).', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-retrofit', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p42 (printed 39): discussion of the statement, three points × (4 + 6) = 30; three best practice guidelines × (4 + 6) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the EnerPHit question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately, so each is its own task and the complete card composes them.'
TAA = 'Discuss the above statement in detail.'
TAB = 'Propose three best practice guidelines that would ensure that buildings are built in the most sustainable way possible and thus minimise their carbon footprint.'
TALL = 'Discuss the above statement in detail and propose three best practice guidelines that would ensure that buildings are built in the most sustainable way possible and thus minimise their carbon footprint.'
GREEN = (['cons-1-2', 'cons-6-4'], ['sustainability-the-environment'])
AA = add('10', 'discussion', ' — discussion', TAA,
         [row(f'point-{i}', f'Discussion: Point {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: global warming from human CO₂ emissions — melting ice caps, extreme weather, forest fires, food and health security.'),
             (2, 'Point 4 and discussion 6. Such as: sustainable development as defined by the Brundtland Report; the Paris Agreement’s targets to hold warming below 2 °C.'),
             (3, 'Point 4 and discussion 6. Such as: the built environment causing about half of climate damage; personal carbon footprints cut by consuming less and choosing local, low-embodied-energy, natural materials. Three distinct, well-argued points are needed.')]],
         *GREEN, None, 'Sustainable design of the built environment (1.2, 6.4).', BALT, SALT, alt=True)
AB = add('10', 'guidelines', ' — guidelines', TAB,
         [row(f'guideline-{i}', f'Guideline {i}: (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: grant-aided renewable energy — solar panels, on-site generation, small wind turbines; heat pumps; energy-saving fittings and A-rated appliances.'),
             (2, 'Point 4 and discussion 6. Such as: planning regulations and clear local guidelines for sustainable homes; on-site water harvesting.'),
             (3, 'Point 4 and discussion 6. Such as: designing out high-embodied-energy materials like concrete and steel; training professionals in airtight, low-energy construction with materials such as cob, rammed earth and hemp-lime. Three distinct guidelines are needed.')]],
         *GREEN, None, 'Sustainable design of the built environment (1.2, 6.4).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, TALL, labels=['Discussion of the statement', 'Three best practice guidelines'], alt=True)

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and any four of the other nine (300 marks); all question banks retained, no full-exam Cartesian cards.'),
          (2, 'Select', 'Q2(c) "Select a different roofing material for each": an open choice of material for every profile, not a closed choice.'),
          (3, 'one of', 'Q4 stem narrative ("purchased one of the houses"): not a candidate choice.'),
          (3, 'one of', 'Q4(a) narrative ("refurbishing one of the townhouses"): not a candidate choice.'),
          (3, 'Select', 'Q4(b) closed choose-two of the three printed areas: one card with an any-two group (choice is not a route).'),
          (3, 'any two', 'Q4(b) closed choose-two of the three printed areas: the same any-two group.'),
          (7, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.'),
          (7, 'One of', 'Alternative Question 10 quotation narrative ("One of the main culprits"): not a candidate choice.'),
          (7, 'or', 'Alternative Question 10 quotation narrative ("directly or indirectly"): not a candidate choice.')]
FINITE = {'4b': dict(choose=2, options=[h for h, _ in AREAS], cardId=A4b['id'], groupRowId='areas')}
REASONS = {
    'q1-b': 'Reshaped to the printed row "wrap around DPC"; tariff unchanged (4).',
    'q2-a': 'Split into three requirements, each notes 3 + sketches 3; tariff unchanged (18).',
    'q2-c': 'Split into the three printed material rows (identify 2, advantage 1, disadvantage 1); tariff unchanged (12).',
    'q3-a': 'Split into the three printed considerations (3 + 3 each); tariff unchanged (18).',
    'q3-b': 'Rebuilt to the printed rows — layout 14, three design considerations 3 each, justification 3: 9 → 26.',
    'q4-a': 'Split into the three printed benefits (4 + 4 each); tariff unchanged (24).',
    'q5-a': 'Rebuilt to the ten printed points (3 each), including both surface resistances: 27 → 30.',
    'q5-b': 'Reshaped to the five printed calculation steps (3 each) with the scheme’s worked answer (€199.60); tariff unchanged (15).',
    'q5-c': 'Reshaped to the five printed calculation steps (3 each) with the scheme’s worked answer (147 mm); tariff unchanged (15).',
    'q6-a': 'Split into three design features, each notes 5 + sketches 5; tariff unchanged (30).',
    'q6-b': 'One row per printed technology (notes/discussion 3 + sketch 3), each named by its scheme heading; tariff unchanged (18).',
    'q6-c': 'Split into the two printed advantages (3 + 3 each); tariff unchanged (12).',
    'q7-a': 'Adds the three printed dimensions (6) and the scale and drafting allowance (8, banded 8/6/4) to the eight details: 40 → 54.',
    'q7-b': 'Reshaped to the printed row "Design details (3 x 2 marks)"; tariff unchanged (6).',
    'q8-a': 'Split into the three printed considerations (3 + 3 each); tariff unchanged (18).',
    'q8-b': 'Rebuilt to the printed rows — notes 10, sketch 10, any three dimensions 6: 20 → 26.',
    'q8-c': 'Reshaped to the printed notes 8 + sketch 8 for one alternative system; tariff unchanged (16).',
    'q9-b': 'Split into the two printed impacts (3 + 3 each); tariff unchanged (12).',
    'q10-a': 'Split into three considerations, each notes 4 + sketches 4; tariff unchanged (24).',
    'q10-b': 'One row per retrofit upgrade, each developing a consideration from (a), notes 4 + sketches 4; the paper requires each consideration, so there is no choice; tariff unchanged (24).',
    'q10-c': 'Split into the two printed advantages (3 + 3 each); tariff unchanged (12).',
}
D.finish(LEDGER, FINITE, REASONS)
