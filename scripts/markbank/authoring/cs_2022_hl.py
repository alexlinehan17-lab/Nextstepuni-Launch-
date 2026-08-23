#!/usr/bin/env python3
"""Construction Studies 2022 Higher Level. See cs_2021_hl.py for the shape."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2022, 'hl')

PLAN = [
    (1, 'a', 'cons-3-10', 'vertical-section-external-wall-and-flat-roof'),
    (2, 'a', 'cons-1-1', 'designing-for-lifetime-use'),
    (2, 'b', 'cons-1-1', 'open-plan-kitchen-for-reduced-mobility'),
    (2, 'c', 'cons-1-1', 'why-provide-for-lifetime-use'),
    (3, 'a', 'cons-1-1', 'design-layout-for-an-extension'),
    (3, 'b', 'cons-1-1', 'reasons-for-a-proposed-layout'),
    (3, 'c', 'cons-1-1', 'vernacular-heritage-of-a-streetscape'),
    (4, 'a', 'cons-2-2', 'functional-requirements-of-a-foundation'),
    (4, 'b', 'cons-2-4', 'choosing-a-foundation-from-site-investigation'),
    (4, 'c', 'cons-2-2', 'advantages-and-disadvantages-of-foundation-types'),
    (6, 'a', 'cons-6-3', 'design-features-for-low-environmental-impact'),
    (6, 'b', 'cons-6-3', 'providing-for-low-environmental-impact'),
    (6, 'c', 'cons-6-5', 'design-for-health-and-wellbeing'),
    (7, 'a', 'cons-4-4', 'vertical-section-stairs-and-landing'),
    (7, 'b', 'cons-4-4', 'safety-details-on-a-landing'),
    (8, 'a', 'cons-5-2', 'installing-a-solar-collector'),
    (8, 'b', 'cons-5-2', 'solar-collector-layout'),
    (8, 'c', 'cons-5-2', 'advantages-and-disadvantages-of-a-solar-collector'),
    (9, 'a', 'cons-6-2', 'advantages-of-an-airtight-house'),
    (9, 'b', 'cons-6-2', 'airtightness-detailing-at-wall-and-roof'),
    (9, 'c', 'cons-6-2', 'testing-airtightness'),
    (10, 'a', 'cons-6-4', 'benefits-of-orientation'),
    (10, 'b', 'cons-6-4', 'choosing-an-orientation'),
    (10, 'c', 'cons-6-4', 'thermal-mass'),
    (1, 'b', 'cons-6-2', 'preventing-a-thermal-bridge'),
    (5, 'b', 'cons-6-1', 'calculating-heat-loss-through-a-wall'),
    (5, 'c', 'cons-6-1', 'upgrading-a-wall-to-a-target-u-value'),
]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2022-hl-q{q}-{letter}', topic=topic, concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
