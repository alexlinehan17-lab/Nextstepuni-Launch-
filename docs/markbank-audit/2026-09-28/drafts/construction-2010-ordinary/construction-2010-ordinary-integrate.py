"""Integrate the validated 2010 Ordinary Q1-Q9 draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2010_ordinary as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2010 Ordinary Construction Studies Question 1: the printed question with a sketch of the cavity wall and quarry-tiled solid floor.',
    'q2-original': 'Original SEC 2010 Ordinary Construction Studies Question 2: the printed question with a sketch of the attic of the 1960s house.',
    'q3-original': 'Original SEC 2010 Ordinary Construction Studies Question 3: the printed question with a sketch of the wood burning stove.',
    'q4-original': 'Original SEC 2010 Ordinary Construction Studies Question 4: the printed question with a sketch of the solid pine door and frame.',
    'q5-original': 'Original SEC 2010 Ordinary Construction Studies Question 5: the printed question with a sketch of the stud partition with its flush door.',
    'q6-original': 'Original SEC 2010 Ordinary Construction Studies Question 6: the printed question on ladder, veneering knife, jig saw and outdoor tool safety.',
    'q7-original': 'Original SEC 2010 Ordinary Construction Studies Question 7: the printed question with a sketch of the lean-to extension and the underground rainwater tank.',
    'q8-original': 'Original SEC 2010 Ordinary Construction Studies Question 8: the printed list of nine construction terms.',
    'q9-original': 'Original SEC 2010 Ordinary Construction Studies Question 9: the printed question with a sketch of the terrace of traditional houses.',
    'q1-section': 'SEC model section through the strip foundation, cavity wall and solid floor, with the specification list and the cold-bridge details.',
    'q2-injecting': 'SEC 2010 Ordinary marking scheme notes and sketch on injecting cavity insulation.',
    'q2-pros-cons': 'SEC 2010 Ordinary marking scheme notes and sketch on the advantages and disadvantages of cavity fill.',
    'q2-attic': 'SEC 2010 Ordinary marking scheme notes and sketches on insulating the attic and the water storage tank (two pages).',
    'q3-system': 'SEC single-line diagram of the stove, back boiler, cylinder and expansion tank, with the list of components.',
    'q3-advantages': 'SEC 2010 Ordinary marking scheme notes on the advantages of a wood burning stove for hot water.',
    'q4-scheme': 'SEC 2010 Ordinary marking scheme notes and sketches on squaring the doorframe, fixing it in the wall and fitting a butt hinge.',
    'q5-scheme': 'SEC model section through the stud partition, door and floor, with the specification list and sound methods.',
    'q6-precautions': 'SEC 2010 Ordinary marking scheme notes on ladder, veneering knife and jig saw safety (two pages).',
    'q6-outdoors': 'SEC 2010 Ordinary marking scheme notes and sketches on using electrical tools out of doors.',
    'q7-scheme': 'SEC 2010 Ordinary marking scheme notes and sketch of the gutter, downpipe, gully, filter and underground storage tank.',
    'q7-uses': 'SEC 2010 Ordinary marking scheme notes on the advantages and uses of stored rainwater.',
    'q8-terms': 'SEC 2010 Ordinary marking scheme notes and sketches for all nine terms — concrete lintel, door saddle, triple glazing, mortice and tenon joint, quarter sawing, window cill, energy rating, ridge board and vapour barrier (two pages).',
    'q9-reasons': 'SEC 2010 Ordinary marking scheme notes on repairing rather than replacing wooden windows.',
    'q9-glass': 'SEC 2010 Ordinary marking scheme notes and sketch on replacing a broken pane of glass.',
    'q9-paint': 'SEC 2010 Ordinary marking scheme notes and sketch on stripping, preparing and repainting a window frame.',
}
cp.integrate(paper, HERE, ALT)
