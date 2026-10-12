"""Integrate the validated 2022 Higher Q1-Q10 (and alternative Q10) draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2022_higher as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2022 Higher Construction Studies Question 1: the printed question with a sketch of a flat-roofed dining area projecting from the rear wall of a house.',
    'q2-original': 'Original SEC 2022 Higher Construction Studies Question 2: the printed question with the ground-floor plan of an open-plan kitchen/dining space.',
    'q3-original': 'Original SEC 2022 Higher Construction Studies Question 3: the printed question with the elevation and ground-floor plan of a terraced former shop and its rear garden, wall A-A marked.',
    'q4-original': 'Original SEC 2022 Higher Construction Studies Question 4: the printed question with a sketch of a digger excavating on a site.',
    'q5-original': 'Original SEC 2022 Higher Construction Studies Question 5: the printed question with a sketch of the externally insulated solid block wall and all the construction and thermal data.',
    'q6-original': 'Original SEC 2022 Higher Construction Studies Question 6: the printed question with the elevation and ground-floor plan of a timber-frame house.',
    'q7-original': 'Original SEC 2022 Higher Construction Studies Question 7: the printed question with a sketch of a cut-string wooden stairs and landing.',
    'q8-original': 'Original SEC 2022 Higher Construction Studies Question 8: the printed question with a sketch of solar collectors on a roof.',
    'q9-original': 'Original SEC 2022 Higher Construction Studies Question 9: the printed question with an outline section through a timber-frame wall and truss roof, three locations circled.',
    'q10-original': 'Original SEC 2022 Higher Construction Studies Question 10: the printed question with a sketch of a proposed Passive House in a rural setting.',
    'q10-alt-original': 'Original SEC 2022 Higher Construction Studies alternative Question 10: the printed SEAI quotation on replacing boilers with air source heat pumps and its two parts.',
    'q1-section': 'SEC model vertical section through the external wall, flat roof and abutment with the rear wall, with the detail lists for each area (two pages).',
    'q1-thermal-bridge': 'SEC model detail of the flat-roof abutment with an arrow to the insulated block, labelled “(b) Insulated block”.',
    'q2-entrance': 'SEC 2022 Higher marking scheme notes on lifetime-use entrance access, with sketches of a wide entrance door and a canopy.',
    'q2-corridor': 'SEC 2022 Higher marking scheme notes on lifetime-use internal corridors, with a sketch of corridor and door widths.',
    'q2-guidelines': 'SEC 2022 Higher marking scheme notes on lifetime-use entrance access and internal corridors, with sketches.',
    'q2-areas': 'SEC model kitchen and dining layout for a wheelchair user with turning circles and clear spaces, and the kitchen and dining notes with sketches (two pages).',
    'q3-layout': 'SEC model layouts of the rear extension with an internal courtyard, with notes on the courtyard, the separate living space and daylight.',
    'q3-reasons': 'SEC 2022 Higher marking scheme reasons for the proposed layout, with a model plan of the extension and courtyard.',
    'q4-requirements': 'SEC 2022 Higher marking scheme notes on the functional requirements of a foundation, with a sketch of loads on a house.',
    'q4-foundations': 'SEC model strip foundation and passive insulated raft foundation, each with its notes and dimensions (two pages).',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 5.229 and U = 0.191 W/m²°C, and the annual heat-loss cost of €100.02 by two methods.',
    'q5-insulation': 'SEC worked solution for the additional insulation: required resistance 8.333, difference 3.104, giving 96 mm.',
    'q6-low-impact': 'SEC 2022 Higher marking scheme notes on low-environmental-impact features, with sketches of timber framing, charred cladding and the plan.',
    'q6-wellbeing': 'SEC 2022 Higher marking scheme notes and sketches for all three Question 6(b) items: internal air quality, thermal environment and social interaction (two pages).',
    'q6-scheme': 'SEC marking-scheme notes and sketches for Question 6(a) and (b): low-impact features, internal air quality, thermal environment and social interaction (three pages).',
    'q7-section': 'SEC model section through the cut-string stairs and landing with the 100 mm sphere and 900 mm handrail height marked, the detail lists and the two safety details.',
    'q8-system': 'SEC model single-line diagram of a solar collector connected to a twin-coil cylinder with pump, controls and expansion vessel, the pipe sizes and how the system works.',
    'q9-locations': 'SEC model airtightness details for all three circled locations: the window head, wallplate level and a ceiling light fitting (two pages).',
    'q9-test': 'SEC 2022 Higher marking scheme notes on the blower door test, with sketches of the fan fitted in a doorway.',
    'q10-orientation': 'SEC model sketches of the preferred orientation with the summer and winter sun paths, and the notes on thermal performance.',
    'q10-thermal-mass': 'SEC 2022 Higher marking scheme notes on thermal mass with sketches of solar gain stored and released, a concrete floor and suitable materials.',
}
cp.integrate(paper, HERE, ALT, anchor_from_sidecar=True)
