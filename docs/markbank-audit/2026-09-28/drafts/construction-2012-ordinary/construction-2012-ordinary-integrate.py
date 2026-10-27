"""Integrate the validated 2012 Ordinary Q1-Q9 draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2012_ordinary as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2012 Ordinary Construction Studies Question 1: the printed question with a sketch of the tiled roof at the eaves.',
    'q2-original': 'Original SEC 2012 Ordinary Construction Studies Question 2: the printed question with a sketch of the rendered house.',
    'q3-original': 'Original SEC 2012 Ordinary Construction Studies Question 3: the printed question with a sketch of the kitchen sink and tap.',
    'q4-original': 'Original SEC 2012 Ordinary Construction Studies Question 4: the printed question with a sketch of the cavity wall on its strip foundation.',
    'q5-original': 'Original SEC 2012 Ordinary Construction Studies Question 5: the printed question with a sketch of the triple-glazed casement window.',
    'q6-original': 'Original SEC 2012 Ordinary Construction Studies Question 6: the printed question with a sketch of a worker carrying a load.',
    'q7-original': 'Original SEC 2012 Ordinary Construction Studies Question 7: the printed question with a sketch of the house and garage to be converted.',
    'q8-original': 'Original SEC 2012 Ordinary Construction Studies Question 8: the printed list of nine construction terms.',
    'q9-original': 'Original SEC 2012 Ordinary Construction Studies Question 9: the printed question with a sketch of the solid oak dining table.',
    'q1-section': 'SEC model sections through the tiled roof at the eaves on the cavity wall, with the specification list.',
    'q1-closer': 'SEC 2012 Ordinary marking scheme notes on closing the cavity at eaves level.',
    'q2-method': 'SEC 2012 Ordinary marking scheme notes and sketch on an external insulation system and its insulation materials.',
    'q2-advantages': 'SEC 2012 Ordinary marking scheme notes on the advantages of external wall insulation.',
    'q3-system': 'SEC single-line diagram of the mains supply through the wall to the kitchen sink, with the list of components.',
    'q3-frost': 'SEC 2012 Ordinary marking scheme notes on protecting the mains supply from frost.',
    'q3-saving': 'SEC 2012 Ordinary marking scheme notes and sketch on reducing the use of treated water.',
    'q4-design': 'SEC 2012 Ordinary marking scheme notes and sketches on the trench, concrete level, reinforcement and wall position of a strip foundation (two pages).',
    'q4-reasons': 'SEC 2012 Ordinary marking scheme notes on the environmental reasons for a strip foundation.',
    'q5-scheme': 'SEC model section through the window cill in the cavity wall, with the specification list and the cold-bridge detail.',
    'q6-precautions': 'SEC 2012 Ordinary marking scheme notes and sketch on safe lifting and on placing concrete from a ready-mix truck (two pages).',
    'q6-ppe': 'SEC 2012 Ordinary marking scheme notes and sketches on a high visibility jacket, a safety helmet and steel cap boots.',
    'q7-reasons': 'SEC 2012 Ordinary marking scheme notes on why planning permission is needed for the conversion.',
    'q7-documents': 'SEC 2012 Ordinary marking scheme notes on the site location map and the site notice.',
    'q7-refusal': 'SEC 2012 Ordinary marking scheme notes on reasons to refuse permission for the conversion.',
    'q8-terms': 'SEC 2012 Ordinary marking scheme notes and sketches for all nine terms — rainwater butt, wall tie, newel post, box dovetail joint, gully trap, through and through sawing, compression joint, angle bead and biscuit joint (three pages).',
    'q9-joint': 'SEC 2012 Ordinary marking scheme notes and sketches of a haunched mortise and tenon and a dowel joint.',
    'q9-restore': 'SEC 2012 Ordinary marking scheme notes and sketches on restoring the tabletop.',
    'q9-finish': 'SEC 2012 Ordinary marking scheme notes and sketches on varnish, lacquer, wax and oil finishes.',
}
cp.integrate(paper, HERE, ALT)
