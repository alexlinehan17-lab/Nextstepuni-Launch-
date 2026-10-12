"""Draft the 2021 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 15-23). Q8 "any five of nine" is ONE card (choice is not a route): it keeps the pre-audit
joist-bridging ID and the other eight per-term IDs alias to it. The other 17 pre-audit 2021 Ordinary
cards keep their IDs and concept IDs and are corrected in place. Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Cut-roof eaves and external wall section', concept='cut-roof-eaves-section',
              stem='The sketch shows portion of the eaves of a pitched roof. The slated cut roof has a pitch of 30°. The roof is supported on a 400 mm concrete block wall with a full-fill insulated cavity. The slates are fixed to 50 mm × 30 mm battens, on a breather membrane, supported on 200 mm × 50 mm rafters. The ceiling joists are 200 mm × 50 mm with plasterboard fixed beneath. The roof is highly insulated at ceiling joist level.',
              note='Original sketch and specification retained. Construction details, dimensions and draughting belong to part (a); the rainwater detail in (b) is marked separately. Any alternative detailing that complies with current Building Regulations is acceptable.'),
    '2': dict(page=2, title='Insulating a solid ground floor', concept='ground-floor-insulation',
              stem='A young couple wish to have a highly insulated ground floor in their new house. The solid ground floor is to have a 100 mm concrete floor slab, finished with a suitable flooring material.',
              note='Original question retained. The insulation method and type and the floor finish are open choices; the scheme lists typical examples.'),
    '3': dict(page=2, title='Cold water supply from the water main', concept='cold-water-supply',
              stem='The public water supply provides households with clean, treated water for domestic consumption.',
              note='Original question retained. The listed components are required content, not a choice; the best-eight list is a marking menu.'),
    '4': dict(page=3, title='Planning permission for a town house', concept='planning-permission',
              stem='The sketch shows a design for a dwelling house which is to be constructed in a town. The owner intends to apply for planning permission to construct this dwelling house.',
              note='Original sketch retained. Both printed planning documents in (b) are required, each separately marked.'),
    '5': dict(page=3, title='External wall and window cill section', concept='window-cill-section',
              stem='The sketch shows portion of a triple glazed wooden window. The window is fixed in a 400 mm concrete block wall with a full-fill insulated cavity. The wall is rendered on both sides. The fixed frame of the window is 120 mm × 80 mm and is thermally broken.',
              note='Original sketch and specification retained. Construction details, dimensions and draughting belong to part (a); the cill detail in (b) is marked separately.'),
    '6': dict(page=3, title='PPE and deep-trench safety', concept='trench-safety', stem='',
              note='Original question retained. All three printed PPE items in (a) are required, each separately marked; risks and precautions are open responses.'),
    '7': dict(page=4, title='Living room layout with kitchen access', concept='living-room-layout',
              stem='A draft design for a living room layout with an adjacent kitchen in a new dwelling house is shown. The positions of the windows and a door are included.',
              note='Original plan retained. All four printed items in (b) are required in one sketch; locations and reasons are open, well-reasoned responses.'),
    '8': dict(page=4, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=4, title='Outdoor living space on softwood decking', concept='outdoor-decking',
              stem='The sketch shows a space for outdoor living to the rear of a dwelling house. The space has been constructed using softwood decking on wooden joists.',
              note='Original sketch retained. The finish, modifications and advantages are open responses; the scheme lists typical examples.'),
}
SCHEME_PAGES = {'1': [4, 15], '2': [5, 16], '3': [6, 17], '4': [7, 18], '5': [8, 19], '6': [9, 20], '7': [10, 11, 21], '8': [12, 13, 22], '9': [14, 23]}
D = cp.Draft(HERE, 2021, 'ordinary', ('58d741d2e4ac4bbbe000a5d8e056d8908291a8488fd9191010eb170fa96672b0',
                                      '88bb726b606474103cf4c1d04ef58cb78c1d4508f68a5bd766681cf40bc4c258'), 26, QUESTIONS, SCHEME_PAGES)
row, add, compose = D.row, D.add, D.compose
BAND8 = [0, 4, 6, 8]


def parts(*cards):
    return D.parts(*[(letter, c['questionText']) for letter, c in zip('abc', cards)])


D.figures({
    'q1-original': D.paper(2, [45, 39, 580, 297]), 'q2-original': D.paper(2, [45, 297, 580, 517]),
    'q3-original': D.paper(2, [45, 517, 580, 765]), 'q4-original': D.paper(3, [45, 39, 580, 295]),
    'q5-original': D.paper(3, [45, 295, 580, 536]), 'q6-original': D.paper(3, [45, 536, 580, 765]),
    'q7-original': D.paper(4, [45, 39, 580, 377]), 'q8-original': D.paper(4, [45, 377, 580, 475]),
    'q9-original': D.paper(4, [45, 511, 580, 765]),
    'q1-scheme': D.scheme(4, [25, 58, 580, 760]),
    'q2-advantages': D.scheme(5, [25, 58, 580, 222]), 'q2-method': D.scheme(5, [25, 222, 580, 478]), 'q2-floor': D.scheme(5, [25, 478, 580, 792]),
    'q3-system': D.scheme(6, [25, 58, 580, 563]), 'q3-meter': D.scheme(6, [25, 563, 580, 680]),
    'q4-reasons': D.composite((7, [25, 58, 580, 116]), (7, [25, 116, 445, 236])), 'q4-documents': D.scheme(7, [25, 240, 580, 575]), 'q4-town': D.scheme(7, [25, 575, 580, 790]),
    'q5-scheme': D.scheme(8, [25, 58, 580, 645]),
    'q6-signs': D.scheme(9, [25, 58, 580, 386]), 'q6-risks': D.scheme(9, [25, 386, 580, 545]), 'q6-trench': D.scheme(9, [25, 545, 580, 792]),
    'q7-access': D.scheme(10, [25, 58, 580, 265]),
    'q7-layout': D.composite((10, [25, 265, 580, 775]), (11, [25, 51, 580, 395])),
    'q7-stove': D.scheme(11, [25, 420, 580, 550]),
    'q8-terms': D.composite((12, [25, 58, 580, 768]), (13, [25, 51, 580, 792])),
    'q9-finish': D.scheme(14, [25, 58, 580, 345]), 'q9-winter': D.scheme(14, [25, 345, 580, 632]), 'q9-advantages': D.scheme(14, [25, 606, 580, 760]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p15 (printed 13): (a) best 7 of 13 listed details × 5 = 35, three typical dimensions 4, draughting/accuracy/scale 8 (8/6/4), all printed within part (a): 47; (b) eaves gutter/downpipe 3. Complete 50.'
S1 = 'One required section and one required rainwater detail. The best-seven detail list is a marking menu, not a printed choose-seven task.'
A1 = add('1', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the external wall and through the eaves of the pitched roof. On your drawing, show the typical construction details from a level 400 mm below the wallplate, through the wall and eaves. Include the first three courses of slate at eaves. Include three typical dimensions on your drawing.',
         [row('details', 'Any 7 x 5 marks', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: slates on 50 × 30 mm battens; breather membrane; rafters 200 × 50 mm; ceiling joists with insulation between; insulated plasterboard with skim; wallplate 100 × 75 mm; airtight membrane and tape; ventilation; tilting fillet, fascia, soffit and gutter; block inner leaf; 200 mm full-fill cavity with ties and cavity closer; block outer leaf; 13 mm plaster and 19 mm render.', list(range(0, 36, 5))),
          row('dimensions', 'Any three typical dimensions', 4, 'Three appropriate typical dimensions on the section.'),
          row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the section: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-3-8', 'cons-3-10', 'cons-3-9', 'cons-3-3'], ['question-one-drawing-questions', 'roofs', 'foundations-floors-walls'], 'q1-scheme',
         'Scaled drawing (1.5) of a cut roof (3.8) at the eaves (3.10) with its covering and insulation (3.9) on a cavity wall (3.3).', B1, S1)
B1b = add('1', 'b', '(b)', 'On your drawing show how rainwater is removed at the eaves.',
          [row('gutter', 'Eaves gutter/ downpipe', 3, 'Show and identify the eaves gutter and downpipe, as in the scheme’s model section.', [0, 3])],
          ['cons-5-4'], ['drainage'], 'q1-scheme', 'Eaves gutters and rainwater pipes (5.4).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-scheme', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p16 (printed 14): (a) two advantages × 5 = 10; (b) method note & sketch 8 + 8 = 16, insulation type 5, thickness 5 = 26; (c) floor type 6 and two reasons × 4 = 14. Complete 50.'
S2 = '"one suitable method" and the floor finish are open choices with no printed list; each part stays one response.'
A2 = add('2', 'a', '(a)', 'List two advantages of constructing a ground floor with a high level of insulation.',
         [row('advantage-1', 'Advantage 1', 5, 'Such as: better for the environment; more thermal comfort.'),
          row('advantage-2', 'Advantage 2', 5, 'A second, different advantage. Such as: lower energy bills; a warmer house; a better BER.')],
         ['cons-6-2', 'cons-6-3'], ['heat-loss-insulation'], 'q2-advantages', 'Insulation (6.2) and running costs (6.3).', B2, S2)
B2b = add('2', 'b', '(b)', 'Using notes and freehand sketches, show one suitable method of insulating the solid ground floor of the new house. Specify the type and thickness of insulation.',
          [row('method', 'Method of insulating floor note & sketch (8 + 8 marks)', 16, 'Note 8 and sketch 8. Such as: a DPM/radon barrier on sand blinding; perimeter insulation against cold bridging; insulation boards tightly butted on the membrane; the concrete slab poured on top.'),
           row('type', 'Preferred insulation type for the floor', 5, 'Such as: extruded polystyrene, polyurethane or foil-faced PIR boards.'),
           row('thickness', 'Thickness of insulation', 5, 'Such as: 150–300 mm insulation boards.')],
          ['cons-4-2', 'cons-6-2'], ['foundations-floors-walls', 'heat-loss-insulation'], 'q2-method', 'An insulated solid ground floor (4.2, 6.2).', B2, S2)
C2 = add('2', 'c', '(c)', 'The couple must decide on the floor finishes for their house. Recommend a suitable flooring material for the open-plan kitchen, and give two reasons for your selection.',
         [row('floor', 'Suitable floor type', 6, 'Such as: tiles, solid wood, laminate, polished concrete or natural stone.'),
          row('reason-1', 'Reason 1', 4, 'A reason matching the floor. Such as, tiles: easy to clean, hygienic, hard wearing; solid wood: attractive, natural feel.'),
          row('reason-2', 'Reason 2', 4, 'A second, different reason. Such as, laminate: cheap and easy to install; polished concrete: durable and maintenance free; natural stone: local and water resistant.')],
         ['cons-4-2', 'cons-1-2'], ['foundations-floors-walls', 'planning-sustainability-environment'], 'q2-floor', 'A ground-floor finish (4.2) chosen for the room (1.2).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-method', B2, S2, parts(A2, B2b, C2))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p17 (printed 15): (a) best 8 of 12 listed items × 4 = 32 and quality of sketch 8 (8/6/4) = 40; (b) two advantages × 5 = 10. Complete 50.'
S3 = 'The printed component list is required content, not a choice; the best-eight list is a marking menu.'
A3 = add('3', 'a', '(a)', 'Using a single-line labelled sketch, show the pipework required to supply cold water from the water main to the kitchen sink and to the water storage tank. Include the following in your sketch: water main; water meter; rising main; pipework to the kitchen sink; insulated cold water storage tank; all necessary valves.',
         [row('items', 'Any 8 × 4 marks', 32, 'Credit the best EIGHT acceptable items at 4 marks each, capped at 32. Marked items: mains water supply; water meter; 15 mm rising main; kitchen sink; connection to the sink; ball valve; cold water storage tank; insulation around the tank; 28 mm overflow; pipe insulation; valves; annotation.', list(range(0, 33, 4))),
          row('presentation', 'Quality of sketch (excellent, good, fair)', 8, 'Quality of the sketch: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-5-2', 'cons-5-1'], ['hot-water-space-heating', 'services-water-gas-electrical'], 'q3-system', 'Cold water supply (5.2) from the service entry (5.1).', B3, S3)
B3b = add('3', 'b', '(b)', 'Discuss two advantages of installing a water meter.',
          [row('advantage-1', 'Advantage 1', 5, 'Such as: encourages water conservation; lower water treatment costs.'),
           row('advantage-2', 'Advantage 2', 5, 'A second, different advantage. Such as: shows leaks and wastage; a lower water bill.')],
          ['cons-5-1'], ['services-water-gas-electrical'], 'q3-meter', 'Water services (5.1).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-system', B3, S3, parts(A3, B3b))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p18 (printed 16): (a) two reasons × 6 = 12; (b) site notice and site location map, each note & sketch 8 + 5 = 26; (c) one advantage 6 and one disadvantage 6 = 12. Complete 50.'
S4 = 'Both printed planning documents in (b) are required, each separately marked, not a choice.'
PLAN = (['cons-1-3'], ['planning-sustainability-environment'])
A4 = add('4', 'a', '(a)', 'Discuss two reasons why it is necessary to apply for planning permission to build a new dwelling house.',
         [row('reason-1', 'Reason 1', 6, 'Such as: to ensure the building meets current regulations; to avoid environmental damage.'),
          row('reason-2', 'Reason 2', 6, 'A second, different reason. Such as: it informs the public; it controls design, height and location; better designed communities; a legal requirement.')],
         *PLAN, 'q4-reasons', 'Planning permission (1.3).', B4, S4)
B4b = add('4', 'b', '(b)', 'Using notes and freehand sketches, describe the information that must be contained in each of the following planning documents: site notice; site location map.',
          [row('site-notice', 'Site notice note & sketch (8 + 5 marks)', 13, 'Note 8 and sketch 5. Such as: the applicant’s name; the application reference; a description of the development; where the plans can be inspected; the date the notice was erected.'),
           row('location-map', 'Site location map note & sketch (8 + 5 marks)', 13, 'Note 8 and sketch 5. Such as: the location of the dwelling and local area; a scale between 1:10560 and 1:2500; the site boundary outlined in red; neighbouring buildings; north point.')],
          *PLAN, 'q4-documents', 'Planning permission documents (1.3).', B4, S4)
C4 = add('4', 'c', '(c)', 'Discuss one advantage and one disadvantage of building a dwelling house in a town.',
         [row('advantage', 'Advantage', 6, 'Such as: public transport; less reliance on a car; amenities within walking distance; access to services and public sewerage.'),
          row('disadvantage', 'Disadvantage', 6, 'Such as: poorer air quality; noise; less connection to nature; less privacy; limited site space.')],
         ['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'], 'q4-town', 'Siting a dwelling in the built environment (1.2, 1.3).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-documents', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p19 (printed 17): (a) best 7 of 12 listed details × 5 = 35, three typical dimensions 3, draughting/accuracy/scale 8 (8/6/4) = 46; (b) throating/drip/DPC 4. Complete 50.'
S5 = 'One required section and one required cill detail. The best-seven detail list is a marking menu, not a printed choice.'
A5 = add('5', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the external wall and bottom portion of the window. Show the typical construction details from a level 400 mm below to a level 300 mm above the concrete window cill. Include three typical dimensions on your drawing.',
         [row('details', 'Any 7 x 5 marks', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: block outer leaf; full-fill insulated cavity; wall ties; block inner leaf; 13 mm plaster and 19 mm render; cavity closer; DPC; precast concrete cill with throating/drip; window board; airtight tape; window frame 120 × 80 mm; triple glazing.', list(range(0, 36, 5))),
          row('dimensions', 'Any three typical dimensions', 3, 'Three appropriate typical dimensions on the section, 1 each.'),
          row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the section: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-3-3', 'cons-3-6', 'cons-3-4'], ['question-one-drawing-questions', 'foundations-floors-walls', 'windows-doors'], 'q5-scheme',
         'Scaled drawing (1.5) of a cavity wall (3.3) at the window cill (3.6) with its DPC (3.4).', B5, S5)
B5b = add('5', 'b', '(b)', 'Show on your drawing the typical design detailing to prevent water entering at the window cill.',
          [row('cill', 'Throating / drip / DPC', 4, 'Show and identify the detail, such as a sloped cill overhanging the render with a throating or drip, wrapped in DPC. Any other suitable detail is accepted.', [0, 4])],
          ['cons-3-6', 'cons-3-4'], ['windows-doors', 'foundations-floors-walls'], 'q5-scheme', 'The window cill (3.6) and its damp proof course (3.4).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-scheme', B5, S5, parts(A5, B5b))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p20 (printed 18): (a) three signs × (sign 6 + specific reason 3) = 27; (b) two risks × 5 = 10; (c) precaution note & sketch 8 + 5 = 13. Complete 50.'
S6 = 'All three printed PPE items in (a) are required, each separately marked, not a choice. Risks and precautions are open responses.'
A6 = add('6', 'a', '(a)', 'Using a large freehand sketch, show the safety sign for each of the following personal protection equipment (PPE) items: high-visibility vest; safety boots; safety helmet. Give one specific reason why each item of personal protective equipment listed above must be worn.',
         [row('vest', 'High-visibility vest sign and specific reason (6 + 3 marks)', 9, 'Sign 6 and specific reason 3. Such as: workers visible on site so machine operators can see them and avoid accidents.'),
          row('boots', 'Safety boots sign and specific reason (6 + 3 marks)', 9, 'Sign 6 and specific reason 3. Such as: feet protected from heavy materials and objects being dropped.'),
          row('helmet', 'Safety helmet sign and specific reason (6 + 3 marks)', 9, 'Sign 6 and specific reason 3. Such as: the head protected from objects and materials falling from heights.')],
         ['cons-1-8'], ['site-safety'], 'q6-signs', 'Personal protective equipment (1.8).', B6, S6)
B6b = add('6', 'b', '(b)', 'Describe two potential risks to construction workers when working in a deep trench.',
          [row('risk-1', 'Risk 1', 5, 'Such as: the trench sides caving in or collapsing; equipment or machinery falling in on workers.'),
           row('risk-2', 'Risk 2', 5, 'A second, different risk. Such as: workers falling when entering or leaving; contact with underground services.')],
          ['cons-1-8'], ['site-safety'], 'q6-risks', 'Safety precautions on site, here in deep trenches (1.8).', B6, S6)
C6 = add('6', 'c', '(c)', 'Using notes and a freehand sketch, describe one safety precaution that workers should observe when working in a deep trench on a construction site.',
         [row('precaution', 'Safety precaution note & sketch (8 + 5 marks)', 13, 'Note 8 and sketch 5. Such as: battering the sides back to a safe angle; sheeting or a trench box beyond 1.25 m deep; guard rails and exclusion zones; spoil stored well back from the edge.')],
         ['cons-1-8'], ['site-safety'], 'q6-trench', 'Safety precautions on site, here in deep trenches (1.8).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-signs', B6, S6, parts(A6, B6b, C6))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p21 (printed 19): (a) sketch 8, kitchen access 6, advantage 6 = 20; (b) four items, each location 3 + reason 3 = 24; (c) one advantage 6. Complete 50.'
S7 = 'All four printed items in (b) are required in one sketch, not a choice.'
LIVING = (['cons-1-2'], ['planning-sustainability-environment'])
A7 = add('7', 'a', '(a)', 'Draw a large freehand sketch of the given design and show on the sketch how the kitchen could be accessed directly from the living room. Discuss one advantage of including direct access to the kitchen from the living room.',
         [row('sketch', 'Sketch of living room', 8, 'A large freehand sketch of the given design.'),
          row('access', 'Suitable access from kitchen', 6, 'Direct access to the kitchen shown, such as a door or opening in the shared wall.'),
          row('advantage', 'Advantage', 6, 'Such as: quicker to reach the kitchen; a larger space to gather; heat circulating between the most-used rooms; the family together while doing different tasks.')],
         *LIVING, 'q7-access', 'Layout design within the built environment (1.2).', B7, S7)
B7b = add('7', 'b', '(b)', 'On the sketch, show your preferred location for each of the following in the living room: sofa (3 seater); stove; sofa (2 seater); television. Give one reason for selecting each location.',
          [row('sofa-3', 'Location and valid reason for 3 seater sofa position (3 + 3 marks)', 6, 'Location 3 and reason 3. Such as: a clear view of the television and stove; against the wall to save space.'),
           row('sofa-2', 'Location and valid reason for 2 seater sofa position (3 + 3 marks)', 6, 'Location 3 and reason 3. Such as: a view of the television beside the stove; placed for conversation; not blocking light.'),
           row('stove', 'Location and valid reason for stove position (3 + 3 marks)', 6, 'Location 3 and reason 3. Such as: on an external wall for the flue; central for heat circulation and as a focal point.'),
           row('television', 'Location and valid reason for television position (3 + 3 marks)', 6, 'Location 3 and reason 3. Such as: on a wall for secure fixing; in a corner away from window glare and damage.')],
          *LIVING, 'q7-layout', 'Layout design within the built environment (1.2).', B7, S7)
C7 = add('7', 'c', '(c)', 'Discuss one advantage of incorporating a wood-burning stove in a modern living room.',
         [row('advantage', 'Advantage', 6, 'Such as: a centrepiece to gather around; warmth in the main room; environmentally friendly with timber fuel; less oil and gas used.')],
         ['cons-5-3', 'cons-5-7'], ['hot-water-space-heating', 'fire-places-fire-prevention'], 'q7-stove', 'Heating (5.3) with a stove and flue (5.7).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-layout', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p22 (printed 20): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination. It keeps the pre-audit joist-bridging ID; the other eight per-term IDs alias to it.'
TERMS = [
    ('joist-bridging', 'joist bridging', 'Joist bridging', ['cons-4-3'], ['foundations-floors-walls'],
     'keeps floor joists vertical and stops them twisting; stiffens and ties the joists together and spreads load to neighbouring joists; solid or herringbone bridging.', 'Suspended timber floors and strutting (4.3).'),
    ('steel-reinforcement', 'steel reinforcement', 'Steel reinforcement', ['cons-2-5'], ['foundations-floors-walls'],
     'combined with concrete as reinforced concrete, taking the tension in load-bearing members; placed low in a foundation; patterned bars (rebar) or mesh for grip, tied into cages.',
     'Steel reinforcement in foundations (2.5). The Ordinary reference taxonomy carries no heading for 2.5; the term keeps the Foundations, Floors & Walls association, and 2.5 is declared outside that heading’s crosswalk.'),
    ('biscuit-joint', 'biscuit joint', 'Biscuit joint', ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'],
     'used in modern furniture for butt and edge joints in boards of different widths and thicknesses; pressed beech biscuits fit grooves cut by a biscuit joiner, giving a larger gluing area.',
     'Joints (10.1) and the choice of joint (10.4). The Ordinary reference taxonomy has no joinery heading; the term keeps the Wood, Rot & Ventilation association used for joinery, and 10.1/10.4 are declared outside that heading’s crosswalk.'),
    ('working-drawing', 'working drawing', 'Working drawing', ['cons-1-5'], ['question-one-drawing-questions'],
     'a scaled drawing used as a guide when building furniture or buildings, with elevations, plan and sections, dimensions and notes; hand drafted or CAD; often called plans or blueprints.', 'Drawings and scales (1.5).'),
    ('heat-pump', 'heat pump', 'Heat pump', ['cons-5-3'], ['hot-water-space-heating'],
     'moves heat from one place to another, such as from the outside air or ground into the house for heating and hot water, very efficiently.', 'Heating systems (5.3).'),
    ('room-thermostat', 'room thermostat', 'Room thermostat', ['cons-5-3'], ['hot-water-space-heating', 'services-water-gas-electrical'],
     'senses the room temperature and switches the heating to keep it at the chosen level; dial, digital or smart (Wi-Fi) control; lower heating bills and less waste.', 'Temperature control (5.3).'),
    ('roof-light', 'rooflight', 'Roof light', ['cons-3-5', 'cons-3-9'], ['windows-doors', 'roofs'],
     'a window in the roof surface for natural light, double, triple or quadruple glazed; lets an attic become a usable room; more privacy than a dormer.', 'Windows (3.5) in the roof covering (3.9).'),
    ('ridge-board', 'ridgeboard', 'Ridge board', ['cons-3-8'], ['roofs'],
     'the horizontal member at the top ends of the rafters forming the apex of a cut roof; rafters are nailed to it; supported by the rafters or gables; typically 225 × 32 or 225 × 25 mm.', 'Roof structure (3.8).'),
    ('building-energy-rating', 'building energy rating', 'Building Energy Rating', ['cons-6-3'], ['heat-loss-insulation'],
     'a certificate rating a home’s energy performance from A to G, calculated on the energy for space heating, hot water, ventilation and lighting; A is the most efficient with the lowest bills.', 'Energy use and running costs (6.3).'),
]
Q8 = add('8', 'None-joist-bridging', '', 'Explain, with the aid of notes and freehand sketches, any five of the following: ' + '; '.join(t[1] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Construction Terms', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{t[2]}: {t[5]}' for t in TERMS),
               group=dict(claimMax=5, perOption=10, options=[t[2] for t in TERMS]))],
         list(dict.fromkeys(n for t in TERMS for n in t[3])), list(dict.fromkeys(a for t in TERMS for a in t[4])), 'q8-terms',
         'The union of the nine printed terms: ' + ' '.join(t[6] for t in TERMS), B8, S8)

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p23 (printed 21): (a) suitable finish 4, two reasons × 4 = 12; (b) two modifications, each notes + sketch 8 + 5 = 13, = 26; (c) two advantages × 6 = 12. Complete 50.'
S9 = 'The finish, modifications and advantages are open responses with no printed list; the scheme lists typical examples.'
A9 = add('9', 'a', '(a)', 'Specify a suitable applied finish to preserve the decking, and give two reasons for your choice.',
         [row('finish', 'Suitable finish', 4, 'Such as: decking, teak or furniture oil; a solvent-based preservative; exterior wood paint; varnish; decking stain.'),
          row('reason-1', 'Reason 1', 4, 'Such as: a better appearance; protection against UV damage and fading.'),
          row('reason-2', 'Reason 2', 4, 'A second, different reason. Such as: a longer life for the softwood; protection against algae, rot and decay; a change of colour.')],
         ['cons-10-7'], ['wood-rot-ventilation'], 'q9-finish', 'Surface finishing and preservation of timber (10.7).', B9, S9)
B9b = add('9', 'b', '(b)', 'The outdoor space needs to be modified so that the occupants can use the space throughout the year. Using notes and freehand sketches, show two modifications to the outdoor space that would allow its use during the winter months.',
          [row('modification-1', 'Modification 1 to space notes + sketch (8 + 5 marks )', 13, 'Notes and sketch, 8 + 5. Such as: a windbreak around the decking; a permanent roof.'),
           row('modification-2', 'Modification 2 to space notes + sketch (8 + 5 marks )', 13, 'Notes and sketch, 8 + 5, for a second, different modification. Such as: a heat source — a fire pit, patio heater or outdoor fireplace.')],
          ['cons-1-2'], ['planning-sustainability-environment'], 'q9-winter', 'Outdoor living in the built environment (1.2).', B9, S9)
C9 = add('9', 'c', '(c)', 'Discuss two advantages for the occupants of creating an outdoor living space.',
         [row('advantage-1', 'Advantage 1', 6, 'Such as: more usable space; a connection with nature and the outdoors.'),
          row('advantage-2', 'Advantage 2', 6, 'A second, different advantage. Such as: outdoor meals in warmer seasons; a higher resale value.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q9-advantages', 'Outdoor living in the built environment (1.2).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-winter', B9, S9, parts(A9, B9b, C9))

LEDGER = [(1, 'Answer any', 'Whole-exam selection: any three of the nine questions (150 marks); all question banks retained, no full-exam Cartesian cards.'),
          (4, 'any five', 'Q8 closed choose-five of nine printed terms: one card with an any-five group over all nine terms (choice is not a route).')]
FINITE = {'8': dict(choose=5, options=[t[0] for t in TERMS], cardId=Q8['id'], groupRowId='terms', wholeQuestionMarks=50, termMarks=10)}
REASONS = {
    'q1-a': 'Adds the three typical dimensions (4) and draughting/accuracy/scale (8/6/4) printed within part (a): 35 → 47.',
    'q1-b': 'Reshaped to the printed all-or-nothing row "Eaves gutter/ downpipe" (0 or 3); tariff unchanged.',
    'q2-a': 'Split into the two printed advantages (5 each); tariff unchanged (10).',
    'q3-a': 'Adds the printed quality-of-sketch band (8/6/4) to the best-eight items: 32 → 40.',
    'q3-b': 'Split into the two printed advantages (5 each); tariff unchanged (10).',
    'q4-a': 'Split into the two printed reasons (6 each); tariff unchanged (12).',
    'q4-b': 'Split into the two printed documents (note & sketch 8 + 5 each); tariff unchanged (26).',
    'q5-a': 'Adds the three typical dimensions (3) and draughting/accuracy/scale (8/6/4) printed within part (a): 35 → 46.',
    'q5-b': 'Reshaped to the printed all-or-nothing row "Throating / drip / DPC" (0 or 4); tariff unchanged.',
    'q6-a': 'Split into the three printed signs (sign 6 + specific reason 3 each); tariff unchanged (27).',
    'q6-b': 'Split into the two printed risks (5 each); tariff unchanged (10).',
    'q6-c': 'Reshaped to the printed note & sketch row (8 + 5); tariff unchanged (13).',
    'q7-b': 'Split into the four printed location-and-reason rows (3 + 3 each); tariff unchanged (24).',
    'q7-c': 'Reshaped to the printed advantage row; tariff unchanged (6).',
    'q9-a': 'Split into the printed finish (4) and two reasons (4 each); tariff unchanged (12).',
    'q9-b': 'Split into the two printed modifications (notes + sketch 8 + 5 each); tariff unchanged (26).',
    'q9-c': 'Split into the two printed advantages (6 each); tariff unchanged (12).',
    'q8-None-joist-bridging': 'Now the whole of Question 8: one card printing all nine terms with an any-five group (10 each, 50), kept under this ID; the other eight per-term IDs alias to it (choice is not a route): 10 → 50.',
}
CONSOLIDATED = {f'q8-None-{t[0]}': 'q8-None-joist-bridging' for t in TERMS[1:]}
GAPS = [dict(cardId=Q8['id'], canonicalTopicIds=['cons-2-5'], atlasTopicId=D.CROSS + 'foundations-floors-walls',
             reason='The Ordinary outgoing reference headings do not cover 2.5 (steel reinforcement); the term keeps the Foundations, Floors & Walls association.'),
        dict(cardId=Q8['id'], canonicalTopicIds=['cons-10-1', 'cons-10-4'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers joinery (10.1, 10.4, biscuit joint).')]
D.finish(LEDGER, FINITE, REASONS, consolidated=CONSOLIDATED, taxonomy_gaps=GAPS, whole_choices={'q8-None-joist-bridging'})
