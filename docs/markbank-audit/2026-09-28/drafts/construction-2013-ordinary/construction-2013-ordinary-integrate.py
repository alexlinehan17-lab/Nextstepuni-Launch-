"""Integrate the validated 2013 Ordinary Q1-Q9 draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2013_ordinary as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2013 Ordinary Construction Studies Question 1: the printed question with a sketch of the felted flat roof at the eaves.',
    'q2-original': 'Original SEC 2013 Ordinary Construction Studies Question 2: the printed question with a sketch of the dwelling house.',
    'q3-original': 'Original SEC 2013 Ordinary Construction Studies Question 3: the printed question with a sketch of a bathroom with a bath and wash hand basin.',
    'q4-original': 'Original SEC 2013 Ordinary Construction Studies Question 4: the printed question with a sketch of the corner of a foundation trench with its profiles.',
    'q5-original': 'Original SEC 2013 Ordinary Construction Studies Question 5: the printed question with a sketch of the stud partition on the timber floor and block wall.',
    'q6-original': 'Original SEC 2013 Ordinary Construction Studies Question 6: the printed question with a sketch of a building site.',
    'q7-original': 'Original SEC 2013 Ordinary Construction Studies Question 7: the printed question with a sketch of the ground floor meeting the cavity wall.',
    'q8-original': 'Original SEC 2013 Ordinary Construction Studies Question 8: the printed list of nine construction terms.',
    'q9-original': 'Original SEC 2013 Ordinary Construction Studies Question 9: the printed question with a sketch of the glazed oak double doors.',
    'q1-section': 'SEC model sections through the flat roof eaves on the cavity wall, with the specification list.',
    'q1-rainwater': 'SEC 2013 Ordinary marking scheme notes on removing rainwater from the flat roof.',
    'q2-systems': 'SEC 2013 Ordinary marking scheme notes and sketches on filling the cavity and on insulating the inside of the walls.',
    'q2-advantages': 'SEC 2013 Ordinary marking scheme notes on the advantages of insulating the external walls.',
    'q3-system': 'SEC single-line diagram of the hot and cold supply to the bath and basin, with the list of components.',
    'q3-tap': 'SEC 2013 Ordinary marking scheme notes and sketches of lever taps for limited hand mobility.',
    'q4-setting-out': 'SEC 2013 Ordinary marking scheme notes and sketches on levelling the profiles, locating and squaring the trench and setting the concrete level.',
    'q4-strip': 'SEC model sketch of a reinforced strip foundation with dimensions.',
    'q5-scheme': 'SEC model section through the stud partition and the timber floor, with the specification list.',
    'q6-signs': 'SEC safety signs for eye protection, ear protection and safety gloves.',
    'q6-tasks': 'SEC 2013 Ordinary marking scheme notes on tasks needing eye protection, ear protection and safety gloves.',
    'q6-other': 'SEC 2013 Ordinary marking scheme notes on a high visibility jacket, a safety helmet and steel cap boots (two pages).',
    'q7-floor': 'SEC model sketch of the insulated solid ground floor at the cavity wall, with the specification list.',
    'q7-cold-bridge': 'SEC 2013 Ordinary marking scheme notes on preventing a cold bridge at the floor and wall junction.',
    'q7-covering': 'SEC 2013 Ordinary marking scheme notes on bathroom floor coverings — ceramic tiles, vinyl, cork, linoleum, marmoleum and natural stone.',
    'q8-terms': 'SEC 2013 Ordinary marking scheme notes and sketches for all nine terms — solar panel, flue liner, wind turbine, dovetail halving joint, purlin, low-e coating, sash cramp, water table and vapour barrier (three pages).',
    'q9-joint': 'SEC 2013 Ordinary marking scheme notes and sketches of the haunched, rebated mortise and tenon joint.',
    'q9-glass': 'SEC 2013 Ordinary marking scheme notes and step sketches on fitting a glass panel in the door.',
    'q9-advantages': 'SEC 2013 Ordinary marking scheme notes on the advantages of glazed double doors.',
}
cp.integrate(paper, HERE, ALT)
