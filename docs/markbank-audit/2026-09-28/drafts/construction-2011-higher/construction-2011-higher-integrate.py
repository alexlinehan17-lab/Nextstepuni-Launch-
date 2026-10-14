"""Integrate the validated 2011 Higher Q1-Q10 (and alternative Q10) draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2011_higher as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2011 Higher Construction Studies Question 1: the printed question with a sketch of a person at the main doorway.',
    'q2-original': 'Original SEC 2011 Higher Construction Studies Question 2: the printed question on roof requirements and pitched roof structures.',
    'q3-original': 'Original SEC 2011 Higher Construction Studies Question 3: the printed question with the elevation and plan of the thirty-year-old house, wall A-A marked.',
    'q4-original': 'Original SEC 2011 Higher Construction Studies Question 4: the printed question with a sketch of the two semi-detached houses.',
    'q5-original': 'Original SEC 2011 Higher Construction Studies Question 5: the printed question with a sketch of the hollow block wall and all the thermal data.',
    'q6-original': 'Original SEC 2011 Higher Construction Studies Question 6: the printed question with the elevation and ground floor plan of the block and cedar-clad house.',
    'q7-original': 'Original SEC 2011 Higher Construction Studies Question 7: the printed question with a sketch of the rendered chimney stack on the slated roof.',
    'q8-original': 'Original SEC 2011 Higher Construction Studies Question 8: the printed question with sketches of the wood burning stove and the solar collector.',
    'q9-original': 'Original SEC 2011 Higher Construction Studies Question 9: the printed question with an outline section of the single storey house, four junctions circled.',
    'q10-original': 'Original SEC 2011 Higher Construction Studies Question 10: the printed question with a sketch of an MHRV system in a Passive House.',
    'q10-alt-original': 'Original SEC 2011 Higher Construction Studies alternative Question 10: the printed quotation from the Urban Design Manual on good neighbourhoods, and the task.',
    'q1-section': 'SEC model sections through the accessible door threshold, sill and lintel in the cavity wall (two pages).',
    'q2-requirements': 'SEC 2011 Higher marking scheme notes on the functional requirements of a roof.',
    'q2-roofs': 'SEC 2011 Higher marking scheme sketches and typical sizes of a traditional cut purlin roof and a prefabricated W truss, with notes on their stability (two pages).',
    'q2-recommendation': 'SEC 2011 Higher marking scheme notes on the merits of cut and trussed roofs.',
    'q3-design': 'SEC 2011 Higher marking scheme notes and sketches on redesigning the envelope — windows, walls, roof and floor — and the layout (three pages).',
    'q3-reasons': 'SEC 2011 Higher marking scheme notes on the reasons for the window, wall and roof changes (two pages).',
    'q4-principles': 'SEC 2011 Higher marking scheme notes and sketches on mass, completeness and isolation (two pages).',
    'q4-party-wall': 'SEC 2011 Higher marking scheme notes and sketches on sound through the party wall and its revised detailing.',
    'q4-partition': 'SEC 2011 Higher marking scheme table and sketches of a double stud partition with notes on mass, isolation and completeness.',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 0.63955 and U = 1.563599 W/m²K, and the 113 mm of expanded polystyrene needed for 0.27 W/m²K.',
    'q5-walls': 'SEC 2011 Higher marking scheme notes on the disadvantages of hollow block walls and four recommended external wall types with sketches (two pages).',
    'q6-features': 'SEC 2011 Higher marking scheme notes and sketches on the low environmental impact features of the design (two pages).',
    'q6-importance': 'SEC 2011 Higher marking scheme notes on the form of the house, materials and labour, and design for lifetime use (three pages).',
    'q7-section': 'SEC model section through the chimney stack and slated roof, with flashings and dimensions.',
    'q8-system': 'SEC single-line diagram of the zoned stove heating system, with notes on control valves, pipe sizes and the solar modifications.',
    'q8-siting': 'SEC 2011 Higher marking scheme notes and sketch on the orientation and inclination of solar panels.',
    'q9-scheme': 'SEC 2011 Higher marking scheme notes and sketches for all the circled junctions — the cill, the window head, the eaves and the floor (Figs 9.1–9.5) — and the advantages (two pages).',
    'q10-principles': 'SEC 2011 Higher marking scheme notes and sketches for all three items — passive foundations, the airtight envelope, and windows and glazing (two pages).',
    'q10-mhrv': 'SEC 2011 Higher marking scheme notes and sketch on how an MHRV system works.',
    'q10-advantages': 'SEC 2011 Higher marking scheme notes on the advantages and disadvantages of MHRV (two pages).',
}
cp.integrate(paper, HERE, ALT)
