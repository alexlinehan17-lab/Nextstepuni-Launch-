"""Draft the 2012 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 15-23). The paper was never carded, so every task is added. Q8 "any five of nine" is ONE card
(choice is not a route). Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Tiled cut roof eaves section', concept='tiled-roof-eaves-section',
              stem='The sketch shows a tiled roof of a dwelling house, which is supported on a 350 mm external concrete block wall with an insulated cavity. The roof is a traditional cut roof and has a pitch of 45°.',
              note='Original sketch and specification retained. The scheme prints the draughting, accuracy and scale band after the part (b) row, so it is marked with the cavity closer.'),
    '2': dict(page=2, title='External insulation of an existing wall', concept='external-insulation-system',
              stem='A dwelling house, as shown in the sketch, has a 300 mm external block wall with 50 mm expanded polystyrene insulation in the cavity. The wall has a smooth external render finish. It is proposed to improve the insulation properties of the wall by adding an external system of insulation.',
              note='Original sketch retained. "one suitable method" is an open choice of method; the scheme gives a typical system.'),
    '3': dict(page=2, title='Mains cold water to a kitchen sink', concept='mains-cold-water-supply',
              stem='A dwelling house is connected to the public water supply system to provide clean, treated water for the household.',
              note='Original sketch retained. The listed components are required content, not a choice; the best-six list is a marking menu.'),
    '4': dict(page=2, title='Strip foundation design', concept='strip-foundation-design',
              stem='A strip foundation is designed to support a 350 mm external wall of a dwelling house. The wall is of concrete block construction with an insulated cavity, as shown in the sketch.',
              note='Original sketch retained. All four printed headings in (a) are required, each separately marked.'),
    '5': dict(page=3, title='Triple-glazed window cill section', concept='window-cill-section',
              stem='A triple-glazed timber casement window, as shown in the sketch, is fixed in a 350 mm external concrete block wall with an insulated cavity. The fixed frame of the window is 150 mm × 80 mm. The wall is plastered on both sides.',
              note='Original sketch and specification retained. The scheme prints the draughting, accuracy and scale band after the part (b) row, so it is marked with the cold-bridge detail.'),
    '6': dict(page=3, title='Lifting, placing concrete and protective equipment', concept='site-safety-lifting-concrete', stem='',
              note='Both printed situations in (a) are required, each separately marked; the two items of equipment in (b) are an open response.'),
    '7': dict(page=3, title='Planning permission for a garage conversion', concept='garage-conversion-planning',
              stem='A homeowner wishes to obtain planning permission to convert an existing garage to a living room, as shown in the accompanying sketch.',
              note='Original sketch retained. Both printed planning documents in (b) are required, each separately marked.'),
    '8': dict(page=3, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=3, title='Restoring a solid oak dining table', concept='oak-table-restoration',
              stem='The sketch shows a traditional dining table made from solid oak.',
              note='Original sketch retained. The joint and the finish are open choices; the scheme gives typical examples.'),
}
SCHEME_PAGES = {'1': [4, 15], '2': [5, 16], '3': [6, 17], '4': [6, 7, 18], '5': [8, 19], '6': [8, 9, 20], '7': [10, 21], '8': [11, 12, 13, 22], '9': [13, 14, 23]}
D = cp.Draft(HERE, 2012, 'ordinary', ('d529d6c698018dc5277c9263c92682f5c6294239f37f59ac891caea7056238e3',
                                      '6e9157b363ec4060b91166a6ce6a623e211cf5e81847a41cd4cdcf5918f0bebe'), 0, QUESTIONS, SCHEME_PAGES)
row, add, compose = D.row, D.add, D.compose
BAND8 = [0, 4, 6, 8]
BAND6 = [0, 2, 4, 6]
BAND4 = [0, 2, 3, 4]


def parts(*cards):
    return D.parts(*[(letter, c['questionText']) for letter, c in zip('abc', cards)])


D.figures({
    'q1-original': D.paper(2, [30, 39, 580, 197]), 'q2-original': D.paper(2, [30, 197, 580, 372]),
    'q3-original': D.paper(2, [30, 372, 580, 580]), 'q4-original': D.paper(2, [30, 580, 580, 790]),
    'q5-original': D.paper(3, [30, 39, 580, 191]), 'q6-original': D.paper(3, [30, 191, 580, 313]),
    'q7-original': D.paper(3, [30, 313, 580, 509]), 'q8-original': D.paper(3, [30, 509, 580, 601]),
    'q9-original': D.paper(3, [30, 601, 580, 790]),
    'q1-section': D.scheme(4, [18, 50, 580, 622]), 'q1-closer': D.scheme(4, [18, 622, 580, 777]),
    'q2-method': D.scheme(5, [25, 50, 580, 564]), 'q2-advantages': D.scheme(5, [25, 564, 580, 777]),
    'q3-system': D.scheme(6, [25, 50, 580, 322]), 'q3-frost': D.scheme(6, [25, 322, 580, 408]), 'q3-saving': D.scheme(6, [25, 408, 580, 563]),
    'q4-design': D.composite((6, [25, 563, 580, 777]), (7, [25, 60, 580, 540])), 'q4-reasons': D.scheme(7, [25, 540, 580, 777]),
    'q5-scheme': D.scheme(8, [25, 46, 580, 436]),
    'q6-precautions': D.composite((8, [25, 436, 580, 777]), (9, [25, 50, 580, 252])), 'q6-ppe': D.scheme(9, [25, 252, 580, 777]),
    'q7-reasons': D.scheme(10, [25, 50, 580, 207]), 'q7-documents': D.scheme(10, [25, 207, 580, 565]), 'q7-refusal': D.scheme(10, [25, 565, 580, 777]),
    'q8-terms': D.composite((11, [25, 50, 580, 777]), (12, [25, 50, 580, 777]), (13, [25, 50, 580, 120])),
    'q9-joint': D.scheme(13, [25, 120, 580, 505]), 'q9-restore': D.scheme(13, [25, 505, 580, 777]), 'q9-finish': D.scheme(14, [25, 50, 580, 560]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p15 (printed 12): (a) best 7 of 16 listed details × 5 = 35, three typical dimensions 5 = 40; (b) cavity closer 4, and draughting, accuracy and scale 6 (6/4/2) printed after it = 10. Complete 50.'
S1 = 'One required section and one required method of closing the cavity. The best-seven detail list is a marking menu, not a printed choice.'
A1 = add('1', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the eaves of the tiled roof and the external wall. Show the typical construction details from a level 400 mm below the wall plate, through the eaves and include three courses of tiles at eaves. Include the roof insulation and show clearly the ventilation path to the roof structure at the eaves. Include three typical dimensions.',
         [row('details', 'Any 7 of the above details (5 marks each)', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: concrete tiles; 44 × 35 mm battens; breathable membrane; rafters 150–250 × 40 mm; roof insulation; 150 × 40 mm ceiling joists; 12.5 mm foil-backed plasterboard and skim; 100 × 75 mm wallplate; internal plaster and external render; 100 mm inner leaf; wall insulation; 50 mm residual cavity; 100 mm outer leaf; fascia and soffit; 100 mm eaves gutter; ventilation path.', list(range(0, 36, 5))),
          row('dimensions', 'Three typical dimensions', 5, 'Three typical dimensions on the section.')],
         ['cons-1-5', 'cons-3-9', 'cons-3-10', 'cons-3-3'], ['question-one-drawing-questions', 'roofs', 'foundations-floors-walls'], 'q1-section',
         'Scaled drawing (1.5) of a tiled roof (3.9) at the eaves (3.10) on a cavity wall (3.3).', B1, S1)
B1b = add('1', 'b', '(b)', 'On your drawing, show one method of closing the cavity at eaves level.',
          [row('closer', 'Method of closing cavity at eaves level', 4, 'Such as: a proprietary cavity closer at the top of the wall; or a slate fixed across the cavity to both leaves.'),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 6, 'Draughting, accuracy and scale of the whole section: excellent 6, good 4, fair 2. The scheme prints this band after the part (b) row.', BAND6)],
          ['cons-3-10', 'cons-3-3'], ['roofs', 'foundations-floors-walls'], 'q1-closer', 'Closing the cavity (3.3) at the eaves (3.10).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-section', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p16 (printed 13): (a) notes — two descriptions × 6, surface finish 6 and insulation type and thickness 3 + 3 = 24 — and sketch — two details × 4 and quality 8 (8/6/4) = 16: 40; (b) two advantages × 5 = 10. Complete 50.'
S2 = '"one suitable method" is an open choice of method; the scheme gives a typical external insulation system.'
A2 = add('2', 'a', '(a)', 'Using notes and neat freehand sketches, show one suitable method of applying an external insulation system to the wall. Specify the insulation material used, indicate its typical thickness and include details of the external surface finish to the insulation.',
         [row('description-1', 'Valid description one', 6, 'Such as: slabs of insulation fixed to the wall with adhesive and mechanical fixings.'),
          row('description-2', 'Valid description two', 6, 'A second, different step. Such as: an acrylic basecoat with a fibre mesh embedded for impact resistance; a coloured primer.'),
          row('finish', 'Details of external surface finish to the insulation', 6, 'Such as: a coloured, textured acrylic render, trowelled or sprayed, durable and in a range of colours.'),
          row('insulation', 'Type and thickness of insulation (3 marks + 3marks)', 6, 'Type 3 and thickness 3. Such as: expanded polystyrene, at least 120 mm and up to 300 mm; phenolic foam, at least 75 mm; or Gutex or cork.'),
          row('sketch', 'External insulation – Sketch', 16, 'Two valid details on the sketch, 4 each, and the quality of the sketch, excellent 8, good 6, fair 4.')],
         ['cons-6-2', 'cons-3-2'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q2-method',
         'External insulation (6.2) on the external envelope (3.2).', B2, S2)
B2b = add('2', 'b', '(b)', 'List two advantages of applying an external system of insulation to the walls of an existing house.',
          [row('advantage-1', 'Advantage one', 5, 'Such as: less heat loss; lower bills and CO₂; no loss of floor area and no disruption inside.'),
           row('advantage-2', 'Advantage two', 5, 'A second, different advantage. Such as: the wall becomes a heat store; a practical way to insulate an existing building; a new finish that hides all the fixings.')],
          ['cons-6-3', 'cons-6-2'], ['heat-loss-insulation'], 'q2-advantages', 'Heat loss and running costs (6.3) with insulation (6.2).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b], 'q2-method', B2, S2, parts(A2, B2b))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p17 (printed 14): (a) best 6 of 11 listed details × 5 = 30 and quality of sketch 8 (8/6/4) = 38; (b) two frost details × 3 = 6; (c) two ways × 3 = 6. Complete 50.'
S3 = 'The printed component list is required content, not a choice; the best-six list is a marking menu.'
WATER = (['cons-5-1', 'cons-5-2'], ['services-water-gas-electrical'])
A3 = add('3', 'a', '(a)', 'Using a single-line labelled diagram, show the pipework required to supply cold water to a kitchen sink, as shown in the sketch. Include the following in your diagram: pipework from public mains to kitchen sink; location of valves; material and typical size of pipework.',
         [row('details', 'Any 6 of the above details (5 marks each)', 30, 'Credit the best SIX acceptable details at 5 marks each, capped at 30. Marked details: connection to the water mains; stop valve; water supply pipe; external wall; protective sleeve for the supply; service pipe insulation; stop valve inside; rising main; connection to the kitchen sink; typical material; typical pipe size.', list(range(0, 31, 5))),
          row('presentation', 'Quality of sketch (excellent, good, fair)', 8, 'Quality of the sketch: excellent 8, good 6, fair 4.', BAND8)],
         *WATER, 'q3-system', 'The water service entry (5.1) and cold water supply (5.2).', B3, S3)
B3b = add('3', 'b', '(b)', 'Include in your sketch two design details that would prevent the water in the mains supply from freezing during very cold weather.',
          [row('frost', 'Designs details (2 × 3 marks)', 6, 'Two details, 3 each. Such as: the pipe laid about one metre deep, at least 750 mm; the last 600 mm of the service pipe insulated; heavy-duty polyethylene or PVC pipe.')],
          *WATER, 'q3-frost', 'Protecting the service entry (5.1) from frost.', B3, S3)
C3 = add('3', 'c', '(c)', 'Outline two ways in which the household could reduce the use of treated water from the public water supply.',
         [row('ways', 'Two ways (2 × 3 marks)', 6, 'Two ways, 3 each. Such as: a displacement bottle in the cistern; push taps; a conical sink; dual-flush cisterns; rainwater harvesting; an aerated shower head; recycled grey water for flushing and gardening.')],
         ['cons-5-2', 'cons-1-2'], ['services-water-gas-electrical', 'planning-sustainability-environment'], 'q3-saving', 'Water supply (5.2) used sustainably (1.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-system', B3, S3, parts(A3, B3b, C3))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p18 (printed 15): (a) four printed headings × (primary communication 6 + other communication 4) = 40; (b) two environmental reasons × 5 = 10. Complete 50.'
S4 = 'All four printed headings in (a) are required, each separately marked; not a choice.'
A4 = add('4', 'a', '(a)', 'Describe, using notes and neat freehand sketches, the design of a typical strip foundation for the above external wall under the following headings: width and depth of trench; finished level of concrete in foundation; reinforcement of foundation; position of wall on strip foundation.',
         [row('trench', 'Width and depth of trench', 10, 'Primary communication 6 and other communication 4. Such as: at least three times the wall thickness, 1050 mm for a 350 mm wall; as deep as the ground needs, at least 600 mm to the top of the concrete, below the frost line.'),
          row('level', 'Finish level of concrete in foundation', 10, 'Primary communication 6 and other communication 4. Such as: pegs driven into the trench base, projecting by the foundation thickness, levelled with a straight edge and laser level.'),
          row('reinforcement', 'Reinforcement of foundation', 10, 'Primary communication 6 and other communication 4. Such as: ribbed mild steel bars supported 75 mm from the bottom, where the tension is; concrete poured, vibrated and compacted around them; or steel mesh.'),
          row('position', 'Position of wall on strip foundation', 10, 'Primary communication 6 and other communication 4. Such as: the wall central on the foundation, with equal projections on both sides.')],
         ['cons-2-4', 'cons-2-5'], ['foundations-floors-walls'], 'q4-design', 'Strip foundations (2.4) and their reinforcement (2.5).', B4, S4)
B4b = add('4', 'b', '(b)', 'Discuss two environmental reasons why a strip foundation is the preferred foundation type for the external wall of the house.',
          [row('reason-1', 'Reason one', 5, 'Such as: less concrete than a raft foundation; minimum excavation, using less energy.'),
           row('reason-2', 'Reason two', 5, 'A second, different reason. Such as: less steel; a lower carbon footprint than other foundations; environmentally sustainable.')],
          ['cons-2-4', 'cons-2-2'], ['foundations-floors-walls'], 'q4-reasons', 'The choice of foundation (2.2, 2.4).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b], 'q4-design', B4, S4, parts(A4, B4b))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p19 (printed 16): (a) best 7 of 13 listed details × 5 = 35, three typical dimensions 5 = 40; (b) cold-bridge detail 4, and draughting, accuracy and scale 6 (6/4/2) printed after it = 10. Complete 50.'
S5 = 'One required section and one required cold-bridge detail. The best-seven detail list is a marking menu, not a printed choice.'
A5 = add('5', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the bottom portion of the window showing the fixed frame of the window and the concrete cill. Show the typical construction details from 300 mm below to a level 250 mm above the concrete cill. Indicate the typical sizes of three main components.',
         [row('details', 'Any 7 of the above details (5 marks each)', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: 25 mm window board; 150 × 80 mm frame; triple low-e glazing; precast concrete cill; mastic or taped seals; DPC; 15 mm plaster outside and in; 100 mm outer leaf; 50 mm residual cavity; wall tie; 100 mm insulation; 100 mm inner leaf; proprietary cavity closer.', list(range(0, 36, 5))),
          row('dimensions', 'Three typical dimensions', 5, 'Typical sizes of three main components.')],
         ['cons-1-5', 'cons-3-6', 'cons-3-3'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls'], 'q5-scheme',
         'Scaled drawing (1.5) of a window cill (3.6) in a cavity wall (3.3).', B5, S5)
B5b = add('5', 'b', '(b)', 'Include in your drawing the typical design detailing that would prevent the formation of a thermal/cold bridge at the concrete cill.',
          [row('cold-bridge', 'Valid design detail', 4, 'Such as: insulation brought up behind the concrete cill; an insulated cavity closer.'),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 6, 'Draughting, accuracy and scale of the whole section: excellent 6, good 4, fair 2. The scheme prints this band after the part (b) row.', BAND6)],
          ['cons-6-2', 'cons-3-6'], ['heat-loss-insulation', 'windows-doors'], 'q5-scheme', 'A thermal bridge (6.2) at the window cill (3.6).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-scheme', B5, S5, parts(A5, B5b))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p20 (printed 17): (a) for each printed situation two precautions × 4 and reasons 2 = 10, 20; (b) two items, each note 5, sketch 5 (5/3/2) and importance 5 = 15, 30. Complete 50.'
S6 = 'Both printed situations in (a) are required, each separately marked; the two items in (b) are an open response.'
SITE = (['cons-1-8'], ['site-safety'])
A6 = add('6', 'a', '(a)', 'List two specific safety precautions that should be observed in each of the following situations and give one reason for each safety precaution listed: manually lifting a load from a floor; placing concrete in a foundation trench from a ready-mix truck.',
         [row('lifting', 'Safety precautions when lifting a load', 10, 'Two precautions 4 each and reasons 2. Such as: stand close, back straight, bend the knees; test the load and get help if too heavy; keep it close to the body; do not twist; a clear, tidy area — protecting your back.'),
          row('concrete', 'Safety precautions when placing concrete in a foundation', 10, 'Two precautions 4 each and reasons 2. Such as: a high visibility jacket, boots and helmet; the driver able to see the work; the truck kept back from the trench edge in wet weather; a deep trench supported; only qualified workers with Safe Pass.')],
         *SITE, 'q6-precautions', 'Safety precautions on site (1.8).', B6, S6)
B6b = add('6', 'b', '(b)', 'Using notes and neat freehand sketches, describe two items of personal protective equipment that must be worn on a building site and discuss the importance of each item to ensure the personal safety of workers on a building site.',
          [row('item-1', 'Item One', 15, 'Note 5, sketch 5 (excellent 5, good 3, fair 2) and importance 5. Such as: a high visibility jacket or vest with reflective strips, so workers are seen, especially near machinery.'),
           row('item-2', 'Item two', 15, 'A second, different item: note 5, sketch 5 (5/3/2) and importance 5. Such as: a safety helmet protecting the head from falling objects; steel cap boots protecting the feet.')],
          *SITE, 'q6-ppe', 'Personal protective equipment on site (1.8).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b], 'q6-precautions', B6, S6, parts(A6, B6b))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p21 (printed 18): (a) two reasons × 6 = 12; (b) site location map three details × 5 = 15 and site notice three details × 5 = 15 = 30; (c) one reason 8. Complete 50.'
S7 = 'Both printed planning documents in (b) are required, each separately marked; not a choice.'
PLAN = (['cons-1-3'], ['planning-sustainability-environment'])
A7 = add('7', 'a', '(a)', 'Discuss two reasons why it is necessary to apply for planning permission to convert the garage to a living room.',
         [row('reason-1', 'Reason one', 6, 'Such as: a change of use; the front appearance of the house changes, with a new window.'),
          row('reason-2', 'Reason two', 6, 'A second, different reason. Such as: a legal requirement when changing the front elevation; others may object or make a submission.')],
         *PLAN, 'q7-reasons', 'Planning permission (1.3).', B7, S7)
B7b = add('7', 'b', '(b)', 'Outline the information that must be contained in each of the following documents when making a planning application to the planning authority: site location map; copy of site notice.',
          [row('map', 'Site location map', 15, 'Three valid details, 5 each. Such as: the Ordnance Survey sheet number; north; the townland; nearby features; boundaries in red, adjoining land owned in blue, wayleaves in yellow; the site notice location.'),
           row('notice', 'Site notice', 15, 'Three valid details, 5 each. Such as: the applicant’s name and address; the type of permission and date; a description of the development; whether it is a protected structure; that it may be inspected at the planning authority within 5 weeks.')],
          *PLAN, 'q7-documents', 'Planning application documents (1.3).', B7, S7)
C7 = add('7', 'c', '(c)', 'Discuss one reason why a planning authority might refuse planning permission for the proposed conversion.',
         [row('refusal', 'Valid detail', 8, 'Such as: it changes the front elevation; defective specifications such as floor-to-ceiling height; windows overlooking a neighbour; a design out of character; a substandard structure.')],
         *PLAN, 'q7-refusal', 'Planning permission (1.3).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-documents', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p22 (printed 19): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination. No pre-audit card existed for this question.'
TERMS = [
    ('rainwater butt', 'Rainwater butt', ['cons-5-4'], ['drainage'],
     'a barrel or tank connected to the downpipe to collect rainwater from the roof, with an overflow and a tap at the base; 100–300 litres; part of rainwater harvesting.', 'Rainwater from gutters and downpipes (5.4).'),
    ('box dovetail joint', 'Box Dovetail Joint', ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'],
     'a joint for box shapes and drawers in quality furniture, by hand or machine; slope 1:6 for softwood, 1:8 for hardwood; decorative, with contrasting woods.',
     'Joints (10.1) and the choice of joint (10.4). The Ordinary reference taxonomy has no joinery heading; the term keeps the Wood, Rot & Ventilation association used for joinery, and 10.1/10.4 are declared outside that heading’s crosswalk.'),
    ('compression joint', 'Compression joint', ['cons-5-2'], ['services-water-gas-electrical'],
     'a brass or PVC plumbing joint for copper or PVC pipe: the ends cut square, the nut and olive slipped on, and the nut tightened to compress the olive into a watertight joint.', 'Water supply pipework (5.2).'),
    ('wall tie', 'Wall tie', ['cons-3-3'], ['foundations-floors-walls'],
     'a stainless steel fitting holding the two leaves of a cavity wall together so they act as one, and holding the insulation; at 900 mm horizontally and 450 mm vertically.', 'Cavity walls (3.3).'),
    ('gully trap', 'Gully trap', ['cons-5-5'], ['drainage'],
     'a PVC fitting at the head of an underground drain collecting waste or rainwater, with a grid against leaves and a water seal keeping odours and gases in the drain; it may have a back inlet.', 'Underground drainage (5.5).'),
    ('angle bead', 'Angle bead', ['cons-4-1'], ['foundations-floors-walls'],
     'a stainless, galvanised steel or plastic bead with a solid rib and mesh flanges, fixed with nails or plaster dabs to give a true, reinforced plaster corner inside or out.',
     'Wall finishes (4.1). No Ordinary outgoing reference heading covers plastering; the term keeps the Foundations, Floors & Walls association, and 4.1 is declared outside that heading’s crosswalk.'),
    ('newel post', 'Newel Post', ['cons-4-4'], ['foundations-floors-walls'],
     'a hardwood or softwood post, usually 75 × 75 or 100 × 100 mm, at the top or bottom of the stairs string or at a landing, supporting the handrail; square or round, often shaped or carved.',
     'Stairs (4.4). No Ordinary outgoing reference heading covers stairs; the term keeps the Foundations, Floors & Walls association, and 4.4 is declared outside that heading’s crosswalk.'),
    ('through and through sawing', 'Through and through sawing', ['cons-10-3'], ['wood-rot-ventilation'],
     'plain sawing: the log cut straight through into boards, with little waste and the widest boards, but boards likely to cup in seasoning and no particular grain pattern.', 'The conversion of timber into boards (10.3).'),
    ('biscuit joint', 'Biscuit joint', ['cons-10-3'], ['wood-rot-ventilation'],
     'a biscuit joiner cuts crescent grooves in the edges for compressed beech biscuits, glued and cramped; ideal for joining boards edge to edge.', 'Jointing boards (10.3).'),
]
Q8 = add('8', 'terms', '', 'Explain, with the aid of notes and neat freehand sketches, any five of the following: ' + '; '.join(t[0] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Terms', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{t[1]}: {t[4]}' for t in TERMS),
               group=dict(claimMax=5, perOption=10, options=[t[1] for t in TERMS]))],
         list(dict.fromkeys(n for t in TERMS for n in t[2])), list(dict.fromkeys(a for t in TERMS for a in t[3])), 'q8-terms',
         'The union of the nine printed terms: ' + ' '.join(t[5] for t in TERMS), B8, S8)

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p23 (printed 20): (a) joint name 4, suitability 4 and quality of sketch 6 (6/4/2) = 14; (b) two preparation details × 6 and quality of sketch 4 (4/3/2) = 16; (c) finish 4, two application details × 6 and quality of sketches 4 (4/3/2) = 20. Complete 50.'
S9 = 'The joint and the finish are open choices; the scheme gives typical examples.'
A9 = add('9', 'a', '(a)', 'Show, using notes and neat freehand sketches, a suitable method of jointing the front rail to the leg and discuss why the method of jointing shown is suitable.',
         [row('name', 'Name', 4, 'Such as: a haunched mortise and tenon; a dowel joint.'),
          row('suitability', 'Suitability of joint', 4, 'Such as, the haunched mortise and tenon: the traditional, strong and sturdy joint for quality work, with a high glue area, resisting twisting; dowels are weaker.'),
          row('presentation', 'Quality of sketch (excellent good fair)', 6, 'Quality of the sketch of the joint: excellent 6, good 4, fair 2.', BAND6)],
         ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'], 'q9-joint', 'Joints (10.1) and the choice of joint (10.4).', B9, S9)
B9b = add('9', 'b', '(b)', 'It has been decided to restore the tabletop, which has become damaged over time, as shown. Show, using notes and neat freehand sketches, the steps involved in removing the marks and in preparing the tabletop for the application of a new applied finish.',
          [row('detail-1', 'Valid detail one', 6, 'Such as: the surface cleaned, with paint or varnish remover if needed; sanded with medium to fine glasspaper or an electric sander.'),
           row('detail-2', 'Valid detail two', 6, 'A second, different step. Such as: deep marks repaired or lightly planed out; steel wool for a smooth finish; cleaned with white spirit and lightly sanded again.'),
           row('presentation', 'Quality of sketch (excellent good fair)', 4, 'Quality of the sketch: excellent 4, good 3, fair 2.', BAND4)],
          ['cons-10-7'], ['wood-rot-ventilation'], 'q9-restore', 'Surface preparation of timber (10.7).', B9, S9)
C9 = add('9', 'c', '(c)', 'Recommend a suitable applied finish for the tabletop. Describe, using notes and neat freehand sketches, the steps to be followed when applying the recommended finish.',
         [row('finish', 'Name of finish', 4, 'Such as: varnish; wax; oil or Danish oil; lacquer.'),
          row('detail-1', 'Valid detail one', 6, 'A step matching the finish. Such as: varnish applied with a good brush, lightly sanded and a second coat applied; oil applied with a lint-free cloth.'),
          row('detail-2', 'Valid detail two', 6, 'A second, different step. Such as: wax applied in very light layers, dried and buffed, layer by layer; lacquer sprayed on for a high quality finish.'),
          row('presentation', 'Quality of sketches (excellent good fair)', 4, 'Quality of the sketches: excellent 4, good 3, fair 2.', BAND4)],
         ['cons-10-7'], ['wood-rot-ventilation'], 'q9-finish', 'Applied finishes for timber (10.7).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-restore', B9, S9, parts(A9, B9b, C9))

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and three other questions (200 marks); all question banks retained, no full-exam Cartesian cards.'),
          (3, 'any five', 'Q8 closed choose-five of nine printed terms: one card with an any-five group over all nine terms (choice is not a route).')]
FINITE = {'8': dict(choose=5, options=[t[1] for t in TERMS], cardId=Q8['id'], groupRowId='terms', wholeQuestionMarks=50, termMarks=10)}
JOIN = 'No Ordinary outgoing reference heading covers joinery (10.1, 10.4); the card keeps the Wood, Rot & Ventilation association.'
GAPS = [dict(cardId=A4['id'], canonicalTopicIds=['cons-2-5'], atlasTopicId=D.CROSS + 'foundations-floors-walls',
             reason='No Ordinary outgoing reference heading covers reinforcement (2.5); the card keeps the Foundations, Floors & Walls association.'),
        dict(cardId=Q8['id'], canonicalTopicIds=['cons-10-1', 'cons-10-4'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers joinery (10.1, 10.4, box dovetail joint).'),
        dict(cardId=Q8['id'], canonicalTopicIds=['cons-4-1', 'cons-4-4'], atlasTopicId=D.CROSS + 'foundations-floors-walls',
             reason='No Ordinary outgoing reference heading covers plastering or stairs (4.1 angle bead, 4.4 newel post).'),
        dict(cardId=A9['id'], canonicalTopicIds=['cons-10-1', 'cons-10-4'], atlasTopicId=D.CROSS + 'wood-rot-ventilation', reason=JOIN)]
D.finish(LEDGER, FINITE, {}, taxonomy_gaps=GAPS, whole_choices={'q8-terms'})
