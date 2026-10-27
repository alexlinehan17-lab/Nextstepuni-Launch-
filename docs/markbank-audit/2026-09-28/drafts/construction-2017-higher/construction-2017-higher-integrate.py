"""Integrate the validated 2017 Higher Q1-Q10 (and alternative Q10) draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2017_higher as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2017 Higher Construction Studies Question 1: the printed question with a sketch of an open-plan kitchen with tiled and timber floors.',
    'q2-original': 'Original SEC 2017 Higher Construction Studies Question 2: the printed question with the ground floor plan of a semi-detached house showing office A and location B.',
    'q3-original': 'Original SEC 2017 Higher Construction Studies Question 3: the printed question with the front elevation and ground floor plan of a 1950s farmhouse, wall A-A marked.',
    'q4-original': 'Original SEC 2017 Higher Construction Studies Question 4: the printed question with a sketch of a timber frame wall with cedar cladding.',
    'q5-original': 'Original SEC 2017 Higher Construction Studies Question 5: the printed question with sketches of the hollow block wall before and after external insulation, and all the thermal data.',
    'q6-original': 'Original SEC 2017 Higher Construction Studies Question 6: the printed question with the elevation and plan of a larch-clad eco-friendly house.',
    'q7-original': 'Original SEC 2017 Higher Construction Studies Question 7: the printed question with a sketch of a slated pitched roof.',
    'q8-original': 'Original SEC 2017 Higher Construction Studies Question 8: the printed question with sketches of a kitchen work surface and a home office.',
    'q9-original': 'Original SEC 2017 Higher Construction Studies Question 9: the printed question with a sketch of a cavity wall on a reinforced strip foundation.',
    'q10-original': 'Original SEC 2017 Higher Construction Studies Question 10: the printed question with the ground floor plan showing the MHRV unit M in the hallway.',
    'q10-alt-original': 'Original SEC 2017 Higher Construction Studies alternative Question 10: the printed quotation from Paul Keogh on adapting heritage buildings and the task.',
    'q1-section': 'SEC model sections through the foundation, cavity wall, solid floor and suspended timber floor with the cross-ventilation ducting, and the detail lists (two pages).',
    'q2-requirements': 'SEC 2017 Higher marking scheme notes and sketches on the functional requirements of a lifetime-use bathroom.',
    'q2-advantages': 'SEC 2017 Higher marking scheme notes on advantages of converting office A.',
    'q2-layout': 'SEC model bathroom layouts at A and sketches of trap seals and a vented stack preventing sewer gases.',
    'q3-layout': 'SEC 2017 Higher marking scheme notes and sketch plans on optimising daylight and open-plan living in the extension.',
    'q3-reasons': 'SEC 2017 Higher marking scheme notes and sketch layouts and renders giving reasons for the design (two pages).',
    'q3-advantages': 'SEC 2017 Higher marking scheme notes and sketches on advantages of extending the farmhouse (two pages).',
    'q4-requirements': 'SEC 2017 Higher marking scheme notes on the functional requirements of an external wall, with a wall section.',
    'q4-walls': 'SEC 2017 Higher marking scheme notes and sketches for all three wall types — concrete block cavity, timber frame with rainscreen, and timber frame with hemp-lime (two pages).',
    'q4-discussion': 'SEC 2017 Higher marking scheme notes on the environmental considerations and ease of construction of each wall type (two pages).',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 1.151 and U = 0.869 W/m²°C.',
    'q5-thickness': 'SEC worked solution for the thickness of external expanded polystyrene: 204.08 mm.',
    'q5-cost': 'SEC worked solution for the annual heat-loss cost through the upgraded wall, €47.99, by two methods (two pages).',
    'q6-advantages': 'SEC 2017 Higher marking scheme notes on the importance of eco-friendly design, with the elevation and plan.',
    'q6-features': 'SEC 2017 Higher marking scheme notes and sketches on the eco-friendly features of the design (two pages).',
    'q6-operating': 'SEC 2017 Higher marking scheme notes and sketches on features that reduce operating costs — storm porch, evacuated tubes, PV, wind and rainwater harvesting (two pages).',
    'q7-section': 'SEC model sections through the trussed rafter roof and timber frame walls with the roof and wall detail lists (two pages).',
    'q8-light': 'SEC 2017 Higher marking scheme notes and sketches on natural and artificial light on a kitchen work surface.',
    'q8-window': 'SEC worked solution by the degree of efficiency method, giving a window area of 8.4 m².',
    'q8-glazing': 'SEC 2017 Higher marking scheme notes and sketches on advances in glazing — insulated glazing units, low-e glazing, smart glass and warm edge spacers (two pages).',
    'q9-foundation': 'SEC model reinforced strip foundation with typical dimensions and the reasons for them.',
    'q9-concrete': 'SEC 2017 Higher marking scheme notes and sketches on mixing, placing, compacting and curing concrete (two pages).',
    'q9-test': 'SEC 2017 Higher marking scheme notes and sketches on the slump test and the cube test (two pages).',
    'q10-principles': 'SEC 2017 Higher marking scheme notes and sketches for all three Passive House items — airtightness, indoor air quality and solar shading (two pages).',
    'q10-mhrv': 'SEC model MHRV ducting layout on the plan, with notes on how the system works.',
    'q10-advantages': 'SEC 2017 Higher marking scheme notes on advantages of siting the MHRV unit in the hallway.',
}
cp.integrate(paper, HERE, ALT)
