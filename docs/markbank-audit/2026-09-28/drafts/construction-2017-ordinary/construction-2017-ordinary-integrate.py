"""Integrate the validated 2017 Ordinary Q1-Q9 draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2017_ordinary as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2017 Ordinary Construction Studies Question 1: the printed question with a sketch of an insulated wooden door with vertical sheeting.',
    'q2-original': 'Original SEC 2017 Ordinary Construction Studies Question 2: the printed question with a sketch of a block outer leaf and timber frame inner leaf.',
    'q3-original': 'Original SEC 2017 Ordinary Construction Studies Question 3: the printed question with a section of a house with a solar panel and cylinder.',
    'q4-original': 'Original SEC 2017 Ordinary Construction Studies Question 4: the printed question with a sketch of waste materials from a house under repair.',
    'q5-original': 'Original SEC 2017 Ordinary Construction Studies Question 5: the printed question with a sketch of a casement window and cill.',
    'q6-original': 'Original SEC 2017 Ordinary Construction Studies Question 6: the printed question with a sketch of a site entrance with safety signs.',
    'q7-original': 'Original SEC 2017 Ordinary Construction Studies Question 7: the printed question with a sketch of an attic being converted to a bedroom.',
    'q8-original': 'Original SEC 2017 Ordinary Construction Studies Question 8: the printed instruction and the nine construction terms.',
    'q9-original': 'Original SEC 2017 Ordinary Construction Studies Question 9: the printed question with a sketch of sliding doors opening on to a timber-decked patio.',
    'q1-scheme': 'SEC model sections through the door head, lintels and cavity wall with the DPC marked (b), the specification list and the notes for part (b).',
    'q2-method': 'SEC 2017 Ordinary marking scheme notes and sketch on insulating the timber frame inner leaf, with insulation types and thickness.',
    'q2-advantages': 'SEC 2017 Ordinary marking scheme notes on advantages of insulating the inner leaf.',
    'q2-finish': 'SEC 2017 Ordinary marking scheme sketches of taping joints and skimming plasterboard.',
    'q3-system': 'SEC model sketch of the solar panel, cylinder and pipework supplying hot water to a kitchen sink, with typical sizes.',
    'q3-solar': 'SEC 2017 Ordinary marking scheme notes on advantages of solar water heating.',
    'q3-tap': 'SEC 2017 Ordinary marking scheme notes and sketches of lever and swivel-neck taps for limited hand mobility.',
    'q4-sorting': 'SEC 2017 Ordinary marking scheme sketches and notes on sorting and storing waste on site.',
    'q4-reasons': 'SEC 2017 Ordinary marking scheme notes on reasons to minimise waste on site.',
    'q4-uses': 'SEC 2017 Ordinary marking scheme notes on reusing sorted wood and the reasons (two pages).',
    'q5-scheme': 'SEC model sections through the window cill and cavity wall with the insulation behind the cill marked (b), and the detail list.',
    'q6-signs': 'SEC 2017 Ordinary marking scheme notes on reasons for safety signs at a site entrance.',
    'q6-ppe': 'SEC 2017 Ordinary marking scheme notes, signs and reasons for a hard hat, safety boots and a high-visibility vest.',
    'q6-power-tools': 'SEC 2017 Ordinary marking scheme notes on safety precautions with electric power tools.',
    'q7-joists': 'SEC 2017 Ordinary marking scheme sketches and notes on herringbone and solid strutting between floor joists.',
    'q7-joint': 'SEC 2017 Ordinary marking scheme sketches and notes on tongue-and-groove flooring.',
    'q7-attic': 'SEC 2017 Ordinary marking scheme notes on an advantage and a disadvantage of an attic conversion.',
    'q8-terms': 'SEC 2017 Ordinary marking scheme notes and sketches for all nine terms: hand rail, damp-proof course, wind turbine, box dovetail joint, ball valve, joist hanger, purlin, energy rating and service cavity (four pages).',
    'q9-decking': 'SEC 2017 Ordinary marking scheme sketches and notes on fixing decking boards to the joists.',
    'q9-finish': 'SEC 2017 Ordinary marking scheme notes and sketches on applying a finish to the decking.',
    'q9-patio': 'SEC 2017 Ordinary marking scheme notes on advantages of an external patio.',
}
cp.integrate(paper, HERE, ALT)
