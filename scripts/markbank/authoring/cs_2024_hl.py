#!/usr/bin/env python3
"""Construction Studies 2024 Higher Level. See cs_2021_hl.py for the shape."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2024, 'hl')

PLAN = [
    (1, 'a', 'cons-3-2', 'vertical-section-entrance-porch'),
    (2, 'a', 'cons-1-8', 'best-practice-guidelines-on-site'),
    (2, 'b', 'cons-1-1', 'designing-an-accessible-en-suite'),
    (3, 'b', 'cons-1-1', 'external-design-for-a-renovated-forge'),
    (3, 'c', 'cons-1-1', 'respecting-irish-vernacular-architecture'),
    (4, 'a', 'cons-1-2', 'why-planning-authorities-regulate-design'),
    (4, 'b', 'cons-1-3', 'choosing-between-two-sites'),
    (4, 'c', 'cons-1-3', 'sketching-a-site-and-its-boundaries'),
    (5, 'c', 'cons-5-3', 'wood-pellet-heating-system'),
    (6, 'a', 'cons-6-3', 'design-features-for-low-environmental-impact'),
    (6, 'b', 'cons-6-3', 'features-that-further-reduce-energy-use'),
    (7, 'a', 'cons-4-3', 'vertical-section-external-wall-window-first-floor'),
    (7, 'b', 'cons-6-2', 'airtightness-at-the-first-floor-junction'),
    (8, 'a', 'cons-5-2', 'hot-water-and-heating-layout'),
    (8, 'b', 'cons-5-2', 'renewable-energy-for-hot-water'),
    (9, 'b', 'cons-8-3', 'reducing-sound-transmission-through-a-floor'),
    (9, 'c', 'cons-8-3', 'approaches-to-reducing-sound-transmission'),
    (10, 'a', 'cons-6-3', 'retrofitting-a-dwelling'),
    (10, 'b', 'cons-6-3', 'improvements-when-upgrading-a-dwelling'),
]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2024-hl-q{q}-{letter}', topic=topic, concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
