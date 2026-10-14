"""Draft the 2018 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 18-26). Q8 "any five of nine" was never carded: it is added as ONE card with an any-five group
(choice is not a route). The 19 pre-audit 2018 Ordinary cards keep their IDs and concept IDs and are
corrected in place; the Q9(c) advantage and disadvantage keep their cards and (c) composes them.
Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Internal wall, door, strip foundation and ground floor section', concept='internal-wall-door-floor-section',
              stem='A 215 mm solid concrete block wall separates two rooms on the ground floor of a dwelling house, as shown. A strip foundation supports the wall, which is plastered on both sides. A flush panel door, 60 mm in thickness, is fixed in the wall. The doorframe is 120 mm × 50 mm. The insulated concrete ground floor is finished with a 20 mm tongue and groove floating hardwood floor.',
              note='Original sketch and specification retained. The scheme prints the draughting, accuracy and scale band after the part (b) row, so it is marked with the radon detail.'),
    '2': dict(page=2, title='External insulation of a hollow block wall', concept='external-wall-insulation',
              stem='The external wall of a house built in the 1960s is of 215 mm single-leaf hollow block construction. The wall is plastered on both sides, as shown. It is proposed to improve the insulation properties of the house by fixing an external system of expanded polystyrene to the wall.',
              note='Original sketch retained. The method, the finish and the advantage and disadvantage are open responses; the scheme lists typical examples.'),
    '3': dict(page=2, title='Hot water to a shower from a stove back boiler', concept='stove-hot-water-shower', stem='',
              note='Original sketch retained. The listed components are required content, not a choice; the best-seven list is a marking menu.'),
    '4': dict(page=3, title='Setting out a strip foundation', concept='strip-foundation-setting-out',
              stem='The sketch shows one corner of a strip foundation for the external wall of a dwelling house. The external wall is to be a 400 mm concrete block wall with a full-fill insulated cavity.',
              note='Original sketch retained. All three printed headings in (b) are required, each separately marked.'),
    '5': dict(page=3, title='Flat roof eaves and cavity wall section', concept='flat-roof-eaves-section',
              stem='The sketch shows portion of the eaves of a flat roof. The roof is covered with layers of bituminous felt, on a 20 mm plywood deck, on battens, on sloping firring pieces, on 200 mm × 50 mm joists. The roof is highly insulated and there is an insulated plasterboard ceiling beneath. The external wall supporting the roof is a 400 mm concrete block wall with a full-fill insulated cavity. The wall is rendered on both sides.',
              note='Original sketch and specification retained. The scheme prints the draughting, accuracy and scale band after the part (b) row, so it is marked with the ventilation detail.'),
    '6': dict(page=3, title='PPE safety signs and design features', concept='ppe-signs-features', stem='',
              note='Original sketch retained. All three printed PPE items in (a) and (b) are required, each separately marked.'),
    '7': dict(page=4, title='Rainwater harvesting to an underground tank', concept='rainwater-harvesting',
              stem='It is proposed to collect rainwater from the roof of a house and to store it in an underground tank as shown.',
              note='Original sketch retained. The layouts are open responses; the scheme gives model sketches.'),
    '8': dict(page=4, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=4, title='Glazed double doors in an internal opening', concept='glazed-double-doors',
              stem='The sketch shows an existing opening in a 100 mm concrete block wall separating a sitting room and a dining room. It is proposed to fit a doorframe and glazed wooden double doors in this opening.',
              note='Original sketch retained. Part (c) requires both one advantage and one disadvantage, each separately marked.'),
}
SCHEME_PAGES = {'1': [4, 18], '2': [5, 6, 19], '3': [6, 7, 20], '4': [7, 8, 9, 21], '5': [9, 10, 22], '6': [10, 11, 12, 23], '7': [12, 13, 24], '8': [13, 14, 15, 25], '9': [16, 17, 26]}
D = cp.Draft(HERE, 2018, 'ordinary', ('ed26d3fbdb863826bd485e22ece6b7aeabc53e70ff7dce447d623b75c98352c3',
                                      '7344fc028e7e7588c55886d87002958a42fe5b79a47980256560228d44000f9c'), 19, QUESTIONS, SCHEME_PAGES)
row, add, compose = D.row, D.add, D.compose
BAND8 = [0, 4, 6, 8]
BAND6 = [0, 2, 4, 6]


def parts(*cards):
    return D.parts(*[(letter, c['questionText']) for letter, c in zip('abc', cards)])


D.figures({
    'q1-original': D.paper(2, [35, 39, 580, 300]), 'q2-original': D.paper(2, [35, 305, 580, 556]),
    'q3-original': D.paper(2, [35, 565, 580, 775]), 'q4-original': D.paper(3, [35, 39, 580, 278]),
    'q5-original': D.paper(3, [35, 280, 580, 563]), 'q6-original': D.paper(3, [35, 570, 580, 783]),
    'q7-original': D.paper(4, [35, 39, 580, 336]), 'q8-original': D.paper(4, [35, 345, 580, 482]),
    'q9-original': D.paper(4, [35, 490, 580, 760]),
    'q1-scheme': D.scheme(4, [25, 50, 580, 692]),
    'q2-method': D.scheme(5, [25, 50, 580, 430]), 'q2-finish': D.scheme(5, [25, 430, 580, 710]), 'q2-advantages': D.scheme(6, [25, 50, 580, 390]),
    'q3-system': D.composite((6, [25, 390, 580, 765]), (7, [25, 50, 580, 313])), 'q3-stove': D.scheme(7, [25, 313, 580, 517]),
    'q4-environment': D.scheme(7, [25, 517, 580, 770]), 'q4-setting-out': D.scheme(8, [25, 50, 580, 677]), 'q4-level': D.scheme(9, [25, 50, 580, 230]),
    'q5-scheme': D.composite((9, [25, 230, 580, 765]), (10, [25, 30, 580, 517])),
    'q6-signs': D.scheme(10, [25, 517, 580, 750]), 'q6-features': D.scheme(11, [25, 50, 580, 730]), 'q6-other': D.scheme(12, [25, 50, 580, 450]),
    'q7-collection': D.scheme(12, [25, 450, 580, 730]), 'q7-pumping': D.scheme(13, [25, 50, 580, 420]), 'q7-advantage': D.scheme(13, [25, 420, 580, 577]),
    'q8-terms': D.composite((13, [25, 577, 580, 780]), (14, [25, 50, 580, 745]), (15, [25, 50, 580, 783])),
    'q9-support': D.scheme(16, [25, 50, 580, 297]), 'q9-frame': D.scheme(16, [25, 297, 580, 703]), 'q9-glazed': D.scheme(17, [25, 50, 580, 386]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p18 (printed 16): (a) best 7 of 13 listed details × 5 = 35, three typical dimensions 3 = 38; (b) radon barrier overlapped, taped and sealed 4, and draughting, accuracy and scale 8 (8/6/4) printed after it = 12. Complete 50.'
S1 = 'One required section and one required radon detail. The best-seven detail list is a marking menu, not a printed choice.'
A1 = add('1', 'a', '(a)', 'To a scale of 1:5 draw a vertical section through the strip foundation, the 215 mm wall, the ground floor and the centre of the door up to a point 500 mm above finished floor level. Show 600 mm width of floor on each side of the wall and include three typical dimensions on your drawing.',
         [row('details', 'Any 7 of the above details ( 5 marks each)', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: 15 mm internal plaster with skim coat; 120 × 50 mm doorframe; 60 mm flush panel door; 65 × 15 mm architrave and 100 × 15 mm skirting; 20 mm floating hardwood floor; 100 mm smooth concrete floor; 250 mm floor insulation with thermal blocks; 200 mm concrete sub-floor; radon barrier; 30 mm sand blinding; 200 mm hardcore; reinforced concrete foundation; 215 mm block wall.', list(range(0, 36, 5))),
          row('dimensions', 'Any three typical dimensions', 3, 'Three appropriate typical dimensions on the section, 1 each.')],
         ['cons-1-5', 'cons-2-4', 'cons-4-2', 'cons-3-7'], ['question-one-drawing-questions', 'foundations-floors-walls', 'windows-doors'], 'q1-scheme',
         'Scaled drawing (1.5) of a strip foundation (2.4) and insulated ground floor (4.2) under an internal wall with a door (3.7).', B1, S1)
B1b = add('1', 'b', '(b)', 'Show on your drawing the typical design detailing to prevent radon gas from entering the rooms through the floor.',
          [row('radon', 'Radon barrier overlapped, taped and sealed', 4, 'Show and identify a continuous radon barrier under the floor with every joint overlapped, taped and sealed, as in the scheme’s model section.', [0, 4]),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the whole section: excellent 8, good 6, fair 4. The scheme prints this band after the part (b) row.', BAND8)],
          ['cons-3-4', 'cons-4-2'], ['foundations-floors-walls'], 'q1-scheme', 'Damp proof and radon membranes (3.4) in a solid ground floor (4.2).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-scheme', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p19 (printed 17): (a) two valid descriptions × 4, thickness 4 and quality of sketch 8 (8/6/4) = 20; (b) two valid steps × 4, surface finish 4 and quality of sketch 8 (8/6/4) = 20; (c) advantage 5, disadvantage 5 = 10. Complete 50.'
S2 = '"one suitable method" is an open choice with no printed list; each part stays one response. Part (c) requires both the advantage and the disadvantage.'
WALL = (['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls'])
A2 = add('2', 'a', '(a)', 'Using notes and freehand sketches show one suitable method of applying an external insulation system to the wall. Specify the typical thickness of the insulation.',
         [row('description-1', 'Valid description one', 4, 'Such as: a stainless-steel track fixed to the wall at DPC level, the first row of boards resting on it, fixed with a proprietary adhesive.'),
          row('description-2', 'Valid description two', 4, 'A second, different step. Such as: further rows staggered; stainless steel fixings drilled through each board into the wall, about seven per square metre.'),
          row('thickness', 'Thickness of insulation', 4, 'Such as: a minimum of 200 mm.'),
          row('presentation', 'Quality of sketch (excellent, good, fair)', 8, 'Quality of the sketch: excellent 8, good 6, fair 4.', BAND8)],
         *WALL, 'q2-method', 'Insulating materials (6.2) on an external wall (3.3).', B2, S2)
B2b = add('2', 'b', '(b)', 'On your sketch show clearly the steps to be followed in applying a surface finish to the insulation. Specify the materials to be used for the surface finish.',
          [row('step-1', 'Valid step one', 4, 'Such as: the fixing heads filled with base coat; a base coat of acrylic plaster applied to the insulation.'),
           row('step-2', 'Valid step two', 4, 'A second, different step. Such as: reinforcing mesh pressed into the wet plaster, also around openings; a further coat before the finish.'),
           row('finish', 'Surface finish', 4, 'Such as: a final acrylic coat applied with a steel trowel, in a range of colours; proprietary finishes such as brick effect.'),
           row('presentation', 'Quality of sketch (excellent, good, fair)', 8, 'Quality of the sketch: excellent 8, good 6, fair 4.', BAND8)],
          *WALL, 'q2-finish', 'Finishing external insulation (6.2) on the wall (3.3).', B2, S2)
C2 = add('2', 'c', '(c)', 'Discuss one advantage and one disadvantage of applying an external system of insulation to the walls of a house.',
         [row('advantage', 'Advantage', 5, 'Such as: lower energy bills and heat loss; a better BER and U-value; no loss of internal floor area; an improved appearance.'),
          row('disadvantage', 'Disadvantage', 5, 'Such as: expensive; window cills, downpipes, fascia and soffit may need altering; the finish needs maintenance.')],
         ['cons-6-2', 'cons-6-3'], ['heat-loss-insulation'], 'q2-advantages', 'Insulation (6.2) and running costs (6.3).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-method', B2, S2, parts(A2, B2b, C2))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p20 (printed 18): (a) best 7 of 11 listed items × 5 = 35 and quality of sketch 8 (8/6/4) = 43; (b) one advantage 7. Complete 50.'
S3 = 'The printed component list is required content, not a choice; the best-seven list is a marking menu.'
HEAT = (['cons-5-2', 'cons-5-3'], ['hot-water-space-heating'])
A3 = add('3', 'a', '(a)', 'A wood-burning stove with a back boiler, as shown, is used to heat water for a dwelling house. Using a single-line labelled diagram, show the pipework required to supply hot water to a shower. Include the following in your diagram: wood-burning stove; rising main and cold water storage tank; hot water cylinder and expansion tank; pipework to shower and all necessary valves.',
         [row('items', 'Any 7 of the above details (5 marks each)', 35, 'Credit the best SEVEN acceptable items at 5 marks each, capped at 35. Secondary circulation: 15 mm rising main; storage tank and 22 mm overflow; 22 mm cold feed to the cylinder; hot water cylinder; 22 mm expansion pipe; 22 mm hot supply to the shower. Primary circulation: wood-burning stove; 28 mm primary flow and return; 22 mm cold feed and expansion pipe from the expansion tank; expansion tank and overflow; valves.', list(range(0, 36, 5))),
          row('presentation', 'Quality of sketch (excellent, good, fair)', 8, 'Quality of the diagram: excellent 8, good 6, fair 4.', BAND8)],
         *HEAT, 'q3-system', 'Hot water systems and cylinders (5.2) heated by a stove (5.3).', B3, S3)
B3b = add('3', 'b', '(b)', 'Discuss one advantage of using a wood-burning stove to heat water for the house.',
          [row('advantage', 'Advantage', 7, 'Such as: wood is renewable and less expensive; modern stoves are highly efficient; trees reabsorb the CO₂ released; it supplements other heating as fossil fuels dwindle.')],
          ['cons-5-3', 'cons-1-2'], ['hot-water-space-heating', 'planning-sustainability-environment'], 'q3-stove', 'Heating systems (5.3) and sustainable fuel (1.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-system', B3, S3, parts(A3, B3b))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p21 (printed 19): (a) two valid details × 5 = 10; (b) three printed headings, each primary communication 6 + other communication 4 = 30; (c) primary 6 + other 4 = 10. Complete 50.'
S4 = 'All three printed headings in (b) are required, each separately marked; not a choice.'
SETOUT = 'No Ordinary outgoing reference heading covers excavation (2.1); the card keeps the Foundations, Floors & Walls association.'
A4 = add('4', 'a', '(a)', 'Discuss one environmental reason why a strip foundation is considered the most suitable foundation for this house.',
         [row('detail-1', 'Valid detail one', 5, 'Such as: minimum ground area and excavation; less machinery and fuel.'),
          row('detail-2', 'Valid detail two', 5, 'A second, different detail of the reason. Such as: the least concrete, aggregate and steel; easy to set out, construct, fill and level.')],
         ['cons-2-2', 'cons-1-2'], ['foundations-floors-walls', 'planning-sustainability-environment'], 'q4-environment', 'Choice of foundation (2.2) for a lower environmental impact (1.2).', B4, S4)
B4b = add('4', 'b', '(b)', 'Using notes and freehand sketches describe how to set out the foundation trench under the following headings: profiles; width and depth of trench; position of wall on strip foundation.',
          [row('profiles', 'Profiles', 10, 'Primary communication 6 and other communication 4. Such as: two upright members with a horizontal cross rail; set out at the formation level from a secured datum, levelled with a laser or optical level.'),
           row('width-depth', 'Width and depth of trench', 10, 'Primary communication 6 and other communication 4. Such as: the 1200 mm trench width and 400 mm wall width marked on the profiles; a minimum 500 mm depth below the frost line, depending on the soil.'),
           row('wall-position', 'Position of wall on strip foundation', 10, 'Primary communication 6 and other communication 4. Such as: lines stretched between the profiles and plumbed down; the wall centred with equal projections on both sides.')],
          ['cons-2-4', 'cons-2-1'], ['foundations-floors-walls'], 'q4-setting-out', 'Setting out the excavation (2.1) for a strip foundation (2.4).', B4, S4)
C4 = add('4', 'c', '(c)', 'Using notes and freehand sketches, show how to determine the top surface of the foundation prior to placing the concrete to ensure that the foundation is level throughout.',
         [row('level', 'Show how to determine the top surface of the foundation prior to placing the concrete', 10, 'Primary communication 6 and other communication 4. Such as: pegs driven into the base of the trench, their tops set at the required foundation level with a laser level, with more pegs around the foundation.')],
         ['cons-2-4'], ['foundations-floors-walls'], 'q4-level', 'Strip foundations (2.4).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-setting-out', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p22 (printed 20): (a) best 7 of 12 listed details × 5 = 35, three typical dimensions 3 = 38; (b) soffit vents with air circulating through the battens 4, and draughting, accuracy and scale 8 (8/6/4) printed after it = 12. Complete 50.'
S5 = 'One required section and one required ventilation detail. The best-seven detail list is a marking menu, not a printed choice.'
A5 = add('5', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the eaves of the flat roof and through the external wall. Show the typical construction details from 500 mm below the roof joists, through the external wall, wallplate, fascia, soffit, and roof joists and include the roof surface. Show 1.5 metres length of roof joist and include three typical dimensions on your drawing.',
         [row('details', 'Any 7 of the above details (5 marks each)', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: three layers of bituminous felt; 18–25 mm marine plywood decking; 50 × 50 mm battens/counter battens and firring piece; 200 × 50 mm roof/ceiling joists; at least 200 mm roof insulation; 12.5 mm insulated plasterboard with skim; 100 × 75 mm wallplate and straps; 100 mm block inner leaf; full-fill cavity insulation and cavity closer; 100 mm block outer leaf; 15 mm plaster and 19 mm render; 25 mm fascia, 12 mm soffit and 100 mm gutter.', list(range(0, 36, 5))),
          row('dimensions', 'Any three typical dimensions', 3, 'Three appropriate typical dimensions on the section, 1 each.')],
         ['cons-1-5', 'cons-3-10', 'cons-3-3'], ['question-one-drawing-questions', 'roofs', 'foundations-floors-walls'], 'q5-scheme',
         'Scaled drawing (1.5) of a flat roof at the eaves (3.10) on a cavity wall (3.3).', B5, S5)
B5b = add('5', 'b', '(b)', 'On your drawing show how the roof is ventilated at the eaves.',
          [row('ventilation', 'Vents in soffit and air circulates through battens and counter battens', 4, 'Show and identify vents in the soffit with air circulating through the battens and counter battens, as in the scheme’s model section.', [0, 4]),
           row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the whole section: excellent 8, good 6, fair 4. The scheme prints this band after the part (b) row.', BAND8)],
          ['cons-3-10', 'cons-6-5'], ['roofs', 'wood-rot-ventilation'], 'q5-scheme', 'Ventilation (6.5) of a flat roof (3.10).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-scheme', B5, S5, parts(A5, B5b))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p23 (printed 21): (a) three printed signs, each quality of sketch 8 (8/6/4) = 24; (b) a design feature for each × 3 and quality of sketches 8 (8/6/4) = 17; (c) other PPE 4 and reason 5 = 9. Complete 50.'
S6 = 'All three printed PPE items in (a) and (b) are required, each separately marked; the other item in (c) is an open choice.'
SAFE = (['cons-1-8'], ['site-safety'])
A6 = add('6', 'a', '(a)', 'Draw a large freehand sketch of the safety sign for each of the items of personal protective equipment (PPE) listed below: high-visibility vest; protective footwear; safety helmet.',
         [row('vest', 'High-visibility vest Quality of sketch (excellent, good, fair)', 8, 'The blue mandatory sign for a high-visibility vest: excellent 8, good 6, fair 4.', BAND8),
          row('footwear', 'Protective footwear Quality of sketch (excellent, good, fair)', 8, 'The blue mandatory sign for protective footwear: excellent 8, good 6, fair 4.', BAND8),
          row('helmet', 'Safety helmet Quality of sketch (excellent, good, fair)', 8, 'The blue mandatory sign for a safety helmet: excellent 8, good 6, fair 4.', BAND8)],
         *SAFE, 'q6-signs', 'Personal protective equipment (1.8).', B6, S6)
B6b = add('6', 'b', '(b)', 'Using notes and freehand sketches, describe one design feature of each of the above safety items that helps to protect the worker from injury.',
          [row('vest', 'High-visibility vest Design feature', 3, 'Such as: fluorescent orange or yellow for daytime visibility; reflective strips that retro-reflect artificial light at night.'),
           row('footwear', 'Protective footwear Design feature', 3, 'Such as: a steel toe cap against falling objects; a mid-sole plate against punctures; a strengthened heel against turning the ankle.'),
           row('helmet', 'Safety helmet Design feature', 3, 'Such as: a high-density shell against falling and protruding objects; a nylon harness that absorbs the impact and spreads the force.'),
           row('presentation', 'Quality of sketches (excellent, good, fair)', 8, 'Quality of the sketches: excellent 8, good 6, fair 4.', BAND8)],
          *SAFE, 'q6-features', 'Personal protective equipment (1.8).', B6, S6)
C6 = add('6', 'c', '(c)', 'Recommend one other item of personal protective equipment (PPE) which should be worn by workers on a construction site. Give one reason for your recommendation.',
         [row('item', 'Other item of personal protection equipment (PPE)', 4, 'Such as: eye protection; ear protection; safety gloves.'),
          row('reason', 'Reason', 5, 'A reason matching the item. Such as: eyes protected from grit, dust and sharp objects when cutting or welding; ears from continuous noise of 85–90 dB; hands from sharp edges, hot bitumen or vibration.')],
         *SAFE, 'q6-other', 'Personal protective equipment (1.8).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-signs', B6, S6, parts(A6, B6b, C6))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p24 (printed 22): (a) given sketch 4, pipework 4, labels and sizes 4, quality of sketch 8 (8/6/4) = 20; (b) two valid details × 4, pipework and pump 4, valves 4, quality of sketch 8 (8/6/4) = 24; (c) one advantage 6. Complete 50.'
S7 = 'The layouts are open responses; the scheme gives model sketches.'
A7 = add('7', 'a', '(a)', 'Draw the given sketch and show the pipework necessary to collect the rainwater from the roof and to convey it to the underground storage tank. Label the main components and give their typical sizes.',
         [row('sketch', 'Draw given sketch', 4, 'The given house and underground tank sketched.'),
          row('pipework', 'Necessary pipework on sketch', 4, 'Pipework from the gutters and downpipes through a gully trap and filter to the tank.'),
          row('labels', 'Labels and typical sizes', 4, 'Such as: 125 mm eaves gutter; 65 mm offset bends and downpipe; gully trap with leaf filter; 100 mm underground pipes; filter with overflow; underground tank and overflow pipe.'),
          row('presentation', 'Quality of sketch (excellent, good, fair)', 8, 'Quality of the sketch: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-5-4'], ['drainage'], 'q7-collection', 'Surface water, gutters and rainwater pipes (5.4).', B7, S7)
B7b = add('7', 'b', '(b)', 'The stored rainwater is used for flushing a toilet. Show, using notes and freehand sketches, the pipework and pump necessary to take the water from the underground tank to a storage tank in the attic. Show also how to connect the toilet cistern to the storage tank in the attic. Include the necessary valves.',
          [row('detail-1', 'Valid detail one', 4, 'Such as: a 12 mm suction pipe with a floating filter; a pump with a power supply raising the water to the attic tank.'),
           row('detail-2', 'Valid detail two', 4, 'A second, different detail. Such as: a 12 mm pipe through a filter to a tank of at least 230 litres; a 12 mm pipe to the toilet cistern.'),
           row('pump', 'Pipework and pump on sketch', 4, 'The pipework and pump shown from the underground tank to the attic tank.'),
           row('valves', 'Valves shown on sketch', 4, 'Such as: a stop valve and a control valve.'),
           row('presentation', 'Quality of sketch (excellent, good, fair)', 8, 'Quality of the sketch: excellent 8, good 6, fair 4.', BAND8)],
          ['cons-5-2', 'cons-5-6'], ['services-water-gas-electrical', 'drainage'], 'q7-pumping', 'Cold water supply (5.2) to a sanitary fitment (5.6).', B7, S7)
C7 = add('7', 'c', '(c)', 'Discuss one advantage of storing rainwater in an underground tank.',
         [row('advantage', 'Advantage', 6, 'Such as: no space taken in small sites; less algae from daylight and temperature swings; no unsightly tank; water stays cool and does not freeze; larger storage.')],
         ['cons-5-4', 'cons-1-2'], ['drainage', 'planning-sustainability-environment'], 'q7-advantage', 'Rainwater (5.4) used sustainably (1.2).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-collection', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p25 (printed 23): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination. No pre-audit card existed for this question.'
TERMS = [
    ('smart meter', 'Smart meter', ['cons-5-8'], ['services-water-gas-electrical'],
     'records the electricity used in the home and shows its cost, giving awareness and control of energy use; it can send readings to the supplier and may also record water or gas.', 'Domestic electrical installation (5.8).'),
    ('biscuit joint', 'Biscuit joint', ['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation'],
     'joins boards of different widths in modern furniture; a biscuit joiner cuts a groove in each edge, and glued pressed-beech biscuits are inserted before the boards are clamped.',
     'Joints (10.1) and the choice of joint (10.4). The Ordinary reference taxonomy has no joinery heading; the term keeps the Wood, Rot & Ventilation association, and 10.1/10.4 are declared outside that heading’s crosswalk.'),
    ('earth rod', 'Earth rod', ['cons-5-8'], ['services-water-gas-electrical'],
     'a copper or steel rod, usually 1200 mm long, driven outside the building and connected to the electrical system; it carries fault current and lightning to earth, preventing shock and fire.', 'Domestic electrical installation and protection (5.8).'),
    ('airtightness tape', 'Airtightness tape', ['cons-6-5'], ['air-tightness-condensation'],
     'tape sealing joints in the structure — around windows, doors, floors, ceilings, joists, pipes and ducts — to prevent draughts and reduce heat loss.', 'Ventilation and airtightness (6.5).'),
    ('evacuated tube', 'Evacuated tube', ['cons-5-2'], ['hot-water-space-heating'],
     'part of a solar panel: a vacuum glass tube around a copper heat pipe whose glycol fluid vaporises, rises to a header and heats the coil in the hot water cylinder.', 'Hot water systems and cylinders (5.2).'),
    ('magnetic catch', 'Magnetic catch', ['cons-10-2'], ['wood-rot-ventilation'],
     'a catch for cabinet and wardrobe doors: a base unit with magnetised strips on the frame and a striking plate on the door, carefully aligned so they meet when the door closes.',
     'Simple fitments (10.2). The Ordinary reference taxonomy has no joinery or furniture heading; the term keeps the Wood, Rot & Ventilation association, and 10.2 is declared outside that heading’s crosswalk.'),
    ('roof-light window', 'Roof light window', ['cons-3-5', 'cons-3-9'], ['windows-doors', 'roofs'],
     'an opening window for sloping, flat or low-pitched roofs, double, triple or quadruple glazed, letting light into rooms in an attic development.', 'Windows (3.5) in the roof covering (3.9).'),
    ('aerated shower', 'Aerated shower', ['cons-5-2'], ['hot-water-space-heating', 'services-water-gas-electrical'],
     'mixes air with the flow of water, cutting use to about 7 litres a minute against 12 for a traditional shower while keeping a comfortable flow; it saves water and energy.', 'Hot and cold water systems (5.2).'),
    ('LED lighting', 'LED lighting', ['cons-5-8'], ['services-water-gas-electrical'],
     'light-emitting diodes for domestic and commercial fittings, using about 90% less energy than halogen bulbs and lasting far longer, though dearer to buy.', 'Domestic electrical installation (5.8).'),
]
Q8 = add('8', 'terms', '', 'Explain, with the aid of notes and freehand sketches, any five of the following: ' + '; '.join(t[0] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Terms', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{t[1]}: {t[4]}' for t in TERMS),
               group=dict(claimMax=5, perOption=10, options=[t[1] for t in TERMS]))],
         list(dict.fromkeys(n for t in TERMS for n in t[2])), list(dict.fromkeys(a for t in TERMS for a in t[3])), 'q8-terms',
         'The union of the nine printed terms: ' + ' '.join(t[5] for t in TERMS), B8, S8)

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p26 (printed 24): (a) two valid details × 4 and quality of sketches 6 (6/4/2) = 14; (b) holding the frame square, two details × 4 and quality 6, and fixing the frame, two details × 4 and quality 6 = 28; (c) advantage 4, disadvantage 4 = 8. Complete 50.'
S9 = 'Both the squaring and the fixing in (b) are required, each separately marked. Part (c) requires both one advantage and one disadvantage, separately marked: two required tasks composed into (c).'
DOORS = (['cons-3-7', 'cons-4-5'], ['windows-doors'])
T9C = 'Discuss one advantage and one disadvantage of fitting glazed double doors between the sitting room and the dining room.'
A9 = add('9', 'a', '(a)', 'Show, using notes and freehand sketches, how the blockwork over the opening is typically supported.',
         [row('detail-1', 'Valid detail one', 4, 'Such as: a prestressed concrete lintel, 100 mm wide and 65 mm thick, bearing on mortar on both sides of the opening.'),
          row('detail-2', 'Valid detail two', 4, 'A second, different detail. Such as: a bearing of 100 mm at each end; blockwork built up at the ends and over the lintel, with smaller blocks to bring the courses level; a reinforced concrete or steel lintel instead.'),
          row('presentation', 'Quality of sketches (excellent, good, fair)', 6, 'Quality of the sketches: excellent 6, good 4, fair 2.', BAND6)],
         ['cons-3-4'], ['foundations-floors-walls'], 'q9-support', 'Lintels over openings (3.4).', B9, S9)
B9b = add('9', 'b', '(b)', 'Show, using notes and freehand sketches, how the doorframe is held square while it is being fitted and show one method of fixing the doorframe to the wall.',
          [row('square', 'How the doorframe is held square while it is being fitted', 8, 'Two valid details, 4 each. Such as: a temporary strip fixed diagonally across one or both corners; a strip across the bottom keeping the jambs parallel and the correct distance apart; the corners checked for square.'),
           row('square-presentation', 'Quality of sketches (excellent, good, fair)', 6, 'Quality of the sketches for squaring the frame: excellent 6, good 4, fair 2.', BAND6),
           row('fixing', 'One method of fixing the doorframe to the wall', 8, 'Two valid details, 4 each. Such as: screw positions marked and drilled through the frame and marked on the wall; holes drilled for plastic plugs; the frame screwed back in place and the heads covered with wooden plugs; or metal frame fixings or steel fixing plates.'),
           row('fixing-presentation', 'Quality of sketches (excellent, good, fair)', 6, 'Quality of the sketches for fixing the frame: excellent 6, good 4, fair 2.', BAND6)],
          *DOORS, 'q9-frame', 'Doors (3.7) and internal door frames and second fixing (4.5).', B9, S9)
c9 = [add('9', f'c-{kind}', f'(c) — {kind}', f'Discuss one {kind} of fitting glazed double doors between the sitting room and the dining room.',
          [row(kind, kind.capitalize(), 4, note)],
          ['cons-3-7', 'cons-1-2'], ['windows-doors', 'planning-sustainability-environment'], 'q9-glazed', 'Glazed doors (3.7) in the layout of the home (1.2).', B9, S9)
      for kind, note in [('advantage', 'Such as: the doors open up the area and make the rooms feel bigger; daylight shared between both rooms; a private, quiet area when closed; wheelchair access between the rooms.'),
                         ('disadvantage', 'Such as: glazed areas can be dangerous; a larger area is harder to heat; less privacy; less wall space for fittings and furniture.')]]
C9 = compose('9', 'c', '(c)', c9, 'q9-glazed', B9, S9, T9C, labels=['Advantage', 'Disadvantage'])
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-frame', B9, S9, D.parts(('a', A9['questionText']), ('b', B9b['questionText']), ('c', T9C)))

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and three other questions (200 marks); all question banks retained, no full-exam Cartesian cards.'),
          (4, 'any five', 'Q8 closed choose-five of nine printed terms: one card with an any-five group over all nine terms (choice is not a route).')]
FINITE = {'8': dict(choose=5, options=[t[1] for t in TERMS], cardId=Q8['id'], groupRowId='terms', wholeQuestionMarks=50, termMarks=10)}
REASONS = {
    'q1-a': 'Adds the three typical dimensions (3) printed within part (a): 35 → 38.',
    'q1-b': 'Adds the draughting, accuracy and scale band (8/6/4) the scheme prints after the part (b) row to the radon detail: 4 → 12.',
    'q2-a': 'Rebuilt to the printed rows — two descriptions and the thickness (4 each) and quality of sketch (8/6/4): 12 → 20.',
    'q2-b': 'Rebuilt to the printed rows — two steps and the surface finish (4 each) and quality of sketch (8/6/4): 12 → 20.',
    'q2-c': 'Split into the printed advantage and disadvantage (5 each); tariff unchanged (10).',
    'q3-a': 'Adds the printed quality-of-sketch band (8/6/4) to the best-seven items: 35 → 43.',
    'q3-b': 'Reshaped to the printed advantage row; tariff unchanged (7).',
    'q4-a': 'Split into the two printed valid details (5 each); tariff unchanged (10).',
    'q5-a': 'Adds the three typical dimensions (3) printed within part (a): 35 → 38.',
    'q5-b': 'Adds the draughting, accuracy and scale band (8/6/4) the scheme prints after the part (b) row to the ventilation detail: 4 → 12.',
    'q6-b': 'Adds the printed quality-of-sketches band (8/6/4) to the three design features: 9 → 17.',
    'q6-c': 'Rebuilt to the printed rows — the other item (4) and its reason (5): 5 → 9.',
    'q7-a': 'Adds the printed quality-of-sketch band (8/6/4) to the sketch, pipework and labels: 12 → 20.',
    'q7-b': 'Adds the printed quality-of-sketch band (8/6/4) to the details, pump and valves: 16 → 24.',
    'q7-c': 'Reshaped to the printed advantage row; tariff unchanged (6).',
    'q9-a': 'Adds the printed quality-of-sketches band (6/4/2) to the two details: 8 → 14.',
    'q9-b': 'Adds the printed quality-of-sketches bands (6/4/2) to both the squaring and the fixing: 16 → 28.',
    'q9-c-advantage': 'Reshaped to the printed advantage row; tariff unchanged (4).',
    'q9-c-disadvantage': 'Reshaped to the printed disadvantage row; tariff unchanged (4).',
}
GAPS = [dict(cardId=B4b['id'], canonicalTopicIds=['cons-2-1'], atlasTopicId=D.CROSS + 'foundations-floors-walls', reason=SETOUT),
        dict(cardId=Q8['id'], canonicalTopicIds=['cons-10-1', 'cons-10-4', 'cons-10-2'], atlasTopicId=D.CROSS + 'wood-rot-ventilation',
             reason='No Ordinary outgoing reference heading covers joinery (10.1, 10.4, biscuit joint) or simple fitments (10.2, magnetic catch).')]
D.finish(LEDGER, FINITE, REASONS, taxonomy_gaps=GAPS, whole_choices={'q8-terms'})
