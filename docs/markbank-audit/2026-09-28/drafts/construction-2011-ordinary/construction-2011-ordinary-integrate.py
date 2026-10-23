"""Integrate the validated 2011 Ordinary Q1-Q9 draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2011_ordinary as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2011 Ordinary Construction Studies Question 1: the printed question with a sketch of the triple-glazed casement window in the wall.',
    'q2-original': 'Original SEC 2011 Ordinary Construction Studies Question 2: the printed question with a sketch of the forty-year-old house.',
    'q3-original': 'Original SEC 2011 Ordinary Construction Studies Question 3: the printed question with a sketch of the bathroom with a basin and mixer shower.',
    'q4-original': 'Original SEC 2011 Ordinary Construction Studies Question 4: the printed question with a sketch of the kitchen layout.',
    'q5-original': 'Original SEC 2011 Ordinary Construction Studies Question 5: the printed question with a sketch of the closed string stairs.',
    'q6-original': 'Original SEC 2011 Ordinary Construction Studies Question 6: the printed question on fitting a cill, working at height and lathe safety.',
    'q7-original': 'Original SEC 2011 Ordinary Construction Studies Question 7: the printed question with an outline of the house, the underground rainwater tank and the attic tank.',
    'q8-original': 'Original SEC 2011 Ordinary Construction Studies Question 8: the printed list of nine construction terms.',
    'q9-original': 'Original SEC 2011 Ordinary Construction Studies Question 9: the printed question with a sketch of the wooden garden seat.',
    'q1-section': 'SEC model section through the window head and lintels in the cavity wall, with the specification list and the flashing and insulation details.',
    'q2-systems': 'SEC 2011 Ordinary marking scheme notes and sketches on injecting cavity insulation and fixing internal insulation.',
    'q2-pros-cons': 'SEC 2011 Ordinary marking scheme notes on the advantages and disadvantages of cavity fill and internal insulation (two pages).',
    'q3-system': 'SEC single-line diagrams of the hot and cold supply to the basin and mixer shower, with the list of components.',
    'q3-shower': 'SEC 2011 Ordinary marking scheme notes on the advantages of a mixer shower over an electric power shower.',
    'q4-cabinets': 'SEC 2011 Ordinary marking scheme notes and sketches on fixing overhead cabinets to a block wall.',
    'q4-floor': 'SEC 2011 Ordinary marking scheme notes and sketches on fitting a solid wood floor and suitable woods.',
    'q4-layout': 'SEC 2011 Ordinary marking scheme notes on the advantages of the sink, cooker and fridge positions.',
    'q5-scheme': 'SEC model section through the bottom steps of the closed string stairs, with specifications and the anti-creak details.',
    'q6-precautions': 'SEC 2011 Ordinary marking scheme notes on fitting a precast cill and working at height.',
    'q6-lathe': 'SEC 2011 Ordinary marking scheme notes and sketches on wood turning lathe safety.',
    'q7-pump': 'SEC 2011 Ordinary marking scheme notes and sketch on pumping rainwater from the underground tank to the attic tank.',
    'q7-appliance': 'SEC 2011 Ordinary marking scheme notes and sketch on connecting the toilet or washing machine to the attic rainwater tank.',
    'q7-reason': 'SEC 2011 Ordinary marking scheme notes on why rainwater is stored in a separate attic tank.',
    'q8-terms': 'SEC 2011 Ordinary marking scheme notes and sketches for all nine terms — fascia, window board, solar panel, strip foundation, butt hinge, wall tie, thermostatic valve, rafter and radon barrier (two pages).',
    'q9-feature': 'SEC 2011 Ordinary marking scheme notes and sketch on the slatted seat design for outdoor use.',
    'q9-joint': 'SEC 2011 Ordinary marking scheme notes and sketch of a mortise and tenon joint for the arm rest.',
    'q9-finish': 'SEC 2011 Ordinary marking scheme notes and sketches on preparing the seat and applying paint, varnish, stain or Danish oil (two pages).',
}
cp.integrate(paper, HERE, ALT)
