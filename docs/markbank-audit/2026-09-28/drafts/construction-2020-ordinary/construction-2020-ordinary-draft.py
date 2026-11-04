"""Draft the 2020 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Wording is lifted from the SEC paper; every row's verbatim is printed in the scheme's mark tables
(pages 18-26). Q8 "any five of nine" is ONE card (choice is not a route): it keeps the pre-audit
stud-partition ID and the other eight per-term IDs alias to it. The other 20 pre-audit 2020 Ordinary
cards keep their IDs and concept IDs and are corrected in place; Q4(b) was never carded and is added.
Shared method: construction_paper.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_paper as cp  # noqa: E402

QUESTIONS = {
    '1': dict(page=2, title='Strip foundation, external wall and ground floor section', concept='strip-foundation-ground-floor-section',
              stem='A dwelling house has a 400 mm concrete block wall with a full-fill insulated cavity supported on a traditional strip foundation. The wall is plastered on both sides. The insulated concrete ground floor is finished with 20 mm floor tiles as shown.',
              note='Original sketch and specification retained. Construction details, dimensions and draughting belong to part (a); the damp detail in (b) is marked separately. Any alternative detailing that complies with current Building Regulations is acceptable.'),
    '2': dict(page=2, title='Insulating a cavity wall', concept='cavity-wall-insulation',
              stem='The proposed external wall for a new house has a 100 mm concrete block outer leaf, a 200 mm cavity and a 100 mm concrete block inner leaf as shown.',
              note='Original sketch retained. The insulating method, the insulation type and the additional insulation are open choices; the scheme lists typical examples.'),
    '3': dict(page=2, title='Wood-burning stove heating radiators and a cylinder', concept='stove-heating-pipework', stem='',
              note='Original sketch retained. The listed components are required content, not a choice; the best-eight list is a marking menu.'),
    '4': dict(page=3, title='Waste management on a construction site', concept='site-waste-management',
              stem='Careful planning is required to manage waste on a construction site so as to reduce, re-use and recycle construction materials. The sketch shows one possible waste management method used to sort materials on a site.',
              note='Original sketch retained. Reasons, materials, re-uses and the sorting method are open responses; the scheme lists typical examples.'),
    '5': dict(page=3, title='Cut roof ridge section', concept='roof-ridge-section',
              stem='The sketch shows portion of a pitched roof including the ridge. This traditional slated cut roof has a pitch of 45°. The slates are fixed to 50 mm × 20 mm battens, on a breather membrane, supported on 200 mm × 50 mm rafters. The roof is highly insulated at collar tie level with an insulated plasterboard ceiling beneath.',
              note='Original sketch and specification retained. Construction details, dimensions and draughting belong to part (a); the ventilation detail in (b) is marked separately.'),
    '6': dict(page=3, title='PPE signs, working at height and safety training', concept='site-safety-ppe-heights', stem='',
              note='Original question retained. The three signs, two precautions and two reasons are open responses; the scheme lists typical examples.'),
    '7': dict(page=4, title='Bathroom for a person with limited mobility', concept='accessible-bathroom-layout',
              stem='A draft design for a bathroom, suitable for a person with limited mobility is shown. The position of a window and a door are included.',
              note='Original plan retained. All three printed fittings in (a) are required in one sketch, each separately marked; the grab-rail locations and reasons are open responses.'),
    '8': dict(page=4, title='Construction terms', concept='construction-terms', stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=4, title='Extension with more natural light', concept='extension-natural-light',
              stem='The sketch shows a semi-detached house with an extension to the rear. The extension is finished externally with wooden cladding.',
              note='Original sketch retained. The reasons, modifications and advantages are open responses; the scheme lists typical examples.'),
}
SCHEME_PAGES = {'1': [4, 18], '2': [5, 19], '3': [6, 20], '4': [7, 21], '5': [8, 22], '6': [9, 10, 23], '7': [11, 12, 24], '8': [13, 14, 15, 25], '9': [16, 26]}
D = cp.Draft(HERE, 2020, 'ordinary', ('a35744b1da7e9a1108d6d061ebb37756af8904d0bb132e54612d729c05ec4202',
                                      '774f5fc6fc917e7f1e6c0e24ba6c896faf5b0327d224b1fe2cad7af9bb6c23fa'), 29, QUESTIONS, SCHEME_PAGES)
row, add, compose = D.row, D.add, D.compose
BAND8 = [0, 4, 6, 8]
BAND6 = [0, 2, 4, 6]


def parts(*cards):
    return D.parts(*[(letter, c['questionText']) for letter, c in zip('abc', cards)])


D.figures({
    'q1-original': D.paper(2, [45, 39, 580, 280]), 'q2-original': D.paper(2, [45, 280, 580, 497]),
    'q3-original': D.paper(2, [45, 497, 580, 765]), 'q4-original': D.paper(3, [45, 39, 580, 276]),
    'q5-original': D.paper(3, [45, 276, 580, 532]), 'q6-original': D.paper(3, [45, 532, 580, 765]),
    'q7-original': D.paper(4, [45, 39, 580, 375]), 'q8-original': D.paper(4, [45, 375, 580, 500]),
    'q9-original': D.paper(4, [45, 515, 580, 765]),
    'q1-scheme': D.scheme(4, [25, 58, 580, 760]),
    'q2-method': D.scheme(5, [25, 58, 580, 478]), 'q2-advantages': D.scheme(5, [25, 357, 465, 478]), 'q2-additional': D.scheme(5, [25, 478, 580, 795]),
    'q3-system': D.scheme(6, [25, 58, 580, 660]), 'q3-underfloor': D.scheme(6, [25, 660, 580, 785]),
    'q4-reasons': D.scheme(7, [25, 58, 580, 234]), 'q4-materials': D.scheme(7, [25, 234, 580, 520]), 'q4-storage': D.scheme(7, [25, 520, 580, 795]),
    'q5-scheme': D.scheme(8, [25, 58, 580, 735]),
    'q6-signs': D.scheme(9, [25, 58, 580, 755]), 'q6-heights': D.scheme(10, [25, 58, 580, 592]), 'q6-training': D.scheme(10, [25, 592, 580, 770]),
    'q7-layout': D.scheme(11, [25, 58, 580, 780]), 'q7-grab-rails': D.scheme(12, [25, 58, 580, 535]), 'q7-advantage': D.scheme(12, [25, 535, 580, 705]),
    'q8-terms': D.composite((13, [25, 58, 580, 768]), (14, [25, 58, 580, 718]), (15, [25, 58, 580, 750])),
    'q9-reasons': D.scheme(16, [25, 58, 580, 236]), 'q9-light': D.scheme(16, [25, 236, 580, 636]), 'q9-advantages': D.scheme(16, [25, 636, 580, 780]),
})

# ---------------------------------------------------------------- Q1
B1 = 'Scheme p18 (printed 16): (a) best 7 of 12 listed details × 5 = 35, four typical dimensions 4, draughting/accuracy/scale 8 (8/6/4), all printed within part (a): 47; (b) damp proof membrane/radon barrier 3. Complete 50.'
S1 = 'One required section and one required damp detail. The best-seven detail list is a marking menu, not a printed choose-seven task.'
A1 = add('1', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the strip foundation, external wall and ground floor. On your drawing show the typical construction details from the bottom of the foundation to a point 200 mm above finished floor level. Show an internal floor width of 900 mm and include four typical dimensions.',
         [row('details', 'Any 7 x 5 marks', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: reinforced strip foundation 1200 × 400 mm; concrete fill / foundation blocks; hardcore and sand blinding; 1200-gauge DPC/radon barrier; 200–300 mm floor insulation; 150 mm concrete floor slab taped and sealed at the wall junction; 20 mm floor tiles; skirting board; block inner leaf with 13 mm plaster; 200 mm full-fill cavity insulation; wall ties; block outer leaf with 19 mm render.', list(range(0, 36, 5))),
          row('dimensions', 'Any 4 typical dimensions', 4, 'Four appropriate typical dimensions on the section.'),
          row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the section: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-2-4', 'cons-3-3', 'cons-4-2'], ['question-one-drawing-questions', 'foundations-floors-walls'], 'q1-scheme',
         'Scaled drawing (1.5) of a strip foundation (2.4), cavity wall (3.3) and solid ground floor (4.2).', B1, S1)
B1b = add('1', 'b', '(b)', 'On your drawing, show the typical design detailing to prevent dampness entering the building through the floor.',
          [row('membrane', 'Damp proof membrane/Radon Barrier', 3, 'Show and identify a continuous damp proof membrane or radon barrier under the floor, lapped with the DPC in the walls, as in the scheme’s model section.', [0, 3])],
          ['cons-3-4', 'cons-4-2'], ['foundations-floors-walls'], 'q1-scheme', 'Damp proof courses and membranes (3.4) in a solid ground floor (4.2).', B1, S1)
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-scheme', B1, S1, parts(A1, B1b))

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p19 (printed 17): (a) method note + sketch 8 + 8 = 16, insulation type 5, thickness 5 = 26; (b) two advantages × 4 = 8; (c) additional insulation note + sketch 8 + 8 = 16. Complete 50.'
S2 = '"one suitable method" and "one method" of additional insulation are open choices with no printed list; each part stays one response.'
A2 = add('2', 'a', '(a)', 'Using notes and freehand sketches, show one suitable method of insulating the proposed cavity. Specify the type and thickness of insulation.',
         [row('method', 'Method of insulating wall note + sketch (8 + 8 marks)', 16, 'Note 8 and sketch 8. Such as: rigid insulation boards installed as the blockwork is built; boards tongued and grooved to fit tightly; wall ties holding the boards tight against the inner leaf.'),
          row('type', 'Preferred insulation type for cavity wall', 5, 'Such as: expanded polystyrene (EPS) boards; polyurethane boards; polyisocyanurate foam panels.'),
          row('thickness', 'Thickness of insulation', 5, 'Such as: 200 mm for a full-filled cavity; 150 mm boards for a partial fill.')],
         ['cons-3-3', 'cons-6-2'], ['foundations-floors-walls', 'heat-loss-insulation'], 'q2-method', 'Cavity walls (3.3) and insulating materials (6.2).', B2, S2)
B2b = add('2', 'b', '(b)', 'List two advantages of installing insulation in the cavity.',
          [row('advantage-1', 'Advantage 1', 4, 'Such as: less heat lost from the building; more thermal comfort for the occupants.'),
           row('advantage-2', 'Advantage 2', 4, 'A second, different advantage. Such as: lower energy bills; less use of fossil fuels; a better Building Energy Rating (BER).')],
          ['cons-6-2', 'cons-6-3'], ['heat-loss-insulation'], 'q2-advantages', 'Insulation (6.2) and running costs (6.3).', B2, S2)
C2 = add('2', 'c', '(c)', 'On a separate sketch show, using notes and freehand sketches, one method of providing additional insulation to this wall to further improve its thermal insulation properties.',
         [row('additional', 'Additional Insulating the wall detail note + sketch (8 + 8 marks)', 16, 'Note 8 and sketch 8. Such as, external: insulation panels fixed and glued to the wall, at least 200 mm thick, finished with acrylic base and finish coats on mesh; internal: 50 × 50 mm battens at 400 mm centres with insulation between, a vapour barrier, and plasterboard or insulated plasterboard with a skim coat.')],
         ['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q2-additional', 'Upgrading a wall (3.3) with insulating materials (6.2).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b, C2], 'q2-method', B2, S2, parts(A2, B2b, C2))

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p20 (printed 18): (a) best 8 of 10 listed items × 5 = 40 and quality of sketch 6 (6/4/2) = 46; (b) one advantage 4. Complete 50.'
S3 = 'The printed component list is required content, not a choice; the best-eight list is a marking menu.'
A3 = add('3', 'a', '(a)', 'A wood-burning stove can be used to heat radiators for a dwelling house. Draw a large freehand sketch of the given house and, on your sketch, show the pipework necessary to supply hot water from the stove to the ground floor radiators and also heat the water in the cylinder on the first floor. Include the following in your sketch: wood-burning stove; hot water cylinder; pipework to cylinder; expansion tank / vessel; pipework to radiators; all necessary pumps and valves.',
         [row('items', 'Any 8 x 5 marks', 40, 'Credit the best EIGHT acceptable items at 5 marks each, capped at 40. Marked items: drawing the given sketch; 15 mm cold feed to the burner; 22 mm flow to the radiators; 22 mm return from the radiators; radiators; 22 mm primary flow to the cylinder; 22 mm primary return to the burner; 22 mm overflow pipe; 22 mm expansion pipe from the cylinder; valves / pumps.', list(range(0, 41, 5))),
          row('presentation', 'Quality of sketch (excellent, good, fair)', 6, 'Quality of the sketch: excellent 6, good 4, fair 2.', BAND6)],
         ['cons-5-3', 'cons-5-2'], ['hot-water-space-heating'], 'q3-system', 'A heating system (5.3) with an indirect hot water cylinder (5.2).', B3, S3)
B3b = add('3', 'b', '(b)', 'The installation of an underfloor heating system is now an alternative to radiators. Discuss one advantage of installing an underfloor heating system.',
          [row('advantage', 'Advantage', 4, 'Such as: heat spread evenly and consistently around each room; a suitably sized system heats a larger room than one radiator; a lower working temperature that can reduce heating bills; more wall space for furniture and decoration.')],
          ['cons-5-3'], ['hot-water-space-heating'], 'q3-underfloor', 'Heating systems (5.3).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-system', B3, S3, parts(A3, B3b))

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p21 (printed 19): (a) two reasons × 8 = 16; (b) two materials × 4 and a re-use for each × 5 = 18; (c) sorting method note + sketch 6 + 10 = 16. Complete 50.'
S4 = 'Reasons, materials, re-uses and the sorting method are open responses with no printed list.'
WASTE = (['cons-1-2', 'cons-1-8'], ['planning-sustainability-environment', 'site-safety'])
A4 = add('4', 'a', '(a)', 'Discuss two reasons why a construction company should have a waste management plan for their site.',
         [row('reason-1', 'Reason 1', 8, 'Such as: to prevent and minimise waste on building sites; to build a culture of re-using and recycling rather than dumping.'),
          row('reason-2', 'Reason 2', 8, 'A second, different reason. Such as: less energy used making new material; a clean, clear site that prevents accidents; hazardous waste kept out of local water supplies; landfill sites are scarce; a lower overall building cost.')],
         *WASTE, 'q4-reasons', 'Managing site waste in the built environment (1.2) and site safety (1.8).', B4, S4)
B4b = add('4', 'b', '(b)', 'Name two construction materials that could be recycled and then re-used on a construction site. Give one suitable re-use for each material.',
          [row('material-1', 'Construction material 1', 4, 'Such as: bedrock, blocks and concrete; bricks; soil/subsoil; timber; slates/tiles; plasterboard; metal.'),
           row('material-2', 'Construction material 2', 4, 'A second, different material from the same kind of list.'),
           row('reuse-1', 'Suitable re-use for material 1', 5, 'A re-use matching material 1. Such as: infill during construction; restoration of heritage buildings; fill on site or replanting green areas; wood products or landscaping woodchips.'),
           row('reuse-2', 'Suitable re-use for material 2', 5, 'A re-use matching material 2. Such as: re-used on the building to keep its character; waste gypsum recycled into new plasterboard; metal processed into new metal products.')],
          ['cons-1-2'], ['planning-sustainability-environment'], 'q4-materials', 'Re-use and recycling of construction materials in the built environment (1.2).', B4, S4)
C4 = add('4', 'c', '(c)', 'Using notes and a freehand sketch, show one other method of sorting and storing waste materials on a construction site.',
         [row('method', 'Method note + sketch (6 + 10 marks)', 16, 'Note 6 and sketch 10. Such as: containers protecting metal and valuable waste from the weather; pallets for bricks and blocks; barrels for lengths of timber and metal; trailers for soil and bedrock; boxes for small items; bulk bags for soil and gravel.')],
         *WASTE, 'q4-storage', 'Sorting and storing site waste (1.2) safely on site (1.8).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-storage', B4, S4, parts(A4, B4b, C4))

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p22 (printed 20): (a) best 7 of 12 listed details × 5 = 35, three typical dimensions 3 × 1, draughting/accuracy/scale 8 (8/6/4) = 46; (b) vent at ridge or vent slate 4. Complete 50.'
S5 = 'One required section and one required ventilation detail. The best-seven detail list is a marking menu, not a printed choice; either ventilation method earns the row.'
A5 = add('5', 'a', '(a)', 'To a scale of 1:5, draw a vertical section through the roof at the ridge. Show the typical construction details from the top of the ridge to a level 100 mm below the collar ties. The collar ties are positioned 900 mm below ridge level. Include three courses of slate at the ridge. Include three typical dimensions on your drawing.',
         [row('details', 'Any 7 x 5 marks', 35, 'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: ridge tile; ridge vent; roofing slates; 50 × 35 mm battens; breather membrane; 275 × 32 mm ridge board; 200 × 50 mm rafter; 200 × 50 mm collar tie; insulation between rafters; airtight membrane; insulated plasterboard; plaster skim.', list(range(0, 36, 5))),
          row('dimensions', 'Any three typical dimensions 3 x 1 mark', 3, 'Three appropriate typical dimensions on the section, 1 each.'),
          row('presentation', 'Draughting, accuracy and scale (excellent, good, fair)', 8, 'Draughting, accuracy and scale of the section: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-1-5', 'cons-3-8', 'cons-3-9'], ['question-one-drawing-questions', 'roofs'], 'q5-scheme',
         'Scaled drawing (1.5) of a cut roof (3.8) at the ridge with its covering and insulation (3.9).', B5, S5)
B5b = add('5', 'b', '(b)', 'On your drawing show one method of ventilating the roof.',
          [row('ventilation', 'Vent at ridge or Vent slate', 4, 'Show and identify a ridge vent at the ridge or vent slates fitted near the ridge, as in the scheme’s model section.', [0, 4])],
          ['cons-3-9', 'cons-6-5'], ['roofs', 'wood-rot-ventilation'], 'q5-scheme', 'Ventilation (6.5) of the roof covering (3.9).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-scheme', B5, S5, parts(A5, B5b))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p23 (printed 21): (a) three signs × (sign 6 + reason 2) = 24; (b) two precautions, each notes + sketch 5 + 4 = 18; (c) two reasons × 4 = 8. Complete 50.'
S6 = 'The three signs, two precautions and two reasons are open responses with no printed list; the scheme lists typical examples.'
SAFE = (['cons-1-8'], ['site-safety'])
SIGNS = 'Such as: steel toe cap boots (feet protected from dropped heavy materials); hi-viz clothing (workers visible to machine operators); hard hat (head protected from falling material); protective eye wear (eyes protected from debris, dust and power tools); ear protection (continuous noise of 85–90 dB or more); hand protection (sharp equipment, corrosive or toxic substances).'
A6 = add('6', 'a', '(a)', 'Using large freehand sketches, show three safety signs highlighting the use of personal protection equipment (PPE) that must be worn by all workers on a construction site. For each sign, state how the personal protection equipment protects workers on the site.',
         [row('sign-1', 'Safety sign 1', 8, 'Sign 6 and how it protects the worker 2 (the scheme’s "Safety sign 1" and "Reason 1"). ' + SIGNS),
          row('sign-2', 'Safety sign 2', 8, 'A second, different sign 6 and how it protects the worker 2 (the scheme’s "Safety sign 2" and "Reason 2").'),
          row('sign-3', 'Safety sign 3', 8, 'A third, different sign 6 and how it protects the worker 2 (the scheme’s "Safety sign 3" and "Reason 3").')],
         *SAFE, 'q6-signs', 'Personal protective equipment (1.8).', B6, S6)
B6b = add('6', 'b', '(b)', 'Using notes and sketches, describe two safety precautions that workers must follow when working at height on a construction site.',
          [row('precaution-1', 'Precaution one notes + sketch (5 + 4 marks)', 9, 'Notes 5 and sketch 4. Such as: scaffolding above 1.5 m, level, supported and properly erected; guard rails and working platforms at eaves level; ladders secured top and bottom at a slope of 1:4.'),
           row('precaution-2', 'Precaution two notes + sketch (5 + 4 marks)', 9, 'Notes 5 and sketch 4 for a second, different precaution. Such as: a safety harness and fall protection; a cherry picker or teleporter for extended work at height; working in pairs with a buddy.')],
          *SAFE, 'q6-heights', 'Safety precautions on site, here working at height (1.8).', B6, S6)
C6 = add('6', 'c', '(c)', 'Give two reasons why all workers must undertake a safety training course prior to working on a construction site.',
         [row('reason-1', 'Reason 1', 4, 'Such as: a legal requirement under Health and Safety regulations; raises the standard of safety awareness on site.'),
          row('reason-2', 'Reason 2', 4, 'A second, different reason. Such as: basic training prevents accidents and avoids health hazards; workers learn to assess risks and identify dangers; it promotes a safety culture.')],
         *SAFE, 'q6-training', 'Safety precautions on site (1.8).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-signs', B6, S6, parts(A6, B6b, C6))

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p24 (printed 22): (a) sketch 6 and three fittings, each location 3 + reason 3 = 24; (b) two grab-rail locations, each note + sketch 2 + 4 and a reason 4 = 20; (c) one advantage 6. Complete 50.'
S7 = 'All three printed fittings in (a) are required in one sketch, not a choice. Grab-rail locations are open responses.'
BATH = (['cons-5-6', 'cons-1-2'], ['drainage', 'planning-sustainability-environment'])
ACCESS = (['cons-1-2'], ['planning-sustainability-environment'])
A7 = add('7', 'a', '(a)', 'Draw a freehand sketch of the given design and show your preferred location for each of the following in the bathroom: toilet; wash basin; shower area. Give one reason for selecting each location.',
         [row('sketch', 'Sketch of bathroom', 6, 'A freehand sketch of the given bathroom design.'),
          row('toilet', 'Location and valid reason for toilet position (3 + 3 marks)', 6, 'Location 3 and reason 3. Such as: on an external wall for easier waste plumbing and secure fixing; free space beside it for grab rails; a 1500 mm turning circle kept clear.'),
          row('wash-basin', 'Location and valid reason for wash basin position (3 + 3 marks)', 6, 'Location 3 and reason 3. Such as: a wall to fix it securely; a 1500 mm turning circle kept clear; wall space for a mirror or grab rails.'),
          row('shower', 'Location and valid reason for shower area position (3 + 3 marks)', 6, 'Location 3 and reason 3. Such as: clear of the door opening; natural light; external walls for secure fixtures; a 1500 mm turning circle kept clear.')],
         *BATH, 'q7-layout', 'Sanitary fitments (5.6) placed in an accessible layout (1.2).', B7, S7)
B7b = add('7', 'b', '(b)', 'The homeowner has decided to install grab-rails, like that shown, in the bathroom to aid ease of use for all users. Using notes and freehand sketches show two possible locations for grab-rails. Give one reason for each location.',
          [row('location-1', 'Suitable location 1 note + sketch (2 + 4 marks)', 6, 'Note 2 and sketch 4. Such as: a horizontal rail beside the toilet, fixed to a solid wall about 700 mm above the floor.'),
           row('reason-1', 'Reason 1', 4, 'A reason for location 1. Such as: extra support lowering onto or rising from the toilet seat; safer, more independent use.'),
           row('location-2', 'Suitable location 2 note + sketch (2 + 4 marks)', 6, 'Note 2 and sketch 4 for a second, different location. Such as: horizontal or vertical rails in the shower area, fixed through the tiles.'),
           row('reason-2', 'Reason 2', 4, 'A reason for location 2. Such as: support when using the shower; safety from slipping; safe, independent use of the shower.')],
          *ACCESS, 'q7-grab-rails', 'Accessible design of the built environment (1.2).', B7, S7)
C7 = add('7', 'c', '(c)', 'Discuss one advantage of designing a bathroom suitable for a person with reduced mobility.',
         [row('advantage', 'Advantage of designing bathroom suitable for people with reduced mobility', 6, 'Such as: future-proofing the home so fewer costly, intrusive modifications are needed later; the family can live in the home for life; less mobile members use it independently; safe access for all.')],
         *ACCESS, 'q7-advantage', 'Accessible design of the built environment (1.2).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-layout', B7, S7, parts(A7, B7b, C7))

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p25 (printed 23): five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50.'
S8 = 'Closed choose-five of nine printed terms. Choice is not a route: one card prints all nine terms and carries one any-five group over them (10 marks each), never a card per term or per combination. It keeps the pre-audit stud-partition ID; the other eight per-term IDs alias to it.'
TERMS = [
    ('stud-partition', 'stud partition', 'Stud partition', ['cons-4-5'], ['foundations-floors-walls', 'windows-doors'],
     'a timber or metal stud frame fixed to the floor, ceiling and walls; vertical studs at 400 mm centres between head and sole plates, braced by noggins and covered with plasterboard; load bearing or non-load bearing.', 'Stud partitions (4.5).'),
    ('domino-joint', 'domino joint', 'Domino joint', ['cons-10-3'], ['wood-rot-ventilation'],
     'a woodworking joint cut with a domino joiner, used in modern furniture to butt, edge or corner join pieces of wood quickly; very strong with wood adhesive.', 'Jointing boards (10.3).'),
    ('slump-test', 'slump test', 'Slump test', ['cons-2-7'], ['concrete'],
     'measures the workability of fresh concrete on site, batch by batch, and checks the water content; a truncated cone, tamping rod and meter stick; 0–50 mm slump low workability, 50–75 mm medium.', 'Site concrete and its water/cement ratio (2.7).'),
    ('dynamic-glass', 'dynamic glass', 'Dynamic glass', ['cons-3-6'], ['windows-doors'],
     'a thin coating that changes from clear to tinted under a small DC voltage (electrochromic) or with the sun’s heat (thermochromic), reducing glare and overheating for the occupants’ comfort.', 'Glass and glazing (3.6).'),
    ('pyrite', 'pyrite', 'Pyrite', ['cons-4-2'], ['foundations-floors-walls'],
     'a naturally occurring iron sulphide in sedimentary rock that cracks and expands when exposed to moisture and oxygen; in fill under a building it heaves ground floors and cracks walls.', 'Solid ground floors and their fill (4.2).'),
    ('pile-foundation', 'pile foundation', 'Pile foundation', ['cons-2-4'], ['foundations-floors-walls'],
     'supports and anchors a building where the soil has low bearing capacity or good soil is deep; end-bearing, friction or short-bored, drilled and poured or driven; a ground beam carries the walls onto the piles.', 'Pile foundations (2.4).'),
    ('trimmer', 'trimmer', 'Trimmer', ['cons-4-3'], ['foundations-floors-walls'],
     'a joist supporting the ends of trimmed joists or rafters around a stairwell or chimney opening, carried by trimming joists; carries more load, so usually 25 mm thicker than common joists.', 'Upper floor framing (4.3).'),
    ('butt-hinge', 'butt hinge', 'Butt hinge', ['cons-3-7', 'cons-3-5'], ['windows-doors'],
     'a widely used hinge of two leaves and a central pin, 12–150 mm long, in brass, mild steel or stainless steel; the leaves sit in shallow trenches and are fixed with countersunk screws; for doors, windows and boxes.', 'Door (3.7) and window (3.5) ironmongery.'),
    ('solar-panel', 'solar panel', 'Solar Panel', ['cons-6-4', 'cons-5-3', 'cons-5-8'], ['services-water-gas-electrical', 'planning-sustainability-environment'],
     'evacuated tubes converting solar radiation to heat, or photovoltaic panels generating electricity; best on a south-facing roof at about 45° in Ireland; a sustainable source that cuts CO2 emissions.', 'Solar heat gain (6.4) for heating (5.3) and electricity (5.8).'),
]
Q8 = add('8', 'None-stud-partition', '', 'Explain, with the aid of notes and freehand sketches, any five of the following: ' + '; '.join(t[1] for t in TERMS) + '.',
         [dict(id='terms', kind='anyN', verbatim='Construction Terms', marks=50,
               contextNote='Explain any five of the nine terms. Each term is marked separately: primary communication of relevant information 6 and other communication 4, in notes or sketches (the scheme reserves no fixed split between them). '
               + ' '.join(f'{t[2]}: {t[5]}' for t in TERMS),
               group=dict(claimMax=5, perOption=10, options=[t[2] for t in TERMS]))],
         list(dict.fromkeys(n for t in TERMS for n in t[3])), list(dict.fromkeys(a for t in TERMS for a in t[4])), 'q8-terms',
         'The union of the nine printed terms: ' + ' '.join(t[6] for t in TERMS), B8, S8)

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p26 (printed 24): (a) two reasons × 6 = 12; (b) two modifications, each notes + sketch 4 + 9 = 13, = 26; (c) two advantages × 6 = 12. Complete 50.'
S9 = 'The reasons, modifications and advantages are open responses with no printed list; the scheme lists typical examples.'
LIGHT = 'No Ordinary outgoing reference heading covers daylighting (7.4); the card keeps the Planning, Sustainability & Environment association.'
A9 = add('9', 'a', '(a)', 'Discuss two reasons why a homeowner would build an extension to their house.',
         [row('reason-1', 'Valid reason one', 6, 'Such as: more floor area for a growing household; more natural light into the existing building.'),
          row('reason-2', 'Valid reason two', 6, 'A second, different reason. Such as: a higher property value; cheaper than moving; personalising an older design; better thermal performance from new materials.')],
         ['cons-1-2'], ['planning-sustainability-environment'], 'q9-reasons', 'Extending a dwelling in the built environment (1.2).', B9, S9)
B9b = add('9', 'b', '(b)', 'Using notes and freehand sketches, show two modifications to the extension that would allow more natural light enter the dwelling.',
          [row('modification-1', 'Modification 1 to extension notes + sketch (4 + 9 marks)', 13, 'Notes 4 and sketch 9. Such as: larger or taller windows; floor-to-ceiling glazing; a sliding or bi-fold door.'),
           row('modification-2', 'Modification 2 to extension notes + sketch (4 + 9 marks)', 13, 'Notes 4 and sketch 9 for a second, different modification. Such as: roof lights in the sloped roof; solar tubes or sky tunnels; removing internal walls to let light through.')],
          ['cons-7-4', 'cons-3-5'], ['planning-sustainability-environment', 'windows-doors'], 'q9-light', 'Good daylighting (7.4) through windows (3.5).', B9, S9)
C9 = add('9', 'c', '(c)', 'Discuss two advantages for the occupants by increasing the amount of natural light entering the dwelling.',
         [row('advantage-1', 'Advantage 1', 6, 'Such as: lower energy costs for lighting and heating; less reliance on fossil fuels for lighting.'),
          row('advantage-2', 'Advantage 2', 6, 'A second, different advantage. Such as: helps regulate Seasonal Affective Disorder; less eye strain and better illumination; more vitamin D; more attractive interiors.')],
         ['cons-7-4', 'cons-6-4'], ['planning-sustainability-environment'], 'q9-advantages', 'Good daylighting (7.4) and solar gain (6.4).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-light', B9, S9, parts(A9, B9b, C9))

LEDGER = [(1, 'Answer Question', 'Whole-exam selection: Question 1 and three other questions (200 marks); all question banks retained, no full-exam Cartesian cards.'),
          (4, 'any five', 'Q8 closed choose-five of nine printed terms: one card with an any-five group over all nine terms (choice is not a route).')]
FINITE = {'8': dict(choose=5, options=[t[0] for t in TERMS], cardId=Q8['id'], groupRowId='terms', wholeQuestionMarks=50, termMarks=10)}
REASONS = {
    'q1-a': 'Adds the four typical dimensions (4) and draughting/accuracy/scale (8/6/4) printed within part (a): 35 → 47.',
    'q1-b': 'Reshaped to the printed all-or-nothing row "Damp proof membrane/Radon Barrier" (0 or 3); tariff unchanged.',
    'q2-a': 'Adds the printed insulation type (5) and thickness (5) to the method note and sketch (8 + 8): 5 → 26.',
    'q2-b': 'Split into the two printed advantages (4 each); tariff unchanged (8).',
    'q2-c': 'Reshaped to the printed note + sketch row (8 + 8); tariff unchanged (16).',
    'q3-a': 'Adds the printed quality-of-sketch band (6/4/2) to the best-eight items: 40 → 46.',
    'q3-b': 'Reshaped to the printed advantage row; tariff unchanged (4).',
    'q4-a': 'Split into the two printed reasons (8 each); tariff unchanged (16).',
    'q4-c': 'Reshaped to the printed note + sketch row (6 + 10); tariff unchanged (16).',
    'q5-a': 'Adds the three typical dimensions (3) and draughting/accuracy/scale (8/6/4) printed within part (a): 35 → 46.',
    'q5-b': 'Reshaped to the printed all-or-nothing row "Vent at ridge or Vent slate" (0 or 4); tariff unchanged.',
    'q6-a': 'All three printed signs, each sign 6 + reason 2: 6 → 24.',
    'q6-b': 'Split into the two printed precautions (notes + sketch 5 + 4 each); tariff unchanged (18).',
    'q6-c': 'Split into the two printed reasons (4 each); tariff unchanged (8).',
    'q7-a': 'Split into the printed sketch (6) and the three location-and-reason rows (3 + 3 each); tariff unchanged (24).',
    'q7-b': 'Both printed locations, each note + sketch (2 + 4) and a reason (4): 8 → 20.',
    'q7-c': 'Reshaped to the printed advantage row; tariff unchanged (6).',
    'q9-a': 'Split into the two printed reasons (6 each); tariff unchanged (12).',
    'q9-b': 'Split into the two printed modifications (notes + sketch 4 + 9 each); tariff unchanged (26).',
    'q9-c': 'Split into the two printed advantages (6 each); tariff unchanged (12).',
    'q8-None-stud-partition': 'Now the whole of Question 8: one card printing all nine terms with an any-five group (10 each, 50), kept under this ID; the other eight per-term IDs alias to it (choice is not a route): 10 → 50.',
}
CONSOLIDATED = {f'q8-None-{t[0]}': 'q8-None-stud-partition' for t in TERMS[1:]}
GAPS = [dict(cardId=B9b['id'], canonicalTopicIds=['cons-7-4'], atlasTopicId=D.CROSS + 'planning-sustainability-environment', reason=LIGHT),
        dict(cardId=C9['id'], canonicalTopicIds=['cons-7-4'], atlasTopicId=D.CROSS + 'planning-sustainability-environment', reason=LIGHT)]
D.finish(LEDGER, FINITE, REASONS, consolidated=CONSOLIDATED, taxonomy_gaps=GAPS, whole_choices={'q8-None-stud-partition'})
