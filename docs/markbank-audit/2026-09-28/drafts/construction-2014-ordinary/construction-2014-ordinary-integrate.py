"""Integrate the validated 2014 Ordinary Q1-Q9 draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2014_ordinary as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2014 Ordinary Construction Studies Question 1: the printed question with a cutaway sketch of the cavity wall and the timber first floor.',
    'q2-original': 'Original SEC 2014 Ordinary Construction Studies Question 2: the printed question with a sketch of a house with a single storey extension.',
    'q3-original': 'Original SEC 2014 Ordinary Construction Studies Question 3: the printed question with a sketch of a modern wood burning stove.',
    'q4-original': 'Original SEC 2014 Ordinary Construction Studies Question 4: the printed question with a sketch of the stud partition between the kitchen and living room.',
    'q5-original': 'Original SEC 2014 Ordinary Construction Studies Question 5: the printed question with a sketch of the tiled cut roof at the ridge.',
    'q6-original': 'Original SEC 2014 Ordinary Construction Studies Question 6: the printed question with a sketch of a site office in front of houses under construction.',
    'q7-original': 'Original SEC 2014 Ordinary Construction Studies Question 7: the printed question with a sketch of a two-storey house with a slated roof.',
    'q8-original': 'Original SEC 2014 Ordinary Construction Studies Question 8: the printed list of nine construction terms.',
    'q9-original': 'Original SEC 2014 Ordinary Construction Studies Question 9: the printed question with the plan of the small kitchen, the worktop A and the windows.',
    'q1-scheme': 'SEC model sections through the cavity wall and first floor joists, minimum standard and best practice with service cavities, with the detail list and joist bridging (two pages).',
    'q2-fixing': 'SEC 2014 Ordinary marking scheme notes and sketch on fixing external insulation boards to the solid block wall.',
    'q2-finish': 'SEC 2014 Ordinary marking scheme notes and sketch on applying the base coat, reinforcing mesh and acrylic finish to the insulation.',
    'q2-advantages': 'SEC 2014 Ordinary marking scheme notes on the advantages of insulating the external walls.',
    'q3-system': 'SEC single-line diagram of the hot water supply to the sink from a wood burning stove and indirect cylinder, with the secondary and primary circulation lists.',
    'q3-solar': 'SEC 2014 Ordinary marking scheme notes on the advantages of a solar panel for domestic hot water.',
    'q4-partition': 'SEC 2014 Ordinary marking scheme notes and sketch of the timber stud partition with typical sizes.',
    'q4-socket': 'SEC 2014 Ordinary marking scheme notes and sketches on fixing a metal socket box or a dry lining back box in the partition.',
    'q4-skim': 'SEC 2014 Ordinary marking scheme notes and sketches on the steps of applying a plaster skim finish (two pages).',
    'q5-scheme': 'SEC model sections through the cut roof at the ridge, typical and best practice, with the specification list (two pages).',
    'q5-vent': 'SEC 2014 Ordinary marking scheme notes on ventilating the roof with ridge vents or vent tiles.',
    'q6-signs': 'SEC safety signs for a safety helmet, a high visibility vest and safety boots.',
    'q6-reasons': 'SEC 2014 Ordinary marking scheme notes on why a safety helmet, a high visibility vest and safety boots must be worn (two pages).',
    'q6-visitors': 'SEC 2014 Ordinary marking scheme notes on why visitors must report to the site office.',
    'q7-collection': 'SEC 2014 Ordinary marking scheme notes and sketches on collecting rainwater in an underground storage tank or a water butt (two pages).',
    'q7-uses': 'SEC 2014 Ordinary marking scheme notes on the advantages of storing rainwater and its uses.',
    'q7-meter': 'SEC 2014 Ordinary marking scheme notes on an advantage and a disadvantage of a water meter.',
    'q8-terms': 'SEC 2014 Ordinary marking scheme notes and sketches for all nine terms — strip foundation, thermostatic valve, roof-light window, housing joint, collar tie, smart meter, laser beam, radon sump and external ramp (three pages).',
    'q9-layout': 'SEC 2014 Ordinary marking scheme kitchen plan with the sink, cooker and fridge located, and the reasons for each.',
    'q9-paint': 'SEC 2014 Ordinary marking scheme notes and sketches on preparing and hand painting a cabinet door.',
    'q9-worktop': 'SEC 2014 Ordinary marking scheme notes on the advantages and disadvantages of granite and solid wood worktops and the recommendation (two pages).',
}
cp.integrate(paper, HERE, ALT)
