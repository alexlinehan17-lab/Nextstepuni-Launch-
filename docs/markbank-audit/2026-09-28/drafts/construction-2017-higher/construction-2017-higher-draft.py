"""Draft the 2017 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 27-37; the English scheme carries Irish running headers). Q4(b) "select any two of the above
wall types" and Q10(a) "any two of the following" are ONE card each with an any-two group over the
three printed items (choice is not a route). The 25 pre-audit 2017 Higher cards keep their IDs and
concept IDs and are corrected in place; their thirteen build-time overrides are retired.
Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Solid and suspended timber floors at a cavity wall', concept='solid-suspended-floor-section',
              stem='A dwelling house has an open-plan kitchen and dining area on the ground floor, as shown. The kitchen has a solid concrete floor with a 20 mm tile finish. The adjoining dining area has a suspended timber floor with a 20 mm tongue and groove hardwood finish on 200 mm × 40 mm joists. Both floors are highly insulated. The external wall of the house is a 400 mm concrete block wall with a full-fill insulated cavity.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the cross-ventilation detail in (b) is marked separately.'),
    '2': dict(page=2, title='A bathroom for lifetime use', concept='lifetime-bathroom', stem='',
              note='Original plan retained. All four printed fittings in (c) and the sewer-gas detail are required, each separately marked.'),
    '3': dict(page=2, title='Extending a 1950s farmhouse', concept='farmhouse-extension',
              stem='The drawing shows the ground floor plan and the front elevation of a farmhouse built in the 1950s. The dimensions shown are in millimetres. The walls are of random rubble construction and are rendered. The rear wall A-A is south facing. The owners intend to build a single-storey extension, not greater than 12.0 m2 in area, to the rear of the kitchen. Consideration at the design stage is to be given to: optimising daylight into both the extension and the kitchen; providing an open-plan kitchen/dining/living space.',
              note='Original plan and elevation retained. Both printed requirements are required in the layout, each separately marked.'),
    '4': dict(page=3, title='High performance external walls', concept='external-wall-types', stem='',
              note='Original sketch retained. Part (b) is a closed choice of any two of the three printed wall types: one card holding all three. Part (c) discusses the two walls selected in (b).'),
    '5': dict(page=3, title='Hollow block wall U-value, insulation thickness and heat-loss cost', concept='hollow-block-wall-u-value',
              stem='The external wall of a house built in the 1970s is of single-leaf, hollow-block construction with an external render. Plasterboard, with bonded expanded polystyrene, is fixed to the internal surface of the wall, as shown.',
              note='All printed data are retained in the original question. Part (b) uses the data from (a); the scheme’s worked answers are U = 0.869 W/m²°C, 204.08 mm of expanded polystyrene and an annual cost of €47.99.'),
    '6': dict(page=4, title='An eco-friendly timber frame house', concept='eco-friendly-house',
              stem='The drawing shows a dwelling house, which has two bedrooms and a bathroom upstairs. The house is of timber frame construction with an external rainscreen of native larch. The house is designed to be eco-friendly.',
              note='Original elevation and plan retained. Features and additions are open responses; the scheme lists typical examples.'),
    '7': dict(page=4, title='Trussed rafter roof on timber frame walls', concept='trussed-rafter-roof-section',
              stem='The slated roof of a new house is constructed using prefabricated trussed rafters and has a pitch of 45 degrees. The internal span of the house is 4.0 metres. The roof is supported on external walls of timber frame construction, having a rendered concrete block external leaf. Both the roof and the walls are highly insulated.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the roof dimensions in (b) are marked separately.'),
    '8': dict(page=4, title='Kitchen lighting, window area and glazing technology', concept='lighting-glazing',
              stem='', note='Original sketches retained. Part (b) is a calculation; the scheme’s worked answer is a window area of 8.4 m².'),
    '9': dict(page=5, title='Reinforced strip foundation and concrete quality', concept='foundation-concrete-quality', stem='',
              note='Original sketch retained. All four printed stages in (b) are required, each separately marked; the scheme accepts either the slump test or the cube test in (c).'),
    '10': dict(page=5, title='Passive House principles and an MHRV system', concept='passive-house-mhrv', stem='',
               note='Original plan retained. Part (a) is a closed choice of any two of the three printed items: one card holding all three.'),
}
ALT = dict(page=5, title='Adapting and reusing heritage buildings (alternative Question 10)', concept='heritage-reuse',
           stem='While there are undoubtedly many buildings whose heritage values dictate that they should be preserved unchanged, the reality is that few are of such importance that they and their settings are not capable of being remodelled to accommodate new uses - especially where they have outlived the functions for which they were constructed, and where adaptation and reuse is the most viable option for extending their lifespans and preserving the vitality of their urban locations. The alternative is to let them fall into disuse and disrepair, along with the ensuing deterioration of their urban environments. Adapted from: Use it or Lose it - Challenges in the Protection of Architectural Heritage – by Paul Keogh. VOL 6 IRISH ARCHITECTURE - THE RIAI ANNUAL REVIEW 2015/2016. ISBN: 978-0-9567493-5-2 Published by: The Royal Institute of Architects of Ireland, 8 Merrion Square, Dublin 2.',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately.')
SCHEME_PAGES = {'1': [4, 5, 27], '2': [5, 6, 28], '3': [7, 8, 9, 29], '4': [9, 10, 11, 30], '5': [12, 13, 31], '6': [13, 14, 15, 32],
                '7': [16, 17, 33], '8': [17, 18, 19, 34], '9': [19, 20, 21, 35], '10': [21, 22, 23, 36], '10-alt': [24, 25, 37]}
D = cp.Draft(HERE, 2017, 'higher', ('3751ae5b7139751f60b07b1c367487cabe10aa77c7953d60b762787498cf8804',
                                    '822396a75a761c0401757fdb5b6a7334fd49f049525c844b7b9437d8df9e299c'), 25, QUESTIONS, SCHEME_PAGES, alt=ALT)
row, add, compose, parts, anyn = D.row, D.add, D.compose, D.parts, D.anyn
BAND8 = [0, 4, 6, 8]
D.figures({
    'q1-original': D.paper(2, [30, 39, 580, 282]), 'q2-original': D.paper(2, [30, 282, 580, 545]),
    'q3-original': D.paper(2, [30, 545, 580, 800]), 'q4-original': D.paper(3, [30, 39, 580, 315]),
    'q5-original': D.paper(3, [30, 315, 580, 800]), 'q6-original': D.paper(4, [30, 39, 580, 300]),
    'q7-original': D.paper(4, [30, 300, 580, 520]), 'q8-original': D.paper(4, [30, 520, 580, 800]),
    'q9-original': D.paper(5, [30, 39, 580, 302]), 'q10-original': D.paper(5, [30, 302, 580, 565]),
    'q10-alt-original': D.paper(5, [30, 590, 580, 800]),
    'q1-section': D.composite((4, [45, 56, 575, 800]), (5, [45, 56, 575, 509])),
    'q2-requirements': D.scheme(5, [45, 509, 575, 790]), 'q2-advantages': D.scheme(6, [45, 56, 575, 270]), 'q2-layout': D.scheme(6, [28, 270, 575, 790]),
    'q3-layout': D.scheme(7, [45, 56, 575, 390]), 'q3-reasons': D.composite((7, [45, 390, 575, 760]), (8, [45, 56, 575, 212])),
    'q3-advantages': D.composite((8, [45, 212, 575, 765]), (9, [45, 56, 575, 176])),
    'q4-requirements': D.composite((9, [45, 174, 415, 200]), (9, [45, 200, 575, 420]), (9, [45, 420, 455, 446])),
    'q4-walls': D.composite((9, [45, 433, 575, 785]), (10, [45, 56, 575, 240])),
    'q4-discussion': D.composite((10, [45, 240, 575, 790]), (11, [45, 56, 575, 755])),
    'q5-calculation': D.scheme(12, [45, 56, 575, 340]), 'q5-thickness': D.scheme(12, [45, 342, 575, 505]),
    'q5-cost': D.composite((12, [45, 505, 575, 790]), (13, [45, 56, 575, 205])),
    'q6-advantages': D.scheme(13, [45, 215, 575, 475]), 'q6-features': D.composite((13, [45, 477, 575, 785]), (14, [45, 56, 575, 326])),
    'q6-operating': D.composite((14, [45, 326, 575, 790]), (15, [45, 56, 575, 495])),
    'q7-section': D.composite((16, [45, 56, 575, 700]), (17, [30, 56, 575, 370])),
    'q8-light': D.scheme(17, [45, 370, 575, 790]), 'q8-window': D.composite((18, [45, 56, 575, 415]), (18, [45, 415, 400, 437])),
    'q8-glazing': D.composite((18, [45, 412, 575, 790]), (19, [45, 56, 575, 205])),
    'q9-foundation': D.scheme(19, [45, 207, 575, 590]),
    'q9-concrete': D.composite((19, [45, 460, 385, 620]), (19, [45, 620, 575, 785]), (20, [45, 56, 575, 415])),
    'q9-test': D.composite((20, [30, 415, 430, 430]), (20, [30, 430, 575, 775]), (21, [45, 56, 575, 440])),
    'q10-principles': D.composite((21, [45, 441, 575, 790]), (22, [45, 56, 575, 816])),
    'q10-mhrv': D.composite((23, [45, 56, 575, 285]), (23, [45, 430, 575, 800])), 'q10-advantages': D.scheme(23, [45, 288, 575, 428]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p27 (printed 25): (a) twelve points × 4 (drawing 3, annotation 1) — best eight from the foundation and external wall, best four from the suspended timber floor = 48, scale and drafting 8 (8/6/4): 56; (b) cross-ventilation detailing 4. Complete 60.'
S1 = 'One required section and one required ventilation detail. The detail lists are marking menus, not printed choices.'
T1A = 'To a scale of 1:10, draw a vertical section through the external wall of the kitchen and through both the concrete and timber floors. Show the typical construction details from the bottom of the strip foundation to a level 400 mm above the finished floor and include the abutment of both floors. Show a width of 1.5 metres for each floor. Note: It is not necessary to show the kitchen cabinets or the furniture.'
T1B = 'On your drawing show the typical design detailing for the cross ventilation of the suspended timber floor through the solid concrete floor.'
A1 = add('1', 'a', '(a)', T1A,
         [row('wall', 'foundation and external wall', 32, 'Best eight points, 4 each (drawing 3, annotation 1). Menu: R.C. foundation; dead blockwork and cavity wall above floor level; wall insulation and thermal block; external and internal render; stepped DPC and DPC at floor level; lintels and vent for ducting; hardcore and sand blinding; radon barrier/DPM; concrete floor detail; perimeter and floor insulation; floor tiles and skirting.', list(range(0, 33, 4))),
          row('timber-floor', 'Suspended timber floor', 16, 'Best four points, 4 each. Menu: subfloor under dwarf/tassel walls; radon barrier; hardcore and blinding; dwarf/tassel/sleeper walls; wallplates and DPC; floor joists; floor insulation; floorboards.', list(range(0, 17, 4))),
          row('presentation', 'Scale Drafting (Excellent 8, Good 6, Fair 4)', 8, 'Scale and drafting, assessed together: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-2-4', 'cons-4-2', 'cons-3-3'], ['question-1-drawing-questions', 'foundations', 'floors', 'walls'], 'q1-section',
         'Scaled drawing (1.5) of a strip foundation (2.4) and cavity wall (3.3) with solid and suspended ground floors (4.2).', B1, S1)
B1b = add('1', 'b', '(b)', T1B,
          [row('ventilation', 'Design detailing for cross ventilation', 4, 'Show and identify ducting, rigid or flexible 75–100 mm, through the external wall and the concrete floor to ventilate the timber floor, with a vent on the external wall, as in the scheme’s model sections.')],
          ['cons-4-2', 'cons-6-5'], ['floors', 'wood-rot-ventilation'], 'q1-section', 'Ventilation (6.5) of a suspended timber ground floor (4.2).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p28 (printed 26): (a) two requirements × (note 6 + sketch 6) = 24; (b) two advantages × (3 + 3) = 12; (c) shower, W.C. and wash basin locations, grab rails, dimensions and the sewer-gas detail × 4 = 24. Complete 60.'
S2 = 'All printed fittings and the sewer-gas detail in (c) are required, each separately marked; requirements and advantages are open responses.'
ACCESS = (['cons-5-6', 'cons-1-2'], ['drainage', 'planning-sustainability-environment'])
T2A = 'Discuss in detail, using notes and freehand sketches, two functional requirements of a bathroom designed for lifetime use.'
T2B = 'The drawing shows the ground floor plan of a semi-detached house. The dimensions shown are in millimetres. It is proposed to provide a bathroom suitable for lifetime use by converting the office A into a bathroom. Discuss two advantages of converting the existing office A rather than building a new bathroom at location B, as shown.'
T2C = 'Using notes and freehand sketches, show a proposed design layout for the bathroom at A. On your design sketches, show the location of the shower area, W.C., wash basin and grab rails. Include appropriate dimensions. On a separate sketch, show one design detail that will prevent the penetration of sewer gases into the bathroom at the W.C.'
A2 = add('2', 'a', '(a)', T2A,
         [row(f'requirement-{i}', f'Functional requirement {i}', 12, note) for i, note in [
             (1, 'Note 6 and sketch 6. Such as: a door at least 850 mm wide; a 1500–1800 mm turning circle; a level-access shower with no upstand.'),
             (2, 'A second, different requirement: note 6 and sketch 6. Such as: grab rails at the W.C., shower and basin; a basin at a suitable height with space beneath; lever or sensor taps; non-slip floors; an emergency pull cord.')]],
         *ACCESS, 'q2-requirements', 'Sanitary fitments (5.6) in an accessible layout (1.2).', B2, S2)
B2b = add('2', 'b', '(b)', T2B,
          [row(f'advantage-{i}', f'Advantage {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
              (1, 'Point 3 and discussion 3. Such as: cheaper than a new build; little disruption while the owners live in the house.'),
              (2, 'A second, different advantage. Such as: existing ventilation and access from the vented lobby; the design integrity of the house kept; the back garden and natural light to the utility room undisturbed.')]],
          ['cons-1-2'], ['planning-sustainability-environment'], 'q2-advantages', 'Adapting a house in the built environment (1.2).', B2, S2)
C2 = add('2', 'c', '(c)', T2C,
         [row('fittings', 'Location of shower area Location of W.C. Location of wash basin', 12, 'The shower area, W.C. and wash basin located, 4 each, as in the scheme’s model layouts.'),
          row('grab-rails', 'Grab rails', 4, 'Grab rails at the W.C., shower and basin.'),
          row('dimensions', 'Dimensions of turning circle/door/any 2 dimensions', 4, 'Any two appropriate dimensions, such as the turning circle or door width.'),
          row('sewer-gas', 'Design detail to prevent the penetration of sewer gases', 4, 'On a separate sketch: such as the water seal in the W.C. trap, or a vented stack and branches that keep the seal.')],
         *ACCESS, 'q2-layout', 'Sanitary fitments and the single stack system (5.6) in an accessible layout (1.2).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-layout', B2, S2, parts(('a', T2A), ('b', T2B), ('c', T2C)))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p29 (printed 27): (a) the kitchen/extension layout, optimising daylight (note 8 + sketches 8) and open plan (note 8 + sketches 8) = 32; (b) three reasons × 6 = 18; (c) two advantages × (2 + 3) = 10. Complete 60.'
S3 = 'Both printed design requirements are required in the layout, each separately marked; reasons and advantages are open responses.'
LIGHT = (['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'])
T3A = 'Using notes and freehand sketches show a proposed design layout that incorporates each of the above requirements.'
T3B = 'Discuss three reasons for your proposed design layout.'
T3C = 'Discuss two advantages of building an extension to the farmhouse shown.'
A3 = add('3', 'a', '(a)', T3A,
         [row('daylight', 'Optimising daylight', 16, 'Note/annotation 8 and sketches 8. Such as: glazing to the south, east and west; roof lights over the extension and kitchen; the rear wall opened up with lintels; high-performance low-e triple glazing.'),
          row('open-plan', 'Open plan', 16, 'Note/annotation 8 and sketches 8. Such as: the rear window removed and an opening formed to link the kitchen/dining area with the new living space; sliding or folding doors to the garden.')],
         *LIGHT, 'q3-layout', 'Layout design (1.2) for good daylighting (7.4).', B3, S3)
B3b = add('3', 'b', '(b)', T3B,
          [row(f'reason-{i}', f'Reason {i}', 6, note) for i, note in [
              (1, 'Such as: glazing to the south and west for long sunshine into the room and the existing house.'),
              (2, 'A second, different reason. Such as: the existing small windows limit solar gain; low-e glazing brings light and heat into the extension and house.'),
              (3, 'A third, different reason. Such as: open plan lets sunlight into the main house; bringing the outside in through sliding doors; flexible spaces for changing needs.')]],
          *LIGHT, 'q3-reasons', 'Layout design (1.2) for good daylighting (7.4).', B3, S3)
C3 = add('3', 'c', '(c)', T3C,
         [row('advantage-1', 'Advantage 1 (2 point,3 discussion)', 5, 'Point 2 and discussion 3. Such as: extending keeps the character of a good vernacular house; services, roads and the garden already exist.'),
          row('advantage-2', 'Advantage 2 (2 point, 3 discussion)', 5, 'A second, different advantage. Such as: modest, low-impact construction while the occupants live in the house; an exemplar for others with vernacular buildings.')],
         ['cons-1-1', 'cons-1-2'], ['conservation-restoration'], 'q3-advantages', 'Extending a vernacular building (1.1) in the built environment (1.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-layout', B3, S3, parts(('a', T3A), ('b', T3B), ('c', T3C)))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p30 (printed 28): (a) three requirements × (note and sketch 4 + 4) = 24; (b) any two of three printed wall types × (note 5, sketch 5, dimensions 2) = 24; (c) the two walls selected, each environmental consideration 3 and ease of construction 3 = 12. Complete 60.'
S4 = 'Choice is not a route: part (b) (select any two of the three printed wall types) is ONE card with an any-two group over the scheme headings; its figure carries all three walls’ drawings. Part (c) discusses the two walls the candidate selected in (b), so it is one task, not a choice.'
WALLS = (['cons-3-3', 'cons-3-2'], ['walls'])
T4A = 'Discuss, using notes and freehand sketches, three functional requirements of an external wall suitable for a new dwelling house.'
T4B = 'When specifying a high performance external wall for a new house, a choice is to be made between: a rendered cavity wall of concrete block construction or a wall of timber frame construction with a rainscreen of cedar cladding, as shown or a rendered wall of timber frame and hemp-lime construction. Select any two of the above wall types, and using notes and freehand sketches, show the typical design detailing for each wall type selected. Name the typical components of each wall and include typical dimensions.'
T4C = 'Discuss the construction of each wall type selected under the following headings: environmental considerations; ease of construction.'
A4 = add('4', 'a', '(a)', T4A,
         [row(f'requirement-{i}', f'Functional requirement {i} (Note and Sketch)', 8, note) for i, note in [
             (1, 'Note 4 and sketch 4. Such as: keep the occupants safe, dry, warm and sheltered; prevent heat transfer.'),
             (2, 'A second, different requirement. Such as: reduce noise; carry the roof and floors and spread the loads to the foundations; robust openings for doors and windows.'),
             (3, 'A third, different requirement. Such as: no cold bridges and low embodied energy; prevent condensation, interstitial dampness and uncontrolled air movement; keep out water and vermin; durable and in keeping with the surroundings.')]],
         *WALLS, 'q4-requirements', 'The external envelope (3.2) and external walls (3.3).', B4, S4)
ITEMS4 = [('Concrete block construction', 'a cavity that prevents moisture ingress; full-fill insulation; internal render for airtightness; strong, robust blocks; durable, weather-resistant external plaster.'),
          ('Timber frame construction', 'T&G cedar or lapped larch or Douglas fir on counter battens for weatherproofing and ventilation; a moisture-resistant layer; OSB/plywood racking; full-fill insulation in the frame; an internal airtightness layer and service cavity.'),
          ('Timber frame and hemp-lime construction', 'hempcrete sprayed or cast 300–500 mm thick around a structural timber frame; Heraklith boards at openings; two coats of internal render; an external leaf of hempcrete and hemp-lime render.')]
A4b = add('4', 'b', '(b)', T4B,
          [anyn('walls', 'Choice of high performance wall (any two)', 2, 12, ITEMS4, 'Any two of the three printed wall types, each note 5, sketch 5 and dimensions 2 = 12.')],
          ['cons-3-3', 'cons-3-2', 'cons-6-2'], ['walls', 'heat-loss-insulation'], 'q4-walls',
          'The union of the three printed wall types: a cavity block wall (3.3), and timber frame walls behind a rainscreen (3.2), all highly insulated (6.2).', B4, S4)
C4 = add('4', 'c', '(c)', T4C,
         [row('wall-1', 'Wall type 1', 6, 'For the first wall selected in (b): environmental consideration 3 and ease of construction 3. Such as, block: robust and long lasting but high embodied energy and CO₂ from cement; skilled trades readily available.'),
          row('wall-2', 'Wall type 2', 6, 'For the second wall selected: environmental consideration 3 and ease of construction 3. Such as, timber frame: stores carbon, fast and precise off-site manufacture, but needs maintenance; hemp-lime: fast-growing hemp sequesters CO₂ and breathes, but skills and materials may be scarce.')],
         ['cons-3-3', 'cons-1-2'], ['walls', 'sustainability-the-environment'], 'q4-discussion', 'Wall construction (3.3) and its environmental impact (1.2).', B4, S4)
compose('4', 'complete', ' — complete', [A4, A4b, C4], 'q4-walls', B4, S4, parts(('a', T4A), ('b', T4B), ('c', T4C)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p31 (printed 29): (a) nine points × 3 = 27 (tabulation, two surface resistances, four layers, total resistance, U-value); (b) six steps × 3 = 18; (c) five steps × 3 = 15. Complete 60.'
S5 = 'No printed choice. Part (b) uses the data from (a).'
DATA5 = ('External render thickness 16 mm; Hollow concrete block thickness 215 mm; Expanded polystyrene thickness 25 mm; Plasterboard thickness 12.5 mm.\n'
         'Thermal data of external wall of house: Resistance of external surface (R) 0.048 m2 °C/W; Resistivity of external render (r) 2.170 m °C/W; Resistance of concrete block (R) 0.210 m2 °C/W; '
         'Conductivity of expanded polystyrene (k) 0.037 W/m °C; Conductivity of plasterboard (k) 0.160 W/m °C; Resistance of internal surface (R) 0.104 m2 °C/W.')
T5A = 'Calculate the U-value of the external wall, given the following data: ' + DATA5
T5B = ('It is proposed to upgrade the thermal properties of the above wall, to meet the Passive House standard, by fixing expanded polystyrene to the external surface, as shown. '
       'Using the given thermal data at 5(a) above, calculate the thickness of expanded polystyrene required to achieve a U-value of 0.15 W/m2 °C.')
T5C = ('Calculate the cost of heat lost annually through the upgraded wall at 5(b) above, using the following data: Area of external wall 140 m2; Average internal temperature 18 °C; '
       'Average external temperature 6 °C; U-value of wall 0.15 W/m2 °C; Heating period 8 hours per day, every day, for 36 weeks per annum; Cost of oil 98 cent per litre; '
       'Calorific value of oil 37350 kJ per litre; 1000 Watts 1 kJ per second.')
A5 = add('5', 'a', '(a)', T5A,
         [row('tabulation', 'Tabulation/methodology', 3, 'The calculation set out in a table of material, conductivity, resistivity, thickness and resistance.'),
          row('resistances', 'External surface resistance External render Hollow block Polystyrene Plasterboard Internal surface resistance', 18,
              'Six resistances, 3 each: external surface 0.048 (given); render 0.016 × 2.170 = 0.03472; hollow block 0.210 (given); polystyrene 0.025/0.037 = 0.67568; plasterboard 0.0125/0.160 = 0.078125; internal surface 0.104 (given). All in m²°C/W.', list(range(0, 19, 3))),
          row('total-resistance', 'Total resistance', 3, 'Total resistance Rt = 1.151 m²°C/W.', [0, 3]),
          row('u-value', 'U-Value of external wall (1 mark for formula)', 3, 'U = 1 ÷ Rt = 1 ÷ 1.151 = 0.869 W/m²°C (1 mark for the formula).', [0, 1, 2, 3])],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Thermal resistance, conductivity and transmittance (6.1).', B5, S5)
B5b = add('5', 'b', '(b)', T5B,
          [row('required-resistance', 'Formula U=1/R R value for 0.15 using R=1/U', 6, 'The formula U = 1/R (3) and the required resistance 1 ÷ 0.15 = 6.6666 m²K/W (3).'),
           row('existing-resistance', 'R value for calculated U-Value from part (a)', 3, 'Existing resistance = 1.151 m²K/W.'),
           row('difference', 'Difference in resistances (required resistance)', 3, 'Difference = 6.6666 − 1.151 = 5.5156 m²K/W.'),
           row('formula', 'Application of formula R = T/k', 3, 'R = T/k, so 5.5156 = T/0.037.'),
           row('thickness', 'Required thickness of insulation', 3, 'T = 5.5156 × 0.037 = 0.20408 m: 204.08 mm of expanded polystyrene (204–205 mm accepted).')],
          ['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation'], 'q5-thickness', 'Thermal transmittance (6.1) and insulating materials (6.2).', B5, S5)
C5 = add('5', 'c', '(c)', T5C,
         [row('heat-loss', 'Heat loss formula and calculation', 3, 'Heat loss = U-value × area × temperature difference = 0.15 × 140 × 12 = 252 watts (joules per second).'),
          row('duration', 'Heating duration for one year', 3, 'Heating period = 60 × 60 × 8 × 7 × 36 = 7,257,600 seconds (2,016 hours).'),
          row('energy', 'k/Joules calculation for one year', 3, 'Energy = 7,257,600 × 252 ÷ 1000 = 1,828,915.2 kJ per year.'),
          row('oil', 'Litres of oil for one year', 3, 'Oil = 1,828,915.2 ÷ 37,350 = 48.9669 litres per year.'),
          row('cost', 'Annual cost of heat loss', 3, 'Annual cost = 48.9669 × €0.98 = €47.99. The scheme’s alternative one-line method gives the same €47.99.')],
         ['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations'], 'q5-cost', 'Heat loss calculation and running costs (6.3) from the U-value (6.1).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p32 (printed 30): (a) two advantages × 5 = 10; (b) three features × (note and sketch 5 + 5) = 30; (c) two added features × (note and sketch 5 + 5) = 20. Complete 60.'
S6 = 'Advantages and features are open responses with no printed list; the scheme lists typical examples.'
T6A = 'Discuss in detail two advantages of eco-friendly house design in the 21st century.'
T6B = 'Using notes and freehand sketches, discuss in detail three features of the given design that contribute to making the house eco-friendly.'
T6C = 'Low operating costs are an important consideration in eco-friendly design. Using notes and freehand sketches, discuss two features that could be added to the design that would further reduce the operating costs of the house.'
A6 = add('6', 'a', '(a)', T6A,
         [row(f'advantage-{i}', f'Advantage {i}', 5, note) for i, note in [
             (1, 'Such as: an ethical way of living — no sustainable planet without sustainable buildings; fossil fuels are diminishing.'),
             (2, 'A second, different advantage. Such as: buildings consume about 40% of total energy, so doing much more with much less matters; materials transported less.')]],
         ['cons-1-2'], ['sustainability-the-environment'], 'q6-advantages', 'Sustainable design of the built environment (1.2).', B6, S6)
B6b = add('6', 'b', '(b)', T6B,
          [row(f'feature-{i}', f'Feature {i} (Note and Sketch)', 10, note) for i, note in [
              (1, 'Note 5 and sketch 5. Such as: built almost entirely of renewable, low-embodied-energy timber; native larch cladding that needs no preservatives.'),
              (2, 'A second, different feature. Such as: large south-facing glazing for solar gain and no windows to the north; external storage to the north as a buffer zone.'),
              (3, 'A third, different feature. Such as: the stove against an inner chimney stack of high thermal mass; a compact open-plan form with no corridors; short pipe runs.')]],
          ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-features',
          'Low-impact design of the built environment (1.2), solar gain (6.4) and insulation (6.2).', B6, S6)
C6 = add('6', 'c', '(c)', T6C,
         [row(f'feature-{i}', f'Feature {i} (Note and Sketch)', 10, note) for i, note in [
             (1, 'Note 5 and sketch 5. Such as: a storm porch at the entrance; zoning doors; larger windows and roof lights on the south façade.'),
             (2, 'A second, different feature. Such as: evacuated tubes for up to 60% of hot water; PV panels; a wind generator; rainwater harvesting.')]],
         ['cons-6-3', 'cons-6-4'], ['heat-loss-insulation', 'sustainability-the-environment'], 'q6-operating', 'Running costs (6.3) and solar gain (6.4).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-features', B6, S6, parts(('a', T6A), ('b', T6B), ('c', T6C)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p33 (printed 31): (a) twelve points × 4 (drawing 3, annotation 1) — best six roof details 24, best five wall details 20, both walls 4 — and scale and drafting 8 (8/6/4) = 56; (b) three typical roof dimensions (3 × 1 + 1) = 4. Complete 60.'
S7 = 'One required section and three required dimensions. The detail lists are marking menus, not printed choices.'
T7A = 'To a scale of 1:10, draw a vertical section through the roof structure. Show the typical construction details from a level 400 mm below the ceiling up to ridge level, and include both external walls. Show the typical design detailing at one of the eaves and include battens, membranes and four courses of slate at eaves. Label the components.'
T7B = 'On your drawing show the typical dimensions of three roof members.'
A7 = add('7', 'a', '(a)', T7A,
         [row('roof', 'Roof Details (any 6 × 4 marks)', 24, 'Best six, 4 each. Menu: ridge level apex; four courses of slates; battens 50 × 30–40 mm; breather membrane and tilting fillet; prefabricated trusses at 400–600 mm centres; 300–600 mm insulation at the ceiling; gypsum plasterboard; fascia, soffit and gutter; ventilation.', list(range(0, 25, 4))),
          row('wall', 'Wall Details (any 5 × 4 marks)', 20, 'Best five, 4 each. Menu: doubled 200 × 50 headplate; 200 × 50 studs at 400 mm centres; insulated service cavity; sealed vapour barrier; 12.5 mm plasterboard and skim; airtight tape at the wall–ceiling junction; 200 mm insulation; 9–20 mm OSB or plywood racking; taped breather membrane; vapour diffusion cavity, wall ties and cavity closer; 100 mm block outer leaf; 15–20 mm render.', list(range(0, 21, 4))),
          row('both-walls', 'Both walls', 4, 'Both external walls shown.'),
          row('presentation', 'Scale & Drafting (Excellent, good, fair)', 8, 'Scale and drafting, assessed together: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-3-8', 'cons-3-9', 'cons-3-10', 'cons-3-3'], ['question-1-drawing-questions', 'roofs', 'walls'], 'q7-section',
         'Scaled drawing (1.5) of a trussed rafter roof (3.8) with its covering and insulation (3.9) at the eaves (3.10) on timber frame walls (3.3).', B7, S7)
B7b = add('7', 'b', '(b)', T7B,
          [row('dimensions', 'Typical dimensions', 4, 'Typical dimensions of three roof members (3 × 1 + 1), such as battens 50 × 40 mm and trussed rafters 150–200 × 40 mm at 600 mm centres.')],
          ['cons-3-8'], ['roofs'], 'q7-section', 'Roof members (3.8).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p34 (printed 32): (a) natural light and artificial light × (note and sketch 4 + 4) = 16; (b) six steps × 3 and the window area 2 = 20; (c) three advancements × (note 4 + sketch 4) = 24. Complete 60.'
S8 = 'Both printed light sources in (a) are required. "or any other suitable method" in (b) is an open choice of method, marked by the same steps.'
LIGHTING = (['cons-7-4', 'cons-7-2'], ['windows-light'])
T8A = 'Using notes and freehand sketches, discuss the importance of each of the following in providing adequate light on a work surface in a kitchen, as shown: natural light; artificial light.'
T8B = 'A home office, as shown, measures 4.8 metres long by 3.5 metres wide. The office has a vertical window and unobstructed views. An average illumination of 500 lux of daylight is required on the work plane. Determine using the degree of efficiency method, or any other suitable method, the approximate area of glazing required to provide the stated illumination. Assume the illumination of a standard overcast sky to be 5000 lux.'
T8C = 'Using notes and freehand sketches, discuss three advances in glazing technology that make modern glazing systems more energy efficient.'
A8 = add('8', 'a', '(a)', T8A,
         [row('natural', 'Natural light (Note and Sketch)', 8, 'Note 4 and sketch 4. Such as: windows placed to light the countertops without glare; roof lights or light tunnels; natural light aids a positive attitude and connects the occupants with the outdoors.'),
          row('artificial', 'Artificial light (Note and Sketch)', 8, 'Note 4 and sketch 4. Such as: task lighting at sinks, worktops and hobs; energy-efficient strip LEDs; sensor lighting; diffused light that softens the room.')],
         *LIGHTING, 'q8-light', 'Conditions for good illumination (7.4).', B8, S8)
B8b = add('8', 'b', '(b)', T8B,
          [row('formula', 'Formula Correct entry into formula', 6, 'The formula Li = Lo × WF × E × (window area) ÷ floor area (3), with the values entered correctly: Li = 500, Lo = 5000, WF = 0.5 for a vertical window, E = 0.4 (3).'),
           row('floor-area', 'Floor area', 3, 'Floor area = 4.8 × 3.5 = 16.8 m².'),
           row('product', 'Lo × WF × E', 3, 'Lo × WF × E = 5,000 × 0.5 × 0.4 = 1,000.'),
           row('solve', 'Solve for w (window area) line 1 Solve for w (window area) line 2', 6, 'Solving for W: 500 × 16.8 = 1,000 W, so 8400 = 1000 W (3 each line).'),
           row('area', 'Window area', 2, 'Window area W = 8400 ÷ 1000 = 8.4 m².')],
          ['cons-7-2', 'cons-3-5'], ['windows-light'], 'q8-window', 'The daylight factor and window area (7.2, 3.5).', B8, S8)
C8 = add('8', 'c', '(c)', T8C,
         [row(f'advancement-{i}', f'Advancement {i} (note 4 marks, sketch 4 marks)', 8, note) for i, note in [
             (1, 'Note 4 and sketch 4. Such as: insulated glazing units — double or triple panes sealed with argon or krypton; aerogel.'),
             (2, 'A second, different advance. Such as: low-emissivity glazing — a thin metallic layer that lets short-wave solar radiation in and reflects long-wave heat back into the room.'),
             (3, 'A third, different advance. Such as: dynamic or smart glass — electrochromic or thermochromic; warm edge spacers of insulating plastic composite.')]],
         ['cons-3-6'], ['windows-light'], 'q8-glazing', 'Glass and glazing (3.6).', B8, S8)
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-window', B8, S8, parts(('a', T8A), ('b', T8B), ('c', T8C)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p35 (printed 33): (a) sketch, note, reinforcement, three dimensions and reasons × 4 = 20; (b) mixing, placing, compacting and curing × (note 3 + sketch 3) = 24; (c) one test, note 8 + sketch 8 = 16. Complete 60.'
S9 = 'All four printed stages in (b) are required, each separately marked. "one test" in (c) is an open choice; the scheme gives the slump test and the cube test.'
CONCRETE = 'No Higher outgoing reference heading covers concrete materials and mixing (2.6, 2.7); the card keeps the Foundations association.'
T9A = 'A reinforced concrete strip foundation supports a 400 mm concrete block external wall with an insulated cavity, as shown. Using notes and freehand sketches, show the typical design detailing of the foundation. Indicate the position of the reinforcement in the foundation. Specify three typical dimensions and discuss the reasons for the dimensions you have specified.'
T9B = 'Using notes and freehand sketches, discuss the importance of each of the following to ensure the maximum strength of concrete in the foundation: mixing; placing; compacting; curing.'
T9C = 'Using notes and freehand sketches, describe one test that may be carried out to measure consistency in the quality of all concrete delivered to a site.'
A9 = add('9', 'a', '(a)', T9A,
         [row('sketch', 'Sketch of foundation', 4, 'A sketch of the reinforced strip foundation under the cavity wall, as in the scheme’s model.'),
          row('note', 'Note', 4, 'Notes on the foundation.'),
          row('reinforcement', 'Position of reinforcement', 4, 'Such as: 12 mm mild steel bars near the bottom, tied at junctions, with 50 mm cover against rust and spalling.'),
          row('dimensions', 'Three typical dimensions', 4, 'Such as: 1000–1200 mm below ground; 1200 mm wide (three times the wall thickness); 400 mm deep.'),
          row('reasons', 'Reasons for dimensions specified', 4, 'Such as: below the frost line and on solid subsoil; wide enough to spread the load and for workers to lay blockwork; cover and depth for the reinforcement.')],
         ['cons-2-4', 'cons-2-5'], ['foundations'], 'q9-foundation', 'Strip foundations (2.4) and steel reinforcement (2.5).', B9, S9)
B9b = add('9', 'b', '(b)', T9B,
          [row('mixing', 'Mixing (note and sketch)', 6, 'Note 3 and sketch 3. Such as: aggregates and water free of impurities; accurate batching allowing for bulking; mechanical mixing or ready-mix; protection from frost and sun.'),
           row('placing', 'Placing (note and sketch)', 6, 'Note 3 and sketch 3. Such as: workable enough to place without voids, but no extra water; placed without dropping from height to avoid separation; oiled, watertight formwork.'),
           row('compacting', 'Compacting (note and sketch)', 6, 'Note 3 and sketch 3. Such as: a tamping beam in layers or mechanical vibration to drive out air voids, without touching the formwork.'),
           row('curing', 'Curing (note and sketch)', 6, 'Note 3 and sketch 3. Such as: placed within about thirty minutes; kept damp under hessian or a mist spray; protected from frost with straw, jute or polythene.')],
          ['cons-2-7', 'cons-2-4'], ['foundations'], 'q9-concrete', 'Mixing, placing and curing site concrete (2.7) for a foundation (2.4).', B9, S9)
C9 = add('9', 'c', '(c)', T9C,
         [row('note', 'Note', 8, 'Such as, the slump test: an oiled mould on a level plate filled in three layers, each tamped 25 times; the mould lifted and the slump measured, the same for all batches on the job. Or the cube test: cubes cast in three layers, cured in water and crushed at 7, 14, 21 and 28 days.'),
          row('sketch', 'Sketch', 8, 'Freehand sketches of the test, as in the scheme.')],
         ['cons-2-7', 'cons-2-4'], ['foundations'], 'q9-test', 'Testing site and ready mixed concrete (2.7) for a foundation (2.4).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-concrete', B9, S9, parts(('a', T9A), ('b', T9B), ('c', T9C)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p36 (printed 34): (a) any two of three printed items × (notes 6 + sketches 6) = 24; (b) line diagram, ducting, airflow and description × 6 = 24; (c) two advantages × 6 = 12. Complete 60.'
S10 = 'Choice is not a route: part (a) (any two of three printed items) is ONE card with an any-two group over the scheme headings; its figure and the complete-question figure carry all three items’ drawings. The OR alternative is a separate Question 10 route.'
MHRV = (['cons-6-5'], ['condensation-air-tightness', 'passive-design'])
T10A = 'Using notes and freehand sketches, discuss the importance of any two of the following in Passive House design: airtightness; indoor air quality; solar shading.'
T10B = 'The diagram shows the ground floor plan of a semi-detached house. Also shown is the location M in the hallway, of the Mechanical Heat Recovery with Ventilation (MHRV) unit. Draw a line diagram of the given room layout and show a typical design for the ducting to the MHRV unit. Indicate clearly the direction of the airflow in the ducts and describe how the MHRV system works.'
T10C = 'Discuss two advantages of siting the MHRV unit in the hallway, as shown.'
ITEMS10 = [('Airtightness', 'an airtight layer in the envelope stops air leakage and moisture ingress, improving comfort and insulation; a service cavity protects it; tested by a blower door test to 0.6 air changes per hour.'),
           ('Indoor air quality', 'mechanical ventilation with heat recovery supplies filtered fresh air and extracts warm damp air; humidity 30–60%; CO₂ below 1000 ppm; internal surfaces above 12.6 °C to prevent condensation.'),
           ('Solar shading', 'roof overhangs or brise-soleil cut the high summer sun but admit the low winter sun; blinds, shades, external roller blinds or dynamic glass control overheating.')]
A10 = add('10', 'a', '(a)', T10A,
          [anyn('items', 'Passive house design - any 2', 2, 12, ITEMS10, 'Any two of the three printed items, each notes 6 and sketches 6 = 12.')],
          ['cons-6-5', 'cons-6-4'], ['passive-design', 'condensation-air-tightness'], 'q10-principles',
          'The union of the three printed items: airtightness and indoor air quality (6.5), and solar shading of solar gain (6.4).', B10, S10)
B10b = add('10', 'b', '(b)', T10B,
           [row('diagram', 'Line diagram of room layout', 6, 'A line diagram of the given ground floor plan.'),
            row('ducting', 'Design for ducting to MHRV unit', 6, 'Supply ducts to the living rooms and extract ducts from the kitchen, utility and bathroom, back to the unit M, as in the scheme’s model plan.'),
            row('airflow', 'Direction of airflow in ducts', 6, 'The direction of airflow shown in the ducts.'),
            row('description', 'Description of how system works', 6, 'Such as: a constant supply of fresh pre-heated air while moist air is extracted from wet rooms; the outgoing warm air pre-heats the incoming air in a heat exchanger without mixing; a filter removes dust and pollen.')],
           *MHRV, 'q10-mhrv', 'Mechanical ventilation with heat recovery (6.5).', B10, S10)
C10 = add('10', 'c', '(c)', T10C,
          [row(f'advantage-{i}', f'Advantage {i}', 6, note) for i, note in [
              (1, 'Such as: on an external wall, so the intake and extract ducts run straight out; away from the living rooms and bedrooms, so its noise is not heard.'),
              (2, 'A second, different advantage. Such as: hidden in a press; easy access for maintenance and filter changes; inside the insulation layer, so little heat is lost from the ducts.')]],
          *MHRV, 'q10-advantages', 'Mechanical ventilation (6.5).', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-principles', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p37 (printed 35): discussion of the statement, three points × (4 + 6) = 30; three best practice guidelines × (4 + 6) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the Passive House question. The printed task is one sentence; the scheme marks its discussion and its guidelines separately, so each is its own task and the complete card composes them.'
TAA = 'Discuss the above statement in detail.'
TAB = 'Propose three best practice guidelines that would promote the adaptation and reuse of heritage buildings built after 1800, to prevent them from falling into disuse and disrepair.'
TALL = 'Discuss the above statement in detail and propose three best practice guidelines that would promote the adaptation and reuse of heritage buildings built after 1800, to prevent them from falling into disuse and disrepair.'
HERITAGE = (['cons-1-1', 'cons-1-2'], ['conservation-restoration'])
AA = add('10', 'discussion', ' — discussion', TAA,
         [row(f'point-{i}', f'Discussion – point {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: buildings of distinctive character give villages and towns a sense of place and continuity with the past, and attract tourism.'),
             (2, 'Point 4 and discussion 6. Such as: buildings outlive their original uses — a church without a congregation, a railway station without a line — and without reuse they degrade and are lost.'),
             (3, 'Point 4 and discussion 6. Such as: reuse needs upgrading for heat, fire and universal access, while keeping the original legible and the changes reversible. Three distinct, well-argued points are needed.')]],
         *HERITAGE, None, 'Conserving historic buildings (1.1) in the built environment (1.2).', BALT, SALT, alt=True)
AB = add('10', 'guidelines', ' — guidelines', TAB,
         [row(f'guideline-{i}', 'Recommendation 1 (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6 (the scheme labels each of its three guideline rows "Recommendation 1"). Such as: successful refurbishments promoted as exemplars of best practice.'),
             (2, 'Point 4 and discussion 6, a second, different guideline. Such as: conservation grants and financial supports; centres of excellence training craftspeople in conservation.'),
             (3, 'Point 4 and discussion 6, a third, different guideline. Such as: conservation architects on the design team; the new use and essential works specified; new work distinct and legible. Three distinct guidelines are needed.')]],
         *HERITAGE, None, 'Conserving historic buildings (1.1) in the built environment (1.2).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, TALL, labels=['Discussion of the statement', 'Three best practice guidelines'], alt=True)

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and any four of the other nine (300 marks); all question banks retained, no full-exam Cartesian cards.'),
          (2, 'or', 'Q1 note ("the kitchen cabinets or the furniture"): not a candidate choice.'),
          (3, 'or', 'Q4(b) printed list of wall types ("concrete block construction or"): the any-two group below, not a separate route.'),
          (3, 'or', 'Q4(b) printed list of wall types ("as shown or"): the same any-two group.'),
          (3, 'Select', 'Q4(b) closed choose-two of three printed wall types: one card with an any-two group (choice is not a route).'),
          (3, 'any two', 'Q4(b) closed choose-two of three printed wall types: the same any-two group.'),
          (4, 'one of', 'Q7(a) wording ("at one of the eaves"): not a candidate choice.'),
          (4, 'or', 'Q8(b) "or any other suitable method": an open choice of calculation method, marked by the same steps.'),
          (4, 'any other', 'Q8(b) "any other suitable method": the same open choice of method.'),
          (5, 'any two', 'Q10(a) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
          (5, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.'),
          (5, 'or', 'Alternative Question 10 source title ("Use it or Lose it"): not a candidate choice.')]
FINITE = {'4b': dict(choose=2, options=[h for h, _ in ITEMS4], cardId=A4b['id'], groupRowId='walls'),
          '10a': dict(choose=2, options=[h for h, _ in ITEMS10], cardId=A10['id'], groupRowId='items')}
REASONS = {
    'q1-b': 'Reshaped to the printed cross-ventilation row; tariff unchanged (4).',
    'q2-a': 'Split into the two printed requirements (note 6 + sketch 6 each); tariff unchanged (24).',
    'q2-b': 'Split into the two printed advantages (3 + 3 each); tariff unchanged (12).',
    'q2-c': 'Rebuilt to the printed rows — the three fittings, grab rails, dimensions and the sewer-gas detail (4 each); tariff unchanged (24).',
    'q3-a': 'Split into the two printed requirements, optimising daylight and open plan (note 8 + sketches 8 each); tariff unchanged (32).',
    'q3-b': 'Split into the three printed reasons (6 each); tariff unchanged (18).',
    'q3-c': 'Split into the two printed advantages (2 + 3 each); tariff unchanged (10).',
    'q4-a': 'Split into the three printed requirements (note and sketch 4 + 4 each); tariff unchanged (24).',
    'q4-b': 'Now one card with an any-two group over all three printed wall types (note 5, sketch 5, dimensions 2 each); choice is not a route: 20 → 24.',
    'q4-c': 'Rebuilt to the printed rows — each selected wall type, environmental consideration 3 and ease of construction 3; tariff unchanged (12).',
    'q5-b': 'Reshaped to the six printed calculation steps (3 each) with the scheme’s worked answer (204.08 mm); tariff unchanged (18).',
    'q5-c': 'Reshaped to the five printed calculation steps (3 each) with the scheme’s worked answer (€47.99); tariff unchanged (15).',
    'q6-a': 'Split into the two printed advantages (5 each); tariff unchanged (10).',
    'q6-b': 'Split into three features, each note and sketch 5 + 5; tariff unchanged (30).',
    'q6-c': 'Split into two added features, each note and sketch 5 + 5; tariff unchanged (20).',
    'q7-a': 'Rows rebuilt to the printed table — best six roof and best five wall details × 4, both walls 4, and scale and drafting (8/6/4): 72 → 56 (72 overran the question’s 60).',
    'q7-b': 'Reshaped to the printed dimensions row (3 × 1 + 1); tariff unchanged (4).',
    'q8-a': 'Reshaped to the two printed light sources (note and sketch 4 + 4 each); tariff unchanged (16).',
    'q8-b': 'Rebuilt to the printed steps (6 × 3) and the window area (2) with the scheme’s worked answer (8.4 m²): 18 → 20.',
    'q8-c': 'Split into three advancements, each note 4 + sketch 4; tariff unchanged (24).',
    'q9-a': 'Split into the five printed rows (4 each); tariff unchanged (20).',
    'q9-c': 'Reshaped to the printed note 8 + sketch 8 for one test; tariff unchanged (16).',
    'q10-a': 'Now one card with an any-two group over all three printed items (notes 6 + sketches 6 each); choice is not a route; tariff unchanged (24).',
    'q10-b': 'Split into the four printed rows (6 each); tariff unchanged (24).',
    'q10-c': 'Split into the two printed advantages (6 each); tariff unchanged (12).',
}
GAPS = [dict(cardId=B9b['id'], canonicalTopicIds=['cons-2-7'], atlasTopicId=D.CROSS + 'foundations', reason=CONCRETE),
        dict(cardId=C9['id'], canonicalTopicIds=['cons-2-7'], atlasTopicId=D.CROSS + 'foundations', reason=CONCRETE)]
D.finish(LEDGER, FINITE, REASONS, taxonomy_gaps=GAPS)
