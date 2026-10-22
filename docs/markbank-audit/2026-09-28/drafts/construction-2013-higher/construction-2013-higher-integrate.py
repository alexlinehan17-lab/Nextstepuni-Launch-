"""Integrate the validated 2013 Higher Q1-Q10 (and alternative Q10) draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2013_higher as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2013 Higher Construction Studies Question 1: the printed question with a sketch of the closed-string stairs rising to a landing with balustrade.',
    'q2-original': 'Original SEC 2013 Higher Construction Studies Question 2: the printed question with a sketch of two construction workers in safety helmets.',
    'q3-original': 'Original SEC 2013 Higher Construction Studies Question 3: the printed question with the elevation, ground floor plan and rear garden of a semi-detached house, walls A-A and B-B marked.',
    'q4-original': 'Original SEC 2013 Higher Construction Studies Question 4: the printed question with a sketch of a solar collector on a pitched roof.',
    'q5-original': 'Original SEC 2013 Higher Construction Studies Question 5: the printed question with sections of the triple-glazed window A and the single-glazed window B, and all the thermal data.',
    'q6-original': 'Original SEC 2013 Higher Construction Studies Question 6: the printed question with the elevation and ground floor plan of the house.',
    'q7-original': 'Original SEC 2013 Higher Construction Studies Question 7: the printed question with a sketch of the wood-burning stove.',
    'q8-original': 'Original SEC 2013 Higher Construction Studies Question 8: the printed question with a sketch of the trial hole in clay subsoil.',
    'q9-original': 'Original SEC 2013 Higher Construction Studies Question 9: the printed question with a section of the two-storey house, four junctions circled.',
    'q10-original': 'Original SEC 2013 Higher Construction Studies Question 10: the printed question with the room layout of the Passive House.',
    'q10-alt-original': 'Original SEC 2013 Higher Construction Studies alternative Question 10: the printed quotation from Orla Murphy on passive living and sustainable housing, and the task.',
    'q1-section': 'SEC model section through the closed-string stairs and landing, with the list of members and sizes.',
    'q2-culture': 'SEC 2013 Higher marking scheme notes on training, vigilance and teamwork in a site safety culture.',
    'q2-risks': 'SEC 2013 Higher marking scheme notes and sketches on safe use of a ladder and fitting a second-storey window (two pages).',
    'q2-tools': 'SEC 2013 Higher marking scheme notes on best practice with electrical power tools on site.',
    'q3-design': 'SEC 2013 Higher marking scheme notes and sketches of rear extension designs and the revised ground floor layout (two pages).',
    'q3-reasons': 'SEC 2013 Higher marking scheme notes on the reasons for more sunlight and a better view of the garden, with a sketch plan (two pages).',
    'q4-system': 'SEC single-line diagram of the stove and solar heating system with two zones, with notes on the control valves, the solar system and typical sizes.',
    'q4-siting': 'SEC 2013 Higher marking scheme notes and sketches on the orientation, inclination, location and sizing of a solar collector.',
    'q4-advantages': 'SEC 2013 Higher marking scheme notes on the advantages and disadvantages of the stove and solar heating system.',
    'q5-calculation': 'SEC worked solution: the U-value tables for the thermally broken frame (U = 0.178) and the triple-glazed unit (U = 0.260495).',
    'q5-comparison': 'SEC 2013 Higher marking scheme notes comparing the thermal properties and environmental considerations of the two windows.',
    'q5-head': 'SEC model details of the window head in the insulated cavity wall, with notes.',
    'q6-features': 'SEC 2013 Higher marking scheme notes and sketches on the low environmental impact features of the design (three pages).',
    'q6-buyers': 'SEC 2013 Higher marking scheme notes on modest scale, ease of modification and proximity to services for first-time buyers (two pages).',
    'q7-section': 'SEC model sections through the hearth and chimney with the stove flue, and notes on the flue liners.',
    'q8-requirements': 'SEC 2013 Higher marking scheme notes and sketch on the functional requirements of a foundation.',
    'q8-foundations': 'SEC 2013 Higher marking scheme notes and sketches of strip and raft foundations and the reasons for each.',
    'q8-concrete': 'SEC 2013 Higher marking scheme notes on ensuring the maximum strength of concrete in a foundation.',
    'q9-locations': 'SEC 2013 Higher marking scheme notes and sketches for all four circled locations — the chimney, the window head, the window cill and the lean-to roof against the wall (two pages).',
    'q9-materials': 'SEC 2013 Higher marking scheme notes and sketches on lead and flexible plastic DPC.',
    'q9-moisture': 'SEC 2013 Higher marking scheme notes and sketch on keeping moisture from the inner leaf of a timber frame wall.',
    'q10-principles': 'SEC 2013 Higher marking scheme notes and sketches for all three items — building orientation, thermal mass and primary energy demand (two pages).',
    'q10-mhrv': 'SEC MHRV ducting plan of the rooms with the supply and extract zones, and notes on how the system works (two pages).',
    'q10-location': 'SEC 2013 Higher marking scheme notes on energy conservation, maintenance, noise and aesthetics in locating the MHRV unit.',
}
cp.integrate(paper, HERE, ALT)
