"""Integrate the validated 2016 Higher Q1-Q10 (and alternative Q10) draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2016_higher as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2016 Higher Construction Studies Question 1: the printed question with a sketch of a house with a flat-roofed front porch.',
    'q2-original': 'Original SEC 2016 Higher Construction Studies Question 2: the printed question with a sketch of a worker on a ladder.',
    'q3-original': 'Original SEC 2016 Higher Construction Studies Question 3: the printed question with the elevation and plan of a 1970s bungalow, wall A-A marked.',
    'q4-original': 'Original SEC 2016 Higher Construction Studies Question 4: the printed question with the site location map showing site A.',
    'q5-original': 'Original SEC 2016 Higher Construction Studies Question 5: the printed question with the timber frame wall specification, its thermal data and a sketch of the wall.',
    'q6-original': 'Original SEC 2016 Higher Construction Studies Question 6: the printed question with the elevation and plan of a cedar-clad single storey house.',
    'q7-original': 'Original SEC 2016 Higher Construction Studies Question 7: the printed question with a sketch of a chimney stack through a slated roof.',
    'q8-original': 'Original SEC 2016 Higher Construction Studies Question 8: the printed question with a sketch of a semi-detached house and a stone storeroom.',
    'q9-original': 'Original SEC 2016 Higher Construction Studies Question 9: the printed question with a sketch of two pendant lights over a dining table.',
    'q10-original': 'Original SEC 2016 Higher Construction Studies Question 10: the printed question with a sketch of a Passive House with large south glazing.',
    'q10-alt-original': 'Original SEC 2016 Higher Construction Studies alternative Question 10: the printed quotation on reusing existing buildings and the task.',
    'q1-section': 'SEC model sections through the flat-roofed porch, window head and abutment with the cavity wall, with the wall, roof and window detail lists (three pages).',
    'q2-culture': 'SEC 2016 Higher marking scheme notes and sketches on initial and ongoing safety training and collective responsibility (two pages).',
    'q2-level-of-risk': 'SEC 2016 Higher marking scheme notes and sketch on the level of risk in using a ladder.',
    'q2-duration-of-task': 'SEC 2016 Higher marking scheme notes and sketch on the duration of the task when using a ladder.',
    'q2-ladder': 'SEC 2016 Higher marking scheme notes and sketches on both printed items: the level of risk and the duration of the task.',
    'q2-guidelines': 'SEC 2016 Higher marking scheme notes and sketch on best practice when placing a ladder to a scaffold platform.',
    'q3-redesign': 'SEC 2016 Higher marking scheme notes and sketch plans and elevations on redesigning the internal layout and external envelope for natural light.',
    'q3-reasons': 'SEC 2016 Higher marking scheme notes and sketches on the reasons for the redesign (two pages).',
    'q4-reasons': 'SEC 2016 Higher marking scheme notes on why site A is suitable, with a sketch of the site.',
    'q4-layout': 'SEC model sketches of the house location, orientation, entrance and access road on site A.',
    'q4-one-off': 'SEC 2016 Higher marking scheme notes on advantages and disadvantages of one-off rural houses.',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 3.655565 and U = 0.27356 W/m²°C, and the annual heat-loss cost of €96.96 by two methods (two pages).',
    'q5-thickness': 'SEC worked solution for the thickness of expanded polystyrene: 111.4 mm.',
    'q6-features': 'SEC 2016 Higher marking scheme notes and sketches on low environmental impact features of the design (two pages).',
    'q6-renewable': 'SEC 2016 Higher marking scheme notes and sketches on on-site renewable energy — wind, PV, evacuated tubes and heat exchangers (two pages).',
    'q6-advantages': 'SEC 2016 Higher marking scheme notes and sketches on advantages of on-site renewable energy.',
    'q7-section': 'SEC model section through the chimney stack and roof with the flashings, the 600 mm and 1000 mm heights and the detail list.',
    'q8-advantages': 'SEC 2016 Higher marking scheme notes and sketches on advantages and disadvantages of refurbishing the storeroom.',
    'q8-upgrades': 'SEC 2016 Higher marking scheme notes and sketches for upgrading all three areas — the rubble walls, the slated roof and the flagged floor (four pages).',
    'q9-circuits': 'SEC 2016 Higher marking scheme notes on the typical use of ring and radial circuits.',
    'q9-lighting': 'SEC model loop-in lighting circuit from the distribution board to the switch and two lights, with cable sizes, colours and safety features.',
    'q9-economy': 'SEC 2016 Higher marking scheme notes on features for the economical use of electricity in lighting.',
    'q10-principles': 'SEC 2016 Higher marking scheme notes and sketches for all three items — foundations, ground floor and walls.',
    'q10-overheating': 'SEC 2016 Higher marking scheme notes and sketches on why a Passive House overheats and details that reduce it (two pages).',
    'q10-planning': 'SEC 2016 Higher marking scheme notes on advantages and disadvantages of the Passive House standard as a planning requirement.',
}
cp.integrate(paper, HERE, ALT)
