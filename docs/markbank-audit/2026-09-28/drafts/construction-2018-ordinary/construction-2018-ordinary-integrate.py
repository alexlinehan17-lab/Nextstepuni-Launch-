"""Integrate the validated 2018 Ordinary Q1-Q9 draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2018_ordinary as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2018 Ordinary Construction Studies Question 1: the printed question with a sketch of a flush door in a plastered block wall on a timber floor.',
    'q2-original': 'Original SEC 2018 Ordinary Construction Studies Question 2: the printed question with a sketch of a plastered hollow block wall.',
    'q3-original': 'Original SEC 2018 Ordinary Construction Studies Question 3: the printed question with a sketch of a wood-burning stove with a back boiler.',
    'q4-original': 'Original SEC 2018 Ordinary Construction Studies Question 4: the printed question with a sketch of one corner of a strip foundation trench with profiles.',
    'q5-original': 'Original SEC 2018 Ordinary Construction Studies Question 5: the printed question with a sketch of the eaves of a felted flat roof.',
    'q6-original': 'Original SEC 2018 Ordinary Construction Studies Question 6: the printed question with a sketch of a building site with safety signage.',
    'q7-original': 'Original SEC 2018 Ordinary Construction Studies Question 7: the printed question with a section of a house and an underground rainwater tank.',
    'q8-original': 'Original SEC 2018 Ordinary Construction Studies Question 8: the printed instruction and the nine construction terms.',
    'q9-original': 'Original SEC 2018 Ordinary Construction Studies Question 9: the printed question with a sketch of an opening between a sitting room and a dining room.',
    'q1-scheme': 'SEC model section through the internal wall, door, strip foundation and ground floor with the radon barrier marked (b), the specification list and the notes for part (b).',
    'q2-method': 'SEC 2018 Ordinary marking scheme notes and sketch on fixing external expanded polystyrene insulation to the wall, and its thickness.',
    'q2-finish': 'SEC 2018 Ordinary marking scheme notes and sketch on applying the surface finish to the insulation.',
    'q2-advantages': 'SEC 2018 Ordinary marking scheme notes on advantages and disadvantages of external insulation.',
    'q3-system': 'SEC model single-line diagram of the hot water supply to a shower from a stove back boiler, with the secondary and primary circulation details (two pages).',
    'q3-stove': 'SEC 2018 Ordinary marking scheme notes on advantages of a wood-burning stove for heating water.',
    'q4-environment': 'SEC 2018 Ordinary marking scheme notes on environmental reasons for a strip foundation.',
    'q4-setting-out': 'SEC 2018 Ordinary marking scheme notes and sketches on profiles, trench width and depth, and the position of the wall.',
    'q4-level': 'SEC 2018 Ordinary marking scheme notes and sketch on levelling pegs for the top of the foundation.',
    'q5-scheme': 'SEC model sections through the flat roof eaves and cavity wall with the soffit ventilation marked (b), the specification lists and the notes for part (b) (two pages).',
    'q6-signs': 'SEC model safety signs for a high-visibility vest, protective footwear and a safety helmet.',
    'q6-features': 'SEC 2018 Ordinary marking scheme notes and sketches on the design features of the vest, footwear and helmet.',
    'q6-other': 'SEC 2018 Ordinary marking scheme notes on other PPE — eye protection, ear protection and safety gloves — and the reasons.',
    'q7-collection': 'SEC model sketch of the gutters, downpipes, filter and pipes conveying rainwater to the underground tank, with typical sizes.',
    'q7-pumping': 'SEC model sketch of the pump and pipework from the underground tank to the attic tank and toilet cistern, with typical details.',
    'q7-advantage': 'SEC 2018 Ordinary marking scheme notes on advantages of an underground rainwater tank.',
    'q8-terms': 'SEC 2018 Ordinary marking scheme notes and sketches for all nine terms: smart meter, airtightness tape, roof light window, biscuit joint, evacuated tube, aerated shower, earth rod, magnetic catch and LED lighting (three pages).',
    'q9-support': 'SEC 2018 Ordinary marking scheme notes and sketch on a concrete lintel supporting the blockwork over the opening.',
    'q9-frame': 'SEC 2018 Ordinary marking scheme notes and sketches on holding the doorframe square and fixing it to the wall.',
    'q9-glazed': 'SEC 2018 Ordinary marking scheme notes on advantages and disadvantages of glazed double doors between the rooms.',
}
cp.integrate(paper, HERE, ALT)
