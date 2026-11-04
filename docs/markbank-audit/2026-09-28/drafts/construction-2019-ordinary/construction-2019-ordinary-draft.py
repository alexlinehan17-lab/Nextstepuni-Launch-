"""Draft the 2019 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 19-27). Q8 "any five of nine" was never carded: it is added as ONE card with an any-five group
(choice is not a route). The 21 pre-audit 2019 Ordinary cards keep their IDs and concept IDs and are
corrected in place; the two printed Q6(a) situations keep their per-item cards and (a) composes them.
Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Window head and cavity wall section', concept='window-head-section',
              stem='The external wall of a dwelling house is a 400 mm concrete block wall with a full-fill insulated cavity. The wall is plastered on both sides. A triple glazed timber casement window is fixed in the external wall, as shown. The fixed frame of the window is 150 mm × 80 mm.',
              note='Original sketch and specification retained. The scheme prints the draughting, accuracy and scale band under part (b)’s sub-total, so it is marked with the cavity-closer detail.'),
    '2': dict(page=2, title='Insulating an attic and its trapdoor', concept='attic-insulation',
              stem='A young couple have bought an old, uninsulated house. They wish to improve the insulation properties of the house and have decided to start by insulating the attic space. The sketch shows the ceiling joists and the trapdoor to the attic. The ceiling joists are 200 mm × 40 mm.',
              note='Original sketch retained. Both the insulation and the sealing of the trapdoor in (b) are required, each separately marked.'),
    '3': dict(page=2, title='Cold water supply to a sink and toilet', concept='cold-water-supply-toilet', stem='',
              note='Original sketches retained. The listed components are required content, not a choice; the best-seven list is a marking menu.'),
    '4': dict(page=3, title='Reinforced strip foundation and cavity wall', concept='reinforced-strip-foundation',
              stem='The sketch shows a reinforced concrete strip foundation, and a 400 mm cavity wall for a new house.',
              note='Original sketch retained. The wall position and the steel reinforcement in (a) are both required, each separately marked.'),
    '5': dict(page=3, title='Stud partition on a floating timber floor', concept='stud-partition-floor-section',
              stem='A non-loadbearing stud partition separates two bedrooms on the first floor of a dwelling house, as shown. The partition is supported on 225 mm × 50 mm flooring joists, and the first floor is a floating tongue and groove wooden floor on 20 mm plywood decking, with a plasterboard ceiling beneath.',
              note='Original sketch and specification retained. The scheme prints the draughting, accuracy and scale band under part (b)’s sub-total, so it is marked with the partition insulation.'),
    '6': dict(page=3, title='Safety in the Construction Studies room', concept='workshop-safety', stem='',
              note='Original sketch retained. Both printed situations in (a) are required, each with two precautions and separately marked.'),
    '7': dict(page=4, title='Small open-plan kitchen and dining area', concept='kitchen-dining-layout',
              stem='A draft design for a small open-plan kitchen and dining area for a new house is shown. The positions of the window and doors are included.',
              note='Original plan retained. All three printed appliances in (a) are required in one sketch, each separately marked; floor types are open choices.'),
    '8': dict(page=4, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=4, title='Eco-friendly garden home office', concept='garden-home-office',
              stem='The sketch shows an eco-friendly home office in a garden setting. The office is of timber frame construction with an external wooden cladding.',
              note='Original sketch retained. The wood, the modification and the advantages are open responses; the scheme lists typical examples.'),
}
SCHEME_PAGES = {'1': [4, 19], '2': [5, 20], '3': [6, 21], '4': [7, 8, 22], '5': [9, 23], '6': [10, 11, 12, 24], '7': [13, 14, 25], '8': [15, 16, 26], '9': [17, 18, 27]}
D = cp.Draft(HERE, 2019, 'ordinary', ('2b3c07cfadcfded21bfd0a773f877a9d648f7c05cf990be01c0f44e981ec78d2',
                                      '7545b54efb409c3f339f58869873772e0dad225735af6d1733d213571529455d'), 21, QUESTIONS, SCHEME_PAGES)
row, add, compose = D.row, D.add, D.compose
BAND8 = [0, 4, 6, 8]
BAND6 = [0, 2, 4, 6]


def parts(*cards):
    return D.parts(*[(letter, c['questionText']) for letter, c in zip('abc', cards)])


D.figures({
    'q1-original': D.paper(2, [45, 39, 580, 235]), 'q2-original': D.paper(2, [45, 240, 580, 465]),
    'q3-original': D.paper(2, [45, 475, 580, 765]), 'q4-original': D.paper(3, [45, 39, 580, 285]),
    'q5-original': D.paper(3, [45, 295, 580, 535]), 'q6-original': D.paper(3, [45, 545, 580, 765]),
    'q7-original': D.paper(4, [45, 39, 580, 340]), 'q8-original': D.paper(4, [45, 365, 580, 470]),
    'q9-original': D.paper(4, [45, 490, 580, 765]),
    'q1-scheme': D.scheme(4, [25, 58, 580, 745]),
    'q2-attic': D.scheme(5, [25, 58, 580, 382]), 'q2-trapdoor': D.scheme(5, [25, 382, 580, 580]), 'q2-reasons': D.composite((5, [25, 562, 372, 580]), (5, [25, 580, 580, 770])),
    'q3-system': D.scheme(6, [25, 58, 580, 450]), 'q3-valve': D.scheme(6, [25, 450, 580, 615]), 'q3-dual-flush': D.scheme(6, [25, 620, 580, 775]),
    'q4-foundation': D.scheme(7, [25, 58, 580, 570]), 'q4-ties': D.scheme(7, [25, 580, 580, 760]), 'q4-ready-mix': D.scheme(8, [25, 70, 580, 255]),
    'q5-scheme': D.scheme(9, [25, 58, 580, 740]),
    'q6-adhesive': D.scheme(10, [25, 140, 580, 290]), 'q6-screwdriver': D.scheme(10, [25, 295, 580, 480]), 'q6-precautions': D.scheme(10, [25, 58, 580, 480]),
    'q6-bandsaw': D.composite((11, [25, 58, 580, 760]), (12, [25, 58, 580, 390])), 'q6-instruction': D.scheme(12, [25, 455, 580, 630]),
    'q7-layout': D.scheme(13, [25, 58, 580, 615]), 'q7-floors': D.composite((13, [25, 635, 580, 790]), (14, [25, 58, 580, 430])),
    'q7-island': D.scheme(14, [25, 465, 580, 770]),
    'q8-terms': D.composite((15, [25, 58, 580, 765]), (16, [25, 58, 580, 710])),
    'q9-cladding': D.scheme(17, [25, 58, 580, 485]), 'q9-modification': D.scheme(17, [25, 490, 580, 795]), 'q9-advantages': D.scheme(18, [25, 70, 580, 250]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p19 (printed 17): (a) best 7 of 9 listed details × 5 = 35, four typical dimensions 4 = 39; (b) cavity closer detail 3 and draughting, accuracy and scale 8 (8/6/4) printed within part (b) = 11. Complete 50.'
S1 = 'One required section and one required cavity-closer detail. The best-seven detail list is a marking menu, not a printed choice.'
A1 = add('1', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the top portion of the window. Show the wall, the concrete lintels and the fixed frame of the window. On your drawing, show the typical construction details from a level 300 mm below to a level 400 mm above the concrete lintels. Include four typical dimensions.',
         [row('details', 'Any 7 of the above details (5 marks each)', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: 19 mm external plaster; 100 mm block outer leaf; 200 mm thermal insulation; stepped DPC/cavity tie; 100 mm block inner leaf; 15 mm internal plaster; prestressed concrete lintels 100 × 70 mm; window head 150 × 80 mm; triple glazing with low-e glass.', list(range(0, 36, 5))),
          row('dimensions', 'Any 4 typical dimensions', 4, 'Four appropriate typical dimensions on the section.')],
         ['cons-1-5', 'cons-3-6', 'cons-3-3', 'cons-3-4'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls'], 'q1-scheme',
         'Scaled drawing (1.5) of a window head (3.6) in a cavity wall (3.3) with lintels and DPC (3.4).', B1, S1)
B1b = add('1', 'b', '(b)', 'Show clearly on your drawing the typical design detailing to ensure that the cavity is closed at the window head.',
          [row('closer', 'Cavity closer detail', 3, 'Show and identify a proprietary fire-stop cavity closer in the cavity above the window head, as in the scheme’s model section.', [0, 3]),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the whole section: excellent 8, good 6, fair 4. The scheme prints this band under part (b)’s sub-total.', BAND8)],
          ['cons-3-6', 'cons-3-3'], ['windows-doors', 'foundations-floors-walls'], 'q1-scheme', 'Closing the cavity (3.3) at the window head (3.6).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-scheme', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p20 (printed 18): (a) sketch 8, insulation type 5, thickness 5, quality of sketch 8 (8/6/4) = 26; (b) insulating the trapdoor 5, sealing the trapdoor 5, quality of sketch 8 (8/6/4) = 18; (c) two reasons × 3 = 6. Complete 50.'
S2 = 'Both the insulation and the sealing of the trapdoor in (b) are required, each separately marked; types and methods are open choices.'
A2 = add('2', 'a', '(a)', 'Draw a large freehand sketch of the triangular attic space. On your sketch show the typical design detailing necessary to highly insulate the attic at ceiling joist level. Recommend a preferred insulation type and give its typical thickness.',
         [row('sketch', 'Draw sketch of insulated attic space', 8, 'A large freehand sketch of the attic with insulation quilt between the joists above the plasterboard and a further layer across the joists.'),
          row('type', 'Preferred insulation type for attic space', 5, 'Such as: fibreglass insulation; rock wool; hemp insulation.'),
          row('thickness', 'Thickness of insulation', 5, 'Such as: a minimum of 350 mm.'),
          row('presentation', 'Quality of sketch (excellent, good, fair)', 8, 'Quality of the sketch: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-3-9', 'cons-6-2'], ['roofs', 'heat-loss-insulation'], 'q2-attic', 'Insulation (6.2) at ceiling level of the roof (3.9).', B2, S2)
B2b = add('2', 'b', '(b)', 'The trapdoor is also to be insulated and well-sealed. Using notes and freehand sketches show the insulation to the trapdoor. Show also one method of sealing the trapdoor.',
          [row('insulating', 'Insulating the trapdoor Valid detail one', 5, 'Such as: a pre-insulated trapdoor; layers of solid insulation fitted and glued to its upper face.'),
           row('sealing', 'Sealing the trapdoor Valid detail two', 5, 'Such as: weather stripping around the edge of the trapdoor; gaps between the frame and the joists sealed against air penetration.'),
           row('presentation', 'Quality of sketch (excellent, good, fair)', 8, 'Quality of the sketches: excellent 8, good 6, fair 4.', BAND8)],
          ['cons-6-2', 'cons-6-5'], ['heat-loss-insulation', 'air-tightness-condensation'], 'q2-trapdoor', 'Insulation (6.2) and airtightness (6.5) at the attic hatch.', B2, S2)
C2 = add('2', 'c', '(c)', 'Discuss two reasons why the couple should begin by insulating the attic space.',
         [row('reason-1', 'Advantage 1', 3, 'Such as: the greatest heat loss, up to 30%, is through the roof; the most effective way to save energy.'),
          row('reason-2', 'Advantage 2', 3, 'A second, different reason. Such as: relatively easy for the home owner to do; lower bills, a warmer house and a better BER.')],
         ['cons-6-3', 'cons-6-2'], ['heat-loss-insulation'], 'q2-reasons', 'Heat loss and running costs (6.3) with insulation (6.2).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-attic', B2, S2, parts(A2, B2b, C2))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p21 (printed 19): (a) best 7 of 9 listed items × 4 = 28 and quality of sketch 6 (6/4/2) = 34; (b) location 3, reason 3, quality of sketches 6 (6/4/2) = 12; (c) one advantage 4. Complete 50.'
S3 = 'The printed component list is required content, not a choice; the best-seven list is a marking menu.'
A3 = add('3', 'a', '(a)', 'A dwelling should have a clean water supply for domestic consumption. Draw a large freehand sketch of the given house and, on your sketch, show the pipework necessary to supply cold water to the kitchen sink on the ground floor and to the toilet on the first floor. Include the following in your diagram: rising main; pipework to the kitchen sink; insulated cold water storage tank; pipework to toilet cistern; all necessary valves.',
         [row('items', 'Any 7 of the above details (4 marks each)', 28, 'Credit the best SEVEN acceptable items at 4 marks each, capped at 28. Marked items: drawing the given sketch; 15 mm rising main; 15 mm cold water feed to the kitchen sink; water storage tank; ball valve in the tank; 28 mm overflow; insulation around the tank; 15 mm cold water supply to the cistern; valves.', list(range(0, 29, 4))),
          row('presentation', 'Quality of sketch (excellent, good, fair)', 6, 'Quality of the sketch: excellent 6, good 4, fair 2.', BAND6)],
         ['cons-5-2', 'cons-5-1'], ['hot-water-space-heating', 'services-water-gas-electrical'], 'q3-system', 'Cold water supply (5.2) from the service entry (5.1).', B3, S3)
B3b = add('3', 'b', '(b)', 'The sketch shows a valve usually used to turn off the water supply to a toilet. Using notes and freehand sketches show the preferred location of the valve. Give one reason for choosing this location for the valve.',
          [row('location', 'Location', 3, 'The isolating valve shown on the supply pipe close to the cistern.'),
           row('reason', 'Reason', 3, 'Such as: fitted close to the cistern; within easy reach to operate.'),
           row('presentation', 'Quality of sketches (excellent, good, fair)', 6, 'Quality of the sketches: excellent 6, good 4, fair 2.', BAND6)],
          ['cons-5-2', 'cons-5-6'], ['services-water-gas-electrical', 'drainage'], 'q3-valve', 'Cold water supply (5.2) to a sanitary fitment (5.6).', B3, S3)
C3 = add('3', 'c', '(c)', 'Discuss one advantage of installing a dual-flush toilet.',
         [row('advantage', 'Advantage', 4, 'Such as: two flush settings, about 6–9 litres for solid and 3–4 litres for liquid waste; less water used; less water entering treatment and sewage systems.')],
         ['cons-5-6'], ['drainage'], 'q3-dual-flush', 'Sanitary fitments (5.6).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b, C3], 'q3-system', B3, S3, parts(A3, B3b, C3))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p22 (printed 20): (a) foundation sketch 11, position of the wall 6, steel reinforcement 6, three dimensions 3, quality of sketches 6 (6/4/2) = 32; (b) method 4 and quality of sketches 6 (6/4/2) = 10; (c) two advantages × 4 = 8. Complete 50.'
S4 = 'The wall position and the steel reinforcement in (a) are both required, each separately marked; the connecting method is an open choice.'
STEEL = 'No Ordinary outgoing reference heading covers 2.5 (steel reinforcement); the card keeps the Foundations, Floors & Walls association.'
A4 = add('4', 'a', '(a)', 'Using notes and freehand sketches show the typical construction details of the strip foundation supporting the concrete block wall. Indicate the position of the wall on the foundation and the location of the steel reinforcement in the foundation. Include three typical dimensions in your sketch.',
         [row('sketch', 'Sketch of a strip foundation', 11, 'A sketch of the reinforced strip foundation under the cavity wall, such as 1100 × 350 mm.'),
          row('wall-position', 'Position of walls on strip foundation', 6, 'The wall centred on the foundation, with equal projections on both sides.'),
          row('reinforcement', 'Location of steel reinforcement', 6, 'Such as: roped steel bars near the bottom of the trench where the tensile strength is needed — generally five 12 mm rods — held about 75 mm up on concrete bricks while the concrete is poured and compacted.'),
          row('dimensions', 'Three typical dimensions', 3, 'Three typical dimensions, 1 each.'),
          row('presentation', 'Quality of sketches (excellent, good, fair)', 6, 'Quality of the sketches: excellent 6, good 4, fair 2.', BAND6)],
         ['cons-2-4', 'cons-2-5'], ['foundations-floors-walls'], 'q4-foundation', 'A strip foundation (2.4) with steel reinforcement (2.5).', B4, S4)
B4b = add('4', 'b', '(b)', 'Using notes and freehand sketches, show one method of connecting the inner and outer leaves of the wall.',
          [row('method', 'Method of connecting inner and outer leafs', 4, 'Such as: corrosion- and fire-resistant wall ties built into both leaves as the wall rises, giving stability; basalt fibre ties in highly insulated walls.'),
           row('presentation', 'Quality of sketches (excellent, good, fair)', 6, 'Quality of the sketches: excellent 6, good 4, fair 2.', BAND6)],
          ['cons-3-3'], ['foundations-floors-walls'], 'q4-ties', 'Cavity walls and wall ties (3.3).', B4, S4)
C4 = add('4', 'c', '(c)', 'Discuss two advantages of using ready-mixed concrete in the foundations of a dwelling house.',
         [row('advantage-1', 'Advantage 1', 4, 'Such as: more consistent quality, produced under controlled conditions; no labour cost of mixing on site.'),
          row('advantage-2', 'Advantage 2', 4, 'A second, different advantage. Such as: minimal waste; fast and reliable; no materials stored on site; less dust from bagged cement.')],
         ['cons-2-7'], ['concrete'], 'q4-ready-mix', 'Site and ready mixed concrete (2.7).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-foundation', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p23 (printed 21): (a) best 7 of 10 listed details × 5 = 35, three typical dimensions 3 = 38; (b) insulation in the partition 4 and draughting, accuracy and scale 8 (8/6/4) printed within part (b) = 12. Complete 50.'
S5 = 'One required section and one required insulation detail. The best-seven detail list is a marking menu, not a printed choice.'
A5 = add('5', 'a', '(a)', 'To a scale of 1:5 draw a vertical section, parallel to the joists, through the floor and the stud partition. Show the typical construction details from the plasterboard ceiling, through the first floor and the stud partition up to a level 400 mm above the finished floor. Show a floor width of 500 mm on each side of the partition. Include three typical dimensions on your drawing.',
         [row('details', 'Any 7 of the above details (5 marks each)', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: upper floor joists 200 × 50 mm; 150 mm insulation between joists; 25 mm plywood; ceiling plasterboard, plaster and vapour barrier; stud partition 100 × 50 mm; stud soleplate 100 × 50 mm; 12.5 mm plasterboard on the partition; floor underlay; floating tongued and grooved timber floor; skirting board 120 × 20 mm.', list(range(0, 36, 5))),
          row('dimensions', 'Any three typical dimensions', 3, 'Three appropriate typical dimensions on the section, 1 each.')],
         ['cons-1-5', 'cons-4-3', 'cons-4-5'], ['question-one-drawing-questions', 'foundations-floors-walls', 'windows-doors'], 'q5-scheme',
         'Scaled drawing (1.5) of a timber upper floor (4.3) carrying a stud partition (4.5).', B5, S5)
B5b = add('5', 'b', '(b)', 'On your drawing show the position of the insulation in the partition.',
          [row('insulation', 'Insulation in stud partition', 4, 'Show and identify the insulation fitted between the studs (or insulated plasterboard on both sides), as in the scheme’s model section.', [0, 4]),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the whole section: excellent 8, good 6, fair 4. The scheme prints this band under part (b)’s sub-total.', BAND8)],
          ['cons-4-5', 'cons-8-3'], ['windows-doors', 'sound'], 'q5-scheme', 'An insulated stud partition (4.5) between bedrooms, reducing sound transfer (8.3).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-scheme', B5, S5, parts(A5, B5b))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p24 (printed 22): (a) two printed situations × two precautions × 4 = 16; (b) three precautions each with a valid reason × 6 and quality of sketches 8 (8/6/4) = 26; (c) two reasons × 4 = 8. Complete 50.'
S6 = 'Both printed situations in (a) are required, each separately marked, so each keeps its pre-audit card and the part composes them; not a choice.'
WORKSHOP = (['cons-9-4'], ['site-safety'])
T6A = 'State two specific safety precautions to be observed in the Construction Studies classroom in each of the following situations: using a contact adhesive to glue veneers; using a battery powered screwdriver.'
ITEMS6 = [('using-a-contact-adhesive-to-glue-veneers', 'Using a contact adhesive to glue veneers', 'q6-adhesive',
           ('Such as: work in a well-ventilated area; keep the glue away from sources of ignition.', 'A second, different precaution. Such as: wear goggles, a mask and latex gloves; do not inhale the fumes or let it touch the skin; follow the container’s instructions.')),
          ('using-a-battery-powered-screwdriver', 'Using a battery-powered screwdriver', 'q6-screwdriver',
           ('Such as: hold the work firmly on a solid surface or in a vice, never in the hand; use the correct size of bit.', 'A second, different precaution. Such as: seat the tip fully in the screw head before starting; keep the finger off the trigger when changing bits; store the charger safely.'))]
a6 = [add('6', f'a-{slug}', f'(a) — {slug}', f'{T6A} — {heading}',
          [row('precaution-1', 'Precaution 1', 4, n1), row('precaution-2', 'Precaution 2', 4, n2)],
          *WORKSHOP, figure, 'Safety with tools and electricity in the workshop (9.4).', B6, S6) for slug, heading, figure, (n1, n2) in ITEMS6]
A6 = compose('6', 'a', '(a)', a6, 'q6-precautions', B6, S6, T6A, labels=[x[1] for x in ITEMS6])
B6b = add('6', 'b', '(b)', 'Using notes and freehand sketches, describe three specific safety precautions to be observed when operating a bandsaw to cut a piece of wood in the Construction Studies room. Give one reason for each safety precaution outlined.',
          [row('precaution-1', 'Precaution one and valid reason', 6, 'Precaution and reason. Such as: the blade guard set within 3–6 mm of the wood with the motor off, so the guard is in place before starting.'),
           row('precaution-2', 'Precaution two and valid reason', 6, 'A second, different precaution and reason. Such as: hands never closer than 100 mm to the blade, with a push stick for small stock, to avoid cutting the hands.'),
           row('precaution-3', 'Precaution three and valid reason', 6, 'A third, different precaution and reason. Such as: wait until the motor is at full speed before cutting, to prevent jamming; eye protection against splinters and dust; long hair and loose clothing contained.'),
           row('presentation', 'Quality of sketches (excellent, good, fair)', 8, 'Quality of the sketches: excellent 8, good 6, fair 4.', BAND8)],
          *WORKSHOP, 'q6-bandsaw', 'Safety with machines in the workshop (9.4).', B6, S6)
C6 = add('6', 'c', '(c)', 'Discuss two reasons why safety instruction is necessary for all students prior to using machinery in a Construction Studies room.',
         [row('reason-1', 'Reason 1', 4, 'Such as: to avoid accidents and serious injury from moving parts of machinery.'),
          row('reason-2', 'Reason 2', 4, 'A second, different reason. Such as: all users understand the dangers; a safe environment for all students; compliance with Health and Safety regulations.')],
         *WORKSHOP, 'q6-instruction', 'Safety with machines in the workshop (9.4).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-bandsaw', B6, S6, D.parts(('a', T6A), ('b', B6b['questionText']), ('c', C6['questionText'])))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p25 (printed 23): (a) sketch 4, three appliances each location 3 + reason 1, quality of sketches 8 (8/6/4) = 24; (b) kitchen floor type 3 and reason 3, dining floor type 3 and reason 3 = 12; (c) island outline and position 4, advantage 4, quality of sketches 6 (6/4/2) = 14. Complete 50.'
S7 = 'All three printed appliances in (a) are required in one sketch, not a choice. "Select a suitable floor type" in (b) is an open choice of material.'
KITCHEN = (['cons-1-2'], ['planning-sustainability-environment'])
A7 = add('7', 'a', '(a)', 'Draw a freehand sketch of the given design and show your preferred location for each of the following in the kitchen area: cooker; fridge; sink. Give one reason for selecting each location.',
         [row('sketch', 'Draw sketch of the given kitchen and dining area', 4, 'A freehand sketch of the given kitchen and dining design.'),
          row('cooker', 'Location and valid reason for cooker position (3 + 1 marks)', 4, 'Location 3 and reason 1. Such as: worktop on either side; part of the work triangle; no crossing the kitchen with hot pans; safe in relation to the door.'),
          row('fridge', 'Location and valid reason for fridge position (3 + 1 marks)', 4, 'Location 3 and reason 1. Such as: near the sink for food preparation; part of the work triangle; worktop to unpack shopping.'),
          row('sink', 'Location and valid reason for sink position (3 + 1 marks)', 4, 'Location 3 and reason 1. Such as: natural light and a view at the window; close to the cooker; worktop on either side.'),
          row('presentation', 'Quality of sketches (excellent, good, fair)', 8, 'Quality of the sketches: excellent 8, good 6, fair 4.', BAND8)],
         *KITCHEN, 'q7-layout', 'Kitchen layout in the built environment (1.2).', B7, S7)
B7b = add('7', 'b', '(b)', 'Select a suitable floor type for the kitchen area A and another appropriate floor type for the dining area B. Discuss one reason for each floor type selected.',
          [row('kitchen-floor', 'Suitable flooring type for Kitchen area A', 3, 'Such as: ceramic tiles; stone (granite, marble, limestone, slate); marmoleum.'),
           row('kitchen-reason', 'Reason for flooring type in Kitchen A', 3, 'A reason matching the kitchen floor. Such as: hard-wearing, impervious to water, easy to maintain.'),
           row('dining-floor', 'Suitable flooring type for Dining area B', 3, 'A different floor type. Such as: wood laminate; vinyl; marmoleum.'),
           row('dining-reason', 'Reason for flooring type in Dining B', 3, 'A reason matching the dining floor. Such as: durable and cheaper than solid wood; resists scuffs and stains; easy to maintain.')],
          ['cons-4-2', 'cons-1-2'], ['foundations-floors-walls', 'planning-sustainability-environment'], 'q7-floors', 'Ground-floor finishes (4.2) chosen for each room (1.2).', B7, S7)
C7 = add('7', 'c', '(c)', 'Draw a sketch of an outline design showing the position of an island unit suitable for the kitchen area A. Discuss one advantage of including an island unit in the kitchen.',
         [row('island', 'Outline design and position of island unit', 4, 'An outline island unit positioned in kitchen area A, as in the scheme’s model plan.'),
          row('advantage', 'Advantage of including island unit', 4, 'Such as: extra seating; extra storage; appliances built in; more worktop; greater design flexibility.'),
          row('presentation', 'Quality of sketches (excellent, good, fair)', 6, 'Quality of the sketches: excellent 6, good 4, fair 2.', BAND6)],
         *KITCHEN, 'q7-island', 'Kitchen layout in the built environment (1.2).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-layout', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p26 (printed 24): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination. No pre-audit card existed for this question.'
TERMS = [
    ('carbon monoxide alarm', 'Carbon monoxide alarm', ['cons-1-9', 'cons-5-7'], ['fire-places-fire-prevention'],
     'detects carbon monoxide and sounds an alarm before dangerous levels build up in a room, preventing poisoning by a colourless, tasteless, odourless "silent killer".', 'Fire and gas safety (1.9) with fuel-burning appliances and flues (5.7).'),
    ('grab rail', 'Grab rail', ['cons-1-2'], ['planning-sustainability-environment'],
     'a safety rail, usually stainless steel, chromed or plastic-coated metal, giving support and balance, lessening fatigue and something to grip in a slip or fall.', 'Inclusive design of the built environment (1.2).'),
    ('furniture castor', 'Furniture castor', ['cons-10-2'], ['wood-rot-ventilation'],
     'a wheel with a fixing plate or screw, fitted to tables, chairs and desks for easy movement; made of cast iron, plastic, nylon, steel or aluminium.',
     'Furniture fitments (10.2). The Ordinary reference taxonomy has no joinery or furniture heading; the term keeps the Wood, Rot & Ventilation association, and 10.2 is declared outside that heading’s crosswalk.'),
    ('laminated safety glass', 'Laminated safety glass', ['cons-3-6'], ['windows-doors'],
     'glass that holds together when shattered, held by a polyvinyl butyral (PVB) or ethylene-vinyl acetate (EVA) interlayer between the sheets.', 'Glass and glazing (3.6).'),
    ('eaves gutter', 'Eaves gutter', ['cons-5-4', 'cons-3-10'], ['drainage', 'roofs'],
     'fixed to the fascia, it collects rainwater from pitched or flat roofs and discharges it to an outlet or downpipe; cast iron, uPVC, aluminium, galvanised steel, copper or zinc.', 'Eaves gutters (5.4) at the roof eaves (3.10).'),
    ('balusters', 'Balusters', ['cons-4-4'], ['wood-rot-ventilation'],
     'vertical hardwood or softwood members between the string and the handrail, supporting the handrail; generally 38 × 38 or 44 × 44 mm, square or turned, no more than 100 mm apart.',
     'Stairs (4.4). The Ordinary reference taxonomy has no stairs heading; the term keeps the Wood, Rot & Ventilation association used for joinery, and 4.4 is declared outside that heading’s crosswalk.'),
    ('sapwood', 'Sapwood', ['cons-10-7'], ['wood-rot-ventilation'],
     'the outer, newer wood of a tree’s cross section, carrying the sap; lighter in colour, softer and less durable than heartwood.', 'Timber and its preservation (10.7); the taxonomy has no node for the structure of a tree.'),
    ('bridle joint', 'Bridle joint', ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'],
     'a strong woodworking joint, tee or corner, used in furniture and frame construction, such as joining table rails to uprights.',
     'Joints (10.1) and the choice of joint (10.4). The Ordinary reference taxonomy has no joinery heading; the term keeps the Wood, Rot & Ventilation association used for joinery, and 10.1/10.4 are declared outside that heading’s crosswalk.'),
    ('fluorescent lighting', 'Fluorescent lighting', ['cons-5-8'], ['services-water-gas-electrical'],
     'a low-pressure mercury-vapour discharge lamp whose ultraviolet light makes a phosphor coating glow; dearer to buy but cheaper to run; used in workplaces and homes.', 'Domestic electrical installation (5.8).'),
]
Q8 = add('8', 'terms', '', 'Explain, with the aid of notes and freehand sketches, any five of the following: ' + '; '.join(t[0] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Construction Terms', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{t[1]}: {t[4]}' for t in TERMS),
               group=dict(claimMax=5, perOption=10, options=[t[1] for t in TERMS]))],
         list(dict.fromkeys(n for t in TERMS for n in t[2])), list(dict.fromkeys(a for t in TERMS for a in t[3])), 'q8-terms',
         'The union of the nine printed terms: ' + ' '.join(t[5] for t in TERMS), B8, S8)

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p27 (printed 25): (a) suitable wood 6, two reasons × 6 = 18; (b) modification notes 6 + sketches 6 = 12 and quality of sketches 8 (8/6/4) = 20; (c) two advantages × 6 = 12. Complete 50.'
S9 = 'The wood, the modification and the advantages are open responses with no printed list; the scheme lists typical examples.'
A9 = add('9', 'a', '(a)', 'Specify a suitable wood for the external cladding, and give two reasons for your choice.',
         [row('wood', 'Suitable wood for external cladding', 6, 'Such as: cedar; larch; red deal or Scots pine; any pressure-impregnated softwood.'),
          row('reason-1', 'Valid reason one', 6, 'A reason matching the wood. Such as, cedar: very resistant to decay, light and easy to work; larch: naturally durable outdoors and grown in Ireland.'),
          row('reason-2', 'Valid reason two', 6, 'A second, different reason. Such as: a pleasant appearance; easily finished with oil; red deal: reasonably priced, strong and stable.')],
         ['cons-3-2', 'cons-10-7'], ['foundations-floors-walls', 'wood-rot-ventilation'], 'q9-cladding', 'External cladding (3.2) in a durable, treated timber (10.7).', B9, S9)
B9b = add('9', 'b', '(b)', 'The home office is to be modified to provide greater views of the surrounding garden. Using notes and freehand sketches, show one modification to the existing design that would increase the visual connection between the office and the garden.',
          [row('modification', 'Modification to existing office (6 notes + 6 sketches)', 12, 'Notes 6 and sketches 6. Such as: a sliding door in place of the existing door; full-height double-glazed clear panels; a larger, taller window; a porch or patio outside the door.'),
           row('presentation', 'Quality of sketches (excellent, good, fair)', 8, 'Quality of the sketches: excellent 8, good 6, fair 4.', BAND8)],
          ['cons-3-5', 'cons-1-2'], ['windows-doors', 'planning-sustainability-environment'], 'q9-modification', 'Windows and glazed doors (3.5) linking the building to its setting (1.2).', B9, S9)
C9 = add('9', 'c', '(c)', 'Discuss two advantages for the home office user of increasing the visual connection with the surrounding garden.',
         [row('advantage-1', 'Advantage 1', 6, 'Such as: the garden becomes part of the office; a connection with the garden area.'),
          row('advantage-2', 'Advantage 2', 6, 'A second, different advantage. Such as: more sunlight and light into the building; a warmer structure with double glazing; wheelchair access.')],
         ['cons-1-2', 'cons-6-4'], ['planning-sustainability-environment'], 'q9-advantages', 'The building in its setting (1.2) with solar gain (6.4).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-modification', B9, S9, parts(A9, B9b, C9))

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and three other questions (200 marks); all question banks retained, no full-exam Cartesian cards.'),
          (4, 'Select', 'Q7(b) "Select a suitable floor type": an open choice of material for each area, not a closed choice.'),
          (4, 'any five', 'Q8 closed choose-five of nine printed terms: one card with an any-five group over all nine terms (choice is not a route).')]
FINITE = {'8': dict(choose=5, options=[t[1] for t in TERMS], cardId=Q8['id'], groupRowId='terms', wholeQuestionMarks=50, termMarks=10)}
REASONS = {
    'q1-a': 'Adds the four typical dimensions (4) printed within part (a): 35 → 39.',
    'q1-b': 'Adds the draughting, accuracy and scale band (8/6/4) the scheme prints under part (b)’s sub-total to the cavity-closer detail: 3 → 11.',
    'q2-b': 'Rebuilt to the printed rows — insulating 5, sealing 5 and quality of sketch (8/6/4): 10 → 18.',
    'q2-c': 'Split into the two printed reasons (3 each); tariff unchanged (6).',
    'q3-a': 'Adds the printed quality-of-sketch band (6/4/2) to the best-seven items: 28 → 34.',
    'q3-b': 'Rebuilt to the printed rows — location 3, reason 3 and quality of sketches (6/4/2): 6 → 12.',
    'q3-c': 'Reshaped to the printed advantage row; tariff unchanged (4).',
    'q4-b': 'Adds the printed quality-of-sketches band (6/4/2) to the connecting method: 4 → 10.',
    'q4-c': 'Split into the two printed advantages (4 each); tariff unchanged (8).',
    'q5-a': 'Adds the three typical dimensions (3) printed within part (a): 35 → 38.',
    'q5-b': 'Adds the draughting, accuracy and scale band (8/6/4) the scheme prints under part (b)’s sub-total to the partition insulation: 4 → 12.',
    'q6-a-using-a-contact-adhesive-to-glue-veneers': 'Split into the two printed precautions (4 each), named by its scheme heading; tariff unchanged (8).',
    'q6-a-using-a-battery-powered-screwdriver': 'Split into the two printed precautions (4 each), named by its scheme heading; tariff unchanged (8).',
    'q6-b': 'Rebuilt to the printed rows — three precautions with reasons (6 each) and quality of sketches (8/6/4): 18 → 26.',
    'q6-c': 'Split into the two printed reasons (4 each): 4 → 8.',
    'q7-a': 'Rebuilt to the printed rows — sketch 4, three locations with reasons (3 + 1 each) and quality of sketches (8/6/4): 16 → 24.',
    'q7-b': 'Split into the printed floor types and reasons for areas A and B (3 each); tariff unchanged (12).',
    'q7-c': 'Rebuilt to the printed rows — island outline 4, advantage 4 and quality of sketches (6/4/2): 8 → 14.',
    'q9-a': 'Split into the printed wood (6) and two reasons (6 each); tariff unchanged (18).',
    'q9-b': 'Adds the printed quality-of-sketches band (8/6/4) to the modification notes and sketches (6 + 6): 12 → 20.',
    'q9-c': 'Split into the two printed advantages (6 each); tariff unchanged (12).',
}
GAPS = [dict(cardId=A4['id'], canonicalTopicIds=['cons-2-5'], atlasTopicId=D.CROSS + 'foundations-floors-walls', reason=STEEL),
        dict(cardId=Q8['id'], canonicalTopicIds=['cons-10-2', 'cons-4-4', 'cons-10-1', 'cons-10-4'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers furniture fitments (10.2, furniture castor), stairs (4.4, balusters) or joinery (10.1, 10.4, bridle joint).')]
D.finish(LEDGER, FINITE, REASONS, taxonomy_gaps=GAPS, whole_choices={'q8-terms'})
