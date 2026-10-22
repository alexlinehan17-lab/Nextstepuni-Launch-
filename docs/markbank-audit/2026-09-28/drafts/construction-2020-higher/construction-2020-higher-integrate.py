"""Integrate the validated 2020 Higher Q1-Q10 (and alternative Q10) draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2020_higher as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2020 Higher Construction Studies Question 1: the printed question with a sketch of a house with a slated cut roof and flush eaves.',
    'q2-original': 'Original SEC 2020 Higher Construction Studies Question 2: the printed question with a sketch of scaffolding against a house under construction.',
    'q3-original': 'Original SEC 2020 Higher Construction Studies Question 3: the printed question with the floor plan and front elevation of a semi-detached bungalow, wall A-A marked.',
    'q4-original': 'Original SEC 2020 Higher Construction Studies Question 4: the printed question with a sketch of a vacant site between two houses.',
    'q5-original': 'Original SEC 2020 Higher Construction Studies Question 5: the printed question with a sketch of the insulated ground floor and all the construction and thermal data.',
    'q6-original': 'Original SEC 2020 Higher Construction Studies Question 6: the printed question with the elevation and plan of a retrofitted and extended vernacular cottage.',
    'q7-original': 'Original SEC 2020 Higher Construction Studies Question 7: the printed question with a sketch of a wood-burning stove in a chimney breast.',
    'q8-original': 'Original SEC 2020 Higher Construction Studies Question 8: the printed question with a sketch of a first-floor bathroom.',
    'q9-original': 'Original SEC 2020 Higher Construction Studies Question 9: the printed question with a cutaway sketch of a two-storey house.',
    'q10-original': 'Original SEC 2020 Higher Construction Studies Question 10: the printed question with the draft ground-floor plan of a new house.',
    'q10-alt-original': 'Original SEC 2020 Higher Construction Studies alternative Question 10: the printed quotation from Moncef Krarti on energy-efficient buildings and its two parts.',
    'q1-section': 'SEC model vertical section through half of the cut roof and externally insulated wall, with the detail lists for the wall, roof and eaves (two pages).',
    'q1-ventilation': 'SEC model eaves detail with arrows showing the ventilation path, labelled “(b) Ventilation”.',
    'q2-scaffolding': 'SEC 2020 Higher marking scheme notes on erecting, accessing and working on scaffolding, with sketches of scaffolds, ladders and guard-rails (three pages).',
    'q3-layout': 'SEC model revised bungalow layouts for a person with limited mobility with an open-plan kitchen/living space, and the notes (two pages).',
    'q4-materials': 'SEC 2020 Higher marking scheme notes on materials and finishes, with sketches of neighbouring houses.',
    'q4-shape': 'SEC 2020 Higher marking scheme notes on shape and form, with sketches of roof forms.',
    'q4-streetscape': 'SEC 2020 Higher marking scheme notes on streetscape, with sketches of building lines and roof heights.',
    'q4-characteristics': 'SEC 2020 Higher marking scheme notes and sketches for all three characteristics: materials and finishes, shape and form, and streetscape (two pages).',
    'q4-design': 'SEC model external designs for the infill house, one pitched and one flat-roofed, with the notes (two pages).',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 9.993 and U = 0.10 W/m²°C, and the annual heat-loss cost of €18.62 by two methods (two pages).',
    'q5-thermal-bridge': 'SEC model detail of the insulated ground floor meeting the cavity wall without a thermal bridge.',
    'q6-low-impact': 'SEC 2020 Higher marking scheme notes on low-environmental-impact features, with sketches of solar gain, the cottage and the plan.',
    'q6-modifications': 'SEC 2020 Higher marking scheme notes on further modifications — draught lobby, trees, solar shading, solar panels, PV, wind turbine, rainwater harvesting and chimney location — with sketches (two pages).',
    'q7-section': 'SEC model section through the floor, hearth, stove and chimney with the independent air supply marked B, and the detail lists.',
    'q8-location': 'SEC 2020 Higher marking scheme notes on locating a first-floor bathroom, with sketches of the bathroom layout.',
    'q8-pipework': 'SEC model above-ground drainage from the shower, wash basin, W.C. and kitchen sink to a 110 mm stack, with the pipe sizes.',
    'q9-completeness': 'SEC 2020 Higher marking scheme notes on completeness, with a sketch of a sealed junction.',
    'q9-flexibility': 'SEC 2020 Higher marking scheme notes on flexibility, with sketches of quilt in a partition and floor.',
    'q9-isolation': 'SEC 2020 Higher marking scheme notes on isolation, with a sketch of double glazing.',
    'q9-principles': 'SEC 2020 Higher marking scheme notes and sketches for completeness, flexibility and isolation.',
    'q9-upgrades': 'SEC model sound-insulated stud partition and floating first floor, with the notes and alternatives (two pages).',
    'q10-mvhr': 'SEC model MVHR layout on the given plan with the unit, ducts and airflow, and notes on how the system works.',
}
cp.integrate(paper, HERE, ALT)
