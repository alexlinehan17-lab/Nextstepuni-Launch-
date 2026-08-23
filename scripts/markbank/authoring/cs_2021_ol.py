#!/usr/bin/env python3
"""Construction Studies 2021 Ordinary Level. See cs_2021_hl.py for the shape."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2021, 'ol')

PLAN = [
    (1, 'b', 'cons-5-4', 'rainwater-removal-at-the-eaves'),
    (2, 'a', 'cons-6-2', 'advantages-of-an-insulated-ground-floor'),
    (2, 'b', 'cons-4-2', 'insulating-a-solid-ground-floor'),
    (3, 'a', 'cons-5-2', 'cold-water-pipework-from-the-tank'),
    (3, 'b', 'cons-5-2', 'advantages-of-a-water-meter'),
    (4, 'a', 'cons-1-3', 'why-planning-permission-is-needed'),
    (4, 'b', 'cons-1-3', 'information-in-a-planning-application'),
    (5, 'a', 'cons-3-6', 'vertical-section-external-wall-and-window'),
    (6, 'b', 'cons-1-8', 'risks-when-working-in-a-deep-trench'),
    (6, 'c', 'cons-1-8', 'safety-precautions-in-a-deep-trench'),
    (7, 'a', 'cons-1-1', 'improving-a-kitchen-design'),
    (7, 'b', 'cons-1-1', 'laying-out-a-living-room'),
    (7, 'c', 'cons-5-7', 'a-wood-burning-stove-in-a-living-room'),
    (9, 'a', 'cons-4-6', 'an-applied-finish-for-decking'),
    (9, 'b', 'cons-1-1', 'using-an-outdoor-space-year-round'),
    (9, 'c', 'cons-1-1', 'advantages-of-an-outdoor-living-space'),
    (1, 'a', 'cons-3-9', 'vertical-section-external-wall-and-pitched-eaves'),
    (2, 'c', 'cons-4-2', 'choosing-a-floor-finish-for-a-kitchen'),
    (5, 'b', 'cons-3-6', 'preventing-water-entering-at-the-window-cill'),
    (6, 'a', 'cons-1-8', 'safety-signs-on-a-construction-site'),
    (8, None, 'cons-1-5', 'construction-terms'),
]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2021-ol-q{q}-{letter}', topic=topic, concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
