"""Draft the 2014 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 18-26). The paper was never carded, so every task is added. Q8 "any five of nine" is ONE card
(choice is not a route).
Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='External wall and first floor section', concept='wall-first-floor-section',
              stem='The sketch shows a portion of the external wall and the first floor of a two storey dwelling house. The external wall is a 350 mm concrete block wall. The cavity is filled with blown polystyrene beads. The first floor is a floating tongued and grooved hardwood floor, on 20 mm plywood, on 225 mm × 40 mm joists with a plasterboard ceiling beneath.',
              note='Original sketch and specification retained. The scheme prints the draughting, accuracy and scale band after the part (b) row, so it is marked with the joist bridging detail.'),
    '2': dict(page=2, title='External insulation to a solid block wall', concept='external-wall-insulation',
              stem='The sketch shows a single storey extension to a dwelling house. The external wall of the extension is a single leaf, 215 mm solid concrete block wall. The wall has an external render but it is not insulated. It is proposed to improve the insulation properties of the external wall of the extension by fixing insulation, 200 mm in thickness, to the outside of the wall.',
              note='Original sketch retained. "one method" in (a) is an open choice of method; the scheme gives a typical method.'),
    '3': dict(page=2, title='Stove and back boiler hot water to the sink', concept='stove-back-boiler-hot-water', stem='',
              note='Original sketch retained. The listed components are required content, not a choice; the best-nine list is a marking menu.'),
    '4': dict(page=2, title='Timber stud partition, socket and skim finish', concept='stud-partition-skim',
              stem='A non load-bearing timber stud partition, with plasterboard on both sides, separates a kitchen and living room, as shown in the sketch.',
              note='Original sketch retained. "one method" in (b) is an open choice of method; the scheme gives two typical methods.'),
    '5': dict(page=3, title='Cut roof section at the ridge', concept='cut-roof-ridge-section',
              stem='A dwelling house has a traditional cut roof pitched at 45°, as shown in the sketch. The roof is covered with concrete tiles, which are supported on 200 mm × 50 mm rafters.',
              note='Original sketch and specification retained. The scheme prints the draughting, accuracy and scale band after the part (b) row, so it is marked with the ventilation detail.'),
    '6': dict(page=3, title='Personal protective equipment on site', concept='site-ppe', stem='',
              note='Original sketches retained. All three printed signs in (a) are required, each separately marked.'),
    '7': dict(page=3, title='Rainwater harvesting and water meters', concept='rainwater-harvesting',
              stem='A two-storey house with a slated roof is shown in the sketch. It has been decided to collect and store the rainwater from the roof for reuse.',
              note='Original sketch retained. The collection method is an open response; the scheme gives an underground tank and a water butt.'),
    '8': dict(page=3, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=3, title='Kitchen layout, painted cabinets and worktops', concept='kitchen-layout-worktops',
              stem='The plan of a small kitchen in a new dwelling house is shown. The position of the worktop is shown at A. The location of the windows is also shown.',
              note='Original plan retained. The locations, the paint finish and the preferred worktop are open responses; the scheme lists typical examples.'),
}
SCHEME_PAGES = {'1': [4, 5, 18], '2': [6, 19], '3': [7, 20], '4': [8, 9, 21], '5': [9, 10, 22], '6': [10, 11, 23], '7': [11, 12, 24], '8': [13, 14, 15, 25], '9': [15, 16, 17, 26]}
D = cp.Draft(HERE, 2014, 'ordinary', ('c333950b806be0bf31dc1c1ef365236fabf05f83e5c38eeb306e4cf9a4e69d7b',
                                      '96b23fa46e5860d21c3a83f2c29f56e4e7f228bd6a1acbe799aec65d3c9ac47f'), 0, QUESTIONS, SCHEME_PAGES)
row, add, compose = D.row, D.add, D.compose
BAND8 = [0, 4, 6, 8]


def parts(*cards):
    return D.parts(*[(letter, c['questionText']) for letter, c in zip('abc', cards)])


def quality(verbatim, what='the sketches', rid='presentation'):
    return row(rid, verbatim, 8, f'Quality of {what}: excellent 8, good 6, fair 4.', BAND8)


D.figures({
    'q1-original': D.paper(2, [30, 39, 580, 228]), 'q2-original': D.paper(2, [30, 230, 580, 422]),
    'q3-original': D.paper(2, [30, 424, 580, 627]), 'q4-original': D.paper(2, [30, 629, 580, 790]),
    'q5-original': D.paper(3, [30, 39, 580, 190]), 'q6-original': D.paper(3, [30, 192, 580, 337]),
    'q7-original': D.paper(3, [30, 339, 580, 508]), 'q8-original': D.paper(3, [30, 510, 580, 590]),
    'q9-original': D.paper(3, [30, 592, 580, 790]),
    'q1-scheme': D.composite((4, [25, 45, 580, 722]), (5, [25, 45, 580, 775])),
    'q2-fixing': D.scheme(6, [25, 45, 580, 296]), 'q2-finish': D.scheme(6, [25, 296, 580, 616]), 'q2-advantages': D.scheme(6, [25, 616, 580, 775]),
    'q3-system': D.scheme(7, [25, 45, 580, 513]), 'q3-solar': D.scheme(7, [25, 513, 580, 690]),
    'q4-partition': D.scheme(8, [25, 45, 580, 280]), 'q4-socket': D.scheme(8, [25, 280, 580, 543]),
    'q4-skim': D.composite((8, [25, 543, 580, 785]), (9, [25, 45, 580, 240])),
    'q5-scheme': D.composite((9, [25, 258, 580, 760]), (10, [25, 45, 580, 376])), 'q5-vent': D.scheme(10, [25, 376, 580, 440]),
    'q6-signs': D.scheme(10, [25, 455, 580, 630]), 'q6-reasons': D.composite((10, [25, 630, 580, 775]), (11, [25, 45, 580, 250])),
    'q6-visitors': D.scheme(11, [25, 252, 580, 490]),
    'q7-collection': D.composite((11, [25, 500, 580, 775]), (12, [25, 45, 450, 196]), (12, [450, 100, 580, 297])), 'q7-uses': D.composite((12, [25, 196, 450, 297]), (12, [25, 297, 580, 515])),
    'q7-meter': D.scheme(12, [25, 515, 580, 775]),
    'q8-terms': D.composite((13, [25, 45, 580, 775]), (14, [25, 45, 580, 775]), (15, [25, 45, 580, 340])),
    'q9-layout': D.scheme(15, [25, 352, 580, 790]), 'q9-paint': D.composite((16, [25, 45, 580, 360]), (16, [25, 360, 450, 460]), (16, [450, 360, 580, 522])),
    'q9-worktop': D.composite((16, [25, 460, 450, 533]), (16, [25, 533, 580, 775]), (17, [25, 45, 580, 350])),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p18 (printed 15): (a) best 9 of 13 listed details × 4 = 36, four typical dimensions 4 = 40; (b) bridging 2, and draughting, accuracy and scale 8 (8/6/4) printed after it = 10. Complete 50.'
S1 = 'One required section and one required method to prevent twisting. The best-nine detail list is a marking menu, not a printed choice.'
A1 = add('1', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the external wall and the first floor. The section should show the typical construction details from a level 300 mm below the plasterboard ceiling, through the wall, joists and floor, to a level 400 mm above the finished floor. Include four typical dimensions on your drawing. Show 1.0 metre width of floor.',
         [row('details', 'Any 9 of the above details ( 4 marks each)', 36, 'Credit the best NINE acceptable details at 4 marks each, capped at 36. Marked details: external render 19 mm; external leaf solid block 100 mm; 150 mm full-fill cavity insulation; cavity ties; internal leaf solid block 100 mm; internal plaster 15 mm; skirting board; floating tongued and grooved hardwood floor; acoustic or adhesive layer for fixing the floor boards; plywood deck 20 mm; adhesive tape to the wall and plywood; floor joists 225 × 40 mm; plasterboard taped to the wall and plaster skim.', list(range(0, 37, 4))),
          row('dimensions', 'Four typical dimensions', 4, 'Four appropriate typical dimensions on the section, 1 each.')],
         ['cons-1-5', 'cons-3-3', 'cons-4-3'], ['question-one-drawing-questions', 'foundations-floors-walls'], 'q1-scheme',
         'Scaled drawing (1.5) of a cavity wall (3.3) and timber upper floor (4.3).', B1, S1)
B1b = add('1', 'b', '(b)', 'On your drawing show one method to prevent the floor joists from twisting.',
          [row('bridging', 'Bridging', 2, 'Show and identify the bridging, as in the scheme: herringbone bridging, 50 × 40 mm or proprietary metal bridging, or solid bridging, 225 × 40 mm.', [0, 2]),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the whole section: excellent 8, good 6, fair 4. The scheme prints this band after the part (b) row.', BAND8)],
          ['cons-4-3'], ['foundations-floors-walls'], 'q1-scheme', 'Strutting of a timber upper floor (4.3).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-scheme', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p19 (printed 16): (a) two descriptions × 4, type of insulation 4 and quality of sketches 8 (8/6/4) = 20; (b) two steps × 4, finish 4 and quality of sketches 8 (8/6/4) = 20; (c) two advantages × 5 = 10. Complete 50.'
S2 = '"one method" in (a) is an open choice of method; the scheme gives a typical method.'
A2 = add('2', 'a', '(a)', 'Using notes and freehand sketches show one method of fixing the insulation to the solid block wall of the extension. Specify the insulation material to be used.',
         [row('description-1', 'Valid description one', 4, 'Such as: a stainless steel base track fixed to the wall at DPC level carries the first row of boards; the boards are fixed with a special adhesive.'),
          row('description-2', 'Valid description two', 4, 'A second, different step. Such as: the next rows fixed in a staggered pattern; mechanical fixings, typically seven per square metre, drilled through the insulation into the wall and hammered home.'),
          row('insulation', 'Type of insulation', 4, 'Such as: polystyrene; mineral fibre board; phenolic foam.'),
          quality('Quality of sketches (excellent, good, fair)')],
         ['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q2-fixing',
         'Insulating materials (6.2) fixed to a solid external wall (3.3).', B2, S2)
B2b = add('2', 'b', '(b)', 'Using notes and freehand sketches show the steps involved in applying a reinforced mesh and an external surface finish to the insulation.',
          [row('step-1', 'Valid step one', 4, 'Such as: the indent at each fixing filled with base coat; a base coat of acrylic plaster applied to the insulation.'),
           row('step-2', 'Valid step two', 4, 'A second, different step. Such as: the reinforcing mesh pressed into the wet base coat, and around the openings; a further base coat or primer before the finish.'),
           row('finish', 'Valid finish', 4, 'Such as: a final acrylic finish applied with a steel trowel over a complete area, without breaks; a proprietary finish in a range of colours.'),
           quality('Quality of sketches (excellent, good, fair)')],
          ['cons-6-2', 'cons-3-2'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q2-finish',
          'External insulation (6.2) finishing the external envelope (3.2).', B2, S2)
C2 = add('2', 'c', '(c)', 'List two advantages of improving the insulation properties of the external wall of the extension.',
         [row('advantage-1', 'Advantage one', 5, 'Such as: less heat loss; lower energy bills; lower CO₂ emissions.'),
          row('advantage-2', 'Advantage two', 5, 'A second, different advantage. Such as: a better U-value and BER; a warmer house; no loss of internal floor area; the household is not disturbed, as the work is outside.')],
         ['cons-6-3', 'cons-6-2'], ['heat-loss-insulation'], 'q2-advantages', 'Heat loss and running costs (6.3) with insulation (6.2).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-fixing', B2, S2, parts(A2, B2b, C2))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p20 (printed 17): (a) best 9 of 16 listed details × 4 = 36 and quality of sketch 8 (8/6/4) = 44; (b) two advantages × 3 = 6. Complete 50.'
S3 = 'The printed component list is required content, not a choice; the best-nine list is a marking menu.'
A3 = add('3', 'a', '(a)', 'A modern wood burning stove, as shown in the sketch, is fitted with a back boiler. The back boiler is connected to an indirect cylinder to provide hot water for a dwelling house. Using a single-line labelled diagram, show the pipework necessary to supply hot water to the kitchen sink. Include the following on your diagram: water storage tank and overflow pipe; rising main; stove and back boiler; hot water cylinder and pipework; location of all necessary valves. On your diagram, show the insulation to the water storage tank and to all the pipework.',
         [row('details', 'Any 9 of the above details (4 marks each)', 36, 'Credit the best NINE acceptable details at 4 marks each, capped at 36. Secondary circulation: rising main; cold water storage tank and ball valve; overflow; cold feed from storage to the indirect cylinder; indirect hot water cylinder; expansion pipe from the cylinder; supply to the sink. Primary circulation: supply to the expansion tank; expansion tank and ball valve; overflow; cold water feed and primary return; wood burning stove and back boiler; expansion pipe and primary flow; valves; insulation to the storage tank and pipework; labelling.', list(range(0, 37, 4))),
          quality('Quality of sketch (excellent, good, fair)', 'the sketch')],
         ['cons-5-2', 'cons-5-3'], ['hot-water-space-heating'], 'q3-system', 'Hot water systems and cylinders (5.2) heated by a stove (5.3).', B3, S3)
B3b = add('3', 'b', '(b)', 'Discuss two advantages of adding a solar panel to supply hot water to a dwelling house.',
          [row('advantage-1', 'Advantage one', 3, 'Such as: lower costs of heating water; free solar energy once the panels are bought and installed.'),
           row('advantage-2', 'Advantage two', 3, 'A second, different advantage. Such as: environmentally friendly and sustainable; less use of the boiler, as the water is not heated from cold; usable in remote areas off the grid.')],
          ['cons-6-4', 'cons-6-3'], ['planning-sustainability-environment', 'heat-loss-insulation'], 'q3-solar', 'Solar heat gain (6.4) and running costs (6.3).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-system', B3, S3, parts(A3, B3b))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p21 (printed 18): (a) three construction details × 4, typical dimensions 4 and quality of sketch 8 (8/6/4) = 24; (b) socket detail 6; (c) three details × 4 and quality of sketches 8 (8/6/4) = 20. Complete 50.'
S4 = '"one method" in (b) is an open choice of method; the scheme gives a metal socket box and a dry lining back box.'
A4 = add('4', 'a', '(a)', 'Using notes and freehand sketches show the typical construction details of the timber stud partition. Name the main components and give their typical dimensions.',
         [row('detail-1', 'Valid construction detail one', 4, 'Such as: a sole piece or base plate, 75 × 50 or 100 × 50 mm.'),
          row('detail-2', 'Valid construction detail two', 4, 'A second, different detail. Such as: studs at 400 mm centres; noggings or bridging for stability; a head plate.'),
          row('detail-3', 'Valid construction detail three', 4, 'A third, different detail. Such as: a fixing piece for electrical services; insulation between the studs; plasterboard 2400 × 1200 × 12.5 mm fixed with zinc-coated nails or screws, and a plaster skim.'),
          row('dimensions', 'Typical dimensions', 4, 'Typical dimensions for the named components, as in the scheme’s list.'),
          quality('Quality of sketch (excellent, good, fair)', 'the sketch')],
         ['cons-4-5'], ['windows-doors'], 'q4-partition', 'Stud partitions (4.5).', B4, S4)
B4b = add('4', 'b', '(b)', 'Show one method of fixing a double electrical socket in the stud partition.',
          [row('detail', 'Valid detail', 6, 'Such as: a metal socket box fixed to a batten set back between the studs so the box is flush with the studs, the plasterboard marked and cut out with a pad saw; or a dry lining back box fitted to a cut-out in the plasterboard, its side clips gripping the board as the screws are tightened.')],
          ['cons-5-8', 'cons-4-5'], ['services-water-gas-electrical', 'windows-doors'], 'q4-socket', 'Domestic electrical installation (5.8) in a stud partition (4.5).', B4, S4)
C4 = add('4', 'c', '(c)', 'Using notes and freehand sketches, show the steps involved in applying a plaster skim finish to one side of the stud partition.',
         [row('detail-1', 'Valid detail one', 4, 'Such as: sheeting over the floor; the joints taped and the partition sealed to the walls and ceiling; plaster added to water in a clean bucket and mixed free of lumps.'),
          row('detail-2', 'Valid detail two', 4, 'A second, different step. Such as: the plaster spread from the hawk with a trowel in smooth strokes, 1 to 2 mm thick, and levelled while soft; a second coat.'),
          row('detail-3', 'Valid detail three', 4, 'A third, different step. Such as: left until firm, then polished with a wet trowel in sweeping strokes for a fine finish; the tools washed at once.'),
          quality('Quality of sketches (excellent good fair)')],
         ['cons-4-1'], ['foundations-floors-walls'], 'q4-skim', 'Wall finishes (4.1).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-partition', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p22 (printed 19): (a) best 6 of 11 listed details × 6 = 36, three typical dimensions 3 = 39; (b) ventilation detail 3, and draughting, accuracy and scale 8 (8/6/4) printed after it = 11. Complete 50.'
S5 = 'One required section and one required ventilation method. The best-six detail list is a marking menu, not a printed choice.'
A5 = add('5', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the portion of the roof at the ridge. Show the typical construction details from the top of the ridge to a level 150 mm below the collar ties. Include the ridge tile and three courses of tiles at the ridge. Label the roof components and include three typical dimensions.',
         [row('details', 'Any 6 of the above details (6 marks each)', 36, 'Credit the best SIX acceptable details at 6 marks each, capped at 36. Marked details: ridge tile; ridge vent; ridge board 300 × 32 mm; tiles; battens 50 × 30 mm; vapour barrier or vapour diffusion membrane; rafters 200 × 50 mm; collar tie 150–200 × 50 mm; insulation; plasterboard; labelling.', list(range(0, 37, 6))),
          row('dimensions', 'Three typical dimensions', 3, 'Three appropriate typical dimensions on the section, 1 each.')],
         ['cons-1-5', 'cons-3-8', 'cons-3-9'], ['question-one-drawing-questions', 'roofs'], 'q5-scheme',
         'Scaled drawing (1.5) of a cut roof (3.8) and its tiled covering (3.9).', B5, S5)
B5b = add('5', 'b', '(b)', 'On your drawing, show one method of ventilating the roof structure.',
          [row('ventilation', 'Valid design detail', 3, 'Such as: ridge vents fitted on the ridge; vent tiles fitted near the ridge.'),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the whole section: excellent 8, good 6, fair 4. The scheme prints this band after the part (b) row.', BAND8)],
          ['cons-3-9', 'cons-6-5'], ['roofs', 'wood-rot-ventilation'], 'q5-vent', 'Ventilating the roof covering (3.9, 6.5).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-scheme', B5, S5, parts(A5, B5b))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p23 (printed 20): (a) three signs, quality of sketch 8 (8/6/4) each = 24; (b) one reason for each item × 4 = 12; (c) two reasons × 7 = 14. Complete 50.'
S6 = 'All three printed items are required in (a) and (b), each separately marked; not a choice.'
SITE = (['cons-1-8'], ['site-safety'])
A6 = add('6', 'a', '(a)', 'For each of the following, draw the particular safety sign to indicate that the following personal protective equipment (ppe) must be worn on a construction site: safety helmet; high visibility vest; safety boots.',
         [row(rid, f'{item} Quality of sketch (excellent good fair)', 8, f'The mandatory blue sign for the {item.lower()}, as in the scheme: quality of the sketch, excellent 8, good 6, fair 4.', BAND8)
          for rid, item in [('helmet', 'Safety helmet'), ('vest', 'High visibility vest'), ('boots', 'Safety boots')]],
         *SITE, 'q6-signs', 'Safety signs on site (1.8).', B6, S6)
B6b = add('6', 'b', '(b)', 'State one reason why each item of personal protective equipment listed at 6(a) above must be worn on a building site.',
          [row('helmet', 'Safety helmet', 4, 'Such as: it protects the head from falling objects, or from striking a solid object; mandatory for workers and visitors.'),
           row('vest', 'High visibility vest', 4, 'Such as: workers are clearly visible on site, especially to machinery operators; mandatory for workers and visitors.'),
           row('boots', 'Safety boots', 4, 'Such as: the steel cap protects the feet from falling objects; mandatory for workers and visitors.')],
          *SITE, 'q6-reasons', 'Personal protective equipment on site (1.8).', B6, S6)
C6 = add('6', 'c', '(c)', 'Discuss two reasons why visitors must report to the site office on entering a construction site.',
         [row('reason-1', 'Valid reason one', 7, 'Such as: management must know who is on site at any one time, in case of an accident; arrival and departure must be recorded.'),
          row('reason-2', 'Valid reason two', 7, 'A second, different reason. Such as: visitors collect a vest, helmet and boots and are told the safety requirements; a guide takes them round, as parts of the site may be closed to them.')],
         *SITE, 'q6-visitors', 'Safety precautions on site (1.8).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-signs', B6, S6, parts(A6, B6b, C6))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p24 (printed 21): (a) three details × 6 and quality of sketches 8 (8/6/4) = 26; (b) two advantages × 4 and two uses × 4 = 16; (c) one advantage 4 and one disadvantage 4 = 8. Complete 50.'
S7 = 'The collection method in (a) is an open response; the scheme gives an underground storage tank and a water butt.'
A7 = add('7', 'a', '(a)', 'Using notes and freehand sketches, show how the rainwater could be collected from the roof and stored for reuse.',
         [row('detail-1', 'Valid detail one', 6, 'Such as: rainwater from the roof flows into the gutter and down the downpipe to a gully, or is diverted into a water butt.'),
          row('detail-2', 'Valid detail two', 6, 'A second, different detail. Such as: a filter between the gully and the underground storage tank traps sediment and is accessible for cleaning; the butt has a tap near the bottom and sits on a stand.'),
          row('detail-3', 'Valid detail three', 6, 'A third, different detail. Such as: a submersible pump lifts the water to the attic tank under a control unit, topped up from the mains when rainwater is low; the stored water is reused as grey water only.'),
          quality('Quality of sketches (excellent good fair)')],
         ['cons-5-4', 'cons-1-2'], ['drainage', 'planning-sustainability-environment'], 'q7-collection',
         'Rainwater from the gutters and downpipes (5.4) reused sustainably (1.2).', B7, S7)
B7b = add('7', 'b', '(b)', 'List two advantages of storing rainwater and suggest two suitable uses for the stored rainwater.',
          [row('advantage-1', 'Advantage one', 4, 'Such as: lower water bills where meters are installed; free of many chemicals in ground water; an independent supply.'),
           row('advantage-2', 'Advantage two', 4, 'A second, different advantage. Such as: supplements the mains; water in a drought; large stores reduce flooding; less demand on wells.'),
           row('use-1', 'Suitable use one', 4, 'Such as: flushing toilets; washing clothes or cars.'),
           row('use-2', 'Suitable use two', 4, 'A second, different use. Such as: the garden; agriculture and livestock; irrigation; any use where non-drinking water is suitable.')],
          ['cons-1-2', 'cons-5-2'], ['planning-sustainability-environment', 'services-water-gas-electrical'], 'q7-uses',
          'Sustainable water use (1.2) in the cold water supply (5.2).', B7, S7)
C7 = add('7', 'c', '(c)', 'Discuss one advantage and one disadvantage of fitting a water meter to the mains water supply of a dwelling house.',
         [row('advantage', 'One advantage', 4, 'Such as: encourages users to conserve water and fit water-saving devices; helps detect leaks; people pay for exactly what they use.'),
          row('disadvantage', 'One disadvantage', 4, 'Such as: paying for water that was once free; meters need maintenance; the cost of buying and installing them; difficult or unfair in apartment blocks.')],
         ['cons-5-1', 'cons-5-2'], ['services-water-gas-electrical'], 'q7-meter', 'The water service entry (5.1) and supply (5.2).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-collection', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p25 (printed 22): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination. No pre-audit card existed for this question.'
TERMS = [
    ('strip foundation', 'Strip Foundation', ['cons-2-4'], ['foundations-floors-walls'],
     'a simple, common and economical concrete foundation, reinforced with steel bars, supporting a solid or cavity wall centrally; typically three times the wall thickness wide and as thick as the wall; the load spreads at 45 degrees to the ground.', 'Strip foundations (2.4).'),
    ('housing joint', 'Housing joint', ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'],
     'a basic joint joining two pieces at right angles: a trench removed from one piece takes the other, glued for strength; used in cabinets, bookcases and shelving; simple, strong and easy to make.',
     'Joints (10.1) and the choice of joint (10.4). The Ordinary reference taxonomy has no joinery heading; the term keeps the Wood, Rot & Ventilation association used for joinery, and 10.1/10.4 are declared outside that heading’s crosswalk.'),
    ('laser beam', 'Laser beam', ['cons-10-7'], ['wood-rot-ventilation'],
     'a light beam used in printers, cutting and welding and barcode scanning; on site a laser projector sends out the beam and a staff with an adjustable sensor detects it, giving levels at different points on the site or on internal walls.', 'Measuring for accuracy (10.7).'),
    ('thermostatic valve', 'Thermostatic Valve', ['cons-5-3'], ['hot-water-space-heating'],
     'a valve fitted to a radiator in a central heating system, controlling its heat output to give the desired room temperature; inexpensive, it reduces heating costs and CO₂ emissions.', 'Temperature control of heating systems (5.3).'),
    ('collar tie', 'Collar tie', ['cons-3-8'], ['roofs'],
     'a member in tension stretching from rafter to rafter, tying them into a triangle for structural stability; purlins may rest on it; typically 200 × 50 mm; it may form the ceiling in an attic conversion.', 'Roof forms (3.8).'),
    ('radon sump', 'Radon sump', ['cons-4-2', 'cons-3-4'], ['foundations-floors-walls'],
     'a compartment placed centrally in the hardcore under the ground floor to collect radon gas through gaps in its walls; pipes from its connectors carry the gas outside the building, where it dissipates.', 'Ground floors (4.2) and radon protection beneath them (3.4).'),
    ('roof-light window', 'Roof-light window', ['cons-3-5', 'cons-3-6'], ['windows-doors'],
     'a window fitted in a sloping roof (or a special roof light for a flat roof), letting light and ventilation into an attic; double or triple glazed and highly insulated, fitting neatly into the roof surface; top or pivot hung.', 'Window types (3.5) and glazing (3.6).'),
    ('smart meter', 'Smart meter', ['cons-5-8'], ['services-water-gas-electrical'],
     'records the electricity used in the home and shows its cost at any time, giving the householder control; may be topped up with credit; can also record gas or water.', 'Domestic electrical installation (5.8).'),
    ('external ramp', 'External ramp', ['cons-1-2'], ['planning-sustainability-environment'],
     'a sloping path for easy access for people with restricted mobility, wheelchairs and buggies: gradient 1:20, sections no longer than 9.0 m, at least 1200 mm clear width, non-slip, lit from the sides.', 'Inclusive design of the built environment (1.2).'),
]
Q8 = add('8', 'terms', '', 'Explain, with the aid of notes and freehand sketches, any five of the following: ' + '; '.join(t[0] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Terms', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{t[1]}: {t[4]}' for t in TERMS),
               group=dict(claimMax=5, perOption=10, options=[t[1] for t in TERMS]))],
         list(dict.fromkeys(n for t in TERMS for n in t[2])), list(dict.fromkeys(a for t in TERMS for a in t[3])), 'q8-terms',
         'The union of the nine printed terms: ' + ' '.join(t[5] for t in TERMS), B8, S8)

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p26 (printed 23): (a) quality of sketch 8 (8/6/4) and sink, cooker and fridge reasons × 4 = 20; (b) two details × 4 and quality of sketches 8 (8/6/4) = 16; (c) granite and solid wood, advantage and disadvantage × 4, preferred worktop 2 and two reasons × 2 = 14. Complete 50.'
S9 = 'The locations, the paint finish and the preferred worktop are open responses; "one of the cabinet doors" names the door to be painted, not a choice.'
A9 = add('9', 'a', '(a)', 'Draw a freehand sketch of the given plan and on your sketch show your preferred location for each of the following: sink, cooker and fridge. Give reasons for selecting each location.',
         [quality('Quality of sketch (excellent good fair)', 'the sketch'),
          row('sink', 'Sink', 4, 'Such as: natural light and a view of the garden through the window; close to the cooker; worktop space at either side; part of the working triangle.'),
          row('cooker', 'Cooker', 4, 'Such as: worktop space at either side; no crossing the kitchen with hot pots; safe in relation to the door; within easy reach of the sink; an extractor on the external wall.'),
          row('fridge', 'Fridge', 4, 'Such as: close to the sink for food preparation; worktop space beside it to unpack shopping; part of the working triangle. Other suitable locations are accepted.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q9-layout', 'Kitchen layout in the built environment (1.2).', B9, S9)
B9b = add('9', 'b', '(b)', 'The kitchen cabinets are hand painted wooden cabinets. Describe, using notes and freehand sketches, the steps involved in preparing the wood and in applying a high quality hand painted finish to one of the cabinet doors.',
          [row('detail-1', 'Valid detail one', 4, 'Such as: the surface cleaned and sanded with fine glass paper; the dust removed with a clean cloth and white spirit.'),
           row('detail-2', 'Valid detail two', 4, 'A second, different step. Such as: a primer applied with a good brush, dried and lightly sanded; an undercoat, sanded; the final coat, and a second if needed; or a water-based all-in-one paint and a gloss or satin finish coat.'),
           quality('Quality of sketches (excellent good fair)')],
          ['cons-10-7'], ['wood-rot-ventilation'], 'q9-paint', 'Surface preparation and finishing of timber (10.7).', B9, S9)
C9 = add('9', 'c', '(c)', 'A choice is to be made between a polished granite worktop and a solid wood worktop. Discuss one advantage and one disadvantage of each worktop. Recommend a preferred worktop and give two reasons for your recommendation.',
         [row('granite', 'Granite worktop Advantage and disadvantage', 4, 'One advantage and one disadvantage. Such as: natural, elegant, hard wearing, heat and waterproof and low maintenance; but expensive, heavy, can chip or crack, needs sealing and has high embodied energy.'),
          row('wood', 'Solid worktop Advantage and disadvantage', 4, 'One advantage and one disadvantage. Such as: attractive and warm, absorbs sound, easily cut and replaced, low embodied energy; but stains easily, must be oiled and maintained, and needs protection from hot items.'),
          row('preferred', 'Preferred worktop', 2, 'Granite or wood.'),
          row('reason-1', 'Reason one', 2, 'A reason for the recommendation.'),
          row('reason-2', 'Reason two', 2, 'A second, different reason.')],
         ['cons-10-7', 'cons-1-2'], ['wood-rot-ventilation', 'planning-sustainability-environment'], 'q9-worktop',
         'Finishing and care of a timber surface (10.7) against a material choice for the built environment (1.2).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-layout', B9, S9, parts(A9, B9b, C9))

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and three other questions (200 marks); all question banks retained, no full-exam Cartesian cards.'),
          (3, 'any five', 'Q8 closed choose-five of nine printed terms: one card with an any-five group over all nine terms (choice is not a route).'),
          (3, 'one of', 'Q9(b) "one of the cabinet doors": the door to be painted, not a candidate choice.')]
FINITE = {'8': dict(choose=5, options=[t[1] for t in TERMS], cardId=Q8['id'], groupRowId='terms', wholeQuestionMarks=50, termMarks=10)}
GAPS = [dict(cardId=C4['id'], canonicalTopicIds=['cons-4-1'], atlasTopicId=D.CROSS + 'foundations-floors-walls',
             reason='No Ordinary outgoing reference heading covers internal wall finishes (4.1); the card keeps the Foundations, Floors & Walls association.'),
        dict(cardId=Q8['id'], canonicalTopicIds=['cons-10-1', 'cons-10-4'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers joinery (10.1, 10.4, housing joint).')]
D.finish(LEDGER, FINITE, {}, taxonomy_gaps=GAPS, whole_choices={'q8-terms'})
