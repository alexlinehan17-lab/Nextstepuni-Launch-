"""Draft the 2022 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 17-25). Q8 "any five of nine" is ONE card (choice is not a route): it keeps the pre-audit
strip-foundation ID and the other eight per-term IDs alias to it. The other 19 pre-audit 2022
Ordinary cards keep their IDs and concept IDs and are corrected in place. Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='External wall, lintels and front door section', concept='door-head-section',
              stem='The sketch shows the front door of a dwelling house. The external wall is a 400 mm concrete block wall with a full-fill insulated cavity. The wall is plastered on both sides. The doorframe, which is fixed in the wall is 150 mm × 80 mm. The highly insulated wooden door is 90 mm in thickness with 15 mm vertical sheeting on both sides.',
              note='Original sketch and specification retained. Construction details, dimensions and draughting belong to part (a); the cavity-closer detail in (b) is marked separately. Any alternative detailing that complies with current Building Regulations is acceptable.'),
    '2': dict(page=2, title='Insulating an attic, tank and pipework', concept='attic-insulation',
              stem='The sketch shows the uninsulated attic space of a dwelling house. The homeowners wish to add insulation to the roof at ceiling joist level and around water storage tank. The ceiling joists are 200 mm × 40 mm.',
              note='Original sketch retained. The insulation method and type are open choices; the scheme lists typical examples. Both the tank and the pipework in (b) are required.'),
    '3': dict(page=2, title='Rainwater harvesting for flushing toilets', concept='rainwater-harvesting',
              stem='Rainwater can be collected from the roof, stored and reused in a dwelling house.',
              note='Original sketch retained. The scheme diagrams are one acceptable layout; the best-six list in (b) is a marking menu.'),
    '4': dict(page=3, title='Timber stud partition between kitchen and living room', concept='stud-partition',
              stem='The sketch shows an open-plan kitchen and living room. The homeowner has decided to construct a timber stud partition with a door to separate these areas.',
              note='Original sketch retained. All five printed items in (a) are required in one sketch, not a choice.'),
    '5': dict(page=3, title='Closed-string stairs section', concept='stairs-section',
              stem='The sketch shows a portion of a closed-string wooden stairs in a dwelling house. The rise of each step is 170 mm.',
              note='Original sketch retained. Construction details, dimensions and draughting belong to part (a); the anti-creak detail in (b) is marked separately.'),
    '6': dict(page=3, title='Jackhammer safety and PPE', concept='jackhammer-safety',
              stem='The sketch shows a construction worker using a jackhammer on a public footpath.',
              note='Original sketch retained. PPE items, risks and precautions are open responses; the scheme lists typical examples.'),
    '7': dict(page=4, title='Designing a family garden', concept='family-garden',
              stem='The draft design for a rear garden of a semi-detached house is shown. The homeowners wish to create a garden space to meet their family needs. The position of existing trees is shown.',
              note='Original plan retained. All four printed items in (b) are required in one sketch; locations and reasons are open, well-reasoned responses.'),
    '8': dict(page=4, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=4, title='A timber-clad front porch', concept='front-porch',
              stem='The sketch shows a detached rural house with a front porch. The porch is of timber frame construction with an external wooden cladding.',
              note='Original sketch retained. The wood, modifications and reasons are open responses; the scheme lists typical examples.'),
}
SCHEME_PAGES = {'1': [4, 17], '2': [5, 18], '3': [6, 19], '4': [7, 20], '5': [8, 21], '6': [9, 10, 22], '7': [11, 12, 23], '8': [13, 14, 15, 24], '9': [16, 25]}
D = cp.Draft(HERE, 2022, 'ordinary', ('69e29520c0fbe774c560c2cd91363cc5cf125b168ec3266f5ea31021f4617b0d',
                                      '196311e890e14bc99d31a4de3318fd97ec5a2850908c00379a6d2ec108282e3b'), 28, QUESTIONS, SCHEME_PAGES)
row, add, compose, parts = D.row, D.add, D.compose, D.parts
BAND8, BAND6 = [0, 4, 6, 8], [0, 2, 4, 6]
D.figures({
    'q1-original': D.paper(2, [45, 39, 580, 284]), 'q2-original': D.paper(2, [45, 284, 580, 530]),
    'q3-original': D.paper(2, [45, 530, 580, 768]), 'q4-original': D.paper(3, [45, 39, 580, 325]),
    'q5-original': D.paper(3, [45, 325, 580, 522]), 'q6-original': D.paper(3, [45, 522, 580, 770]),
    'q7-original': D.paper(4, [45, 52, 580, 394]), 'q8-original': D.paper(4, [45, 394, 580, 494]),
    'q9-original': D.paper(4, [45, 530, 580, 765]),
    'q1-scheme': D.scheme(4, [25, 58, 580, 790]),
    'q2-method': D.scheme(5, [25, 58, 580, 365]), 'q2-tank': D.scheme(5, [25, 365, 580, 655]), 'q2-advantages': D.scheme(5, [25, 655, 580, 790]),
    'q3-collection': D.scheme(6, [25, 58, 580, 384]), 'q3-supply': D.scheme(6, [25, 384, 580, 714]), 'q3-advantage': D.scheme(6, [51, 698, 410, 790]),
    'q4-partition': D.scheme(7, [25, 58, 580, 520]), 'q4-pros-cons': D.scheme(7, [25, 520, 580, 650]), 'q4-reasons': D.scheme(7, [25, 650, 580, 790]),
    'q5-scheme': D.scheme(8, [25, 58, 580, 790]),
    'q6-signs': D.scheme(9, [25, 58, 580, 625]), 'q6-risks': D.scheme(9, [25, 625, 580, 775]), 'q6-public': D.scheme(10, [25, 51, 580, 770]),
    'q7-reasons': D.scheme(11, [25, 58, 580, 255]),
    'q7-layout': D.composite((11, [25, 255, 580, 790]), (12, [25, 51, 580, 580])),
    'q7-advantages': D.scheme(12, [25, 585, 580, 745]),
    'q8-terms': D.composite((13, [25, 51, 580, 790]), (14, [25, 51, 580, 690]), (15, [25, 51, 580, 780])),
    'q9-wood': D.scheme(16, [25, 51, 580, 320]), 'q9-light': D.scheme(16, [25, 325, 580, 590]), 'q9-porch': D.scheme(16, [25, 590, 580, 775]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p17 (printed 15): (a) best 7 of 10 listed details × 5 = 35, four typical dimensions 4, draughting/accuracy/scale 8 (8/6/4), all printed within part (a): 47; (b) cavity closer 3. Complete 50.'
S1 = 'One required section and one required cavity-closer detail. The best-seven detail list is a marking menu, not a printed choose-seven task.'
A1 = add('1', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the external wall, concrete lintels, doorframe and door. On your drawing show the typical construction details from 400 mm below to a level 400 mm above the concrete lintels. Include four typical dimensions.',
         [row('details', 'Any 7 x 5 marks', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: concrete block inner leaf with 15 mm internal plaster; 200 mm full-fill cavity insulation; concrete block outer leaf with 19 mm render; wall ties; concrete lintels; stepped DPC; airtight tape; cavity closer; thermally broken door frame (150 × 80 mm); insulated external door (90 mm).', list(range(0, 36, 5))),
          row('dimensions', 'Any 4 typical dimensions', 4, 'Four appropriate typical dimensions on the section.'),
          row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the section: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-3-7', 'cons-3-4', 'cons-3-3'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls'], 'q1-scheme',
         'Scaled drawing (1.5) of an external door (3.7) with its lintels and stepped DPC (3.4) in a cavity wall (3.3).', B1, S1)
B1b = add('1', 'b', '(b)', 'On your drawing, show the typical design detailing to ensure that the cavity is closed at the door head.',
          [row('closer', 'Cavity closer', 3, 'Show and identify the cavity closer at the door head, as in the scheme’s model section. Any alternative detail that complies with current Building Regulations is accepted.', [0, 3])],
          ['cons-3-3', 'cons-6-2'], ['foundations-floors-walls', 'heat-loss-insulation'], 'q1-scheme', 'Closing the cavity wall (3.3) against a thermal bridge (6.2).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-scheme', B1, S1, D.parts(('a', A1['questionText']), ('b', B1b['questionText'])))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p18 (printed 16): (a) method note & sketch 7 + 7 = 14, insulation type 4, thickness 4 = 22; (b) water tank and pipework, each note & sketch 5 + 4 = 18; (c) two advantages × 5 = 10. Complete 50.'
S2 = '"one suitable method" is an open choice with no printed list; both the tank and the pipework in (b) are required.'
A2 = add('2', 'a', '(a)', 'Using notes and freehand sketches, show one suitable method of insulating the roof at ceiling joist level. Specify the type and thickness of insulation.',
         [row('method', 'Method of insulating attic note & sketch (7 + 7 marks)', 14, 'Note 7 and sketch 7. Such as: insulation roll cut to the width between the ceiling joists and packed tightly above the plasterboard, with further layers laid crosswise on top.'),
          row('type', 'Preferred insulation type for attic', 4, 'Such as: fibreglass, blown-in cellulose, spray foam or hemp insulation.'),
          row('thickness', 'Thickness of insulation', 4, 'At least 300 mm of insulation.')],
         ['cons-3-9', 'cons-6-2'], ['roofs', 'heat-loss-insulation'], 'q2-method', 'Roof insulation at ceiling level (3.9) with insulating materials (6.2).', B2, S2)
B2b = add('2', 'b', '(b)', 'The water storage tank and pipework in the attic are also to be insulated. On a separate sketch show, using notes and freehand sketches, how the water tank and pipework could be insulated.',
          [row('tank', 'Method to insulating water tank note & sketch (5 + 4 marks)', 9, 'Note 5 and sketch 4. Such as: no attic insulation under the tank, so heat rises and stops it freezing; insulation cut to size around the sides and top of the tank.'),
           row('pipework', 'Method of insulating pipework note & sketch (5 + 4 marks)', 9, 'Note 5 and sketch 4. Such as: polyethylene foam tubes around all attic pipework, joined with duct tape; or reflective pipe lagging.')],
          ['cons-5-2', 'cons-6-2'], ['hot-water-space-heating', 'heat-loss-insulation'], 'q2-tank', 'Cold water storage (5.2) protected with insulation (6.2).', B2, S2)
C2 = add('2', 'c', '(c)', 'Discuss two advantages of highly insulating the attic space of a house.',
         [row('advantage-1', 'Advantage 1', 5, 'Such as: reduced heat loss; reduced energy bills.'),
          row('advantage-2', 'Advantage 2', 5, 'A second, different advantage. Such as: more thermal comfort; a better BER; better for the environment.')],
         ['cons-6-2', 'cons-6-3'], ['heat-loss-insulation'], 'q2-advantages', 'Insulation (6.2) and running costs (6.3).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-method', B2, S2, D.parts(('a', A2['questionText']), ('b', B2b['questionText']), ('c', C2['questionText'])))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p19 (printed 17): (a) sketch 4 and three pipework items × 4 = 16; (b) best 6 of 9 listed items × 4 = 24 and sketch 4 = 28; (c) one advantage 6. Complete 50.'
S3 = 'The printed requirements in (b) (all necessary pumps and valves) are required content; the best-six list is a marking menu, not a printed choice.'
A3 = add('3', 'a', '(a)', 'Draw a large freehand sketch of the given house and underground storage tank. On your sketch show the pipework necessary to collect the rainwater from the roof and carry it to the underground tank.',
         [row('sketch', 'Sketch', 4, 'A large freehand sketch of the house and underground tank.'),
          row('collection', 'Pipework to collect water from roof', 4, 'Such as: a 125 mm eaves gutter and 65 mm downpipe.'),
          row('to-tank', 'Pipework from roof to storage tank', 4, 'Such as: a 100 mm underground pipe to the storage tank.'),
          row('filters', 'Filters and overflow pipe', 4, 'Such as: a debris filter and an overflow pipe from the underground tank.')],
         ['cons-5-4'], ['drainage'], 'q3-collection', 'Surface water, gutters and rainwater pipes (5.4).', B3, S3)
B3b = add('3', 'b', '(b)', 'The stored rainwater is used for flushing toilets. On the sketch, show the pipework necessary to take rainwater from the underground tank to the storage tank in the attic. Show the pipework necessary to connect the toilet cistern to the storage tank in the attic. Include all necessary pumps and valves.',
          [row('items', 'Any 6 x 4 marks', 24, 'Credit the best SIX acceptable items at 4 marks each, capped at 24. Marked items: pumps; pipework from the underground tank to the attic tank; filters; attic storage tank; ball valve; 28 mm overflow; pipework from the attic tank to the cistern; toilet cistern; valves. Typical details: a submersible pump, 12 mm pipe to an in-line filter, a 230 litre attic tank, 12 mm feed to the cistern.', list(range(0, 25, 4))),
           row('sketch', 'Sketch', 4, 'The supply pipework drawn on the sketch.')],
          ['cons-5-2', 'cons-5-6'], ['hot-water-space-heating', 'drainage'], 'q3-supply', 'Cold water storage and supply (5.2) to a sanitary fitment (5.6).', B3, S3)
C3 = add('3', 'c', '(c)', 'Discuss one advantage of reusing rainwater in a dwelling house.',
         [row('advantage', 'Advantage', 6, 'Such as: sustainable living; less flooding around the property; lower water treatment costs from reduced use.')],
         ['cons-5-4', 'cons-1-2'], ['drainage', 'planning-sustainability-environment'], 'q3-advantage', 'Rainwater (5.4) reused in a sustainable built environment (1.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-supply', B3, S3, D.parts(('a', A3['questionText']), ('b', B3b['questionText']), ('c', C3['questionText'])))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p20 (printed 18): (a) five items × 4 = 20, note 4, quality of sketch 6 (6/4/2) = 30; (b) advantage 5 + disadvantage 5 = 10; (c) two reasons × 5 = 10. Complete 50.'
S4 = 'All five printed items in (a) are required in one sketch, not a choice.'
A4 = add('4', 'a', '(a)', 'Using notes and a freehand sketch, show the typical construction details of the stud partition required to separate the rooms. Include the following in your sketch: headplate; soleplate; timber studs; noggins; door lintel.',
         [row('items', 'Typical construction details of the stud partition', 20, 'All five printed items, 4 each: headplate; soleplate; timber studs; noggins; door lintel. The scheme specifies 100 × 45 mm sole plate, head plate, studs, noggins, door head and jambs.'),
          row('note', 'Note', 4, 'Notes on the construction, such as noggins between the studs for rigidity and jambs supporting the door head.'),
          row('presentation', 'Quality of sketch (excellent, good, fair)', 6, 'Quality of the sketch: excellent 6, good 4, fair 2.', BAND6)],
         ['cons-4-5'], ['windows-doors'], 'q4-partition', 'Stud partitions and internal doors (4.5).', B4, S4)
B4b = add('4', 'b', '(b)', 'Discuss one advantage and one disadvantage of using a timber stud partition to create separate rooms.',
          [row('advantage', 'Advantage', 5, 'Such as: quick to install; cheaper than a block partition; services easily run in the wall; an environmentally friendly material.'),
           row('disadvantage', 'Disadvantage', 5, 'Such as: sound travels through easily; shrinkage and swelling; heavy items hard to fix; easily damaged.')],
          ['cons-4-5', 'cons-8-3'], ['windows-doors', 'sound'], 'q4-pros-cons', 'Stud partitions (4.5) and sound insulation (8.3).', B4, S4)
C4 = add('4', 'c', '(c)', 'Discuss two reasons for creating a living room which is separate from the kitchen.',
         [row('reason-1', 'Reason 1', 5, 'Such as: less noise in the living room; privacy for the occupants of each room.'),
          row('reason-2', 'Reason 2', 5, 'A second, different reason. Such as: cooking odours kept from the living room; less echo in a smaller space; separate spaces to eat and to relax.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q4-reasons', 'Layout design within the built environment (1.2).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-partition', B4, S4, D.parts(('a', A4['questionText']), ('b', B4b['questionText']), ('c', C4['questionText'])))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p21 (printed 19): (a) best 7 of 9 listed details × 5 = 35, three typical dimensions 3, draughting/accuracy/scale 8 (8/6/4) = 46; (b) one anti-creak detail 4. Complete 50.'
S5 = 'One required section and one required detail. The best-seven detail list is a marking menu, not a printed choice.'
A5 = add('5', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the centre of the bottom three steps of the stairs. Show the string, treads and risers. Include three typical dimensions on your drawing.',
         [row('details', 'Any 7 x 5 marks', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: string 250 × 50 mm; tread 250 × 25 mm; riser 170 × 20 mm; joint between tread and riser; nosing (16 mm minimum); vertical wedge; horizontal wedge; glue blocks 60 × 60 mm; pitch line (maximum 42°).', list(range(0, 36, 5))),
          row('dimensions', 'Any three typical dimensions 3 x 1 mark', 3, 'Three appropriate typical dimensions on the section, 1 each.'),
          row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the section: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-4-4'], ['question-one-drawing-questions', 'foundations-floors-walls'], 'q5-scheme',
         'Scaled drawing (1.5) of a stairs (4.4).', B5, S5)
B5b = add('5', 'b', '(b)', 'On your drawing, show one design detail to prevent creaking when the stairs is in use.',
          [row('creaking', 'Block joint / Use of horizontal and vertical wedges / Tightly fitted connection between riser and tread.', 4, 'One design detail shown and identified: a block joint, horizontal and vertical wedges, or a tightly fitted connection between riser and tread. Any other suitable detail is accepted.', [0, 4])],
          ['cons-4-4', 'cons-10-1'], ['foundations-floors-walls', 'wood-rot-ventilation'], 'q5-scheme', 'Stairs (4.4) and their joints (10.1).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-scheme', B5, S5, D.parts(('a', A5['questionText']), ('b', B5b['questionText'])))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p22 (printed 20): (a) three signs × (sign 6 + specific reason 3) = 27; (b) two risks × 5 = 10; (c) precaution note & sketch 7 + 6 = 13. Complete 50.'
S6 = 'Signs, risks and precautions are open responses with no printed list; the scheme lists typical examples.'
A6 = add('6', 'a', '(a)', 'Using a large freehand sketch, show three safety signs highlighting the use of personal protective equipment (PPE) that must be worn by workers while using a jackhammer. For each sign, state how the personal protective equipment protects workers while using the jackhammer.',
         [row('sign-1', 'Sign 1 and specific reason. (6 + 3 marks)', 9, 'Sign 6 and specific reason 3. Such as: ear protectors, protecting hearing from the jackhammer’s high decibel levels.'),
          row('sign-2', 'Sign 2 and specific reason (6 + 3 marks)', 9, 'A second, different sign: 6 + 3. Such as: safety boots, protecting feet from dropped or falling materials; safety glasses, protecting eyes from flying debris and dust.'),
          row('sign-3', 'Sign 3 and specific reason (6 + 3 marks)', 9, 'A third, different sign: 6 + 3. Such as: a dust mask, protecting the lungs from dust; safety gloves, protecting hands when moving broken debris.')],
         ['cons-1-8'], ['site-safety'], 'q6-signs', 'Personal protective equipment (1.8).', B6, S6)
B6b = add('6', 'b', '(b)', 'Describe two potential risks to a construction worker when using power tools on a construction site.',
          [row('risk-1', 'Risk 1', 5, 'Such as: hearing damage from excessive noise; electrical injury from exposed live cables.'),
           row('risk-2', 'Risk 2', 5, 'A second, different risk. Such as: dust and fumes without the correct PPE; hand-arm vibration syndrome from hammer-action tools; striking underground services.')],
          ['cons-1-8', 'cons-9-4'], ['site-safety'], 'q6-risks', 'Safety on site (1.8) with power tools (9.4).', B6, S6)
C6 = add('6', 'c', '(c)', 'Using notes and a freehand sketch, describe one safety precaution that will reduce the risk to the public while the footpath is being replaced.',
         [row('precaution', 'Safety precaution note & sketch (7 + 6 marks)', 13, 'Note 7 and sketch 6. Such as: signage directing the public away from the work zone; guard rails and exclusion zones; materials stored away from public areas; a dust shelter around the work area.')],
         ['cons-1-8'], ['site-safety'], 'q6-public', 'Safety precautions on site (1.8).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-signs', B6, S6, D.parts(('a', A6['questionText']), ('b', B6b['questionText']), ('c', C6['questionText'])))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p23 (printed 21): (a) two reasons × 5 = 10; (b) sketch 6 and four items, each location 3 + reason 3 = 6, = 30; (c) two advantages × 5 = 10. Complete 50.'
S7 = 'All four printed items in (b) are required in one sketch, not a choice.'
A7 = add('7', 'a', '(a)', 'Discuss two reasons why it is important to create a garden space that meet the needs of the family.',
         [row('reason-1', 'Reason 1', 5, 'Such as: a safe area to socialise and entertain; a private area to enjoy the outdoors.'),
          row('reason-2', 'Reason 2', 5, 'A second, different reason. Such as: outdoor living for all age groups; an extension of the home; space to grow herbs and vegetables; extra storage.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q7-reasons', 'Layout design of the built environment (1.2).', B7, S7)
B7b = add('7', 'b', '(b)', 'Draw a large freehand sketch of the given design and show your preferred location for each of the following in the garden area: outdoor dining/living space; garden storage; flower beds; lawn area. Give one reason for selecting each location.',
          [row('sketch', 'Sketch', 6, 'A large freehand sketch of the given garden design.'),
           row('outdoor', 'Location and valid reason for outdoor space (3 + 3 marks)', 6, 'Location 3 and reason 3. Such as: close to the house for indoor-outdoor living, or placed to catch south-facing sun.'),
           row('storage', 'Location and valid reason for garden storage (3 + 3 marks)', 6, 'Location 3 and reason 3. Such as: near the entrance gate for supplies, or at the back or side fence to keep the garden open and unshaded.'),
           row('flower-beds', 'Location and valid reason for flower beds (3 + 3 marks)', 6, 'Location 3 and reason 3. Such as: in sight of the house, in the sun, or along a boundary fence.'),
           row('lawn', 'Location and valid reason for lawn area (3 + 3 marks)', 6, 'Location 3 and reason 3. Such as: in the occupants’ line of vision, close to the house, or at the rear to keep dirt out of the house.')],
          ['cons-1-2'], ['planning-sustainability-environment'], 'q7-layout', 'Layout design of the built environment (1.2).', B7, S7)
C7 = add('7', 'c', '(c)', 'Discuss two advantages of incorporating trees and plants into a garden design.',
         [row('advantage-1', 'Advantage 1', 5, 'Such as: wellbeing; better air quality; pollinators attracted to the garden.'),
          row('advantage-2', 'Advantage 2', 5, 'A second, different advantage. Such as: a better appearance; natural shade and shelter for the house; less flooding from run-off.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q7-advantages', 'The sustainable built environment (1.2).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-layout', B7, S7, D.parts(('a', A7['questionText']), ('b', B7b['questionText']), ('c', C7['questionText'])))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p24 (printed 22): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination. It keeps the pre-audit strip-foundation ID; the other eight per-term IDs alias to it.'
TERMS = [
    ('strip-foundation', 'strip foundation', 'Strip foundation', ['cons-2-4'], ['foundations-floors-walls'],
     'a simple, common foundation for homes; concrete reinforced with steel for tensile strength; the wall placed centrally with loads spread at 45° to the ground; used where the soil has a good bearing capacity.', 'Strip foundations (2.4).'),
    ('fascia-board', 'fascia board', 'Fascia board', ['cons-3-10'], ['roofs'],
     'gives a finished appearance and protects the house from the weather; part of the eaves with the soffit; carries the gutters; usually wood, PVC or aluminium.', 'Eaves (3.10).'),
    ('airtight-tape', 'airtight tape', 'Airtight tape', ['cons-6-5'], ['air-tightness-condensation'],
     'a highly adhesive tape used with an airtight membrane at every junction of building elements and around door and window frames, preventing draughts and heat loss.', 'Airtightness (6.5).'),
    ('wind-turbine', 'wind turbine', 'Wind turbine', ['cons-5-8', 'cons-1-2'], ['services-water-gas-electrical', 'planning-sustainability-environment'],
     'converts wind energy into mechanical energy that generates electricity; sustainable, reducing reliance on fossil fuels; commercial wind farms or smaller domestic turbines; horizontal- or vertical-axis.', 'Domestic electricity (5.8) from a renewable source in the built environment (1.2).'),
    ('septic-tank', 'septic tank', 'Septic tank', ['cons-5-5'], ['drainage'],
     'an underground chamber that collects, stores and treats domestic wastewater; anaerobic bacteria break down solids, which settle as sludge; treated water returns to the ground through the percolation area.', 'Septic tanks (5.5).'),
    ('dovetail-joint', 'dovetail joint', 'Dovetail joint', ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'],
     'a common joint in drawer and box construction and quality furniture; the slope of the tail (1:8 hardwood, 1:6 softwood) gives its tensile strength; cut by hand or with a router jig.',
     'Joints (10.1) and the choice of joint (10.4). The Ordinary reference taxonomy has no joinery heading; the term keeps the Wood, Rot & Ventilation association used for joinery, and 10.1/10.4 are declared outside that heading’s crosswalk.'),
    ('wall-tie', 'wall tie', 'Wall tie', ['cons-3-3'], ['foundations-floors-walls'],
     'ties the two leaves of a cavity wall into one stable unit, embedded in the mortar; stainless steel or basalt fibre (less thermal bridging); lengths to suit the cavity.', 'Cavity walls (3.3).'),
    ('cordless-jigsaw', 'cordless jigsaw', 'Cordless jigsaw', ['cons-9-2'], ['wood-rot-ventilation'],
     'cuts shapes and curves with a reciprocating blade; battery powered, portable and safer without a lead; the base rests on the work and is pushed along; used on a range of materials.',
     'Power tools (9.2). The Ordinary reference taxonomy has no tools heading; the term keeps the Wood, Rot & Ventilation association used for tools and craft, and 9.2 is declared outside that heading’s crosswalk.'),
    ('underfloor-heating', 'underfloor heating', 'Underfloor heating', ['cons-5-3'], ['hot-water-space-heating'],
     'polyethylene pipes beneath the floor carry water heated by a heat pump; the floor becomes a large heat source with no cold spots and a constant temperature, replacing radiators; efficient at low temperatures.', 'Heating systems (5.3).'),
]
Q8 = add('8', 'None-strip-foundation', '', 'Explain, with the aid of notes and freehand sketches, any five of the following: ' + '; '.join(t[1] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Construction Terms', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{t[2]}: {t[5]}' for t in TERMS),
               group=dict(claimMax=5, perOption=10, options=[t[2] for t in TERMS]))],
         list(dict.fromkeys(n for t in TERMS for n in t[3])), list(dict.fromkeys(a for t in TERMS for a in t[4])), 'q8-terms',
         'The union of the nine printed terms: ' + ' '.join(t[6] for t in TERMS), B8, S8)

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p25 (printed 23): (a) suitable wood 4, two reasons × 4 = 12; (b) two modifications, each notes + sketch 8 + 5 = 13, = 26; (c) two reasons × 6 = 12. Complete 50.'
S9 = 'The wood, modifications and reasons are open responses with no printed list; the scheme lists typical examples.'
A9 = add('9', 'a', '(a)', 'Specify a suitable wood for the external cladding, and give two reasons for your choice.',
         [row('wood', 'Suitable wood', 4, 'Such as: cedar, larch, Douglas fir, oak or teak.'),
          row('reason-1', 'Reason 1', 4, 'A reason matching the wood. Such as: a durable species; no preservative needed because of its natural oils.'),
          row('reason-2', 'Reason 2', 4, 'A second, different reason. Such as: naturally resistant to insect attack or to moisture.')],
         ['cons-3-2', 'cons-10-3'], ['foundations-floors-walls', 'wood-rot-ventilation'], 'q9-wood', 'External cladding (3.2) in a durable timber (10.3).', B9, S9)
B9b = add('9', 'b', '(b)', 'The owner wishes to modify the porch to allow more natural light into the house. Using notes and freehand sketches, show two modification to the porch that would allow more natural light to enter the house.',
          [row('modification-1', 'Modification 1 to porch notes + sketch (8 + 5 marks )', 13, 'Notes and sketch, 8 + 5. Such as: roof lights; a window in the entrance door.'),
           row('modification-2', 'Modification 2 to porch notes + sketch (8 + 5 marks )', 13, 'Notes and sketch, 8 + 5, for a second, different modification. Such as: windows in the external walls; a glass roof.')],
          ['cons-3-5'], ['windows-doors'], 'q9-light', 'Windows (3.5) letting more daylight into the house.', B9, S9)
C9 = add('9', 'c', '(c)', 'Discuss two reasons why homeowners would wish to build a front porch to their house.',
         [row('reason-1', 'Advantage 1', 6, 'Such as: more usable space; an extra draught barrier.'),
          row('reason-2', 'Advantage 2', 6, 'A second, different reason. Such as: blending in with neighbouring houses; extra security; better insulation of the house; a higher resale value.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q9-porch', 'Extending a dwelling in the built environment (1.2).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-light', B9, S9, D.parts(('a', A9['questionText']), ('b', B9b['questionText']), ('c', C9['questionText'])))

LEDGER = [(1, 'Answer any', 'Whole-exam selection: any three of the nine questions (150 marks); all question banks retained, no full-exam Cartesian cards.'),
          (4, 'any five', 'Q8 closed choose-five of nine printed terms: one card with an any-five group over all nine terms (choice is not a route).')]
FINITE = {'8': dict(choose=5, options=[t[0] for t in TERMS], cardId=Q8['id'], groupRowId='terms', wholeQuestionMarks=50, termMarks=10)}
REASONS = {
    'q1-a': 'Adds the four typical dimensions (4) and draughting/accuracy/scale (8/6/4) printed within part (a): 35 → 47.',
    'q1-b': 'Reshaped to the printed all-or-nothing row "Cavity closer" (0 or 3); tariff unchanged.',
    'q2-b': 'Split into the printed tank and pipework rows (note & sketch 5 + 4 each); tariff unchanged (18).',
    'q2-c': 'Split into the two printed advantages (5 each); tariff unchanged (10).',
    'q3-a': 'Reshaped to the printed sketch and three pipework rows (4 each); tariff unchanged (16).',
    'q3-b': 'Adds the printed sketch (4) to the best-six items (6 × 4): 24 → 28.',
    'q3-c': 'Reshaped to the printed advantage row; tariff unchanged (6).',
    'q4-a': 'Adds the printed note (4) and quality-of-sketch band (6/4/2) to the five items (4 each): 24 → 30.',
    'q4-c': 'Split into the two printed reasons (5 each); tariff unchanged (10).',
    'q5-a': 'Adds the three typical dimensions (3) and draughting/accuracy/scale (8/6/4) printed within part (a): 35 → 46.',
    'q6-a': 'Split into the three printed signs (sign 6 + specific reason 3 each); tariff unchanged (27).',
    'q6-b': 'Split into the two printed risks (5 each); tariff unchanged (10).',
    'q6-c': 'Reshaped to the printed note & sketch row (7 + 6); tariff unchanged (13).',
    'q7-a': 'Split into the two printed reasons (5 each); tariff unchanged (10).',
    'q7-b': 'Rebuilt to the printed rows — sketch 6 and four location-and-reason rows (3 + 3 each); tariff unchanged (30).',
    'q7-c': 'Split into the two printed advantages (5 each); tariff unchanged (10).',
    'q9-a': 'Split into the printed wood (4) and two reasons (4 each); tariff unchanged (12).',
    'q9-b': 'Split into the two printed modifications (notes + sketch 8 + 5 each); tariff unchanged (26).',
    'q9-c': 'Split into the two printed reasons (6 each); tariff unchanged (12).',
    'q8-None-strip-foundation': 'Now the whole of Question 8: one card printing all nine terms with an any-five group (10 each, 50), kept under this ID; the other eight per-term IDs alias to it (choice is not a route): 10 → 50.',
}
CONSOLIDATED = {f'q8-None-{t[0]}': 'q8-None-strip-foundation' for t in TERMS[1:]}
GAPS = [dict(cardId=Q8['id'], canonicalTopicIds=['cons-10-1', 'cons-10-4', 'cons-9-2'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers joinery (10.1, 10.4, dovetail joint) or workshop tools (9.2, cordless jigsaw).'),
        dict(cardId=A5['id'], canonicalTopicIds=['cons-4-4'], atlasTopicId=D.CROSS + 'foundations-floors-walls',
             reason='No Ordinary outgoing reference heading covers stairs (4.4); the stairs section keeps the Foundations, Floors & Walls association.'),
        dict(cardId=B5b['id'], canonicalTopicIds=['cons-4-4'], atlasTopicId=D.CROSS + 'foundations-floors-walls',
             reason='No Ordinary outgoing reference heading covers stairs (4.4).'),
        dict(cardId=B5b['id'], canonicalTopicIds=['cons-10-1'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers joinery (10.1, the tread-riser joint); it keeps the Wood, Rot & Ventilation association used for joinery.')]
D.finish(LEDGER, FINITE, REASONS, consolidated=CONSOLIDATED, taxonomy_gaps=GAPS, whole_choices={'q8-None-strip-foundation'})
