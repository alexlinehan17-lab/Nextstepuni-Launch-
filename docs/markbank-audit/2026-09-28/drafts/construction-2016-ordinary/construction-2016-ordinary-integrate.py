"""Integrate the validated 2016 Ordinary Q1-Q9 draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2016_ordinary as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2016 Ordinary Construction Studies Question 1: the printed question with a cutaway sketch of the cavity wall and timber-finished ground floor.',
    'q2-original': 'Original SEC 2016 Ordinary Construction Studies Question 2: the printed question with a sketch of the attic with its rafters, joists and water tank.',
    'q3-original': 'Original SEC 2016 Ordinary Construction Studies Question 3: the printed question with a section of the house with the stove, cylinder, tanks and solar collector.',
    'q4-original': 'Original SEC 2016 Ordinary Construction Studies Question 4: the printed question with a sketch of a house with a sunspace on its gable.',
    'q5-original': 'Original SEC 2016 Ordinary Construction Studies Question 5: the printed question with a sketch of a cut string stairs to a landing.',
    'q6-original': 'Original SEC 2016 Ordinary Construction Studies Question 6: the printed question with a sketch of a bowl being turned on a lathe.',
    'q7-original': 'Original SEC 2016 Ordinary Construction Studies Question 7: the printed question with a sketch of a stud partition with a door between two bedrooms.',
    'q8-original': 'Original SEC 2016 Ordinary Construction Studies Question 8: the printed instruction and the nine construction terms.',
    'q9-original': 'Original SEC 2016 Ordinary Construction Studies Question 9: the printed question with a sketch of a timber-clad garden room.',
    'q1-scheme': 'SEC model sections through the strip foundation, cavity wall and ground floor with the thermal-bridge detail marked (b), the specification list and the notes for part (b).',
    'q2-attic': 'SEC model sketches of the insulated attic, the insulated tank on its supports and the lagged pipework.',
    'q2-reasons': 'SEC 2016 Ordinary marking scheme notes on reasons to insulate the attic first.',
    'q3-system': 'SEC model sketch of the stove, cylinder, tanks and solar collector pipework, with the secondary and primary circulation details.',
    'q3-solar': 'SEC 2016 Ordinary marking scheme notes on connecting the solar collector to the cylinder.',
    'q3-advantages': 'SEC 2016 Ordinary marking scheme notes on advantages of a solar collector for hot water.',
    'q4-reasons': 'SEC 2016 Ordinary marking scheme notes on why planning permission is needed for the sunspace, with a sketch.',
    'q4-documents': 'SEC 2016 Ordinary marking scheme notes on the information on the site layout map and the newspaper planning notice.',
    'q4-public': 'SEC 2016 Ordinary marking scheme notes on why the public may view planning documents.',
    'q5-scheme': 'SEC model section through the bottom three steps of the cut string stairs with the baluster joint marked (b), and the details.',
    'q6-precautions': 'SEC 2016 Ordinary marking scheme notes on safety precautions with a scalpel, carrying a chisel and using contact adhesive.',
    'q6-lathe': 'SEC 2016 Ordinary marking scheme notes and sketches on safety precautions when turning a bowl on a lathe.',
    'q7-partition': 'SEC model sketches of the stud partition framing around the door opening, with typical sizes.',
    'q7-sound': 'SEC 2016 Ordinary marking scheme plan views and notes on reducing sound through the stud partition (two pages).',
    'q7-finish': 'SEC 2016 Ordinary marking scheme notes on two methods of finishing plasterboard before painting.',
    'q8-terms': 'SEC 2016 Ordinary marking scheme notes and sketches for all nine terms: lever valve, thermal bridge, solar gain, mortice and tenon joint, dual flush toilet, low-e glazing, cob wall, smart meter and access ramp (four pages).',
    'q9-wood': 'SEC 2016 Ordinary marking scheme notes on suitable woods for cladding — cedar, larch and Douglas fir — and the reasons (two pages).',
    'q9-finish': 'SEC 2016 Ordinary marking scheme notes and sketches on applying a finish to the cladding.',
    'q9-eco': 'SEC 2016 Ordinary marking scheme notes on eco-friendly features of the garden room.',
}
cp.integrate(paper, HERE, ALT)
