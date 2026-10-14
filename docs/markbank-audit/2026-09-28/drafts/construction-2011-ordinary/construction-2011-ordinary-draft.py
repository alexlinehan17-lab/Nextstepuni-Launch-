"""Draft the 2011 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 16-24). The paper was never carded, so every task is added. Q8 "any five of nine" is ONE card
(choice is not a route); Q7(b)'s "one of these appliances" is one task marked alike for either.
Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Triple-glazed window head section', concept='window-head-section',
              stem='A triple glazed timber casement window is fixed in the external wall of a dwelling house, as shown in the sketch. The external wall is a 350 mm concrete block wall with an insulated cavity. The wall is plastered on both sides. The fixed frame of the window is 150 mm × 80 mm.',
              note='Original sketch and specification retained. The scheme prints the draughting, accuracy and scale band after the part (b) row, so it is marked with the flashing and insulation detail.'),
    '2': dict(page=2, title='Cavity fill and internal insulation', concept='cavity-fill-internal-insulation',
              stem='A dwelling house built 40 years ago, as shown in the sketch, has a 300 mm external concrete block wall with a 100 mm un-insulated cavity. The owner intends to refurbish the house to improve the thermal insulation levels of the external walls by: injecting insulation into the cavity of the external walls and fixing an internal insulation system to the external walls.',
              note='Original sketch retained. Both printed systems are required in (a) and (b), each separately marked.'),
    '3': dict(page=2, title='Back boiler hot water to a basin and mixer shower', concept='back-boiler-mixer-shower',
              stem='A wood burning stove has a back boiler fitted to heat domestic water for a dwelling house.',
              note='Original sketch retained. The listed components are required content, not a choice; the best-seven list is a marking menu.'),
    '4': dict(page=2, title='Kitchen cabinets, a solid wood floor and the work triangle', concept='kitchen-cabinets-floor',
              stem='The sketch shows the layout of a kitchen space. The location of the kitchen cabinets, sink, cooker and fridge is shown.',
              note='Original plan retained. "one method" in (a) and (b) is an open choice of method; the scheme gives typical methods.'),
    '5': dict(page=3, title='Closed string stairs section', concept='closed-string-stairs-section',
              stem='The sketch shows a portion of a closed string timber stairs suitable for a dwelling house.',
              note='Original sketch retained. The scheme prints the draughting, accuracy and scale band after the part (b) row, so it is marked with the anti-creak detail.'),
    '6': dict(page=3, title='Fitting a cill, working at height and lathe safety', concept='cill-height-lathe-safety', stem='',
              note='Both printed situations in (a) are required, each separately marked.'),
    '7': dict(page=3, title='Pumped rainwater harvesting', concept='pumped-rainwater-harvesting',
              stem='The sketch shows an outline of a single storey house, an underground rainwater storage tank and a separate rainwater storage tank in the attic of the house.',
              note='Original sketch retained. In (b) either printed appliance may be chosen; the scheme marks the toilet and the washing machine alike.'),
    '8': dict(page=3, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=3, title='A wooden garden seat', concept='garden-seat',
              stem='The sketch shows a wooden garden seat designed for use in a public park.',
              note='Original sketch retained. The design feature, joint and finish are open responses; the scheme gives typical examples.'),
}
SCHEME_PAGES = {'1': [4, 16], '2': [5, 6, 17], '3': [6, 7, 18], '4': [7, 8, 9, 19], '5': [9, 20], '6': [10, 21], '7': [11, 22], '8': [12, 13, 23], '9': [14, 15, 24]}
D = cp.Draft(HERE, 2011, 'ordinary', ('d02ee1cffc9d9c404ca6299e98001f373fba97977988b9b1b0f46150bc81d304',
                                      '2ab53d9280c298352ee2d11cce327a37d5b1c9e08ddd0f33cd3243d29fd2fd7b'), 0, QUESTIONS, SCHEME_PAGES)
row, add, compose = D.row, D.add, D.compose
BAND4 = [0, 2, 3, 4]
BAND5 = [0, 3, 4, 5]
BAND3 = [0, 1, 2, 3]


def parts(*cards):
    return D.parts(*[(letter, c['questionText']) for letter, c in zip('abc', cards)])


D.figures({
    'q1-original': D.paper(2, [30, 39, 580, 208]), 'q2-original': D.paper(2, [30, 208, 580, 407]),
    'q3-original': D.paper(2, [30, 407, 580, 592]), 'q4-original': D.paper(2, [30, 592, 580, 790]),
    'q5-original': D.paper(3, [30, 39, 580, 170]), 'q6-original': D.paper(3, [30, 170, 580, 284]),
    'q7-original': D.paper(3, [30, 284, 580, 498]), 'q8-original': D.paper(3, [30, 498, 580, 593]),
    'q9-original': D.paper(3, [30, 593, 580, 790]),
    'q1-section': D.scheme(4, [25, 45, 580, 778]),
    'q2-systems': D.scheme(5, [25, 45, 580, 575]), 'q2-pros-cons': D.composite((5, [25, 575, 580, 778]), (6, [25, 45, 580, 384])),
    'q3-system': D.scheme(6, [25, 384, 580, 778]), 'q3-shower': D.scheme(7, [25, 45, 580, 252]),
    'q4-cabinets': D.scheme(7, [25, 252, 580, 778]), 'q4-floor': D.scheme(8, [25, 45, 580, 710]), 'q4-layout': D.scheme(9, [25, 45, 580, 194]),
    'q5-scheme': D.scheme(9, [25, 194, 580, 778]),
    'q6-precautions': D.scheme(10, [25, 45, 580, 435]), 'q6-lathe': D.scheme(10, [25, 435, 580, 778]),
    'q7-pump': D.scheme(11, [25, 45, 580, 441.5]), 'q7-appliance': D.scheme(11, [25, 441.5, 580, 640]), 'q7-reason': D.scheme(11, [25, 640, 580, 778]),
    'q8-terms': D.composite((12, [25, 60, 580, 778]), (13, [25, 45, 580, 778])),
    'q9-feature': D.scheme(14, [25, 45, 580, 265]), 'q9-joint': D.scheme(14, [25, 265, 580, 410]),
    'q9-finish': D.composite((14, [25, 410, 580, 778]), (15, [25, 60, 580, 250])),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p16 (printed 13): (a) best 7 of 10 listed details × 6 = 42; (b) flashing and insulation 2 + 2 = 4, and draughting, accuracy and scale 4 (4/3/2) printed after it = 8. Complete 50.'
S1 = 'One required section and one required flashing and insulation detail. The best-seven detail list is a marking menu, not a printed choice.'
A1 = add('1', 'a', '(a)', 'To a scale of 1:5 draw a vertical section through the top portion of the window showing the fixed window frame and the concrete lintels. Show the typical construction details from 300 mm below to a level 400 mm above the concrete lintels. Include four typical dimensions.',
         [row('details', 'Any 7 of the above details (6 marks each)', 42, 'Credit the best SEVEN acceptable details at 6 marks each, capped at 42. Marked details: 15 mm external plaster; 100 mm outer leaf; 50 mm residual cavity; 100 mm insulation; 100 mm inner leaf; 15 mm internal plaster; 100 × 70 mm pre-stressed concrete lintels; the 150 × 80 mm window head; triple low-e glazing; typical dimensions.', list(range(0, 43, 6)))],
         ['cons-1-5', 'cons-3-6', 'cons-3-4', 'cons-3-3'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls'], 'q1-section',
         'Scaled drawing (1.5) of a window head (3.6) with its lintels (3.4) in a cavity wall (3.3).', B1, S1)
B1b = add('1', 'b', '(b)', 'Show clearly on your drawing the flashing (dpc) and the insulation at the window head.',
          [row('flashing', 'Valid detail - flashing (dpc) and the insulation (2 marks + 2 marks)', 4, 'The flashing (DPC) at the window head 2 and the insulation above the window head 2, as in the scheme’s model section.'),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 4, 'Draughting, accuracy and scale of the whole section: excellent 4, good 3, fair 2. The scheme prints this band after the part (b) row.', BAND4)],
          ['cons-3-4', 'cons-6-2'], ['foundations-floors-walls', 'heat-loss-insulation'], 'q1-section', 'A DPC tray (3.4) and insulation (6.2) at the window head.', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p17 (printed 14): (a) for each printed system, notes — description 6 and insulation type 4 — and sketch — quality 6 and detail 4 = 20, 40; (b) an advantage and a disadvantage of each system × 5 = 10. Complete 50.'
S2 = 'Both printed systems are required in (a) and (b), each separately marked; not a choice.'
A2 = add('2', 'a', '(a)', 'For each insulation system listed above, show using notes and neat freehand sketches the procedures to be followed when applying the insulation system. For each system, specify the insulation material used.',
         [row('cavity-notes', 'Injecting the insulation into the cavity of the external wall - Notes', 10, 'A valid description 6 and the type of insulation 4. Such as: by a specialist company, 22 mm holes drilled through the outer leaf at 800 mm horizontally and 1350 mm vertically, with extra holes at cills and heads; polystyrene beads with a light glue, or cellulose, pumped in; the holes filled to match.'),
          row('cavity-sketch', 'Injecting the insulation into the cavity of the external wall - Sketch', 10, 'The quality of the sketch 6 and a valid detail 4, as in the scheme’s model sketches.'),
          row('internal-notes', 'Fixing an internal insulation system to the external walls - Notes', 10, 'A valid description 6 and the type of insulation 4. Such as: 50 × 50 mm treated battens at 400 mm centres with insulation between, a vapour barrier and 12 mm plasterboard with a skim coat; or insulated plasterboard on dabs with mechanical fixings. Cork, wood fibre, sheep’s wool, fibreglass, polystyrene or polyurethane.'),
          row('internal-sketch', 'Fixing an internal insulation system to the external walls - Sketch', 10, 'The quality of the sketch 6 and a valid detail 4, as in the scheme’s model sketches.')],
         ['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q2-systems', 'Insulating materials (6.2) in a cavity wall (3.3).', B2, S2)
B2b = add('2', 'b', '(b)', 'Discuss one advantage and one disadvantage of each system of insulation.',
          [row('cavity', 'Advantage and disadvantage of injecting insulation into the cavity', 5, 'Such as: less heat loss, quick and economical, with no disturbance inside and the block’s thermal mass kept; but the cavity is bridged, damp may cross it, the holes show and the fill may leave cold spots.'),
           row('internal', 'Advantage and disadvantage of fixing internal insulation system', 5, 'Such as: a better U-value, no change outside and local labour can do it; but rooms lose floor area, the work is disruptive, dusty and dear, and fittings must be moved.')],
          ['cons-6-2', 'cons-6-3'], ['heat-loss-insulation'], 'q2-pros-cons', 'Insulation (6.2) and running costs (6.3).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b], 'q2-systems', B2, S2, parts(A2, B2b))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p18 (printed 15): (a) best 7 of 12 listed details × 5 = 35 and quality of sketch 6 = 41; (b) two advantages, 5 and 4 = 9. Complete 50.'
S3 = 'The printed component list is required content, not a choice; the best-seven list is a marking menu.'
WATER = (['cons-5-2'], ['hot-water-space-heating', 'services-water-gas-electrical'])
A3 = add('3', 'a', '(a)', 'Using a single-line labelled diagram, show the pipework required to supply hot and cold water to a wash hand basin and to a mixer shower in a bathroom, as shown in the sketch. Include the following in your diagram: water storage tank and overflow; rising main; indirect cylinder; pipework to wash hand basin and shower; valves and insulation.',
         [row('details', 'Any 7 of the above details (5 marks each)', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: rising main; ballvalve; cold water storage tank; overflow; cold feed to the indirect cylinder; indirect cylinder; expansion pipe; hot water supply to the appliances; cold supply from the tank to the appliances; valves; insulation to the tank, cylinder and pipework; labelling.', list(range(0, 36, 5))),
          row('presentation', 'Quality of sketch (excellent, good, fair)', 6, 'Quality of the sketch, excellent, good or fair, up to 6.')],
         *WATER, 'q3-system', 'Hot and cold water systems, cisterns and cylinders (5.2).', B3, S3)
B3b = add('3', 'b', '(b)', 'Discuss two advantages of using a mixer shower as shown, which is connected to the system outlined at 3(a) above, rather than an electric power shower.',
          [row('advantage-1', 'Advantage one', 5, 'Such as: water heated by a renewable, carbon-neutral wood stove, cheaper and better for the environment than an electric shower using fossil-fuel electricity.'),
           row('advantage-2', 'Advantage two', 4, 'A second, different advantage. Such as: cheaper to buy and fit; uses less water; gravity pressure with no pump, using less electricity.')],
          ['cons-5-2', 'cons-5-8'], ['hot-water-space-heating', 'services-water-gas-electrical'], 'q3-shower', 'Hot water supply (5.2) against electric heating (5.8).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-system', B3, S3, parts(A3, B3b))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p19 (printed 16): (a) two descriptions × 4, sketch quality 6 and detail 4 = 18; (b) two descriptions × 4, sketch quality 6 and detail 4, wood 2 and two reasons 4 = 24; (c) two advantages × 4 = 8. Complete 50.'
S4 = '"one method" in (a) and (b) is an open choice of method; the scheme gives typical methods.'
A4 = add('4', 'a', '(a)', 'Using notes and neat freehand sketches, show one method of fixing the overhead cabinets to a concrete block wall so that they are both level and secure.',
         [row('description-1', 'Valid description one', 4, 'Such as: a chipboard, MDF or solid wood strip inside the top of the unit, drilled for at least two screws; or steel or plastic angle brackets.'),
          row('description-2', 'Valid description two', 4, 'A second, different step. Such as: a level line about 500 mm above the worktop with a temporary straight edge to rest the cabinet on; holes marked, bored and plugged; the cabinet screwed in place and caps fitted.'),
          row('presentation', 'Quality of sketch (excellent, good, fair)', 6, 'Quality of the sketch, excellent, good or fair, up to 6.'),
          row('detail', 'Valid detail', 4, 'A valid detail on the sketch, as in the scheme’s model sketches.')],
         ['cons-10-2'], ['wood-rot-ventilation'], 'q4-cabinets', 'Fitting simple fitments (10.2).', B4, S4)
B4b = add('4', 'b', '(b)', 'A solid wood floor is to be fitted on the existing concrete floor. Using notes and neat freehand sketches show one method of fitting the wooden floor. Recommend a wood suitable for a kitchen floor and give two reasons for your choice.',
          [row('description-1', 'Valid description one', 4, 'Such as: the concrete cleaned and levelled with compound; a straight edge fixed on a centre line as a base line.'),
           row('description-2', 'Valid description two', 4, 'A second, different step. Such as: the strips glued to the concrete with staggered joints and a 10–15 mm expansion gap round the edge; pre-finished, or varnished or oiled.'),
           row('sketch', 'Fitting the wooden floor to the existing concrete floor - Sketch', 10, 'The quality of the sketch, up to 6, and a valid detail 4.'),
           row('wood', 'Name of wood', 2, 'Such as: maple; oak; ash; pine.'),
           row('reasons', 'Two reasons', 4, 'Two reasons matching the wood, 2 each. Such as, oak: hard, durable and attractive; maple: close grained and hard wearing; pine: cheaper, renewable and easily sanded.')],
          ['cons-4-2', 'cons-10-7'], ['foundations-floors-walls', 'wood-rot-ventilation'], 'q4-floor', 'A timber finish on a solid ground floor (4.2) and the choice of timber (10.7).', B4, S4)
C4 = add('4', 'c', '(c)', 'Discuss two advantages of locating the sink, cooker and fridge in the positions shown in the sketch.',
         [row('advantage-1', 'Advantage one', 4, 'Such as: a work triangle that cuts walking while cooking; worktop space beside the sink and cooker.'),
          row('advantage-2', 'Advantage two', 4, 'A second, different advantage. Such as: the extractor removes steam from the cooking area; the sink at the window with a view, light and ventilation.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q4-layout', 'Kitchen layout in the built environment (1.2).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-floor', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p20 (printed 17): (a) best 7 of 9 listed details × 5 = 35 and typical sizes 5 = 40; (b) anti-creak detail 4, and draughting, accuracy and scale 6 printed after it = 10. Complete 50.'
S5 = 'One required section and one required anti-creak detail. The best-seven detail list is a marking menu, not a printed choice.'
STAIRS = (['cons-4-4', 'cons-10-1'], ['foundations-floors-walls', 'wood-rot-ventilation'])
A5 = add('5', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the bottom three steps of the stairs. Show the string, treads and risers and give their typical sizes.',
         [row('details', 'Any 7 of the above details (5 marks each)', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: string 250 × 44 mm; treads with 2R + G between 550 and 700 mm and a going of at least 220 mm; a nosing of at least 16 mm; risers of at most 220 mm; wedges; glue blocks; the joint between tread and riser; the pitch line; the bottom three steps.', list(range(0, 36, 5))),
          row('sizes', 'Typical sizes', 5, 'Typical sizes of the string, treads and risers.')],
         *STAIRS, 'q5-scheme', 'Stairs (4.4) and their joints (10.1).', B5, S5)
B5b = add('5', 'b', '(b)', 'Show on your drawing one design detail which will ensure that the stairs does not creak when in use.',
          [row('detail', 'Valid design detail', 4, 'Such as: vertical wedges behind the risers and horizontal wedges under the treads; glue blocks between the risers and treads and the treads and string; threaded bars holding the strings together.'),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 6, 'Draughting, accuracy and scale of the whole section, excellent, good or fair, up to 6. The scheme prints this band after the part (b) row.')],
          *STAIRS, 'q5-scheme', 'Stairs (4.4) and their joints (10.1).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-scheme', B5, S5, parts(A5, B5b))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p21 (printed 18): (a) for each printed situation two precautions × 5 and reasons 5 = 15, 30; (b) two lathe precautions × 5, reasons 3 + 2 and quality of sketch 5 (5/4/3) = 20. Complete 50.'
S6 = 'Both printed situations in (a) are required, each separately marked; not a choice.'
A6 = add('6', 'a', '(a)', 'List two specific safety precautions to be observed in each of the following situations and give one reason for each safety precaution listed: fitting a precast concrete window cill at ground floor level in a house; working at height when renovating an old house.',
         [row('cill', 'Safety precautions to be observed when fitting a precast window cill', 15, 'Two precautions 5 each and reasons 5. Such as: a clear, tidy area; help to lift, in unison; steel-capped boots and gloves; the cill rested on supports before lifting into place — so it is lifted safely and feet and hands are protected.'),
          row('height', 'Safety precautions when working at height', 15, 'Two precautions 5 each and reasons 5. Such as: scaffolding erected by a qualified person, with hand rails and toe boards; a ladder at 1:4, extending 1.0 m above the platform, secured on level ground — a safe platform, nothing falling on those below, no slipping.')],
         ['cons-1-8'], ['site-safety'], 'q6-precautions', 'Safety precautions on site (1.8).', B6, S6)
B6b = add('6', 'b', '(b)', 'Using notes and neat freehand sketches, describe two specific safety precautions that should be observed when using a wood turning lathe in school. Give one specific reason why each safety precaution listed should be observed.',
          [row('precaution-1', 'Precaution one', 5, 'Such as: know how to start and stop the lathe; face and eye protection.'),
           row('precaution-2', 'Precautions two', 5, 'A second, different precaution. Such as: a sound, properly prepared piece secured on the lathe and rotated by hand first; no loose clothing; the correct speed; supervision and concentration.'),
           row('reasons', 'Reasons for each precaution (3 marks + 2 marks)', 5, 'A reason for each precaution, 3 and 2. Such as: material may fly off; a secure, sound piece stays solid while turning.'),
           row('presentation', 'Quality of sketch (excellent, good, fair)', 5, 'Quality of the sketch: excellent 5, good 4, fair 3.', BAND5)],
          ['cons-9-4'], ['site-safety'], 'q6-lathe', 'Safety with machines in the workshop (9.4).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b], 'q6-precautions', B6, S6, parts(A6, B6b))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p22 (printed 19): (a) notes two details × 5 and sketch best three of eight details × 5 and quality 6 = 31; (b) note 5, sketch quality 6 and annotation 4 = 15; (c) reason 4. Complete 50.'
S7 = '(b) "connect one of these appliances": the toilet or the washing machine, one task marked alike for either (choice is not a route).'
A7 = add('7', 'a', '(a)', 'Using notes and neat freehand sketches show the pipework necessary to pump the rainwater from the underground storage tank to the tank in the attic. Label the components and give their typical sizes.',
         [row('detail-1', 'Valid detail one', 5, 'Such as: filtered rainwater flows from the eaves gutter to the underground tank, with an overflow to the drains or a soakaway.'),
          row('detail-2', 'Valid detail two', 5, 'A second, different detail. Such as: a submersible pump with a floating intake filter pumps to the attic tank under a control panel, with a mains top-up when the rainwater is low.'),
          row('sketch', 'Any 3 of the above details (5 marks each)', 15, 'The best three sketch details, 5 each, capped at 15: an underground tank of 2500–6500 litres; a pump with power supply, 12 mm suction pipe and floating filter; a 12 mm rainwater pipe to the control panel and attic tank; the control panel; a 12 mm mains top-up pipe; an attic tank of at least 230 litres with ball valve and 22 mm overflow; labels; typical sizes.', list(range(0, 16, 5))),
          row('presentation', 'Quality of sketch (excellent, good, fair)', 6, 'Quality of the sketch, excellent, good or fair, up to 6.')],
         ['cons-5-4', 'cons-5-2'], ['drainage', 'services-water-gas-electrical'], 'q7-pump', 'Rainwater from the gutters (5.4) pumped to a storage cistern (5.2).', B7, S7)
B7b = add('7', 'b', '(b)', 'Stored rainwater may be used in both a toilet and a washing machine. Show, using notes and neat freehand sketches, the pipework necessary to connect one of these appliances to the storage tank in the attic. Show the necessary valves.',
          [row('note', 'Valid detail', 5, 'For either appliance. Such as: a pipe from the attic rainwater tank to the toilet or washing machine, with a gate valve to the toilet or an isolating valve to the washing machine for repairs.'),
           row('presentation', 'Quality of sketch (excellent, good, fair)', 6, 'Quality of the sketch, excellent, good or fair, up to 6.'),
           row('annotation', 'Valid annotation/note for pipework', 4, 'A valid annotation of the pipework, stop valve and connection, as in the scheme’s model sketch.')],
          ['cons-5-2', 'cons-5-6'], ['services-water-gas-electrical', 'drainage'], 'q7-appliance', 'Cold water supply (5.2) to sanitary appliances (5.6).', B7, S7)
C7 = add('7', 'c', '(c)', 'Discuss one reason why the rainwater is stored in a separate storage tank in the attic.',
         [row('reason', 'Valid reason', 4, 'Such as: rainwater is not drinkable and may contain micro-organisms or be stagnant, so untreated rainwater cannot mix with treated mains water; it is used only for the toilet and washing machine.')],
         ['cons-5-2', 'cons-1-2'], ['services-water-gas-electrical', 'planning-sustainability-environment'], 'q7-reason', 'Water supply (5.2) used sustainably (1.2).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-pump', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p23 (printed 20): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination. No pre-audit card existed for this question.'
TERMS = [
    ('fascia', 'Fascia', ['cons-3-10'], ['roofs'],
     'the horizontal member fixed to the ends of the rafters, forming the eaves with the soffit; red or white deal or uPVC; it finishes the rafter ends and carries the gutter brackets.', 'Roof eaves (3.10).'),
    ('strip foundation', 'Strip foundation', ['cons-2-4'], ['foundations-floors-walls'],
     'the most common concrete foundation, a reinforced strip under the wall, typically three times the wall thickness wide and 300 mm thick; the wall central and the load spread at 45°.', 'Strip foundations (2.4).'),
    ('thermostatic valve', 'Thermostatic valve', ['cons-5-3'], ['hot-water-space-heating', 'services-water-gas-electrical'],
     'a radiator valve set to the room temperature, regulating the flow to control the radiator’s output; inexpensive, it cuts CO₂ and energy costs.', 'Temperature control of heating systems (5.3).'),
    ('window board', 'Window board', ['cons-3-6'], ['windows-doors'],
     'a hardwood, softwood or uPVC board, 18–30 mm thick, fixed horizontally inside the window frame, with insulation beneath against a cold bridge and airtight taped or mastic joints.', 'Window details at the sill (3.6).'),
    ('butt hinge', 'Butt hinge', ['cons-3-7'], ['windows-doors'],
     'a brass or mild steel hinge, 12–150 mm long, of two leaves and a pin, fitted into shallow trenches with countersunk screws; used for doors, windows and boxes.', 'Door ironmongery (3.7).'),
    ('rafter', 'Rafter', ['cons-3-8'], ['roofs'],
     'the sloping member of the roof from the eaves to the ridge board, usually white deal, typically 200 × 50 mm, secured to the wall plate and the ridge board.', 'Roof forms (3.8).'),
    ('solar panel', 'Solar panel', ['cons-6-4'], ['planning-sustainability-environment'],
     'collects solar radiation and converts it to heat; usually on a south-facing roof or a ground fixing, flat plate or evacuated tube, used with other heating; reduces CO₂.', 'Solar heat gain (6.4).'),
    ('wall tie', 'Wall tie', ['cons-3-3'], ['foundations-floors-walls'],
     'a polypropylene or stainless steel fitting holding the two leaves of a cavity wall together as one unit and holding the insulation; typically at 900 mm horizontally and 450 mm vertically.', 'Cavity walls (3.3).'),
    ('radon barrier', 'Radon barrier', ['cons-3-4', 'cons-4-2'], ['foundations-floors-walls'],
     'a complete, sealed flexible membrane under the whole floor and the external walls stopping radon gas entering; installed by specialists, not damaged, and sealed round service pipes.', 'Membranes (3.4) under ground floors (4.2).'),
]
Q8 = add('8', 'terms', '', 'Explain with the aid of notes and neat freehand sketches, any five of the following: ' + '; '.join(t[0] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Details and definitions', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{t[1]}: {t[4]}' for t in TERMS),
               group=dict(claimMax=5, perOption=10, options=[t[1] for t in TERMS]))],
         list(dict.fromkeys(n for t in TERMS for n in t[2])), list(dict.fromkeys(a for t in TERMS for a in t[3])), 'q8-terms',
         'The union of the nine printed terms: ' + ' '.join(t[5] for t in TERMS), B8, S8)

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p24 (printed 21): (a) feature 5, sketch quality 6 and details 4 = 15; (b) joint details 5, sketch quality 6 and details 4 = 15; (c) finish 5, two details × 6 and quality of sketches 3 (3/2/1) = 20. Complete 50.'
S9 = 'The design feature, joint and finish are open responses; the scheme gives typical examples.'
A9 = add('9', 'a', '(a)', 'Discuss, with the aid of notes and neat freehand sketches, one design feature that makes the seat suitable for outdoor use.',
         [row('feature', 'Valid design feature', 5, 'Such as: narrow, spaced slats so water drains off; a curved top rail that sheds water; narrow planks that resist splitting and warping; spacing that eases maintenance.'),
          row('presentation', 'Quality of sketch (excellent, good, fair)', 6, 'Quality of the sketch, excellent, good or fair, up to 6.'),
          row('details', 'Valid details', 4, 'Valid details on the sketch, as in the scheme’s model sketches.')],
         ['cons-10-7'], ['wood-rot-ventilation'], 'q9-feature', 'Timber for outdoor use (10.7).', B9, S9)
B9b = add('9', 'b', '(b)', 'Show using notes and neat freehand sketches, a suitable method of jointing the arm rest to the back leg and discuss why the method of jointing shown is suitable.',
          [row('joint', 'Valid details', 5, 'Such as: a mortise and tenon, or a double tenon for strength, wedged, with a high glue area and waterproof glue — suitable outdoors.'),
           row('presentation', 'Quality of sketch (excellent, good, fair)', 6, 'Quality of the sketch of the joint, excellent, good or fair, up to 6.'),
           row('details', 'Valid details', 4, 'Valid details on the sketch, as in the scheme’s model sketches.')],
          ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'], 'q9-joint', 'Joints (10.1) and the choice of joint (10.4).', B9, S9)
C9 = add('9', 'c', '(c)', 'Recommend a suitable applied finish for the garden seat. Describe using notes and freehand sketches, the steps to be followed when preparing the surface of the wood and applying the recommended finish to the garden seat.',
         [row('finish', 'Recommended finish', 5, 'Such as: paint; varnish; stain; Danish oil; any suitable waterproof finish.'),
          row('detail-1', 'Valid detail 1', 6, 'Such as: the surface cleaned, sanded with medium to fine glasspaper, cleaned with white spirit and lightly sanded again.'),
          row('detail-2', 'Valid detail 2', 6, 'A step matching the finish. Such as: primer, undercoat and two coats of gloss with sanding between; or two coats of varnish or stain with a light sanding; or Danish oil in coats with a lint-free cloth.'),
          row('presentation', 'Quality of sketches (excellent, good, fair)', 3, 'Quality of the sketches: excellent 3, good 2, fair 1.', BAND3)],
         ['cons-10-7'], ['wood-rot-ventilation'], 'q9-finish', 'Surface preparation and finishing of timber (10.7).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-joint', B9, S9, parts(A9, B9b, C9))

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and three other questions (200 marks); all question banks retained, no full-exam Cartesian cards.'),
          (3, 'one of', 'Q7(b) "connect one of these appliances": the toilet or the washing machine, one task marked alike for either (choice is not a route).'),
          (3, 'any five', 'Q8 closed choose-five of nine printed terms: one card with an any-five group over all nine terms (choice is not a route).')]
FINITE = {'8': dict(choose=5, options=[t[1] for t in TERMS], cardId=Q8['id'], groupRowId='terms', wholeQuestionMarks=50, termMarks=10)}
GAPS = [dict(cardId=A4['id'], canonicalTopicIds=['cons-10-2'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers fitments (10.2); the card keeps the Wood, Rot & Ventilation association.'),
        dict(cardId=A5['id'], canonicalTopicIds=['cons-4-4'], atlasTopicId=D.CROSS + 'foundations-floors-walls',
             reason='No Ordinary outgoing reference heading covers stairs (4.4); the card keeps the Foundations, Floors & Walls association.'),
        dict(cardId=A5['id'], canonicalTopicIds=['cons-10-1'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers joinery (10.1); the card keeps the Wood, Rot & Ventilation association.'),
        dict(cardId=B5b['id'], canonicalTopicIds=['cons-4-4'], atlasTopicId=D.CROSS + 'foundations-floors-walls',
             reason='No Ordinary outgoing reference heading covers stairs (4.4); the card keeps the Foundations, Floors & Walls association.'),
        dict(cardId=B5b['id'], canonicalTopicIds=['cons-10-1'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers joinery (10.1); the card keeps the Wood, Rot & Ventilation association.'),
        dict(cardId=B9b['id'], canonicalTopicIds=['cons-10-1', 'cons-10-4'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers joinery (10.1, 10.4); the card keeps the Wood, Rot & Ventilation association.')]
D.finish(LEDGER, FINITE, {}, taxonomy_gaps=GAPS, marked_alike={'7b': dict(options=['toilet', 'washing machine'], cardId=B7b['id'])}, whole_choices={'q8-terms'})
