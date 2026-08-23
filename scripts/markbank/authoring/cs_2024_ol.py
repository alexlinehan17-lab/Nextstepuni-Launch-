#!/usr/bin/env python3
"""Construction Studies 2024 Ordinary Level. See cs_2021_hl.py for the shape."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2024, 'ol')

PLAN = [
    (1, 'b', 'cons-3-8', 'securing-a-wallplate-to-an-external-wall'),
    (2, 'a', 'cons-6-3', 'advantages-of-improving-a-ber'),
    (2, 'b', 'cons-6-2', 'applying-internal-insulation'),
    (2, 'c', 'cons-6-2', 'upgrading-walls-and-windows-together'),
    (3, 'a', 'cons-5-2', 'hot-and-cold-water-pipework'),
    (3, 'b', 'cons-5-6', 'an-accessible-shower-area'),
    (4, 'a', 'cons-3-3', 'a-natural-stone-finish-for-an-entrance-wall'),
    (4, 'b', 'cons-2-4', 'strip-foundation-detailing'),
    (5, 'a', 'cons-3-6', 'vertical-section-external-wall-and-window'),
    (6, 'a', 'cons-1-8', 'operating-a-site-dumper-safely'),
    (6, 'c', 'cons-1-8', 'why-vehicle-operators-are-trained'),
    (7, 'a', 'cons-1-1', 'converting-an-attic-to-a-bedroom'),
    (7, 'b', 'cons-1-1', 'laying-out-a-converted-attic'),
    (9, 'a', 'cons-3-3', 'zinc-as-a-cladding-material'),
    (9, 'b', 'cons-1-1', 'modifying-a-family-room'),
    (9, 'c', 'cons-1-1', 'access-from-a-family-room-to-the-garden'),
]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2024-ol-q{q}-{letter}', topic=topic, concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
