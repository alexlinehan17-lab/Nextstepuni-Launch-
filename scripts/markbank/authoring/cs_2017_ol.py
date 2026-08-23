#!/usr/bin/env python3
"""Construction Studies 2017 Ordinary Level.

Filed by cs_topics.py rather than by hand. Filing is a librarian's decision --
the question and the answer are lifted either way -- and one rule applied to
twenty papers is more consistent than a judgement made part by part across ten.
See cs_2021_hl.py for the card shape.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2017, 'ol')

PLAN = [
    (2, 'a', 'cons-1-1', 'how-inner-leaf-insulated-type-thickness'),
    (2, 'b', 'cons-1-1', 'list-advantages-insulating-inner-leaf-wall'),
    (3, 'a', 'cons-5-2', 'solar-panel-used-provide-hot-water'),
    (3, 'b', 'cons-5-2', 'advantages-solar-panel-provide-hot-water'),
    (4, 'b', 'cons-1-1', 'reasons-why-waste-should-kept-minimum'),
    (5, 'a', 'cons-1-5', 'vertical-section-through-external-wall-bottom'),
    (5, 'b', 'cons-6-2', 'typical-design-detailing-prevent-formation-cold'),
    (6, 'a', 'cons-1-8', 'reasons-why-safety-signs-must-displayed'),
    (6, 'b', 'cons-1-8', 'items-personal-protective-equipment-ppe-must'),
    (6, 'c', 'cons-1-8', 'specific-safety-precautions-should-observed-when'),
    (7, 'a', 'cons-1-1', 'method-preventing-floor-joists-from-twisting'),
    (7, 'c', 'cons-3-9', 'advantage-disadvantage-converting-attic-provide-additional'),
    (9, 'a', 'cons-1-1', 'how-fix-wooden-decking-joists-ensure'),
    (9, 'b', 'cons-1-1', 'recommend-applied-finish-preserve-external-decking'),
    (1, 'b', 'cons-3-4', 'clearly-how-prevent-penetration-rainwater-head'),
    (1, 'a', 'cons-1-5', 'vertical-section-through-top-door-showing'),
    (7, 'b', 'cons-1-1', 'large-tongue-groove-joint-between-flooring'),]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2017-ol-q{q}-{letter}', topic=topic,
               concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
