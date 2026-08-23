#!/usr/bin/env python3
"""Construction Studies 2023 Ordinary Level. See cs_2021_hl.py for the shape."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2023, 'ol')

PLAN = [
    (1, 'b', 'cons-3-3', 'connecting-the-inner-and-outer-leaves'),
    (2, 'a', 'cons-6-3', 'why-energy-upgrade-grants-exist'),
    (2, 'b', 'cons-6-2', 'applying-an-external-insulation-system'),
    (2, 'c', 'cons-6-3', 'other-energy-upgrades-for-an-old-house'),
    (3, 'a', 'cons-5-2', 'pipework-for-a-solar-installation'),
    (3, 'b', 'cons-6-4', 'where-to-locate-solar-panels'),
    (4, 'a', 'cons-3-8', 'advantages-of-prefabricated-trussed-rafters'),
    (4, 'b', 'cons-3-8', 'how-a-trussed-rafter-is-fixed'),
    (5, 'a', 'cons-3-10', 'vertical-section-wall-and-flat-roof-eaves'),
    (6, 'a', 'cons-9-4', 'safety-in-the-construction-studies-room'),
    (6, 'b', 'cons-9-4', 'safety-precautions-with-workshop-equipment'),
    (6, 'c', 'cons-9-1', 'why-a-workshop-is-kept-tidy'),
    (7, 'a', 'cons-1-1', 'advantages-of-a-large-utility-room'),
    (7, 'b', 'cons-1-1', 'laying-out-a-utility-room'),
    (9, 'a', 'cons-3-7', 'choosing-a-material-for-a-front-door'),
    (9, 'c', 'cons-1-1', 'an-accessible-front-entrance'),
    (1, 'a', 'cons-3-2', 'vertical-section-external-wall-and-floor'),
    (4, 'c', 'cons-3-9', 'choosing-a-roof-finish-material'),
    (5, 'b', 'cons-3-4', 'keeping-the-cavity-clear-of-mortar'),
    (7, 'c', 'cons-4-6', 'choosing-a-floor-covering-for-a-utility-room'),
    (9, 'b', 'cons-1-1', 'modifying-a-front-entrance'),
    (8, None, 'cons-1-5', 'construction-terms'),
]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2023-ol-q{q}-{letter}', topic=topic, concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
