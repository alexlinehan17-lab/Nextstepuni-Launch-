#!/usr/bin/env python3
"""Construction Studies 2023 Higher Level. See cs_2021_hl.py for the shape."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2023, 'hl')

PLAN = [
    (1, 'a', 'cons-3-8', 'vertical-section-roof-eaves-to-ridge'),
    (2, 'a', 'cons-1-8', 'maintaining-a-safe-working-environment'),
    (2, 'b', 'cons-1-8', 'best-practice-guidelines-on-site'),
    (2, 'c', 'cons-1-8', 'why-a-site-needs-a-safety-statement'),
    (3, 'a', 'cons-1-1', 'design-considerations-for-a-first-floor-living-area'),
    (3, 'b', 'cons-1-1', 'revised-internal-layout'),
    (3, 'c', 'cons-1-1', 'living-space-on-the-first-floor'),
    (4, 'a', 'cons-1-1', 'features-of-vernacular-irish-architecture'),
    (4, 'b', 'cons-1-2', 'refurbishing-an-old-cottage'),
    (4, 'c', 'cons-1-2', 'why-refurbish-traditional-cottages'),
    (6, 'a', 'cons-6-3', 'design-features-for-low-environmental-impact'),
    (6, 'b', 'cons-6-3', 'reducing-operational-energy-demand'),
    (6, 'c', 'cons-6-3', 'advantages-of-reducing-energy-demand'),
    (7, 'a', 'cons-3-2', 'vertical-section-door-external-wall-ground-floor'),
    (7, 'b', 'cons-3-4', 'preventing-moisture-at-the-threshold'),
    (8, 'a', 'cons-5-5', 'functional-requirements-of-wastewater-treatment'),
    (8, 'b', 'cons-5-5', 'installing-a-wastewater-treatment-system'),
    (8, 'c', 'cons-5-5', 'why-wastewater-must-be-treated'),
    (9, 'a', 'cons-3-6', 'functional-requirements-of-a-glazing-system'),
    (9, 'c', 'cons-3-6', 'advantages-and-disadvantages-of-triple-glazing'),
    (10, 'a', 'cons-6-3', 'passive-house-design'),
    (10, 'b', 'cons-6-3', 'designing-a-low-energy-ground-floor-plan'),
    (10, 'c', 'cons-6-3', 'where-to-locate-a-low-energy-feature'),
    (1, 'b', 'cons-6-5', 'ventilation-detailing-at-the-eaves'),
    (5, 'b', 'cons-6-1', 'calculating-heat-loss-through-a-roof'),
    (5, 'c', 'cons-6-2', 'best-practice-detailing-against-heat-loss'),
    (9, 'b', 'cons-8-2', 'reverberation-in-a-living-room'),
]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2023-hl-q{q}-{letter}', topic=topic, concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
