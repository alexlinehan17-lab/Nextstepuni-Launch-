"""Draft the 2022 Higher Level Construction Studies theory paper (LC029ALP000EV), Q1-Q10 and the Q10 alternative.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 29-39). The printed choices Q6(b) and Q9(b) (any two of three) are one card each with an
any-two group, and their figures carry every item's scheme drawings. The 27 pre-audit 2022 Higher
cards keep their IDs and concept IDs and are corrected in place. Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Flat roof abutment and external wall section', concept='flat-roof-abutment-section',
              stem='A dining area has a flat roof section which projects 1.6 metres from the rear wall of a house, as shown. The flat roof is covered with a waterproof membrane, on 150 mm rigid insulation, on plywood decking, supported on 200 mm × 50 mm roof joists. Insulated plasterboard is fixed to the underside of the roof joists. The external wall of the house is a 450 mm rendered concrete block wall with a full-fill cavity.',
              note='Original sketch and specification retained. Construction and scale/drafting marks belong to part (a); the thermal-bridge detail in (b) is marked separately.'),
    '2': dict(page=2, title='Designing for lifetime use', concept='lifetime-use',
              stem='Providing for lifetime use should be a key consideration at the design stage of a dwelling house.',
              note='Original question and kitchen/dining plan retained. Both printed areas in (a) are required, each separately marked. The two areas in (b) are an open choice; the scheme shows the kitchen and dining areas.'),
    '3': dict(page=3, title='Rear extension with an internal courtyard', concept='courtyard-extension',
              stem='The drawing shows the elevation and ground floor plan of a terraced house which has been converted from a traditional town shop. Also shown is a portion of the rear garden. The rear wall A-A is south facing. The owners wish to build a single-storey extension to the rear of the property to include an internal courtyard. Internal courtyards draw natural light and air into the centre of a house. The extension should be not greater than 15 m2 in area. Consideration at the design stage is to be given to: providing a separate additional living space; optimising daylight into both the extension and the existing kitchen.',
              note='Original elevation and plan retained. Both printed requirements and the courtyard are required in one layout. The scheme’s layouts are examples, not required designs.'),
    '4': dict(page=3, title='Foundations for a two-storey house', concept='foundation-design', stem='',
              note='Original site sketch retained. The two foundations in (b) are an open choice; the scheme models a strip foundation and an insulated raft.'),
    '5': dict(page=4, title='Externally insulated wall U-value, heat-loss cost and Passive House upgrade', concept='external-insulation-u-value',
              stem='The proposed external wall design detail for a new house is a 215 mm single leaf wall of solid block construction with external insulation, as shown.',
              note='All printed data are retained in the original question. Parts (b) and (c) use the U-value from (a); the scheme’s worked answers are U = 0.191 W/m²°C, an annual cost of €100.02 and 96 mm of additional insulation.'),
    '6': dict(page=5, title='Low-impact house designed for health and wellbeing', concept='wellbeing-house',
              stem='The elevation and ground floor plan of a house are shown. The house has additional living space upstairs. The external walls are of timber frame construction with a rendered concrete block and charred timber cladding finish. The house is designed to enhance the health and wellbeing of the occupants and to have a low environmental impact.',
              note='Original elevation and plan retained. Part (b) chooses any two of three printed items, each keeping its own 10 marks.'),
    '7': dict(page=5, title='Cut-string stairs and first-floor landing section', concept='stairs-landing-section',
              stem='A cut-string wooden stairs leads to the first floor of a house, as shown. The first floor landing has a hardwood tongued and grooved floor, on 225 mm × 50 mm joists with a plasterboard ceiling beneath. The newel post is 110 mm × 110 mm and the rise of a step should not exceed 175 mm.',
              note='Original sketch and specification retained. Construction, dimension and scale/drafting marks belong to part (a); the two safety details in (b) are marked separately.'),
    '8': dict(page=6, title='Solar collector for domestic hot water', concept='solar-collector-hot-water',
              stem='The owners of a house wish to upgrade the energy efficiency of their home by installing a solar collector on the roof, as shown, to provide hot water for the house.',
              note='Original sketch retained. The scheme’s system diagram is one acceptable layout. Part (c) requires both two advantages and two disadvantages, separately marked.'),
    '9': dict(page=6, title='Airtightness in a nearly Zero Energy Building', concept='airtight-nzeb',
              stem='An airtight external building envelope is vital in the design of a nearly Zero Energy Building (nZEB).',
              note='Original section drawing retained. Part (b) chooses any two of the three circled locations, each keeping its own 18 marks.'),
    '10': dict(page=7, title='Orientation and thermal mass of a Passive House', concept='orientation-thermal-mass',
               stem='The sketch shows the proposed design of a Passive House which is to be constructed in a rural setting.',
               note='Original sketch retained. Orientations, sun paths and thermal-mass features are open, well-reasoned responses.'),
}
ALT = dict(page=7, title='Air source heat pumps (alternative Question 10)', concept='air-source-heat-pumps',
           stem='“Older gas and oil-fired boilers are wasteful of energy and costly to run because of the amount of fuel needed to maintain adequate comfort levels and hot water in the home. Replacing a conventional heating system with an air source heat pump system can transform the comfort levels in your home while reducing running costs, energy usage and harmful greenhouse gas emissions.” Adapted from: Home Upgrades. Sustainable Energy Authority of Ireland Published on: www.seai.ie',
           note='This is the alternative Question 10 printed after OR. It is a separate 60-mark route under the same Question 10 anchor; its marks are never added to the orientation question.')
SCHEME_PAGES = {'1': [4, 5, 29], '2': [6, 7, 8, 30], '3': [9, 10, 31], '4': [11, 12, 13, 32], '5': [14, 15, 33], '6': [16, 17, 18, 34],
                '7': [19, 35], '8': [20, 21, 36], '9': [22, 23, 37], '10': [24, 25, 38], '10-alt': [26, 27, 39]}
D = cp.Draft(HERE, 2022, 'higher', ('2e74b08fa90a1063dda36fc6d33cf08d67f2d83f63cc663bffb0cb598dde6bb9',
                                    'cc608ae4393ae400dcf2d2ce36bca603e0e542e2a5c937bb22fc0bea65cc0e82'), 27, QUESTIONS, SCHEME_PAGES, alt=ALT)
row, add, compose, parts, anyn = D.row, D.add, D.compose, D.parts, D.anyn
D.figures({
    'q1-original': D.paper(2, [45, 53, 580, 410]), 'q2-original': D.paper(2, [45, 410, 580, 760]),
    'q3-original': D.paper(3, [45, 53, 580, 466]), 'q4-original': D.paper(3, [45, 466, 580, 765]),
    'q5-original': D.paper(4, [45, 53, 580, 720]), 'q6-original': D.paper(5, [45, 53, 580, 447]),
    'q7-original': D.paper(5, [45, 447, 580, 765]), 'q8-original': D.paper(6, [45, 53, 580, 413]),
    'q9-original': D.paper(6, [45, 413, 580, 760]), 'q10-original': D.paper(7, [45, 53, 580, 421]),
    'q10-alt-original': D.paper(7, [45, 495, 580, 715]),
    'q1-section': D.composite((4, [51, 51, 545, 790]), (5, [51, 51, 545, 440])),
    'q1-thermal-bridge': D.scheme(5, [51, 465, 545, 775]),
    'q2-entrance': D.scheme(6, [51, 51, 545, 470]), 'q2-corridor': D.scheme(6, [51, 470, 545, 780]),
    'q2-guidelines': D.scheme(6, [51, 51, 545, 780]),
    'q2-areas': D.composite((7, [51, 51, 545, 790]), (8, [51, 51, 545, 330])),
    'q3-layout': D.scheme(9, [51, 51, 545, 780]), 'q3-reasons': D.scheme(10, [51, 51, 545, 470]),
    'q4-requirements': D.scheme(11, [51, 51, 545, 445]),
    'q4-foundations': D.composite((11, [51, 445, 545, 731]), (12, [51, 51, 545, 580])),
    'q5-calculation': D.scheme(14, [51, 51, 545, 792]), 'q5-insulation': D.scheme(15, [51, 51, 570, 300]),
    'q6-low-impact': D.scheme(16, [51, 51, 545, 790]),
    'q6-wellbeing': D.composite((17, [51, 51, 545, 790]), (18, [51, 51, 545, 450])),
    'q6-scheme': D.composite((16, [51, 51, 545, 790]), (17, [51, 51, 545, 790]), (18, [51, 51, 545, 450])),
    'q7-section': D.scheme(19, [51, 51, 545, 786]),
    'q8-system': D.scheme(21, [51, 51, 545, 565]),
    'q9-locations': D.composite((22, [51, 252, 545, 790]), (23, [51, 51, 545, 325])),
    'q9-test': D.scheme(23, [51, 330, 545, 770]),
    'q10-orientation': D.scheme(24, [51, 280, 545, 704]), 'q10-thermal-mass': D.scheme(25, [51, 51, 550, 795]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p29 (printed 27): (a) external wall and eaves 4 × 4, flat roof 4 × 4, rear wall and abutment 4 × 4 (3 for drawing, 1 for annotation) = 48, scale 4 + drafting 4 banded excellent 8/good 6/fair 4 = 56; (b) thermal-bridge detail 4. Complete 60. The scale/drafting allowance assesses the section drawn in (a), so it stays with (a).'
S1 = 'One required section and one required thermal-bridge detail. The scheme detail lists are marking menus, not printed choices.'
T1A = 'To a scale of 1:5, draw a vertical section through the external wall of the dining area, the flat roof and the rear wall of the house. Show the typical construction details from a level 300 mm below the wallplate of the dining area wall, through the flat roof, to a level 400 mm above the abutment of the roof and the rear wall of the house.'
T1B = 'On your drawing, indicate the typical design detailing to prevent the formation of a thermal bridge at the junction of the flat roof and the rear wall of the house.'
A1 = add('1', 'a', '(a)', T1A,
         [row('external-wall', 'External wall and eaves', 16, 'Best four details, 4 each (3 for drawing, 1 for annotation). Marking menu: external and internal render; cavity blockwork (100 mm leaves) and wall ties; 250 mm full-fill insulation; wallplate 100 × 75 mm; cavity closer; fascia/soffit/gutter (any two).'),
          row('flat-roof', 'Flat roof', 16, 'Best four details, 4 each (3 for drawing, 1 for annotation). Marking menu: waterproof membrane; 150 mm roof insulation; breather membrane; OSB/plywood decking; firring pieces (1:40 slope); 200 × 50 mm roof joists; air-barrier/airtightness membrane; insulated plasterboard (50 mm insulation + 12.5 mm plasterboard).'),
          row('rear-wall', 'Rear wall and abutment', 16, 'Best four details, 4 each (3 for drawing, 1 for annotation). Marking menu: external and internal render; cavity blockwork and wall ties; concrete lintels 100 × 75 mm; cavity closer; wallplate 200 × 50 mm and metal hanger; tilting (angle) fillet and stepped DPC; lead flashings (two).'),
          row('presentation', 'Scale - 4 marks Drafting - 4 marks', 8, 'Scale 4 and drafting 4, assessed together: excellent 8, good 6, fair 4.', [0, 4, 6, 8])],
         ['cons-1-5', 'cons-3-10', 'cons-3-3', 'cons-3-4'], ['question-1-drawing-questions', 'roofs', 'walls'], 'q1-section',
         'Scaled drawing (1.5) of a flat roof and its abutment (3.10) on cavity walls (3.3) with lintels, stepped DPC and flashings (3.4).', B1, S1)
B1b = add('1', 'b', '(b)', T1B,
          [row('thermal-bridge', 'Design detailing to prevent a thermal bridge', 4, 'Show and identify the detail, as in the scheme’s model: an insulated block at the junction of the flat roof and the rear wall, keeping the insulation continuous.')],
          ['cons-6-2', 'cons-3-10'], ['heat-loss-insulation', 'roofs'], 'q1-thermal-bridge', 'A thermal bridge (6.2) at a flat-roof abutment (3.10).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(('a', T1A), ('b', T1B)))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p30 (printed 28): (a) each area two details × (notes 3 + sketches 3) = 24; (b) two areas × (notes 5 + sketches 5) and dimensions 4 = 24; (c) two reasons × (3 for point + 3 for discussion) = 12. Complete 60.'
S2 = 'Part (a) requires both printed areas, each separately marked, so each area is its own task and the part composes them; not a choice. The two areas in (b) are an open choice with no printed list.'
T2A = 'Using notes and freehand sketches, discuss two best practice guidelines that should be followed when designing for lifetime use at each of the following areas of a house: entrance access; internal corridor.'
AREAS = [('entrance-access', 'Entrance access', 'q2-entrance',
          'Notes 3 and sketches 3. Such as: a main entrance with a clear opening of at least 1000 mm; level thresholds with at most a 15 mm upstand; a level landing with an Ø1800 mm turning circle; a ramp no steeper than 1:50.',
          'A second, different guideline: notes 3 and sketches 3. Such as: a 300 mm clear space at the leading edge of the door; a canopy at least 900 mm deep; sensor-activated lighting; door handles 800–1100 mm above floor level; a vision panel.'),
         ('internal-corridor', 'Internal corridor', 'q2-corridor',
          'Notes 3 and sketches 3. Such as: an entrance hallway at least 1500 mm wide beside the entrance door; a corridor 1050–1200 mm wide between walls (Universal Design Guidelines recommend 1200–1500 mm).',
          'A second, different guideline: notes 3 and sketches 3. Such as: internal doors with a clear opening of 800–850 mm and a 300 mm clear space at the leading edge; level thresholds; sockets and switches 400–1000 mm above floor level; 100 lux of light at floor level.')]
a2 = [add('2', f'a-{slug}', f'(a) — {slug}', f'{T2A} — {heading}',
          [row('detail-1', f'{heading} - (2 details) Detail 1', 6, g1), row('detail-2', 'Detail 2', 6, g2)],
          ['cons-1-2'], ['planning-sustainability-environment'], figure, 'Designing a dwelling for lifetime use within the built environment (1.2).', B2, S2)
      for slug, heading, figure, g1, g2 in AREAS]
A2 = compose('2', 'a', '(a)', a2, 'q2-guidelines', B2, S2, T2A, labels=[x[1] for x in AREAS])
T2B = 'The drawing shows the ground floor plan of an open-plan kitchen / dining space, that is to be used by a person in a wheelchair. With reference to the design shown, discuss using notes and freehand sketches, two areas of the internal layout that require specific design detailing to ensure ease of use by a person in a wheelchair. Indicate on your sketches typical dimensions as appropriate.'
B2b = add('2', 'b', '(b)', T2B,
          [row('area-1', 'Area 1', 10, 'Notes 5 and sketches 5 for one area. Such as, the kitchen: a U- or L-shaped layout with an Ø1500–1800 mm turning circle; 1200–1500 mm between opposite work surfaces; a 900 mm worktop that can be raised or lowered; clear knee space beneath the sink and hob; pull-out drawers; wall units no more than 450 mm above the worktop.'),
           row('area-2', 'Area 2', 10, 'Notes 5 and sketches 5 for a second, different area. Such as, the dining area: a clearly defined passage; the table close to the kitchen with at least 1200 mm clear on two sides; a central pedestal table at an adjustable 700–900 mm; a level, slip-resistant floor between kitchen and dining.'),
           row('dimensions', 'Dimension(s)', 4, 'Typical dimensions shown on the sketches, such as a turning circle, clear widths or worktop and table heights.')],
          ['cons-1-2'], ['planning-sustainability-environment'], 'q2-areas', 'Accessible layout design within the built environment (1.2).', B2, S2)
T2C = 'Discuss in detail two reasons why provision for lifetime use should be considered in the design of a house.'
C2 = add('2', 'c', '(c)', T2C,
         [row('reason-1', 'Reason 1 (3 for point, 3 for discussion)', 6, 'Point 3 and discussion 3. Such as: flexibility and ease of adaptation to changing needs at low cost; cradle-to-grave living with minimal interventions.'),
          row('reason-2', 'Reason 2 (3 for point, 3 for discussion)', 6, 'A second, different reason. Such as: no need to relocate or carry out costly works as needs change; more people able to live independently; a house ready to resell without reconstruction costs; smart infrastructure fitted at the outset.')],
         ['cons-1-2'], ['planning-sustainability-environment'], None, 'Lifetime design of the built environment (1.2).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-areas', B2, S2, parts(('a', T2A), ('b', T2B), ('c', T2C)))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p31 (printed 29): (a) layout sketch 15 and notes for the separate living space, optimising daylight and the internal courtyard 5 each = 30; (b) three reasons × (3 + 3) = 18; (c) two advantages × (3 + 3) = 12. Complete 60.'
S3 = 'The two printed requirements and the courtyard are all required in one layout, not a choice. Layouts, reasons and advantages are open responses.'
T3A = 'Using notes and freehand sketches, show a proposed design layout for the extension that incorporates each of the above requirements.'
T3B = 'Discuss three reasons for your proposed design layout.'
T3C = 'Discuss in detail two advantages of maintaining the vernacular heritage of the streetscape in a town.'
A3 = add('3', 'a', '(a)', T3A,
         [row('layout', 'Proposed design layout sketch for extension to include separate living space, optimise daylight and internal courtyard', 15, 'A freehand layout of the extension (no more than 15 m²) with its separate living space and internal courtyard, as in the scheme’s model plan.'),
          row('living-space', 'Note for separate living space', 5, 'Such as: open-plan layouts so daylight penetrates; the kitchen kept at the rear with the new living space in the extension and dining in the link.'),
          row('daylight', 'Note for optimising daylight', 5, 'Such as: large south-facing windows for light and solar gain; triple or quadruple low-e glazing; glazing in place of part of the rear wall; lower cills.'),
          row('courtyard', 'Note for internal courtyard', 5, 'Such as: a courtyard linking the house and the extension, with sliding or folding doors, glazing on three sides and planting.')],
         ['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'], 'q3-layout',
         'Layout design within the built environment (1.2) for good daylighting (7.4).', B3, S3)
B3b = add('3', 'b', '(b)', T3B,
          [row(f'reason-{i}', f'Reason {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
              (1, 'Point 3 and discussion 3. Such as: natural light floods every living space throughout the day, including areas that would otherwise have none.'),
              (2, 'A second, different reason. Such as: a living space slightly separated from the house, reducing noise, with dual-aspect windows; the kitchen window kept by the open courtyard.'),
              (3, 'A third, different reason. Such as: a planted courtyard brings the outside in on a small, tight site; a utility room converted to a bigger dining area opening onto the courtyard.')]],
          ['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'], 'q3-reasons',
          'Layout design within the built environment (1.2) for good daylighting (7.4).', B3, S3)
C3 = add('3', 'c', '(c)', T3C,
         [row(f'advantage-{i}', f'Advantage {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: historic buildings contribute to the local character of a town; reuse underpins sustainable development by bringing empty structures into use.'),
             (2, 'A second, different advantage. Such as: reuse reduces the demand for new housing; people and families kept living in town centres; fewer new materials needed.')]],
         ['cons-1-1', 'cons-1-2'], ['conservation-restoration', 'planning-sustainability-environment'], None,
         'Conserving historic buildings (1.1) in the built environment (1.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-layout', B3, S3, parts(('a', T3A), ('b', T3B), ('c', T3C)))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p32 (printed 30): (a) three requirements × (notes 4 + sketches 4) = 24; (b) two foundations, each notes 4 + sketches 4 and reinforcement 2 + dimensions 2 = 24; (c) for each foundation one advantage and one disadvantage × (1 for point + 2 for discussion) = 12. Complete 60.'
S4 = '"Two different foundations" is an open choice with no printed list; each part stays one response. The scheme models a strip foundation and a passive insulated raft.'
T4A = 'Discuss in detail, using notes and freehand sketches, three functional requirements of a foundation suitable for a dwelling house.'
T4B = 'The owners of the site shown have been granted permission to construct a two-storey house. Site investigations have revealed moderately firm clay subsoil for the foundations. The external wall of the house is to be a 450 mm concrete block wall with a full-fill insulated cavity. Using notes and freehand sketches, show the typical design detailing for two different foundations suitable for the proposed house. Indicate the position of the reinforcement and the typical dimensions of each foundation.'
T4C = 'Discuss one advantage and one disadvantage of each foundation you have shown at 4(b) above.'
A4 = add('4', 'a', '(a)', T4A,
         [row(f'requirement-{i}', f'Functional requirement {i}', 8, note) for i, note in [
             (1, 'Notes 4 and sketches 4. Such as: to distribute all live loads (wind, snow, furniture, people) and dead loads (the building’s own weight) evenly to the ground.'),
             (2, 'A second, different requirement: notes 4 and sketches 4. Such as: to anchor the building against wind; to give a level surface to build on; to limit differential settlement.'),
             (3, 'A third, different requirement: notes 4 and sketches 4. Such as: to resist failure under applied stresses; to withstand swelling or shrinking of the surrounding soil; to give the building stability.')]],
         ['cons-2-2'], ['foundations'], 'q4-requirements', 'Functions of a foundation (2.2).', B4, S4)
B4b = add('4', 'b', '(b)', T4B,
          [row('foundation-1', 'Foundation design 1', 8, 'Notes 4 and sketches 4 for one foundation. Such as, a strip foundation for a 450 mm wall (T): depth T, width 3T = 1350 mm, projecting T beyond the wall; its top at least 600 mm below ground, on firm subsoil about 1000 mm down.'),
           row('details-1', 'Reinforcement (2) + dimensions (2)', 4, 'Reinforcement 2 and dimensions 2 for the first foundation. Such as: 10 mm welded steel mesh and longitudinal bars with 80 mm cover; the dimensions above.'),
           row('foundation-2', 'Foundation design 2', 8, 'Notes 4 and sketches 4 for a second, different foundation. Such as, a passive insulated raft: rigid EPS edge formwork carrying the 450 mm wall, 300 mm of EPS under a 100–150 mm reinforced slab, on compacted hardcore, blinding and a radon membrane.'),
           row('details-2', 'Reinforcement (2) + dimensions (2)', 4, 'Reinforcement 2 and dimensions 2 for the second foundation. Such as: steel in the edge beam tied to 10 mm mesh at 200 mm centres raised on spacers; the dimensions above.')],
          ['cons-2-4', 'cons-2-5', 'cons-2-2'], ['foundations'], 'q4-foundations',
          'Strip and raft foundations (2.4) with their reinforcement (2.5), chosen for the subsoil (2.2).', B4, S4)
C4 = add('4', 'c', '(c)', T4C,
         [row('advantage-1', 'Foundation design 1 Advantage (1 for point, 2 for discussion)', 3, 'Point 1 and discussion 2. Such as, strip: well understood, shallow, cheap and quick to build.'),
          row('disadvantage-1', 'Disadvantage (1 for point, 2 for discussion)', 3, 'Point 1 and discussion 2. Such as, strip: a large volume of concrete with high embodied energy; uninsulated, so heat is lost; limited to medium bearing soils and buildings.'),
          row('advantage-2', 'Foundation design 2 Advantage (1 for point, 2 for discussion)', 3, 'Point 1 and discussion 2 for the second foundation. Such as, insulated raft: minimal excavation; less concrete and embodied energy; very quick; no thermal bridge at the wall-floor junction.'),
          row('disadvantage-2', 'Disadvantage (1 for point, 2 for discussion)', 3, 'Point 1 and discussion 2 for the second foundation. Such as, insulated raft: high workmanship and specialist training; an engineer’s design for each house; higher capital cost.')],
         ['cons-2-4', 'cons-2-2'], ['foundations'], None, 'Strip and raft foundations (2.4) and the choice of foundation (2.2).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-foundations', B4, S4, parts(('a', T4A), ('b', T4B), ('c', T4C)))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p33 (printed 31): (a) tabulation, seven resistances, total resistance and U-value, 10 × 3 = 30; (b) five steps × 3 = 15; (c) five steps × 3 = 15. Complete 60.'
S5 = 'No printed choice. Parts (b) and (c) use the U-value from (a).'
DATA5 = ('Acrylic external render thickness 8 mm; external insulation thickness 150 mm; external scratch coat thickness 10 mm; concrete block thickness 215 mm; internal plaster thickness 12 mm.\n'
         'Thermal data of the external wall: resistance of external surface (R) 0.048 m2 ⁰C/W; conductivity of acrylic external render (k) 0.670 W/m ⁰C; '
         'conductivity of external insulation (k) 0.031 W/m ⁰C; conductivity of external scratch coat (k) 2.170 W/m ⁰C; conductivity of concrete blockwork (k) 1.440 W/m ⁰C; '
         'resistivity of internal plaster (r) 4.550 m ⁰C/W; resistance of internal surface (R) 0.122 m2 ⁰C/W.')
T5A = 'Calculate the U-value of the wall, given the construction has the following sequence and data: ' + DATA5
T5B = ('Using the U-value of the wall obtained at 5(a) above and the following data, calculate the cost of heat lost annually through this wall: area of external wall 144 m2; '
       'average internal temperature 20 ⁰C; average external temperature 5 ⁰C; heating period 10 hours daily for 37 weeks per annum; cost of oil 97 cent per litre; '
       'calorific value of oil 37350 kJ per litre; 1000 watts: 1 kJ per second.')
T5C = 'It is proposed to redesign the above external wall and upgrade its thermal properties to meet the Passive House standard by increasing the width of external insulation in the design. Calculate the thickness of additional external insulation required to achieve a U-value of 0.12 W/m2 ⁰C.'
A5 = add('5', 'a', '(a)', T5A,
         [row('tabulation', 'Tabulation/methodology', 3, 'A clear table of the materials with their conductivity or resistivity, thickness in metres and resistance.'),
          row('resistances', 'Formulae: R=T/k R=T × r', 21, 'Seven resistances, 3 each, by R = T/k (or R = T × r for the plaster): external surface 0.048 (given); acrylic render 0.008/0.670 = 0.012; external insulation 0.150/0.031 = 4.839; scratch coat 0.010/2.170 = 0.005; blockwork 0.215/1.44 = 0.149; internal plaster 0.012 × 4.550 = 0.055; internal surface 0.122 (given). All in m²°C/W.', list(range(0, 22, 3))),
          row('total-resistance', 'Total resistance', 3, 'Total resistance Rt = 5.229 m²°C/W (the sum of all the resistances).', [0, 3]),
          row('u-value', 'Calculation of U-value (w/m2 °c or w/m2k)', 3, 'U = 1 ÷ Rt = 1 ÷ 5.229 = 0.191 W/m²°C, with units.', [0, 3])],
         ['cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Thermal resistance, conductivity and transmittance (6.1).', B5, S5)
B5b = add('5', 'b', '(b)', T5B,
          [row('heat-loss', 'Heat loss formula and calculation', 3, 'Heat loss = U-value × area × temperature difference = 0.191 × 144 × (20 − 5) = 413.068 watts (joules per second).'),
           row('duration', 'Heating duration for one year', 3, 'Heating period = 60 × 60 × 7 × 10 × 37 = 9,324,000 seconds (2,590 hours).'),
           row('energy', 'k/Joules calculation for one year', 3, 'Energy = 9,324,000 × 413.068 ÷ 1000 = 3,851,446.032 kJ per year.'),
           row('oil', 'Litres of oil for one year', 3, 'Oil = 3,851,446.032 ÷ 37,350 = 103.118 litres per year.'),
           row('cost', 'Annual cost of heat loss', 3, 'Annual cost = 103.118 × €0.97 = €100.02. The scheme’s alternative one-line method gives the same €100.02.')],
          ['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations'], 'q5-calculation', 'Heat loss calculation and running costs (6.3) from the U-value (6.1).', B5, S5)
C5 = add('5', 'c', '(c)', T5C,
         [row('required-resistance', 'Resistance for U- value for 0.12 W/m2 °c (using R=1/U)', 3, 'Required resistance = 1 ÷ 0.12 = 8.333 m²°C/W.'),
          row('existing-resistance', 'Resistance from calculated U-value from part (a)', 3, 'Resistance of the wall from (a) = 1 ÷ 0.191 = 5.229 m²°C/W.'),
          row('difference', 'Difference in resistances (required resistance)', 3, 'Difference = 8.333 − 5.229 = 3.104 m²°C/W.'),
          row('formula', 'Application of formula R = T/k', 3, '3.104 = T ÷ 0.031, so T = 3.104 × 0.031 = 0.096 metres.'),
          row('thickness', 'Required thickness of insulation in mm.', 3, 'Additional insulation = 96 mm (95 or 97 mm accepted). Alternative calculation methods are acceptable.')],
         ['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation'], 'q5-insulation',
         'Thermal resistance and transmittance (6.1) of added insulation (6.2).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b, C5], 'q5-calculation', B5, S5, parts(('a', T5A), ('b', T5B), ('c', T5C)))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p34 (printed 32): (a) three features × (notes 5 + sketches 5) = 30; (b) any two of three printed items × (notes 5 + sketches 5) = 20; (c) two advantages × (2 for point + 3 for discussion) = 10. Complete 60.'
S6 = 'Choice is not a route: part (b) (any two of three printed items) is ONE card with an any-two group over the scheme headings; its figure and the complete-question figure carry all three items’ drawings.'
T6A = 'With reference to the design shown, discuss using notes and freehand sketches, three features of the design that contribute to the house having a low environmental impact.'
T6B = 'Using notes and freehand sketches, discuss the importance of providing for any two of the following in the design of a house, to enhance the health and wellbeing of the occupants: internal air quality; thermal environment; social interaction.'
T6C = 'Discuss in detail two advantages of designing a house that will enhance the health and wellbeing of the occupants.'
A6 = add('6', 'a', '(a)', T6A,
         [row(f'feature-{i}', f'Design Feature {i}', 10, note) for i, note in [
             (1, 'Notes 5 and sketches 5. Such as: local timber frame with lower embodied energy and stored carbon; flame-charred larch cladding needing no preservatives.'),
             (2, 'A second, different feature. Such as: large south-facing glazing and dual-aspect rooms for daylight and solar gain; small north windows.'),
             (3, 'A third, different feature. Such as: a central chimney whose thermal mass releases heat to all sides, with an efficient wood-burning stove; high insulation and high-performance glazing; upstairs living space avoiding extra foundations.')]],
         ['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment'], 'q6-low-impact',
         'Low-impact design of the built environment (1.2), solar gain (6.4) and insulation (6.2).', B6, S6)
ITEMS6 = [('Internal air quality', 'natural ventilation through openable glazing; mechanical ventilation with heat recovery supplying filtered fresh air and recovering about 95% of the heat from stale, moist air.'),
          ('Thermal environment', 'high-quality insulation and high-performance glazing; solar gain from the south, east and west with overhangs, brise-soleil or deciduous trees against overheating; 20 °C in living and 18 °C in sleeping areas.'),
          ('Social interaction', 'multifunctional rooms such as a table in the kitchen; seating in shared spaces; quieter separate spaces; open plan that can be closed off with pocket doors; outdoor living spaces.')]
A6b = add('6', 'b', '(b)', T6B,
          [anyn('items', 'How each could be incorporated to enhance health and wellbeing', 2, 10, ITEMS6,
                'Any two of the three, each notes 5 and sketches 5 = 10.')],
          ['cons-6-5', 'cons-6-2', 'cons-1-2'], ['condensation-air-tightness', 'heat-loss-insulation', 'planning-sustainability-environment'], 'q6-wellbeing',
          'The union of the three printed items: indoor air quality and ventilation (6.5), the thermal environment (6.2) and social spaces in the built environment (1.2).', B6, S6)
C6 = add('6', 'c', '(c)', T6C,
         [row(f'advantage-{i}', f'Advantage {i} (2 for point, 3 for discussion)', 5, note) for i, note in [
             (1, 'Point 2 and discussion 3. Such as: less stress and better mental health; a calm, secure, private home.'),
             (2, 'A second, different advantage. Such as: natural light and fresh air improving comfort and mood; a connection with nature; better sleep.')]],
         ['cons-1-2', 'cons-6-5'], ['planning-sustainability-environment', 'condensation-air-tightness'], None,
         'Health and comfort in the built environment (1.2, 6.5).', B6, S6)
compose('6', 'complete', ' — complete', [A6, A6b, C6], 'q6-scheme', B6, S6, parts(('a', T6A), ('b', T6B), ('c', T6C)))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p35 (printed 33): (a) best nine of fourteen details × 5 (4 for drawing, 1 for annotation) = 45, three dimensions 3, scale 4 + drafting 4 banded 8/6/4 = 56; (b) two design details × 2 = 4. Complete 60.'
S7 = 'One required section and two required safety details. The detail list is a marking menu, not a printed choice.'
T7A = 'To a scale of 1:5, draw a vertical section through the centre of the stairs and first floor landing. The section should show the typical construction details through the top three steps and the first floor landing, showing the newel post, balusters and handrails. Include the typical dimensions of three structural members of the stairs. Note: On your drawing, show a 500 mm length of landing.'
T7B = 'On your drawing, show two design details that ensure the safety of users on the first floor landing.'
A7 = add('7', 'a', '(a)', T7A,
         [row('details', '9 × 5 marks', 45, 'Best nine details, 5 each (4 for drawing, 1 for annotation). Marking menu: cut string; newel post; riser; tread; glue blocks; handrail (stairs and landing); balusters (stairs and landing); nosing/pitch line; handrail-to-newel joint; string-to-newel joint; trimmer joist; tongue and groove flooring; first-floor joists (500 mm); plasterboard ceiling. Typical sizes: string 250 × 50, newel 110 × 110, tread 250 × 25, riser 175 × 20, balusters 40 × 40, handrail 60 × 60, trimmer 225 × 75 mm.'),
          row('dimensions', 'Three dimensions of the stairs', 3, 'Typical dimensions of three structural members of the stairs, 1 each.'),
          row('presentation', 'Scale - 4 marks Drafting - 4 marks', 8, 'Scale 4 and drafting 4, assessed together: excellent 8, good 6, fair 4.', [0, 4, 6, 8])],
         ['cons-1-5', 'cons-4-4', 'cons-4-3'], ['question-1-drawing-questions', 'stairs', 'floors'], 'q7-section',
         'Scaled drawing (1.5) of a stairs (4.4) at a timber upper floor (4.3).', B7, S7)
B7b = add('7', 'b', '(b)', T7B,
          [row('detail-1', 'Design detail 1', 2, 'Such as: balusters spaced so that a 100 mm sphere cannot pass between them.'),
           row('detail-2', 'Design detail 2', 2, 'A second, different detail. Such as: a handrail at least 900 mm high on the landing.')],
          ['cons-4-4'], ['stairs'], 'q7-section', 'Stairs: handrail height and baluster spacing (4.4).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b], 'q7-section', B7, S7, parts(('a', T7A), ('b', T7B)))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p36 (printed 34): (a) three considerations × (2 for point + 3 for discussion) = 15; (b) best five of eight components × 4 (3 for drawing, 1 for annotation) = 20, control valves and pipe sizes 4, description 5 = 29; (c) two advantages and two disadvantages × (2 + 2) = 16. Complete 60.'
S8 = 'No printed choice. Part (c) requires both two advantages and two disadvantages, separately marked: two required tasks composed into (c).'
T8A = 'Discuss in detail three considerations when installing a solar collector for heating domestic hot water.'
T8B = 'Using notes and a single-line diagram, show a typical design layout for a solar collector that will connect with an existing system to supply domestic hot water. Indicate the location of all control valves and give typical sizes of pipework. Describe how the system works.'
T8C = 'Discuss two advantages and two disadvantages of installing a solar collector system in a domestic house.'
A8 = add('8', 'a', '(a)', T8A,
         [row(f'consideration-{i}', f'Consideration {i} (2 for point, 3 for discussion)', 5, note) for i, note in [
             (1, 'Point 2 and discussion 3. Such as: south facing at 30°–45° to the horizontal; no shadows at midday from trees, chimneys or buildings.'),
             (2, 'A second, different consideration. Such as: enough roof area and extra work to fix brackets; a cylinder sized for the household; short pipe runs to the cylinder.'),
             (3, 'A third, different consideration. Such as: a planning application may be needed; the cost of purchase and installation; the SEAI grant.')]],
         ['cons-5-2', 'cons-6-4'], ['hot-water-space-heating', 'sustainability-the-environment'], None, 'Hot water supply (5.2) from solar heat gain (6.4).', B8, S8)
B8b = add('8', 'b', '(b)', T8B,
          [row('components', 'Typical design layout for solar collector', 20, 'Best five components, 4 each (3 for drawing, 1 for annotation): solar panel; flow pipe to the panel; return pipe from the panel; cylinder with twin coil; pump; control panel and wiring; expansion vessel; pressure relief valve.'),
           row('valves', 'Control valves and typical size of pipework (any 2)', 4, 'Any two, 2 each: the control valves located, or typical pipe sizes such as Ø22 mm for 10–20 m² or Ø28 mm for 20–30 m² of collector.'),
           row('description', 'Description of how the system works', 5, 'Sunlight heats the fluid in the collector tubes; the heated fluid passes through the coil of the cylinder, heating the water, and returns to be reheated; the control panel runs the pump to the required temperatures; the expansion vessel takes up pressure from thermal expansion.')],
          ['cons-5-2', 'cons-6-4'], ['hot-water-space-heating', 'sustainability-the-environment'], 'q8-system', 'Hot water supply (5.2) from solar heat gain (6.4).', B8, S8)
c8 = [add('8', f'c-{kind}s', f'(c) — {kind}s', f'Discuss two {kind}s of installing a solar collector system in a domestic house.',
          [row(f'{kind}-1', f'{kind.capitalize()} 1 (2 for point, 2 for discussion)', 4, n1), row(f'{kind}-2', f'{kind.capitalize()} 2 (2 for point, 2 for discussion)', 4, n2)],
          ['cons-5-2', 'cons-6-4'], ['hot-water-space-heating', 'sustainability-the-environment'], None, 'Solar hot water (5.2, 6.4).', B8, S8)
      for kind, n1, n2 in [('advantage', 'Point 2 and discussion 2. Such as: lower heating costs and better energy efficiency; little maintenance.',
                            'A second, different advantage. Such as: grants and tax incentives; less dependence on finite fossil fuels.'),
                           ('disadvantage', 'Point 2 and discussion 2. Such as: high upfront equipment and installation costs; weather dependent.',
                            'A second, different disadvantage. Such as: needs a lot of roof area and internal space; specialist installation and maintenance.')]]
C8 = compose('8', 'c', '(c)', c8, None, B8, S8, T8C, labels=['Advantages', 'Disadvantages'])
compose('8', 'complete', ' — complete', [A8, B8b, C8], 'q8-system', B8, S8, parts(('a', T8A), ('b', T8B), ('c', T8C)))

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p37 (printed 35): (a) two advantages × (3 + 3) = 12; (b) any two of three circled locations × (notes 9 + sketches 9) = 36; (c) notes/discussion 6 + sketches 6 = 12. Complete 60.'
S9 = 'Choice is not a route: part (b) (any two of the three circled locations) is ONE card with an any-two group over the scheme headings; its figure carries all three locations’ drawings.'
T9A = 'Discuss in detail two advantages of an airtight dwelling house.'
T9B = 'The drawing shows an outline section through a portion of a house. The house has a truss roof. The wall is of timber frame construction with an external concrete block leaf and the window frame is thermally broken. Using notes and freehand sketches, show best practice design detailing that will prevent air leakage at any two of the locations circled on the drawing.'
T9C = 'Describe using notes and freehand sketches, one test that is carried out to determine the airtightness of a house.'
A9 = add('9', 'a', '(a)', T9A,
         [row(f'advantage-{i}', f'Advantage {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
             (1, 'Point 3 and discussion 3. Such as: comfort without draughts; less heat lost through gaps in the fabric.'),
             (2, 'A second, different advantage. Such as: better indoor air quality; moisture kept out of the fabric; insulation and mechanical ventilation work better; less noise; lower carbon emissions.')]],
         ['cons-6-5'], ['condensation-air-tightness'], None, 'Airtightness and ventilation (6.5).', B9, S9)
ITEMS9 = [('Head of window detail', 'an airtight membrane on the inner face of the timber frame, the thermally broken frame sealed to the frame and the junction taped with airtightness tape.'),
          ('Wallplate position detail', 'the wall membrane with a service cavity inside it, a membrane under the ceiling joists and the junction of the two taped.'),
          ('Light fitting detail', 'the ceiling membrane under the joists with the cable sealed through it by an airtightness grommet or self-adhesive patch.')]
A9b = add('9', 'b', '(b)', T9B,
          [anyn('items', 'Best practice design detailing to prevent air leakage', 2, 18, ITEMS9, 'Any two of the three circled locations, each notes 9 and sketches 9 = 18.')],
          ['cons-6-5', 'cons-3-6', 'cons-3-9'], ['condensation-air-tightness', 'windows-light', 'roofs'], 'q9-locations',
          'The union of the three circled locations: airtightness (6.5) at the window head (3.6) and at wallplate and ceiling level (3.9).', B9, S9)
C9 = add('9', 'c', '(c)', T9C,
         [row('notes', 'Notes / discussion', 6, 'Such as, the blower door test by a trained professional: a frame and panel in an external doorway with a variable-speed fan, pressure gauge and airflow measurement; the fan lowers (or raises) the pressure inside so air flows through every gap; leaks may be found with an infrared camera or smoke pencil; the result gives the air infiltration rate.'),
          row('sketches', 'Sketches', 6, 'Freehand sketches of the test, such as the fan in the door frame.')],
         ['cons-6-5'], ['condensation-air-tightness'], 'q9-test', 'Airtightness testing (6.5).', B9, S9)
compose('9', 'complete', ' — complete', [A9, A9b, C9], 'q9-locations', B9, S9, parts(('a', T9A), ('b', T9B), ('c', T9C)))

# ---------------------------------------------------------------- Q10
B10 = 'Scheme p38 (printed 36): (a) three benefits × (3 + 3) = 18; (b) sketch 12, orientation 4, sun path 4, optimum thermal performance 4 = 24; (c) thermal mass notes 5 + sketches 5, two design features 4 each = 18. Complete 60.'
S10 = 'No printed choice. The OR alternative is a separate Question 10 route.'
T10A = 'Discuss in detail three benefits to the occupants of considering the orientation of a house at the design stage.'
T10B = 'Using notes and freehand sketches, suggest a preferred orientation for the house shown. On your sketch include the sun path and discuss how your preferred orientation ensures the optimum thermal performance of the house.'
T10C = 'Using notes and freehand sketches, discuss the importance of thermal mass and show two ways in which thermal mass could be incorporated into the house shown. Suggest a material choice for each, and justify your choices.'
A10 = add('10', 'a', '(a)', T10A,
          [row(f'benefit-{i}', f'Benefit {i} (3 for point, 3 for discussion)', 6, note) for i, note in [
              (1, 'Point 3 and discussion 3. Such as: comfort from solar gain and passive heating; lower heating and cooling needs and costs.'),
              (2, 'A second, different benefit. Such as: windows placed to bring sun to the living areas and give pleasant views.'),
              (3, 'A third, different benefit. Such as: privacy and security away from neighbours and busy roads; use of natural shading; the garden layout planned.')]],
          ['cons-6-4'], ['passive-design'], None, 'Solar heat gain and orientation (6.4).', B10, S10)
B10b = add('10', 'b', '(b)', T10B,
           [row('sketch', 'Sketch', 12, 'A freehand sketch of the house on its site with the sun path, as in the scheme’s model.'),
            row('orientation', 'Orientation', 4, 'Such as: the large glazed façade facing south or south-west, within 30° of the east-west axis.'),
            row('sun-path', 'Sun path', 4, 'The sun path shown, with the winter and summer paths.'),
            row('thermal-performance', 'Optimum thermal performance', 4, 'Such as: greater solar gain and lower heating demand; a solid north wall with minimal glazing for shelter; a south overhang against overheating and glare.')],
           ['cons-6-4'], ['passive-design'], 'q10-orientation', 'Solar heat gain and orientation (6.4).', B10, S10)
C10 = add('10', 'c', '(c)', T10C,
          [row('thermal-mass', 'Thermal mass', 10, 'Notes 5 and sketches 5. Such as: thermal mass absorbs, stores and releases the sun’s heat; heavy materials (concrete, brick, tiles) absorb solar gain through south glazing and release it later, cutting peak temperatures and heating demand; thermal lag.'),
           row('feature-1', 'Design Feature 1', 4, 'Notes, material and justification. Such as: a concrete ground floor and screed, or a polished concrete or tiled floor.'),
           row('feature-2', 'Design Feature 2', 4, 'A second, different way. Such as: concrete block internal walls; a hollow-core concrete upper floor; a concrete chimney and hearth; brick or stone walls; rammed earth.')],
          ['cons-6-4', 'cons-6-2'], ['passive-design', 'heat-loss-insulation'], 'q10-thermal-mass', 'Passive solar design with thermal mass (6.4, 6.2).', B10, S10)
compose('10', 'complete', ' — complete', [A10, B10b, C10], 'q10-orientation', B10, S10, parts(('a', T10A), ('b', T10B), ('c', T10C)))

BALT = 'Scheme p39 (printed 37): (a) three discussion points × (4 + 6) = 30; (b) three guidelines × (4 + 6) = 30. Complete alternative 60.'
SALT = 'The OR question is an alternative whole Question 10 with its own 60-mark route; it never combines with the orientation question. Its parts are open responses.'
TAA = 'Discuss the above statement in detail.'
TAB = 'Propose three best practice guidelines that would promote the installation of air source heat pumps in dwelling houses.'
AA = add('10', 'a', '(a)', TAA,
         [row(f'point-{i}', f'Discussion Point {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: older oil and gas boilers are only 65–75% efficient (condensing boilers at best 80%) and burn fossil fuels with high CO₂ emissions.'),
             (2, 'Point 4 and discussion 6. Such as: rising fossil-fuel costs and fuel poverty; finite fuels whose search threatens pristine environments.'),
             (3, 'Point 4 and discussion 6. Such as: heat pumps cut carbon emissions by up to 70%, have a coefficient of performance of 3–4, are grant aided by SEAI and suit airtight, well-insulated houses. Three distinct, well-argued points are needed.')]],
         ['cons-5-3', 'cons-1-2'], ['hot-water-space-heating', 'sustainability-the-environment'], None,
         'Heating systems (5.3) in a sustainable built environment (1.2).', BALT, SALT, alt=True)
AB = add('10', 'b', '(b)', TAB,
         [row(f'guideline-{i}', f'Guideline {i} (4 for point, 6 for discussion)', 10, note) for i, note in [
             (1, 'Point 4 and discussion 6. Such as: larger grants for new builds and for deep retrofits of older houses, ring-fenced through local authorities.'),
             (2, 'Point 4 and discussion 6. Such as: public information on heat pumps; fast-tracked planning for deep retrofits.'),
             (3, 'Point 4 and discussion 6. Such as: phased legislation, with notice of a date after which fossil-fuel boilers are no longer acceptable; funding for third-level energy research. Three distinct guidelines are needed.')]],
         ['cons-5-3', 'cons-1-2'], ['hot-water-space-heating', 'sustainability-the-environment'], None,
         'Heating systems (5.3) in a sustainable built environment (1.2).', BALT, SALT, alt=True)
compose('10', 'complete', ' — complete', [AA, AB], None, BALT, SALT, parts(('a', TAA), ('b', TAB)), alt=True)

LEDGER = [
    (1, 'Answer any', 'Whole-exam selection: any four of the ten questions (240 marks); all question banks retained, no full-exam Cartesian cards.'),
    (5, 'any two', 'Q6(b) closed choose-two of three printed items: one card with an any-two group (choice is not a route).'),
    (6, 'any two', 'Q9(b) closed choose-two of the three circled locations: one card with an any-two group (choice is not a route).'),
    (7, 'OR', 'Alternative Question 10: a separate whole 60-mark route under the same printed Question 10 anchor.'),
]
FINITE = {'6b': dict(choose=2, options=[h for h, _ in ITEMS6], cardId=A6b['id'], groupRowId='items'),
          '9b': dict(choose=2, options=[h for h, _ in ITEMS9], cardId=A9b['id'], groupRowId='items')}
REASONS = {
    'q1-a': 'Rows rebuilt to the printed table, with the scale and drafting allowance (8, banded 8/6/4) it prints: 48 → 56.',
    'q1-b': 'Reshaped to the printed criterion row; tariff unchanged (4).',
    'q2-a-entrance-access': 'Reshaped to the two printed details (notes 3 + sketches 3 each); tariff unchanged (12).',
    'q2-a-internal-corridor': 'Reshaped to the two printed details (notes 3 + sketches 3 each); tariff unchanged (12).',
    'q2-b': 'Rebuilt to the printed rows — two areas (notes 5 + sketches 5) and dimensions 4; tariff unchanged (24).',
    'q2-c': 'Split into the two printed reasons (3 for point + 3 for discussion); tariff unchanged (12).',
    'q3-a': 'Adds the printed layout sketch (15) to the three notes (5 each): 15 → 30.',
    'q3-b': 'Split into the three printed reasons (3 + 3 each); tariff unchanged (18).',
    'q3-c': 'Split into the two printed advantages (3 + 3 each); tariff unchanged (12).',
    'q4-a': 'Split into the three printed requirements (notes 4 + sketches 4 each); tariff unchanged (24).',
    'q4-b': 'Rebuilt to the printed rows — each foundation notes 4 + sketches 4 and reinforcement 2 + dimensions 2; tariff unchanged (24); the build-time source override is retired.',
    'q4-c': 'Reshaped to the four printed advantage/disadvantage rows (1 + 2 each); tariff unchanged (12); the build-time source override is retired.',
    'q5-b': 'Reshaped to the five printed calculation steps (3 each) with the scheme’s worked answer; tariff unchanged (15).',
    'q5-c': 'Reshaped to the five printed calculation steps (3 each) with the scheme’s worked answer (96 mm); tariff unchanged (15).',
    'q6-a': 'Split into three design features, each notes 5 + sketches 5; tariff unchanged (30).',
    'q6-b': 'Now one card printing all three items with an any-two group over the scheme headings (notes 5 + sketches 5 each); tariff unchanged (20).',
    'q6-c': 'Split into the two printed advantages (2 for point + 3 for discussion); tariff unchanged (10).',
    'q7-a': 'Adds the three printed dimensions (3) and the scale and drafting allowance (8, banded 8/6/4) to the nine details: 45 → 56.',
    'q7-b': 'Split into the two printed design details (2 each); tariff unchanged (4).',
    'q8-a': 'Split into the three printed considerations (2 for point + 3 for discussion); tariff unchanged (15).',
    'q8-b': 'Rebuilt to the printed rows — best five components (4 each), control valves and pipe sizes 4, description 5: 20 → 29.',
    'q8-c-advantages': 'Split into the two printed advantages (2 + 2 each); tariff unchanged (8).',
    'q8-c-disadvantages': 'Split into the two printed disadvantages (2 + 2 each); tariff unchanged (8).',
    'q9-a': 'Split into the two printed advantages (3 + 3 each); tariff unchanged (12).',
    'q9-b': 'Now one card printing all three circled locations with an any-two group over the scheme headings (notes 9 + sketches 9 each); tariff unchanged (36).',
    'q9-c': 'Reshaped to the printed notes 6 + sketches 6; tariff unchanged (12).',
    'q10-a': 'Split into the three printed benefits (3 + 3 each); tariff unchanged (18).',
}
D.finish(LEDGER, FINITE, REASONS)
