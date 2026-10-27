"""Integrate the validated 2021 Higher Q1-Q10 (and alternative Q10) draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2021_higher as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2021 Higher Construction Studies Question 1: the printed question with a sketch of an accessible sheeted external door.',
    'q2-original': 'Original SEC 2021 Higher Construction Studies Question 2: the printed question with a sketch of workers on a construction site.',
    'q3-original': 'Original SEC 2021 Higher Construction Studies Question 3: the printed question with the ground-floor plan of a semi-detached house and its rear garden, wall A-A marked.',
    'q4-original': 'Original SEC 2021 Higher Construction Studies Question 4: the printed question with the site location map showing sites A and B.',
    'q5-original': 'Original SEC 2021 Higher Construction Studies Question 5: the printed question with a sketch of the brick-clad timber-frame wall and all the construction and thermal data.',
    'q6-original': 'Original SEC 2021 Higher Construction Studies Question 6: the printed question with the elevation and ground-floor plan of an urban terraced house.',
    'q7-original': 'Original SEC 2021 Higher Construction Studies Question 7: the printed question with a sketch of a rendered chimney stack on a slated roof.',
    'q8-original': 'Original SEC 2021 Higher Construction Studies Question 8: the printed question with a sketch of a wood-burning stove.',
    'q9-original': 'Original SEC 2021 Higher Construction Studies Question 9: the printed question with a sketch of sockets above a kitchen worktop.',
    'q10-original': 'Original SEC 2021 Higher Construction Studies Question 10: the printed question with a sketch of a barn-inspired rural house.',
    'q10-alt-original': 'Original SEC 2021 Higher Construction Studies alternative Question 10: the printed Roscommon County Council quotation on reusing historic buildings and its two parts.',
    'q1-section': 'SEC model vertical section through the accessible threshold, cavity wall, insulated floor and strip foundation, with the detail lists (two pages).',
    'q1-thermal-bridge': 'SEC model threshold detail with an arrow to the vertical insulation, labelled “(b) Vertical Insulation”.',
    'q2-procedures': 'SEC 2021 Higher marking scheme notes on safety procedures for chimney repair, overhead cables and site hygiene, with sketches of scaffolding, bunting and signs (two pages).',
    'q3-layout': 'SEC model layouts and sketches of the garden home office, with the notes on each design consideration (two pages).',
    'q4-services': 'SEC 2021 Higher marking scheme notes on the availability of services, with sketches of overhead lines and service connections.',
    'q4-trees': 'SEC 2021 Higher marking scheme notes on existing trees and hedgerows, with a sketch of a house among mature hedgerows.',
    'q4-topography': 'SEC 2021 Higher marking scheme notes on site topography, with sketches of a house sheltered below the skyline.',
    'q4-factors': 'SEC 2021 Higher marking scheme notes and sketches for all three site factors: services, trees and hedgerows, and topography.',
    'q4-sites': 'SEC 2021 Higher marking scheme considerations for site A and site B, with sketches of each site.',
    'q4-site-plans': 'SEC model site sketches for sites A and B showing the house location and orientation, road entrance and driveway, with the notes.',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 5.424 and U = 0.184 W/m²°C, and the additional insulation of 42 mm.',
    'q5-layers': 'SEC model sketch of a timber-frame wall with the breather membrane and vapour control layer marked, and the notes.',
    'q6-low-impact': 'SEC 2021 Higher marking scheme notes on low-environmental-impact features, with sketches of the timber frame, plan and cladding.',
    'q6-features': 'SEC 2021 Higher marking scheme notes on added energy-saving features — PV panels, evacuated tubes, MVHR, a heat pump, triple glazing and extra insulation — with sketches (three pages).',
    'q7-section': 'SEC model section through the chimney stack and roof with the moisture details marked B, the detail lists and the two design details.',
    'q8-system': 'SEC model single-line diagram of the stove supplying the cylinder and two radiator zones, with the typical pipe sizes.',
    'q8-features': 'SEC 2021 Higher marking scheme notes on heating efficiency features — thermostatic valves, room thermostats, radiator design and time switches — with sketches (two pages).',
    'q8-heat-pump': 'SEC 2021 Higher marking scheme notes on air-to-water heat pumps and their advantages, with a sketch of the outdoor unit.',
    'q9-ring-main': 'SEC model ring main circuit from the distribution board through three sockets, with the cable sizes and colours.',
    'q10-shading': 'SEC 2021 Higher marking scheme notes on reducing overheating — overhangs, brise-soleil, shutters, thermal mass, vegetation and dynamic glass — with sketches.',
    'q10-setting': 'SEC 2021 Higher marking scheme notes on how the house responds to its rural setting, with sketches of a hay barn and the house plan.',
}
cp.integrate(paper, HERE, ALT, anchor_from_sidecar=True)
