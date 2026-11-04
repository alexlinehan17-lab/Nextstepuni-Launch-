"""Integrate the validated 2019 Ordinary Q1-Q9 draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2019_ordinary as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2019 Ordinary Construction Studies Question 1: the printed question with a sketch of a casement window in a rendered cavity wall.',
    'q2-original': 'Original SEC 2019 Ordinary Construction Studies Question 2: the printed question with a sketch of the ceiling joists and the attic trapdoor.',
    'q3-original': 'Original SEC 2019 Ordinary Construction Studies Question 3: the printed question with a section of a two-storey house and a sketch of a toilet isolating valve.',
    'q4-original': 'Original SEC 2019 Ordinary Construction Studies Question 4: the printed question with a sketch of a cavity wall on a reinforced concrete strip foundation.',
    'q5-original': 'Original SEC 2019 Ordinary Construction Studies Question 5: the printed question with a sketch of a stud partition on a floating timber floor.',
    'q6-original': 'Original SEC 2019 Ordinary Construction Studies Question 6: the printed question with a sketch of a bandsaw.',
    'q7-original': 'Original SEC 2019 Ordinary Construction Studies Question 7: the printed question with the draft plan of the kitchen area A and dining area B.',
    'q8-original': 'Original SEC 2019 Ordinary Construction Studies Question 8: the printed instruction and the nine construction terms.',
    'q9-original': 'Original SEC 2019 Ordinary Construction Studies Question 9: the printed question with a sketch of a timber-clad home office in a garden.',
    'q1-scheme': 'SEC model section through the window head with the cavity closer marked (b), the specification list and the notes for part (b).',
    'q2-attic': 'SEC model sketch of the insulated attic with the method, insulation types and 350 mm minimum thickness.',
    'q2-trapdoor': 'SEC 2019 Ordinary marking scheme notes and sketches on insulating and sealing the attic trapdoor.',
    'q2-reasons': 'SEC 2019 Ordinary marking scheme notes on reasons to begin by insulating the attic.',
    'q3-system': 'SEC model sketch of the cold water supply from the rising main to the storage tank, kitchen sink and toilet cistern, with the typical details list.',
    'q3-valve': 'SEC model sketch of the isolating valve beside the toilet cistern, with the reasons.',
    'q3-dual-flush': 'SEC 2019 Ordinary marking scheme notes on advantages of a dual-flush toilet cistern.',
    'q4-foundation': 'SEC model sketches of the 1100 × 350 mm reinforced strip foundation with the wall centred and the steel near the bottom, with notes.',
    'q4-ties': 'SEC 2019 Ordinary marking scheme notes and sketch on wall ties connecting the inner and outer leaves.',
    'q4-ready-mix': 'SEC 2019 Ordinary marking scheme notes on advantages of ready-mixed concrete for foundations.',
    'q5-scheme': 'SEC model section through the floor and stud partition with the partition insulation marked (b), the specification list and the notes for part (b).',
    'q6-adhesive': 'SEC 2019 Ordinary marking scheme notes on safety precautions when using a contact adhesive to glue veneers.',
    'q6-screwdriver': 'SEC 2019 Ordinary marking scheme notes on safety precautions when using a battery-powered screwdriver.',
    'q6-precautions': 'SEC 2019 Ordinary marking scheme notes on safety precautions for both situations: contact adhesive and battery-powered screwdriver.',
    'q6-bandsaw': 'SEC 2019 Ordinary marking scheme table of bandsaw safety precautions and reasons, with sketches of the bandsaw, a push stick and safety glasses (two pages).',
    'q6-instruction': 'SEC 2019 Ordinary marking scheme notes on reasons for safety instruction before using machinery.',
    'q7-layout': 'SEC model kitchen layout with the sink, cooker and fridge in a work triangle, and the reasons for each location.',
    'q7-floors': 'SEC 2019 Ordinary marking scheme notes on floor types for kitchen area A and dining area B (two pages).',
    'q7-island': 'SEC model kitchen plan with an island unit, and the advantages of an island unit.',
    'q8-terms': 'SEC 2019 Ordinary marking scheme notes and sketches for all nine terms: carbon monoxide alarm, laminated safety glass, sapwood, grab rail, eaves gutter, bridle joint, furniture castor, balusters and fluorescent lighting (two pages).',
    'q9-cladding': 'SEC 2019 Ordinary marking scheme notes on suitable woods for external cladding and the reasons, with a sketch of the home office.',
    'q9-modification': 'SEC 2019 Ordinary marking scheme notes on modifications linking the office to the garden, with sketches of glazed doors and full-height glazing.',
    'q9-advantages': 'SEC 2019 Ordinary marking scheme notes on advantages of a visual connection with the garden.',
}
cp.integrate(paper, HERE, ALT)
