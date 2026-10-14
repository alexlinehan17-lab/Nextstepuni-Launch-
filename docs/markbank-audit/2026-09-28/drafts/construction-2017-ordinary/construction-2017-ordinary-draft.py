"""Draft the 2017 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 16-24). Q8 "any five of nine" is ONE card (choice is not a route): it keeps the pre-audit
hand-rail ID and the other eight per-term IDs alias to it. The other 18 pre-audit 2017 Ordinary cards
keep their IDs and concept IDs and are corrected in place; the pre-audit Q9(c) card had been built from
the practical-test marking scheme and is rebuilt from the theory scheme. Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Insulated door head in a cavity wall', concept='door-head-section',
              stem='The main door of a house is an insulated wooden door with 12 mm cedar sheeting on both sides, as shown. The door is fitted in a 400 mm concrete block external wall with a full-fill insulated cavity. The wall is rendered on both sides. The doorframe is 150 mm × 70 mm and the door is 90 mm in thickness.',
              note='Original sketch and specification retained. The scheme prints the draughting, accuracy and scale band after the part (b) row, so it is marked with the rainwater detail.'),
    '2': dict(page=2, title='Insulating a timber frame inner leaf', concept='timber-frame-inner-leaf',
              stem='The external wall of a new house has a 100 mm concrete block outer leaf, a cavity and a 200 mm inner leaf of timber frame construction, as shown. The inner leaf is insulated and insulated plasterboard is also fixed to the timber studs.',
              note='Original sketch retained. The insulation, its type and the plasterboard finish are open responses; the scheme lists typical examples.'),
    '3': dict(page=2, title='Solar panel hot water to a kitchen sink', concept='solar-hot-water', stem='',
              note='Original sketch retained. The listed components are required content, not a choice; the best-seven list is a marking menu.'),
    '4': dict(page=3, title='Sorting and reusing waste on site', concept='site-waste-reuse', stem='',
              note='Original sketch retained. Methods, reasons and uses are open responses; the scheme lists typical examples.'),
    '5': dict(page=3, title='Triple-glazed window cill in a cavity wall', concept='window-cill-section',
              stem='A triple-glazed wooden casement window, as shown, is fixed in a 400 mm external concrete block wall with a full-fill insulated cavity. The fixed frame of the window is 100 mm × 80 mm and is thermally broken. The wall is rendered on both sides.',
              note='Original sketch and specification retained. The scheme prints the draughting, accuracy and scale band after the part (b) row, so it is marked with the cold-bridge detail.'),
    '6': dict(page=3, title='Site signs, PPE and power tools', concept='site-signs-ppe-tools', stem='',
              note='Original sketch retained. The three PPE items in (b) are open; the scheme’s rows name a hard hat, safety boots and a high-visibility vest.'),
    '7': dict(page=4, title='Attic bedroom conversion', concept='attic-conversion',
              stem='The sketch shows an attic which is being converted to provide an additional bedroom. The floor is a tongue-and-groove hardwood floor.',
              note='Original sketch retained. Part (c) requires both one advantage and one disadvantage, each separately marked.'),
    '8': dict(page=4, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=4, title='Softwood decking patio', concept='decking-patio',
              stem='The sketch shows sliding doors which open on to an external patio at the rear of a house. The patio is constructed using softwood decking on wooden joists.',
              note='Original sketch retained. The fixing, finish and advantages are open responses; the scheme lists typical examples.'),
}
SCHEME_PAGES = {'1': [4, 16], '2': [5, 17], '3': [6, 18], '4': [7, 8, 19], '5': [8, 20], '6': [9, 10, 21], '7': [10, 11, 22], '8': [11, 12, 13, 14, 23], '9': [14, 15, 24]}
D = cp.Draft(HERE, 2017, 'ordinary', ('d3b27427c7d7cb63b783c6d94cefde26f5f5f692b8ff26a5d9d5b677b766a0e0',
                                      '0bd3312f2540c026eccd6a33c2b4a18eaaa690e9a5f305ed4762f2674ba8dda9'), 27, QUESTIONS, SCHEME_PAGES)
row, add, compose = D.row, D.add, D.compose
BAND8 = [0, 4, 6, 8]
BAND6 = [0, 2, 4, 6]
SKETCH8 = ('Quality of sketch (excellent, good, fair)', 8)


def parts(*cards):
    return D.parts(*[(letter, c['questionText']) for letter, c in zip('abc', cards)])


def quality(rid='presentation', marks=8, what='the sketches'):
    return row(rid, 'Quality of sketch (excellent, good, fair)', marks,
               f'Quality of {what}: excellent {marks}, good {marks - 2}, fair {marks - 4}.', BAND8 if marks == 8 else BAND6)


D.figures({
    'q1-original': D.paper(2, [30, 39, 580, 262]), 'q2-original': D.paper(2, [30, 268, 580, 470]),
    'q3-original': D.paper(2, [30, 488, 580, 770]), 'q4-original': D.paper(3, [30, 39, 580, 240]),
    'q5-original': D.paper(3, [30, 258, 580, 485]), 'q6-original': D.paper(3, [30, 505, 580, 700]),
    'q7-original': D.paper(4, [30, 39, 580, 255]), 'q8-original': D.paper(4, [30, 272, 580, 395]),
    'q9-original': D.paper(4, [30, 413, 580, 660]),
    'q1-scheme': D.scheme(4, [25, 50, 580, 775]),
    'q2-method': D.scheme(5, [25, 50, 580, 410]), 'q2-advantages': D.scheme(5, [25, 410, 580, 608]), 'q2-finish': D.scheme(5, [25, 608, 580, 775]),
    'q3-system': D.scheme(6, [25, 50, 580, 440]), 'q3-solar': D.scheme(6, [25, 440, 580, 606]), 'q3-tap': D.scheme(6, [25, 606, 580, 775]),
    'q4-sorting': D.scheme(7, [25, 50, 580, 436]), 'q4-reasons': D.scheme(7, [25, 436, 580, 649]),
    'q4-uses': D.composite((7, [25, 649, 580, 790]), (8, [25, 50, 580, 260])),
    'q5-scheme': D.scheme(8, [25, 270, 580, 775]),
    'q6-signs': D.scheme(9, [25, 50, 580, 230]), 'q6-ppe': D.scheme(9, [25, 230, 580, 785]), 'q6-power-tools': D.scheme(10, [25, 50, 580, 265]),
    'q7-joists': D.scheme(10, [25, 270, 580, 770]), 'q7-joint': D.scheme(11, [25, 50, 580, 275]), 'q7-attic': D.scheme(11, [25, 275, 580, 590]),
    'q8-terms': D.composite((11, [25, 590, 580, 785]), (12, [25, 50, 580, 670]), (13, [25, 50, 580, 640]), (14, [25, 50, 580, 392])),
    'q9-decking': D.scheme(14, [25, 392, 580, 785]), 'q9-finish': D.scheme(15, [25, 50, 580, 336]), 'q9-patio': D.scheme(15, [25, 336, 580, 500]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p16 (printed 13): (a) best 7 of 13 listed details × 5 = 35, three typical dimensions 3 = 38; (b) DPC between the leaves 4, and draughting, accuracy and scale 8 (8/6/4) printed after it = 12. Complete 50.'
S1 = 'One required section and one required rainwater detail. The best-seven detail list is a marking menu, not a printed choice.'
A1 = add('1', 'a', '(a)', 'To a scale of 1:5 draw a vertical section through the top of the door, showing the wall, the concrete lintels over the door, the doorframe and the door. Show the typical construction details from 400 mm below the lintels to a level 400 mm above the lintels. Include three typical dimensions on your drawing.',
         [row('details', 'Any 7 of the above details ( 5 marks each)', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: 19 mm external render; 100 mm block outer leaf; 200 mm full-fill cavity insulation; DPC; 100 mm block inner leaf; 15 mm plaster with skim; reinforced concrete lintels; 18 mm plywood with airtightness seal; insulated plasterboard with skim; proprietary cavity closer; 150 × 70 mm doorframe; 90 mm door top rail and insulation; 12 mm vertical sheeting both sides.', list(range(0, 36, 5))),
          row('dimensions', 'Three typical dimensions', 3, 'Three appropriate typical dimensions on the section, 1 each.')],
         ['cons-1-5', 'cons-3-7', 'cons-3-4', 'cons-3-3'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls'], 'q1-scheme',
         'Scaled drawing (1.5) of a door head (3.7) with lintels and DPC (3.4) in a cavity wall (3.3).', B1, S1)
B1b = add('1', 'b', '(b)', 'Show clearly on your drawing how to prevent the penetration of rainwater at the head of the door.',
          [row('dpc', 'Damp Proof Course between the inner and outer leaf', 4, 'Show and identify a DPC between the inner and outer leaf over the lintels, sloping towards the outside, as in the scheme’s model sections.', [0, 4]),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the whole section: excellent 8, good 6, fair 4. The scheme prints this band after the part (b) row.', BAND8)],
          ['cons-3-4', 'cons-3-7'], ['foundations-floors-walls', 'windows-doors'], 'q1-scheme', 'Damp proof courses (3.4) at a door head (3.7).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-scheme', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p17 (printed 14): (a) sketches — inner leaf 5, insulation 5, quality 8 (8/6/4) — and notes — two valid details × 4, type and thickness 4 = 30; (b) two advantages × 6 = 12; (c) quality of sketch 8 (8/6/4). Complete 50.'
S2 = 'The insulation, its type and the plasterboard finish are open responses with no printed list.'
A2 = add('2', 'a', '(a)', 'Using notes and freehand sketches show how the inner leaf is to be insulated. Specify the type and thickness of insulation.',
         [row('sketch', 'How the inner leaf is insulated - Sketches', 10, 'Sketches showing the inner leaf (5) and its insulation (5), as in the scheme’s model sketch.'),
          quality(what='the sketches'),
          row('notes', 'How the inner leaf is insulated - Notes', 8, 'Two valid details, 4 each. Such as: insulation placed between the uprights; structural sheeting board fixed to the uprights for rigidity; a breather membrane; the airtightness/vapour barrier on the warm side; insulated plasterboard fitted inside.'),
          row('type-thickness', 'Type and thickness of insulation', 4, 'Such as: blown cellulose, sheep’s wool, fibreglass, woodfibre, cork, mineral fibre batts or spray foam, at least 200 mm thick.')],
         ['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q2-method', 'Insulating materials (6.2) in a timber frame wall (3.3).', B2, S2)
B2b = add('2', 'b', '(b)', 'List two advantages of insulating the inner leaf of the wall.',
          [row('advantage-1', 'Advantage one', 6, 'Such as: less heat lost; the most effective way to save energy; better thermal comfort.'),
           row('advantage-2', 'Advantage two', 6, 'A second, different advantage. Such as: lower energy bills; a better U-value and BER; a warmer house of higher value.')],
          ['cons-6-2', 'cons-6-3'], ['heat-loss-insulation'], 'q2-advantages', 'Insulation (6.2) and running costs (6.3).', B2, S2)
C2 = add('2', 'c', '(c)', 'On a separate sketch, show one method of providing a surface finish to the plasterboard prior to painting.',
         [quality(what='the sketch, such as joints taped and filled and a skim coat applied with a steel trowel')],
         ['cons-4-1'], ['foundations-floors-walls'], 'q2-finish', 'Wall finishes (4.1).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-method', B2, S2, parts(A2, B2b, C2))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p18 (printed 15): (a) best 7 of 10 listed items × 4 = 28 and quality of sketch 8 (8/6/4) = 36; (b) two advantages × 4 = 8; (c) quality of sketch 6 (6/4/2). Complete 50.'
S3 = 'The printed component list is required content, not a choice; the best-seven list is a marking menu.'
A3 = add('3', 'a', '(a)', 'A solar panel is used to provide hot water for a dwelling house as shown. Draw a large freehand sketch of the given house and, on your sketch, show the pipework necessary to supply hot water to a kitchen sink. Include the following in your diagram: solar panel; rising main and cold water storage tank; hot water cylinder, as shown; pipework from solar panel to cylinder; expansion tank / vessel; pipework to hot tap; all necessary valves.',
         [row('items', 'Any 7 of the above details ( 4 marks each)', 28, 'Credit the best SEVEN acceptable items at 4 marks each, capped at 28. Marked items: 15 mm rising main; storage tank and overflow; 22 mm cold supply to the cylinder; hot water cylinder; 22 mm expansion pipe; hot supply to the kitchen sink; solar panel; pipework from the panel to the cylinder; expansion vessel; all necessary valves.', list(range(0, 29, 4))),
          quality(what='the sketch')],
         ['cons-5-2', 'cons-6-4'], ['hot-water-space-heating', 'planning-sustainability-environment'], 'q3-system', 'Hot water systems and cylinders (5.2) heated by solar gain (6.4).', B3, S3)
B3b = add('3', 'b', '(b)', 'Discuss two advantages of using a solar panel to provide hot water for a dwelling house.',
          [row('advantage-1', 'Advantage one', 4, 'Such as: lower energy bills; low running costs once installed.'),
           row('advantage-2', 'Advantage two', 4, 'A second, different advantage. Such as: less CO₂ from burning fossil fuels; an eco-friendly source of energy.')],
          ['cons-6-4', 'cons-6-3'], ['planning-sustainability-environment', 'heat-loss-insulation'], 'q3-solar', 'Solar heat gain (6.4) and running costs (6.3).', B3, S3)
C3 = add('3', 'c', '(c)', 'On a separate sketch, show a design for a tap which will be easy to use by a person with limited hand movement.',
         [quality('presentation', 6, 'the sketch, such as a lever tap needing a quarter turn, or a tall swivel-neck mixer within easy reach')],
         ['cons-5-6', 'cons-1-2'], ['drainage', 'planning-sustainability-environment'], 'q3-tap', 'Sanitary fitments (5.6) in accessible design (1.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-system', B3, S3, parts(A3, B3b, C3))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p19 (printed 16): (a) sketches — valid details 4, quality 8 (8/6/4) — and notes — two valid details × 6 = 24; (b) two reasons × 5 = 10; (c) two uses × 5 and a specific reason for each × 3 = 16. Complete 50.'
S4 = 'Methods, reasons and uses are open responses with no printed list.'
WASTE = (['cons-1-2', 'cons-1-8'], ['planning-sustainability-environment', 'site-safety'])
A4 = add('4', 'a', '(a)', 'The sketch shows waste materials from a house under repair. To improve waste management, this waste needs to be sorted and stored on-site for reuse. Using notes and freehand sketches, show how to properly sort and store this waste.',
         [row('sketch', 'Valid details', 4, 'Sketches of the sorted, stored waste, as in the scheme’s model sketches.'),
          quality(what='the sketches'),
          row('detail-1', 'Valid detail one', 6, 'Such as: old boards stacked together on blocks as a base; doors stored on edge beside them.'),
          row('detail-2', 'Valid detail two', 6, 'A second, different detail. Such as: bricks, blocks and paint cans segregated; drums for smaller offcuts; a cover over the stored waste.')],
         *WASTE, 'q4-sorting', 'Managing site waste in the built environment (1.2) safely (1.8).', B4, S4)
B4b = add('4', 'b', '(b)', 'Discuss two reasons why waste should be kept to a minimum on a construction site.',
          [row('reason-1', 'Reason one', 5, 'Such as: waste is a safety hazard to trip over or fall on workers; a managed site reduces accidents.'),
           row('reason-2', 'Reason two', 5, 'A second, different reason. Such as: good for the environment; landfill is scarce; it lowers the cost of the building and of disposal.')],
          *WASTE, 'q4-reasons', 'Managing site waste (1.2) safely (1.8).', B4, S4)
C4 = add('4', 'c', '(c)', 'Recommend two suitable uses for the wood that has been sorted on-site for reuse, and give one specific reason in support of each recommendation.',
         [row('use-1', 'Suitable use one', 5, 'Such as: old doors cleaned, painted and reused; shelving in a utility room.'),
          row('use-2', 'Suitable use two', 5, 'A second, different use. Such as: floorboards reused inside or out; furniture, fences, gates or garden sheds; fuel.'),
          row('reason-1', 'Specific reason one', 3, 'A reason for the first use. Such as: lower costs; keeps the architectural integrity of the building.'),
          row('reason-2', 'Specific reason two', 3, 'A reason for the second use. Such as: environmentally friendly; no transport; low embodied energy.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q4-uses', 'Re-using materials in the built environment (1.2).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-sorting', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p20 (printed 17): (a) best 9 of 12 listed details × 4 = 36, three typical dimensions 3 = 39; (b) insulation behind the cill 3, and draughting, accuracy and scale 8 (8/6/4) printed after it = 11. Complete 50.'
S5 = 'One required section and one required cold-bridge detail. The best-nine detail list is a marking menu, not a printed choice.'
A5 = add('5', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the external wall and bottom portion of the window, showing the fixed frame of the window and the concrete cill. Show the typical construction details from 300 mm below to a level 250 mm above the concrete cill. Include three typical dimensions on your drawing.',
         [row('details', 'Any 9 of the above details (4 marks each)', 36, 'Credit the best NINE acceptable details at 4 marks each, capped at 36. Marked details: reinforced concrete cill; DPC wrapped around the cill; 19 mm render; 100 mm block outer leaf; wall tie; full-fill cavity insulation; proprietary cavity closer; 100 mm block inner leaf; 15 mm plaster with skim; window board; 100 × 80 mm thermally broken frame; triple glazing with low-e glass.', list(range(0, 37, 4))),
          row('dimensions', 'Three typical dimensions', 3, 'Three appropriate typical dimensions on the section, 1 each.')],
         ['cons-1-5', 'cons-3-6', 'cons-3-3', 'cons-3-4'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls'], 'q5-scheme',
         'Scaled drawing (1.5) of a window cill (3.6) in a cavity wall (3.3) with its DPC (3.4).', B5, S5)
B5b = add('5', 'b', '(b)', 'Show on your drawing the typical design detailing to prevent the formation of a cold bridge at the concrete cill.',
          [row('cold-bridge', 'Insulation is placed at the back of the window cill to prevent thermal/cold bridge', 3, 'Show and identify insulation behind the concrete cill, with the DPC wrapped around it, as in the scheme’s model section.', [0, 3]),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the whole section: excellent 8, good 6, fair 4. The scheme prints this band after the part (b) row.', BAND8)],
          ['cons-6-2', 'cons-3-6'], ['heat-loss-insulation', 'windows-doors'], 'q5-scheme', 'A thermal bridge (6.2) at the window cill (3.6).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-scheme', B5, S5, parts(A5, B5b))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p21 (printed 18): (a) two reasons × 5 = 10; (b) three PPE items, each quality of sketch 6 (6/4/2) and note with specific reason 4 = 30; (c) two specific precautions × 5 = 10. Complete 50.'
S6 = 'The three PPE items in (b) are an open choice; the scheme’s rows name a hard hat, safety boots and a high-visibility vest.'
SAFE = (['cons-1-8'], ['site-safety'])
A6 = add('6', 'a', '(a)', 'Discuss two reasons why safety signs must be displayed at the entrance to a construction site, as shown.',
         [row('reason-1', 'Reason one', 5, 'Such as: signs are needed wherever a potential hazard exists; they alert people to the dangers on site.'),
          row('reason-2', 'Reason two', 5, 'A second, different reason. Such as: they remind everyone of Health and Safety; they show machinery, heights and trenches on site; they remind workers and visitors to wear hard hats, hi-vis and correct footwear.')],
         *SAFE, 'q6-signs', 'Safety precautions on site (1.8).', B6, S6)
B6b = add('6', 'b', '(b)', 'Using notes and freehand sketches, show three items of personal protective equipment (PPE) that must be worn by workers on a construction site. Give one specific reason why each item of personal protective equipment must be worn.',
          [row('item-1', 'Hard hat', 10, 'Quality of sketch 6 (6/4/2) and note with specific reason 4. Such as: a hard hat protects workers from falling objects; mandatory for workers and visitors.'),
           row('item-2', 'Safety boots', 10, 'Quality of sketch 6 (6/4/2) and note with specific reason 4, for a second item. Such as: safety boots with a steel toecap and protective sole protect the feet from heavy objects and cutting equipment.'),
           row('item-3', 'High visibility vest', 10, 'Quality of sketch 6 (6/4/2) and note with specific reason 4, for a third item. Such as: a high-visibility vest with reflective strips lets machine operators see workers.')],
          *SAFE, 'q6-ppe', 'Personal protective equipment (1.8).', B6, S6)
C6 = add('6', 'c', '(c)', 'Describe two specific safety precautions that should be observed when using electric power tools on a construction site.',
         [row('precaution-1', 'Specific safety precaution one', 5, 'Such as: check that all leads are in good condition and replace damaged ones; use the correct transformer for outdoor connections.'),
          row('precaution-2', 'Specific safety precaution two', 5, 'A second, different precaution. Such as: never in wet conditions; only skilled, trained operators; CE-marked, double-insulated tools; eye and ear protection.')],
         ['cons-1-8', 'cons-9-4'], ['site-safety'], 'q6-power-tools', 'Safety on site (1.8) with electric tools (9.4).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-ppe', B6, S6, parts(A6, B6b, C6))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p22 (printed 19): (a) sketch — valid details 4, quality 8 (8/6/4) — and notes — two valid details × 4 = 20; (b) sketch — valid details 4, quality 8 (8/6/4) — and two advantages × 5 = 22; (c) advantage 4, disadvantage 4 = 8. Complete 50.'
S7 = '"one method" in (a) is an open choice. Part (c) requires both one advantage and one disadvantage, each separately marked.'
A7 = add('7', 'a', '(a)', 'Show, using notes and freehand sketches, one method of preventing the floor joists from twisting.',
         [row('sketch', 'Valid details', 4, 'A sketch of the strutting between the joists, as in the scheme’s model sketches.'),
          quality(what='the sketch'),
          row('detail-1', 'Valid detail one', 4, 'Such as: herringbone strutting of wood, tightened between the joists; or metal bridging.'),
          row('detail-2', 'Valid detail two', 4, 'A second, different detail. Such as: solid strutting staggered for nailing, the same height as the joists, at mid-span, tied and wedged to the walls.')],
         ['cons-4-3'], ['foundations-floors-walls'], 'q7-joists', 'Suspended timber floors and strutting (4.3).', B7, S7)
B7b = add('7', 'b', '(b)', 'Using a large freehand sketch, show the tongue-and- groove joint between two flooring boards and list two advantages of this method of jointing.',
          [row('sketch', 'Valid details', 4, 'A large sketch of the tongue-and-groove joint between two boards.'),
           quality(what='the sketch'),
           row('advantage-1', 'Advantage one', 5, 'Such as: closes the gap between boards; draught-proofs the floor.'),
           row('advantage-2', 'Advantage two', 5, 'A second, different advantage. Such as: strengthens the floor; the gap stays closed if the boards shrink; secret nailing through the tongue.')],
          ['cons-4-3', 'cons-10-3'], ['foundations-floors-walls', 'wood-rot-ventilation'], 'q7-joint', 'Upper floors (4.3) and jointing boards (10.3).', B7, S7)
C7 = add('7', 'c', '(c)', 'Discuss one advantage and one disadvantage of converting an attic to provide additional bedroom accommodation.',
         [row('advantage', 'Advantage', 4, 'Such as: cheaper than a ground floor extension; no extra ground space; may not need planning permission with roof lights to the rear; better insulation and lower bills.'),
          row('disadvantage', 'Disadvantage', 4, 'Such as: difficult to get the head height; may compromise the roof structure; disruption during the work; hard to meet the building regulations in older houses.')],
         ['cons-3-9', 'cons-1-2'], ['roofs', 'planning-sustainability-environment'], 'q7-attic', 'A habitable roof space (3.9) in the built environment (1.2).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-joists', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p23 (printed 20): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination. It keeps the pre-audit hand-rail ID; the other eight per-term IDs alias to it.'
TERMS = [
    ('hand-rail', 'handrail', 'Hand rail', ['cons-4-4'], ['wood-rot-ventilation'],
     'the solid member fitted to the newel posts, parallel to the pitch line, carried on the balusters; generally 75 × 50 mm, jointed to the newel by mortise and tenon, 900–1000 mm above the pitch line.',
     'Stairs (4.4). The Ordinary reference taxonomy has no stairs heading; the term keeps the Wood, Rot & Ventilation association used for joinery, and 4.4 is declared outside that heading’s crosswalk.'),
    ('box-dovetail-joint', 'box dovetail joint', 'Box dovetail joint', ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'],
     'a joint of tails and pins for box shapes and drawers in high-quality furniture, by hand or with jigs; dovetail slope 1:6 in softwood and 1:8 in hardwood; decorative with contrasting woods.',
     'Joints (10.1) and the choice of joint (10.4). The Ordinary reference taxonomy has no joinery heading; the term keeps the Wood, Rot & Ventilation association, and 10.1/10.4 are declared outside that heading’s crosswalk.'),
    ('purlin', 'purlin', 'Purlin', ['cons-3-8'], ['roofs'],
     'the member under the rafters giving them support and alignment in a traditional cut roof, typically 175 × 75 mm, carried on struts to an internal load-bearing wall or on a steel joist.', 'Roof structure (3.8).'),
    ('damp-proof-course', 'damp-proof course', 'Damp-proof course', ['cons-3-4'], ['foundations-floors-walls'],
     'an impermeable barrier, usually heavy plastic, in external and internal walls, linked to the damp-proof membrane, 150 mm above ground; stops rising damp and damp crossing the cavity at openings.', 'Damp proof courses (3.4).'),
    ('ball-valve', 'ball valve', 'Ball valve', ['cons-5-2'], ['services-water-gas-electrical'],
     'controls the water entering a cistern or tank: a float rises with the water and closes the valve; mounted on the side of the cistern and connected to the supply.', 'Cold water systems and cisterns (5.2).'),
    ('energy-rating', 'energy rating', 'Energy rating', ['cons-6-3'], ['heat-loss-insulation'],
     'labels rating appliances, and homes through the Building Energy Rating, from A (most efficient, lowest bills) to G, to help consumers choose.', 'Energy use and running costs (6.3).'),
    ('wind-turbine', 'wind turbine', 'Wind turbine', ['cons-5-8', 'cons-1-2'], ['services-water-gas-electrical', 'planning-sustainability-environment'],
     'converts wind energy to mechanical energy and then electricity through its blades, generator and tower; small or large scale, sited for the wind; an eco-friendly source of energy.', 'Electrical installation (5.8) from a sustainable source (1.2).'),
    ('joist-hanger', 'joist hanger', 'Joist hanger', ['cons-4-3'], ['foundations-floors-walls'],
     'a galvanised steel hanger wrapping three sides of a joist end, nailed or screwed through predrilled holes, anchoring floor, ceiling and decking joists; stronger than nails alone.', 'Suspended and upper timber floors (4.3).'),
    ('service-cavity', 'service cavity', 'Service cavity', ['cons-3-3'], ['foundations-floors-walls'],
     'a separate cavity on the inside of an external wall carrying wiring and plumbing so they do not damage the airtightness membrane; used in solid and timber frame walls.', 'External walls (3.3).'),
]
Q8 = add('8', 'None-hand-rail', '', 'Explain, with the aid of notes and freehand sketches, any five of the following: ' + '; '.join(t[1] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Terms', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{t[2]}: {t[5]}' for t in TERMS),
               group=dict(claimMax=5, perOption=10, options=[t[2] for t in TERMS]))],
         list(dict.fromkeys(n for t in TERMS for n in t[3])), list(dict.fromkeys(a for t in TERMS for a in t[4])), 'q8-terms',
         'The union of the nine printed terms: ' + ' '.join(t[6] for t in TERMS), B8, S8)

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p24 (printed 21): (a) sketches — valid details 4, quality 8 (8/6/4) — and notes — two valid details × 4 = 20; (b) finish 4, two valid steps × 4 and quality of sketch 8 (8/6/4) = 20; (c) two advantages × 5 = 10. Complete 50.'
S9 = 'The fixing, the finish and the advantages are open responses with no printed list.'
TIMBER = (['cons-10-3', 'cons-10-7'], ['wood-rot-ventilation'])
A9 = add('9', 'a', '(a)', 'Show, using notes and freehand sketches, how to fix the wooden decking to the joists to ensure that the decking does not warp or bow, especially during wet weather.',
         [row('sketch', 'Valid details', 4, 'Sketches of the decking fixed to the joists, as in the scheme’s model sketches.'),
          quality(what='the sketches'),
          row('detail-1', 'Valid detail one', 4, 'Such as: boards laid starting next to the house with a 6 mm gap between them for drainage and expansion.'),
          row('detail-2', 'Valid detail two', 4, 'A second, different detail. Such as: pilot holes drilled and stainless steel screws used, more secure than nails; the board ends fixed first, then every joist between.')],
         *TIMBER, 'q9-decking', 'Fixing boards (10.3) to resist moisture movement (10.7).', B9, S9)
B9b = add('9', 'b', '(b)', 'Recommend a suitable applied finish to preserve the external decking. Using notes and freehand sketches, describe the steps involved in preparing the wood and in applying the recommended applied finish.',
          [row('finish', 'Suitable applied finish', 4, 'Such as: an oil-based varnish or stain; deck oil or deck stain; deck paint.'),
           row('step-1', 'Valid detail one', 4, 'Such as: the surface cleaned, with white spirit or, for a water-based finish, a damp cloth.'),
           row('step-2', 'Valid detail two', 4, 'A second, different step. Such as: the finish applied with a brush or cloth in two or three coats, each left to dry.'),
           quality(what='the sketch')],
          ['cons-10-7'], ['wood-rot-ventilation'], 'q9-finish', 'Surface preparation and finishing of timber (10.7).', B9, S9)
C9 = add('9', 'c', '(c)', 'An external patio has many advantages for the occupants of a dwelling house. Discuss two advantages of having an external patio, as shown.',
         [row('advantage-1', 'Advantage one', 5, 'Such as: extends the area of the house; a level surface for people with mobility issues; an open play area for children.'),
          row('advantage-2', 'Advantage two', 5, 'A second, different advantage. Such as: a place to eat and relax outdoors; close to nature; adds to the value of the house.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q9-patio', 'Outdoor living in the built environment (1.2).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-decking', B9, S9, parts(A9, B9b, C9))

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and three other questions (200 marks); all question banks retained, no full-exam Cartesian cards.'),
          (4, 'any five', 'Q8 closed choose-five of nine printed terms: one card with an any-five group over all nine terms (choice is not a route).'),
          (4, 'or', 'Q9(a) wording ("does not warp or bow"): not a candidate choice.')]
FINITE = {'8': dict(choose=5, options=[t[0] for t in TERMS], cardId=Q8['id'], groupRowId='terms', wholeQuestionMarks=50, termMarks=10)}
REASONS = {
    'q1-a': 'Adds the three typical dimensions (3) printed within part (a): 35 → 38.',
    'q1-b': 'Adds the draughting, accuracy and scale band (8/6/4) the scheme prints after the part (b) row to the DPC detail: 4 → 12.',
    'q2-a': 'Rebuilt to the printed rows — sketches (inner leaf 5, insulation 5, quality 8/6/4) and notes (two details 4 each, type and thickness 4): 5 → 30.',
    'q2-b': 'Split into the two printed advantages (6 each); tariff unchanged (12).',
    'q3-a': 'Adds the printed quality-of-sketch band (8/6/4) to the best-seven items: 28 → 36.',
    'q3-b': 'Split into the two printed advantages (4 each); tariff unchanged (8).',
    'q4-b': 'Split into the two printed reasons (5 each); tariff unchanged (10).',
    'q5-a': 'Adds the three typical dimensions (3) printed within part (a): 36 → 39.',
    'q5-b': 'Adds the draughting, accuracy and scale band (8/6/4) the scheme prints after the part (b) row to the cold-bridge detail: 3 → 11.',
    'q6-a': 'Split into the two printed reasons (5 each); tariff unchanged (10).',
    'q6-b': 'Rebuilt to the printed rows — three items, each quality of sketch (6/4/2) and note with reason 4: 12 → 30.',
    'q6-c': 'Split into the two printed precautions (5 each); tariff unchanged (10).',
    'q7-a': 'Rebuilt to the printed rows — sketch details 4, quality (8/6/4) and two notes (4 each): 12 → 20.',
    'q7-b': 'Rebuilt to the printed rows — sketch details 4, quality (8/6/4) and two advantages (5 each): 10 → 22.',
    'q7-c': 'Reshaped to the printed advantage and disadvantage rows (4 each); tariff unchanged (8).',
    'q9-a': 'Rebuilt to the printed rows — sketch details 4, quality (8/6/4) and two notes (4 each): 12 → 20.',
    'q9-b': 'Rebuilt to the printed rows — finish 4, two steps (4 each) and quality (8/6/4): 12 → 20.',
    'q9-c': 'The pre-audit authored card carried the practical-test marking scheme (34), which a build override replaced with the ten-mark patio question; rebuilt from the theory scheme’s two printed advantages (5 each) and the override retired: 34 → 10.',
    'q8-None-hand-rail': 'Now the whole of Question 8: one card printing all nine terms with an any-five group (10 each, 50), kept under this ID; the other eight per-term IDs alias to it (choice is not a route): 10 → 50.',
}
CONSOLIDATED = {f'q8-None-{t[0]}': 'q8-None-hand-rail' for t in TERMS[1:]}
GAPS = [dict(cardId=C2['id'], canonicalTopicIds=['cons-4-1'], atlasTopicId=D.CROSS + 'foundations-floors-walls',
             reason='No Ordinary outgoing reference heading covers internal wall finishes (4.1); the card keeps the Foundations, Floors & Walls association.'),
        dict(cardId=Q8['id'], canonicalTopicIds=['cons-4-4', 'cons-10-1', 'cons-10-4'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers stairs (4.4, handrail) or joinery (10.1, 10.4, box dovetail joint).')]
D.finish(LEDGER, FINITE, REASONS, consolidated=CONSOLIDATED, taxonomy_gaps=GAPS, whole_choices={'q8-None-hand-rail'})
