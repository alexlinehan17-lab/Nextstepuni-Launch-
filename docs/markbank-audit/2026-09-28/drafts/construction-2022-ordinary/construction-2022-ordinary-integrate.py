"""Integrate the validated 2022 Ordinary Q1-Q9 draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2022_ordinary as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2022 Ordinary Construction Studies Question 1: the printed question with a sketch of a sheeted front door in a cavity wall.',
    'q2-original': 'Original SEC 2022 Ordinary Construction Studies Question 2: the printed question with a sketch of an uninsulated attic with a water tank.',
    'q3-original': 'Original SEC 2022 Ordinary Construction Studies Question 3: the printed question with a sketch of a house and an underground rainwater tank.',
    'q4-original': 'Original SEC 2022 Ordinary Construction Studies Question 4: the printed question with a sketch of an open-plan kitchen and living room.',
    'q5-original': 'Original SEC 2022 Ordinary Construction Studies Question 5: the printed question with a sketch of a closed-string wooden stairs.',
    'q6-original': 'Original SEC 2022 Ordinary Construction Studies Question 6: the printed question with a sketch of a worker using a jackhammer on a footpath.',
    'q7-original': 'Original SEC 2022 Ordinary Construction Studies Question 7: the printed question with the draft plan of a rear garden with existing trees.',
    'q8-original': 'Original SEC 2022 Ordinary Construction Studies Question 8: the printed list of nine construction terms.',
    'q9-original': 'Original SEC 2022 Ordinary Construction Studies Question 9: the printed question with a sketch of a rural house with a timber-clad front porch.',
    'q1-scheme': 'SEC model section through the cavity wall, lintels, doorframe and door with the cavity closer marked (b), and the specification list.',
    'q2-method': 'SEC 2022 Ordinary marking scheme notes on insulating at ceiling joist level, with sketches of laying roll insulation, and the insulation types and thickness.',
    'q2-tank': 'SEC 2022 Ordinary marking scheme notes on insulating the water tank and pipework, with sketches of an insulated tank and foam pipe lagging.',
    'q2-advantages': 'SEC 2022 Ordinary marking scheme notes on the advantages of a highly insulated attic.',
    'q3-collection': 'SEC model diagram of the gutter, downpipe and underground pipe to the rainwater tank, with the typical details.',
    'q3-supply': 'SEC model diagram of the pump, filter and pipework from the underground tank to the attic tank and toilet cistern, with the typical details.',
    'q3-advantage': 'SEC 2022 Ordinary marking scheme notes on an advantage of reusing rainwater.',
    'q4-partition': 'SEC model sketch of a stud partition with headplate, soleplate, studs, noggins and door lintel labelled, with the notes and sizes.',
    'q4-pros-cons': 'SEC 2022 Ordinary marking scheme table of the advantages and disadvantages of a timber stud partition.',
    'q4-reasons': 'SEC 2022 Ordinary marking scheme notes on reasons for a living room separate from the kitchen.',
    'q5-scheme': 'SEC model section through the bottom three steps with the wedges marked (b), the specification list and the anti-creak details.',
    'q6-signs': 'SEC model PPE signs for ear protectors, safety boots, safety glasses, a dust mask and safety gloves, each with how it protects the worker.',
    'q6-risks': 'SEC 2022 Ordinary marking scheme notes on risks to workers using power tools.',
    'q6-public': 'SEC 2022 Ordinary marking scheme notes on protecting the public near footpath works, with sketches of barriers, cones and signs.',
    'q7-reasons': 'SEC 2022 Ordinary marking scheme notes on why a garden should meet the family’s needs.',
    'q7-layout': 'SEC model garden layouts showing the outdoor dining space, storage, flower beds and lawn, with the reasons for each location (two pages).',
    'q7-advantages': 'SEC 2022 Ordinary marking scheme notes on the advantages of trees and plants in a garden.',
    'q8-terms': 'SEC marking-scheme notes and sketches for all nine Question 8 terms, in scheme order: strip foundation, fascia board, airtight tape, wind turbine, septic tank, dovetail joint, wall tie, cordless jigsaw and underfloor heating.',
    'q9-wood': 'SEC 2022 Ordinary marking scheme notes on suitable woods for cladding and reasons, with a sketch of a timber-clad porch.',
    'q9-light': 'SEC 2022 Ordinary marking scheme notes on letting more light into the porch, with sketches of a roof light and a glazed porch.',
    'q9-porch': 'SEC 2022 Ordinary marking scheme notes on reasons for a front porch, with a sketch of a porch.',
}
cp.integrate(paper, HERE, ALT)
