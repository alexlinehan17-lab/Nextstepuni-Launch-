#!/usr/bin/env python3
"""Construction Studies 2025 Ordinary Level. See cs_2021_hl.py for the shape."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2025, 'ol')

PLAN = [
    (1, 'b', 'cons-3-4', 'preventing-rainwater-at-the-window-head'),
    (2, 'a', 'cons-6-2', 'advantages-of-insulating-a-sloped-ceiling'),
    (2, 'b', 'cons-3-9', 'insulating-a-sloped-ceiling'),
    (2, 'c', 'cons-3-9', 'a-feature-for-a-sloped-ceiling'),
    (3, 'a', 'cons-5-3', 'pipework-for-a-heating-system'),
    (3, 'b', 'cons-5-3', 'advantages-of-a-zoned-heating-system'),
    (4, 'a', 'cons-1-3', 'choosing-between-two-sites'),
    (4, 'b', 'cons-1-3', 'laying-out-a-chosen-site'),
    (4, 'c', 'cons-1-3', 'building-a-house-in-the-countryside'),
    (5, 'a', 'cons-4-4', 'vertical-section-top-three-steps'),
    (6, 'b', 'cons-1-8', 'risks-when-working-at-height'),
    (6, 'c', 'cons-1-8', 'safety-measures-when-working-at-height'),
    (7, 'a', 'cons-3-3', 'timber-frame-for-a-garden-office'),
    (7, 'b', 'cons-1-1', 'laying-out-a-garden-office'),
    (7, 'c', 'cons-1-1', 'a-garden-office-separate-from-the-home'),
    (9, 'a', 'cons-1-1', 'creating-an-outdoor-dining-space'),
    (9, 'b', 'cons-1-1', 'modifying-the-rear-of-a-house'),
    (9, 'c', 'cons-1-1', 'family-uses-of-a-large-garden'),
    (1, 'a', 'cons-3-2', 'vertical-section-external-wall'),
    (5, 'b', 'cons-4-4', 'a-design-detail-for-a-safe-stairs'),
    (6, 'a', 'cons-1-8', 'safety-signs-on-a-construction-site'),
]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2025-ol-q{q}-{letter}', topic=topic, concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
