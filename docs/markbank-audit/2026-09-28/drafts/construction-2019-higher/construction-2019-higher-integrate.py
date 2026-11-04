"""Integrate the validated 2019 Higher Q1-Q10 (and alternative Q10) draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2019_higher as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2019 Higher Construction Studies Question 1: the printed question with a sketch of a triple-glazed window below a larch-clad panel in a rendered wall.',
    'q2-original': 'Original SEC 2019 Higher Construction Studies Question 2: the printed question with a sketch of a rural house and the outline of the proposed extension.',
    'q3-original': 'Original SEC 2019 Higher Construction Studies Question 3: the printed question with the elevation and first-floor plan of a detached house, wall A-A marked.',
    'q4-original': 'Original SEC 2019 Higher Construction Studies Question 4: the printed question with a sketch of a row of brick terraced townhouses and the three surveyed areas.',
    'q5-original': 'Original SEC 2019 Higher Construction Studies Question 5: the printed question with sketches of the partially filled cavity wall and the external insulation, and all the thermal data.',
    'q6-original': 'Original SEC 2019 Higher Construction Studies Question 6: the printed question with the elevation and ground floor plan of a low environmental impact house.',
    'q7-original': 'Original SEC 2019 Higher Construction Studies Question 7: the printed question with a sketch of a closed riser stairs with a bullnose bottom step.',
    'q8-original': 'Original SEC 2019 Higher Construction Studies Question 8: the printed question with the site layout map showing the new house and driveway on site A.',
    'q9-original': 'Original SEC 2019 Higher Construction Studies Question 9: the printed question with an outline section through an external door with three locations circled.',
    'q10-original': 'Original SEC 2019 Higher Construction Studies Question 10: the printed question with the elevation and plan of a 1970s bungalow, wall B-B marked.',
    'q10-alt-original': 'Original SEC 2019 Higher Construction Studies alternative Question 10: the printed quotation from Henry Skates on global warming and carbon footprints, and the task.',
    'q1-section': 'SEC model vertical section through the triple-glazed window, the timber frame wall with its block outer leaf and the larch-clad panel above, with the cill detail for part (b) (two pages).',
    'q1-cill': 'SEC model cill detail with the wrap-around DPC marked “(b) DPC”.',
    'q2-profiles': 'SEC 2019 Higher marking scheme sketches of four possible roof profiles for the extension — pitched, pitched with roof lights, flat green roof and curved roof.',
    'q3-layout': 'SEC model first-floor layouts for the bedroom and en suite with notes on furniture, access, storage, flexibility, ergonomics and the senses (two pages).',
    'q3-external': 'SEC 2019 Higher marking scheme notes and sketches of external designs for the extension (two pages).',
    'q4-upgrades': 'SEC 2019 Higher marking scheme notes and sketches for upgrading all three areas — the slated roof, the sliding sash windows and the solid brick walls with lime render (five pages).',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 1.939 and U = 0.516 W/m²°C, and the annual heat-loss cost of €199.60 by two methods.',
    'q5-thickness': 'SEC worked solution for the thickness of external expanded polystyrene: 147 mm.',
    'q6-features': 'SEC 2019 Higher marking scheme notes on low environmental impact features, with sketches of solar shading, the plan and photovoltaic panels.',
    'q6-renewables': 'SEC 2019 Higher marking scheme notes and sketches on evacuated tubes, wind turbines and photovoltaic cells, and how each makes a home more eco-friendly (three pages).',
    'q7-section': 'SEC model section through the closed string stairs with the typical member sizes, the Ø100 mm sphere and the 840–900 mm handrail height, and the safety features for part (b).',
    'q8-layout': 'SEC model site layout of the septic tank and percolation area with the minimum distances.',
    'q8-alternative': 'SEC 2019 Higher marking scheme notes and sketches of three alternative wastewater systems: a raised percolation area, a constructed wetland and a peat filter.',
    'q9-details': 'SEC model details preventing thermal bridges at the wallplate, the door head and the door threshold in a full-fill cavity wall.',
    'q10-retrofit': 'SEC 2019 Higher marking scheme notes and sketches on retrofitting the bungalow to EnerPHit — envelope, heat recovery ventilation, airtightness, comfort, renewables and solar gain (two pages).',
}
cp.integrate(paper, HERE, ALT)
