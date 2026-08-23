#!/usr/bin/env python3
"""Construction Studies 2022 Ordinary Level. See cs_2021_hl.py for the shape."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2022, 'ol')

PLAN = [
    (1, 'a', 'cons-3-4', 'vertical-section-wall-lintel-and-doorframe'),
    (2, 'a', 'cons-3-9', 'insulating-a-roof-at-ceiling-joist-level'),
    (2, 'b', 'cons-5-2', 'insulating-a-tank-and-pipework-in-an-attic'),
    (2, 'c', 'cons-6-2', 'advantages-of-insulating-an-attic'),
    (3, 'a', 'cons-5-4', 'an-underground-rainwater-storage-tank'),
    (3, 'b', 'cons-5-6', 'pipework-for-flushing-with-rainwater'),
    (3, 'c', 'cons-5-4', 'advantages-of-reusing-rainwater'),
    (4, 'a', 'cons-4-5', 'construction-of-a-stud-partition'),
    (4, 'c', 'cons-1-1', 'separating-a-living-room-from-a-kitchen'),
    (5, 'a', 'cons-4-4', 'vertical-section-bottom-three-steps'),
    (5, 'b', 'cons-4-4', 'preventing-a-stairs-from-creaking'),
    (6, 'b', 'cons-9-4', 'risks-when-using-power-tools'),
    (6, 'c', 'cons-9-4', 'safety-precautions-with-power-tools'),
    (7, 'a', 'cons-1-1', 'designing-a-garden-for-a-family'),
    (7, 'b', 'cons-1-1', 'laying-out-a-garden'),
    (7, 'c', 'cons-1-1', 'trees-and-plants-in-a-garden-design'),
    (9, 'a', 'cons-3-3', 'choosing-a-wood-for-external-cladding'),
    (9, 'b', 'cons-7-4', 'bringing-natural-light-into-a-porch'),
    (9, 'c', 'cons-1-1', 'why-build-a-front-porch'),
]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2022-ol-q{q}-{letter}', topic=topic, concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
