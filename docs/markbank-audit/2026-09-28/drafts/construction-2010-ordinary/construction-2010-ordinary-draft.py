"""Draft the 2010 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 14-22). The paper was never carded, so every task is added. Q8 "any five of nine" is ONE card
(choice is not a route); its nine bullets follow Q9 in the text layer and are read back into Q8 (module TAILS).
Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Strip foundation, cavity wall and solid floor section', concept='foundation-wall-floor-section',
              stem='A living room has a solid concrete ground floor with a 20 mm quarry tile finish as shown. The external wall of the living room is a 350 mm concrete block wall with an insulated cavity. The wall is plastered on both sides. The foundation is a traditional strip foundation.',
              note='Original sketch and specification retained. Construction, dimension and draughting marks belong to part (a); the cold-bridge detail in (b) is marked separately.'),
    '2': dict(page=2, title='Cavity fill and attic insulation', concept='cavity-attic-insulation',
              stem='The owner of a house built in the 1960s intends to improve the thermal insulation levels by insulating the external walls and the attic space. The external wall is a 300 mm concrete block wall with an uninsulated cavity. The attic space is also uninsulated. It is proposed to inject insulation into the cavity of the external walls.',
              note='Original sketch retained. The attic insulation material in (c) is an open choice; the scheme gives typical materials.'),
    '3': dict(page=2, title='Wood burning stove, back boiler and cylinder', concept='stove-back-boiler-cylinder',
              stem='A wood burning stove, as shown in the accompanying sketch, has a back boiler fitted. The back boiler is connected to an indirect cylinder to supply hot water for a dwelling house.',
              note='Original sketch retained. The listed components are required content, not a choice; the best-nine list is a marking menu.'),
    '4': dict(page=2, title='Fitting a pine doorframe and hanging a door', concept='doorframe-hinge',
              stem='A solid pine door and doorframe are shown in the accompanying sketch. The door and frame are fitted in a 100 mm internal concrete block wall which is plastered on both sides.',
              note='Original sketch retained. The hinge in (c) is an open choice; the scheme gives a butt hinge.'),
    '5': dict(page=3, title='Stud partition, floor and door section', concept='stud-partition-door-section',
              stem='A non-load bearing timber stud partition separates two bedrooms on the first floor of a two storey dwelling house, as shown in the accompanying sketch. The first floor joists are 225 mm × 50 mm, the floor is a tongued and grooved floor and there is a plasterboard ceiling beneath. A flush panel door is fitted in the partition.',
              note='Original sketch retained. Construction and draughting marks belong to part (a); the sound detail in (b) is marked separately.'),
    '6': dict(page=3, title='Ladder, veneering knife, jig saw and outdoor tool safety', concept='tool-ladder-safety', stem='',
              note='All three printed situations in (a) are required, each separately marked.'),
    '7': dict(page=3, title='Collecting and storing rainwater from a lean-to roof', concept='lean-to-rainwater',
              stem='An extension to the side of a dwelling house has a lean-to roof, as shown in the accompanying sketch. Also shown is an underground rainwater storage tank.',
              note='Original sketch retained. The pipework and filter are shown as in the scheme’s model sketch.'),
    '8': dict(page=3, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=3, title='Repairing traditional wooden windows', concept='window-repair',
              stem='A terrace of traditional houses is shown in the accompanying sketch. The houses have slated roofs and wooden windows and doors. The windows are in need of repair.',
              note='Original sketch retained. "one of the windows" and "one of the houses" name the window being repaired, not a choice.'),
}
SCHEME_PAGES = {'1': [4, 14], '2': [5, 6, 15], '3': [6, 16], '4': [7, 17], '5': [8, 18], '6': [8, 9, 19], '7': [10, 20], '8': [11, 12, 21], '9': [13, 22]}
D = cp.Draft(HERE, 2010, 'ordinary', ('e3dc8aa0f218165fb0a4c9e834df5d1aedfb899f064773d95a3f0456f8f2e7d2',
                                      '6601a161493382099d7cd0e7e43e2a5ac7fd6a014cc4b680c51dacbee436297e'), 0, QUESTIONS, SCHEME_PAGES)
row, add, compose = D.row, D.add, D.compose


def parts(*cards):
    return D.parts(*[(letter, c['questionText']) for letter, c in zip('abc', cards)])


def quality(verbatim, marks, what='the sketch', rid='presentation'):
    return row(rid, verbatim, marks, f'Quality of {what}, excellent, good or fair, up to {marks}.')


D.figures({
    'q1-original': D.paper(2, [30, 39, 580, 201]), 'q2-original': D.paper(2, [30, 201, 580, 414]),
    'q3-original': D.paper(2, [30, 414, 580, 610]), 'q4-original': D.paper(2, [30, 610, 580, 790]),
    'q5-original': D.paper(3, [30, 39, 580, 207]), 'q6-original': D.paper(3, [30, 207, 580, 336]),
    'q7-original': D.paper(3, [30, 336, 580, 510]), 'q8-original': D.paper(3, [30, 510, 580, 606]),
    'q9-original': D.paper(3, [30, 606, 580, 790]),
    'q1-section': D.scheme(4, [25, 45, 580, 778]),
    'q2-injecting': D.scheme(5, [25, 45, 580, 270]), 'q2-pros-cons': D.scheme(5, [25, 270, 580, 513]),
    'q2-attic': D.composite((5, [25, 513, 580, 778]), (6, [25, 45, 580, 249])),
    'q3-system': D.scheme(6, [25, 249, 580, 604]), 'q3-advantages': D.scheme(6, [25, 604, 580, 778]),
    'q4-scheme': D.scheme(7, [25, 45, 580, 563]),
    'q5-scheme': D.scheme(8, [25, 45, 580, 470]),
    'q6-precautions': D.composite((8, [25, 470, 580, 778]), (9, [25, 45, 580, 413])), 'q6-outdoors': D.scheme(9, [25, 413, 580, 778]),
    'q7-scheme': D.scheme(10, [25, 45, 580, 520]), 'q7-uses': D.scheme(10, [25, 520, 580, 778]),
    'q8-terms': D.composite((11, [25, 45, 580, 778]), (12, [25, 45, 580, 778])),
    'q9-reasons': D.scheme(13, [25, 45, 580, 193]), 'q9-glass': D.scheme(13, [25, 193, 580, 453]), 'q9-paint': D.scheme(13, [25, 453, 580, 778]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p14 (printed 11): (a) best 7 of 15 listed details × 5 = 35, four typical dimensions 4 and draughting, accuracy and scale 8 = 47; (b) cold-bridge detail 3. Complete 50.'
S1 = 'One required section and one required cold-bridge detail. The best-seven detail list is a marking menu, not a printed choice.'
A1 = add('1', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the external wall and ground floor. The section should show all the construction details from the bottom of the foundation to 400 mm above finished floor level. Indicate the typical sizes of four main components.',
         [row('details', 'Any 7 of the above details (5 marks each)', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: 19 mm render and 13 mm plaster; 100 mm outer leaf; DPC; 50 mm residual cavity; wall tie; 100 mm insulation; 100 mm inner leaf; 120 × 20 mm skirting; 20 mm quarry tiles sealed at the wall; 150 mm concrete floor; 150 mm floor insulation; DPM or radon barrier; hardcore and sand blinding; concrete fill or foundation blocks; reinforced concrete foundation.', list(range(0, 36, 5))),
          row('dimensions', 'Any four typical dimensions', 4, 'Typical sizes of four main components, 1 each.'),
          row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the section, excellent, good or fair, up to 8.')],
         ['cons-1-5', 'cons-2-4', 'cons-3-3', 'cons-4-2'], ['question-one-drawing-questions', 'foundations-floors-walls'], 'q1-section',
         'Scaled drawing (1.5) of a strip foundation (2.4), cavity wall (3.3) and solid ground floor (4.2).', B1, S1)
B1b = add('1', 'b', '(b)', 'Show on your drawing the typical design detailing to prevent a thermal/cold bridge at the junction of the concrete floor and the external wall.',
          [row('cold-bridge', 'Design detail to prevent a thermal/cold bridge at the junction of the concrete floor and the external wall', 3, 'Such as: an inner leaf of thermal blocks from the foundation to floor level; the cavity insulation overlapping the floor insulation; perimeter insulation at floor level; a flexible seal between wall and floor.')],
          ['cons-6-2', 'cons-4-2'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q1-section', 'A thermal bridge (6.2) at the ground floor junction (4.2).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p15 (printed 12): (a) two descriptions × 4, insulation type 4, sketch detail 4 and quality 5 = 21; (b) one advantage 4 and one disadvantage 4 = 8; (c) two details × 4, insulation type 4, thickness 4 and quality of sketch 5 = 21. Complete 50.'
S2 = 'No printed choice; the attic insulation material in (c) is an open response.'
A2 = add('2', 'a', '(a)', 'Using notes and neat freehand sketches, describe the procedures to be followed when injecting the insulation into the cavity. Specify the type of insulation to be used.',
         [row('description-1', 'Valid description one', 4, 'Such as: carried out by a specialist company registered with SEAI; 22 mm holes drilled through the outer leaf at 800 mm horizontally and 1350 mm vertically, with extra holes at cills and heads.'),
          row('description-2', 'Valid description two', 4, 'A second, different step. Such as: polystyrene beads pumped in with a light glue that sets them solid; the holes filled and blended with the external finish.'),
          row('insulation', 'Type of insulation', 4, 'Such as: polystyrene beads.'),
          row('detail', 'Valid detail', 4, 'A valid detail on the sketch, as in the scheme’s model sketches.'),
          quality('Quality of sketch (excellent, good, fair)', 5)],
         ['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q2-injecting', 'Insulating materials (6.2) in a cavity wall (3.3).', B2, S2)
B2b = add('2', 'b', '(b)', 'Discuss one advantage and one disadvantage of this method of cavity insulation.',
          [row('advantage', 'One advantage', 4, 'Such as: less heat loss and lower bills; no interference inside; the floor area unchanged; economical.'),
           row('disadvantage', 'One disadvantage', 4, 'Such as: the cavity is bridged, a problem on exposed sites; damp may cross it; the holes show; the beads may not fill it completely.')],
          ['cons-6-2', 'cons-6-3'], ['heat-loss-insulation'], 'q2-pros-cons', 'Insulation (6.2) and running costs (6.3).', B2, S2)
C2 = add('2', 'c', '(c)', 'Using notes and neat freehand sketches, show how the attic is to be insulated and include the insulation to the water storage tank. Specify the insulation material for the attic and give its typical thickness.',
         [row('detail-1', 'Valid detail one', 4, 'Such as: glass fibre quilt, 100 mm between the joists and 200–300 mm across them, with a vapour barrier on the warm side and ventilation above.'),
          row('detail-2', 'Valid detail two', 4, 'A second, different detail. Such as: the tank insulated on the sides and top but not underneath, with 65–100 mm polystyrene board; the pipes in pipe sections; or blown insulation by a specialist.'),
          row('insulation', 'Type of insulation', 4, 'Such as: glass fibre, sheep’s wool, rockwool or cork quilt; blown glass, mineral or cellulose fibre; polystyrene board.'),
          row('thickness', 'Thickness of insulation', 4, 'Such as: 100 mm between the joists and 200–300 mm over them.'),
          quality('Quality of sketch (excellent, good, fair)', 5)],
         ['cons-3-9', 'cons-6-2', 'cons-5-2'], ['roofs', 'heat-loss-insulation', 'hot-water-space-heating'], 'q2-attic',
         'Insulating the roof space (3.9, 6.2) and its cistern (5.2).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-injecting', B2, S2, parts(A2, B2b, C2))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p16 (printed 13): (a) best 9 of 16 listed details × 4 = 36 and quality of sketch 6 = 42; (b) two advantages × 4 = 8. Complete 50.'
S3 = 'The printed component list is required content, not a choice; the best-nine list is a marking menu.'
A3 = add('3', 'a', '(a)', 'Using a single-line labelled diagram, show the pipework required to connect the back boiler, cylinder and expansion tank. Include the following in your diagram: back boiler and indirect cylinder; expansion tank and overflow; rising main; pipework and insulation; valves.',
         [row('details', 'Any 9 of the above details (4 marks each)', 36, 'Credit the best NINE acceptable details at 4 marks each, capped at 36. Secondary circulation: 15 mm rising main with stop valve; insulated storage tank and ballvalve; 22 mm overflow; 22 mm insulated cold feed to the cylinder; insulated indirect cylinder; 22 mm insulated expansion pipe; 22 mm hot water supply. Primary circulation: 15 mm supply to the expansion tank; insulated expansion tank with ballvalve; 22 mm overflow; 22 mm insulated cold feed; 28 mm primary return; stove and back boiler; 28 mm primary flow; 22 mm insulated expansion pipe; valves.', list(range(0, 37, 4))),
          quality('Quality of sketch (excellent, good, fair)', 6)],
         ['cons-5-2', 'cons-5-3'], ['hot-water-space-heating'], 'q3-system', 'Hot water systems and cylinders (5.2) heated by a stove (5.3).', B3, S3)
B3b = add('3', 'b', '(b)', 'Discuss two advantages of using a wood burning stove to heat domestic hot water.',
          [row('advantage-1', 'Advantage one', 4, 'Such as: wood is renewable and cheaper; modern stoves are highly efficient and designed to heat hot water.'),
           row('advantage-2', 'Advantage two', 4, 'A second, different advantage. Such as: nearly carbon neutral as trees re-absorb the CO₂; supplements other heating as fossil fuels dwindle; logs from waste wood or fast-growing willow.')],
          ['cons-5-3', 'cons-1-2'], ['hot-water-space-heating', 'planning-sustainability-environment'], 'q3-advantages', 'Heating (5.3) from a renewable fuel (1.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-system', B3, S3, parts(A3, B3b))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p17 (printed 14): (a) and (b) each two descriptions × 3, sketch 4 and quality 5 = 15; (c) hinge sketch quality 5, two details × 3, sketch 4 and quality 5 = 20. Complete 50.'
S4 = 'No printed choice; the hinge in (c) is an open response.'
DOOR = (['cons-4-5'], ['windows-doors'])
A4 = add('4', 'a', '(a)', 'Show, using notes and neat freehand sketches, how to ensure that the doorframe is assembled square prior to fitting the door.',
         [row('description-1', 'Valid description one', 3, 'Such as: the head joined to the two jambs with rebated butt joints, nailed or screwed.'),
          row('description-2', 'Valid description two', 3, 'A second, different step. Such as: a corner checked with a large steel square and a brace fixed within the rebate; a cross piece at the bottom holding the width.'),
          row('sketch', 'Sketch', 4, 'A sketch of the squared, braced frame, as in the scheme’s model sketches.'),
          quality('Quality of sketch (excellent, good, fair)', 5)],
         ['cons-4-5', 'cons-10-7'], ['windows-doors', 'wood-rot-ventilation'], 'q4-scheme', 'Internal door frames (4.5) set out accurately (10.7).', B4, S4)
B4b = add('4', 'b', '(b)', 'Show, using notes and neat freehand sketches, how the doorframe is fitted in the block wall.',
          [row('description-1', 'Valid description one', 3, 'Such as: the frame placed in the opening against the lintel, the jambs plumb, with the brace and spacer holding it square.'),
           row('description-2', 'Valid description two', 3, 'A second, different step. Such as: small wedges to firm it; special screws, rawl bolts, anchor fixings or brackets into the blockwork.'),
           row('sketch', 'Sketch', 4, 'A sketch of the frame fixed in the wall, as in the scheme’s model sketches.'),
           quality('Quality of sketch (excellent, good, fair)', 5)],
          *DOOR, 'q4-scheme', 'Fixing internal door frames (4.5).', B4, S4)
C4 = add('4', 'c', '(c)', 'Sketch a suitable hinge for this door and show, using notes and neat freehand sketches, the steps involved in fitting one hinge to the door.',
         [quality('Quality of sketch (excellent, good, fair)', 5, 'the hinge sketch', 'hinge'),
          row('detail-1', 'Valid detail one', 3, 'Such as: a butt hinge; its position and ends marked on the door edge; a marking gauge set to the width and the leaf thickness.'),
          row('detail-2', 'Valid detail two', 3, 'A second, different step. Such as: the waste removed with a sharp bevel-edged chisel, or a router and jig, the trench sloped slightly on the outer edge.'),
          row('sketch', 'Sketch', 4, 'A sketch of the hinge being fitted, as in the scheme’s model sketches.'),
          quality('Quality of sketch (excellent, good, fair)', 5)],
         ['cons-4-5', 'cons-3-7'], ['windows-doors'], 'q4-scheme', 'Hanging an internal door (4.5) with its ironmongery (3.7).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-scheme', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p18 (printed 15): (a) best 9 of 10 listed details × 4 = 36 and draughting, accuracy and scale 8 = 44; (b) sound detail 6. Complete 50.'
S5 = 'One required section and one required sound method. The best-nine detail list is a marking menu, not a printed choice.'
A5 = add('5', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the floor and stud partition. Show all the construction details from the bottom of the plasterboard ceiling, through the floor joists, the door and saddle to a point 1.5 metres above finished floor level. Label the components and give their typical sizes.',
         [row('details', 'Any 9 of the above details (4 marks each)', 36, 'Credit the best NINE acceptable details at 4 marks each, capped at 36. Marked details: plasterboard ceiling; 225 × 50 mm joists; tongued and grooved floor; door saddle; 120 × 20 mm skirting each side; 70 × 20 mm architrave each side; the internal door; 110 × 44 mm door frame.', list(range(0, 37, 4))),
          row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the section, excellent, good or fair, up to 8.')],
         ['cons-1-5', 'cons-4-5', 'cons-4-3'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls'], 'q5-scheme',
         'Scaled drawing (1.5) of a stud partition and door (4.5) on a timber upper floor (4.3).', B5, S5)
B5b = add('5', 'b', '(b)', 'Show on your drawing one method that will help reduce the transmittance of sound through the stud partition.',
          [row('sound', 'Method that will help reduce the transmittance of sound through stud partition', 6, 'Such as: mineral wool between the studs; acoustic sealing tape at the surrounding walls; acoustic plasterboard or double layers with staggered joints; a double stud partition with acoustic quilt.')],
          ['cons-8-3', 'cons-4-5'], ['sound', 'windows-doors'], 'q5-scheme', 'Airborne sound insulation (8.3) of a stud partition (4.5).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-scheme', B5, S5, parts(A5, B5b))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p19 (printed 16): (a) for each printed situation two precautions × 5 and reasons 4 = 14, 42; (b) two precautions × 2 and quality of sketch 4 = 8. Complete 50.'
S6 = 'All three printed situations in (a) are required, each separately marked; not a choice.'
A6 = add('6', 'a', '(a)', 'List two specific safety precautions to be observed in each of the following situations and give one reason for each safety precaution listed: using a ladder when painting an external wall; using a veneering knife to cut veneers; using a jig saw to cut a wooden panel.',
         [row('ladder', 'Safety precautions using a ladder when painting an external wall', 14, 'Two precautions 5 each and reasons 4. Such as: a ladder in good condition on firm level ground at 1:4; no over-reaching, three points of contact; coned off from traffic and held by a helper — the angle and over-reaching are dangerous.'),
          row('veneer', 'Safety precautions when using a veneering knife to cut veneers', 14, 'Two precautions 5 each and reasons 4. Such as: a sharp, good-quality knife on a solid surface; a straight edge held firmly to guide it; light passes; concentration — a sharp knife on a firm surface is safer.'),
          row('jigsaw', 'Safety precautions when using a jig saw to cut a wooden panel', 14, 'Two precautions 5 each and reasons 4. Such as: the wood firmly clamped; the lead clear of the blade; cut slowly; eye and face protection and a mask — moving wood and a cut lead are dangerous.')],
         ['cons-1-8', 'cons-9-4'], ['site-safety'], 'q6-precautions', 'Safety on site (1.8) and with tools (9.4).', B6, S6)
B6b = add('6', 'b', '(b)', 'Using notes and neat freehand sketches, describe two specific safety precautions that should be observed when using electrical tools out-of-doors.',
          [row('precaution-1', 'Precaution one', 2, 'Such as: dry conditions and double-insulated tools.'),
           row('precaution-2', 'Precaution two', 2, 'A second, different precaution. Such as: leads and connections in good condition; 110 volt equipment outdoors; eye and face protection.'),
           quality('Quality of sketch (excellent, good, fair)', 4)],
          ['cons-9-4'], ['site-safety'], 'q6-outdoors', 'Safety with electrical tools (9.4).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b], 'q6-precautions', B6, S6, parts(A6, B6b))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p20 (printed 17): (a) gutter 4, downpipe 4, sketch quality 5 and two descriptions × 4 = 21; (b) tank and piping 4, filter 4, sketch quality 5 and two descriptions × 4 = 21; (c) two advantages with uses × 4 = 8. Complete 50.'
S7 = 'No printed choice; the scheme gives a model system.'
A7 = add('7', 'a', '(a)', 'Using notes and neat freehand sketches, show how the rainwater is collected from the lean-to roof and discharged to a gulley trap at ground level. Label the components and give their typical sizes.',
         [row('gutter', 'Eave gutter - typical 125 mm', 4, 'The eaves gutter, typically 125 mm.'),
          row('downpipe', 'Downpipe - typical 65 mm', 4, 'The downpipe, typically 65 mm.'),
          quality('Quality of sketch (excellent, good, fair)', 5),
          row('description-1', 'Valid description one', 4, 'Such as: rainwater collected into the gutter from the sloping roof, with stopends at its ends.'),
          row('description-2', 'Valid description two', 4, 'A second, different description. Such as: the water runs through outlets into the downpipe and down to the gully or back inlet gully.')],
         ['cons-5-4', 'cons-3-10'], ['drainage', 'roofs'], 'q7-scheme', 'Eaves gutters and rainwater pipes (5.4) at the roof eaves (3.10).', B7, S7)
B7b = add('7', 'b', '(b)', 'The rainwater is conveyed to the underground water storage tank for re-use. Using notes and neat freehand sketches, show the pipework necessary to convey the rainwater from the gulley trap to the storage tank and show the location of a rainwater filter in this system.',
          [row('tank', 'Storage tank and Underground piping', 4, 'The underground piping and the storage tank, with an overflow and a submersible pump.'),
           row('filter', 'Filter', 4, 'The filter between the gully trap and the tank, accessible from the top for cleaning.'),
           quality('Quality of sketch (excellent, good, fair)', 5),
           row('description-1', 'Valid description one', 4, 'Such as: rainwater flows from the gully through underground piping; the filter traps sediment.'),
           row('description-2', 'Valid description two', 4, 'A second, different description. Such as: filtered water flows into the tank, reused as grey water only, pumped back to the house.')],
          ['cons-5-4', 'cons-5-5'], ['drainage'], 'q7-scheme', 'Surface water (5.4) carried underground (5.5).', B7, S7)
C7 = add('7', 'c', '(c)', 'Discuss two advantages of storing rainwater and give two suitable uses for the stored rainwater.',
         [row('use-1', 'Valid advantage and use one', 4, 'An advantage and a use. Such as: less domestic water used — watering gardens and plants with no chlorine.'),
          row('use-2', 'Valid advantage and use two', 4, 'A second advantage and use. Such as: less surface water to the drains and less flooding, kinder to appliances — washing machines, toilets and outdoor cleaning.')],
         ['cons-1-2', 'cons-5-2'], ['planning-sustainability-environment', 'services-water-gas-electrical'], 'q7-uses', 'Sustainable water use (1.2) in the water supply (5.2).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-scheme', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p21 (printed 18): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination. No pre-audit card existed for this question.'
TERMS = [
    ('concrete lintel', 'Concrete lintel', ['cons-3-4', 'cons-2-6'], ['foundations-floors-walls', 'concrete'],
     'a reinforced, often pre-stressed, concrete beam spanning the opening over a window or door, carrying the blockwork above to the wall on either side; its length suits the opening.', 'Lintels (3.4) in reinforced concrete (2.6).'),
    ('mortice and tenon', 'Mortice and tenon joint', ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'],
     'used in furniture, doors and windows: a mortice formed in one piece and a tenon, ideally a third of the thickness, on the other to fit it.',
     'Joints (10.1) and the choice of joint (10.4). The Ordinary reference taxonomy has no joinery heading; the term keeps the Wood, Rot & Ventilation association used for joinery, and 10.1/10.4 are declared outside that heading’s crosswalk.'),
    ('energy rating', 'Energy rating', ['cons-6-3'], ['heat-loss-insulation'],
     'the BER of a dwelling, an A to G rating of its energy performance and CO₂ emissions, compulsory when a house is sold or rented since 1 January 2009.', 'Heat loss and running costs (6.3).'),
    ('door saddle', 'Door saddle', ['cons-3-7'], ['windows-doors'],
     'a hardwood or softwood piece, typically 110 × 15 mm, fixed at the bottom of the door frame, giving clearance under the door and covering the joint between floor coverings.', 'Door details (3.7).'),
    ('quarter sawing', 'Quarter sawing', ['cons-10-3'], ['wood-rot-ventilation'],
     'radial conversion of a log cut parallel to the rays, giving stable boards that wear evenly and silver grain in oak; expensive and labour intensive.', 'The conversion of timber into boards (10.3).'),
    ('ridge board', 'Ridge board', ['cons-3-8'], ['roofs'],
     'the horizontal softwood member at the apex between the tops of the rafters, giving the roof rigidity and straightness; opposite rafters are nailed to it.', 'Roof forms (3.8).'),
    ('triple glazing', 'Triple glazing', ['cons-3-6', 'cons-6-2'], ['windows-doors', 'heat-loss-insulation'],
     'three layers of glass giving better insulation, sound performance and U-value, less condensation and a comfortable temperature, ideal on exposed sites.', 'Glazing (3.6) that cuts heat loss (6.2).'),
    ('window cill', 'Window cill', ['cons-3-6'], ['windows-doors'],
     'usually a reinforced concrete unit under the window, sloping away to shed rainwater, with a drip beneath; also PVC, stone, steel or wood.', 'Window details at the sill (3.6).'),
    ('vapour barrier', 'Vapour barrier', ['cons-6-6'], ['air-tightness-condensation'],
     'a continuous membrane on the warm side of insulation slowing water vapour into it (the 5:1 rule); used in timber frame walls, flat roofs and attic conversions.', 'Vapour barriers (6.6).'),
]
Q8 = add('8', 'terms', '', 'Explain, with the aid of notes and neat freehand sketches, any five of the following: ' + '; '.join(t[0] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Primary communication of relevant information', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{t[1]}: {t[4]}' for t in TERMS),
               group=dict(claimMax=5, perOption=10, options=[t[1] for t in TERMS]))],
         list(dict.fromkeys(n for t in TERMS for n in t[2])), list(dict.fromkeys(a for t in TERMS for a in t[3])), 'q8-terms',
         'The union of the nine printed terms: ' + ' '.join(t[5] for t in TERMS), B8, S8)

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p22 (printed 19): (a) two reasons × 4 = 8; (b) three printed steps × 4, sketch details 4 and quality 5 = 21; (c) three printed steps × 4, sketch details 4 and quality 5 = 21. Complete 50.'
S9 = '"one of the windows" and "one of the houses" name the window being repaired, not a choice.'
A9 = add('9', 'a', '(a)', 'Discuss two reasons why it is advisable to repair the existing wooden windows in these houses rather than replace them with new windows.',
         [row('reason-1', 'Valid reason one', 4, 'Such as: conserving the existing wooden frames for environmental reasons; keeping the original features, style, character and workmanship.'),
          row('reason-2', 'Valid reason two', 4, 'A second, different reason. Such as: modern windows may not suit the building; repair is cheaper, sustainable and less disruptive.')],
         ['cons-1-2', 'cons-3-5'], ['planning-sustainability-environment', 'windows-doors'], 'q9-reasons', 'Windows (3.5) in the built environment (1.2).', B9, S9)
B9b = add('9', 'b', '(b)', 'Describe, using notes and neat freehand sketches, the steps to be followed when replacing a broken pane of glass in one of the windows.',
          [row('cleaning', 'Broken glass / Cleaning out rebate', 4, 'The broken glass and pins removed and the rebate scraped, cleaned and sanded.'),
           row('pins', 'Tool removing / replacing glazing pins / fasteners', 4, 'Removing and replacing the glazing pins or fasteners with a suitable tool.'),
           row('glazing', 'Inserting new glass / Applying new glazing compound', 4, 'The rebate primed and bedded with glazing compound, the glass inserted and pinned, then compound bevelled round the edge and trimmed.'),
           row('details', 'Valid details', 4, 'Valid details on the sketch, as in the scheme’s model sketch.'),
           quality('Quality of sketch (excellent, good, fair)', 5)],
          ['cons-3-6'], ['windows-doors'], 'q9-glass', 'Glass and glazing (3.6).', B9, S9)
C9 = add('9', 'c', '(c)', 'Describe, using notes and neat freehand sketches, the steps to be followed when removing the existing paint, preparing the surface and repainting a window frame in one of the houses.',
         [row('removal', 'Removal of existing paint by sandpaper, scraper, chemical or heat gun', 4, 'The floor protected; the old paint removed with sandpaper, a scraper, chemical stripper or a heat gun.'),
          row('preparation', 'Preparation of surfaces by sanding, taping of hinges, catches, glass perimeter', 4, 'Surfaces clean and dry; hinges, catches and the glass edge masked with tape.'),
          row('painting', 'Application of primer / undercoat / final coat', 4, 'Primer and undercoat, then the final coats brushed in the direction of the grain.'),
          row('details', 'Valid details', 4, 'Valid details on the sketch, as in the scheme’s model sketch.'),
          quality('Quality of sketch (excellent, good, fair)', 5)],
         ['cons-10-7', 'cons-3-5'], ['wood-rot-ventilation', 'windows-doors'], 'q9-paint', 'Surface preparation and painting of timber (10.7) windows (3.5).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-glass', B9, S9, parts(A9, B9b, C9))

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and three other questions (200 marks); all question banks retained, no full-exam Cartesian cards.'),
          (3, 'any five', 'Q8 closed choose-five of nine printed terms: one card with an any-five group over all nine terms (choice is not a route).'),
          (3, 'one of', 'Q9(b) "in one of the windows": the window being reglazed, not a candidate choice.'),
          (3, 'one of', 'Q9(c) "in one of the houses": the window frame being repainted, not a candidate choice.')]
FINITE = {'8': dict(choose=5, options=[t[1] for t in TERMS], cardId=Q8['id'], groupRowId='terms', wholeQuestionMarks=50, termMarks=10)}
GAPS = [dict(cardId=Q8['id'], canonicalTopicIds=['cons-10-1', 'cons-10-4'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers joinery (10.1, 10.4, mortice and tenon).')]
D.finish(LEDGER, FINITE, {}, taxonomy_gaps=GAPS, whole_choices={'q8-terms'})
