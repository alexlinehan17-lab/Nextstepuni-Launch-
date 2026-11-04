"""Integrate the validated 2014 Higher Q1-Q10 (and alternative Q10) draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2014_higher as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2014 Higher Construction Studies Question 1: the printed question with a sketch of the eaves of a slated roof on a rendered wall.',
    'q2-original': 'Original SEC 2014 Higher Construction Studies Question 2: the printed question with a sketch of a sheeted front door above a step.',
    'q3-original': 'Original SEC 2014 Higher Construction Studies Question 3: the printed question with the elevation, ground floor plan and rear garden of a semi-detached house with a storeroom, wall A-A marked.',
    'q4-original': 'Original SEC 2014 Higher Construction Studies Question 4: the printed question with a sketch of a two-storey vernacular house and the three surveyed areas.',
    'q5-original': 'Original SEC 2014 Higher Construction Studies Question 5: the printed question with a sketch of the insulated ground floor and all the thermal data.',
    'q6-original': 'Original SEC 2014 Higher Construction Studies Question 6: the printed question with the elevation and ground floor plan of a low environmental impact house.',
    'q7-original': 'Original SEC 2014 Higher Construction Studies Question 7: the printed question with sketches of a casement window in a rendered wall.',
    'q8-original': 'Original SEC 2014 Higher Construction Studies Question 8: the printed question with the plan of the 7.0 m × 5.0 m bedroom.',
    'q9-original': 'Original SEC 2014 Higher Construction Studies Question 9: the printed question with a section of a two-storey house with music playing in an upstairs bedroom.',
    'q10-original': 'Original SEC 2014 Higher Construction Studies Question 10: the printed question with a sketch of a single-storey Passive House.',
    'q10-alt-original': 'Original SEC 2014 Higher Construction Studies alternative Question 10: the printed quotation from Michelle Fagan on resilient neighbourhoods and the task.',
    'q1-section': 'SEC model sections through the trussed rafter roof and timber frame wall, typical and best practice, with the wall and roof detail lists (two pages).',
    'q2-entrance': 'SEC 2014 Higher marking scheme notes and sketches on the threshold and access ramp, weather protection and lighting at the entrance (two pages).',
    'q2-reasons': 'SEC 2014 Higher marking scheme notes on reasons to design for lifetime use at the design stage.',
    'q3-requirements': 'SEC 2014 Higher marking scheme notes on the functional requirements of a study, with a sketch layout.',
    'q3-layout': 'SEC 2014 Higher marking scheme notes and sketches of the study layout for thermal, acoustic, visual and olfactory comfort and a flexible space.',
    'q3-external': 'SEC 2014 Higher marking scheme notes and sketches of external designs for the study.',
    'q4-step': 'SEC 2014 Higher marking scheme notes on advantages and disadvantages of step-by-step refurbishment.',
    'q4-upgrades': 'SEC 2014 Higher marking scheme notes and sketches for upgrading all three areas — the rubble walls, the slated roof and the suspended timber floor (five pages).',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 7.70 and U = 0.1298 W/m²K, and the annual heat-loss cost of €49.59.',
    'q5-cold-bridge': 'SEC model detail of the cavity wall and solid ground floor junction without a cold bridge.',
    'q6-features': 'SEC 2014 Higher marking scheme notes and sketches on the low environmental impact features of the design (two pages).',
    'q6-other': 'SEC 2014 Higher marking scheme notes and sketches on further features — solar collectors, photovoltaics, a winter garden, draught lobbies, internal doors, wind turbines and rainwater harvesting (three pages).',
    'q6-importance': 'SEC 2014 Higher marking scheme notes on the importance of low environmental impact housing.',
    'q7-section': 'SEC model sections through the triple-glazed window head and cill in the cavity wall, with the cavity closer detail.',
    'q8-layout': 'SEC model en suite layouts in the bedroom with notes on the door, window, shower, wash hand basin and WC.',
    'q8-pipework': 'SEC 2014 Higher marking scheme notes and sketch of the above-ground drainage from the shower, basin and WC to the stack.',
    'q8-water': 'SEC 2014 Higher marking scheme notes and sketches on economical use of water at the WC, basin and shower.',
    'q9-principles': 'SEC 2014 Higher marking scheme notes and sketches for all three principles — sound reflection, sound absorption and reverberation time.',
    'q9-upgrades': 'SEC 2014 Higher marking scheme notes and sketches on sound insulation of the stud partition and the floor (two pages).',
    'q9-insulating': 'SEC 2014 Higher marking scheme notes on sound insulation principles: isolation, mass, flexibility and completeness.',
    'q10-principles': 'SEC 2014 Higher marking scheme notes and sketches for all three items — building form, indoor air quality and foundation design (two pages).',
    'q10-orientation': 'SEC 2014 Higher marking scheme notes and sun-path sketch on orienting a Passive House.',
    'q10-overheating': 'SEC 2014 Higher marking scheme notes and sketches on why a Passive House overheats and details that reduce it (two pages).',
}
cp.integrate(paper, HERE, ALT, anchor_from_sidecar=True)
