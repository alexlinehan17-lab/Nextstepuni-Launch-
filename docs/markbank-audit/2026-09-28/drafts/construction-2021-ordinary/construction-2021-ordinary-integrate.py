"""Integrate the validated 2021 Ordinary Q1-Q9 draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2021_ordinary as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2021 Ordinary Construction Studies Question 1: the printed question with a sketch of the slated eaves of a cut roof with its gutter.',
    'q2-original': 'Original SEC 2021 Ordinary Construction Studies Question 2: the printed question with a sketch of a ground floor being insulated.',
    'q3-original': 'Original SEC 2021 Ordinary Construction Studies Question 3: the printed question with sketches of a kitchen sink and a water meter.',
    'q4-original': 'Original SEC 2021 Ordinary Construction Studies Question 4: the printed question with a sketch of a proposed town house.',
    'q5-original': 'Original SEC 2021 Ordinary Construction Studies Question 5: the printed question with a sketch of a triple-glazed window on its cill.',
    'q6-original': 'Original SEC 2021 Ordinary Construction Studies Question 6: the printed question with a sketch of an excavator digging a trench.',
    'q7-original': 'Original SEC 2021 Ordinary Construction Studies Question 7: the printed question with the draft plan of a living room beside a kitchen.',
    'q8-original': 'Original SEC 2021 Ordinary Construction Studies Question 8: the printed list of nine construction terms.',
    'q9-original': 'Original SEC 2021 Ordinary Construction Studies Question 9: the printed question with a sketch of softwood decking behind a house.',
    'q1-scheme': 'SEC model section through the cut-roof eaves and cavity wall with the gutter marked (b), and the specification list.',
    'q2-advantages': 'SEC 2021 Ordinary marking scheme notes on the advantages of a highly insulated ground floor.',
    'q2-method': 'SEC 2021 Ordinary marking scheme notes on insulating a solid ground floor, with sketches of the insulation boards and membrane, and the insulation types and thickness.',
    'q2-floor': 'SEC 2021 Ordinary marking scheme table of kitchen floor types (tiles, solid wood, laminate, polished concrete, natural stone) with reasons for each.',
    'q3-system': 'SEC model single-line diagram of the cold water supply from the main through the meter to the sink and attic tank, with the typical details.',
    'q3-meter': 'SEC 2021 Ordinary marking scheme notes on the advantages of a water meter.',
    'q4-reasons': 'SEC 2021 Ordinary marking scheme notes on why planning permission is needed.',
    'q4-documents': 'SEC 2021 Ordinary marking scheme notes on the site notice and site location map, with sketches of each.',
    'q4-town': 'SEC 2021 Ordinary marking scheme table of the advantages and disadvantages of building in a town.',
    'q5-scheme': 'SEC model section through the cavity wall and window cill with the drip marked (b), the specification list and the cill detail.',
    'q6-signs': 'SEC model PPE signs for a high-visibility vest, safety boots and a safety helmet, each with its reason.',
    'q6-risks': 'SEC 2021 Ordinary marking scheme notes on risks in deep trenches, with a sketch of an excavator and ladder.',
    'q6-trench': 'SEC 2021 Ordinary marking scheme notes on trench safety precautions, with sketches of shoring and barriers.',
    'q7-access': 'SEC 2021 Ordinary marking scheme notes on direct kitchen access, with a sketch of the door between the rooms.',
    'q7-layout': 'SEC model living room plan with the sofas, stove and television placed, and the reasons for each location (two pages).',
    'q7-stove': 'SEC 2021 Ordinary marking scheme notes on the advantages of a wood-burning stove.',
    'q8-terms': 'SEC marking-scheme notes and sketches for all nine Question 8 terms, in scheme order: joist bridging, working drawing, roof light, steel reinforcement, heat pump, ridge board, biscuit joint, room thermostat and building energy rating (two pages).',
    'q9-finish': 'SEC 2021 Ordinary marking scheme notes on finishes for decking and reasons.',
    'q9-winter': 'SEC 2021 Ordinary marking scheme notes on making the space usable in winter, with sketches of a windbreak and a roofed deck.',
    'q9-advantages': 'SEC 2021 Ordinary marking scheme notes on the advantages of an outdoor living space, with a sketch of an outdoor fireplace.',
}
cp.integrate(paper, HERE, ALT, anchor_from_sidecar=True)
