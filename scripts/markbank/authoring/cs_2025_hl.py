#!/usr/bin/env python3
"""Construction Studies 2025 Higher Level. See cs_2021_hl.py for the shape."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2025, 'hl')

PLAN = [
    (1, 'a', 'cons-3-2', 'vertical-section-external-wall-ground-floor-window'),
    (2, 'a', 'cons-1-8', 'maintaining-a-health-and-safety-culture'),
    (2, 'b', 'cons-1-8', 'risks-in-trench-attic-and-chimney-work'),
    (2, 'c', 'cons-1-8', 'guidelines-that-reduce-the-risk-of-injury'),
    (3, 'a', 'cons-1-1', 'revised-ground-floor-layout'),
    (3, 'b', 'cons-1-1', 'reasons-for-a-proposed-layout'),
    (3, 'c', 'cons-1-1', 'improving-the-external-appearance-of-a-garage'),
    (4, 'a', 'cons-3-3', 'functional-requirements-of-an-external-wall'),
    (4, 'b', 'cons-3-3', 'high-performance-external-wall-designs'),
    (4, 'c', 'cons-3-3', 'advantages-and-disadvantages-of-wall-types'),
    (6, 'a', 'cons-6-3', 'design-features-for-low-environmental-impact'),
    (6, 'b', 'cons-6-5', 'creating-a-healthy-indoor-environment'),
    (6, 'c', 'cons-6-3', 'benefits-of-locally-sourced-materials'),
    (7, 'a', 'cons-3-10', 'vertical-section-chimney-stack-and-roof'),
    (7, 'b', 'cons-3-10', 'rainwater-at-the-chimney-roof-junction'),
    (8, 'a', 'cons-6-2', 'benefits-of-preventing-air-leakage'),
    (8, 'b', 'cons-6-2', 'airtightness-detailing-in-a-block-wall-house'),
    (9, 'a', 'cons-5-8', 'wiring-layout-for-two-light-points'),
    (9, 'b', 'cons-5-8', 'safety-features-in-an-electrical-installation'),
    (9, 'c', 'cons-5-8', 'reducing-household-electricity-consumption'),
    (10, 'a', 'cons-6-3', 'passive-house-design'),
    (10, 'b', 'cons-6-4', 'choosing-an-orientation'),
    (10, 'c', 'cons-6-4', 'reducing-solar-overheating'),
    (1, 'b', 'cons-3-4', 'preventing-rainwater-penetration'),
    (5, 'c', 'cons-6-1', 'upgrading-a-wall-to-passive-house-standard'),
]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2025-hl-q{q}-{letter}', topic=topic, concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
