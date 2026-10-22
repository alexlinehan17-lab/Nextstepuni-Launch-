"""Integrate the validated 2010 Higher Q1-Q10 (and alternative Q10) draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2010_higher as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2010 Higher Construction Studies Question 1: the printed question with a sketch of the wall, casement window and trussed slated roof.',
    'q2-original': 'Original SEC 2010 Higher Construction Studies Question 2: the printed question with the plan of the open-plan living, dining and kitchen space and its entrance.',
    'q3-original': 'Original SEC 2010 Higher Construction Studies Question 3: the printed question on internal and external insulation of a 1970s cavity wall.',
    'q4-original': 'Original SEC 2010 Higher Construction Studies Question 4: the printed question with a sketch of the manhole at a branch and main drain.',
    'q5-original': 'Original SEC 2010 Higher Construction Studies Question 5: the printed question with all the thermal data for the solid concrete wall.',
    'q6-original': 'Original SEC 2010 Higher Construction Studies Question 6: the printed question with the elevation and plan of the timber frame house.',
    'q7-original': 'Original SEC 2010 Higher Construction Studies Question 7: the printed question with a sketch of the top of the open riser stairs.',
    'q8-original': 'Original SEC 2010 Higher Construction Studies Question 8: the printed question on window size by daylight and a high-performance window.',
    'q9-original': 'Original SEC 2010 Higher Construction Studies Question 9: the printed question with an outline sketch of the attic space.',
    'q10-original': 'Original SEC 2010 Higher Construction Studies Question 10: the printed question with a sketch of the MHRV layout in a Passive House.',
    'q10-alt-original': 'Original SEC 2010 Higher Construction Studies alternative Question 10: the printed quotation from Anthony Reddy on sustainable urbanism, and the task.',
    'q1-section': 'SEC model sections through the wall, window and trussed roof, with typical roof sizes.',
    'q2-entrance': 'SEC 2010 Higher marking scheme notes and sketch on the accessible entrance threshold.',
    'q2-areas': 'SEC 2010 Higher marking scheme notes and sketches on the dining and kitchen areas for a wheelchair user (two pages).',
    'q3-systems': 'SEC 2010 Higher marking scheme notes and sketches on internal dry lining and external insulation, with cill and head details (three pages).',
    'q3-advantages': 'SEC 2010 Higher marking scheme notes on the advantages of internal and external insulation.',
    'q4-requirements': 'SEC 2010 Higher marking scheme notes and sketches on the functional requirements of below ground drainage.',
    'q4-manhole': 'SEC 2010 Higher marking scheme notes and sketches on the construction of a manhole.',
    'q4-test': 'SEC 2010 Higher marking scheme notes and sketch on the water, air and smoke tests (two pages).',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 0.55372 and U = 1.805, and 78.75 mm of phenolic foam for 0.27 W/m²K (two pages).',
    'q5-mass': 'SEC 2010 Higher marking scheme notes and sketches on thermal mass and passive solar collection and storage (two pages).',
    'q6-features': 'SEC 2010 Higher marking scheme notes and sketches on the cladding, passive solar gain and compact form (two pages).',
    'q6-materials': 'SEC 2010 Higher marking scheme notes on renewable, durable and locally sourced materials.',
    'q7-scheme': 'SEC model section through the open riser stairs and landing with handrail heights, and notes and sketches on stairs safety (two pages).',
    'q8-calculation': 'SEC worked solution by the degree of efficiency method, giving a window area of 2.85 m².',
    'q8-window': 'SEC 2010 Higher marking scheme notes and sketches on thermally efficient window frames and glazing.',
    'q8-environment': 'SEC 2010 Higher marking scheme notes on environmental considerations for the window frame material.',
    'q9-requirements': 'SEC 2010 Higher marking scheme notes and sketches on the functional requirements of an attic living space.',
    'q9-leakage': 'SEC 2010 Higher marking scheme notes and sketches on sealing air leakage routes in the attic (two pages).',
    'q9-advantages': 'SEC 2010 Higher marking scheme notes on the advantages of airtightness.',
    'q10-principles': 'SEC 2010 Higher marking scheme notes and sketches for all three items — shape and form, continuity of insulation and reduced cold bridging (two pages).',
    'q10-mhrv': 'SEC 2010 Higher marking scheme notes and sketches on MHRV operation and advantages, and on preventing overheating.',
}
cp.integrate(paper, HERE, ALT)
