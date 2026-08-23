#!/usr/bin/env python3
"""Construction Studies 2021 Higher Level.

One card per part, rows from the scheme's own groups. See cs_lib.py for why the
part and not the group is the card, and cs_scheme.py for how the two halves of
the scheme are read.

Topics are the syllabus sections in components/MarkBank/deck.ts. Where a
question spans several -- a vertical section runs from foundation to roof -- it
is filed under the element the SCHEME spends its marks on, not the first one the
question names.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2021, 'hl')

PLAN = [
    # (q, letter, topic, concept)
    (1, 'a', 'cons-3-2', 'vertical-section-door-external-wall-ground-floor'),
    (2, 'a', 'cons-1-8', 'duty-of-care-on-a-construction-site'),
    (2, 'b', 'cons-1-8', 'risks-in-chimney-roof-and-scaffold-work'),
    (2, 'c', 'cons-1-8', 'safety-procedures-that-eliminate-a-risk'),
    (3, 'a', 'cons-1-1', 'design-considerations-for-a-house'),
    (3, 'b', 'cons-1-1', 'designing-a-home-office-layout'),
    (3, 'c', 'cons-1-1', 'working-from-a-home-office'),
    (4, 'a', 'cons-1-3', 'factors-when-selecting-a-site'),
    (4, 'b', 'cons-1-3', 'choosing-between-two-rural-sites'),
    (4, 'c', 'cons-1-3', 'sketching-a-site-and-its-boundaries'),
    (6, 'a', 'cons-6-3', 'designing-for-low-environmental-impact'),
    (6, 'b', 'cons-6-3', 'reducing-operational-energy-use'),
    (6, 'c', 'cons-6-3', 'advantages-of-low-operational-energy-use'),
    (7, 'a', 'cons-3-10', 'vertical-section-chimney-stack-and-roof'),
    (7, 'b', 'cons-3-10', 'moisture-at-the-chimney-roof-junction'),
    (8, 'a', 'cons-5-3', 'heating-and-hot-water-layout'),
    (8, 'b', 'cons-5-3', 'features-that-make-a-heating-system-efficient'),
    (8, 'c', 'cons-5-3', 'air-to-water-heat-pump'),
    (9, 'a', 'cons-5-8', 'designing-a-socket-layout'),
    (9, 'b', 'cons-5-8', 'ring-main-circuit-wiring-layout'),
    (9, 'c', 'cons-1-9', 'renewable-energy-ratio'),
    (10, 'a', 'cons-6-4', 'why-solar-overheating-occurs'),
    (10, 'b', 'cons-6-4', 'reducing-solar-overheating'),
    (10, 'c', 'cons-6-4', 'design-features-for-thermal-comfort'),
    (1, 'b', 'cons-6-2', 'preventing-a-thermal-bridge-at-the-threshold'),
    (5, 'b', 'cons-6-1', 'insulation-thickness-for-a-target-u-value'),
    (5, 'c', 'cons-6-6', 'moisture-and-vapour-control-layers'),
]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2021-hl-q{q}-{letter}', topic=topic, concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
