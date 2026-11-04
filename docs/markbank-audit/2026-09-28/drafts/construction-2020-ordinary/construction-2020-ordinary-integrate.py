"""Integrate the validated 2020 Ordinary Q1-Q9 draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2020_ordinary as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2020 Ordinary Construction Studies Question 1: the printed question with a sketch of the strip foundation, cavity wall and tiled insulated ground floor.',
    'q2-original': 'Original SEC 2020 Ordinary Construction Studies Question 2: the printed question with a sketch of the 100 mm block outer leaf, 200 mm cavity and 100 mm block inner leaf.',
    'q3-original': 'Original SEC 2020 Ordinary Construction Studies Question 3: the printed question with a section of a two-storey house with a wood-burning stove, radiators and a cylinder.',
    'q4-original': 'Original SEC 2020 Ordinary Construction Studies Question 4: the printed question with a sketch of coloured skips sorting waste on a site.',
    'q5-original': 'Original SEC 2020 Ordinary Construction Studies Question 5: the printed question with a sketch of a slated cut roof at the ridge.',
    'q6-original': 'Original SEC 2020 Ordinary Construction Studies Question 6: the printed question with a sketch of workers on scaffolding at a house.',
    'q7-original': 'Original SEC 2020 Ordinary Construction Studies Question 7: the printed question with the draft bathroom plan and a sketch of a grab-rail.',
    'q8-original': 'Original SEC 2020 Ordinary Construction Studies Question 8: the printed instruction and the nine construction terms.',
    'q9-original': 'Original SEC 2020 Ordinary Construction Studies Question 9: the printed question with a sketch of a semi-detached house with a timber-clad rear extension.',
    'q1-scheme': 'SEC model section through the strip foundation, cavity wall and insulated ground floor with the damp proof membrane marked (b), the specification list and the notes for part (b).',
    'q2-method': 'SEC 2020 Ordinary marking scheme notes on insulating the cavity wall — method, type and thickness of insulation — with sketches of insulation boards in the cavity, and the advantages for part (b).',
    'q2-advantages': 'SEC 2020 Ordinary marking scheme notes listing advantages of installing cavity wall insulation.',
    'q2-additional': 'SEC 2020 Ordinary marking scheme notes and labelled sketches of external and internal methods of adding insulation to the wall.',
    'q3-system': 'SEC model sketch of the house with pipework from the wood-burning stove to the ground-floor radiators and the first-floor cylinder, with the typical details list.',
    'q3-underfloor': 'SEC 2020 Ordinary marking scheme notes on advantages of underfloor heating.',
    'q4-reasons': 'SEC 2020 Ordinary marking scheme notes on reasons for a site waste management plan.',
    'q4-materials': 'SEC 2020 Ordinary marking scheme notes on recyclable construction materials and re-uses, with sketches of a bulk bag, a crate and a barrel.',
    'q4-storage': 'SEC 2020 Ordinary marking scheme notes on methods of sorting and storing site waste, with sketches of a pallet, a container and a covered store.',
    'q5-scheme': 'SEC model section through the cut roof at the ridge with the ridge vent marked (b), the specification list and the ventilation notes.',
    'q6-signs': 'SEC 2020 Ordinary marking scheme table of PPE safety signs — boots, hi-viz clothing, hard hat, eye wear, ear and hand protection — and how each protects workers.',
    'q6-heights': 'SEC 2020 Ordinary marking scheme notes on working safely at height, with sketches of a guard rail, ladders, a cherry picker and a safety harness.',
    'q6-training': 'SEC 2020 Ordinary marking scheme notes on reasons for site safety training.',
    'q7-layout': 'SEC model bathroom layout with the toilet, wash basin and shower area placed, and the reasons for each location.',
    'q7-grab-rails': 'SEC 2020 Ordinary marking scheme notes on grab-rail locations at the toilet and in the shower, with sketches.',
    'q7-advantage': 'SEC 2020 Ordinary marking scheme notes on advantages of a bathroom designed for reduced mobility.',
    'q8-terms': 'SEC 2020 Ordinary marking scheme notes and sketches for all nine terms: stud partition, domino joint, slump test, dynamic glass, pyrite, pile foundation, trimmer, butt hinge and solar panel (three pages).',
    'q9-reasons': 'SEC 2020 Ordinary marking scheme notes on reasons for building an extension.',
    'q9-light': 'SEC 2020 Ordinary marking scheme notes on modifications that let more natural light into the extension, with sketches of glazing, roof lights and folding doors.',
    'q9-advantages': 'SEC 2020 Ordinary marking scheme notes on advantages of more natural light for the occupants.',
}
cp.integrate(paper, HERE, ALT)
