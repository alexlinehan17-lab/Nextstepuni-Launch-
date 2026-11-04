"""Integrate the validated 2018 Higher Q1-Q10 (and alternative Q10) draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2018_higher as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2018 Higher Construction Studies Question 1: the printed question with a sketch of a cedar-clad front porch with a lean-to slated roof.',
    'q2-original': 'Original SEC 2018 Higher Construction Studies Question 2: the printed question with a sketch of an excavator digging a trench.',
    'q3-original': 'Original SEC 2018 Higher Construction Studies Question 3: the printed question with the front elevation and ground floor plan of a terraced cottage and its rear garden.',
    'q4-original': 'Original SEC 2018 Higher Construction Studies Question 4: the printed question with the site location map showing sites A and B.',
    'q5-original': 'Original SEC 2018 Higher Construction Studies Question 5: the printed question with a sketch of the uninsulated ground floor and all the thermal data.',
    'q6-original': 'Original SEC 2018 Higher Construction Studies Question 6: the printed question with the elevation and plan of a small larch-clad self-build house.',
    'q7-original': 'Original SEC 2018 Higher Construction Studies Question 7: the printed question with the outline drawing of the door head, cavity wall and first floor joists.',
    'q8-original': 'Original SEC 2018 Higher Construction Studies Question 8: the printed question with a sketch of a wood-burning stove.',
    'q9-original': 'Original SEC 2018 Higher Construction Studies Question 9: the printed question with a cutaway sketch of an attic bedroom in a slated cut roof.',
    'q10-original': 'Original SEC 2018 Higher Construction Studies Question 10: the printed question with the elevation and plan of the preliminary house design.',
    'q10-alt-original': 'Original SEC 2018 Higher Construction Studies alternative Question 10: the printed quotation from Jane Burnside on green design and the task.',
    'q1-section': 'SEC model vertical section through the timber-clad porch wall, the lean-to roof and its abutment with the cavity wall, with the detail lists (two pages).',
    'q2-guidelines': 'SEC 2018 Higher marking scheme notes and sketches on best practice guidelines for excavating near cables, deep trenches and slating at height (two pages).',
    'q3-considerations': 'SEC 2018 Higher marking scheme notes on health and wellbeing considerations for the extension, with a sketch plan.',
    'q3-layout': 'SEC model extension layouts and modifications to the cottage, with sketches of glazed garden rooms.',
    'q3-meets': 'SEC 2018 Higher marking scheme notes and sketches on how the design meets each consideration.',
    'q4-characteristics': 'SEC 2018 Higher marking scheme notes and sketches on the characteristics of existing dwellings and of the proposed site (two pages).',
    'q4-sites': 'SEC 2018 Higher marking scheme notes on why site A or site B may be chosen, with sketches of each site (two pages).',
    'q4-layout': 'SEC model sketches of the house location, orientation, entrance and driveway on sites A and B.',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 0.8042 and U = 1.2434 W/m²°C, and the annual heat-loss cost of €352.5 by two methods.',
    'q5-thickness': 'SEC worked solution for the thickness of expanded polystyrene: 216.9 mm.',
    'q6-self-build': 'SEC 2018 Higher marking scheme notes on advantages and disadvantages of self-build, with sketches of the house.',
    'q6-features': 'SEC 2018 Higher marking scheme notes on design features that suit self-build, with sketch plans (two pages).',
    'q6-modifications': 'SEC 2018 Higher marking scheme notes and sketches on nZEB modifications — storm porch, thicker insulation, south glazing, glazed partition, solar panels, PV, rainwater harvesting and wind (two pages).',
    'q7-section': 'SEC model section through the door head, cavity wall and first floor with the typical floor, wall and door details.',
    'q8-layout': 'SEC model single-line diagram of the stove and solar heating with two zoned radiator circuits and the twin-coil cylinder.',
    'q8-safety': 'SEC 2018 Higher marking scheme notes and sketches on safety features of the system (two pages).',
    'q8-chimney': 'SEC 2018 Higher marking scheme notes and sketches on locating the chimney for the stove.',
    'q9-requirements': 'SEC 2018 Higher marking scheme notes and sketches on the functional requirements of an attic bedroom (two pages).',
    'q9-structure': 'SEC model sketches and notes on the structural stability, insulation and stud side walls of the attic roof (two pages).',
    'q9-air-leakage': 'SEC model detail and notes on preventing air leakage at the junction of the stud wall and the sloped ceiling.',
    'q10-principles': 'SEC 2018 Higher marking scheme notes and sketches for all three Passive House items — space heating energy demand, building form and thermal bridging (two pages).',
    'q10-modifications': 'SEC 2018 Higher marking scheme notes and sketches on Passive House modifications to the design.',
    'q10-orientation': 'SEC 2018 Higher marking scheme notes and sketches on the preferred orientation and the sun path (two pages).',
}
cp.integrate(paper, HERE, ALT)
